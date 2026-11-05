from rag.embeddings import create_embedding
from rag.vectorstore import search_database



def retrieve_information(query):

    query_embedding = create_embedding(
        query
    )


    results = search_database(
        query_embedding,
        n_results=3
    )


    return results



if __name__ == "__main__":


    query = (
        "What FOREO routine is suitable "
        "for increased redness?"
    )


    results = retrieve_information(
        query
    )


    print("\nRetrieved documents:\n")


    for doc in results["documents"][0]:

        print("----------------")
        print(doc)