from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import argparse

load_dotenv()
API_KEY = os.getenv("SCRAPERAPI_KEY")
HUNTER_KEY = os.getenv("HUNTER_API_KEY")

def find_email(domain):
    if not domain or domain == "N/A":
        return "N/A"
    
    # Skip yellowpages internal links
    if "yellowpages.com" in domain:
        return "N/A"
    
    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
    
    try:
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        emails = data.get("data", {}).get("emails", [])
        if emails:
            return emails[0].get("value", "N/A")
        return "N/A"
    except:
        return "N/A"

def scrape_yellowpages(search_term, location, pages=5):
    all_leads = []
    
    for page_num in range(1, pages + 1):
        target_url = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location}&page={page_num}"
        url = f"http://api.scraperapi.com?api_key={API_KEY}&url={target_url}&render=true"
        
        print(f"Scraping page {page_num}...")
        response = requests.get(url, timeout=60)
        print(f"Status: {response.status_code}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.select("div.result")
        print(f"Found {len(listings)} listings")
        
        for listing in listings:
            name_tag = listing.select_one("a.business-name")
            name = name_tag.text.strip() if name_tag else "N/A"
            
            phone_tag = listing.select_one("div.phones")
            phone = phone_tag.text.strip() if phone_tag else "N/A"
            
            street_tag = listing.select_one("div.street-address")
            city_tag = listing.select_one("div.locality")
            street = street_tag.text.strip() if street_tag else ""
            city = city_tag.text.strip() if city_tag else ""
            address = f"{street} {city}".strip()
            
            website_tag = listing.select_one("a.track-visit-website")
            website = website_tag["href"] if website_tag else "N/A"
            
            all_leads.append({
                "name": name,
                "phone": phone,
                "address": address,
                "website": website
            })
        
        print(f"Total so far: {len(all_leads)}")
        time.sleep(2)
    
    return all_leads

def enrich_with_emails(df):
    print("\nFinding emails via Hunter.io...")
    emails = []
    
    for i, row in df.iterrows():
        website = row.get("website", "N/A")
        email = find_email(website)
        emails.append(email)
        
        if email != "N/A":
            print(f"  ✓ {row['name']} → {email}")
        else:
            print(f"  ✗ {row['name']} → no email found")
        
        time.sleep(0.5)  # stay under rate limit
    
    df["email"] = emails
    return df

def clean_and_save(leads, search_term, location):
    df = pd.DataFrame(leads)
    
    if df.empty:
        print("No data captured")
        return
    
    df = df[df["phone"] != "N/A"]
    df = df[df["phone"] != ""]
    df = df.drop_duplicates(subset=["name"])
    df = df.reset_index(drop=True)
    
    # Enrich with emails
    df = enrich_with_emails(df)
    
    filename = f"{search_term}_{location}_leads.csv"
    df.to_csv(filename, index=False, encoding="utf-8")
    
    found = len(df[df["email"] != "N/A"])
    print(f"\nDone. {len(df)} leads saved to {filename}")
    print(f"Emails found: {found}/{len(df)}")

def main():
    parser = argparse.ArgumentParser(description="Scrape Yellow Pages for business leads")
    parser.add_argument("--search", required=True, help="Business type e.g. hvac")
    parser.add_argument("--location", required=True, help="City and state e.g. Tampa+FL")
    parser.add_argument("--pages", type=int, default=5, help="Number of pages to scrape")
    
    args = parser.parse_args()
    
    print(f"\nSearching for: {args.search}")
    print(f"Location: {args.location}")
    print(f"Pages: {args.pages}\n")
    
    leads = scrape_yellowpages(args.search, args.location, args.pages)
    clean_and_save(leads, args.search, args.location)

if __name__ == "__main__":
    main()