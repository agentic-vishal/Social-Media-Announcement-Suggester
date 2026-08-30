## Social Media Announcement Suggester -- Architecture

How It Works

User enters announcement
        |
        v
   [user_announcement]
        |
        +---> [write_formal_announcement]  \
        |                                     |
        +---> [create_social_hook]            +--> run in PARALLEL
        |                                     |
        +---> [suggest_hashtags]             /
        |
        v
 [decide_announcement_tone]
        |
        +-- PROFESSIONAL --> [linkedin_style_post]
        |
        +-- PLAYFUL ------> [instagram_style_post]
        |
        v
    Final output

Interactive Mode

$ python social_media_post.py

  =======================================================
    ANNOUNCEMENT SUGGESTER
  =======================================================

    Tell me what announcement you want to post and I'll
    create a personalized social media post.
    Type 'quit' to exit.

    What announcement do you want to post? > I got promoted to Senior Manager

    ...graph runs...

    YOUR PERSONALIZED ANNOUNCEMENT
    ...

    What announcement do you want to post? > I'm getting married!

    ...graph runs...

    YOUR PERSONALIZED ANNOUNCEMENT
    ...

    What announcement do you want to post? > quit
    Goodbye!

Graph Structure

                    +-------+
                    | START |
                    +---+---+
                        |
           +------------+------------+
           |            |            |
           v            v            v
+----------+----+ +-----+--------+ +--+-------------+
| write_formal  | | create_social| | suggest_       |
| announcement  | | hook         | | hashtags       |
+-------+-------+ +------+-------+ +------+----------+
        |                |                |
        +----------------+----------------+
                         |
                         v
             +-----------+------------+
             | decide_announcement_   |
             | tone                   |
             |                        |
             | Professional / Playful |
             +-----------+------------+
                         |
                 CONDITIONAL EDGE
                    /         \
                   /           \
        Professional           Playful
               |                   |
               v                   v
     +---------+---------+ +------+----------+
     | linkedin_style_   | | instagram_      |
     | post              | | style_post      |
     +---------+---------+ +------+----------+
               |                  |
               +--------+---------+
                        |
                        v
                       END

State Fields

Announcement
|
|-- user_announcement
|       <-- set by user input
|
|-- formal_announcement_suggestion
|       <-- written by write_formal_announcement
|
|-- social_hook_suggestion
|       <-- written by create_social_hook
|
|-- hashtags_suggestion
|       <-- written by suggest_hashtags
|
|-- needs_professional_announcement
|       <-- written by decide_announcement_tone
|
|-- announcement_reason
|       <-- written by decide_announcement_tone
|
|-- final_suggestion
|       <-- written by linkedin_style_post
|           OR instagram_style_post
|
|-- messages
        <-- appended by all nodes (operator.add)

LangGraph Concepts Used

Concept

Where in Code

What It Does

State (Pydantic)

Announcement class

Typed shared data that flows through every node

Nodes

Specialist and final functions

Each node performs one focused task

Parallel Execution

Three specialist branches

Formal announcement, hooks, and hashtags run independently

Fan-In

Three edges into decide_announcement_tone

Decision node receives specialist outputs

Conditional Edge

route_announcement()

Routes to LinkedIn or Instagram

Graph Compilation

graph.compile()

Converts graph definition into a runnable application

Invocation

app.invoke({...})

Starts graph execution

Message Accumulation

Annotated[list, operator.add]

Appends messages without overwriting existing messages

Node Responsibilities

Specialist Node 1 — write_formal_announcement

Creates a concise professional version of the user's announcement.

Specialist Node 2 — create_social_hook

Creates engaging social-media hook options.

Specialist Node 3 — suggest_hashtags

Suggests relevant hashtags based on the announcement.

Decision Node — decide_announcement_tone

Determines whether the announcement is better suited for a professional or playful tone.

Professional:
- Work
- Business
- Career
- Company announcements

Playful:
- Vacation
- Marriage
- Birthday
- Celebration
- Personal updates

Final Node — linkedin_style_post

Creates a professional, humble and concise LinkedIn-style announcement.

Final Node — instagram_style_post

Creates a casual, warm and playful Instagram-style announcement.

Tech Stack

Component

Purpose

LangGraph

Graph orchestration, nodes, parallel execution and conditional routing

LangChain

LLM integration through ChatOpenAI

OpenAI

gpt-4o-mini for announcement generation and classification

Pydantic

State validation and type safety

python-dotenv

Loads OPENAI_API_KEY from .env

File Structure

Social-Media-Announcement-Suggester/
|
|-- social_media_post.py       Main application and LangGraph workflow
|-- architecture.md            Architecture documentation
|-- architecture.drawio        Visual graph diagram
|-- README.md                  Project documentation
|-- requirements.txt           Python dependencies
|-- .env                       OPENAI_API_KEY (not committed)
|-- .env.example               Environment variable template
|-- .gitignore                 Git ignore configuration

Execution Flow

User Input
    |
    v
Three Specialist Nodes
    |
    +--> Formal Announcement
    +--> Social Hooks
    +--> Hashtags
    |
    v
Decision Node
    |
    +--> Professional --> LinkedIn Post
    |
    +--> Playful ------> Instagram Post
    |
    v
Final Response

This project demonstrates parallel node execution, shared state management, fan-in, conditional routing, and workflow orchestration using LangGraph.