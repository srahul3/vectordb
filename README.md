# vectordb

## Setup

Run the setup script to install dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

## Run

Run the example script:

```bash
chmod +x run.sh
./run.sh
```

## Consul Documentation Vector DB

### 1. Populate the Database
This script fetches Consul documentation from GitHub and stores it in a local ChromaDB instance.

```bash
python cmd/consul-docs/main-persistance.py
```

### 2. Query the Knowledge Base
Run an interactive query session to ask questions about Consul configuration.

```bash
python cmd/consul-docs/query-docs.py
```
