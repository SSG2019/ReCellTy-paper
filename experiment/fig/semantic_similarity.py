import openai
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

openai.api_key = 'your_api_key'

def get_embeddings(tissue, texts, path, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        model=model,
        input=texts
    )

    embeddings = [embedding.embedding for embedding in response.data]  
    embedding_data = {'embedding': embeddings}
    embedding_df = pd.DataFrame(embedding_data)
    embedding_df.insert(0, 'tissue', tissue)
    embedding_df.insert(1, 'Annotation', texts)
    embedding_df.to_csv(path, index=False)

    # return np.array(embeddings)


list_model = ['gpt_4o_mini_FinalCellType', 'gpt_4o_FinalCellType', 'deepseek_chat_FinalCellType', 'claude_3_7_FinalCellType',
              'gpt_4o_mini', 'gpt_4o', 'deepseek_chat', 'claude_3_7', 'Manual Annotation']

output_excel = '../experimental_analysis.xlsx'
df = pd.read_excel(output_excel, sheet_name='agreement', header=1)
tissue_name = list(df['Tissue'])
for i in list_model:
    group = list(df[i])
    path = 'embedding_result' + '/' + i + '.csv'
    get_embeddings(tissue_name, group, path)


model="text-embedding-3-small"
text = list(df['CellMarker2_0'])
path = 'embedding_result' + '/' + 'CellMarker2_0' + '.csv'
results_list = [] 
for item in text:
    embedding = None
    if isinstance(item, str) and item.strip():
        response = openai.embeddings.create(model=model, input=[item])
        embedding = response.data[0].embedding
    results_list.append({'Annotation': item, 'embedding': embedding})

final_df = pd.DataFrame(results_list)
final_df.insert(0, 'tissue', tissue_name)
final_df.to_csv(path, index=False)




