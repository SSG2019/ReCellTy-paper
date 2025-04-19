import os
import pandas as pd
from langchain_openai import ChatOpenAI
from io import StringIO
from langchain_community.document_loaders.csv_loader import CSVLoader
from Agent.feature_marker_extraction import feature_marker_extraction
from Agent.name_joint import search_model

your_api_key = "your_api_key"

# Segment csv from generated content
def segment(text: str):
    _, after = text.split("```csv")
    text = after.split("```")[0]
    return text

def read_and_deduplicate_csv(file_path, namecell, column):
    df = pd.read_csv(file_path)
    combined_data = pd.concat([df[column[0]], df[column[1]]], axis=0).drop_duplicates().tolist()
    name = pd.concat([df[namecell]]).drop_duplicates().tolist()
    combined_data = " ".join(map(str, filter(lambda x: x == x, combined_data)))
    name = " ".join(name)
    return name, combined_data

def joint_data(new_data, original_data):
    num_rows = len(new_data)
    add_data = {
        'species': [original_data['species'].iloc[0]] * num_rows,
        'tissue_class': [original_data['tissue_class'].iloc[0]] * num_rows,
        'tissue_type': [original_data['tissue_type'].iloc[0]] * num_rows,
        'cancer_type': [original_data['cancer_type'].iloc[0]] * num_rows,
        'cell_type': [original_data['cell_type'].iloc[0]] * num_rows,
        'cell_name': [original_data['cell_name'].iloc[0]] * num_rows
    }
    add_data_df = pd.DataFrame(add_data)
    combined_df = pd.concat([new_data, add_data_df], axis=1)
    return combined_df

def save_csv(folder, llm_content, original_file_path, original_csv_path):
    csv_data = StringIO(segment(llm_content))
    df_new = pd.read_csv(csv_data)

    df_original = pd.read_csv(original_file_path)
    final_data = joint_data(df_new, df_original)

    new_file_name = os.path.splitext(original_csv_path)[0] + '.csv'

    new_file_path = folder + '/' + new_file_name

    final_data.to_csv(new_file_path, index=False)

def txt_process(path):
    if not os.path.exists(path):
        with open(path, "w") as filell:
            filell.write("-1")
        x_index = -1
    elif os.path.exists(path):
        with open(path, "r+") as filell:
            x_index = int(filell.read().strip())
    return x_index

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

model = search_model(1, your_api_key)

input_folder = "../data/data_cellmarker2_cellname"
output_folder = "../data/data_feature_marker"

tissue_files = [f for f in os.listdir(input_folder)]
x_tissue = len(tissue_files)

last_processed_index_tissue = txt_process(output_folder + "/" + "processed_index_tissue.txt")


for i in range(last_processed_index_tissue + 1, len(tissue_files)):
    if tissue_files[i] != 'Blood':
        os.makedirs(output_folder + "/" + tissue_files[i], exist_ok=True)

        for ii in range(2):
            last_processed_index_huamn_seq = txt_process(output_folder + "/" + tissue_files[i] + "/" + "processed_index_huamn_seq.txt")
            if last_processed_index_huamn_seq == -1:
                input_folder_cellname = input_folder + "/" + tissue_files[i] + "/" + "human"
                output_folder_cellname = output_folder + "/" + tissue_files[i] + "/" + "human"
                os.makedirs(output_folder_cellname, exist_ok=True)

                csv_files = [f for f in os.listdir(input_folder_cellname) if f.endswith('.csv')]
                x_cellname = len(csv_files)

                last_processed_index_cellname = txt_process(output_folder_cellname + "/" + "processed_index_cellname.txt")
                # with open(output_folder_cellname + "/" + "processed_index_cellname.txt", "a+") as file:
                #     try:
                #         last_processed_index_cellname = int(file.read().strip())
                #     except:
                #         last_processed_index_cellname = -1

                for j in range(last_processed_index_cellname + 1, len(csv_files)):
                    csv_file = csv_files[j]
                    file_path = input_folder_cellname + '/' + csv_file

                    cell_name, marker = read_and_deduplicate_csv(file_path, 'cell_name', ['marker', 'Symbol'])
                    cvs_feature = feature_marker_extraction(model, cell_name, marker)
                    # print(cvs_feature)

                    save_csv(output_folder_cellname, cvs_feature, file_path, csv_file)

                    print("*************************")
                    print(f"{i + 1}/{x_tissue} tissue is doing")
                    print(f"{last_processed_index_huamn_seq + 2}/{2} human(1) or seq(2) is doing")
                    print(f"{j + 1}/{x_cellname} cell has done")
                    print("*************************")

                    with open(output_folder_cellname + "/" + "processed_index_cellname.txt", "w") as file:
                        file.write(str(j))
                with open(output_folder + "/" + tissue_files[i] + "/" + "processed_index_huamn_seq.txt", "w") as file:
                    file.write(str(0))
            elif last_processed_index_huamn_seq == 0:
                input_folder_cellname = input_folder + "/" + tissue_files[i] + "/" + "seq"
                output_folder_cellname = output_folder + "/" + tissue_files[i] + "/" + "seq"
                os.makedirs(output_folder_cellname, exist_ok=True)

                csv_files = [f for f in os.listdir(input_folder_cellname) if f.endswith('.csv')]
                x_cellname = len(csv_files)

                last_processed_index_cellname = txt_process(output_folder_cellname + "/" + "processed_index_cellname.txt")

                for j in range(last_processed_index_cellname + 1, len(csv_files)):
                    csv_file = csv_files[j]
                    file_path = input_folder_cellname + '/' + csv_file

                    cell_name, marker = read_and_deduplicate_csv(file_path, 'cell_name', ['marker', 'Symbol'])
                    cvs_feature = feature_marker_extraction(model, cell_name, marker)
                    # print(cvs_feature)

                    save_csv(output_folder_cellname, cvs_feature, file_path, csv_file)

                    print("*************************")
                    print(f"{i + 1}/{x_tissue} tissue is doing")
                    print(f"{last_processed_index_huamn_seq + 2}/{2} human(1) or seq(2) is doing")
                    print(f"{j + 1}/{x_cellname} cell has done")
                    print("*************************")
                    # break

                    with open(output_folder_cellname + "/" + "processed_index_cellname.txt", "w") as file:
                        file.write(str(j))
                break

        with open(output_folder + "/" + "processed_index_tissue.txt", "w") as file:
            file.write(str(i))

    elif tissue_files[i] == 'Blood':
        with open(output_folder + "/" + "processed_index_tissue.txt", "w") as file:
            file.write(str(i))





