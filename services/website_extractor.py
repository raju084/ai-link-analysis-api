import httpx
from bs4 import BeautifulSoup
import re
from dataclasses import dataclass, field
from fastapi import HTTPException


BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}


@dataclass
class WebsiteContent:
    url: str
    title: str = ""
    description: str = ""
    keywords: str = ""
    headings: list = field(default_factory=list)
    main_text: str = ""
    nav_items: list = field(default_factory=list)
    footer_text: str = ""
    og_data: dict = field(default_factory=dict)
    full_text: str = ""
    word_count: int = 0


def _clean_text(text: str) -> str:
    """Clean and normalize whitespace in text."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def _extract_meta(soup: BeautifulSoup, name: str = None, property: str = None) -> str:
    """Extract meta tag content."""
    if name:
        tag = soup.find("meta", attrs={"name": name})
    elif property:
        tag = soup.find("meta", attrs={"property": property})
    else:
        return ""
    return tag.get("content", "").strip() if tag else ""


async def extract_website_content(url: str, timeout: int = 30) -> WebsiteContent:
    """
    Fetch and extract clean content from a website URL.
    
    Args:
        url: The website URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        WebsiteContent dataclass with extracted content
        
    Raises:
        HTTPException: On fetch errors
    """
    try:
        async with httpx.AsyncClient(
            headers=BROWSER_HEADERS,
            follow_redirects=True,
            max_redirects=5,
            timeout=httpx.Timeout(timeout),
            verify=True,
        ) as client:
            response = await client.get(url)
            
            if response.status_code == 403:
                raise HTTPException(
                    status_code=502,
                    detail=f"Website returned 403 Forbidden. The site may block automated access."
                )
            elif response.status_code == 404:
                raise HTTPException(
                    status_code=502,
                    detail=f"Website returned 404 Not Found."
                )
            elif response.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f"Website returned HTTP {response.status_code}. Cannot fetch content."
                )
            
            html = response.text
            
    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail=f"Request timed out after {timeout} seconds. The website may be slow or unreachable."
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch website: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while fetching website: {str(e)}"
        )
    
    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")
    
    # Extract title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    # Extract meta tags
    description = _extract_meta(soup, name="description")
    keywords = _extract_meta(soup, name="keywords")
    
    # Extract Open Graph data
    og_data = {
        "title": _extract_meta(soup, property="og:title"),
        "description": _extract_meta(soup, property="og:description"),
        "type": _extract_meta(soup, property="og:type"),
        "site_name": _extract_meta(soup, property="og:site_name"),
        "url": _extract_meta(soup, property="og:url"),
    }
    
    # Extract headings
    headings = []
    for tag in ["h1", "h2", "h3", "h4"]:
        for heading in soup.find_all(tag)[:20]:
            text = heading.get_text(strip=True)
            if text and len(text) > 2:
                headings.append(f"{tag.upper()}: {text}")
    headings = headings[:20]
    
    # Extract nav items
    nav_items = []
    nav_tags = soup.find_all(["nav", "header"])
    for nav in nav_tags:
        for a in nav.find_all("a"):
            text = a.get_text(strip=True)
            if text and len(text) > 1 and len(text) < 60:
                nav_items.append(text)
    nav_items = list(dict.fromkeys(nav_items))[:15]  # deduplicate
    
    # Extract footer text
    footer = soup.find("footer")
    footer_text = ""
    if footer:
        footer_text = _clean_text(footer.get_text())[:500]
    
    # Remove unwanted tags for main text extraction
    for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe"]):
        tag.decompose()
    
    # Extract main text
    main_text = _clean_text(soup.get_text(separator=" "))[:8000]
    
    # Build full text for LLM (combine all extracted info)
    parts = []
    if title:
        parts.append(f"PAGE TITLE: {title}")
    if og_data.get("site_name"):
        parts.append(f"SITE NAME: {og_data['site_name']}")
    if description:
        parts.append(f"META DESCRIPTION: {description}")
    if og_data.get("description"):
        parts.append(f"OG DESCRIPTION: {og_data['description']}")
    if keywords:
        parts.append(f"META KEYWORDS: {keywords}")
    if headings:
        parts.append(f"HEADINGS:\n" + "\n".join(headings))
    if nav_items:
        parts.append(f"NAVIGATION ITEMS: {', '.join(nav_items)}")
    if main_text:
        parts.append(f"MAIN CONTENT:\n{main_text}")
    if footer_text:
        parts.append(f"FOOTER: {footer_text}")
    
    full_text = "\n\n".join(parts)[:15000]
    word_count = len(full_text.split())
    
    return WebsiteContent(
        url=url,
        title=title,
        description=description,
        keywords=keywords,
        headings=headings,
        main_text=main_text,
        nav_items=nav_items,
        footer_text=footer_text,
        og_data=og_data,
        full_text=full_text,
        word_count=word_count,
    )
