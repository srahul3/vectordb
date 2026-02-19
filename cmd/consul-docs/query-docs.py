import chromadb
import sys

# Initialize a persistent client
# This saves the database to the directory './chroma_db'
# Note: We need to make sure we point to the same directory used in main-persistance.py
# Since that script ran in specific directory, let's assume this is run from the project root
# or adjust path accordingly.
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Get the collection
collection = chroma_client.get_or_create_collection(name="consul-docs")

print("Welcome to Consul Docs Query Interface!")
print("Type 'exit' or 'quit' to stop.")

while True:
    try:
        query = input("\nEnter your question: ")
        if query.lower() in ['exit', 'quit']:
            break

        if not query.strip():
            continue

        print(f"Querying: {query}...")
        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        print("\nResults:")
        # chromadb results structure: {'ids': [['id1', 'id2']], 'distances': [[0.1, 0.2]], 'metadatas': [[{...}, {...}]], 'documents': [['doc1', 'doc2']]}
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                source = results['metadatas'][0][i].get('source', 'Unknown')
                print(f"\n--- Result {i+1} (Source: {source}) ---")
                print(doc[:500] + "..." if len(doc) > 500 else doc)
        else:
            print("No results found.")

    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except EOFError:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
