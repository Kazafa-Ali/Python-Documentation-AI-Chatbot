"""
chatbot.py

Python Documentation AI Assistant
Powered by Hugging Face FLAN-T5

Uses:
- TF-IDF Retrieval
- Hugging Face Transformers
- Gradio

Author: Your Name
"""

import json
import torch

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

# =====================================================
# CONFIGURATION
# =====================================================

MODEL_NAME = "google/flan-t5-base"

DATA_PATH = "data/clean_data.json"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MAX_CONTEXT_LENGTH = 1800

# =====================================================
# LOAD MODEL
# =====================================================

print("=" * 60)
print("Loading Hugging Face Model...")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

model.to(DEVICE)

print("Model Loaded Successfully!")

# =====================================================
# LOAD DOCUMENTATION
# =====================================================

print("\nLoading Documentation...")

with open(DATA_PATH, "r", encoding="utf-8") as f:

    documents = json.load(f)

print(f"{len(documents)} pages loaded.")

# =====================================================
# BUILD SEARCH INDEX
# =====================================================

print("Building TF-IDF Index...")

texts = []

for doc in documents:

    text = f"{doc['title']}\n{doc['content']}"

    texts.append(text)

vectorizer = TfidfVectorizer(
    stop_words="english"
)

document_vectors = vectorizer.fit_transform(texts)

print("Search Index Ready!")

# =====================================================
# DOCUMENT SEARCH
# =====================================================

def search_document(question):

    question_vector = vectorizer.transform([question])

    similarities = cosine_similarity(
        question_vector,
        document_vectors
    )

    best_index = similarities.argmax()

    best_score = similarities[0][best_index]

    return documents[best_index], best_score

# =====================================================
# PROMPT BUILDER
# =====================================================

def build_prompt(question, document):

    context = document["content"][:MAX_CONTEXT_LENGTH]

    return f"""
You are an expert Python programming assistant.

Answer ONLY from the documentation below.

If the documentation does not contain the answer,
reply exactly:

I couldn't find this information in the documentation.

Documentation Title:
{document["title"]}

Documentation:
{context}

Question:
{question}

Write a detailed answer in simple English.

Include a short Python example whenever possible.
"""

# =====================================================
# GENERATE ANSWER
# =====================================================

def generate_answer(question):

    if len(question.strip()) == 0:

        return "Please enter a question."

    document, score = search_document(question)

    if score < 0.05:

        return "I couldn't find this information in the documentation."

    prompt = build_prompt(
        question,
        document
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(DEVICE)

    outputs = model.generate(
        **inputs,
        max_new_tokens=220,
        temperature=0.4,
        top_p=0.9,
        repetition_penalty=1.15,
        do_sample=True
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer.strip()

import gradio as gr

# =====================================================
# CHAT FUNCTION
# =====================================================

def chat(message, history):

    if history is None:
        history = []

    answer = generate_answer(message)

    history.append(
        {
            "role": "user",
            "content": message
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return history


# =====================================================
# CLEAR CHAT
# =====================================================

def clear_history():
    return []


# =====================================================
# USER INTERFACE
# =====================================================

with gr.Blocks(title="Python Documentation AI Assistant") as demo:

    gr.Markdown("""
# 🐍 Python Documentation AI Assistant

### Powered by Hugging Face FLAN-T5 Base

Ask questions about Python.

The assistant answers **only using the scraped Python documentation**.
""")

    chatbot = gr.Chatbot(
        label="Conversation",
        min_height=500
    )

    msg = gr.Textbox(
        label="Your Question",
        placeholder="Example: What is list comprehension?"
    )

    with gr.Row():
        send_btn = gr.Button(
            "Send",
            variant="primary"
        )

        clear_btn = gr.Button("Clear")

    send_btn.click(
        fn=chat,
        inputs=[msg, chatbot],
        outputs=chatbot
    ).then(
        lambda: "",
        outputs=msg
    )

    msg.submit(
        fn=chat,
        inputs=[msg, chatbot],
        outputs=chatbot
    ).then(
        lambda: "",
        outputs=msg
    )

    clear_btn.click(
        fn=clear_history,
        outputs=chatbot
    )

    gr.Markdown("""
---

### Internship Project

**Technologies Used**

- Python
- BeautifulSoup
- Requests
- Hugging Face Transformers
- FLAN-T5 Base
- TF-IDF Search
- Gradio
""")

# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    demo.launch(
        inbrowser=True
    )