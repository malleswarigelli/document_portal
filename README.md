'''
create virtual environmnet : conda create -n llmops python==3.10 -y
activate virtual enviromnet: conda activate llmops

# install requirements
pip install -r requirements.txt

# git commands
initialze git: git init
git add .
git commit -m "your commit message"
git push origin main


### Requirements for this project
1. LLM Model ## from groq, huggingface (free), openai, claue (paid), gemini (15 days free access), Ollama (local setup)
2. Embedding model ## huggingface (free), openai, gemini (paid)
3. Vector database ## inmemory (chroma DB, FAISS), ## ondisk ## cloud based for deployment (AWS bedrock)




'''