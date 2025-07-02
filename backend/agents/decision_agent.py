from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class ValidationResult(BaseModel):
    """pydantic model for structured output"""
    is_valid: bool = Field(description="Indicates if the candidate answer is valid")
    reason: str = Field(default="", description="Feedback on the candidate answer")
def validator_agent(state):

    """ validation of the results thrown in llm, rag or web"""

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    parser = JsonOutputParser(pydantic_object=ValidationResult)

    validation_prompt_template = PromptTemplate(
        input_variables=["query", "candidate_answer", "context", "format_instructions"],
        template=(
            "You are a validation agent. Your task is to evaluate the candidate answer "
            "based on the user's query and the provided context.\n\n"
            "User Query: {query}\n"
            "Candidate Answer: {candidate_answer}\n"
            "Context: {context}\n\n"
            "{format_instructions}"
        )
    )

    full_context = "\n\n".join(state.context + state.web_data)
    prompt = validation_prompt_template.format(
        query = state.query,
        context = full_context,
        candidate_answer = state.candidate_answer,
        format_instructions=parser.get_format_instructions()
    )

    llm_response = llm.invoke(prompt).content
    print("\n--- VALIDATOR AGENT ---")
    print(f"RAW LLM RESPONSE:\n{llm_response}")
    print("-----------------------\n")

    try:
        parsed_result = parser.parse(llm_response)
        state.is_valid = parsed_result['is_valid']
        state.feedback = parsed_result['reason']

        if parsed_result['is_valid']:
            state.final_answer = state.candidate_answer
    except Exception as e:
        print(f"ERROR: Failed to parse validator response. Error: {e}")
        state.is_valid = False
        state.feedback = "The validator's response was malformed and could not be parsed."

    return state 
    