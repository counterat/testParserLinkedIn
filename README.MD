
---


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
{
  "profile_url": "https://www.linkedin.com/in/yurii-zholtov",
  "posts_count": 30,
  "created_at": "2025-09-06T21:21:33.149565",
  "posts": [
    {
      "post_id": "urn:li:activity:7366789478570549248",
      "author_name": "Aleksandr S.",
      "author_name_of_commented_content": "",
      "posted_at": "2025-08-16T18:21:32.212615+00:00",
      "text": "\n        ❗ Cписок Telegram-каналов, на которые должен быть подписан каждый из индустрии iGaming➡️t.me/igaming_inside (iGaming Insides) — Данный канал старается собрать из различных источников всё самое важное из индустрии iGaming (аналитика и просто полезная информация от экспертов iGaming-индустрии, исследования и обзоры по различным ГЕО, а так же главные новости и инсайды).➡️https://t.me/igamingcpo (Igaming CPO) — канал с разборами Igaming продуктов (реальные кейсы / Аналитика / CRO / CRM / Retention / Bonus management / UX&UI / Product&Game management). Рекомендуем подписаться каждому, кто работает в iGaming индустрии (причем не важно на какой позиции). Уверен, что каждый сможет найти что-то полезное для себя. Так же хочу отметить LinkedIn владельца данного канала (Vladimir KH) — в нем на постоянной основе выходит много полезных рассуждений и информации, которую так же не стоит упускать.➡️https://t.me/iGaming_CMO (iGaming CMO) — канал будет полезен для маркетологов из сферы Gambling / iGaming / Betting. Канал ведет человек с большим опытом работы в performance и full-funnel маркетинге. Так же рекомендуем подписаться на его LinkedIn (Александр З.) в котором он так же публикует много полезной информации и просто интересных постов.➡️https://t.me/gamblnews (Gambla4) — новостной канал, который уже несколько лет публикует новости гемблинг индустрии. Новости выходят в коротком формате и всегда есть ссылка на первоисточник.➡️https://t.me/igaming_news (iGN) — еще один новостной канал, но посты выходят в развернутом виде с выделением ключевых данных и цифр. Помимо всего редакция берет много интервью с конференций и ведет свой Youtube канал (https://lnkd.in/eefirrfE).➡️https://t.me/reg2bet (R2B.Nеws) — скорее всего не нуждаются в представлении, т.к. думаю все кто читает данный пост уже подписаны на них. Если в двух словах, то деловое B2B медиа (интервью, аналитические материалы, новости индустрии). У них кстати так же есть LinkedIn, поэтому на него так же рекомендуем подписаться (R2B.Work)➡️https://t.me/wager_3 (Wager 3.0) — канал рассказывает о гемблинге на стыке Web3 и Telegram, недавно на канале стали выходить интервью с владельцами различных гемблинговых telegram-канлов. Определенно интересный канал.➡️https://t.me/igamingceo (iGaming CEO) — цифры, аналитика, Growth Hack, инсайды о гемблинг-индустрии. Автор канала делится результатами тестирования различных теорий, проводимых на собственных продуктах, а также обзорами различных гео. Стоит подписаться.➡️https://lnkd.in/e3zRDBHr (The Gambler) — на постоянной основе в канале публикуются топы брендов в самых актуальных гео, обзоры различных рынков, обзоры топовых креативов в разных гео, разборы маркетинговых стратегий топовых iGaming-брендов и их динамики роста. ➡️https://lnkd.in/etFd3HcB (BRAZINO777 INSIDER) — канал Brazino777, бренда с локальной лицензией в Бразилии. В канале много инсадов по бразильскому рынку. Будет интересен всем, кто работает с этим гео.\n      ",
      "hashtags": [],
      "links": [
        "http://t.me/igaming_inside",
        "https://t.me/igamingcpo",
        "https://t.me/iGaming_CMO",
        "https://t.me/gamblnews",
        "https://t.me/igaming_news",
        "https://lnkd.in/eefirrfE",
        "https://t.me/reg2bet",
        "https://t.me/wager_3",
        "https://t.me/igamingceo",
        "https://lnkd.in/e3zRDBHr",
        "https://lnkd.in/etFd3HcB"
      ],
      "reposts_count": 12,
      "comments_count": 22
    }
  ]
}
```

---

## 🧾 License

MIT License. Educational & research use only. Respect LinkedIn’s Terms of Service.

---

## 🤖 Author

Built with ❤️ by [Yurii Zholtov](https://www.linkedin.com/in/yurii-zholtov)
Telegram: [@yuriy_akzy](https://t.me/yuriy_akzy)

```
