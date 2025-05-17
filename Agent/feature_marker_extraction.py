from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


prompt_system = """
You are a professional bioinformatics analyst specializing in handling CSV files, especially in the field of cells and genes.
your task is to analyze the task and output the required cvs file based on the given content.
"""
prompt_task = """
Your response should be as follows:
Firstly, separate the features and functions in the cell name.
Secondly, Analyze the relationship between each gene and feature&function, and save the genes that can reflect the feature function into cvs file species.
If the input cell itself belongs to a major cell type without any feature or function, all genes will be output for each row, and the feature & function fields will be left blank.
The output csv file header includes: broad_cell_types, feature&function, marker
note: The markers in each line of the generated csv file should determine the feature&function.
cell name: {cell_name},
marker: {marker}(Please analyze every marker, some genes may be associated with traits, while others are not).

Here is an example:
input:
cell name: Effector CD4+ T cell
marker: markerA, markerB, markerC, markerD, markerE,
output:
markerA is associated with CD4+ ,markerE is associated with Effector.
'''csv
broad_cell_types,feature&function,marker
T cell,CD4+,markerC
T cell,CD4+,markerA 
T cell,Effector,markerE
T cell,Effector,markerB 
T cell,Effector,markerD 
'''
"""

def feature_marker_extraction(model, cell_name, marker):
    prompt_template = ChatPromptTemplate([
        ("system", prompt_system),
        ("user", prompt_task)
    ])
    chain = prompt_template | model | StrOutputParser()
    return chain.invoke({'cell_name': cell_name,'marker': marker})



