import requests
from pathlib import Path
from pypdf import PdfWriter
from utils import url_to_safe_filename
import os

OUTPUT_PDF_DIR = Path('output_pdf')
EXTRACT_TEXT_DIR = Path('extract_text')
OPTIMIZED_PDF_DIR = Path('optimized_pdf')
OUTPUT_PDF_DIR.mkdir(exist_ok=True)
EXTRACT_TEXT_DIR.mkdir(exist_ok=True)
OPTIMIZED_PDF_DIR.mkdir(exist_ok=True)

def extract_text_from_pdf(pdf_path, out_txt_path):
    url = "https://universal-file-to-text-extractor.vercel.app/extract"
    with open(pdf_path, 'rb') as f:
        files = {'files': (os.path.basename(pdf_path), f, 'application/pdf')}
        data = {
            'mode': 'single',
            'output_type': 'jsonl',
            'include_images': 'false',
        }
        resp = requests.post(url, files=files, data=data)
        resp.raise_for_status()
        with open(out_txt_path, 'w', encoding='utf-8') as out_f:
            out_f.write(resp.text)
        return out_txt_path

def optimize_pdf(input_pdf, output_pdf, quality=80):
    writer = PdfWriter(clone_from=input_pdf)
    for page in writer.pages:
        for img in getattr(page, "images", []):
            img.replace(img.image, quality=quality)
    for page in writer.pages:
        page.compress_content_streams()
    writer.remove_links()
    with open(output_pdf, "wb") as f:
        writer.write(f)

def extract_texts_from_pdfs():
    for pdf_file in OUTPUT_PDF_DIR.glob('*.pdf'):
        txt_file = EXTRACT_TEXT_DIR / (pdf_file.stem + '.txt')
        if txt_file.exists():
            print(f"Text already extracted for {pdf_file.name}")
            continue
        print(f"Extracting text from {pdf_file.name}")
        try:
            extract_text_from_pdf(pdf_file, txt_file)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 413:
                print(f"File too large, optimizing {pdf_file.name} and retrying...")
                optimized_pdf = OPTIMIZED_PDF_DIR / (pdf_file.stem + "_optimized.pdf")
                optimize_pdf(pdf_file, optimized_pdf, quality=80)
                try:
                    extract_text_from_pdf(optimized_pdf, txt_file)
                except Exception as e2:
                    print(f"Failed after optimization: {e2}")
            else:
                print(f"Failed to extract for {pdf_file}: {e}")
        except Exception as e:
            print(f"Failed to extract for {pdf_file}: {e}") 