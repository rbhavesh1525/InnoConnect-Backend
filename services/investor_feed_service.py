"""
Investor Feed Service
=====================
Fetches personalized project recommendations for an investor by:
1. Pulling their verified interests (preferred_industries, startup_stages,
   investor_type) from the investor_verification_requests table.
2. Building a natural-language query string from those interests.
3. Generating a sentence embedding for the query.
4. Running cosine-similarity against all stored project embeddings.
5. Returning the top-N most relevant projects.
"""

import json
import numpy as np

from database.dbconfig import get_supabase_client
from app.embeddings import generate_embedding
from app.repository import get_all_embeddings
from app.vector_utils import parse_vector
from app.similarity import find_similar

supabase = get_supabase_client()


def _safe_list(val):
    """Parse Supabase array field that may be a JSON string or already a list."""
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        try:
            return json.loads(val)
        except Exception:
            return [val]
    return []


# ── Actual project industry_category values in the DB ────────────────────────
# ['AI', 'Agriculture', 'Cybersecurity', 'EdTech', 'Energy', 'FinTech',
#  'Healthcare', 'IoT', 'Logistics', 'Smart Cities']
# Each has exactly 10 projects (100 total).

# Maps investor form label → rich vocabulary aligned with actual project categories
INDUSTRY_EXPANSION = {
    # Form: "FinTech"  ↔  DB category: "FinTech"
    "FinTech": (
        "FinTech financial technology banking payments digital finance "
        "investment portfolio wealth management insurance lending credit "
        "blockchain cryptocurrency digital wallet neobank stock trading"
    ),
    # Form: "HealthTech"  ↔  DB category: "Healthcare"
    "HealthTech": (
        "Healthcare health medical technology telemedicine digital health "
        "patient monitoring diagnostics hospital clinical wearable fitness "
        "mental health wellness pharmaceutical electronic health records"
    ),
    # Form: "EdTech"  ↔  DB category: "EdTech"
    "EdTech": (
        "EdTech education technology e-learning online learning student "
        "training skill development courses tutoring university academic "
        "gamification assessment curriculum personalized learning AI tutor"
    ),
    # Form: "AI/ML"  ↔  DB category: "AI"
    "AI/ML": (
        "AI artificial intelligence machine learning deep learning neural network "
        "natural language processing computer vision data science automation "
        "predictive analytics recommendation system generative AI chatbot "
        "large language model intelligent system"
    ),
    # Form: "Agriculture"  ↔  DB category: "Agriculture"
    "Agriculture": (
        "Agriculture farming precision farming crop monitoring irrigation "
        "smart farming livestock supply chain food technology rural farmer "
        "yield optimization drone satellite agri-tech sensor soil"
    ),
    # Form: "E-Commerce"  ↔  DB category: "Logistics" (closest match in DB)
    "E-Commerce": (
        "Logistics e-commerce online shopping marketplace retail consumer "
        "supply chain delivery fulfillment inventory management shipping "
        "last-mile tracking warehouse distribution"
    ),
    # Form: "Clean Energy"  ↔  DB category: "Energy"
    "Clean Energy": (
        "Energy clean energy renewable energy solar wind electric vehicle "
        "sustainability green technology carbon emission climate change "
        "energy storage battery smart grid energy efficiency environment"
    ),
    # Form: "SaaS"  ↔  DB categories: "IoT" + "Smart Cities" + "Cybersecurity"
    "SaaS": (
        "IoT Smart Cities Cybersecurity software as a service cloud platform "
        "subscription B2B enterprise productivity tool workflow automation "
        "internet of things connected devices smart infrastructure security "
        "data privacy network threat detection dashboard analytics"
    ),
}

# Direct alias: investor form label → closest actual DB industry_category
# Used for logging and future filtering enhancements
CATEGORY_ALIAS = {
    "FinTech":      "FinTech",
    "HealthTech":   "Healthcare",
    "EdTech":       "EdTech",
    "AI/ML":        "AI",
    "Agriculture":  "Agriculture",
    "E-Commerce":   "Logistics",
    "Clean Energy": "Energy",
    "SaaS":         "IoT",
}

STAGE_EXPANSION = {
    "Idea":      "early stage idea concept pre-seed exploration proof of concept",
    "Prototype": "prototype proof of concept early build mockup pilot testing validation",
    "MVP":       "minimum viable product MVP early traction first users beta launch",
    "Seed":      "seed stage seed funding early revenue growing user base product-market fit",
    "Series A":  "Series A scaling growth funded team expansion revenue traction",
}



def _build_investor_query(record: dict) -> str:
    """
    Build a rich semantic query string from investor interest labels.
    Each label is expanded into descriptive vocabulary that closely
    matches how project problem statements and solutions are written.
    """
    industries = _safe_list(record.get("preferred_industries", []))
    stages     = _safe_list(record.get("startup_stages", []))
    inv_type   = record.get("investor_type", "")

    parts = []

    # Expand each industry into rich descriptive text
    industry_expansions = []
    for ind in industries:
        expansion = INDUSTRY_EXPANSION.get(ind)
        if expansion:
            industry_expansions.append(expansion)
        else:
            industry_expansions.append(ind)  # fallback to raw label

    # Expand each stage
    stage_expansions = []
    for stage in stages:
        expansion = STAGE_EXPANSION.get(stage)
        if expansion:
            stage_expansions.append(expansion)
        else:
            stage_expansions.append(stage)

    if inv_type:
        parts.append(f"Investor profile: {inv_type}.")

    if industry_expansions:
        parts.append(
            "Interested in startups and projects focused on: "
            + " | ".join(industry_expansions)
        )

    if stage_expansions:
        parts.append(
            "Preferred startup stages: "
            + " | ".join(stage_expansions)
        )

    if not parts:
        parts.append(
            "startup innovation technology product solution problem solving "
            "market opportunity scalable business"
        )

    return " ".join(parts)


