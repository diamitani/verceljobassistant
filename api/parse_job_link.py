import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def handler(request):
    url = request.query.get("url")
    if not url:
        return {"error": "Missing 'url' parameter"}

    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.find("h1") or soup.find("h2")
    description = (
        soup.find("div", class_="description")
        or soup.find("div", class_="job-description")
        or soup.find("article")
    )

    return {
        "title": title.get_text(strip=True) if title else "N/A",
        "description": description.get_text(strip=True)[:1000] if description else "N/A",
        "source": urlparse(url).netloc,
        "link": url
    }
