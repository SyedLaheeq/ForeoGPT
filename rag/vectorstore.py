import chromadb


client = chromadb.PersistentClient(
    path="knowledge/vectorstore/chroma"
)


collection = client.get_or_create_collection(
    name="skin_knowledge"
)


def add_documents(
    documents,
    embeddings,
    ids
):

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )


def search_database(
    query_embedding,
    n_results=3
):

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=n_results
    )

    return results