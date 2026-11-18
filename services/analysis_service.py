import logging
from app.schemas import (
    BrandInfo, CompetitorInfo, CompetitorAnalysis, SearchQuery,
    SEOKeywords, SEOTitle, MetaDescription, SupportingContent, SEOImprovements,
    ServiceInfo, AudienceSegment, TargetAudience, AnalysisResult
)

logger = logging.getLogger(__name__)


def _safe_list(data: dict, key: str, default=None) -> list:
    """Safely extract a list from dict."""
    val = data.get(key, default or [])
    return val if isinstance(val, list) else []


def _safe_str(data: dict, key: str, default: str = "") -> str:
    """Safely extract a string from dict."""
    val = data.get(key, default)
    return str(val) if val is not None else default


def map_llm_response_to_schemas(llm_data: dict) -> tuple[BrandInfo, AnalysisResult]:
    """
    Map raw LLM JSON response to Pydantic schema models.
    
    Args:
        llm_data: Raw dict from LLM JSON response
        
    Returns:
        Tuple of (BrandInfo, AnalysisResult)
    """
    # --- Brand ---
    brand_data = llm_data.get("brand", {})
    brand = BrandInfo(
        name=_safe_str(brand_data, "name", "Unknown Brand"),
        category=_safe_str(brand_data, "category", "Unknown Category"),
        summary=_safe_str(brand_data, "summary", "No summary available."),
    )
    
    # --- Competitor Analysis ---
    ca_data = llm_data.get("competitor_analysis", {})
    competitors = []
    for c in _safe_list(ca_data, "competitors"):
        if isinstance(c, dict):
            competitors.append(CompetitorInfo(
                name=_safe_str(c, "name", "Unknown"),
                overview=_safe_str(c, "overview", ""),
                strengths=_safe_list(c, "strengths"),
                weaknesses=_safe_list(c, "weaknesses"),
            ))
    
    competitor_analysis = CompetitorAnalysis(
        brand_name=_safe_str(ca_data, "brand_name", brand.name),
        brand_overview=_safe_str(ca_data, "brand_overview", brand.summary),
        main_category=_safe_str(ca_data, "main_category", brand.category),
        main_products_services=_safe_list(ca_data, "main_products_services"),
        competitors=competitors,
        your_brand_strengths=_safe_list(ca_data, "your_brand_strengths"),
        competitive_advantages=_safe_list(ca_data, "competitive_advantages"),
        opportunities=_safe_list(ca_data, "opportunities"),
    )
    
    # --- Target Search Queries ---
    search_queries = []
    for q in _safe_list(llm_data, "target_search_queries"):
        if isinstance(q, dict):
            search_queries.append(SearchQuery(
                query=_safe_str(q, "query", ""),
                platforms=_safe_list(q, "platforms"),
                intent=_safe_str(q, "intent", ""),
                business_relevance=_safe_str(q, "business_relevance", ""),
                target_audience=_safe_str(q, "target_audience", ""),
            ))
    
    # --- SEO Improvements ---
    seo_data = llm_data.get("seo_improvements", {})
    kw_data = seo_data.get("keywords", {})
    keywords = SEOKeywords(
        primary_keyword=_safe_str(kw_data, "primary_keyword", ""),
        secondary_keywords=_safe_list(kw_data, "secondary_keywords"),
        long_tail_keywords=_safe_list(kw_data, "long_tail_keywords"),
        relevant_business_keywords=_safe_list(kw_data, "relevant_business_keywords"),
    )
    
    title_data = seo_data.get("seo_title", {})
    seo_title = SEOTitle(
        recommended_title=_safe_str(title_data, "recommended_title", ""),
        primary_keyword=_safe_str(title_data, "primary_keyword", ""),
        improved_structure_notes=_safe_str(title_data, "improved_structure_notes", ""),
    )
    
    meta_data = seo_data.get("meta_description", {})
    meta_description = MetaDescription(
        recommended_description=_safe_str(meta_data, "recommended_description", ""),
        business_summary=_safe_str(meta_data, "business_summary", ""),
        keywords_used=_safe_list(meta_data, "keywords_used"),
    )
    
    additional_content = []
    for ac in _safe_list(seo_data, "additional_content"):
        if isinstance(ac, dict):
            additional_content.append(SupportingContent(
                type=_safe_str(ac, "type", ""),
                title=_safe_str(ac, "title", ""),
                description=_safe_str(ac, "description", ""),
            ))
    
    seo_improvements = SEOImprovements(
        keywords=keywords,
        seo_title=seo_title,
        meta_description=meta_description,
        additional_content=additional_content,
    )
    
    # --- Top Services ---
    top_services = []
    for svc in _safe_list(llm_data, "top_services"):
        if isinstance(svc, dict):
            top_services.append(ServiceInfo(
                name=_safe_str(svc, "name", ""),
                description=_safe_str(svc, "description", ""),
                target_industry=_safe_str(svc, "target_industry", ""),
                target_customer=_safe_str(svc, "target_customer", ""),
                main_benefit=_safe_str(svc, "main_benefit", ""),
            ))
    
    # --- Target Audience ---
    ta_data = llm_data.get("target_audience", {})
    
    def parse_audience_segments(segments_data: list) -> list:
        segments = []
        for seg in segments_data:
            if isinstance(seg, dict):
                segments.append(AudienceSegment(
                    audience_name=_safe_str(seg, "audience_name", ""),
                    business_type=_safe_str(seg, "business_type", ""),
                    requirement=_safe_str(seg, "requirement", ""),
                    customer_profile=_safe_str(seg, "customer_profile", ""),
                    needs_challenges=_safe_list(seg, "needs_challenges"),
                ))
        return segments
    
    target_audience = TargetAudience(
        primary_audience=parse_audience_segments(_safe_list(ta_data, "primary_audience")),
        secondary_audience=parse_audience_segments(_safe_list(ta_data, "secondary_audience")),
        industries=_safe_list(ta_data, "industries"),
        business_types=_safe_list(ta_data, "business_types"),
        location_focus=_safe_str(ta_data, "location_focus", "Global"),
        interests=_safe_list(ta_data, "interests"),
        recommended_segments=_safe_list(ta_data, "recommended_segments"),
    )
    
    analysis = AnalysisResult(
        competitor_analysis=competitor_analysis,
        target_search_queries=search_queries,
        seo_improvements=seo_improvements,
        top_services=top_services,
        target_audience=target_audience,
    )
    
    return brand, analysis
