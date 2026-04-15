"""
FREE RAG System - Retrieval Augmented Generation
Allows AI to read and understand your documents
100% Free, Offline capable, No API costs
"""

import os
import json
from typing import List, Dict, Optional
from pathlib import Path

# Try to import required libraries
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("[!] sentence-transformers not installed")

try:
    import faiss
    import numpy as np
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("[!] faiss-cpu not installed")


class DocumentStore:
    """Simple document storage and retrieval."""
    
    def __init__(self, storage_path: str = "documents_db.json"):
        self.storage_path = storage_path
        self.documents = []
        self.load()
    
    def load(self):
        """Load documents from disk."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
            except:
                self.documents = []
    
    def save(self):
        """Save documents to disk."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, indent=2)
        except Exception as e:
            print(f"[!] Could not save documents: {e}")
    
    def add_document(self, content: str, metadata: Dict = None):
        """Add a document."""
        doc = {
            "id": len(self.documents),
            "content": content,
            "metadata": metadata or {}
        }
        self.documents.append(doc)
        self.save()
        return doc["id"]
    
    def get_document(self, doc_id: int) -> Optional[Dict]:
        """Get document by ID."""
        for doc in self.documents:
            if doc["id"] == doc_id:
                return doc
        return None
    
    def get_all_documents(self) -> List[Dict]:
        """Get all documents."""
        return self.documents
    
    def clear(self):
        """Clear all documents."""
        self.documents = []
        self.save()


class RAGSystem:
    """
    FREE Retrieval Augmented Generation system.
    Uses sentence-transformers for embeddings and FAISS for vector search.
    """
    
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        storage_path: str = "rag_data"
    ):
        """
        Initialize RAG system.
        
        Args:
            model_name: Sentence transformer model
                - all-MiniLM-L6-v2: Fast, 384 dims (recommended)
                - all-mpnet-base-v2: Better quality, 768 dims
            storage_path: Directory for storing data
        """
        self.model_name = model_name
        self.storage_path = storage_path
        self.model = None
        self.index = None
        self.doc_store = None
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        # Initialize components
        self._init_components()
    
    def _init_components(self):
        """Initialize all components."""
        # Initialize document store
        doc_path = os.path.join(self.storage_path, "documents.json")
        self.doc_store = DocumentStore(doc_path)
        
        # Initialize embedding model
        if EMBEDDINGS_AVAILABLE:
            try:
                print(f"[🧠] Loading embedding model '{self.model_name}'...")
                self.model = SentenceTransformer(self.model_name)
                print("[✓] Embedding model loaded")
            except Exception as e:
                print(f"[!] Failed to load model: {e}")
                return
        else:
            print("[!] Embeddings not available - install sentence-transformers")
            return
        
        # Initialize FAISS index
        if FAISS_AVAILABLE:
            index_path = os.path.join(self.storage_path, "faiss.index")
            
            if os.path.exists(index_path):
                try:
                    self.index = faiss.read_index(index_path)
                    print(f"[✓] Loaded existing index with {self.index.ntotal} vectors")
                except Exception as e:
                    print(f"[!] Failed to load index: {e}")
                    self._create_new_index()
            else:
                self._create_new_index()
        else:
            print("[!] FAISS not available - install faiss-cpu")
    
    def _create_new_index(self):
        """Create new FAISS index."""
        if not self.model:
            return
        
        # Get embedding dimension
        sample_embedding = self.model.encode(["test"])
        dimension = sample_embedding.shape[1]
        
        # Create index
        self.index = faiss.IndexFlatL2(dimension)
        print(f"[✓] Created new FAISS index (dimension: {dimension})")
    
    def _save_index(self):
        """Save FAISS index to disk."""
        if self.index:
            try:
                index_path = os.path.join(self.storage_path, "faiss.index")
                faiss.write_index(self.index, index_path)
            except Exception as e:
                print(f"[!] Failed to save index: {e}")
    
    def add_document(self, content: str, metadata: Dict = None) -> bool:
        """
        Add document to RAG system.
        
        Args:
            content: Document text
            metadata: Optional metadata (filename, source, etc.)
        
        Returns:
            Success status
        """
        if not self.model or not self.index:
            print("[!] RAG system not initialized")
            return False
        
        try:
            # Add to document store
            doc_id = self.doc_store.add_document(content, metadata)
            
            # Generate embedding
            embedding = self.model.encode([content])
            
            # Add to FAISS index
            self.index.add(embedding.astype('float32'))
            
            # Save index
            self._save_index()
            
            print(f"[✓] Added document (ID: {doc_id})")
            return True
        
        except Exception as e:
            print(f"[!] Failed to add document: {e}")
            return False
    
    def add_file(self, filepath: str) -> bool:
        """
        Add file to RAG system.
        
        Args:
            filepath: Path to text file
        
        Returns:
            Success status
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metadata = {
                "filename": os.path.basename(filepath),
                "filepath": filepath,
                "size": len(content)
            }
            
            return self.add_document(content, metadata)
        
        except Exception as e:
            print(f"[!] Failed to add file: {e}")
            return False
    
    def add_directory(self, directory: str, extensions: List[str] = None) -> int:
        """
        Add all files from directory.
        
        Args:
            directory: Directory path
            extensions: File extensions to include (e.g., ['.txt', '.md'])
        
        Returns:
            Number of files added
        """
        if extensions is None:
            extensions = ['.txt', '.md', '.py', '.js', '.json', '.csv']
        
        count = 0
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    filepath = os.path.join(root, file)
                    if self.add_file(filepath):
                        count += 1
        
        print(f"[✓] Added {count} files from '{directory}'")
        return count
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of relevant documents with scores
        """
        if not self.model or not self.index:
            print("[!] RAG system not initialized")
            return []
        
        if self.index.ntotal == 0:
            print("[!] No documents in index")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])
            
            # Search in FAISS
            distances, indices = self.index.search(
                query_embedding.astype('float32'),
                min(top_k, self.index.ntotal)
            )
            
            # Get documents
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                doc = self.doc_store.get_document(int(idx))
                if doc:
                    results.append({
                        "rank": i + 1,
                        "score": float(distance),
                        "document": doc
                    })
            
            return results
        
        except Exception as e:
            print(f"[!] Search error: {e}")
            return []
    
    def get_context(self, query: str, max_length: int = 2000) -> str:
        """
        Get context for query (for LLM prompts).
        
        Args:
            query: User query
            max_length: Maximum context length
        
        Returns:
            Context string
        """
        results = self.search(query, top_k=3)
        
        if not results:
            return ""
        
        context = "Relevant information:\n\n"
        current_length = len(context)
        
        for result in results:
            doc = result["document"]
            content = doc["content"]
            
            # Add document with truncation if needed
            if current_length + len(content) > max_length:
                remaining = max_length - current_length
                content = content[:remaining] + "..."
            
            context += f"--- Document {result['rank']} ---\n"
            context += content + "\n\n"
            current_length = len(context)
            
            if current_length >= max_length:
                break
        
        return context
    
    def get_statistics(self) -> Dict:
        """Get RAG system statistics."""
        return {
            "total_documents": len(self.doc_store.documents),
            "total_vectors": self.index.ntotal if self.index else 0,
            "model": self.model_name,
            "embeddings_available": EMBEDDINGS_AVAILABLE,
            "faiss_available": FAISS_AVAILABLE,
            "ready": bool(self.model and self.index)
        }
    
    def clear(self):
        """Clear all data."""
        self.doc_store.clear()
        if self.index:
            self._create_new_index()
            self._save_index()
        print("[✓] RAG system cleared")


