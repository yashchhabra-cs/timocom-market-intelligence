import os
import json
from dotenv import load_dotenv
import anthropic

SYSTEM_PROMPT = """You are a senior market analyst specialising in logistics, freight, and transportation technology.

You will receive scraped web data for one company at a time. Analyse the data and return your response as a valid JSON object with exactly these four keys:

{
  "summary": "A concise 2-3 sentence overview of what the company does and its market position.",
  "key_insights": ["insight 1", "insight 2", "..."],
  "trends": ["trend 1", "trend 2", "..."],
  "recommendations": ["recommendation 1", "recommendation 2", "..."]
}

Rules:
- Return only the JSON object. No markdown, no code fences, no extra text.
- Base your analysis strictly on the data provided.
- Be factual, professional, and specific."""


def load_api_key():
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not found. Make sure it is set in your .env file."
        )
    return api_key


def build_client(api_key):
    try:
        client = anthropic.Anthropic(api_key=api_key)
        return client
    except Exception as e:
        raise ConnectionError(f"Failed to initialise Anthropic client: {e}")


def build_prompt(site_data):
    lines = [
        f"Company: {site_data.get('company', 'Unknown')}",
        f"URL: {site_data.get('url', '')}",
        f"Page Title: {site_data.get('title') or '(not found)'}",
        f"Meta Description: {site_data.get('meta_description') or '(not found)'}",
    ]

    h1_list = site_data.get("h1", [])
    if h1_list:
        lines.append("H1 Headings:")
        for h in h1_list:
            lines.append(f"  - {h}")
    else:
        lines.append("H1 Headings: (not found)")

    h2_list = site_data.get("h2", [])
    if h2_list:
        lines.append("H2 Headings:")
        for h in h2_list:
            lines.append(f"  - {h}")
    else:
        lines.append("H2 Headings: (not found)")

    return "\n".join(lines)


def analyse_company(client, site_data):
    company = site_data.get("company", "Unknown")

    if "error" in site_data:
        return {"error": f"Skipped — scrape failed: {site_data['error']}"}

    prompt = build_prompt(site_data)

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Here is the scraped web data for {company}. "
                        "Analyse it and return the JSON response.\n\n"
                        + prompt
                    ),
                }
            ],
        )
        raw = message.content[0].text.strip()

    except anthropic.APIConnectionError as e:
        raise ConnectionError(f"Network error while contacting Claude API: {e}")
    except anthropic.AuthenticationError as e:
        raise PermissionError(f"Authentication failed — check your API key: {e}")
    except anthropic.RateLimitError as e:
        raise RuntimeError(f"Rate limit hit for {company}: {e}")
    except anthropic.APIStatusError as e:
        raise RuntimeError(
            f"Claude API returned an error for {company}: {e.status_code} — {e.message}"
        )
    except Exception as e:
        raise RuntimeError(f"Unexpected error calling Claude for {company}: {e}")

    try:
        analysis = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Claude response for {company} was not valid JSON: {e}\nRaw response:\n{raw}"
        )

    return analysis


def process_results(scraped_data):
    try:
        api_key = load_api_key()
    except EnvironmentError as e:
        print(f"[CONFIG ERROR] {e}")
        return []

    try:
        client = build_client(api_key)
    except ConnectionError as e:
        print(f"[CONNECTION ERROR] {e}")
        return []

    results = []

    for site_data in scraped_data:
        company = site_data.get("company", "Unknown")
        print(f"Analysing {company}...")

        company_result = {
            "company": company,
            "url": site_data.get("url", ""),
        }

        try:
            analysis = analyse_company(client, site_data)
            company_result["analysis"] = analysis
        except (ConnectionError, PermissionError) as e:
            print(f"  [FATAL] {e}")
            company_result["analysis"] = {"error": str(e)}
            results.append(company_result)
            break
        except (RuntimeError, ValueError) as e:
            print(f"  [ERROR] {e}")
            company_result["analysis"] = {"error": str(e)}

        results.append(company_result)

    return results


def print_analysis(results):
    for company_result in results:
        print("\n" + "=" * 70)
        print(f"Company : {company_result.get('company', 'Unknown')}")
        print(f"URL     : {company_result.get('url', '')}")
        print("-" * 70)

        analysis = company_result.get("analysis", {})

        if "error" in analysis:
            print(f"  ERROR: {analysis['error']}")
            continue

        print(f"\nSUMMARY\n{analysis.get('summary', '(not available)')}")

        key_insights = analysis.get("key_insights", [])
        if key_insights:
            print("\nKEY INSIGHTS")
            for item in key_insights:
                print(f"  - {item}")

        trends = analysis.get("trends", [])
        if trends:
            print("\nTRENDS")
            for item in trends:
                print(f"  - {item}")

        recommendations = analysis.get("recommendations", [])
        if recommendations:
            print("\nRECOMMENDATIONS")
            for item in recommendations:
                print(f"  - {item}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    from scraper import scrape_websites, WEBSITES

    scraped_data = scrape_websites(WEBSITES)
    results = process_results(scraped_data)

    print_analysis(results)

    print("\nFull results as list of dictionaries:")
    print(json.dumps(results, indent=2))
