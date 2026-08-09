from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text:\n\n{dom_content}\n\n"
    "Instructions:\n"
    "1. Extract only the information that matches: {parse_description}.\n"
    "2. Do not include any extra text or explanation.\n"
    "3. If nothing matches, return ''.\n"
    "4. Always output as a Markdown table with headers and rows."
)

model = OllamaLLM(model="llama3.1")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_result = []
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({
            "dom_content": chunk,
            "parse_description": parse_description
        })
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_result.append(response)

    return "\n".join(parsed_result)
