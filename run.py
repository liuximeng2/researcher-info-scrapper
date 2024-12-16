import pandas as pd
import time
from utils import forge_query, save_json
from scrap import scrape
from extractor import extract_fileds
from collections import Counter


if __name__ == '__main__':
    data = forge_query(pd.read_excel('data/Unresponsive AI researchers list.xlsx'))
    #read list of urls from .txt file
    with open('data/target_urls.txt') as f:
        urls = f.readlines()
    urls = [x.strip() for x in urls]
    domains = [url.split(".emory.edu")[0].split("//")[-1] for url in urls]

    # Calculate statistics
    domain_counts = Counter(domains)
    total_domains = len(domains)
    print("Total domains:", domain_counts)

    for domain, url, researcher in zip(domains, urls, data):
        print(researcher)
        name = researcher[0]
        print(f"Domain: {domain}, URL: {url}")
        text = scrape(url, domain, name, need_images=False)
        info = extract_fileds(text)
        save_json(info.dict(), name)
        print(info)
        print('='*80)
