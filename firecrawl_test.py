from firecrawl import FirecrawlApp
import os
import pandas as pd
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("FIRECRAWL_API_KEY")
app = FirecrawlApp(api_key=API_KEY)

# Load first 6 valid PDF URLs
df = pd.read_csv("kenya_docs_master.csv")
pdf_urls = (
    df["pdfurl"]
    .dropna()
    .astype(str)
    .str.strip()
    .loc[lambda s: s.str.startswith("http")]
    .iloc[2005:2010] 
    .tolist()
)

print(f"\n🔍 Submitting {len(pdf_urls)} URLs to Firecrawl...\n")

# Submit and wait for completion
batch_scrape_result = app.batch_scrape_urls(
    pdf_urls,
    formats=["extract", 'markdown'],
    extract={
        'prompt': 'Extract these: purpose, if it is a loan document, loan size ($), grace period (in years), interest rate, transation year, summary from the document.',
        'schema': {
            'type': 'object',
            'properties': {
                'purpose': {'type': 'string'},
                'loan': {'type': 'bool'},
                'loan_size': {'type': 'int'},
                'grace_period': {'type': 'int'},
                'transaction_year': {'type': 'int'},
                # 'description': {'type': 'string'}
            },
            # 'required': ['description']

            'required': ['purpose', 'loan', 'loan_size', 'grace_period', 'transaction_year']
        }
    }
)

print(batch_scrape_result)