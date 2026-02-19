import chromadb
import requests


# Initialize a persistent client
# This saves the database to the directory './chroma_db'
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 2. Create a collection
collection = chroma_client.get_or_create_collection(name="consul-docs")

def fetch_github_files(owner, repo, path, branch='main'):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Error fetching tree: {response.status_code}")
        return []

    tree = response.json().get('tree', [])
    files_data = []

    for item in tree:
        if item['path'].startswith(path) and item['type'] == 'blob':
             # focusing on md/mdx files for docs
            if not item['path'].endswith('.md') and not item['path'].endswith('.mdx'):
                 continue

            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{item['path']}"
            print(f"Fetching {item['path']}...")
            file_resp = requests.get(raw_url)
            if file_resp.status_code == 200:
                files_data.append({
                    "path": item['path'],
                    "content": file_resp.text
                })

    return files_data

# URL: https://github.com/hashicorp/web-unified-docs/tree/main/content/consul/v1.22.x
owner = "hashicorp"
repo = "web-unified-docs"
path = "content/consul/v1.22.x"

print("Fetching documents from GitHub...")
docs = fetch_github_files(owner, repo, path)

if docs:
    documents = [doc['content'] for doc in docs]
    metadatas = [{"source": doc['path']} for doc in docs]
    ids = [doc['path'] for doc in docs]

    print(f"Adding {len(documents)} documents to collection...")
    # 3. Add some text documents to the collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
else:
    print("No documents found.")

# 4. Query the collection
query = "How do I configure Consul?"
print(f"\nQuerying: {query}")
results = collection.query(
    query_texts=[query],
    n_results=2
)

print("Query Results:")
print(results)
