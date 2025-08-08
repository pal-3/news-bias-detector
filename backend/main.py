from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel
import random

app = FastAPI(title="Bias Lab API", version="0.1.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class BiasScores(BaseModel):
    ideological_stance: int  # 0-100 (0=far left, 50=center, 100=far right)
    factual_grounding: int   # 0-100 (higher = more factual)
    framing_choices: int     # 0-100 (higher = more manipulative framing)
    emotional_tone: int      # 0-100 (higher = more inflammatory)
    source_transparency: int # 0-100 (higher = better attribution)
    confidence: float        # 0-1 confidence interval

class BiasedPhrase(BaseModel):
    text: str
    start: int
    end: int
    dimension: str  # which bias dimension this phrase indicates
    explanation: str

class Article(BaseModel):
    id: str
    title: str
    source: str
    source_lean: str  # left, center, right
    published: datetime
    url: str
    excerpt: str
    full_text: str
    bias_scores: BiasScores
    biased_phrases: List[BiasedPhrase]
    narrative_cluster: str

class Narrative(BaseModel):
    id: str
    title: str
    article_count: int
    sources: List[str]
    average_bias: BiasScores
    divergence_score: float  # how differently outlets cover this
    trending: bool

# Mock Data for Trump Tariff Rebate Story
MOCK_ARTICLES = [
    {
        "id": "cnn-001",
        "title": "Trump's Tariff Rebate Checks: Economic Relief or Political Theater?",
        "source": "CNN",
        "source_lean": "left",
        "published": datetime.now(),
        "url": "https://cnn.com/...",
        "excerpt": "Critics argue the proposed rebate checks are a political ploy ahead of primary season, with economists warning of inflationary pressures.",
        "full_text": "Critics argue the proposed rebate checks are a political ploy ahead of primary season, with economists warning of inflationary pressures. The plan, which Trump claims will 'put money back in hardworking Americans' pockets,' has drawn skepticism from fiscal conservatives who question the timing. Leading economists suggest the rebates could fuel inflation rather than provide meaningful relief. 'This is clearly about politics, not policy,' said one Democratic strategist.",
        "bias_scores": {
            "ideological_stance": 25,
            "factual_grounding": 72,
            "framing_choices": 65,
            "emotional_tone": 45,
            "source_transparency": 78,
            "confidence": 0.85
        },
        "biased_phrases": [
            {
                "text": "political ploy",
                "start": 35,
                "end": 49,
                "dimension": "framing_choices",
                "explanation": "Frames policy as manipulative rather than genuine"
            },
            {
                "text": "Critics argue",
                "start": 0,
                "end": 13,
                "dimension": "ideological_stance",
                "explanation": "Leads with opposition perspective"
            }
        ],
        "narrative_cluster": "tariff-rebates"
    },
    {
        "id": "fox-001",
        "title": "Trump Delivers: Rebate Checks to Offset Biden's Inflation Crisis",
        "source": "Fox News",
        "source_lean": "right",
        "published": datetime.now(),
        "url": "https://foxnews.com/...",
        "excerpt": "President Trump's bold plan to return tariff revenue directly to American families offers real relief from the Biden administration's economic failures.",
        "full_text": "President Trump's bold plan to return tariff revenue directly to American families offers real relief from the Biden administration's economic failures. The rebate checks, ranging from $500 to $2000 per household, will help struggling families cope with skyrocketing prices. Trump stated, 'We're putting America First by returning China's tariff payments directly to the people.' Conservative economists praise the move as 'innovative fiscal policy' that rewards working Americans.",
        "bias_scores": {
            "ideological_stance": 78,
            "factual_grounding": 68,
            "framing_choices": 72,
            "emotional_tone": 58,
            "source_transparency": 71,
            "confidence": 0.87
        },
        "biased_phrases": [
            {
                "text": "Biden's Inflation Crisis",
                "start": 75,
                "end": 99,
                "dimension": "framing_choices",
                "explanation": "Attributes complex economic issue to single administration"
            },
            {
                "text": "Trump Delivers",
                "start": 0,
                "end": 14,
                "dimension": "emotional_tone",
                "explanation": "Heroic framing without policy details"
            },
            {
                "text": "bold plan",
                "start": 22,
                "end": 31,
                "dimension": "ideological_stance",
                "explanation": "Positive characterization of policy"
            }
        ],
        "narrative_cluster": "tariff-rebates"
    },
    {
        "id": "reuters-001",
        "title": "Trump Proposes Tariff Revenue Rebates to American Households",
        "source": "Reuters",
        "source_lean": "center",
        "published": datetime.now(),
        "url": "https://reuters.com/...",
        "excerpt": "Former President Trump announced a plan to distribute tariff revenues as direct payments to Americans, with details remaining unclear.",
        "full_text": "Former President Trump announced a plan to distribute tariff revenues as direct payments to Americans, with details remaining unclear. The proposal would allocate approximately $50 billion in collected tariff revenues for direct household payments. Treasury analysts note implementation challenges and potential trade partner responses. The rebates would range from $500-2000 based on household size, though funding mechanisms require congressional approval.",
        "bias_scores": {
            "ideological_stance": 50,
            "factual_grounding": 88,
            "framing_choices": 25,
            "emotional_tone": 15,
            "source_transparency": 92,
            "confidence": 0.91
        },
        "biased_phrases": [
            {
                "text": "details remaining unclear",
                "start": 98,
                "end": 123,
                "dimension": "factual_grounding",
                "explanation": "Highlights uncertainty without speculation"
            }
        ],
        "narrative_cluster": "tariff-rebates"
    },
    {
        "id": "wsj-001",
        "title": "Tariff Rebate Proposal Faces Economic Scrutiny",
        "source": "Wall Street Journal",
        "source_lean": "center",
        "published": datetime.now(),
        "url": "https://wsj.com/...",
        "excerpt": "Economists question the fiscal impact of Trump's proposed tariff rebate system on federal revenues and trade relationships.",
        "full_text": "Economists question the fiscal impact of Trump's proposed tariff rebate system on federal revenues and trade relationships. The plan would redistribute an estimated $50-75 billion in tariff collections directly to households. Federal Reserve officials express concern about potential inflationary effects. Trade partners may retaliate with their own tariff adjustments, potentially escalating trade tensions. Market analysts project a 0.3% GDP impact if implemented.",
        "bias_scores": {
            "ideological_stance": 48,
            "factual_grounding": 85,
            "framing_choices": 30,
            "emotional_tone": 20,
            "source_transparency": 89,
            "confidence": 0.88
        },
        "biased_phrases": [
            {
                "text": "Economists question",
                "start": 0,
                "end": 19,
                "dimension": "source_transparency",
                "explanation": "Cites expert perspective neutrally"
            }
        ],
        "narrative_cluster": "tariff-rebates"
    },
    {
        "id": "msnbc-001",
        "title": "Trump's Rebate Scheme: A Desperate Bid for Relevance",
        "source": "MSNBC",
        "source_lean": "left",
        "published": datetime.now(),
        "url": "https://msnbc.com/...",
        "excerpt": "The former president's latest proposal reveals a dangerous pattern of fiscal irresponsibility designed to buy voter support.",
        "full_text": "The former president's latest proposal reveals a dangerous pattern of fiscal irresponsibility designed to buy voter support. Experts warn that the rebate checks could destabilize carefully balanced trade agreements. Progressive economists call it 'a cynical attempt to purchase popularity' while ignoring climate and social priorities. The timing, coinciding with primary season, is hardly coincidental say political observers.",
        "bias_scores": {
            "ideological_stance": 18,
            "factual_grounding": 65,
            "framing_choices": 78,
            "emotional_tone": 72,
            "source_transparency": 70,
            "confidence": 0.83
        },
        "biased_phrases": [
            {
                "text": "Desperate Bid",
                "start": 22,
                "end": 35,
                "dimension": "emotional_tone",
                "explanation": "Emotionally charged characterization"
            },
            {
                "text": "dangerous pattern",
                "start": 58,
                "end": 75,
                "dimension": "framing_choices",
                "explanation": "Frames policy as threatening without specifics"
            },
            {
                "text": "cynical attempt",
                "start": 241,
                "end": 256,
                "dimension": "ideological_stance",
                "explanation": "Attributes negative motives"
            }
        ],
        "narrative_cluster": "tariff-rebates"
    }
]

# Add more articles for broader coverage
ADDITIONAL_ARTICLES = [
    {
        "id": "bloomberg-001",
        "title": "Fed Signals Concern Over Fiscal Stimulus Timing",
        "source": "Bloomberg",
        "source_lean": "center",
        "published": datetime.now(),
        "url": "https://bloomberg.com/...",
        "excerpt": "Federal Reserve officials privately express concerns about additional stimulus measures affecting monetary policy objectives.",
        "full_text": "Federal Reserve officials privately express concerns about additional stimulus measures affecting monetary policy objectives...",
        "bias_scores": {
            "ideological_stance": 52,
            "factual_grounding": 90,
            "framing_choices": 22,
            "emotional_tone": 12,
            "source_transparency": 88,
            "confidence": 0.92
        },
        "biased_phrases": [],
        "narrative_cluster": "fed-policy"
    },
    {
        "id": "nyt-001",
        "title": "How Tariff Policies Reshape American Trade Dynamics",
        "source": "New York Times",
        "source_lean": "left",
        "published": datetime.now(),
        "url": "https://nytimes.com/...",
        "excerpt": "A comprehensive analysis of how tariff revenues and rebate proposals reflect broader shifts in American trade policy.",
        "full_text": "A comprehensive analysis of how tariff revenues and rebate proposals reflect broader shifts in American trade policy...",
        "bias_scores": {
            "ideological_stance": 35,
            "factual_grounding": 82,
            "framing_choices": 38,
            "emotional_tone": 25,
            "source_transparency": 85,
            "confidence": 0.86
        },
        "biased_phrases": [],
        "narrative_cluster": "trade-analysis"
    }
]

# Combine all articles
ALL_ARTICLES = MOCK_ARTICLES + ADDITIONAL_ARTICLES

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Bias Lab API v0.1", "status": "running"}

@app.get("/api/articles", response_model=List[Article])
def get_articles(limit: int = 10, narrative: Optional[str] = None):
    """Get list of recent articles with bias scores"""
    articles = ALL_ARTICLES.copy()
    
    if narrative:
        articles = [a for a in articles if a.get("narrative_cluster") == narrative]
    
    return articles[:limit]

@app.get("/api/articles/{article_id}", response_model=Article)
def get_article(article_id: str):
    """Get detailed article breakdown with highlighted phrases"""
    article = next((a for a in ALL_ARTICLES if a["id"] == article_id), None)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.get("/api/narratives", response_model=List[Narrative])
def get_narratives():
    """Get clustered story framings"""
    narratives = [
        {
            "id": "tariff-rebates",
            "title": "Trump Tariff Rebate Checks",
            "article_count": 5,
            "sources": ["CNN", "Fox News", "Reuters", "WSJ", "MSNBC"],
            "average_bias": {
                "ideological_stance": 48,
                "factual_grounding": 75,
                "framing_choices": 48,
                "emotional_tone": 38,
                "source_transparency": 79,
                "confidence": 0.86
            },
            "divergence_score": 0.78,  # High divergence = very different coverage
            "trending": True
        },
        {
            "id": "fed-policy",
            "title": "Federal Reserve Policy Response",
            "article_count": 2,
            "sources": ["Bloomberg", "WSJ"],
            "average_bias": {
                "ideological_stance": 51,
                "factual_grounding": 88,
                "framing_choices": 26,
                "emotional_tone": 15,
                "source_transparency": 87,
                "confidence": 0.90
            },
            "divergence_score": 0.15,
            "trending": False
        },
        {
            "id": "trade-analysis",
            "title": "US-China Trade Relations",
            "article_count": 3,
            "sources": ["NYT", "Reuters", "Bloomberg"],
            "average_bias": {
                "ideological_stance": 42,
                "factual_grounding": 83,
                "framing_choices": 32,
                "emotional_tone": 22,
                "source_transparency": 84,
                "confidence": 0.87
            },
            "divergence_score": 0.35,
            "trending": True
        }
    ]
    return narratives

@app.get("/api/comparison/{article_id1}/{article_id2}")
def compare_articles(article_id1: str, article_id2: str):
    """Compare bias between two articles covering the same story"""
    art1 = next((a for a in ALL_ARTICLES if a["id"] == article_id1), None)
    art2 = next((a for a in ALL_ARTICLES if a["id"] == article_id2), None)
    
    if not art1 or not art2:
        raise HTTPException(status_code=404, detail="Article(s) not found")
    
    return {
        "article1": art1,
        "article2": art2,
        "bias_delta": {
            "ideological_stance": abs(art1["bias_scores"]["ideological_stance"] - art2["bias_scores"]["ideological_stance"]),
            "factual_grounding": abs(art1["bias_scores"]["factual_grounding"] - art2["bias_scores"]["factual_grounding"]),
            "framing_choices": abs(art1["bias_scores"]["framing_choices"] - art2["bias_scores"]["framing_choices"]),
            "emotional_tone": abs(art1["bias_scores"]["emotional_tone"] - art2["bias_scores"]["emotional_tone"]),
            "source_transparency": abs(art1["bias_scores"]["source_transparency"] - art2["bias_scores"]["source_transparency"])
        },
        "same_facts_different_spin": [
            {
                "fact": "Rebate amounts range from $500-2000",
                "article1_framing": "will help struggling families",
                "article2_framing": "could destabilize trade agreements"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)