import pandas as pd
import json
myCSV = "/home/alberto/analysis_bundle_stats/tract_info_csv/tract_info_dff.csv"
output_file = "/home/alberto/analysis_bundle_stats/outlier_list.json"

# Load data
data = pd.read_csv(myCSV)

# Grouping data by 'bundle_name' and 'source'
grouped_data = data.groupby(['bundle_name', 'source'])

# Calculate mean and standard deviation for each group
bundle_means = grouped_data[['bundle_Volume']].mean()
bundle_stds = grouped_data[['bundle_Volume']].std()

# Initialize a dictionary to collect outlier subject IDs for each source
outlier_subject_ids = {'replicated_tractograms': {'AF_L':[], 'FAT_L':[], 'IFOF_L':[], 'ILF_L':[], 'PYT_L':[]}, 
                       'original_tractograms': {'AF_L':[], 'FAT_L':[], 'IFOF_L':[], 'ILF_L':[], 'PYT_L':[]}}

# Iterate through each bundle and source to identify outliers
for (bundle_name, source), bundle_group in grouped_data:
    # Calculate thresholds
    bundle_Volume_mean = bundle_means.loc[(bundle_name, source), 'bundle_Volume']
    bundle_Volume_std = bundle_stds.loc[(bundle_name, source), 'bundle_Volume']
    
    bundle_Volume_upper = bundle_Volume_mean + 2 * bundle_Volume_std
    bundle_Volume_lower = bundle_Volume_mean - 2 * bundle_Volume_std
    
    # Identify outliers in bundle_Volume
    bundle_Volume_outliers = bundle_group[
        (bundle_group['bundle_Volume'] > bundle_Volume_upper) |
        (bundle_group['bundle_Volume'] < bundle_Volume_lower)
    ]
    
    # Append outlier subject IDs to the corresponding list in the dictionary
    outlier_subject_ids[source][bundle_name].extend(bundle_Volume_outliers['subject_id'].tolist())

# Output the list of outlier subject IDs for each source
print("Outlier Subject IDs for replicated_tractograms:", outlier_subject_ids['replicated_tractograms'])
print("Outlier Subject IDs for original_tractograms:", outlier_subject_ids['original_tractograms'])

with open(output_file, 'w') as json_file:
    json.dump(outlier_subject_ids, json_file, indent=4)
