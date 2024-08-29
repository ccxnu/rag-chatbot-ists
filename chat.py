from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from get_embedding_function import get_embedding_function

OLLAMA_MODEL = "llama3.1:8b"
PERSIST_DIRECTORY = "db"

# Define the RAG prompt template
RAG_TEMPLATE = """
Eres un asistente español experimentado, experto en interpretar y responder preguntas basadas en las fuentes proporcionadas. Utilizando el contexto proporcionado entre las etiquetas <context></context>, genera una respuesta concisa para una pregunta rodeada con las etiquetas <question></question>. Debes usar únicamente información del contexto. Usa un tono imparcial y formal. No repitas texto. Si no hay nada en el contexto relevante para la pregunta en cuestión, simplemente di "No lo sé". No intentes inventar una respuesta. Responde en unas 5 líneas y sé conciso.

<context>
{context}
</context>

Responde la siguiente pregunta:

<question>
{question}
</question>"""

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def answer_question_with_context(question):
    messages = []
    persist_directory = PERSIST_DIRECTORY
    local_embeddings = get_embedding_function()

    vectorstore = Chroma(
        persist_directory=persist_directory, embedding_function=local_embeddings
    )

    docs = vectorstore.similarity_search_with_score(question, k=5)
    if not docs:
        messages.append("No relevant information was found")
        return

    rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
    model = ChatOllama(model=OLLAMA_MODEL)

    chain = (
        RunnablePassthrough.assign(context=lambda input: format_docs(input["context"]))
        | rag_prompt
        | model
        | StrOutputParser()
    )

    response = chain.invoke({"context": docs, "question": question})
    return {"response": response, "messages": messages}
