import streamlit as st
import os

from dotenv import load_dotenv
from groq import Groq

from sentence_transformers import SentenceTransformer
import chromadb

from utils.pdf_reader import extract_text_from_pdf
from utils.rag_pipeline import split_text


# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="DocMind AI",
    page_icon="🧠",
    layout="wide"
)

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a,
            #1e293b,
            #334155
        );
    }

    h1, h2, h3, p, label {
        color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

load_dotenv()

client_groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="document_chunks"
)


st.title("🧠 DocMind AI")

st.markdown("""
### Intelligent Document Question Answering System

Upload a PDF or paste text and ask questions based only on the provided content.
""")

st.info("""
✨ Features

• PDF Upload

• Paste Text


""")

# -------------------------
# INPUT SOURCE
# -------------------------

source_type = st.radio(
    "Choose Knowledge Source",
    ["PDF Upload", "Paste Text"]
)

text = ""

# -------------------------
# PDF INPUT
# -------------------------

if source_type == "PDF Upload":

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if uploaded_file:
        text = extract_text_from_pdf(
            uploaded_file
        )

# -------------------------
# TEXT INPUT
# -------------------------

else:

    text = st.text_area(
        "Paste your document text here",
        height=300
    )

# -------------------------
# PROCESS DOCUMENT
# -------------------------

if text and len(text.strip()) > 0:

    chunks = split_text(text)

    # Clear old data

    try:

        existing_count = collection.count()

        if existing_count > 0:

            ids = [
                str(i)
                for i in range(existing_count)
            ]

            collection.delete(ids=ids)

    except Exception:
        pass

    # Create embeddings

    embeddings = embedding_model.encode(
        chunks
    )

    # Store in ChromaDB

    for i, chunk in enumerate(chunks):

        collection.add(
            ids=[str(i)],
            embeddings=[
                embeddings[i].tolist()
            ],
            documents=[chunk]
        )

    st.success(
        "✅ Knowledge source processed successfully!"
    )

    # -------------------------
    # QUESTION INPUT
    # -------------------------

    question = st.text_input(
        "💬 Ask a question about the document"
    )

    if question:

        question_embedding = embedding_model.encode(
            question
        )

        results = collection.query(
            query_embeddings=[
                question_embedding.tolist()
            ],
            n_results=8
        )

        retrieved_chunks = (
            results["documents"][0]
        )

        context = "\n".join(
            retrieved_chunks
        )

        prompt = f"""
You are a Context-Aware Document Q&A Assistant.

STRICT RULES:

1. Answer ONLY from the provided context.
2. Never use outside knowledge.
3. Never guess.
4. If the answer is not clearly present in the context, reply exactly:

This information is not available in the document.

Context:
{context}

Question:
{question}

Answer:
"""

        try:

            response = client_groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            st.markdown("## 🤖 Answer")

            st.success(
                response.choices[0].message.content
            )

        except Exception as e:

            st.error(
                f"Groq Error: {e}"
            )

# -------------------------
# FOOTER
# -------------------------

st.markdown("---")

st.caption(
    "Built by Sindhu Sunkara | Azentrix Generative AI Internship Task"
)