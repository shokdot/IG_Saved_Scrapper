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
- Organizes each post into its own folder
- Handles network errors gracefully

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
└── README.md
```

## Requirements

- Python 3.8+
- Internet connection

### Python Dependencies
```bash
pip install requests
```

*(Standard library modules used: `json`, `pathlib`, `urllib.parse`)*

## Input Format

The script expects a file named `medias.json` containing a list of Instagram media objects.

**Supported `product_type` values:**
- `feed`
- `clips`
- `carousel_container`
- `ad`

### Example (simplified)
```json
[
  {
    "id": "123",
    "product_type": "feed",
    "code": "ABCxyz",
    "owner": {
      "username": "example_user",
      "full_name": "Example Name"
    },
    "caption": {
      "text": "Hello world",
      "text_translation": null
    },
    "image_versions2": {
      "candidates": [
        { "url": "https://example.com/image.jpg" }
      ]
    }
  }
]
```

## How It Works

1. Loads and filters media from `medias.json`
2. Detects media type:
   - Image
   - Video
   - Carousel
3. Extracts metadata
4. Creates a folder for each post
5. Downloads media files
6. Saves post information in `info.txt`

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
```

## Notes

- Carousel posts download multiple files (`media_1.jpg`, `media_2.mp4`, etc.)
- File extensions are inferred from the media URL
- If a media URL is missing or invalid, the script skips it safely

## Disclaimer

This project is for educational and personal use only.

**Make sure you comply with Instagram's Terms of Service and applicable laws when using this tool.**

## License

[MIT License](LICENSE) *(or specify your preferred license)*

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

---

**Made with ❤️ for personal archiving purposes**
