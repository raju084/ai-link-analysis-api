import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from app.schemas import LinkAnalysisRequest, LinkAnalysisResponse
from utils.validators import validate_url
from services.website_extractor import extract_website_content
from services.llm_service import analyze_website_with_llm
from services.analysis_service import map_llm_response_to_schemas

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI-Powered Website Link Analysis API")
    yield
    logger.info("Shutting down AI-Powered Website Link Analysis API")


app = FastAPI(
    title="AI-Powered Website Link Analysis API",
    description="""
    Analyzes a given website URL using AI to generate business intelligence insights.
    
    ## Features
    - 🏢 **Competitor Analysis** - Identify and compare competitors
    - 🔍 **Search Query Intelligence** - Find relevant search queries across platforms
    - 📈 **SEO Improvements** - Get actionable SEO recommendations
    - 🛠️ **Service Identification** - Discover top business services
    - 🎯 **Target Audience** - Identify and segment target customers
    
    ## LLM
    Powered by **Google Gemini 1.5 Flash** for fast, accurate, and cost-effective analysis.
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
@app.get("/api", tags=["Health"], include_in_schema=False)
@app.get("/api/index.py", tags=["Health"], include_in_schema=False)
async def root():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI-Powered Website Link Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoint": "POST /link-analysis"
    }


@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"], include_in_schema=False)
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "AI-Powered Website Link Analysis API",
        "llm": "Google Gemini 2.5 Flash",
        "version": "1.0.0"
    }


@app.get("/link-analysis", tags=["Analysis"])
@app.get("/link-analysis/", tags=["Analysis"], include_in_schema=False)
@app.get("/api/link-analysis", tags=["Analysis"], include_in_schema=False)
async def link_analysis_info():
    """Information endpoint for GET requests to /link-analysis."""
    return {
        "message": "The /link-analysis endpoint requires a POST request with a JSON body.",
        "usage": {
            "method": "POST",
            "url": "https://ai-link-analysis-api.vercel.app/link-analysis",
            "headers": {"Content-Type": "application/json"},
            "body": {"url": "https://example.com"}
        },
        "docs": "/docs"
    }


@app.post(
    "/link-analysis",
    response_model=LinkAnalysisResponse,
    tags=["Analysis"],
    summary="Analyze a website URL",
    description="""
    Accepts a website URL and returns a comprehensive AI-powered analysis including:
    - Competitor analysis and brand comparison
    - Top 5 target search queries across platforms
    - SEO improvement recommendations
    - Top 5 identified services
    - Target audience identification
    """,
)
@app.post(
    "/link-analysis/",
    response_model=LinkAnalysisResponse,
    include_in_schema=False,
)
@app.post(
    "/api/link-analysis",
    response_model=LinkAnalysisResponse,
    include_in_schema=False,
)
async def analyze_link(request: LinkAnalysisRequest) -> LinkAnalysisResponse:
    """
    Analyze a website URL and return structured business intelligence.
    
    - **url**: Valid HTTP/HTTPS website URL to analyze
    """
    logger.info(f"Received analysis request for URL: {request.url}")
    
    # Step 1: Validate URL (SSRF protection)
    validated_url = validate_url(request.url)
    logger.info(f"URL validated: {validated_url}")
    
    # Step 2: Fetch and extract website content
    logger.info(f"Fetching website content from: {validated_url}")
    website_content = await extract_website_content(validated_url)
    logger.info(f"Extracted {website_content.word_count} words from website")
    
    # Step 3: Analyze with LLM
    logger.info("Sending content to Gemini for analysis...")
    llm_response = await analyze_website_with_llm(website_content)
    
    # Step 4: Map to schemas
    brand, analysis = map_llm_response_to_schemas(llm_response)
    
    # Step 5: Return structured response
    response = LinkAnalysisResponse(
        success=True,
        website=validated_url,
        brand=brand,
        analysis=analysis,
    )
    
    logger.info(f"Analysis complete for: {validated_url}")
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Global HTTP exception handler returning consistent JSON error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "website": str(request.url),
            "error": exc.detail,
            "brand": None,
            "analysis": None,
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Catch-all exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "website": str(request.url),
            "error": "An unexpected error occurred. Please try again.",
            "brand": None,
            "analysis": None,
        }
    )
