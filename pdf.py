import pdfplumber
import openai
import os
import tkinter as tk
from tkinter import filedialog

# Set your OpenAI API key
openai.api_key = "YOUR_API"

# Function to extract text from a PDF file
import concurrent.futures

def extract_text_from_page(page):
    return page.extract_text()

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            page_texts = list(executor.map(extract_text_from_page, pdf.pages))
        text = ' '.join(page_texts)
    return text

# Function to send a message to the GPT API
def send_message_to_gpt(prompt):
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

# Function to divide the text into smaller sections
def divide_text(text, max_tokens):
    sections = []
    tokens = text.split()
    current_section = []

    for token in tokens:
        if len(" ".join(current_section)) + len(token) + 1 <= max_tokens:
            current_section.append(token)
        else:
            sections.append(" ".join(current_section))
            current_section = [token]

    if current_section:
        sections.append(" ".join(current_section))

    return sections

# Function to get information about a PDF
def analyze_pdf(pdf_text, question):
    max_tokens = 4096 - 150
    sections = divide_text(pdf_text, max_tokens)

    responses = []
    for i, section in enumerate(sections):
        prompt = f"Analyze the following text from section {i + 1} of {len(sections)} in a PDF and answer this question:\n\n{section}\n\nQuestion: {question}"
        gpt_response = send_message_to_gpt(prompt)
        responses.append(f"Section {i + 1}: {gpt_response}")

    return "\n".join(responses)

# Function to select the PDF folder and start the conversation
def main():
    # Create a simple directory dialog for selecting the PDF folder
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

        # Open a file dialog for selecting a PDF
        selected_pdf = filedialog.askopenfilename(initialdir=folder_path, title="Select a PDF", filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))

        if not selected_pdf:
            print("GPT: No PDF was selected.")
            continue

        # Extract and store the text for each PDF only once
        if selected_pdf not in pdf_texts:
            pdf_texts[selected_pdf] = extract_text_from_pdf(selected_pdf)
        
        pdf_text = pdf_texts[selected_pdf]
        analysis = analyze_pdf(pdf_text, user_input)
        print(f"GPT:\n{analysis}")

if __name__ == "__main__":
    main()
