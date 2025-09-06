
---

````markdown
# LinkedIn Recent Activity Scraper

A Python-based CLI tool for scraping recent LinkedIn posts from public user profiles using Playwright and a headless Chromium browser.

---

## ⚙️ Features

- 🔒 Manual login flow using real browser session (storage persistence)
- 🧠 Human-like scrolling with jitter & idle detection
- 📥 Parses and saves recent activity (posts only) into structured JSON
- 📝 Configurable output paths for logs and scraped data
- ✅ Simple CLI interface via `typer`

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Login to LinkedIn

Before scraping, you **must authenticate** to persist your session cookies.

```bash
python -m main login
```

This will open a browser window. Log in manually to your LinkedIn account — cookies will be saved to `out/storage.json`.

---

### 3. Scrape recent posts

Run the scraper with a full LinkedIn profile URL:

```bash
python -m main scrape https://www.linkedin.com/in/yurii-zholtov
```

> ✅ Parsed posts will be saved to `out/li_posts.json`
> 📄 Logs will be written to `out/run.log`

---

## 🛠 Configuration

Edit `src/session/config.py` to change default output paths:

```python
from pathlib import Path

URL_FOR_LOGIN = "https://www.linkedin.com/login"

FILE_FOR_RESULTS = Path("out/li_posts.json")  # <- Change this path if needed
FILE_FOR_LOGS = Path("out/run.log")           # <- Log file output
```

---

## 📁 Project Structure

```
src/
├── cli/              # CLI entry points (Typer commands)
├── loginflow/        # Manual login logic (Playwright session storage)
├── parser/           # Helpers for formatting post data
├── person/           # Main object representing a LinkedIn user
├── scraper/          # Core scraping logic
├── session/          # Storage, config, and session management
├── out/              # Output files (results, logs, session cookies)
└── main.py           # CLI runner for login / scrape
```

---

## 🧪 Example Output

Sample JSON result:

```json
[
  {
    "timestamp": "2025-09-06T14:32:45",
    "content": "Excited to announce our new project in AI infrastructure...",
    "likes": 123,
    "comments": 45,
    "url": "https://linkedin.com/posts/example"
  },
  ...
]
```

---

## 🧾 License

MIT License. Educational & research use only. Respect LinkedIn’s Terms of Service.

---

## 🤖 Author

Built with ❤️ by [Yurii Zholtov](https://www.linkedin.com/in/yurii-zholtov)
Telegram: [@yuriy_akzy](https://t.me/yuriy_akzy)

```
