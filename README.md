# PDFGPT
PDF Analysis with GPT

Description: This Python program uses OpenAI's GPT model to analyze and summarize the content of PDF files. The user can visually select a PDF file, and the program will extract its text, divide it into smaller sections, and send multiple prompts to the GPT API to analyze each section. The program combines the responses for all sections to provide a comprehensive analysis of the selected PDF file.

How to use:

Install the required libraries:

Copy code
```
pip install pdfplumber openai
```
Replace 'your_openai_api_key' in the script with your actual OpenAI API key.

Run the script:

Copy code
```
python pdf.py
```
Follow the prompts in the terminal to interact with the program. Type your question, and the program will let you visually select a PDF file for analysis. Once the analysis is complete, the program will display the response from the GPT model. Type 'quit' to exit the program.

Key Features:

Extracts text from PDF files using the pdfplumber library.
Divides the extracted text into smaller sections to overcome GPT's token limit.
Processes PDF pages concurrently to speed up text extraction.
Uses the tkinter library to create file dialogs for selecting folders and PDF files.
Dependencies:

pdfplumber
openai
tkinter
Note: This program is designed for educational purposes only. The performance and quality of the analysis may vary depending on the input and the specific GPT model used. Make sure to comply with OpenAI's usage policies when using the GPT API.
