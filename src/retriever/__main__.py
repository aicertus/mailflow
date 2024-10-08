from retriever import rag_retrieval

retriever = rag_retrieval()
retriever.read_db()
response = retriever.query("Resume las reuniones que hay programados para octubre. Indica día del mes, hora, objetivo de la reunión y quién la propone")
print(response.response)