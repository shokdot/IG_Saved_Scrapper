import json
from pathlib import Path
import requests
from urllib.parse import urlparse

filtered_data = []
medias_dir = Path("medias")

def collect_generic_data(media):
      owner = media.get("owner", {})
      caption = media.get("caption", {})

      return {
		"id": media.get("id"),
        "product_type": media.get("product_type"),
        "code": media.get("code"),
        "owner": (
              {
				  "full_name": owner.get("full_name", None),
				  "username": owner.get("username", None),
			  }
			  if isinstance(owner, dict)
			  else None
		),
        "caption": (
			  {
				  "text": caption.get("text", None),
				  "text_translation": caption.get("text_translation", None),
			  }
			  if isinstance(caption, dict)
			  else None
		),
		# "post_url": f"https://www.instagram.com/{owner.get('username')}/p/{media.get('code')}/"
	  }

def get_media_type(media):
    if media.get("video_versions"):
        return "video"
    elif media.get("carousel_media"):
        return "carousel"
    else:
        return "image"

def retrive_carousel_url(media):
    carousel = media.get("carousel_media")
    url = []
    for item in carousel:
        item["media_type"] = get_media_type(item)
        item["src_url"] = retrive_media_url(item)
        url.append(item["src_url"])
    return url

def retrive_media_url(media):
    if get_media_type(media) == "video":
        return media.get("video_versions")[0].get("url")
    elif get_media_type(media) == "image":
        return media.get("image_versions2").get("candidates")[0].get("url")
    elif get_media_type(media) == "carousel":
        return retrive_carousel_url(media)
    else:
        print("Unknown media type for feed.")
        return None

def process_resource(media):
    processed_clips = collect_generic_data(media)
    processed_clips["media_type"] = get_media_type(media)
    processed_clips["src_url"] = retrive_media_url(media)
    filtered_data.append(processed_clips)

def organize_media(filtered, i):
    owner = filtered.get("owner", {})
    caption_data = filtered.get("caption", {})

    post_id = filtered.get("id", "unknown")
    product_type = filtered.get("product_type", "unknown")
    username = owner.get("username", "unknown")
    full_name = owner.get("full_name", "unknown")
    if caption_data is not None:
        caption_text = caption_data.get("text", "")
        caption_translation = caption_data.get("text_translation", "")
    else:
        caption_text = ""
        caption_translation = ""

    media_folder = medias_dir / f"media_{i+1}"
    media_folder.mkdir(exist_ok=True)
    txt_file = media_folder / "info.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"id: {post_id}\n")
        f.write(f"product_type: {product_type}\n")
        f.write(f"Owner: {username} ({full_name})\n")
        f.write(f"Caption: {caption_text}\n")
        if caption_translation:
            f.write(f"Caption translate: {caption_translation}\n")

def download_media(url, dest_folder):
    """
    Download media files from URL(s) to the destination folder.
    Handles single URLs (images/videos) and lists of URLs (carousels).
    """
    if url is None:
        print(f"No URL provided for {dest_folder}")
        return
    
    # Handle carousel (list of URLs)
    if isinstance(url, list):
        for idx, media_url in enumerate(url, start=1):
            download_single_file(media_url, dest_folder, idx)
    # Handle single URL (image or video)
    else:
        download_single_file(url, dest_folder)

def download_single_file(url, dest_folder, index=None):
    """
    Download a single file from URL to destination folder.
    """
    try:
        # Parse URL to get file extension
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        # Determine file extension from URL
        if '.jpg' in path or '.jpeg' in path:
            ext = '.jpg'
        elif '.png' in path:
            ext = '.png'
        elif '.mp4' in path:
            ext = '.mp4'
        elif '.webp' in path:
            ext = '.webp'
        else:
            # Default to .jpg for images, .mp4 for videos
            ext = '.mp4' if 'video' in url else '.jpg'
        
        # Create filename
        if index is not None:
            filename = f"media_{index}{ext}"
        else:
            filename = f"media{ext}"
        
        filepath = dest_folder / filename
        
        # Download the file
        print(f"Downloading: {filename}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Write to file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ Saved: {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to download {url}: {e}")
    except Exception as e:
        print(f"✗ Error saving file: {e}")

def main():
    with open("medias.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        

    product_types = ('ad', 'feed', 'carousel_container', 'clips')

    for media in data:
        if media['product_type'] in product_types:
            process_resource(media)
        else:
            print(f"Unknown product_type: {media['product_type']}")

    
    medias_dir.mkdir(exist_ok=True)

    for i, filtered in enumerate(filtered_data):
        organize_media(filtered, i)
        download_media(filtered["src_url"], medias_dir / f"media_{i+1}")

if __name__ == "__main__":
    main()
