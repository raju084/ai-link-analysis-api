import os
import json
import asyncio
import re
import logging
from typing import TYPE_CHECKING
from fastapi import HTTPException
import google.generativeai as genai

logger = logging.getLogger(__name__)

# --- Lazy model initialization ---
_model = None

def _get_model():
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="GEMINI_API_KEY is not configured. Please set it in your .env file."
            )
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=8192,
                response_mime_type="application/json",
            ),
        )
    return _model


def build_analysis_prompt(content) -> str:
    """Build a structured prompt for Gemini analysis."""
    website_data = f"""
WEBSITE URL: {content.url}
WORD COUNT: {content.word_count}

{content.full_text}
""".strip()

    # Truncate if too long
    if len(website_data) > 12000:
        website_data = website_data[:12000] + "\n[Content truncated for analysis]"

    prompt = f"""You are an expert business analyst, SEO specialist, and digital marketing consultant.

Analyze the following website content and return a comprehensive JSON analysis.

WEBSITE CONTENT:
{website_data}

INSTRUCTIONS:
1. Analyze ONLY the actual website content provided above. Do not make up information not present.
2. Identify the brand name, business category, and what the company does.
3. Identify at least 3 real, well-known competitors based on the business type/industry.
4. Generate exactly 5 target search queries across different platforms.
5. Provide detailed SEO improvements based on the actual content.
6. Identify exactly 5 top services from the website (infer from content if needed, label inferred ones).
7. Identify target audience segments based on the business.
8. For competitor weaknesses and strengths, base on general industry knowledge.
9. Do NOT invent search volume numbers or rankings.
10. Return ONLY valid JSON — no markdown, no code blocks, no extra text.

Return this exact JSON structure:
{{
  "brand": {{
    "name": "Brand name from website",
    "category": "Main business category",
    "summary": "2-3 sentence business overview"
  }},
  "competitor_analysis": {{
    "brand_name": "Brand name",
    "brand_overview": "Detailed overview of this brand",
    "main_category": "Main business category",
    "main_products_services": ["Service 1", "Service 2", "Service 3"],
    "competitors": [
      {{
        "name": "Competitor Name",
        "overview": "Brief overview of competitor",
        "strengths": ["Strength 1", "Strength 2"],
        "weaknesses": ["Weakness 1", "Weakness 2"]
      }}
    ],
    "your_brand_strengths": ["Strength 1", "Strength 2", "Strength 3"],
    "competitive_advantages": ["Advantage 1", "Advantage 2"],
    "opportunities": ["Opportunity 1", "Opportunity 2", "Opportunity 3"]
  }},
  "target_search_queries": [
    {{
      "query": "search query here",
      "platforms": ["Google"],
      "intent": "Service Search",
      "business_relevance": "Why this query matters for the business",
      "target_audience": "Who would search this"
    }},
    {{
      "query": "another search query",
      "platforms": ["Facebook"],
      "intent": "Business Discovery",
      "business_relevance": "Why this query matters",
      "target_audience": "Target audience description"
    }},
    {{
      "query": "visual search query",
      "platforms": ["Instagram"],
      "intent": "Inspiration",
      "business_relevance": "Why this query matters",
      "target_audience": "Target audience description"
    }},
    {{
      "query": "professional search query",
      "platforms": ["LinkedIn"],
      "intent": "B2B Search",
      "business_relevance": "Why this query matters",
      "target_audience": "Target audience description"
    }},
    {{
      "query": "trending search query",
      "platforms": ["X"],
      "intent": "Service Discovery",
      "business_relevance": "Why this query matters",
      "target_audience": "Target audience description"
    }}
  ],
  "seo_improvements": {{
    "keywords": {{
      "primary_keyword": "Main keyword",
      "secondary_keywords": ["keyword1", "keyword2", "keyword3"],
      "long_tail_keywords": ["long tail 1", "long tail 2", "long tail 3"],
      "relevant_business_keywords": ["biz keyword1", "biz keyword2", "biz keyword3"]
    }},
    "seo_title": {{
      "recommended_title": "Optimized SEO Title | Brand Name",
      "primary_keyword": "primary keyword used",
      "improved_structure_notes": "Explanation of title improvements"
    }},
    "meta_description": {{
      "recommended_description": "Compelling 150-160 character meta description with keywords.",
      "business_summary": "One line human-friendly business summary",
      "keywords_used": ["keyword1", "keyword2"]
    }},
    "additional_content": [
      {{
        "type": "Service Landing Page",
        "title": "Page title suggestion",
        "description": "What this page should cover"
      }},
      {{
        "type": "Blog Post",
        "title": "Blog title suggestion",
        "description": "What this blog post should cover"
      }},
      {{
        "type": "FAQ Page",
        "title": "Frequently Asked Questions",
        "description": "Common questions to address"
      }},
      {{
        "type": "Industry Page",
        "title": "Industry-specific page",
        "description": "Target industry content"
      }},
      {{
        "type": "Location Page",
        "title": "Location-based page",
        "description": "Geographic targeting content"
      }}
    ]
  }},
  "top_services": [
    {{
      "name": "Service Name",
      "description": "Service description",
      "target_industry": "Target industry",
      "target_customer": "Customer type",
      "main_benefit": "Primary customer benefit"
    }}
  ],
  "target_audience": {{
    "primary_audience": [
      {{
        "audience_name": "Audience Name",
        "business_type": "Business Type",
        "requirement": "What they need",
        "customer_profile": "Detailed customer profile",
        "needs_challenges": ["Need 1", "Challenge 1"]
      }}
    ],
    "secondary_audience": [
      {{
        "audience_name": "Secondary Audience",
        "business_type": "Business Type",
        "requirement": "What they need",
        "customer_profile": "Profile",
        "needs_challenges": ["Need 1"]
      }}
    ],
    "industries": ["Industry 1", "Industry 2", "Industry 3"],
    "business_types": ["Type 1", "Type 2"],
    "location_focus": "Geographic focus if identifiable, else 'Global'",
    "interests": ["Interest 1", "Interest 2", "Interest 3"],
    "recommended_segments": ["Segment 1", "Segment 2", "Segment 3"]
  }}
}}

Remember: Return ONLY the JSON object above. No explanations, no markdown code blocks.
"""
    return prompt


