## Announcement Suggester — LangGraph

A LangGraph-based announcement suggestion system that analyzes a user's announcement and generates a suitable social media post. The workflow uses multiple specialist nodes in parallel, followed by a decision node that determines whether the final tone should be professional or playful.

## Overview
The application accepts a short announcement from the user, such as:
"I have joined a new company"
"I'm getting married next month"
"Going to Bali for vacation"
"I got promoted to Senior Manager"
"We are celebrating our anniversary"
The graph generates multiple suggestions and then selects an appropriate final format.

## Architecture

START
   │
   ├──────────────────┬──────────────────┐
   ↓                  ↓                  ↓
write_formal      create_social     suggest_hashtags
announcement          hook
   │                  │                  │
   └──────────────────┴──────────────────┘
                      ↓
            decide_announcement_tone
                      │
             ┌────────┴────────┐
             ↓                 ↓
       Professional          Playful
             ↓                 ↓
    linkedin_style_post  instagram_style_post
             ↓                 ↓
            END               END

## Workflow

1. write_formal_announcement
Creates a professional version of the user's announcement.
2. create_social_hook
Creates short and engaging social-media hooks.
3. suggest_hashtags
Generates relevant hashtags based on the announcement topic.
4. decide_announcement_tone
Determines whether the announcement should be treated as:
Professional — work, business, career, company-related announcements
Playful — vacation, marriage, birthday, celebrations and personal updates
The decision is returned as a Boolean value:
{
  "needs_professional_announcement": true,
  "reason": "The announcement is career-related."
}
5. linkedin_style_post
Executed when the decision is Professional and creates a concise LinkedIn-style post.
6. instagram_style_post
Executed when the decision is Playful and creates a casual, warm and engaging Instagram-style post.

## Technologies

Python
LangGraph
LangChain
OpenAI
Pydantic
python-dotenv

## Installation
Create a virtual environment:
python -m venv venv

Activate:
Windows - .\venv\Scripts\Activate
macOS/Linux - source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Environment Configuration:
Create a .env file in the project root

OPENAI_API_KEY=your_openai_api_key

Do not commit .env to Git.

Add it to .gitignore:

.env
venv/
__pycache__/
*.pyc

You can provide a .env.example:

OPENAI_API_KEY=your_api_key_here

## Running the Application

Run:
python social_media_post.py

The application will prompt:

What announcement do you want to post? >

Enter an announcement, for example:

I am getting married next month

The graph will execute the specialist nodes, determine the appropriate tone, and generate the final announcement.

Example Flow

Professional Announcement

Input:

I have been promoted to Senior Manager

Decision:

Professional = True

Final Node:

linkedin_style_post

Personal Announcement

Input:

I'm getting married next month!

Decision:

Professional = False

Final Node:

instagram_style_post

Key LangGraph Concepts Demonstrated

State

A Pydantic model maintains the shared graph state:

class Announcement(BaseModel):
    user_announcement: str = ""
    formal_announcement_suggestion: str = ""
    social_hook_suggestion: str = ""
    hashtags_suggestion: str = ""
    needs_professional_announcement: bool = False
    announcement_reason: str = ""
    final_suggestion: str = ""

Parallel Execution

The three specialist nodes work independently:

write_formal_announcement
create_social_hook
suggest_hashtags

Their results are then used by the downstream decision and final stages.

Conditional Routing

The decision node controls which final node executes:

graph.add_conditional_edges(
    "decide_announcement_tone",
    route_announcement,
    {
        "professional": "linkedin_style_post",
        "playful": "instagram_style_post",
    },
)

State-Based Decision

The router examines the state:

def route_announcement(state: Announcement) -> str:
    if state.needs_professional_announcement:
        return "professional"

    return "playful"

Project Structure

langgraph_framework/
│
├── social_media_post.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md