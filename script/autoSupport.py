from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai
import os
import PyPDF2

# Load the environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API credentials
openai.api_key = api_key

# Load PDF file and extract text
pdf_file = "2023_Google built-in Guide_Final.pdf"
pdf_reader = PyPDF2.PdfReader(open(pdf_file, "rb"))
pdf_text = ""
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    
    pdf_text += page.extract_text()

# Define function to generate response
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

# Set up Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get_answer", methods=["POST"])
def get_answer():
    user_input = request.form["user_input"]
    prompt = pdf_text + "\nUser question: " + user_input
    response = generate_response(prompt)
    return jsonify(answer=response)

if __name__ == "__main__":
    app.run(debug=True)
