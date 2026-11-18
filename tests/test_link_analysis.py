"""
Tests for the AI-Powered Website Link Analysis API.
Run with: python -m pytest tests/ -v
"""
import pytest
import os
from unittest.mock import patch, AsyncMock

# Set test env vars before importing app
os.environ.setdefault("GEMINI_API_KEY", "test-api-key-for-testing")

from fastapi.testclient import TestClient
from app.main import app
from utils.validators import validate_url


# --- Sync test client (no lifespan issues) ---
client = TestClient(app)


# --- Mock LLM Response ---
MOCK_LLM_RESPONSE = {
    "brand": {
        "name": "Example Corp",
        "category": "Technology Services",
        "summary": "A technology company providing digital solutions to businesses.",
    },
    "competitor_analysis": {
        "brand_name": "Example Corp",
        "brand_overview": "A digital technology solutions provider.",
        "main_category": "Technology Services",
        "main_products_services": ["Web Development", "Cloud Solutions", "Digital Marketing"],
        "competitors": [
            {
                "name": "TechRival Inc",
                "overview": "A leading tech company",
                "strengths": ["Established brand", "Large team"],
                "weaknesses": ["Higher pricing", "Less personalized service"],
            },
            {
                "name": "DigiSolutions Ltd",
                "overview": "Digital solutions provider",
                "strengths": ["Global reach", "Diverse portfolio"],
                "weaknesses": ["Complex onboarding", "Less agile"],
            },
            {
                "name": "WebMasters Co",
                "overview": "Web development specialists",
                "strengths": ["Strong portfolio", "Good reviews"],
                "weaknesses": ["Limited services", "Niche focus"],
            },
        ],
        "your_brand_strengths": ["Competitive pricing", "Fast delivery", "Customer focus"],
        "competitive_advantages": ["Personalized approach", "Flexible contracts"],
        "opportunities": ["Expand to new markets", "Add AI services", "Improve SEO"],
    },
    "target_search_queries": [
        {
            "query": "best technology services company",
            "platforms": ["Google"],
            "intent": "Service Search",
            "business_relevance": "High intent users seeking tech services",
            "target_audience": "SMBs looking for tech solutions",
        },
        {
            "query": "digital solutions for business",
            "platforms": ["Facebook"],
            "intent": "Business Discovery",
            "business_relevance": "Broad audience discovery",
            "target_audience": "Business owners on social media",
        },
        {
            "query": "web development inspiration",
            "platforms": ["Instagram"],
            "intent": "Inspiration",
            "business_relevance": "Visual discovery of web projects",
            "target_audience": "Entrepreneurs and startups",
        },
        {
            "query": "technology partner for enterprise",
            "platforms": ["LinkedIn"],
            "intent": "B2B Search",
            "business_relevance": "Enterprise decision makers",
            "target_audience": "C-suite and IT managers",
        },
        {
            "query": "affordable web development services",
            "platforms": ["X"],
            "intent": "Service Discovery",
            "business_relevance": "Cost-conscious buyers",
            "target_audience": "Startups and freelancers",
        },
    ],
    "seo_improvements": {
        "keywords": {
            "primary_keyword": "technology services",
            "secondary_keywords": ["web development", "digital solutions", "cloud services"],
            "long_tail_keywords": [
                "affordable technology services for small business",
                "best web development company near me",
            ],
            "relevant_business_keywords": ["IT consulting", "software development", "digital transformation"],
        },
        "seo_title": {
            "recommended_title": "Professional Technology Services | Example Corp",
            "primary_keyword": "technology services",
            "improved_structure_notes": "Added primary keyword at start, brand name at end",
        },
        "meta_description": {
            "recommended_description": "Example Corp delivers expert technology services including web development and cloud solutions. Contact us for a free consultation.",
            "business_summary": "Expert technology services company",
            "keywords_used": ["technology services", "web development", "digital marketing"],
        },
        "additional_content": [
            {
                "type": "Service Landing Page",
                "title": "Web Development Services",
                "description": "Dedicated page for web development services",
            },
            {
                "type": "Blog Post",
                "title": "Top 10 Technology Trends for 2025",
                "description": "Educational blog content for target audience",
            },
            {
                "type": "FAQ Page",
                "title": "Frequently Asked Questions",
                "description": "Common questions about services and pricing",
            },
            {
                "type": "Industry Page",
                "title": "Technology Solutions for Healthcare",
                "description": "Industry-specific content",
            },
            {
                "type": "Location Page",
                "title": "Technology Services in New York",
                "description": "Local SEO page",
            },
        ],
    },
    "top_services": [
        {
            "name": "Web Development",
            "description": "Custom website and web application development",
            "target_industry": "All Industries",
            "target_customer": "SMBs and enterprises",
            "main_benefit": "Professional online presence",
        },
        {
            "name": "Cloud Solutions",
            "description": "Cloud infrastructure and migration services",
            "target_industry": "Technology, Finance",
            "target_customer": "Mid-market companies",
            "main_benefit": "Scalability and cost savings",
        },
        {
            "name": "Digital Marketing",
            "description": "SEO, PPC, and social media marketing",
            "target_industry": "Retail, E-commerce",
            "target_customer": "Growth-stage businesses",
            "main_benefit": "Increased online visibility",
        },
        {
            "name": "IT Consulting",
            "description": "Strategic IT advice and planning",
            "target_industry": "All Industries",
            "target_customer": "Business executives",
            "main_benefit": "Informed technology decisions",
        },
        {
            "name": "Software Development",
            "description": "Custom software solutions",
            "target_industry": "All Industries",
            "target_customer": "Companies needing custom tools",
            "main_benefit": "Tailored business solutions",
        },
    ],
    "target_audience": {
        "primary_audience": [
            {
                "audience_name": "Small Business Owners",
                "business_type": "Small Businesses",
                "requirement": "Affordable technology solutions",
                "customer_profile": "Owner-operated businesses with 1-50 employees",
                "needs_challenges": ["Limited budget", "No in-house IT team"],
            },
            {
                "audience_name": "Startup Founders",
                "business_type": "Startups",
                "requirement": "Scalable digital solutions",
                "customer_profile": "Early-stage companies seeking rapid growth",
                "needs_challenges": ["Fast time to market", "Cost efficiency"],
            },
        ],
        "secondary_audience": [
            {
                "audience_name": "Enterprise IT Managers",
                "business_type": "Enterprise Companies",
                "requirement": "Custom software and integration",
                "customer_profile": "IT decision makers at large organizations",
                "needs_challenges": ["Legacy system integration", "Security compliance"],
            }
        ],
        "industries": ["Technology", "Retail", "Finance", "Healthcare", "Education"],
        "business_types": ["SMBs", "Startups", "Enterprise", "Non-profit"],
        "location_focus": "Global",
        "interests": ["Digital transformation", "Cost reduction", "Business growth"],
        "recommended_segments": ["SMB owners", "Startup founders", "Enterprise IT teams"],
    },
}


