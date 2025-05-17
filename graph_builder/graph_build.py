import os
from langchain_neo4j import Neo4jGraph


os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "your_password"

graph = Neo4jGraph()

delete_query = """
MATCH (n)
DETACH DELETE n
"""

blood_marker_feature_query = """
LOAD CSV WITH HEADERS FROM 'file:///Blood_feature.csv' AS row 

MERGE (bct:BroadCellType {name: row.broad_cell_types})

MERGE (m:Marker {name: row.marker})

MERGE (tc:TissueClass {name: row.tissue_class})

MERGE (tt:TissueType {name: row.tissue_type})

MERGE (s:Species {name: row.species})

MERGE (cn:CellName {name: row.cell_name, cancer_type: row.cancer_type, cell_type: row.cell_type})

MERGE (s)-[:HAS_TISSUE]->(tc)

MERGE (tt)-[:BELONGS_TO_TISSUE_CLASS]->(tc)

MERGE (bct)-[:IS_LOCATED_IN_TISSUE_TYPE]->(tt)

MERGE (m)-[:MARK_BROAD]->(bct)

MERGE (cn)-[:BELONGS_TO_BROAD_CELL_TYPE]->(bct)

WITH row, bct, m, tc, tt, cn

WHERE row.`feature&function` IS NOT NULL AND row.`feature&function` <> ''
MERGE (ff:FeatureFunction {name: row.`feature&function`})

MERGE (cn)-[:HAS_FEATURE_FUNCTION]->(ff)

MERGE (m)-[:MARK]->(ff)

"""
graph.query(delete_query)
graph.query(blood_marker_feature_query)
graph.refresh_schema()