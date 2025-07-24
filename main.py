#!/usr/bin/env python3
"""
DBT Chatbot - Crawl4ai Simple Example
"""

import asyncio
from crawl_and_save_pdfs import crawl_and_save_pdfs
from extract_text import extract_texts_from_pdfs
from embed_and_store import embed_and_store_all

STR_URL = 'https://www.digitalbiz.tech/'

def main():
    # Step 1: Crawl and save PDFs
    asyncio.run(crawl_and_save_pdfs(STR_URL))
    # Step 2: Extract text from PDFs
    extract_texts_from_pdfs()
    # Step 3: For each .txt, get embedding and store in Supabase
    embed_and_store_all()

if __name__ == "__main__":
    main() 