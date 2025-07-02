from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel

class TopicSelectionParser(BaseModel):
    agent: str  # Should be "A", "B", or "C"

def supervisor(state):
    """ Using llm to decide which node to use next"""
    parser = JsonOutputParser(pydantic_object=TopicSelectionParser)
    llm = ChatOpenAI(model_name="gpt-4o" ,temperature=0)
    routing_prompt = PromptTemplate(
        input_variables=["query","format_instructions"],
        template=(
            "You are an intelligent router for a multi-agent system. "
            "Given the user's question, decide which agent should handle it:\n"
            "A: RAG agent (for any C# interview related questions)\n"
            "B: Web agent (for latest news or real-time info)\n"
            "C: LLM agent (for general knowledge or chit-chat)\n\n"
            "User question: {query}\n"
            "{format_instructions}"
        )
    )
    prompt = routing_prompt.format(
    query=state.query + "\nValidation feedback: " + (state.feedback or ""),
    format_instructions=parser.get_format_instructions()
    )
    llm_response = llm.invoke(prompt).content


    try:
        # The parser returns a dictionary
        parsed = parser.parse(llm_response)
        agent_map = {"A": "rag", "B": "web", "C": "llm"}
        # Use dictionary key access
        state.next_agent = agent_map.get(parsed['agent'].strip().upper(), "llm")
    except Exception as e:
        print(f"ERROR: Supervisor failed to parse routing decision. Defaulting to LLM. Error: {e}")
        state.next_agent = "llm"
        
    return state



    