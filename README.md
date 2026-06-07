# Context-Aware Document Q&A Bot
##workflow
PDF Upload / Paste Text
          ↓
     Text Extraction
          ↓
      Text Chunking
          ↓
   Vector Embeddings
          ↓
        ChromaDB
          ↓
 Similarity Retrieval
          ↓
       Groq LLM
          ↓
     Final Answer
     
## Features

- PDF Upload
- Text Extraction
- Text Chunking
- Vector Embeddings
- ChromaDB Retrieval
- Gemini LLM
- Hallucination Prevention

## Installation

pip install -r requirements.txt

## Run

streamlit run app.py

## Tech Stack

- Streamlit
- ChromaDB
- Sentence Transformers
- Gemini API
- Python
