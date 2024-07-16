import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.switch_backend('Agg')

# Load the dataset
file_path = '/home/alberto/analysis_bundle_stats/volume_dice_score.csv'
data = pd.read_csv(file_path)

# Extract mean and standard deviation of dice scores for each bundle
bundle_stats = data.groupby('bundle_name')['volume_dice_score'].agg(['mean', 'std']).reset_index()

# Save the extracted bundle dice scores to a new CSV file
output_path = '/home/alberto/analysis_bundle_stats/bundle_dice_score.csv'
bundle_stats.to_csv(output_path, index=False)

# Display the table
print(bundle_stats)

# Plot the results in a bar graph with different colors and error bars
colors = plt.cm.tab20(np.linspace(0, 1, len(bundle_stats['bundle_name'])))

plt.figure(figsize=(10, 6))
bars = plt.bar(bundle_stats['bundle_name'], bundle_stats['mean'], yerr=bundle_stats['std'], color=colors, capsize=5)
plt.xlabel('Bundle Name')
plt.ylabel('Mean Dice Score')
plt.title('Mean Dice Score for Each Bundle')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Add legend
plt.legend(bars, bundle_stats['bundle_name'], title='Bundles')

# Save the plot to a file
plot_path = '/home/alberto/analysis_bundle_stats/bundle_dice_scores_plot.png'
plt.savefig(plot_path)
plt.close()

print(f"The plot has been saved to {plot_path}")