# --- Mock WebsiteContent ---
def _make_mock_content():
    from services.website_extractor import WebsiteContent
    return WebsiteContent(
        url="https://example.com",
        title="Example Corp - Technology Services",
        description="We provide technology solutions",
        keywords="technology, web development",
        headings=["H1: Welcome to Example Corp", "H2: Our Services"],
        main_text="Example Corp provides technology services.",
        nav_items=["Home", "Services", "About", "Contact"],
        footer_text="© 2024 Example Corp.",
        og_data={"title": "Example Corp", "description": "Technology Solutions"},
        full_text="Example Corp - Technology Services\nWe provide technology solutions",
        word_count=50,
    )


# ───────────────────────────────────────────
# Health / root tests
# ───────────────────────────────────────────

def test_root_endpoint():
    """GET / returns healthy status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "endpoint" in data


def test_health_endpoint():
    """GET /health returns healthy status with llm field."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "llm" in data


# ───────────────────────────────────────────
# Link analysis — success path
# ───────────────────────────────────────────

def test_link_analysis_success():
    """POST /link-analysis returns full structured analysis when mocks are in place."""
    mock_content = _make_mock_content()

    with patch("app.main.extract_website_content", new_callable=AsyncMock, return_value=mock_content), \
         patch("app.main.analyze_website_with_llm", new_callable=AsyncMock, return_value=MOCK_LLM_RESPONSE):

        response = client.post("/link-analysis", json={"url": "https://example.com"})

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["website"] == "https://example.com"
    assert data["brand"]["name"] == "Example Corp"
    assert data["brand"]["category"] == "Technology Services"

    analysis = data["analysis"]
    # 5 search queries
    assert len(analysis["target_search_queries"]) == 5
    # 5 services
    assert len(analysis["top_services"]) == 5
    # 3+ competitors
    assert len(analysis["competitor_analysis"]["competitors"]) >= 3
    # SEO fields present
    assert "keywords" in analysis["seo_improvements"]
    assert "seo_title" in analysis["seo_improvements"]
    assert "meta_description" in analysis["seo_improvements"]
    # Audience fields
    assert len(analysis["target_audience"]["primary_audience"]) >= 1


