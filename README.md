# PDF Analyzer with GPT

This project is a PDF analyzer tool powered by GPT-3 that allows you to ask questions, generate summaries, or perform sentiment analysis on the contents of PDF files. The tool features a simple visual interface for selecting PDF files and supports multi-page PDF documents.

## Features

- Summarize PDF content: Generate a summary of the selected PDF file.
- Sentiment analysis: Analyze the sentiment of the content in the PDF file.
- Ask a question: Ask a question related to the content of the PDF file, and get an answer based on the GPT analysis.
- Simple visual interface

## Requirements

- Python 3.x
- PyMuPDF
- openai
- tkinter

## Installation

1. Clone this repository or download the source code.
2. Install the required packages:

```
pip install PyMuPDF openai tkinter
```
Set your OpenAI API key in the pdf.py script:
```
openai.api_key = "your-api-key-here"
```
Usage
Run the pdf.py script:
```
python pdf.py
```
Follow the on-screen instructions to select a PDF file and choose an analysis option.


If you'd like to contribute to this project, please feel free to fork the repository and submit a pull request.
