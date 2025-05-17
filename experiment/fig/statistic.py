import openai
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

def score(dictc):
    y = 0
    s = 0
    for k, v in dictc.items():
        if k == 'super fully':
            s += 1.5 * v
            y += v
        elif k == 'fully':
            s += 1 * v
            y += v
        elif k == 'partially':
            s += 0.5 * v
            y += v
        elif k == 'mismatch':
            y += v
    return s/y

priority = {
        'super fully': 3,
        'fully': 2,
        'partially': 1,
        'mismatch': 0
    }

tissue_list = ['Adipose', 'Bone Marrow', 'Fetal Development', 'Heart', 'Kidney', 'Liver', 'Lung', 'Motor Cortex', 'Pancreas', 'PBMC', 'Tonsil']

def pick_higher(val1, val2):
    p1 = priority.get(val1, -1)
    p2 = priority.get(val2, -1)
    return val1 if p1 >= p2 else val2

# Manual scoring Result count
def single_column_count(df, column):
    column_data = df[column].fillna('mismatch')  # 将NA视为'mismatch'
    # column_data = df[column]
    counts = column_data.value_counts()
    target_strings = ['super fully', 'fully', 'partially', 'mismatch']
    filtered_counts = {k: counts.get(k, 0) for k in target_strings}
    return filtered_counts

    # for k, v in filtered_counts.items():
    #     print(f"{k}: {v}")

# Manual scoring result count(process modification)
def double_column_count(df, column_one, column_two):
    result_df = pd.DataFrame()
    result_df['max_agreement'] = df.apply(lambda row: pick_higher(row[column_one], row[column_two]), axis=1)

    target_strings = ['super fully', 'fully', 'partially', 'mismatch']
    counts = result_df['max_agreement'].value_counts()
    filtered_counts = {label: counts.get(label, 0) for label in target_strings}

    return filtered_counts

    # for label, count in result.items():
    #     print(f"{label}: {count}")

# Manual scoring Result count(single tissue)
def single_column_count_tissue(df, column):
    column_data = df.fillna('mismatch')
    grouped = column_data.groupby('Tissue')
    target_strings = ['super fully', 'fully', 'partially', 'mismatch']
    final_count = {}
    for i in tissue_list:
        tissue_group = grouped.get_group(i)
        column_data = tissue_group[column]
        counts = column_data.value_counts()
        filtered_counts = {k: counts.get(k, 0) for k in target_strings}
        final_count[i] = filtered_counts
    return final_count

# Manual scoring Result count(process modification, single tissue)
def double_column_count_tissue(df, column_one, column_two):
    grouped = df.groupby('Tissue')
    target_strings = ['super fully', 'fully', 'partially', 'mismatch']
    final_count = {}
    for i in tissue_list:
        tissue_group = grouped.get_group(i)
        result_df = pd.DataFrame()
        result_df['max_agreement'] = tissue_group.apply(lambda row: pick_higher(row[column_one], row[column_two]), axis=1)
        counts = result_df['max_agreement'].value_counts()
        filtered_counts = {label: counts.get(label, 0) for label in target_strings}
        final_count[i] = filtered_counts
    return final_count

def calculate_cosine_similarity(embeddings1, embeddings2):
    if len(embeddings1) == len(embeddings2):
        cos = cosine_similarity(embeddings1, embeddings2)
        sim_list = []
        for i in range(len(embeddings1)):
            sim_list.append(cos[i][i])
        return sim_list
    else:
        raise Exception("data exception")

def calculate_cosine_similarity_self(embeddings):
    cos = cosine_similarity(embeddings, embeddings)
    sim_list = []
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            sim_list.append(cos[i][j])
    return sim_list

def score_get_embedding(sim1_list):
    scaler = MinMaxScaler()
    # normalization
    data_scaled = scaler.fit_transform(np.array(sim1_list).reshape(-1, 1)).flatten()

    # Map to 1-5
    bins = np.linspace(0, 1, 6)
    categories = np.digitize(data_scaled, bins[1:], right=True) + 1

    sim = 0
    for i in range(len(categories)):
        sim += (categories[i] - 1) * 0.25

    return sim/len(categories)





