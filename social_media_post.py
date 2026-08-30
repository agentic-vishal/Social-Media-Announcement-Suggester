import sys
import operator
import json
from typing import Annotated

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()


# ---------------------------------------------------------
# State
# ---------------------------------------------------------

class Announcement(BaseModel):
    user_announcement: str = ""

    formal_announcement_suggestion: str = ""
    social_hook_suggestion: str = ""
    hashtags_suggestion: str = ""

    needs_professional_announcement: bool = False
    announcement_reason: str = ""

    final_suggestion: str = ""

    messages: Annotated[list, operator.add] = []


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)


# ---------------------------------------------------------
# Specialist Node 1
# ---------------------------------------------------------

def write_formal_announcement(state: Announcement) -> dict:

    response = llm.invoke(
        f"""Write a professional announcement.

Announcement: "{state.user_announcement}"

Keep it concise, clear and professional."""
    )

    return {
        "formal_announcement_suggestion": response.content,
        "messages": [
            "[write_formal_announcement] Completed"
        ],
    }


# ---------------------------------------------------------
# Specialist Node 2
# ---------------------------------------------------------

def create_social_hook(state: Announcement) -> dict:

    response = llm.invoke(
        f"""Create a few engaging social media hooks.

Announcement: "{state.user_announcement}"

Keep them short and engaging."""
    )

    return {
        "social_hook_suggestion": response.content,
        "messages": [
            "[create_social_hook] Completed"
        ],
    }


# ---------------------------------------------------------
# Specialist Node 3
# ---------------------------------------------------------

def suggest_hashtags(state: Announcement) -> dict:

    response = llm.invoke(
        f"""Suggest relevant hashtags.

Announcement: "{state.user_announcement}"

Provide a short list of useful hashtags."""
    )

    return {
        "hashtags_suggestion": response.content,
        "messages": [
            "[suggest_hashtags] Completed"
        ],
    }


# ---------------------------------------------------------
# Decision Node
# ---------------------------------------------------------

def decide_announcement_tone(state: Announcement) -> dict:

    response = llm.invoke(
        f"""Classify this announcement as professional or playful.

Announcement: "{state.user_announcement}"

Professional: work, business, career, company.
Playful: vacation, marriage, birthday, celebration, personal.

Personal announcements are playful unless explicitly business-related.

Return ONLY JSON:
{{"needs_professional_announcement": true/false, "reason": "one sentence"}}"""
    )

    try:
        result = json.loads(response.content)

        needs_professional = result["needs_professional_announcement"]
        reason = result["reason"]

    except (json.JSONDecodeError, KeyError):
        needs_professional = False
        reason = "Could not determine tone, defaulting to playful."

    return {
        "needs_professional_announcement": needs_professional,
        "announcement_reason": reason,
        "messages": [
            f"[decide_announcement_tone] "
            f"professional={needs_professional}"
        ],
    }


# ---------------------------------------------------------
# Routing
# ---------------------------------------------------------

def route_announcement(state: Announcement) -> str:

    if state.needs_professional_announcement:
        return "professional"

    return "playful"


# ---------------------------------------------------------
# Final Node 1 - LinkedIn
# ---------------------------------------------------------

def linkedin_style_post(state: Announcement) -> dict:

    response = llm.invoke(
        f"""Create a short LinkedIn-style announcement.

Announcement:
{state.user_announcement}

Formal announcement:
{state.formal_announcement_suggestion}

Social hooks:
{state.social_hook_suggestion}

Hashtags:
{state.hashtags_suggestion}

Create a professional, humble and clear post.
Keep it concise."""
    )

    return {
        "final_suggestion": (
            f"LINKEDIN STYLE POST\n"
            f"{'=' * 45}\n"
            f"{response.content}"
        ),
        "messages": [
            "[linkedin_style_post] Generated"
        ],
    }


# ---------------------------------------------------------
# Final Node 2 - Instagram
# ---------------------------------------------------------

def instagram_style_post(state: Announcement) -> dict:

    response = llm.invoke(
        f"""Create a short Instagram-style announcement.

Announcement:
{state.user_announcement}

Formal announcement:
{state.formal_announcement_suggestion}

Social hooks:
{state.social_hook_suggestion}

Hashtags:
{state.hashtags_suggestion}

Create a casual, warm and playful post.
Do not make it sound like a joke."""
    )

    return {
        "final_suggestion": (
            f"INSTAGRAM STYLE POST\n"
            f"{'=' * 45}\n"
            f"{response.content}"
        ),
        "messages": [
            "[instagram_style_post] Generated"
        ],
    }


# ---------------------------------------------------------
# Build Graph
# ---------------------------------------------------------

graph = StateGraph(Announcement)


# Add nodes
graph.add_node(
    "write_formal_announcement",
    write_formal_announcement,
)

graph.add_node(
    "create_social_hook",
    create_social_hook,
)

graph.add_node(
    "suggest_hashtags",
    suggest_hashtags,
)

graph.add_node(
    "decide_announcement_tone",
    decide_announcement_tone,
)

graph.add_node(
    "linkedin_style_post",
    linkedin_style_post,
)

graph.add_node(
    "instagram_style_post",
    instagram_style_post,
)


# ---------------------------------------------------------
# Graph Flow
# ---------------------------------------------------------

graph.add_edge(
    START,
    "write_formal_announcement",
)

graph.add_edge(
    START,
    "create_social_hook",
)

graph.add_edge(
    START,
    "suggest_hashtags",
)


# All three specialists → Decision Node

graph.add_edge(
    "write_formal_announcement",
    "decide_announcement_tone",
)

graph.add_edge(
    "create_social_hook",
    "decide_announcement_tone",
)

graph.add_edge(
    "suggest_hashtags",
    "decide_announcement_tone",
)


# Decision → Final Node

graph.add_conditional_edges(
    "decide_announcement_tone",
    route_announcement,
    {
        "professional": "linkedin_style_post",
        "playful": "instagram_style_post",
    },
)


# Final nodes → END

graph.add_edge(
    "linkedin_style_post",
    END,
)

graph.add_edge(
    "instagram_style_post",
    END,
)


# Compile

app = graph.compile()


# ---------------------------------------------------------
# Main Function
# ---------------------------------------------------------

def run_announcement_suggestion(announcement: str):

    print("=" * 55)
    print("  ANNOUNCEMENT SUGGESTER")
    print(f'  You said: "{announcement}"')
    print("=" * 55)

    result = app.invoke(
        {
            "user_announcement": announcement,
            "messages": [],
        }
    )

    print("\n" + "=" * 55)
    print("  YOUR PERSONALIZED ANNOUNCEMENT")
    print("=" * 55)

    print(f"\n{result['final_suggestion']}")

    print("\n" + "-" * 55)
    print("  MESSAGE LOG")
    print("-" * 55)

    for msg in result["messages"]:
        print(f"  {msg}")

    return result


# ---------------------------------------------------------
# Run Application
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\n" + "=" * 55)
    print("  ANNOUNCEMENT SUGGESTER")
    print("=" * 55)

    print(
        "\nTell me what announcement you want to post "
        "and I'll create a suggestion."
    )

    print("Type 'quit' to exit.\n")

    while True:

        announcement = input(
            "  What announcement do you want to post? > "
        ).strip()

        if announcement.lower() in ("quit", "exit", "q"):
            print("\nGoodbye!\n")
            break

        if not announcement:
            print("Please enter an announcement.\n")
            continue

        try:
            run_announcement_suggestion(announcement)

        except Exception as e:
            print(f"\nError: {e}\n")