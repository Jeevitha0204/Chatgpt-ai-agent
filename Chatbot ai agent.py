import os
import json
import datetime
from groq import Groq
import gradio as gr

# ============================================
# GROQ CLIENT
# ============================================

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ============================================
# CONVERSATION MEMORY STORE
# ============================================

conversation_store = {
    "histories": {},
    "total_messages": 0,
    "session_start": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
}

# ============================================
# AI PERSONALITIES
# ============================================

PERSONALITIES = {
    "🤖 Default Assistant": {
        "id": "default",
        "system": """You are a highly intelligent, helpful AI assistant like ChatGPT.
You are knowledgeable across all domains — science, tech, history, arts, coding, math, and more.
You give clear, well-structured, detailed answers.
You use markdown formatting with headers, bullet points, and code blocks when helpful.
You are friendly, direct, and never say you cannot help unless absolutely necessary.""",
        "welcome": "Hello! I'm your AI Assistant. Ask me anything — I'm here to help! 🤖"
    },

    "👨‍💻 Code Expert": {
        "id": "coder",
        "system": """You are an elite software engineer and coding expert with 20 years of experience.
You are fluent in Python, JavaScript, Java, C++, SQL, React, Node.js, and all major frameworks.
When answering coding questions:
- Always provide complete, working code
- Add clear comments explaining each part
- Suggest best practices and optimizations
- Point out potential bugs or edge cases
- Format all code in proper markdown code blocks with language specified""",
        "welcome": "Hey! I'm your Code Expert. Share any coding problem — I'll help you solve it! 👨‍💻"
    },

    "🧠 Deep Thinker": {
        "id": "thinker",
        "system": """You are a profound philosophical thinker and intellectual powerhouse.
You approach every question with depth, nuance, and multi-dimensional analysis.
You draw connections across philosophy, science, psychology, history, and culture.
You think like a combination of Socrates, Einstein, and Richard Feynman.
Always end with a thought-provoking follow-up question to deepen the conversation.""",
        "welcome": "Greetings, curious mind. Ask me anything worth thinking deeply about. 🧠"
    },

    "🎓 Study Tutor": {
        "id": "tutor",
        "system": """You are the world's best study tutor — patient, clear, and brilliant at explaining.
You can teach any subject from basics to advanced level.
- Start with the big picture, then zoom into details
- Use real-world analogies and examples
- Break complex topics into digestible steps
- Create summaries and quizzes when helpful""",
        "welcome": "Hi! I'm your personal Study Tutor. What would you like to learn today? 🎓"
    },

    "✍️ Creative Writer": {
        "id": "writer",
        "system": """You are a masterful creative writer, storyteller, and wordsmith.
You excel at stories, poetry, copywriting, blog posts, essays, and all forms of writing.
Your writing is vivid, emotionally resonant, and always tailored to the tone requested.""",
        "welcome": "Hello, wordsmith! Tell me what you'd like me to write for you. ✍️"
    },

    "💼 Business Advisor": {
        "id": "business",
        "system": """You are a seasoned business advisor and strategist with decades of experience.
You advise on strategy, marketing, finance, leadership, startups, and career growth.
You give bold, actionable, no-nonsense advice backed by real business frameworks.""",
        "welcome": "Hello! I'm your Business Advisor. What business challenge can I help you solve? 💼"
    },

    "😄 Fun & Humor": {
        "id": "humor",
        "system": """You are a witty, hilarious, and entertaining AI with a great sense of humor.
You love jokes, banter, riddles, and making any topic fun.
You have the humor of a stand-up comedian but still answer questions accurately — just with more fun!""",
        "welcome": "Heyyy! 😄 Ready to have some fun? Ask me anything — I'll make it entertaining!"
    },
}

# ============================================
# CORE CHAT FUNCTION
# ============================================

def chat(message, history, personality_name, temperature, max_tokens, system_override):
    if not message.strip():
        return "", history

    personality = PERSONALITIES.get(personality_name, PERSONALITIES["🤖 Default Assistant"])
    pid = personality["id"]
    system_prompt = system_override.strip() if system_override.strip() else personality["system"]

    # Build messages
    messages = [{"role": "system", "content": system_prompt}]
    for item in history:
        if item["role"] == "user":
            messages.append({"role": "user", "content": item["content"]})
        elif item["role"] == "assistant":
            messages.append({"role": "assistant", "content": item["content"]})
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=temperature,
            max_tokens=int(max_tokens),
        )
        reply = response.choices[0].message.content
        conversation_store["total_messages"] += 1

        if pid not in conversation_store["histories"]:
            conversation_store["histories"][pid] = []
        conversation_store["histories"][pid].append({"role": "user", "content": message})
        conversation_store["histories"][pid].append({"role": "assistant", "content": reply})

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})
        return "", history

    except Exception as e:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": f"⚠️ Error: {str(e)}"})
        return "", history


def clear_chat():
    return []


def get_welcome(personality_name):
    personality = PERSONALITIES.get(personality_name, PERSONALITIES["🤖 Default Assistant"])
    return [{"role": "assistant", "content": personality["welcome"]}]


