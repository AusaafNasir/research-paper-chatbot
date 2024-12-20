import requests
import os
import xml.etree.ElementTree as ET

# API endpoint
ARXIV_API_URL = "https://export.arxiv.org/api/query"

# Query parameters
search_query = "machine learning OR deep learning OR natural language processing"
results_per_request = 200  
max_papers = 1000  
output_folder = "data/papers"
os.makedirs(output_folder, exist_ok=True)

def fetch_arxiv_papers(query, start=0, max_results=200):
    """Fetch papers from arXiv API."""
    print(f"Fetching results {start} to {start + max_results}...")
    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    response = requests.get(ARXIV_API_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    return response.text

def parse_and_download_pdfs(response_xml, save_folder):
    """Parse arXiv XML response and download PDFs."""
    root = ET.fromstring(response_xml)
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", namespace):
        title = entry.find("atom:title", namespace).text.strip()
        pdf_link = entry.find("atom:link[@title='pdf']", namespace).attrib['href']
        paper_id = pdf_link.split("/")[-1]

        print(f"Downloading PDF: {title}")
        pdf_response = requests.get(pdf_link)
        if pdf_response.status_code == 200:
            pdf_path = os.path.join(save_folder, f"{paper_id}.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf_response.content)
            print(f"Saved: {pdf_path}")
        else:
            print(f"Failed to download {pdf_link}")

# Loop to fetch results in batches
print("Starting arXiv paper download...")
for start in range(0, max_papers, results_per_request):
    try:
        xml_data = fetch_arxiv_papers(search_query, start, results_per_request)
        parse_and_download_pdfs(xml_data, output_folder)
    except Exception as e:
        print(f"Error occurred: {e}")
        break

print("Finished downloading papers!")
