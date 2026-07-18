# 🐍 Python Documentation AI Chatbot

An AI-powered chatbot that answers Python programming questions using official Python documentation. The project scrapes Python documentation, preprocesses the content, retrieves the most relevant documentation using TF-IDF, and generates human-readable answers using Hugging Face's FLAN-T5 model.

---

## 📌 Features

- 🌐 Scrapes Python documentation automatically
- 🧹 Cleans and preprocesses scraped data
- 🔎 Retrieves relevant documentation using TF-IDF
- 🤖 Generates answers with Hugging Face FLAN-T5
- 💬 Interactive web interface using Gradio
- ⚡ Fast and easy to use

---

## 🛠️ Technologies Used

- Python
- Requests
- BeautifulSoup4
- JSON
- Scikit-learn (TF-IDF)
- Hugging Face Transformers
- PyTorch
- Gradio

---

## 📂 Project Structure

```
Python-Documentation-AI-Chatbot/
│
├── chatbot.py              # Main chatbot application
├── scraper.py              # Scrapes Python documentation
├── preprocess.py           # Cleans scraped data
├── dataset_builder.py      # Creates dataset
├── requirements.txt        # Python dependencies
├── README.md
│
├── data/
│   ├── raw_data.json
│   └── clean_data.json
│
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kazafa-Ali/Python-Documentation-AI-Chatbot.git
```

### 2. Navigate to the project

```bash
cd Python-Documentation-AI-Chatbot
```

### 3. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate it

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Chatbot

```bash
python chatbot.py
```

The Gradio interface will automatically open in your browser.

---

## 🧠 How It Works

1. Scrape Python documentation using BeautifulSoup.
2. Store the documentation in JSON format.
3. Clean and preprocess the collected data.
4. Build a TF-IDF index of all documentation pages.
5. Search for the most relevant documentation based on the user's question.
6. Send the retrieved context to Hugging Face FLAN-T5.
7. Display the generated answer in the Gradio interface.

---

## 💡 Example Questions

- What is a list in Python?
- Explain dictionary in Python.
- What is list comprehension?
- What is inheritance?
- Explain lambda functions.
- What is exception handling?
- How do I open a file in Python?
- What is the difference between list and tuple?
- What is the zip() function?
- Explain enumerate().

---

## 📸 Project Demo

You can add screenshots of the chatbot interface here.

Example:

```
screenshots/
    <img width="1153" height="636" alt="Chatbot_home" src="https://github.com/user-attachments/assets/8eaf1915-b211-4609-a1cf-6a132c15bea4" />
<img width="1144" height="638" alt="chatbot_response" src="https://github.com/user-attachments/assets/ffbc5a6c-f66e-42e3-ab5d-24f8745b9790" />


```

---

## 🚀 Future Improvements

- Semantic Search using Sentence Transformers
- Multi-document Retrieval
- Support for PDF documentation
- Voice-based interaction
- Conversation memory
- Deployment on Hugging Face Spaces

---

## 👨‍💻 Author

**Kazafa Ali**

BS Computer Science Student

AI & Automation Intern at Infrix

GitHub: https://github.com/Kazafa-Ali

---

## 📜 License

This project is developed for educational and learning purposes.
