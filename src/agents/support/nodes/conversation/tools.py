#Declaro un arreglo de ID donde esta mi RAG en OpenAI
openai_vector_store_ids=[
    "vs_6ad697ce3b0c81918cad194beb70a4a4"
]
#Declaro la tool a usar propias de OpenAI
file_search_tool = {
    "type": "file_search",
    "vector_store_ids": openai_vector_store_ids
}


tools= [file_search_tool]