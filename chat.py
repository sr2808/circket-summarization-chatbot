from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
from models import Models

# Initialize models
models = Models()
embeddings = models.embeddings_ollama
llm = models.model_ollama

# Initialize vector store
vector_store = Chroma(
    collection_name="cricket-documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db",
)

# Chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a cricket analyst. Answer the user's query based only on the provided match data."),
        ("human", "Use the user question: {input}. Based on the following match data: {context}. Provide a detailed response."),
    ]
)

# Retrieval setup
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retriever_chain = create_retrieval_chain(retriever, combine_docs_chain)

# Chat loop
def main():
    while True:
        query = input("User (or type 'q', 'quit' or 'exit' to end): ")
        if query.lower() in ["q", "quit", "exit"]:
            break

        # Retrieve relevant documents
        retrieved_docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])  # Extract text
        # print(f"Context: {context}")
        # Ensure correct input format for retriever_chain
        result = retriever_chain.invoke({"input": query, "context": context})

        # Debug output format if needed
        if "answer" in result:
            print("\nAssistant:", result["answer"], "\n")
        else:
            print("\nAssistant:", result, "\n")  # Fallback if key is different

if __name__ == "__main__":
    main()
