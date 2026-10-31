# Instagram Saved Posts Scraper

A Python tool that **fetches your Instagram saved posts** via the private Instagram API and **downloads all media** (images, videos, and carousels) into an organized local folder structure.

## Features

- 🔐 Authenticates using your Instagram session credentials (no password required)
- 📥 Fetches **all saved posts** with automatic pagination
- 🖼️ Downloads **images**, 🎬 **videos**, and 🗂️ **carousel posts**
- 📄 Saves post metadata to `info.txt` per post (ID, owner, caption, translation)
- 🗂️ Organizes each post into its own numbered folder (`media_1/`, `media_2/`, …)
- 🔁 Handles network errors gracefully and infers file extensions (`.jpg`, `.png`, `.mp4`, `.webp`)
- 📄 Caches raw API response to `medias.json` for re-processing without re-fetching

## How It Works

The tool runs in two sequential phases:

1. **Fetch** (`download.py`) — Authenticates with Instagram, paginates through your saved posts, and writes all raw JSON data to `medias.json`.
2. **Process & Download** (`main.py`) — Parses `medias.json`, extracts metadata, and downloads each media file.

Both phases are triggered automatically by running `main.py`.

## Project Structure

```text
.
├── main.py              # Entry point — orchestrates fetch + download
├── download.py          # Fetches saved posts from Instagram API → medias.json
├── medias.json          # Auto-generated: raw Instagram API response cache
├── medias/              # Auto-generated: output directory
│   ├── media_1/
│   │   ├── media.jpg
│   │   └── info.txt
│   ├── media_2/
│   │   ├── media_1.jpg
│   │   ├── media_2.mp4
│   │   └── info.txt
│   └── ...
├── .env                 # Your credentials (not committed — see .env.example)
├── .env.example         # Credential template
├── requirements.txt     # Python dependencies
└── README.md
```

## Requirements

- Python 3.8+
- An active Instagram account with saved posts
- Your Instagram session credentials (see [Setup](#setup))

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**

| Package | Purpose |
|---|---|
| `requests` | HTTP requests to the Instagram API |
| `python-dotenv` | Loads credentials from `.env` |
| `certifi`, `charset-normalizer`, `idna`, `urllib3` | Supporting HTTP/SSL libraries |

### 2. Configure Credentials

Copy `.env.example` to `.env` and fill in your Instagram session values:

```bash
cp .env.example .env
```

```env
SESSION_ID = "your_session_id"
CSRF_TOKEN = "your_csrf_token"
USER_ID    = "your_numeric_user_id"
USER_AGENT = "your_browser_user_agent"
```

#### How to get your credentials

1. Open **Instagram** in your browser and log in.
2. Open **Developer Tools** (`F12`) → **Application** tab → **Cookies** → `https://www.instagram.com`.
3. Copy the values for:
   - `sessionid` → `SESSION_ID`
   - `csrftoken` → `CSRF_TOKEN`
   - `ds_user_id` → `USER_ID`
4. For `USER_AGENT`, go to **Console** and run:
   ```js
   navigator.userAgent
   ```

> **⚠️ Keep your `.env` file private.** Never commit it to version control. It is already listed in `.gitignore`.

## Usage

```bash
python main.py
```

The script will:
1. Connect to the Instagram API and fetch all your saved posts (paginated, with a 2-second delay between pages).
2. Save the raw data to `medias.json`.
3. Parse each post, create a numbered folder under `medias/`, and download all media files.

### Re-processing without re-fetching

If you already have a `medias.json` and only want to re-download or re-parse, you can call `main()` directly:

```python
# In a Python shell or a custom script
from main import main
main()
```

## Supported Media Types

| `product_type` | Description |
|---|---|
| `feed` | Standard photo or video post |
| `clips` | Instagram Reel |
| `carousel_container` | Carousel (multiple images/videos) |
| `ad` | Sponsored post |

## Output

### Folder structure

Each post gets its own numbered folder:

```
medias/
├── media_1/        # Single image post
│   ├── media.jpg
│   └── info.txt
├── media_2/        # Carousel post
│   ├── media_1.jpg
│   ├── media_2.mp4
│   └── info.txt
└── media_3/        # Video post
    ├── media.mp4
    └── info.txt
```

### `info.txt` format

```text
id: 3012345678901234567
product_type: feed
Owner: example_user (Example Full Name)
Caption: Hello world 🌍
Caption translate: Bonjour le monde 🌍
```

> `Caption translate` is only written when a translation is available.

## Input JSON Format (Advanced)

The parser accepts `medias.json` in either of these shapes:

**Dict with `items` key** (default output from `download.py`):
```json
{
  "items": [
    { "media": { "id": "123", "product_type": "feed", ... } }
  ]
}
```

**Bare list** (e.g., from a third-party exporter):
```json
[
  { "id": "123", "product_type": "feed", ... }
]
```

## Notes

- The script adds a **2-second delay** between API pages to reduce the risk of rate limiting.
- File extensions are inferred from the media URL. If none can be determined, `.jpg` is used for images and `.mp4` for videos.
- Missing metadata fields (caption, translation, owner name) are handled gracefully — the script continues without crashing.
- Carousel posts produce multiple numbered files: `media_1.jpg`, `media_2.mp4`, etc.

## Disclaimer

This project is intended for **personal and educational use only**.

Use this tool only to download your **own saved posts**. Always comply with [Instagram's Terms of Service](https://help.instagram.com/581066165581870) and all applicable laws. The author is not responsible for any misuse.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an [issue](../../issues) or submit a pull request.

---

**Made with ❤️ for personal archiving purposes**
