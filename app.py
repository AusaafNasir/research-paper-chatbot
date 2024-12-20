import streamlit as st
from query_engine import search_query

# Streamlit UI Setup
st.title("AI Research Paper Chatbot 📚")
st.write("Ask a question, and I'll find relevant research papers for you!")

# Input box for the user query
query = st.text_input("Enter your research question:")

# Search and display results
if query:
    st.subheader("Searching for Relevant Papers...")
    results = search_query(query, top_k=5)

    if results:
        st.subheader("Top Relevant Papers:")
        for result in results:
            st.markdown(f"**[Title: {result['title']}]({result['link']})**")
            st.write(f"Relevance Score: {result['relevance']:.4f}")
            
            # Display matching snippets
            st.write("**Relevant Snippets:**")
            for snippet, score in result["snippets"]:
                st.write(f"- {snippet} (Score: {score:.4f})")
            
            st.write("---")  
    else:
        st.write("No relevant papers found. Try another query!")