# ─── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  🧠 FREE RAG System - Test Mode")
    print("=" * 60)
    
    # Check availability
    print("\n📊 System Status:")
    if EMBEDDINGS_AVAILABLE:
        print("  ✅ Sentence Transformers available")
    else:
        print("  ❌ Sentence Transformers not available")
        print("     Install: pip install sentence-transformers")
    
    if FAISS_AVAILABLE:
        print("  ✅ FAISS available")
    else:
        print("  ❌ FAISS not available")
        print("     Install: pip install faiss-cpu")
    
    if not EMBEDDINGS_AVAILABLE or not FAISS_AVAILABLE:
        print("\n[!] Missing dependencies. Exiting.")
        exit(1)
    
    print("\n" + "=" * 60)
    
    # Initialize RAG system
    rag = RAGSystem(storage_path="test_rag_data")
    
    # Add sample documents
    print("\n[Test] Adding sample documents...")
    
    rag.add_document(
        "Python is a high-level programming language known for its simplicity.",
        {"topic": "programming", "language": "python"}
    )
    
    rag.add_document(
        "Machine learning is a subset of artificial intelligence.",
        {"topic": "ai", "subtopic": "ml"}
    )
    
    rag.add_document(
        "FastAPI is a modern web framework for building APIs with Python.",
        {"topic": "programming", "framework": "fastapi"}
    )
    
    rag.add_document(
        "Neural networks are computing systems inspired by biological brains.",
        {"topic": "ai", "subtopic": "neural-networks"}
    )
    
    # Get statistics
    print("\n📊 Statistics:")
    stats = rag.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test search
    print("\n🔍 Search Tests:")
    
    queries = [
        "What is Python?",
        "Tell me about AI",
        "How to build APIs?"
    ]
    
    for query in queries:
        print(f"\n  Query: '{query}'")
        results = rag.search(query, top_k=2)
        
        for result in results:
            doc = result["document"]
            print(f"    Rank {result['rank']} (score: {result['score']:.4f})")
            print(f"    → {doc['content'][:80]}...")
    
    # Test context generation
    print("\n📝 Context Generation Test:")
    query = "Explain machine learning"
    context = rag.get_context(query, max_length=500)
    print(f"\n  Query: '{query}'")
    print(f"  Context:\n{context}")
    
    # Clean up
    print("\n[Test] Cleaning up...")
    rag.clear()
    
    # Remove test directory
    import shutil
    if os.path.exists("test_rag_data"):
        shutil.rmtree("test_rag_data")
    
    print("\n✅ All tests passed!")
    print("=" * 60)
