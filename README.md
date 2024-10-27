# Cyber II
The second version of Cyber Hammer. The only way to use it is through web browser, but the LLM logic is amazing.

## System Arch

![](./doc/pic/cyber.svg)

## Software in Use

* Front-end User Interface: Streamlit
* LLM (Ollama) and LangChain
    * Basic LangChain tools
    * ChromaDB
    * LangChain for Ollama LLM and Ollama Word Embeddings

## Environment

### Python & Conda Env

```bash
conda create -n ai python=3.11
conda activate ai
pip install -r requirements.txt
```

### Ollama Env

* Download Ollama: [https://ollama.com/download](https://ollama.com/download)
* Install LLM and Embedding Model

```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```