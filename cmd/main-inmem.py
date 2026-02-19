import chromadb

# 1. Get the Chroma Client
# For persistence, use chromadb.PersistentClient(path="./chroma_db")
chroma_client = chromadb.Client()

# 2. Create a collection
collection = chroma_client.create_collection(name="my_collection")

# 3. Add some text documents to the collection
collection.add(
    documents=[
        "This is a document",
        "This is another document",
        "This is a third document"
    ],
    metadatas=[
        {"source": "my_source"},
        {"source": "my_source"},
        {"source": "my_source"}
    ],
    ids=["id1", "id2", "id3"]
)

# 4. Query the collection
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2
)

print("Query Results:")
print(results)
