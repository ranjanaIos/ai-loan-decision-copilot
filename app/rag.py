from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .config import DB_DIR, CHAT_MODEL, EMBED_MODEL


def ask_question(query):
    # Load DB
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 4})

    # LLM
    llm = ChatOllama(model=CHAT_MODEL)

    # Prompt
    prompt = ChatPromptTemplate.from_template(
        """You are a company policy assistant.
Answer ONLY from the provided context.
If not found, say 'Not mentioned in policy'.

Context:
{context}

Question:
{question}
"""
    )

    # Chain (modern LCEL)
    chain = (
        {"context": retriever, "question": lambda x: x}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(query)