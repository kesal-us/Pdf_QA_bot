# PDF Q&A with Retrieval-Augmented Generation (RAG)

This project is a web-based Question & Answering application that allows users to upload a PDF document and ask questions about its content. It uses a Retrieval-Augmented Generation (RAG) pipeline built with LangChain, Google's Gemini, and ChromaDB for vector storage. The user interface is created with Streamlit.

## Features

-   **PDF Upload**: Easily upload any PDF document through a web interface.
-   **Intelligent Q&A**: Ask questions in natural language and receive context-aware answers based on the document's content.
-   **Persistent Knowledge Base**: The processed PDF is converted into a vector store using ChromaDB and persisted to disk, allowing for quick re-loading without reprocessing.
-   **Isolated Sessions**: Each user session is independent. One user's uploaded document will not be accessible or used in another user's session.
-   **Powered by Google Gemini**: Leverages Google's powerful embedding and generative models for state-of-the-art performance.

## How It Works

The application follows a Retrieval-Augmented Generation (RAG) architecture:

1.  **Load & Chunk**: When a user uploads a PDF, the text is extracted and split into smaller, manageable chunks.
2.  **Embed & Store**: Each text chunk is converted into a numerical representation (embedding) using Google's `text-embedding-004` model. These embeddings are stored in a `ChromaDB` vector database on the local disk.
3.  **Retrieve**: When a user asks a question, their query is also converted into an embedding. The application then performs a similarity search in the ChromaDB to find the most relevant text chunks from the original PDF.
4.  **Generate**: The retrieved text chunks (the context) and the user's original question are passed to the `gemini-2.0-flash-lite` model. The model then generates a comprehensive answer based *only* on the provided context.

## Tech Stack

-   **Framework**: LangChain
-   **Frontend**: Streamlit
-   **LLM & Embeddings**: Google Gemini (`gemini-2.0-flash-lite`, `text-embedding-004`)
-   **Vector Database**: ChromaDB
-   **PDF Loading**: PyMuPDF
-   **Environment Variables**: `python-dotenv`

## 📦 Setup and Installation

Follow these steps to run the application on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

*(Note: You will need to create a `requirements.txt` file containing libraries like `streamlit`, `langchain`, `langchain-google-genai`, `langchain-chroma`, `pypdf`, `python-dotenv`, `pymupdf`)*

### 4. Set Up Your Google API Key

The application requires a Google API key to function.

1.  Create a file named `.env` in the root directory of the project.
2.  Add your Google API key to the `.env` file in the following format:

    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
    ```

    Replace `"YOUR_GOOGLE_API_KEY_HERE"` with your actual API key.

    **⚠️ Important Security Note:** The `.env` file contains sensitive credentials. The provided `.gitignore` file should be configured to ignore this file, ensuring it is **never** committed to version control.

## ▶️ How to Run the Application

Once the setup is complete, run the following command in your terminal:

```bash
streamlit run app.py
```

Your web browser will automatically open a new tab with the application running.

## 📂 Project Structure

```
.
├── app.py              # Main Streamlit application file
├── rag_engine.py       # Core RAG logic and class
├── prompt_template.py  # Contains the prompt template for the LLM
├── utils.py            # Helper functions (e.g., loading PDFs)
├── chroma_db/          # Directory where the vector store is persisted
├── .env                # Stores the Google API key (should not be in Git)
└── requirements.txt    # List of Python dependencies
```

## 🔒 Data Persistence and Session Management

A key aspect of this application is how it handles data:

-   **Data Persistence**: The `RAGEngine` class saves the created ChromaDB vector store to a local directory named `chroma_db`. When the application restarts, it will automatically load the existing vector store from this directory, avoiding the need to re-process the last uploaded PDF. To start fresh, simply delete the `chroma_db` directory.