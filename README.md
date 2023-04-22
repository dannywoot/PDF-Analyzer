# PDF Analyzer with GPT

PDF Analyzer is a Python program that utilizes the GPT API to analyze and process PDF files. It allows users to summarize the content, perform sentiment analysis, or ask a question about the content of a PDF file.

## Features

- Summarize PDF content: Generate a summary of the selected PDF file.
- Sentiment analysis: Analyze the sentiment of the content in the PDF file.
- Ask a question: Ask a question related to the content of the PDF file, and get an answer based on the GPT analysis.

## Requirements

- Python 3.x
- pdfplumber
- openai
- tkinter

## Installation

1. Clone this repository or download the source code.
2. Install the required packages:

```
pip install pdfplumber openai tkinter
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

You can change engine, temperature and token limit by going here in pdf.py:
```
def send_message_to_gpt_api(prompt):
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
```


If you'd like to contribute to this project, please feel free to fork the repository and submit a pull request.
