from rag.embeddings import create_embedding


result = create_embedding(
    "Red LED supports skincare routines"
)


print(len(result))