from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_innovation_guidance(project, similar_projects):

    similar_projects_text = "\n".join([
        f"- {p['project_title']} "
        f"(Industry: {p['industry']}, "
        f"Similarity: {p['similarity']})"
        for p in similar_projects
    ])

    if not similar_projects_text:
        similar_projects_text = "No similar projects found."

    prompt = f"""
You are an innovation mentor.

Analyze the project and provide actionable suggestions.

Project Title:
{project['project_title']}

Problem Statement:
{project['problem_statement']}

Solution Overview:
{project['solution_overview']}

Industry:
{project.get('industry_category', 'Unknown')}

Similar Projects:
{similar_projects_text}

Return ONLY valid JSON.

Rules:
- Do not include markdown.
- Do not wrap JSON in ```json blocks.
- Return valid JSON only.
- differentiators must contain exactly 5 items.
- unique_features must contain exactly 5 items.

JSON Schema:

{{
    "similarity_analysis": "",
    "differentiators": [],
    "unique_features": [],
    "improved_title": "",
    "rewritten_solution": ""
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def generate_innovation_chat(project, similar_projects, user_message: str) -> str:
    """
    Conversational innovation mentor reply.

    Given the user's current project idea, similar projects already found,
    and the user's question, return a helpful plain-text reply.
    """

    similar_projects_text = "\n".join([
        f"- {p['project_title']} "
        f"(Industry: {p.get('industry', 'N/A')}, "
        f"Similarity: {round(p.get('similarity', 0) * 100, 1)}%)"
        for p in similar_projects
    ]) or "No similar projects found."

    prompt = f"""You are an expert innovation mentor helping a user refine and differentiate their project idea before submitting it.

The user has NOT submitted their project yet. Your role is to help them:
- Differentiate their idea from existing similar projects
- Suggest unique features or angles
- Explore alternative industries or target audiences
- Improve their problem statement or solution overview
- Suggest pivots, extensions, or business models
- Identify unique selling points

Be concise, specific, and encouraging. Respond in plain text (no JSON, no markdown headers).

--- PROJECT IDEA ---
Title: {project.get('project_title', '')}
Industry: {project.get('industry_category', 'Unknown')}

Problem Statement:
{project.get('problem_statement', '')}

Solution Overview:
{project.get('solution_overview', '')}

--- SIMILAR EXISTING PROJECTS ---
{similar_projects_text}

--- USER'S QUESTION ---
{user_message}

Your response:"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


if __name__ == "__main__":
    print(
        generate_innovation_guidance(
            {
                "project_title": "Test",
                "problem_statement": "Test",
                "solution_overview": "Test",
                "industry_category": "AI"
            },
            []
        )
    )