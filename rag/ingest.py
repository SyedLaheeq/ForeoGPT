import json
import os

from rag.embeddings import create_embedding
from rag.vectorstore import add_documents



DATA_PATH = "knowledge/raw"



documents = []
embeddings = []
ids = []



counter = 0


for root, dirs, files in os.walk(DATA_PATH):

    for file in files:

        if file.endswith(".json"):

            path = os.path.join(
                root,
                file
            )


            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)



            text = json.dumps(
                data,
                indent=2
            )


            documents.append(text)


            embeddings.append(
                create_embedding(text)
            )


            ids.append(
                f"doc_{counter}"
            )


            counter += 1



add_documents(
    documents,
    embeddings,
    ids
)



print(
    f"✅ Added {len(documents)} documents"
)