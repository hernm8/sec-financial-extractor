import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import warnings
from bs4 import XMLParsedAsHTMLWarning
import re

# Ignore XMLParsedAsHTMLWarning from BeautifulSoup
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

HEADERS = {
    "User-Agent": "YourName Contact: your.email@example.com"
}

def sanitize_sheet_name(name):
    """Removes characters not allowed in Excel sheet names and truncates to 31 characters."""
    return re.sub(r'[\[\]\:\*\?\/\\]', '', name)[:31]

def fetch_filing_summary(cik, accession_number):
    cik_padded = str(cik).zfill(10)
    accession_folder = accession_number.replace("-", "")
    base_url = f"https://www.sec.gov/Archives/edgar/data/{cik_padded}/{accession_folder}/"
    filing_summary_url = base_url + "FilingSummary.xml"

    print(f"Fetching FilingSummary.xml from {filing_summary_url}")
    r = requests.get(filing_summary_url, headers=HEADERS)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, "lxml")
    reports = soup.find_all("report")

    report_dict = {}
    for report in reports:
        title = report.shortname.text.lower()
        if any(x in title for x in ["income", "balance", "cash"]):
            url = base_url + report.htmlfilename.text
            report_dict[report.shortname.text.strip()] = url

    if not report_dict:
        print("No main financial reports found in FilingSummary.xml.")
    return report_dict

def parse_html_table(url):
    print(f"Downloading report: {url}")
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table")

    if not table:
        print("No table found in the report:", url)
        return pd.DataFrame()

    rows = []
    for row in table.find_all("tr"):
        cols = row.find_all(["td", "th"])
        cols = [col.get_text(strip=True).replace("\xa0", " ") for col in cols]
        rows.append(cols)

    df = pd.DataFrame(rows)
    df = df.dropna(how='all')
    return df

def save_reports_to_excel(report_dict, filename):
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", filename)
    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
        for sheet_name, url in report_dict.items():
            df = parse_html_table(url)
            safe_name = sanitize_sheet_name(sheet_name)
            if not df.empty:
                df.to_excel(writer, sheet_name=safe_name, index=False)
            else:
                print(f"Skipping empty DataFrame for sheet: {sheet_name}")
    print(f"\n✅ Saved to {path}")

def main():
    print("Enter company details to download financial reports from SEC EDGAR:")

    cik = input("Enter the company's CIK (numbers only): ").strip()
    accession = input("Enter the accession number (format: xxxxxxxx-xx-xxxxxx): ").strip()
    company_name = input("Enter a short name for the company (used in output filename): ").strip()

    try:
        reports = fetch_filing_summary(cik, accession)
        if reports:
            output_file = f"{company_name}_{accession.replace('-', '')}_report.xlsx"
            save_reports_to_excel(reports, output_file)
        else:
            print(f"No reports to save for {company_name}.")
    except requests.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
