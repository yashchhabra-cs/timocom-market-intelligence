# TIMOCOM Market Intelligence Tool

Built as part of the TIMOCOM interview project — an end-to-end market intelligence pipeline that scrapes competitor websites, analyses them using the Claude AI API, and exports structured reports as both Excel and PDF.

---

## What It Does

1. **Scrapes** the homepages of target logistics/freight companies (Transporeon, Sennder, Cargonexx, FreightWaves) — extracting page titles, meta descriptions, and H1/H2 headings.
2. **Analyses** each company's scraped data one by one using the Claude API, acting as a senior market analyst to produce structured insights.
3. **Exports** the analysis into two report formats saved to the `output/` folder:
   - `market_intelligence.xlsx` — a styled Excel file with one row per company
   - `market_intelligence_report.pdf` — a formatted PDF report with sections per company

---

## Tech Stack

| Component | Library |
|---|---|
| Web scraping | `requests`, `BeautifulSoup4` |
| AI analysis | `anthropic` (Claude API) |
| Excel output | `openpyxl` |
| PDF output | `ReportLab` |
| Environment config | `python-dotenv` |
| Language | Python 3 |

---

## Project Structure

```
timocom-market-intelligence/
├── scraper.py        # Scrapes target websites
├── processor.py      # Sends scraped data to Claude API and returns analysis
├── excel_output.py   # Generates styled Excel report
├── pdf_output.py     # Generates formatted PDF report
├── main.py           # Orchestrates the full pipeline
├── requirements.txt  # Python dependencies
├── .env              # API keys (not committed to version control)
└── output/           # Generated reports saved here
```

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yashchhabra-cs/timocom-market-intelligence.git
   cd timocom-market-intelligence
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

4. Run the pipeline:
   ```bash
   python3 main.py
   ```

---

## Output

Both files are saved to the `output/` folder (created automatically if it doesn't exist):

- **Excel** (`market_intelligence.xlsx`) — columns: Company, URL, Summary, Key Insights, Trends, Recommendations. Header row styled in bold black on light blue. Content in dark blue with wrapped text.
- **PDF** (`market_intelligence_report.pdf`) — report-style document with a title page header, per-company sections with bullet-pointed insights, and horizontal dividers between companies.

---

## Notes

- The `.env` file is excluded from version control. Never commit your API key.
- Requires an active Anthropic API account with available credits.
- Target websites can be updated in the `WEBSITES` list in `scraper.py`.
