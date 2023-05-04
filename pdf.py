import pdfplumber
import openai
import os
import fitz
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import concurrent.futures

# Set your OpenAI API key
openai.api_key = "your-api-key-here"

def extract_text_from_page(page):
    return page.extract_text()


def extract_text_from_pdf(pdf_path):
    try:
        with fitz.open(pdf_path) as pdf:
            page_texts = [page.get_text("text") for page in pdf]
            return "\n".join(page_texts)
    except Exception as e:
        print(f"Error while extracting text from {pdf_path}: {e}")
        return ""



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

# Tkinter GUI code starts here
root = tk.Tk()
root.title("PDF Analyzer")
root.geometry("800x600")

selected_pdf = None
pdf_texts = {}

def select_pdf():
    global selected_pdf
    selected_pdf = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if selected_pdf:
        pdf_name.set(os.path.basename(selected_pdf))
        if selected_pdf not in pdf_texts:
            pdf_texts[selected_pdf] = extract_text_from_pdf(selected_pdf)
    else:
        pdf_name.set("No PDF selected")

def analyze_selected_pdf():
    global selected_pdf, pdf_texts

    user_input = user_input_var.get()
    if not selected_pdf:
        analysis_text.delete("1.0", tk.END)
        analysis_text.insert(tk.END, "No PDF was selected.")
        return

    pdf_text = pdf_texts[selected_pdf]
    summarise = user_input.lower() == 'summarise'
    summary_length = 50  # You can change this
    if summarise:
        summary_length = 50  # You can change this

    analysis = analyze_pdf(pdf_text, user_input, summarise, summary_length)
    analysis_text.delete("1.0", tk.END)
    analysis_text.insert(tk.END, f"\nAnalysis for {os.path.basename(selected_pdf)}:")
    analysis_text.insert(tk.END, f"\nGPT: {analysis}")

pdf_name = tk.StringVar()
pdf_name.set("No PDF selected")

select_button = ttk.Button(root, text="Select PDF", command=select_pdf)
select_button.pack(pady=10)

pdf_label = ttk.Label(root, textvariable=pdf_name)
pdf_label.pack(pady=5)

user_input_label = ttk.Label(root, text="Type 'summarise' to generate a summary, 'sentiment' for sentiment analysis, or ask a question:")
user_input_label.pack(pady=5)

user_input_var = tk.StringVar()
user_input_entry = ttk.Entry(root, textvariable=user_input_var, width=60)
user_input_entry.pack(pady=5)

analyze_button = ttk.Button(root, text="Analyze PDF", command=analyze_selected_pdf)
analyze_button.pack(pady=10)

analysis_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
analysis_text.pack(pady=10)

root.mainloop()
