# Market Intelligence Tool

A Market Intelligence Tool built as part of the TIMOCOM interview project.

## Overview

This tool scrapes market data from the web, processes and analyzes it using Claude AI, and exports the results as structured Excel and PDF reports.

## Project Structure

```
timocom-market-intelligence/
├── scraper.py        # Web scraping logic
├── processor.py      # Data processing and Claude AI analysis
├── excel_output.py   # Excel report generation
├── pdf_output.py     # PDF report generation
├── main.py           # Entry point — orchestrates the pipeline
├── requirements.txt  # Python dependencies
├── .env              # API keys (not committed to version control)
└── output/           # Generated reports (Excel and PDF)
```

## Setup

1. Clone the repository and navigate to the project directory.

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your Anthropic API key to `.env`:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```

## Usage

```bash
python main.py
```

Reports will be saved to the `output/` directory.

## Dependencies

- `anthropic` — Claude AI for market data analysis
- `beautifulsoup4` — HTML parsing for web scraping
- `requests` — HTTP requests
- `openpyxl` — Excel file generation
- `reportlab` — PDF file generation
- `python-dotenv` — Environment variable management
