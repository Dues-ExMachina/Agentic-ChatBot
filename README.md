## LangGraph Chatbot

This is a multi-turn chatbot application built with Streamlit and LangGraph. The chatbot can use various tools like a calculator, a stock price checker, and a search engine to answer your questions.

### Features

- **Conversational Memory:** The chatbot remembers previous turns in the conversation.
- **Tool Use:** The chatbot can use external tools to answer questions it can't answer on its own. It can:
    - Perform calculations (add, subtract, multiply, divide).
    - Fetch the latest stock prices.
    - Search the web for information.
- **Web Interface:** A simple and intuitive web interface built with Streamlit.
- **Conversation History:** The chatbot saves your conversations, and you can switch between them.

### Technologies Used

- **LangGraph:** A library for building stateful, multi-agent applications with LLMs.
- **LangChain:** A framework for developing applications powered by language models.
- **Streamlit:** A Python library for building and sharing web apps for data science and machine learning.
- **Google Generative AI:** The "Gemini 1.5 Flash" model is used as the core language model.
- **DuckDuckGo Search:** Used as a search engine tool.
- **Alpha Vantage:** Used to get the latest stock prices.

### Getting Started

To run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/langgraph-chatbot.git
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file and add your Google API key:**

   ```
   GOOGLE_API_KEY="your-google-api-key"
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

### Usage

1. Open the app in your browser (usually at `http://localhost:8501`).
2. Type a message in the chat input box and press Enter.
3. The chatbot will respond to your message. If it needs to use a tool, you'll see a "Using tool..." message.
4. To start a new conversation, click the "New Chat" button in the sidebar.
5. To switch between conversations, click on a thread ID in the sidebar.

### File Descriptions

- **`app.py`:** This file contains the Streamlit code for the user interface.
- **`backend.py`:** This file contains the LangGraph code for the chatbot's backend.
- **`requirements.txt`:** This file lists the Python dependencies for the project.