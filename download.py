from dotenv import load_dotenv
import json
import os
import time
import requests

def download_json():
    load_dotenv()

    try:
        SESSION_ID = os.getenv("SESSION_ID")
        CSRF_TOKEN = os.getenv("CSRF_TOKEN")
        USER_ID = os.getenv("USER_ID")
        USER_AGENT = os.getenv("USER_AGENT")

        if not all([SESSION_ID, CSRF_TOKEN, USER_ID, USER_AGENT]):
            raise ValueError("Missing required environment variables")

    except ValueError as e:
        print("Please setup envoriment")
        raise e

    session = requests.Session()

    session.cookies.set("sessionid", SESSION_ID, domain=".instagram.com")
    session.cookies.set("csrftoken", CSRF_TOKEN, domain=".instagram.com")
    session.cookies.set("ds_user_id", USER_ID, domain=".instagram.com")

    headers = {
        "User-Agent": USER_AGENT,
        "X-CSRFToken": CSRF_TOKEN,
        "X-IG-App-ID": "936619743392459",
        "Referer": "https://www.instagram.com/",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }

    target_url = "https://www.instagram.com/api/v1/feed/saved/posts/"

    max_id = None
    all_posts = []
    more_available = True
    page_count = 1

    print("Starting to fetch saved posts...")

    while more_available:
        params = {}
        if max_id:
            params["max_id"] = max_id

        response = session.get(target_url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                items = data.get("items", [])
                all_posts.extend(items)
                print(f"Successfully fetched page {page_count} JSON data!")

                more_available = data.get("more_available", False)
                max_id = data.get("next_max_id")

                page_count += 1
                time.sleep(2)

            except ValueError:
                print("Response was not JSON. Content received:")
                print(response.text[:500])
                break
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            break

        output_data = {"items": all_posts, "num_results": len(all_posts), "status" : "ok"}

    with open("medias.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(
        f"Done! Saved a total of {output_data['num_results']} items to 'medias.json'."
    )


if __name__ == "__main__":
    print("Please run main.py")
