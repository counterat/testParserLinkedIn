import asyncio
from pathlib import Path
from typing import Optional
import typer
from config import FILE_FOR_RESULTS
from loginflow.login import login_and_save
from person.person import Person 

app = typer.Typer(add_completion=False, help="LinkedIn Recent Posts Extractor")

def run(coro):
    return asyncio.run(coro)

@app.command(help="Open a real browser, login to LinkedIn, and save storage.json")
def login():

    run(login_and_save())
    typer.echo(f"✅ Storage saved")
    
@app.command(help="Scrape 'Recent activity → Posts' for a given profile")
def scrape(
    profile_url: str = typer.Argument(..., help="LinkedIn profile URL, e.g. https://www.linkedin.com/in/xxx/"),
    min_posts: int = typer.Option(10, "--min-posts", min=1, help="Minimum posts to load"),
    max_posts: int = typer.Option(50, "--max-posts", min=1, help="Hard cap to stop scrolling"),
    timeout: int = typer.Option(60, "--timeout", help="Global scroll timeout (sec)"),
):

    person = Person(profile_url)
    run(person.parse_section(min_posts=min_posts, max_posts=max_posts, timeout=timeout))
    typer.echo(f"✅ Scraped posts from {profile_url}")
    typer.echo(f"💾 Saved to {FILE_FOR_RESULTS}")