def test_link_analysis_response_structure():
    """Verify the full response schema has all required top-level keys."""
    mock_content = _make_mock_content()

    with patch("app.main.extract_website_content", new_callable=AsyncMock, return_value=mock_content), \
         patch("app.main.analyze_website_with_llm", new_callable=AsyncMock, return_value=MOCK_LLM_RESPONSE):

        response = client.post("/link-analysis", json={"url": "https://example.com"})

    data = response.json()
    for key in ("success", "website", "brand", "analysis"):
        assert key in data, f"Missing top-level key: {key}"

    for key in ("competitor_analysis", "target_search_queries", "seo_improvements", "top_services", "target_audience"):
        assert key in data["analysis"], f"Missing analysis key: {key}"


# ───────────────────────────────────────────
# Validation — error paths
# ───────────────────────────────────────────

def test_link_analysis_missing_url():
    """POST with no url field → 422 Pydantic validation error."""
    response = client.post("/link-analysis", json={})
    assert response.status_code == 422


def test_link_analysis_private_ip_blocked():
    """SSRF: 192.168.x.x must be blocked with 400."""
    response = client.post("/link-analysis", json={"url": "http://192.168.1.1"})
    assert response.status_code == 400
    body = response.json()
    assert "private" in body.get("error", "").lower() or "internal" in body.get("error", "").lower()


def test_link_analysis_localhost_blocked():
    """SSRF: localhost must be blocked with 400."""
    response = client.post("/link-analysis", json={"url": "http://localhost:8080/admin"})
    assert response.status_code == 400


def test_link_analysis_metadata_ip_blocked():
    """SSRF: 169.254.169.254 (AWS/GCP metadata) must be blocked with 400."""
    response = client.post("/link-analysis", json={"url": "http://169.254.169.254/latest/meta-data/"})
    assert response.status_code == 400


def test_link_analysis_ftp_scheme_blocked():
    """Non-http(s) schemes must be blocked with 400."""
    response = client.post("/link-analysis", json={"url": "ftp://example.com/file"})
    assert response.status_code == 400


# ───────────────────────────────────────────
# Validator unit tests
# ───────────────────────────────────────────

def test_url_validator_valid():
    """Valid URLs pass through unchanged (or with https:// prepended)."""
    assert validate_url("https://google.com") == "https://google.com"
    assert validate_url("http://example.com") == "http://example.com"


def test_url_validator_adds_scheme():
    """URL without scheme gets https:// prepended."""
    assert validate_url("example.com") == "https://example.com"


def test_url_validator_blocks_loopback():
    """127.0.0.1 is blocked."""
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        validate_url("http://127.0.0.1")
    assert exc.value.status_code == 400


def test_url_validator_blocks_private_class_a():
    """10.x.x.x is blocked."""
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        validate_url("http://10.0.0.1")
    assert exc.value.status_code == 400


def test_url_validator_blocks_private_class_b():
    """172.16.x.x is blocked."""
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        validate_url("http://172.16.5.5")
    assert exc.value.status_code == 400


def test_url_validator_blocks_localhost_hostname():
    """localhost hostname is blocked."""
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        validate_url("http://localhost")
    assert exc.value.status_code == 400


def test_url_validator_blocks_ftp():
    """ftp:// scheme is rejected."""
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        validate_url("ftp://example.com")
    assert exc.value.status_code == 400
