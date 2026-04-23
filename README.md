# 🤖 AI Chat Assistant — Multi-Personality Chatbot

A full ChatGPT-like experience built with **Groq (LLaMA 3.3 70B)** and **Gradio**,
featuring multiple AI personalities, conversation memory, export, and summarization.

---

## ✨ Features

- 🎭 **7 AI Personalities** — Switch between modes instantly
- 🧠 **Conversation Memory** — Remembers full chat history per session
- ⚙️ **Customizable Settings** — Control creativity and response length
- 🛠️ **Custom System Prompt** — Override any personality with your own instructions
- 📋 **Summarize Chat** — Get a 5-point summary of your conversation
- 💾 **Export Chat** — Download your full conversation as text
- 📊 **Session Stats** — Track messages and personalities used
- ⚡ **Quick Prompts** — One-click starter questions

---

## 🎭 Available Personalities

| Personality | Best For |
|-------------|----------|
| 🤖 Default Assistant | General questions & knowledge |
| 👨‍💻 Code Expert | Programming, debugging, code reviews |
| 🧠 Deep Thinker | Philosophy, analysis, deep discussions |
| 🎓 Study Tutor | Learning any subject step by step |
| ✍️ Creative Writer | Stories, poems, blogs, essays |
| 💼 Business Advisor | Strategy, startups, career advice |
| 😄 Fun & Humor | Jokes, banter, entertainment |

---

## 🧰 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Groq API** | LLM backend (LLaMA 3.3 70B Versatile) |
| **Gradio** | Chat UI interface |
| **Python** | Core language |

---

## 📁 Project Structure
ai-chat-assistant/
├── app.py            # Main application
├── requirements.txt  # Dependencies
└── README.md

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-chat-assistant.git
cd ai-chat-assistant
```

### 2. Install dependencies
```bash
pip install groq gradio
```

### 3. Set your Groq API Key
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```
> Get your free API key at: https://console.groq.com

### 4. Run the app
```bash
python app.py
```


---

## 💬 Example Use Cases
👨‍💻 "Write a REST API in FastAPI with authentication"
🎓 "Explain neural networks like I'm a beginner"
✍️ "Write a short story about a robot learning to feel emotions"
💼 "How do I validate my startup idea before building?"
😄 "Tell me the funniest joke you know"
🧠 "Is free will real or just an illusion?"

---

## 🖥️ UI Overview
┌─────────────────┬──────────────────────────────┐
│  🎭 Personality  │                              │
│  ⚙️ Settings     │     💬 Chat Window           │
│  🛠️ Custom Prompt│                              │
│  🔧 Actions      │     📝 Message Input         │
│  📄 Output Box   │     ⚡ Quick Prompts          │
└─────────────────┴──────────────────────────────┘

---

## 🚀 Deployment

### Deploy on Hugging Face Spaces:
1. Create a new Space at huggingface.co/spaces
2. Choose **Gradio** as the SDK
3. Upload `app.py` and `requirements.txt`
4. Add `GROQ_API_KEY` in Space Secrets settings
5. Your app goes live automatically! ✅

   link
   https://huggingface.co/spaces/jeevitha-app/ai-agent

---

## 📦 Requirements
groq
gradio

---

## 👤 Author
**Jeevitha M**
Data Science

---

## ⭐ If you found this useful, give it a star!