def _parse_json_response(text: str) -> dict:
    """Parse JSON from LLM response, handling markdown code blocks."""
    # Remove markdown code blocks if present
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
        text = text.strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}\nResponse text: {text[:500]}")
        raise HTTPException(
            status_code=500,
            detail=f"LLM returned invalid JSON response. Please try again."
        )


async def analyze_website_with_llm(content) -> dict:
    """
    Analyze website content using Google Gemini LLM.
    
    Args:
        content: WebsiteContent dataclass instance
        
    Returns:
        dict with all 5 analysis sections + brand info
        
    Raises:
        HTTPException: On API or parsing errors
    """
    prompt = build_analysis_prompt(content)
    
    try:
        model = _get_model()
        
        # Run synchronous Gemini call in thread pool
        response = await asyncio.to_thread(model.generate_content, prompt)
        
        if not response.text:
            raise HTTPException(
                status_code=500,
                detail="LLM returned an empty response. Please try again."
            )
        
        result = _parse_json_response(response.text)
        logger.info(f"Successfully analyzed {content.url}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Gemini API error: {error_msg}")
        
        if "API_KEY" in error_msg.upper() or "api key" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail="Invalid or missing Gemini API key. Please check your GEMINI_API_KEY configuration."
            )
        elif ("quota" in error_msg.lower() or "429" in error_msg) and "not found" not in error_msg.lower():
            raise HTTPException(
                status_code=429,
                detail="Gemini API rate limit exceeded. Please try again later."
            )
        elif "not found" in error_msg.lower() or "404" in error_msg:
            raise HTTPException(
                status_code=503,
                detail=f"Gemini model not available. Please check your API key permissions or model name. Detail: {error_msg}"
            )
        else:
            raise HTTPException(
                status_code=503,
                detail=f"LLM service error: {error_msg}"
            )
