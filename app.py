from flask import Flask, render_template, request, session
import os
from groq import Groq
from dotenv import load_dotenv

# 🔥 Load .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "marketmind-secret"

# 🔥 Get API key safely
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# 🔥 Initialize Groq
client = Groq(api_key=api_key)


# ===========================
# GROQ GENERATION FUNCTION
# ===========================
def generate_with_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert AI Marketing Strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content


# ===========================
# HOME
# ===========================
@app.route("/")
def index():
    return render_template("index.html")


# ===========================
# GENERATE
# ===========================
@app.route("/generate", methods=["POST"])
def generate():
    product = request.form.get("product")
    audience = request.form.get("audience")
    platform = request.form.get("platform")
    mode = request.form.get("mode")
    tone = request.form.get("tone")

    prompt = f"""
You are an AI Marketing Command Center.

MODE: {mode}
TONE: {tone}

Product Details:
{product}

Target Audience:
{audience}

Platform:
{platform}

Generate a highly professional and structured marketing output.
"""

    result = generate_with_groq(prompt)
    session["last_output"] = result

    return render_template("index.html", result=result)


# ===========================
# RUN APP
# ===========================
if __name__ == "__main__":
    app.run(debug=True)