import os
import pandas as pd
from langchain_openai import ChatOpenAI
from io import StringIO
from langchain_community.document_loaders.csv_loader import CSVLoader
from Agent.feature_marker_extraction import feature_marker_extraction
from feature_marker import read_and_deduplicate_csv, save_csv
from Agent.name_joint import search_model

your_api_key = "your_api_key"

# path_input = '../data/data_cellmarker2_cellname/Airway/human/Activated tissue resident memory CD4+ T cell_Normal cell_Normal_Airway.csv'
# path_output = '../data/data_feature_marker/Airway/human'
# csv_file = 'Activated tissue resident memory CD4+ T cell_Normal cell_Normal_Airway.csv'

# path_input = '../data/data_cellmarker2_cellname/Bladder/seq/Inflammatory cancer‐associated fibroblast (iCAF)_Cancer cell_Bladder Cancer_Bladder.csv'
# path_output = '../data/data_feature_marker/Bladder/seq'
# csv_file = 'Inflammatory cancer‐associated fibroblast (iCAF)_Cancer cell_Bladder Cancer_Bladder.csv'

# path_input = '../data/data_cellmarker2_cellname/Brain/seq/Dividing cell_Normal cell_Normal_Neocortex.csv'
# path_output = '../data/data_feature_marker/Brain/seq'
# csv_file = 'Dividing cell_Normal cell_Normal_Neocortex.csv'

# path_input = '../data/data_cellmarker2_cellname/Esophagus/human/FGFR1HighNME5- epithelial cell_Normal cell_Normal_Esophagus.csv'
# path_output = '../data/data_feature_marker/Esophagus/human'
# csv_file = 'FGFR1HighNME5- epithelial cell_Normal cell_Normal_Esophagus.csv'

# path_input = '../data/data_cellmarker2_cellname/Genitals/human/CD14+ monocyte-derived macrophage_Normal cell_Normal_Anogenital tract.csv'
# path_output = '../data/data_feature_marker/Genitals/human'
# csv_file = 'CD14+ monocyte-derived macrophage_Normal cell_Normal_Anogenital tract.csv'

# path_input = '../data/data_cellmarker2_cellname/Intestine/human/IgA+ Regulatory B cell_Cancer cell_Colorectal Cancer_Intestine.csv'
# path_output = '../data/data_feature_marker/Intestine/human'
# csv_file = 'IgA+ Regulatory B cell_Cancer cell_Colorectal Cancer_Intestine.csv'

# path_input = '../data/data_cellmarker2_cellname/Kidney/human/Adult podocyte_Normal cell_Normal_Kidney.csv'
# path_output = '../data/data_feature_marker/Kidney/human'
# csv_file = 'Adult podocyte_Normal cell_Normal_Kidney.csv'

# path_input = '../data/data_cellmarker2_cellname/Liver/seq/Exhausted double-positive T cell_Cancer cell_Hepatocellular Carcinoma_Liver.csv'
# path_output = '../data/data_feature_marker/Liver/seq'
# csv_file = 'Exhausted double-positive T cell_Cancer cell_Hepatocellular Carcinoma_Liver.csv'

# path_input = '../data/data_cellmarker2_cellname/Lung/human/Naive T(Th0) cell_Normal cell_Normal_Lung.csv'
# path_output = '../data/data_feature_marker/Lung/human'
# csv_file = 'Naive T(Th0) cell_Normal cell_Normal_Lung.csv'

# path_input = '../data/data_cellmarker2_cellname/Prostate/human/GrB+ Regulatory B cell_Cancer cell_Prostate Cancer_Prostate.csv'
# path_output = '../data/data_feature_marker/Prostate/human'
# csv_file = 'GrB+ Regulatory B cell_Cancer cell_Prostate Cancer_Prostate.csv'

# path_input = '../data/data_cellmarker2_cellname/Testis/seq/CD4+ T cell_Cancer cell_Testicular Germ Cell Tumor_Testis.csv'
# path_output = '../data/data_feature_marker/Testis/seq'
# csv_file = 'CD4+ T cell_Cancer cell_Testicular Germ Cell Tumor_Testis.csv'

# path_input = '../data/data_cellmarker2_cellname/Thymus/seq/Immature medullary thymic epithelial cell_Normal cell_Normal_Thymus.csv'
# path_output = '../data/data_feature_marker/Thymus/seq'
# csv_file = 'Immature medullary thymic epithelial cell_Normal cell_Normal_Thymus.csv'

# path_input = '../data/data_cellmarker2_cellname/Undefined/human/Naive T(Th0) cell_Cancer cell_B-cell malignancies_Undefined.csv'
# path_output = '../data/data_feature_marker/Undefined/human'
# csv_file = 'Naive T(Th0) cell_Cancer cell_B-cell malignancies_Undefined.csv'

# path_input = '../data/data_cellmarker2_cellname/Undefined/human/T memory stem cell_Normal cell_Normal_Undefined.csv'
# path_output = '../data/data_feature_marker/Undefined/human'
# csv_file = 'T memory stem cell_Normal cell_Normal_Undefined.csv'

path_input = '../data/data_cellmarker2_cellname/Nose/human/Dividing cell_Normal cell_Normal_Nose.csv'
path_output = '../data/data_feature_marker/Nose/human'
csv_file = 'Dividing cell_Normal cell_Normal_Nose.csv'

# path_input = '../data/data_cellmarker2_cellname/Skin/human/Cycling cell_Normal cell_Normal_Skin.csv'
# path_output = '../data/data_feature_marker/Skin/human'
# csv_file = 'Cycling cell_Normal cell_Normal_Skin.csv'

model = search_model(1, your_api_key)
cell_name, marker = read_and_deduplicate_csv(path_input, 'cell_name', ['marker', 'Symbol'])
cvs_feature = feature_marker_extraction(model, cell_name, marker)
save_csv(path_output, cvs_feature, path_input, csv_file)
