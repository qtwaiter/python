import pandas as pd
import difflib
import re

# Load data from Excel file
file_path = '居家20240820.xlsx'
sheets = pd.read_excel(file_path, sheet_name=None)

# Extract relevant sheets
home_df = sheets['居家']
area_info_df = sheets['区域信息']

# Preprocess addresses by removing digits and special characters
def preprocess_address(addr):
    addr = str(addr)  # Ensure the address is treated as a string
    return re.sub(r'\d+', '', addr).translate(str.maketrans('', '', '号幢单元室楼栋'))

home_df['签约地址简化'] = home_df['签约地址'].fillna('').astype(str).apply(preprocess_address)

# Create mappings from area to community and street, ensure all entries are strings
area_to_community = dict(zip(area_info_df['小区（自然村）'].astype(str), area_info_df['社区（行政村）'].astype(str)))
community_to_street = dict(zip(area_info_df['社区（行政村）'].astype(str), area_info_df['街道（乡镇）'].astype(str)))

# Function to find the best matching area and return corresponding community and street
def find_best_area_match(address, area_dict, community_dict):
    best_match = None
    best_score = 0
    for area, community in area_dict.items():
        area = str(area)  # Ensure comparisons are made with strings
        score = difflib.SequenceMatcher(None, address, area).ratio()
        if score > best_score:
            best_match = (community_dict.get(community), community)
            best_score = score
    return best_match if best_score > 0.5 else (None, None)

# Function to find the best matching community and return corresponding street
def find_best_community_match(address, community_dict):
    best_match = None
    best_score = 0
    for community, street in community_dict.items():
        community = str(community)  # Ensure comparisons are made with strings
        score = difflib.SequenceMatcher(None, address, community).ratio()
        if score > best_score:
            best_match = (street, community)
            best_score = score
    return best_match if best_score > 0.5 else (None, None)

# Apply the matching functions to each row in the home_df
def apply_matching(row):
    community, street = find_best_area_match(row['签约地址简化'], area_to_community, community_to_street)
    if community and street:
        return pd.Series([street, community], index=['街道（乡镇）', '社区（行政村）'])
    else:
        street, community = find_best_community_match(row['签约地址简化'], community_to_street)
        return pd.Series([street, community], index=['街道（乡镇）', '社区（行政村）'])

# Add results to DataFrame
home_df[['街道（乡镇）', '社区（行政村）']] = home_df.apply(apply_matching, axis=1)

# Export the results to a new Excel file
output_path = 'outputfile4.xlsx'
home_df.to_excel(output_path, index=False)
