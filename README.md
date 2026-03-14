# Instagram Media Saver

A Python script that parses Instagram media JSON data, extracts useful metadata, and downloads images, videos, and carousel media into an organized folder structure.

## Features

- Supports **images**, **videos**, and **carousel posts**
- Extracts and saves:
  - Post ID
  - Product type
  - Owner username and full name
  - Caption text and translation (if available)
- Automatically downloads media files
- Organizes each post into its own folder (e.g., `media_1`, `media_2`)
- Handles network errors gracefully and infer file extensions (`.jpg`, `.png`, `.mp4`, `.webp`)

## Project Structure
```text
.
├── medias.json          # Input JSON file (Instagram media data)
├── main.py              # Main script
├── medias/              # Output directory (auto-generated)
│   ├── media_1/
│   │   ├── media.jpg
│   │   └── info.txt
│   ├── media_2/
│   │   ├── media_1.jpg
│   │   ├── media_2.mp4
│   │   └── info.txt
│   └── ...
├── requirements.txt     # Python dependencies
└── README.md
```

## Requirements

- Python 3.8+
- Internet connection

### Python Dependencies
Install the required packages using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

*(Standard library modules used: `json`, `pathlib`, `urllib.parse`)*

## Input Format

The script expects a file named `medias.json` in the same directory.
The JSON structure can be either:
1. A direct list of Instagram media objects.
2. A dictionary containing an `"items"` list (e.g., exported by some Instagram data scrapers).

**Supported `product_type` values:**
- `feed`
- `clips`
- `carousel_container`
- `ad`

### Example
```json
{
  "items": [
    {
      "media": {
        "id": "123",
        "product_type": "feed",
        "code": "ABCxyz",
        "owner": {
          "username": "example_user",
          "full_name": "Example Name"
        },
        "caption": {
          "text": "Hello world",
          "text_translation": "Bonjour le monde"
        },
        "image_versions2": {
          "candidates": [
            { "url": "https://example.com/image.jpg" }
          ]
        }
      }
    }
  ]
}
```

## How It Works

1. Loads and parses the media from `medias.json`.
2. Filters by supported media `product_type`.
3. Detects media type (Image, Video, or Carousel) and retrieves source URLs.
4. Extracts metadata (ID, owner, caption, etc.).
5. Creates an isolated folder for each post in the `medias/` directory.
6. Downloads the media files with inferred extensions.
7. Saves post information inside `info.txt`.

## Usage
```bash
python main.py
```

After execution, all downloaded content will be available inside the `medias/` directory.

## Output Example (`info.txt`)
```text
id: 123
product_type: feed
Owner: example_user (Example Name)
Caption: Hello world
Caption translate: Bonjour le monde
```

## Notes

- Carousel posts download multiple files (`media_1.jpg`, `media_2.mp4`, etc.).
- File extensions are inferred from the media URL (`.jpg`, `.png`, `.mp4`, `.webp`).
- If a media URL is missing or invalid, the script skips it safely and continues processing.
- The script gracefully handles missing metadata fields (e.g., if a post has no caption).

## Disclaimer

This project is for educational and personal use only.

**Make sure you comply with Instagram's Terms of Service and applicable laws when using this tool.**

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

---

**Made with ❤️ for personal archiving purposes**
