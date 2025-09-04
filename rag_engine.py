import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from prompt_template import QA_PROMPT

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

load_dotenv()

PERSIST_DIR = "chroma_db"

class RAGEngine:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004"
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            temperature=0.3,
            top_p=0.2,
            generation_config={"max_output_tokens": 1024}       
        )
        self.vectordb = None

        if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
            print("Loading existing vectorstore from disk...")
            self.vectordb = Chroma(
                embedding_function=self.embeddings,
                persist_directory=PERSIST_DIR
            )
        else:
            print("No existing vectorstore found. Please upload a PDF.")

    def build_vector_store(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        texts = splitter.split_documents(documents)

        self.vectordb = Chroma.from_documents(
            texts,
            embedding=self.embeddings,
            persist_directory=PERSIST_DIR
        )
        print("Vectorstore built and persisted to disk.")

    def query(self, question):
        if not self.vectordb:
            return "Knowledge base is not ready. Please upload and process a PDF first."

        results = self.vectordb.similarity_search_with_score(question, k=3)

        if not results:
            return (
                "I'm unable to answer this question as it doesn't appear related to the uploaded document."
            )

        for i, (doc, score) in enumerate(results, 1):
            print(f"Chunk {i}: similarity score = {score:.4f}")

        context = "\n\n".join([doc.page_content for doc, _ in results])

        prompt = QA_PROMPT.format(
            context=context.strip(),
            question=question.strip()
        )

        response = self.llm.invoke(prompt)

        chain= QA_PROMPT | self.llm

        response = chain.invoke({'context':context.strip(), 'question':question.strip()})
        return response.content
