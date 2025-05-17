import pandas as pd
import os

def split_tissue():
    file1 = "../data/data_cellmarker2/Cell_marker_Human.xlsx"
    file2 = "../data/data_cellmarker2/Cell_marker_Seq.xlsx"

    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    df_human = df1[df1['species'] == 'Human']
    df_seq = df2[df2['species'] == 'Human']

    tissue_classes_1 = df_human['tissue_class'].dropna().unique()
    tissue_classes_2 = df_seq['tissue_class'].dropna().unique()
    all_tissue_classes = set(tissue_classes_1) | set(tissue_classes_2)

    columns_to_keep = ['species', 'tissue_class', 'tissue_type', 'uberonongology_id',
                       'cancer_type', 'cell_type', 'cell_name', 'cellontology_id', 'marker', 'Symbol']

    for tissue in all_tissue_classes:
        if not os.path.exists('../data/data_cellmarker2_tissue/' + tissue):
            os.makedirs('../data/data_cellmarker2_tissue/' + tissue)

        df_subset_human = df_human[df_human['tissue_class'] == tissue]
        df2_subset_seq = df_seq[df_seq['tissue_class'] == tissue]

        df_subset_human = df_subset_human[columns_to_keep]
        df2_subset_seq = df2_subset_seq[columns_to_keep]

        output_path1 = '../data/data_cellmarker2_tissue/' + f"{tissue}/" + f"{tissue}_human.xlsx"
        output_path2 = '../data/data_cellmarker2_tissue/' + f"{tissue}/" + f"{tissue}_seq.xlsx"

        df_subset_human.to_excel(output_path1, index=False)
        df2_subset_seq.to_excel(output_path2, index=False)


def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def split_excel_by_multiple_headers(excel_file, save_path, header):
    df = pd.read_excel(excel_file)
    grouped = df.groupby(header)

    for (cell_name, type_val, group_val, type_tissue), group_df in grouped:
        cell_name = str(cell_name).replace("/", "_")
        type_val = str(type_val).replace("/", "_")
        group_val = str(group_val).replace("/", "_")
        type_tissue = str(type_tissue).replace("/", "_")
        filename = f"{save_path}{cell_name}_{type_val}_{group_val}_{type_tissue}.csv"
        group_df.to_csv(filename, index=False)


def get_cellname_csv():
    base_path = "../data/data_cellmarker2_tissue/"
    save_base_file = "../data/data_cellmarker2_cellname/"
    tissue_folders = os.listdir(base_path)

    header = ['cell_name', 'cell_type', 'cancer_type', 'tissue_type']  # 根据需要修改 header

    for tissue in tissue_folders:
        tissue_path = base_path + f"{tissue}/"

        if os.path.isdir(tissue_path):
            os.makedirs(save_base_file + f"{tissue}/", exist_ok=True)

            human_file = tissue_path + f"{tissue}_human.xlsx"
            seq_file = tissue_path + f"{tissue}_seq.xlsx"

            human_save_path = save_base_file + f"{tissue}/" + "human/"
            seq_save_path = save_base_file + f"{tissue}/" +  "seq/"

            os.makedirs(human_save_path, exist_ok=True)
            os.makedirs(seq_save_path, exist_ok=True)

            if os.path.exists(human_file):
                split_excel_by_multiple_headers(human_file, human_save_path, header)

            if os.path.exists(seq_file):
                split_excel_by_multiple_headers(seq_file, seq_save_path, header)


split_tissue()
get_cellname_csv()