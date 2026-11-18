# 🤖 AI-Powered Website Link Analysis API

A production-ready FastAPI application that analyzes any website URL using Google Gemini AI to generate comprehensive business intelligence insights — including competitor analysis, SEO improvements, search query intelligence, service identification, and target audience profiling.

---

## 🚀 Live Demo

| Resource | URL |
|---|---|
| Live API | `https://ai-link-analysis-api.vercel.app` |
| API Endpoint | `https://ai-link-analysis-api.vercel.app/link-analysis` |
| API Documentation | `https://ai-link-analysis-api.vercel.app/docs` |

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [API Usage](#api-usage)
- [Sample Request & Response](#sample-request--response)
- [LLM Platform Research & Recommendation](#llm-platform-research--recommendation)
- [Cost Optimization Strategies](#cost-optimization-strategies)
- [Security](#security)
- [Running Tests](#running-tests)
- [Deployment](#deployment)

---

## ✨ Features

| Section | Description |
|---|---|
| 🏢 **Competitor Analysis** | Brand overview, 3+ real competitors, strengths, weaknesses, opportunities |
| 🔍 **Search Query Intelligence** | 5 targeted queries across Google, Facebook, Instagram, LinkedIn, X |
| 📈 **SEO Improvements** | Keywords, optimized title, meta description, supporting content suggestions |
| 🛠️ **Top 5 Services** | Service identification with target industry, customer, and benefit |
| 🎯 **Target Audience** | Primary/secondary segments, industries, customer needs, recommended segments |

---

## 📁 Project Structure

```
ai-link-analysis/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, routes, middleware, exception handlers
│   ├── config.py            # Pydantic settings with env var support
│   └── schemas.py           # All Pydantic v2 request/response models
│
├── services/
│   ├── __init__.py
│   ├── website_extractor.py # Async HTTP fetcher + BeautifulSoup HTML parser
│   ├── llm_service.py       # Google Gemini API integration + prompt engineering
│   └── analysis_service.py  # LLM JSON → Pydantic model mapper
│
├── utils/
│   ├── __init__.py
│   └── validators.py        # URL validation + SSRF protection
│
├── tests/
│   └── test_link_analysis.py # Pytest async test suite
│
├── .env.example             # Environment variable template
├── requirements.txt         # Pinned Python dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-link-analysis.git
cd ai-link-analysis
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
APP_HOST=0.0.0.0
APP_PORT=4000
MAX_CONTENT_LENGTH=50000
REQUEST_TIMEOUT=30
```

> **Get a free Gemini API key:** https://aistudio.google.com/app/apikey

### 5. Start the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

The API is now running at:
- **API:** http://localhost:4000
- **Swagger Docs:** http://localhost:4000/docs
- **ReDoc:** http://localhost:4000/redoc

---

## 🔌 API Usage

### Endpoint

```
POST http://localhost:4000/link-analysis
```

### Request Body

```json
{
  "url": "https://example.com"
}
```

### cURL Example

```bash
curl -X POST http://localhost:4000/link-analysis \
  -H "Content-Type: application/json" \
  -d '{"url": "https://stripe.com"}'
```

### Python Example

```python
import httpx

response = httpx.post(
    "http://localhost:4000/link-analysis",
    json={"url": "https://stripe.com"},
    timeout=120
)
print(response.json())
```

---

## 📊 Sample Request & Response

**Request:**
```json
{
  "url": "https://stripe.com"
}
```

**Response:**
```json
{
  "success": true,
  "website": "https://stripe.com",
  "brand": {
    "name": "Stripe",
    "category": "Financial Technology (FinTech) / Payment Processing",
    "summary": "Stripe is a global technology company that builds economic infrastructure for the internet, providing payment processing, billing, and financial tools for businesses of all sizes."
  },
  "analysis": {
    "competitor_analysis": {
      "brand_name": "Stripe",
      "brand_overview": "Stripe provides payment APIs and financial infrastructure for internet businesses.",
      "main_category": "Payment Processing & FinTech",
      "main_products_services": ["Payment Processing", "Billing & Subscriptions", "Stripe Connect", "Stripe Capital", "Fraud Detection"],
      "competitors": [
        {
          "name": "PayPal",
          "overview": "Global payments leader with consumer and merchant solutions.",
          "strengths": ["Brand recognition", "Large user base", "Consumer trust"],
          "weaknesses": ["Higher fees for small merchants", "Less developer-friendly APIs"]
        },
        {
          "name": "Square (Block)",
          "overview": "Payment and business management platform for SMBs.",
          "strengths": ["POS integration", "SMB focus", "Easy onboarding"],
          "weaknesses": ["Less suited for enterprise", "Limited international reach"]
        },
        {
          "name": "Adyen",
          "overview": "Enterprise-grade payment platform for large merchants.",
          "strengths": ["Global coverage", "Enterprise features", "Unified commerce"],
          "weaknesses": ["Complex for small businesses", "Higher entry barrier"]
        }
      ],
      "your_brand_strengths": ["Developer-first API design", "Comprehensive documentation", "Global reach in 135+ countries"],
      "competitive_advantages": ["Best-in-class developer experience", "Comprehensive financial infrastructure beyond payments"],
      "opportunities": ["Expand banking-as-a-service offerings", "Target emerging markets", "Grow Stripe Capital"]
    },
    "target_search_queries": [
      {
        "query": "best payment gateway for SaaS companies",
        "platforms": ["Google"],
        "intent": "Service Search",
        "business_relevance": "Directly targets Stripe's core SaaS customer segment",
        "target_audience": "SaaS founders and CTOs evaluating payment solutions"
      },
      {
        "query": "online payment solutions for e-commerce",
        "platforms": ["Facebook"],
        "intent": "Business Discovery",
        "business_relevance": "Broad audience of e-commerce business owners",
        "target_audience": "E-commerce store owners and entrepreneurs"
      },
      {
        "query": "startup payment integration tutorial",
        "platforms": ["Instagram"],
        "intent": "Inspiration",
        "business_relevance": "Appeals to developer and startup community",
        "target_audience": "Startup founders and indie developers"
      },
      {
        "query": "enterprise payment infrastructure provider",
        "platforms": ["LinkedIn"],
        "intent": "B2B Search",
        "business_relevance": "Targets enterprise decision-makers",
        "target_audience": "CFOs and CTOs at enterprise companies"
      },
      {
        "query": "stripe alternative payment api 2024",
        "platforms": ["X"],
        "intent": "Service Discovery",
        "business_relevance": "Captures comparison shoppers and competitive positioning",
        "target_audience": "Developers and tech-savvy business owners"
      }
    ],
    "seo_improvements": {
      "keywords": {
        "primary_keyword": "payment processing API",
        "secondary_keywords": ["online payment gateway", "payment infrastructure", "developer payments"],
        "long_tail_keywords": ["best payment API for startups", "how to integrate payment gateway in website", "accept online payments for small business"],
        "relevant_business_keywords": ["Stripe payments", "recurring billing software", "subscription management platform"]
      },
      "seo_title": {
        "recommended_title": "Payment Processing API & Financial Infrastructure | Stripe",
        "primary_keyword": "payment processing API",
        "improved_structure_notes": "Lead with primary keyword, clarify value proposition, end with brand name"
      },
      "meta_description": {
        "recommended_description": "Stripe's payment processing API lets you accept payments, manage subscriptions, and scale your financial operations globally. Start for free today.",
        "business_summary": "Global payment infrastructure for internet businesses",
        "keywords_used": ["payment processing API", "accept payments", "subscriptions"]
      },
      "additional_content": [
        {
          "type": "Service Landing Page",
          "title": "Payment Gateway for E-Commerce",
          "description": "Dedicated page targeting e-commerce store owners with specific features and pricing"
        },
        {
          "type": "Industry Page",
          "title": "Payment Solutions for SaaS Companies",
          "description": "Industry-specific content for SaaS businesses covering subscription billing"
        },
        {
          "type": "FAQ Page",
          "title": "Stripe Pricing & Fee Calculator",
          "description": "Interactive FAQ addressing common questions about transaction fees and pricing"
        },
        {
          "type": "Blog Post",
          "title": "How to Choose the Right Payment Gateway in 2025",
          "description": "Educational content to capture top-of-funnel comparison searches"
        },
        {
          "type": "Location Page",
          "title": "Payment Solutions for UK Businesses",
          "description": "Region-specific landing pages targeting local search intent"
        }
      ]
    },
    "top_services": [
      {
        "name": "Stripe Payments",
        "description": "Unified API for accepting online and in-person payments globally",
        "target_industry": "E-commerce, SaaS, Marketplaces",
        "target_customer": "Businesses of all sizes",
        "main_benefit": "Accept payments in 135+ currencies with one integration"
      },
      {
        "name": "Stripe Billing",
        "description": "Subscription and recurring billing management platform",
        "target_industry": "SaaS, Media, Membership",
        "target_customer": "Companies with subscription revenue models",
        "main_benefit": "Automate recurring revenue with smart retry logic"
      },
      {
        "name": "Stripe Connect",
        "description": "Payment infrastructure for platforms and marketplaces",
        "target_industry": "Marketplaces, Platforms, Gig Economy",
        "target_customer": "Platform operators and marketplace builders",
        "main_benefit": "Onboard sellers and route payments at scale"
      },
      {
        "name": "Stripe Capital",
        "description": "Fast business financing based on Stripe payment history",
        "target_industry": "All industries using Stripe",
        "target_customer": "Growing businesses needing working capital",
        "main_benefit": "Get funding with no fixed monthly repayments"
      },
      {
        "name": "Stripe Radar",
        "description": "Machine learning fraud detection and prevention",
        "target_industry": "E-commerce, Financial Services",
        "target_customer": "Businesses with high transaction volume",
        "main_benefit": "Reduce fraud while maximizing revenue"
      }
    ],
    "target_audience": {
      "primary_audience": [
        {
          "audience_name": "SaaS Founders & Developers",
          "business_type": "Software-as-a-Service",
          "requirement": "Reliable, scalable payment API",
          "customer_profile": "Technical founders and CTOs building internet products",
          "needs_challenges": ["Easy API integration", "Subscription billing support", "Global payment acceptance"]
        },
        {
          "audience_name": "E-Commerce Businesses",
          "business_type": "Online Retail",
          "requirement": "Seamless checkout and payment processing",
          "customer_profile": "Online store owners seeking conversion-optimized payments",
          "needs_challenges": ["Cart abandonment reduction", "Multi-currency support", "Fraud prevention"]
        }
      ],
      "secondary_audience": [
        {
          "audience_name": "Enterprise Finance Teams",
          "business_type": "Large Enterprise",
          "requirement": "Financial infrastructure and reporting",
          "customer_profile": "CFOs and finance teams at large organizations",
          "needs_challenges": ["Compliance and regulatory requirements", "Revenue reconciliation", "Global tax handling"]
        }
      ],
      "industries": ["Financial Technology", "E-Commerce", "SaaS", "Marketplace & Gig Economy", "Non-Profit"],
      "business_types": ["Startups", "SMBs", "Enterprise", "Platform Operators", "Non-Profits"],
      "location_focus": "Global (135+ countries)",
      "interests": ["Developer tools", "Financial automation", "Business scaling", "API integrations"],
      "recommended_segments": ["SaaS developers", "E-commerce store owners", "Platform builders", "Enterprise finance teams"]
    }
  }
}
```

---

## 🧠 LLM Platform Research & Recommendation

### A. LLM Platform Comparison

| Criteria | OpenAI GPT-4o | Google Gemini 1.5 Flash | Anthropic Claude 3.5 Haiku | Mistral Large |
|---|---|---|---|---|
| **Provider** | OpenAI | Google DeepMind | Anthropic | Mistral AI |
| **Model Name** | gpt-4o | gemini-1.5-flash | claude-3-5-haiku-20241022 | mistral-large-latest |
| **Input Cost** | \$2.50 / 1M tokens | **\$0.075 / 1M tokens** | \$0.80 / 1M tokens | \$2.00 / 1M tokens |
| **Output Cost** | \$10.00 / 1M tokens | **\$0.30 / 1M tokens** | \$4.00 / 1M tokens | \$6.00 / 1M tokens |
| **Response Speed** | ~3–6s | **~1–3s** | ~2–4s | ~3–5s |
| **Context Window** | 128K tokens | **1M tokens** | 200K tokens | 128K tokens |
| **JSON Support** | Excellent | **Excellent (native)** | Excellent | Good |
| **Website Analysis Accuracy** | Very High | **High** | Very High | Moderate |
| **Free Tier** | No | **Yes (Gemini API)** | No | No |
| **Recommendation** | High accuracy, high cost | ✅ **Best value for this task** | High quality, higher cost | Less proven for structured output |

> **Pricing source:** OpenAI pricing page (Nov 2024), Google AI Studio pricing (Nov 2024), Anthropic pricing page (Nov 2024), Mistral pricing (Nov 2024).  
> **Response times:** Estimates based on documented benchmarks and community reports; not independently measured.

---

### B. ✅ Recommended Model: Google Gemini 1.5 Flash

**Why Gemini 1.5 Flash is the best choice for this application:**

1. **Lowest cost** — At \$0.075/1M input tokens and \$0.30/1M output tokens, it is **10–30× cheaper** than GPT-4o and Claude 3.5 Haiku for equivalent output.
2. **1 Million token context window** — Handles even the largest website content without truncation.
3. **Native JSON output** — `response_mime_type="application/json"` guarantees structured output without markdown noise.
4. **Fast response time** — Typically 1–3 seconds for website analysis tasks (estimated from Google AI Studio benchmarks).
5. **Free tier available** — Gemini API offers a free tier via Google AI Studio, ideal for development and testing.
6. **Sufficient accuracy** — For business analysis of website content, Gemini 1.5 Flash produces high-quality, well-reasoned output comparable to GPT-4o at a fraction of the cost.

---

### C. Cost Optimization Strategies

| Strategy | Implementation | Savings Estimate |
|---|---|---|
| **Content cleaning** | Strip HTML tags, scripts, styles before sending to LLM | 30–50% token reduction |
| **Text truncation** | Cap extracted content at 12,000 chars | Prevents runaway costs |
| **Single API call** | Generate all 5 sections in one prompt instead of 5 calls | 80% cost reduction vs. multi-call |
| **Smaller model for extraction** | Use Gemini Flash (not Pro) for all tasks | 10× cheaper than Pro |
| **Response caching** | Cache analysis results by URL hash for 24h | Eliminates repeat costs |
| **Deduplication** | Remove duplicate nav items and repetitive footer text | 5–10% token savings |
| **Prompt optimization** | Concise, structured prompt with clear JSON schema | 15–20% token savings |

---

### D. Final LLM Recommendation

| Field | Value |
|---|---|
| **Recommended Provider** | Google (via Google AI Studio / Google Cloud) |
| **Recommended Model** | `gemini-1.5-flash` |
| **Estimated Input Tokens per Analysis** | ~3,000–6,000 tokens (website content + prompt) |
| **Estimated Output Tokens per Analysis** | ~1,500–2,500 tokens (structured JSON response) |
| **Estimated Cost per Analysis** | **\$0.0003–\$0.0007** (less than 1/10th of a cent) |
| **Expected Response Time** | 2–5 seconds (estimated) |
| **Why Selected** | Best balance of cost, speed, context window, and native JSON support |
| **Alternative / Fallback Model** | `claude-3-5-haiku-20241022` (Anthropic) — higher quality, ~10× more expensive |
| **Recommended Approach** | Use Gemini 1.5 Flash for production; cache results by URL for 24h; fall back to Claude Haiku for complex/low-confidence sites |

---

## 🔒 Security

This API implements **SSRF (Server-Side Request Forgery) protection** in `utils/validators.py`:

- ✅ Only `http://` and `https://` schemes are allowed
- ✅ Blocks private IPv4 ranges: `10.x.x.x`, `172.16–31.x.x`, `192.168.x.x`
- ✅ Blocks loopback: `127.x.x.x`, `localhost`
- ✅ Blocks link-local: `169.254.x.x` (AWS/GCP metadata endpoint)
- ✅ Blocks internal hostnames: `metadata.google.internal`
- ✅ DNS resolution check prevents hostname-based SSRF bypass
- ✅ API keys stored in environment variables — never hardcoded
- ✅ `.env` file excluded from version control via `.gitignore`

---

## 🧪 Running Tests

Install test dependencies:
```bash
pip install pytest pytest-asyncio
```

Run all tests:
```bash
pytest tests/ -v
```

Expected output:
```
tests/test_link_analysis.py::test_root_endpoint PASSED
tests/test_link_analysis.py::test_health_endpoint PASSED
tests/test_link_analysis.py::test_link_analysis_success PASSED
tests/test_link_analysis.py::test_link_analysis_invalid_url PASSED
tests/test_link_analysis.py::test_link_analysis_private_ip_blocked PASSED
tests/test_link_analysis.py::test_link_analysis_localhost_blocked PASSED
tests/test_link_analysis.py::test_link_analysis_missing_url PASSED
tests/test_link_analysis.py::test_url_validation PASSED
tests/test_link_analysis.py::test_url_ssrf_protection PASSED
```

---

## 🚀 Deployment

### Option 1: Deploy on Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Set environment variables in Railway dashboard: `GEMINI_API_KEY`, `APP_HOST=0.0.0.0`, `APP_PORT=4000`

### Option 2: Deploy on Render

1. Connect your GitHub repo to [render.com](https://render.com)
2. Set **Build Command:** `pip install -r requirements.txt`
3. Set **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add `GEMINI_API_KEY` as an environment variable

### Option 3: Deploy with Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 4000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000"]
```

```bash
docker build -t ai-link-analysis .
docker run -p 4000:4000 --env-file .env ai-link-analysis
```

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Core language |
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |
| **Pydantic v2** | Request/response validation |
| **HTTPX** | Async HTTP client for website fetching |
| **BeautifulSoup4** | HTML parsing |
| **Google Generative AI** | Gemini LLM integration |
| **python-dotenv** | Environment variable management |
| **pytest + pytest-asyncio** | Async test suite |

---

## 📧 Contact

Developed as part of the Dxora Technologies Python Practical Test.

---

*Built with ❤️ using FastAPI + Google Gemini AI*
