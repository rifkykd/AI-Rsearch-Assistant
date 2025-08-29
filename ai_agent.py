import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "File not found."

def read_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return " ".join([p.get_text() for p in soup.find_all("p")])
    except Exception as e:
        return f"Error fetching website: {e}"

def ask_ai(content, question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a research assistant."},
            {"role": "user", "content": f"Content: {content}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("=== AI Research Assistant 🚀 ===")
    choice = input("Do you want to analyze a (1) file or (2) website? ")

    if choice == "1":
        filename = input("Enter file name (e.g., notes.txt): ")
        content = read_file(filename)
    else:
        url = input("Enter website URL: ")
        content = read_website(url)

    question = input("What do you want to ask? ")
    answer = ask_ai(content, question)

    print("\nAI Answer:", answer)
