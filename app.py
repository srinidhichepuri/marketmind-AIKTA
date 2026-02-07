from flask import Flask, render_template, request, session
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "marketmind-secret"

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(mode, tone, product, audience, platform):
    base_info = f"""
Product Details:
{product}

Target Audience:
{audience if audience else "Not specified"}

Platform:
{platform if platform else "General"}

Tone:
{tone}
"""

    if mode == "campaign":
        return f"""
You are a professional AI Marketing Strategist.

Create a COMPLETE marketing campaign.

{base_info}

Include:
- Campaign Name
- Objective
- Target Strategy
- Content Strategy
- Reels / Short Video Ideas
- Influencer Strategy
- Paid Ads Strategy
- KPIs
"""

    elif mode == "social":
        return f"""
Generate social media content.

{base_info}

Include:
- 5 Instagram captions
- 5 LinkedIn posts
- 3 Reel scripts
- Hashtag sets
- Carousel content idea
"""

    elif mode == "ads":
        return f"""
Generate high-converting ad copy.

{base_info}

Include:
- Google Ad copy
- Instagram Ad copy
- LinkedIn Ad copy
- 5 CTA variations
"""

    elif mode == "email":
        return f"""
Generate an email marketing sequence.

{base_info}

Include:
- Welcome email
- Follow-up email
- Sales email
- Subject lines
"""

    elif mode == "sales":
        return f"""
Create a persuasive sales pitch.

{base_info}

Include:
- Elevator pitch
- Long-form pitch
- Objection handling
- Closing strategy
"""

    elif mode == "positioning":
        return f"""
Generate product positioning strategy.

{base_info}

Include:
- Unique Selling Proposition (USP)
- Competitor positioning angle
- Pricing strategy
- Brand messaging framework
"""

    elif mode == "swot":
        return f"""
Perform a SWOT analysis.

{base_info}

Provide:
- Strengths
- Weaknesses
- Opportunities
- Threats
"""

    elif mode == "calendar":
        return f"""
Create a 30-day content calendar.

{base_info}

Provide:
- Daily content idea
- Format (Reel/Post/Story)
- Hook
- CTA
"""

    elif mode == "persona":
        return f"""
Generate a detailed target buyer persona.

{base_info}

Include:
- Demographics
- Pain points
- Buying triggers
- Interests
- Online behavior
"""

    else:
        return f"""
Generate a marketing strategy.

{base_info}
"""


def generate_with_groq(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert AI Marketing Strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    mode = request.form["mode"]
    tone = request.form["tone"]
    product = request.form["product"]
    audience = request.form.get("audience", "")
    platform = request.form.get("platform", "")

    prompt = build_prompt(mode, tone, product, audience, platform)

    result = generate_with_groq(prompt)

    session["last_output"] = result

    return render_template("index.html", result=result)


@app.route("/refine", methods=["POST"])
def refine():
    followup = request.form["followup"]
    previous_output = session.get("last_output", "")

    prompt = f"""
Refine and improve this marketing output based on the instruction below.

Instruction:
{followup}

Existing Output:
{previous_output}
"""

    refined_output = generate_with_groq(prompt)

    session["last_output"] = refined_output

    return render_template("index.html", result=refined_output)


if __name__ == "__main__":
    app.run(debug=True)