import os

from langchain.llms import VLLMOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import LLMChain
from langchain.evaluation import load_evaluator
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)

INFERENCE_SERVER_URL = "_INFERENCE_URL_LLM_"
MAX_NEW_TOKENS = 512
TOP_P = 0.92
TEMPERATURE = 0.01
PRESENCE_PENALTY = 1.03

def infer_with_template(input_text, system_template_string, user_template_string):
    llm = VLLMOpenAI(
        openai_api_key="EMPTY",
        openai_api_base= f"{INFERENCE_SERVER_URL}/v1",
        model_name="/mnt/models/",
        max_tokens=MAX_NEW_TOKENS,
        top_p=TOP_P,
        temperature=TEMPERATURE,
        presence_penalty=PRESENCE_PENALTY,
        streaming=False,
        verbose=False,
    )
    
    system_template = SystemMessagePromptTemplate.from_template(system_template_string)
    user_template = HumanMessagePromptTemplate.from_template(user_template_string)
    print(">>---")
    print("system_template:")
    print(system_template)
    print("user_template:")
    print(user_template)
    print("<<---")

    PROMPT = ChatPromptTemplate.from_messages([system_template, user_template])
    
    llm_chain = LLMChain(llm=llm, prompt=PROMPT)
    
    return llm_chain.run(input_text)
    
def similarity_metric(predicted_text, reference_text):
    embedding_model = HuggingFaceEmbeddings()
    evaluator = load_evaluator("embedding_distance", embeddings=embedding_model)
    distance_score = evaluator.evaluate_strings(prediction=predicted_text, reference=reference_text)
    return 1-distance_score["score"]
