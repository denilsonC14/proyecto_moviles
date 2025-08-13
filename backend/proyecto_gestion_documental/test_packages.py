#!/usr/bin/env python3
"""Test script to verify all Python packages are installed correctly."""

def test_imports():
    """Test if all required packages can be imported."""
    try:
        import fastapi
        print("[OK] FastAPI installed successfully")
        
        import uvicorn
        print("[OK] Uvicorn installed successfully")
        
        import langchain
        print("[OK] LangChain installed successfully")
        
        import sentence_transformers
        print("[OK] Sentence Transformers installed successfully")
        
        import chromadb
        print("[OK] ChromaDB installed successfully")
        
        import ollama
        print("[OK] Ollama Python package installed successfully")
        
        print("\nAll Python packages installed successfully!")
        return True
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()