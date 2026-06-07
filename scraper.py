import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

WEBSITES = [
    {"company": "Transporeon", "url": "https://www.transporeon.com"},
    {"company": "Sennder", "url": "https://www.sennder.com"},
    {"company": "Cargonexx", "url": "https://www.cargonexx.com"},
    {"company": "FreightWaves", "url": "https://www.freightwaves.com"},
]


def scrape_websites(urls):
    results = []

    for site in urls:
        site_data = {"company": site["company"], "url": site["url"]}

        try:
            response = requests.get(site["url"], headers=HEADERS, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            site_data["error"] = str(e)
            results.append(site_data)
            continue

        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            site_data["error"] = f"Parsing failed: {e}"
            results.append(site_data)
            continue

        # Title
        title_tag = soup.find("title")
        site_data["title"] = title_tag.get_text(strip=True) if title_tag else None

        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        site_data["meta_description"] = (
            meta_desc.get("content", "").strip() if meta_desc else None
        )

        # H1 tags
        h1_tags = soup.find_all("h1")
        site_data["h1"] = [h.get_text(strip=True) for h in h1_tags] if h1_tags else []

        # H2 tags
        h2_tags = soup.find_all("h2")
        site_data["h2"] = [h.get_text(strip=True) for h in h2_tags] if h2_tags else []

        results.append(site_data)

    return results


def print_results(results):
    for site in results:
        print("=" * 70)
        print(f"Company: {site['company']}")
        print(f"URL: {site['url']}")

        if "error" in site:
            print(f"  ERROR: {site['error']}")
            continue

        print(f"  Title:            {site.get('title') or '(not found)'}")
        print(f"  Meta Description: {site.get('meta_description') or '(not found)'}")

        h1_list = site.get("h1", [])
        if h1_list:
            print(f"  H1 ({len(h1_list)}):")
            for text in h1_list:
                print(f"    - {text}")
        else:
            print("  H1: (not found)")

        h2_list = site.get("h2", [])
        if h2_list:
            print(f"  H2 ({len(h2_list)}):")
            for text in h2_list[:10]:
                print(f"    - {text}")
            if len(h2_list) > 10:
                print(f"    ... and {len(h2_list) - 10} more")
        else:
            print("  H2: (not found)")

    print("=" * 70)


if __name__ == "__main__":
    data = scrape_websites(WEBSITES)
    print_results(data)
