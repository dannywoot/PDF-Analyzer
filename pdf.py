import pdfplumber
import openai
import os
import tkinter as tk
import concurrent.futures
from tkinter import filedialog

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

def analyze_pdf(pdf_text, user_input, summarise=False, summary_length=0):
    max_tokens = 4096 - 150
    sections = divide_text(pdf_text, max_tokens)

    responses = []
    for i, section in enumerate(sections):
        if summarise:
            prompt = f"Please provide a summary of the following text from section {i + 1} of {len(sections)} in a PDF (limit to {summary_length} words):\n\n{section}"
        elif user_input.lower() == 'sentiment':
            prompt = f"Perform sentiment analysis on the following text from section {i + 1} of {len(sections)} in a PDF:\n\n{section}"
        else:
            prompt = f"Analyze the following text from section {i + 1} of {len(sections)} in a PDF and answer this question:\n\n{section}\n\nQuestion: {user_input}"
        
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
    print("Type 'summarise' to generate a summary, 'sentiment' for sentiment analysis, or ask a question.")
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
        summarise = user_input.lower() == 'summarise'
        summary_length = 50  # You can change this
        if summarise:
            summary_length = 50  # You can change this

        analysis = analyze_pdf(pdf_text, user_input, summarise, summary_length)
        print(f"\nAnalysis for {os.path.basename(selected_pdf)}:")
        print(f"GPT: {analysis}")

if __name__ == "__main__":
    main()
