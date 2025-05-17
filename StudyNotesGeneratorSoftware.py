import streamlit as st
from utils.openai_tools import generate_study_notes

st.set_page_config(
    page_title="Study Notes - ExamPrepAI",
    page_icon="📚",
    layout="wide"
)

# Check for API key
if 'gemini_api_key' not in st.session_state:
    st.warning("Please set up your Gemini API key on the main page first.")
    if st.button("🏠 Go to Main Page"):
        st.switch_page("app.py")
else:
    st.title("📚 Study Notes Generator")
    st.markdown("Generate comprehensive study notes on any topic.")
    
    # Topic input
    topic = st.text_input("📝 Topic:", 
                         placeholder="Enter the topic you want to study...")
    
    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            detail_level = st.select_slider(
                "Detail Level",
                options=["Basic", "Comprehensive", "In-depth"],
                value="Comprehensive"
            )
        with col2:
            include_examples = st.checkbox("Include Examples", value=True)
            include_diagrams = st.checkbox("Include Diagram Descriptions", value=True)
    
    if st.button("📖 Generate Notes", use_container_width=True) and topic:
        with st.spinner("Generating study notes..."):
            # Prepare the prompt with options
            prompt = f"Generate study notes on: {topic}\n\n"
            if detail_level == "Basic":
                prompt += "Provide basic concepts and key points."
            elif detail_level == "In-depth":
                prompt += "Provide detailed explanations with advanced concepts."
            
            if include_examples:
                prompt += " Include practical examples."
            if include_diagrams:
                prompt += " Include descriptions of relevant diagrams or visual aids."
            
            notes = generate_study_notes(prompt, st.session_state['gemini_api_key'])
            
            # Display the notes in a nice format
            st.markdown("### 📖 Generated Notes")
            st.markdown(notes)
            
            # Add download button
            st.download_button(
                label="📥 Download Notes",
                data=notes,
                file_name=f"study_notes_{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )
            
            # Add a feedback section
            st.markdown("---")
            st.markdown("### 💭 Was this helpful?")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👍 Yes"):
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎 No"):
                    st.info("We'll try to improve our notes.")
            with col3:
                if st.button("🔄 Generate New Notes"):
                    st.rerun() 