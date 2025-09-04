from langchain.prompts import PromptTemplate

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful AI assistant.
Use the context below to answer the question thoroughly with as much relevant information possible include details.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question:
{question}

Answer:"""
)
