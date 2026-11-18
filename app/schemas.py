from pydantic import BaseModel
from typing import Optional, List


class LinkAnalysisRequest(BaseModel):
    url: str


class BrandInfo(BaseModel):
    name: str
    category: str
    summary: str


class CompetitorInfo(BaseModel):
    name: str
    overview: str
    strengths: List[str]
    weaknesses: List[str]


class CompetitorAnalysis(BaseModel):
    brand_name: str
    brand_overview: str
    main_category: str
    main_products_services: List[str]
    competitors: List[CompetitorInfo]
    your_brand_strengths: List[str]
    competitive_advantages: List[str]
    opportunities: List[str]


class SearchQuery(BaseModel):
    query: str
    platforms: List[str]
    intent: str
    business_relevance: str
    target_audience: str


class SEOKeywords(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str]
    long_tail_keywords: List[str]
    relevant_business_keywords: List[str]


class SEOTitle(BaseModel):
    recommended_title: str
    primary_keyword: str
    improved_structure_notes: str


class MetaDescription(BaseModel):
    recommended_description: str
    business_summary: str
    keywords_used: List[str]


class SupportingContent(BaseModel):
    type: str
    title: str
    description: str


class SEOImprovements(BaseModel):
    keywords: SEOKeywords
    seo_title: SEOTitle
    meta_description: MetaDescription
    additional_content: List[SupportingContent]


class ServiceInfo(BaseModel):
    name: str
    description: str
    target_industry: str
    target_customer: str
    main_benefit: str


class AudienceSegment(BaseModel):
    audience_name: str
    business_type: str
    requirement: str
    customer_profile: str
    needs_challenges: List[str]


class TargetAudience(BaseModel):
    primary_audience: List[AudienceSegment]
    secondary_audience: List[AudienceSegment]
    industries: List[str]
    business_types: List[str]
    location_focus: str
    interests: List[str]
    recommended_segments: List[str]


class AnalysisResult(BaseModel):
    competitor_analysis: CompetitorAnalysis
    target_search_queries: List[SearchQuery]
    seo_improvements: SEOImprovements
    top_services: List[ServiceInfo]
    target_audience: TargetAudience


class LinkAnalysisResponse(BaseModel):
    success: bool
    website: str
    brand: Optional[BrandInfo] = None
    analysis: Optional[AnalysisResult] = None
    error: Optional[str] = None
