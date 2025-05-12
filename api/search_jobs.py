import requests
from bs4 import BeautifulSoup

def handler(request):
    query = request.query.get("query", "AI Engineer")
    url = f"https://remoteok.com/remote-{query.lower().replace(' ', '-')}-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    jobs = []
    for div in soup.find_all("tr", class_="job")[:10]:
        title_tag = div.find("h2")
        link_tag = div.find("a", href=True)
        if title_tag and link_tag:
            jobs.append({
                "title": title_tag.text.strip(),
                "link": "https://remoteok.com" + link_tag["href"]
            })
    return {"jobs": jobs}
