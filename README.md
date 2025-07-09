# 🚀 SEC Financial Data Extractor — No Coding Needed

This tool automates the extraction of key financial reports (Income Statement, Balance Sheet, Cash Flow) from SEC EDGAR filings. Designed with usability in mind, it requires **no API setup or manual scraping** — just enter a company’s **CIK** and **accession number** via a simple prompt.

## 🔍 Project Goal

Built during a research collaboration, this tool addresses the challenge of time-consuming financial data collection by providing a lightweight, beginner-friendly solution that supports fast and clean data access for analysis.

## 💡 Features

- 🔎 Extracts financial reports from EDGAR filings (10-K, 10-Q)
- ✅ No API key or developer setup needed
- 🧼 Cleans and organizes financial tables
- 📊 Exports to Excel with labeled tabs
- 🗃️ Saves a combined CSV for easy use in BI tools

## ⚙️ How It Works

1. Enter **CIK** and **accession number** when prompted
2. Script fetches and parses `FilingSummary.xml`
3. Extracts key financial tables from relevant HTML reports
4. Outputs:
   - `.xlsx` file with structured sheets
   - `.csv` file with combined and cleaned data

## 🛠️ Tech Stack

- Python 3
- `requests`
- `BeautifulSoup`
- `pandas`
- `xlsxwriter`

## 📦 Example Output

- `output/CompanyName_2023Q4_report.xlsx`
- `output/CompanyName_2023Q4_data.csv`

## 📁 Folder Structure

