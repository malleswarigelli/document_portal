from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Prompt for document analysis
document_analysis_prompt = ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to analyze and summarize documents.
Return ONLY valid JSON matching the exact schema below.

{format_instructions}

Analyze this document:
{document_text}
""")

# Prompt for document comparison
document_comparison_prompt = ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to compare documents.
                                                              
Return ONLY valid JSON matching the exact schema below.
{format_instructions}       
Compare the following two documents and highlight their differences:
Document 1: 
{document1_text}
Document 2:
{document2_text}
""")

# Central dictionary to register prompts
PROMPT_REGISTRY = {
    "document_analysis": document_analysis_prompt,
    # "document_comparison": document_comparison_prompt,
    # "contextualize_question": contextualize_question_prompt,
    # "context_qa": context_qa_prompt,
}