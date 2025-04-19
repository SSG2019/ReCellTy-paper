from langchain_neo4j import GraphCypherQAChain
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Examples: Here are a few examples of generated Cypher statements for particular questions:
Note: only change the marker and 'tissue_class' according to the question, do not change the rest of the Cypher code.
MATCH (m:Marker)-[:MARK_BROAD]->(bct:BroadCellType)-[:IS_LOCATED_IN_TISSUE_TYPE]->(t: TissueType)-[:BELONGS_TO_TISSUE_CLASS]->(tc: TissueClass)
WHERE m.name IN ['Marker1', 'Marker2', 'Marker3'...]
  AND tc.name = 'tissue_class'
RETURN m.name AS Marker, COLLECT(DISTINCT bct.name) AS BroadCellType


The question is:
{question}
"""
CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)


CYPHER_GENERATION_TEMPLATE_GLOBAL = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Examples: Here are a few examples of generated Cypher statements for particular questions:
Note: only change the marker according to the question, do not change the rest of the Cypher code.
MATCH (m:Marker)-[:MARK_BROAD]->(bct:BroadCellType)
WHERE m.name IN ['Marker1', 'Marker2', 'Marker3'...]
RETURN m.name AS Marker, COLLECT(DISTINCT bct.name) AS BroadCellType


The question is:
{question}
"""

CYPHER_GENERATION_PROMPT_GLOBAL = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE_GLOBAL
)


broad_system_prompt = """
You are an expert in the field of biological cell marker functions. Your task is to perform a step in cell type annotation: identify broad cell types based on relevant information and tissue types.
"""

broad_task_prompt = """
The information provides possible major cell types: {broad_cell_type_info}
The tissue is {Tissue}
Give me your final judgment(The only one broad type of cell). 
Return only the cell type as the output.
"""


def broad_type_agent(model, graph, marker, tissue, global_search=False):
    if global_search:
        chain = GraphCypherQAChain.from_llm(model,
                                            graph=graph,
                                            verbose=True,
                                            top_k=1000,
                                            cypher_prompt=CYPHER_GENERATION_PROMPT_GLOBAL,
                                            allow_dangerous_requests=True)

        prompt_marker2cell = f"""
        I need to perform cell type annotation based on given markers. Your task is to summarize the broad cell types corresponding to the relevant genes.
        Markers: {marker}
        Summary template is as follows: 
        marker1: BroadCellType1, BroadCellType2, BroadCellType3....
        marker2: BroadCellType1, BroadCellType2, BroadCellType3....
        .....
        """
    else:
        chain = GraphCypherQAChain.from_llm(model,
                                            graph=graph,
                                            verbose=True,
                                            top_k=1000,
                                            cypher_prompt=CYPHER_GENERATION_PROMPT,
                                            allow_dangerous_requests=True)

        prompt_marker2cell = f"""
        I need to perform cell type annotation based on given markers. Your task is to summarize the broad cell types corresponding to the relevant genes.
        Markers: {marker}
        TissueClass: {tissue}
        Summary template is as follows: 
        marker1: BroadCellType1, BroadCellType2, BroadCellType3....
        marker2: BroadCellType1, BroadCellType2, BroadCellType3....
        .....
        """
    response = chain.invoke({"query": prompt_marker2cell})
    print(response['result'])
    return response['result']

def bct_judgement(model, broad_cell_type_info, tissue):
    prompt_template = ChatPromptTemplate([
        ("system", broad_system_prompt),
        ("user", broad_task_prompt)
    ])
    chain = prompt_template | model | StrOutputParser()
    return chain.invoke({'broad_cell_type_info': broad_cell_type_info,
                         'Tissue': tissue})

