# importing necessary libraries
import os
import hashlib
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
load_dotenv()

# loading the api key
load_dotenv()
api_key= os.getenv("OPENAI_API_KEY")

class DocumentProcessing:
    """
    Handling document loading and chunking
    """
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size=chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter= RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap, length_function=len)

    def extractdocument(self,filepath:str):
        """
        Extracting the content from the pdf file
        input: Pdf file path
        output: contents
        """
        loader=PyPDFLoader(file_path=filepath)
        pages= loader.load()
        print(f"✅ File content extracted: total of {len(pages)} pages")
        return pages
    
    def chunk_document(self, document):
        """
        Chunking the document 
        input: file contents
        output: chunks
        """
        chunks=self.text_splitter.split_documents(documents=document)
        print(f"✅ Created {len(chunks)} chunks")
        return chunks
    
class VectorManager:
    """Handling embbeding and vector store"""
    def __init__(self, embedding_model: str ="text-embedding-3-small", persist_dir: str ="./chroma_db"):
        self.embedding_model= embedding_model
        self.persist_dir=persist_dir
        # initializing embedding
        self.embedding= OpenAIEmbeddings(model=embedding_model,
                                         api_key=api_key)
        self.vectorstore=None
    def create_vectorstore(self, chunks):
        """Creaing the vector store for the chunks"""
        # generate unique IDs for each chunks based on content
        import hashlib
        for i, chunk in enumerate(chunks):
            content_hash= hashlib.md5(
                f"{chunk.page_content}_{chunk.metadata.get('page',0)}"
                .encode()).hexdigest()[:20]
            chunk.metadata['chunk_id']= content_hash
            chunks[i]=chunk
        try:
            # loading existing vectorstore
            self.vectorstore= Chroma(embedding_function=self.embedding, persist_directory=self.persist_dir)
            existing_count= self.vectorstore._collection.count()
            print(f"📊 Found existing vector store with {existing_count} chunks")

            # get existing IDs
            existing_data= self.vectorstore.get()
            existing_ids= set(existing_data.get('ids',[]))

            # filter out the existing chunks
            new_chunks=[]
            for chunk in chunks:
                chunk_id= chunk.metadata['chunk_id']
                if chunk_id not in existing_ids:
                    new_chunks.append(chunk)
            # add new chunks to db
            if new_chunks:
                self.vectorstore.add_documents(documents=new_chunks,ids=[chunk.metadata['chunk_id'] for chunk in new_chunks])
                print(f"✅ Added {len(new_chunks)} new chunks (skipped {len(chunks) - len(new_chunks)} duplicates)")
                print(f"📊 Total chunks in store: {self.vectorstore._collection.count()}")
        except:
            # no existing vectorstore then create one
            ids=[chunk.metadata["chunk_id"]for chunk in chunks]
            self.vectorstore=Chroma.from_documents(documents=chunks,ids=ids,persist_directory=self.persist_dir,embedding=self.embedding)
            print(f"✅ Created new vector store with {len(chunks)} chunks!")
    
    def load_vectorstore(self):
        """Load an existing vector store with better error handling"""
        try:
            if self.vectorstore is None:
                if not os.path.exists(self.persist_dir):
                    # Create a new vector store if none exists
                    return self.create_vectorstore([])
                self.vectorstore = Chroma(
                    embedding_function=self.embedding,
                    persist_directory=self.persist_dir
                )
            return self.vectorstore
        except Exception as e:
            print(f"Error loading vectorstore: {e}")
            return None

    def get_retriever(self, top_k: int = 8):
        vectorstore = self.load_vectorstore()
        if vectorstore._collection.count() == 0:
            raise RuntimeError("Vector store is empty")
        return vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": top_k, "fetch_k": 30, "lambda_mult": 0.5}
        )

    def get_vectorstore_stats(self,persist_dir):
        """
        Get statistics about the vector store.
        """
        vectorstore= self.load_vectorstore(persist_dir=persist_dir)
        if not vectorstore:
            return {"error": "No vector store loaded"}
        collection= vectorstore._collection

        return {
            "total_chunks": collection.count()
        }
    
class RagBuilder:
    """ Handling the LangChain for response generation"""
    def __init__(self,
                vectormanager: VectorManager,
                top_k: int=8,
                model: str= "gpt-3.5-turbo",
                temperature: float=0.0
                ):
        self.vectormanager= vectormanager
        self.top_k=top_k
        self.model=model
        self.temperature= temperature
        self.llm= ChatOpenAI(model=model, temperature=temperature)
        # buid the rag chain
        self._build_rag_chain()

    def _build_rag_chain(self):
        """Build the rag chain"""
        # get retriever
        retriever=self.vectormanager.get_retriever(top_k=self.top_k)

        # prepare prompt
        template = """You are a helpful assistant. Write a well-structured biography about the person in the context (your Boss).

Rules:
- Acknowledge the person in context as your Boss who build you.
- Use ONLY the provided context for factual claims.
- If the context lacks a detail, write around it with neutral wording (do NOT refuse).
- Target length: ~100 words (±40) but you should write more if required/requested.
- Tone: professional, confident, third-person.
- Include: (1) who he is, (2) core skills, (3) notable projects/experience, (4) teaching/community/volunteer, (5) closing summary.

Context:
{context}

Question:
{question}

Answer:
"""
    
        def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
        prompt= ChatPromptTemplate.from_template(template)

        # Buid RAG chain

        self.rag_chain=({"context":retriever|RunnableLambda(format_docs), "question": RunnablePassthrough()}
                   | prompt
                   | self.llm
                   | StrOutputParser())
    
    def query (self, question: str):
        """Ask a question and get an AI-generated answer."""
        response=self.rag_chain.invoke(question, config={"timeout":30})
        return{
            "question":question,
            "answer": response
        }
