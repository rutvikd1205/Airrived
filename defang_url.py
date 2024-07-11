import re
import requests
import PyPDF2
import ioc_fanger
from urllib.parse import urlparse

def fang_pdf(file):
    text = extract_text_from_pdf(file)
    cleaned = extract_custom_urls(text)
    valid_iocs = filter_valid_iocs(cleaned)
    separated_iocs = separate_iocs(valid_iocs)

    return separated_iocs

def fang_url(url):
    text = fetch_url_content(url)
    cleaned = extract_custom_urls(text)
    valid_iocs = filter_valid_iocs(cleaned)
    separated_iocs = separate_iocs(valid_iocs)

    return separated_iocs

def fetch_url_content(url):
    response = requests.get(url)
    return response.text

def extract_text_from_pdf(pdf_file):
    text = ''
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_custom_urls(text):
    pattern = r'\b(hxxps?://\S+?)(?:</?[^>]+>|(?=\s|$))'
    matches = re.findall(pattern, text, re.IGNORECASE)
    cleaned_matches = [match.rstrip('.') for match in matches]
    return cleaned_matches

def filter_valid_iocs(defanged_iocs):
    valid_iocs = []
    for ioc in defanged_iocs:
        fanged_ioc = ioc_fanger.fang(ioc)
        valid_iocs.append(fanged_ioc)
    return valid_iocs

def separate_iocs(iocs):
    separated_iocs = []
    for ioc in iocs:
        parsed_url = urlparse(ioc.strip("'"))
        
        scheme = parsed_url.scheme 
        domain = parsed_url.hostname
        ip_address = parsed_url.hostname 
        port = parsed_url.port  
        path = parsed_url.path 
        
        separated_iocs.append({
            'original_ioc': ioc.strip("'"),
            'scheme': scheme,
            'domain': domain,
            'ip_address': ip_address,
            'port': port,
            'path': path
        })
    
    return separated_iocs


