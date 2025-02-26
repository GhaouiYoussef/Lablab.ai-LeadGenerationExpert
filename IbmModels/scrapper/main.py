from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import find_company_website, scrape_company_website
from summarizer import summarize_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://leads-gen-ai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/company-info")
async def company_info(company: str):
    website = find_company_website(company)
    if not website:
        return {"company": company, "data": "No website found."}

    text = scrape_company_website(website)
    if not text:
        return {"company": company, "data": "Failed to scrape."}

    summary = summarize_text(text)
    return {"company": company, "website": website, "summary": summary}
