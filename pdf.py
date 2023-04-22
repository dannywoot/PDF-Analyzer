import pdfplumber
import openai
import concurrent.futures
import os
import tkinter as tk
from tkinter import filedialog
from functools import lru_cache

# Set your OpenAI API key
openai.api_key = "YOUR_API"

def extract_text_from_page(page):
    return page.extract_text()

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            page_texts = list(executor.map(extract_text_from_page, pdf.pages))
        text = ' '.join(page_texts)
    return text

@lru_cache(maxsize=100)
def send_message_to_gpt(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = response.choices[0].text.strip()
        return message
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing the request."

def divide_text(text, max_tokens):
    sections = []
    start = 0
    end = max_tokens
    while start < len(text):
        if end < len(text) and text[end] != " ":
            end = text.rfind(" ", start, end)
        sections.append(text[start:end].strip())
        start = end + 1
        end = start + max_tokens
    return sections

def analyze_pdf(pdf_text, question):
    max_tokens = 4096 - 150
    sections = divide_text(pdf_text, max_tokens)

    responses = []
    for i, section in enumerate(sections):
        prompt = f"Analyze the following text from section {i + 1} of {len(sections)} in a PDF and answer this question:\n\n{section}\n\nQuestion: {question}"
        gpt_response = send_message_to_gpt(prompt)
        responses.append(f"Section {i + 1}: {gpt_response}")

    return "\n".join(responses)

def main():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()

    if not folder_path:
        print("No folder selected. Exiting...")
        return

    print("Starting the conversation. Type 'quit' to exit.")
    pdf_texts = {}
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        selected_pdf = filedialog.askopenfilename(initialdir=folder_path, title="Select a PDF", filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))

        if not selected_pdf:
            print("GPT: No PDF was selected.")
            continue

        if selected_pdf not in pdf_texts:
            pdf_texts[selected_pdf] = extract_text_from_pdf(selected_pdf)

        pdf_text = pdf_texts[selected_pdf]
        analysis = analyze_pdf(pdf_text, user_input)
        print(f"GPT:\n{analysis}")

if __name__ == "__main__":
    main()
    
