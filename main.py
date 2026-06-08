from scraper import scrape_websites, WEBSITES
from processor import process_results
from excel_output import save_to_excel
from pdf_output import save_to_pdf


def main():
    # Step 1 — Scrape
    print("Scraping websites...")
    try:
        scraped_data = scrape_websites(WEBSITES)
    except Exception as e:
        print(f"[ERROR] Scraper failed unexpectedly: {e}")
        return

    if not scraped_data:
        print("[ERROR] Scraper returned no data. Stopping.")
        return

    print(f"  Scraped {len(scraped_data)} website(s).\n")

    # Step 2 — Analyse with Claude
    print("Analysing with Claude API...")
    try:
        results = process_results(scraped_data)
    except Exception as e:
        print(f"[ERROR] Processor failed unexpectedly: {e}")
        return

    if not results:
        print("[ERROR] Processor returned no results. Stopping.")
        return

    print(f"  Analysis complete for {len(results)} company/companies.\n")

    # Step 3 — Excel
    print("Creating Excel file...")
    try:
        save_to_excel(results)
    except Exception as e:
        print(f"[ERROR] Excel output failed: {e}")

    print()

    # Step 4 — PDF
    print("Creating PDF report...")
    try:
        save_to_pdf(results)
    except Exception as e:
        print(f"[ERROR] PDF output failed: {e}")

    print("\nAll done!")


if __name__ == "__main__":
    main()