def get_investor_feed(user_id: str, top_k: int = 10):
    """
    Return personalised project feed for an investor.
    Uses per-industry embeddings + max-score pooling so that
    no single industry dominates the results.
    Falls back to unranked projects if no approved verification exists.
    """
    try:
        # ── 1. Fetch investor interest profile ──────────────────────────
        result = (
            supabase
            .table("investor_verification_requests")
            .select(
                "preferred_industries, startup_stages, "
                "investor_type, status"
            )
            .eq("user_id", user_id)
            .eq("status", "approved")
            .order("id", desc=True)
            .limit(1)
            .execute()
        )

        rows = get_all_embeddings()
        valid_rows = [r for r in rows if r.get("embedding") is not None and r.get("project_title")]

        # ── 2. No approved profile → generic unranked feed ───────────────
        if not result.data:
            print(f"[INVESTOR FEED] No approved verification for {user_id}. Generic feed.")
            generic = [
                {
                    "project_id":        r["id"],
                    "project_title":     r["project_title"],
                    "description":       r.get("description"),
                    "problem_statement": r.get("problem_statement"),
                    "solution_overview": r.get("solution_overview"),
                    "industry":          r.get("industry_category"),
                    "owner":             r.get("owner"),
                    "owner_id":          r.get("owner_id"),
                    "similarity":        None,
                }
                for r in valid_rows
            ]
            
            # Sort generic feed to prioritize real projects
            generic.sort(key=lambda x: x.get("owner_id") is not None, reverse=True)
            
            return {
                "success": True,
                "personalised": False,
                "count": len(generic[:top_k]),
                "data": generic[:top_k],
            }

        investor_record = result.data[0]
        industries = _safe_list(investor_record.get("preferred_industries", []))
        stages     = _safe_list(investor_record.get("startup_stages", []))
        inv_type   = investor_record.get("investor_type", "")

        print(f"[INVESTOR FEED] User {user_id}: industries={industries}, stages={stages}")

        if not valid_rows:
            return {"success": True, "personalised": True, "count": 0, "data": []}

        project_embeddings = np.array([parse_vector(r["embedding"]) for r in valid_rows])

        # ── 3. Build one query per industry ─────────────────────────────
        # Each industry gets its own embedding so no single domain
        # dominates the pooled result vector.

        # Stage suffix shared across all industry queries
        stage_suffix = ""
        if stages:
            stage_texts = [STAGE_EXPANSION.get(s, s) for s in stages]
            stage_suffix = " Startup stage: " + " ".join(stage_texts)

        type_prefix = f"{inv_type} investor interested in: " if inv_type else "Investor interested in: "

        query_texts = []
        if industries:
            for ind in industries:
                expansion = INDUSTRY_EXPANSION.get(ind, ind)
                query_texts.append(type_prefix + expansion + stage_suffix)
        else:
            # Fallback: generic startup query
            query_texts.append(
                "startup innovation technology product solution problem solving "
                "market opportunity scalable business" + stage_suffix
            )

        n_industries = len(query_texts)
        print(f"[INVESTOR FEED] Generating {n_industries} industry embeddings (quota mode)...")

        # ── 4. Per-industry quota bucketing ──────────────────────────────
        # Allocate slots_per_industry to each industry so the feed is ALWAYS
        # diverse, regardless of how skewed the project corpus is.
        # e.g. 4 industries, top_k=10 → 3 slots each (last industry gets 1 extra)

        slots_per_industry = max(1, top_k // n_industries)
        # Last industry absorbs any remainder
        slots = [slots_per_industry] * n_industries
        slots[-1] += top_k - slots_per_industry * n_industries

        n_projects = len(valid_rows)
        seen_ids   = set()   # prevent duplicates across buckets
        buckets    = []      # list of (similarity, project_dict) per industry

        for bucket_idx, (query_text, quota) in enumerate(zip(query_texts, slots)):
            query_emb = generate_embedding(query_text)
            ranked_idxs, scores = find_similar(query_emb, project_embeddings, top_k=n_projects)

            ind_label = industries[bucket_idx] if bucket_idx < len(industries) else "General"
            collected = 0

            for idx in ranked_idxs:
                p   = valid_rows[idx]
                pid = p["id"]

                if pid in seen_ids:
                    continue

                similarity = round(float(scores[idx]), 4)

                seen_ids.add(pid)
                buckets.append({
                    "project_id":        pid,
                    "project_title":     p["project_title"],
                    "description":       p.get("description"),
                    "problem_statement": p.get("problem_statement"),
                    "solution_overview": p.get("solution_overview"),
                    "industry":          p.get("industry_category"),
                    "owner":             p.get("owner"),
                    "owner_id":          p.get("owner_id"),
                    "similarity":        similarity,
                    "_bucket":           ind_label,
                })
                collected += 1
                if collected >= quota:
                    break

            print(f"[INVESTOR FEED]   [{ind_label}] collected {collected}/{quota} projects")

        # ── 5. Sort final list by (is_real, similarity) (best first) ──────────
        # Real projects have a non-null owner_id. We prioritize them over synthetic projects.
        results = sorted(buckets, key=lambda x: (x.get("owner_id") is not None, x.get("similarity", 0)), reverse=True)

        # Remove internal _bucket key before returning
        for r in results:
            r.pop("_bucket", None)

        print(f"[INVESTOR FEED] Returning {len(results)} diverse projects")

        return {
            "success":      True,
            "personalised": True,
            "industries":   industries,
            "count":        len(results),
            "data":         results,
        }

    except Exception as e:
        print(f"[INVESTOR FEED ERROR] {str(e)}")
        return {"success": False, "message": str(e)}

