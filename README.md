# Cricket Chatbot using LangChain, Ollama, and ChromaDB

This is a **Cricket Chatbot** built using **LangChain**, **Ollama**, and **Mistral LLM**. It scrapes cricket-related data from **NDTV.com** using **BeautifulSoup**, stores it in **ChromaDB**, and allows users to chat about cricket-related information using the data stored in the database.

---

## 🚀 Features
- **Web Scraping**: Uses BeautifulSoup to fetch live cricket data from **NDTV.com**.
- **Vector Database**: Stores the scraped data in **ChromaDB**.
- **Data Chunking**: Splits data for better retrieval and efficient processing.
- **LLM-Powered Chat**: Uses **Ollama** locally with **Mistral:7B-Instruct-Q4_K_M** for natural language responses.
- **Interactive Chatbot**: Allows users to ask queries related to cricket based on the stored data.

---

## 🛠️ Installation & Setup
### 1️⃣ Install Requirements
Make sure you have **Python 3.8+** installed. Clone the repository and install dependencies:
```sh
pip install -r requirements.txt
```

### 2️⃣ Install & Setup Ollama Locally
Install Ollama following the official [Ollama installation guide](https://ollama.ai/). Then, download the required **Mistral** model:
```sh
ollama pull mistral:7b-instruct-q4_K_M
```

### 3️⃣ Run the Project
Execute the following commands in order:

#### 1️⃣ Scrape Data:
```sh
python scraper/scraper.py
```

#### 2️⃣ Ingest Data into Vector Database:
```sh
python ingest.py
```

#### 3️⃣ Start the Chatbot:
```sh
python chat.py
```

---

## 📁 Project Structure
```
📂 cricket-chatbot
│-- 📂 scraper
│   └── scraper.py  # Fetches cricket data from NDTV
│-- ingest.py       # Stores scraped data into ChromaDB
│-- chat.py         # Runs the chatbot using LangChain
│-- requirements.txt # Dependencies
│-- README.md       # Project documentation
```

---

## 🤖 Usage
Once the chatbot is running, you can ask questions like:
- **"Who won the last cricket match?"**
- **"What is the latest cricket news?"**
- **"Which team is leading in ICC rankings?"**

The chatbot will provide responses based on the scraped and stored data.

---

## 🔗 Credits & References
- **LangChain** - [Docs](https://python.langchain.com/)
- **Ollama** - [Website](https://ollama.ai/)
- **Mistral LLM** - [Model](https://mistral.ai/)
- **ChromaDB** - [Docs](https://www.trychroma.com/)

---

## 🎯 Future Enhancements
- Integrate **real-time API fetching** instead of static scraping.
- Improve **vector search efficiency**.
- Deploy chatbot on a **web interface**.

---

💡 **Contributions are welcome!** Feel free to fork, open issues, or submit pull requests. Happy Coding! 🚀

