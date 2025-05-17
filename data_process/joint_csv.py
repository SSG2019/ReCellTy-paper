import os
import pandas as pd

# folder_path1 = '../data/cell_data_feature_human'
# folder_path2 = '../data/cell_data_feature_seq'
# output_file = '../data/blood_feature.csv'
#
# xlsx_file = '../data/blood_feature.xlsx'
#
# neo4j_home = os.environ.get("NEO4J_HOME")
# output_neo4j_file = os.path.join(neo4j_home, "import", "feature_marker.csv")
#
# csv_files1 = [f for f in os.listdir(folder_path1) if f.endswith('.csv')]
# csv_files2 = [f for f in os.listdir(folder_path2) if f.endswith('.csv')]
#
# dfs = []
#
# for file in csv_files1:
#     file_path = os.path.join(folder_path1, file)
#     df = pd.read_csv(file_path)
#     dfs.append(df)
#
# for file in csv_files2:
#     file_path = os.path.join(folder_path2, file)
#     df = pd.read_csv(file_path)
#     dfs.append(df)
#
# merged_df = pd.concat(dfs, ignore_index=True)
#
# merged_df.to_csv(output_file, index=False)
# merged_df.to_csv(output_neo4j_file, index=False)
# merged_df.to_excel(xlsx_file, index=False, engine='openpyxl')

############################################################################################################################

path_file = "../data/data_feature_marker"
neo4j_home = os.environ.get("NEO4J_HOME")
output_neo4j_file = os.path.join(neo4j_home, "import", "feature_marker.csv")
df_feature = []
for item in os.listdir(path_file):
    item_path = os.path.join(path_file, item)
    if os.path.isdir(item_path):
        folder_path1 = item_path + "/" + "human"
        folder_path2 = item_path + "/" + "seq"
        output_file = item_path + f"/{item}_feature.csv"
        xlsx_file = item_path + f"/{item}_feature.xlsx"

        csv_files1 = [f for f in os.listdir(folder_path1) if f.endswith('.csv')]
        csv_files2 = [f for f in os.listdir(folder_path2) if f.endswith('.csv')]
        dfs = []

        for file in csv_files1:
            file_path = os.path.join(folder_path1, file)
            df = pd.read_csv(file_path)
            dfs.append(df)
        for file in csv_files2:
            file_path = os.path.join(folder_path2, file)
            df = pd.read_csv(file_path)
            dfs.append(df)

        merged_df = pd.concat(dfs, ignore_index=True)

        df_feature.append(merged_df)

        merged_df.to_csv(output_file, index=False)
        merged_df.to_excel(xlsx_file, index=False, engine='openpyxl')

df_feature = pd.concat(df_feature, ignore_index=True)
df_feature.to_csv(path_file + "/" + "feature_marker.csv", index=False)
df_feature.to_excel(path_file + "/" + "feature_marker.xlsx", index=False, engine='openpyxl')
df_feature.to_csv(output_neo4j_file, index=False)


