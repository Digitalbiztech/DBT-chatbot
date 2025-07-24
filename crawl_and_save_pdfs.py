import asyncio
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, FilterChain, DomainFilter, ContentTypeFilter
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import types
from utils import url_to_safe_filename

OUTPUT_PDF_DIR = Path('output_pdf')
OUTPUT_PDF_DIR.mkdir(exist_ok=True)


def save_pdf_from_crawl_result(result, pdf_path):
    if hasattr(result, 'pdf') and result.pdf:
        with open(pdf_path, 'wb') as f:
            f.write(result.pdf)
        return True
    return False

def get_internal_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    base_domain = urlparse(base_url).netloc
    links = set()
    for a in soup.find_all('a', href=True):
        from bs4.element import Tag
        if not isinstance(a, Tag):
            continue
        href = a.get('href')
        if not isinstance(href, str):
            continue
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == base_domain:
            links.add(full_url.split('#')[0])
    return links

async def crawl_and_save_pdfs(start_url):
    browser_config = BrowserConfig(headless=True, verbose=False)
    filter_chain = FilterChain([
        DomainFilter(allowed_domains=["www.digitalbiz.tech", "digitalbiz.tech"]),
        ContentTypeFilter(allowed_types=["text/html"])
    ])
    bfs_strategy = BFSDeepCrawlStrategy(
        max_depth=4,
        include_external=False,
        filter_chain=filter_chain
    )
    crawler_config = CrawlerRunConfig(
        css_selector='#mainView',
        excluded_tags=["form", "nav", "footer", "header"],
        page_timeout=50000000,
        pdf=True,
        wait_for_images=True,
        scan_full_page=True,
        wait_for="js:() => document.readyState === 'complete'",
        deep_crawl_strategy=bfs_strategy,
        stream=False,
        verbose=True
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        print(f"Deep crawling: {start_url}")
        results = await crawler.arun(start_url, config=crawler_config)
        import inspect
        if isinstance(results, list):
            pass
        elif inspect.isasyncgen(results):
            results = [item async for item in results]
        else:
            results = [results]
        print(f"Crawled {len(results)} pages.")
        for result in results:
            if not hasattr(result, 'url') or isinstance(result, (types.AsyncGeneratorType, types.GeneratorType)):
                print(f"Skipping result without 'url': {type(result)}")
                continue
            pdf_path = OUTPUT_PDF_DIR / (url_to_safe_filename(result.url) + '.pdf')
            save_pdf_from_crawl_result(result, pdf_path) 