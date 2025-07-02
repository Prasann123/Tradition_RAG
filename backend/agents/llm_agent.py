from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


def llm_agent(state):
    """LLM agent for general knowledge chat"""

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    prompt_template = PromptTemplate(
        input_variables=["query", "context"],
        template=(
             "You are a helpful assistant with the following context:\n"
            "{context}\n\n"
            "Answer the user's question:\n{query}"

        )
    )
    context_str = "\n\n".join(state.context + state.web_data)
    prompt = prompt_template.format(context=context_str, query=state.query)
    result = llm.invoke(prompt).content

    # Store the LLM’s response
    state.candidate_answer = result
    if state.context:
        state.answer_source = "RAG Agent (Internal Documents)"
    elif state.web_data:
        state.answer_source = "Web Agent (Live Web Search)"
    else:
        state.answer_source = "LLM Agent (General Knowledge)"
    return state