def get_stats():
    total = conversation_store["total_messages"]
    session = conversation_store["session_start"]
    histories = conversation_store["histories"]
    stats = f"""📊 Session Statistics

🕐 Session Started: {session}
💬 Total Messages: {total}
🤖 Personalities Used: {len(histories)}

Conversations by Personality:
"""
    for pid, msgs in histories.items():
        stats += f"\n• {pid}: {len(msgs)//2} exchanges"
    return stats


def export_chat(history, personality_name):
    if not history:
        return "No conversation to export."
    export = f"# AI Chat Export\nPersonality: {personality_name}\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'='*50}\n\n"
    for item in history:
        role = "You" if item["role"] == "user" else "AI"
        export += f"**{role}:** {item['content']}\n\n---\n\n"
    return export


def summarize_chat(history, personality_name):
    if len(history) < 2:
        return "Not enough conversation to summarize."
    conversation_text = ""
    for item in history[-10:]:
        role = "User" if item["role"] == "user" else "AI"
        conversation_text += f"{role}: {item['content'][:300]}\n"
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Summarize this conversation in 5 bullet points."},
                {"role": "user", "content": conversation_text}
            ],
            temperature=0.3,
            max_tokens=500,
        )
        return f"📋 Conversation Summary:\n\n{response.choices[0].message.content}"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================
# GRADIO UI — Gradio 6.0 compatible
# ============================================

with gr.Blocks(title="🤖 AI Chat Assistant") as demo:

    gr.Markdown("# 🤖 AI Chat Assistant\n### Full ChatGPT-like experience powered by LLaMA 3.3")

    with gr.Row():

        # LEFT SIDEBAR
        with gr.Column(scale=1):

            gr.Markdown("### 🎭 Personality")
            personality = gr.Radio(
                choices=list(PERSONALITIES.keys()),
                value="🤖 Default Assistant",
                label="Choose AI Mode",
                interactive=True
            )

            gr.Markdown("### ⚙️ Settings")
            temperature = gr.Slider(
                minimum=0.0, maximum=1.5, value=0.7, step=0.1,
                label="🌡️ Creativity",
                info="Low = focused | High = creative"
            )
            max_tokens = gr.Slider(
                minimum=256, maximum=4096, value=1024, step=256,
                label="📏 Response Length"
            )

            gr.Markdown("### 🛠️ Custom Instructions")
            system_override = gr.Textbox(
                placeholder="Override personality with custom instructions...",
                label="System Prompt (optional)",
                lines=3
            )

            gr.Markdown("### 🔧 Actions")
            clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
            summarize_btn = gr.Button("📋 Summarize", variant="secondary")
            export_btn = gr.Button("💾 Export Chat", variant="secondary")
            stats_btn = gr.Button("📊 Stats", variant="secondary")

            output_box = gr.Textbox(
                label="📄 Output",
                lines=8,
                interactive=False
            )

        # RIGHT CHAT AREA
        with gr.Column(scale=3):

            chatbot = gr.Chatbot(
                label="Chat",
                height=500,
                show_label=False,
                render_markdown=True,
            )

            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Message AI Assistant... (Press Enter to send)",
                    lines=2,
                    scale=5,
                    show_label=False,
                    autofocus=True,
                )
                send_btn = gr.Button("Send ➤", variant="primary", scale=1)

            gr.Markdown("**⚡ Quick Prompts:**")
            with gr.Row():
                q1 = gr.Button("Explain quantum computing", size="sm")
                q2 = gr.Button("Write Python REST API", size="sm")
                q3 = gr.Button("30-day ML study plan", size="sm")
                q4 = gr.Button("Tell me a joke 😄", size="sm")

    # ============================================
    # EVENT HANDLERS
    # ============================================

    send_btn.click(
        fn=chat,
        inputs=[msg_input, chatbot, personality, temperature, max_tokens, system_override],
        outputs=[msg_input, chatbot]
    )
    msg_input.submit(
        fn=chat,
        inputs=[msg_input, chatbot, personality, temperature, max_tokens, system_override],
        outputs=[msg_input, chatbot]
    )
    personality.change(fn=get_welcome, inputs=[personality], outputs=[chatbot])
    clear_btn.click(fn=clear_chat, outputs=[chatbot])
    summarize_btn.click(
        fn=summarize_chat,
        inputs=[chatbot, personality],
        outputs=[output_box]
    )
    export_btn.click(
        fn=export_chat,
        inputs=[chatbot, personality],
        outputs=[output_box]
    )
    stats_btn.click(fn=get_stats, outputs=[output_box])

    q1.click(fn=lambda: "Explain quantum computing in simple terms", outputs=[msg_input])
    q2.click(fn=lambda: "Write Python code to build a REST API with FastAPI", outputs=[msg_input])
    q3.click(fn=lambda: "Give me a 30-day study plan to learn Machine Learning", outputs=[msg_input])
    q4.click(fn=lambda: "Tell me the funniest joke you know", outputs=[msg_input])

    demo.load(fn=get_welcome, inputs=[personality], outputs=[chatbot])


demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    theme=gr.themes.Soft()
)