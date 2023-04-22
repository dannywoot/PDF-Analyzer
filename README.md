# PDF Analysis with GPT

This project provides a command-line tool that leverages GPT to analyze and summarize PDF documents. Users can generate summaries, perform sentiment analysis, and ask questions about the content of the document. The tool is built using Python, pdfplumber, and OpenAI's GPT API.

## Features

- Analyze and summarize text from PDF documents
- Perform sentiment analysis on PDF content
- Ask questions about the content of the document
- Process multiple PDFs in a single session

## Installation

1. Clone the repository:
```
git clone https://github.com/dannywoot/PDFGPT/
```

2. Change to the project directory:
```
cd pdfapi
```


3. Install required Python packages:
```
pip install -r requirements.txt
```

4. Replace `your-api-key-here` in the `pdf.py` file with your OpenAI API key. You can get an API key by signing up for an account at https://onboard.openai.com.

## Usage

1. Run the `pdf.py` script:
```
python pdf.py
```

2. Follow the prompts to analyze a PDF document. You can:
- Type 'summarise' to generate a summary
- Type 'sentiment' for sentiment analysis
- Ask a question about the content of the document

3. Type 'quit' to exit the application.

## Dependencies

- Python 3.6+
- pdfplumber
- openai

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements, bug fixes, or feature requests.

## License

This project is licensed under the [MIT License](LICENSE).

