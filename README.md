# DBT Chatbot Crawler Pipeline 

This project crawls a website, saves each page as a PDF, extracts text from the PDFs, generates OpenAI embeddings, and stores the results in Supabase for search and analysis.

## Project Structure

- `main.py` — Orchestrates the workflow.
- `crawl_and_save_pdfs.py` — Crawls the website and saves each page as a PDF.
- `extract_text.py` — Extracts text from PDFs, optimizes large PDFs if needed.
- `embed_and_store.py` — Embeds extracted text using OpenAI and stores it in Supabase.
- `utils.py` — Shared helper functions.
- `config.py` — Stores API keys and configuration variables (**not tracked in git; you must create this file**).

## Workflow

```mermaid
flowchart TB
    A["Crawl Website"] --> B["Save PDFs"]
    B --> C["Extract Text"]
    C L_C_D_0@-.-> D(["Optimize Large PDFs"])
    C --> n2["Untitled Node"]
    C L_C_n1_0@<-.-> n1["Call text Extraction API"]
    D L_D_C_0@-.-> C
    n2 --> n3["Generate Embeddings"]
    n3 --> n4["Store in Supabase"]

    A@{ shape: procs}
    B@{ shape: disk}
    C@{ shape: manual-file}
    n2@{ shape: anchor}
    n1@{ shape: doc}
    n3@{ shape: paper-tape}
    n4@{ shape: internal-storage}
     A:::Sky
     n4:::Ash
    classDef Sky stroke-width:1px, stroke-dasharray:none, stroke:#374D7C, fill:#E2EBFF, color:#374D7C
    classDef Ash stroke-width:1px, stroke-dasharray:none, stroke:#999999, fill:#EEEEEE, color:#000000

    L_C_D_0@{ animation: slow } 
    L_C_n1_0@{ animation: none } 
    L_D_C_0@{ animation: slow } 


```

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a `config.py` file in the project root**
   - This file should contain your `SUPABASE_URL`, `SUPABASE_KEY`, and `OPENAI_API_KEY` variables. Example:
     ```python
     SUPABASE_URL = "your_supabase_url"
     SUPABASE_KEY = "your_supabase_key"
     OPENAI_API_KEY = "your_openai_api_key"
     ```
   - **Note:** `config.py` is not tracked by git for security reasons.

## Running the Pipeline

Run the entire workflow:
```bash
python main.py
```

This will:
1. Crawl the target website and save PDFs to `output_pdf/`
2. Extract text from PDFs to `extract_text/` (optimizing large PDFs as needed)
3. Generate embeddings and store them in Supabase

## Running Steps Individually

You can also run each step separately by importing and calling the relevant functions from each module.

## Requirements
- Python 3.8+
- See `requirements.txt` for Python dependencies

## License
MIT 
