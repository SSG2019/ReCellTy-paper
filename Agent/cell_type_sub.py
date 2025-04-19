from http.client import responses

from langchain_neo4j import GraphCypherQAChain
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def segment_output(text: str):
    try:
        _, after = text.rsplit("```answer\n", 1)
        return after.split("```")[0]
    except:
        _, after = text.split("'''", )
        return after.split("'''")[0]


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
MATCH (m:Marker)-[:MARK]->(ff:FeatureFunction)<-[:HAS_FEATURE_FUNCTION]-(cn:CellName)-[:BELONGS_TO_BROAD_CELL_TYPE]->(bct:BroadCellType)-[:IS_LOCATED_IN_TISSUE_TYPE]->(t: TissueType)-[:BELONGS_TO_TISSUE_CLASS]->(tc: TissueClass)
WHERE m.name IN ['Marker1', 'Marker2', 'Marker3'...]
  AND tc.name = 'Tissue_class'
RETURN m.name AS Marker, COLLECT(DISTINCT ff.name) AS FeatureFunctions


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
MATCH (m:Marker)-[:MARK]->(ff:FeatureFunction)
WHERE m.name IN ['Marker1', 'Marker2', 'Marker3'...]
RETURN m.name AS Marker, COLLECT(DISTINCT ff.name) AS FeatureFunctions


The question is:
{question}
"""

CYPHER_GENERATION_PROMPT_GLOBAL = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE_GLOBAL
)



subtype_system_prompt = """
You are an expert in the field of biological cell marker functions. Your task is to perform a step in cell type annotation. 
Based on the determined broad cell type and the feature functions corresponding to the markers, select at most three features/functions that you believe are most likely to be expressed.
Please first analyze according to the requirements. 
"""

subtype_task_prompt = """
The broad cell type is known: {broad_type}.
the corresponding feature functions for each marker are as follows: {marker_feature}
Select the relevant features according to the following three steps:
First, analyze the correlation between other feature functions and markers, and make the selection.
Second, check if there are feature function names that highly overlap with the marker name. If so, the feature/function must be included in your answer.
for example, if a marker gene is named 'ABC' and its corresponding features include 'ABC+', then 'ABC+' is a mandatory option.
Finally, check the number of features corresponding to each marker. If a marker corresponds to only one or two feature functions. If so, the feature/function must be included in your answer.
In ang cases, your answer should include a answer string, e.g.:
```answer
feature_one, feature_two, feature_three
```
Do not include markers in the answer string
"""


def sub_type_agent(model, graph, marker, tissue, global_search=False):
    if global_search:
        chain = GraphCypherQAChain.from_llm(model,
                                            graph=graph,
                                            verbose=True,
                                            top_k=1000,
                                            cypher_prompt=CYPHER_GENERATION_PROMPT_GLOBAL,
                                            allow_dangerous_requests=True)

        prompt_marker2feature = f"""
        Query and summarize the feature functions of the following markers. 
        Markers: {marker}
        Summary template is as follows: 
        marker1: feature1, feature2, feature3....
        marker2: feature1, feature2, feature3....
        .....
        """
    else:
        chain = GraphCypherQAChain.from_llm(model,
                                            graph=graph,
                                            verbose=True,
                                            top_k=1000,
                                            cypher_prompt=CYPHER_GENERATION_PROMPT,
                                            allow_dangerous_requests=True)

        prompt_marker2feature = f"""
        Query and summarize the feature functions of the following markers. 
        Markers: {marker}
        TissueClass: {tissue}
        Summary template is as follows: 
        marker1: feature1, feature2, feature3....
        marker2: feature1, feature2, feature3....
        .....
        """
    response = chain.invoke({"query": prompt_marker2feature})
    print(response['result'])
    return response['result']

def feature_select(model, broad_type, marker_feature):
    prompt_template = ChatPromptTemplate([
        ("system", subtype_system_prompt),
        ("user", subtype_task_prompt)
    ])
    chain = prompt_template | model | StrOutputParser()
    response = chain.invoke({'broad_type': broad_type,
                         'marker_feature': marker_feature})
    return response