import pandas as pd
import plotly.graph_objects as go

# Load data
stats = pd.read_csv('/home/alberto/analysis_bundle_stats/tract_info_csv/tract_info_dff.csv')

# Group data by bundle name

source_grouping = stats.groupby('source')
replicated = source_grouping.get_group('replicated_tractograms')
original = source_grouping.get_group('original_tractograms')
grouped_data2 = original.groupby('bundle_name')
grouped_data1 = replicated.groupby('bundle_name')
# Get specific bundle volumes and subject ids
volume_AF_L1 = grouped_data1.get_group('AF_L')[['bundle_Volume', 'subject_id','source']]
volume_FAT_L1 = grouped_data1.get_group('FAT_L')[['bundle_Volume', 'subject_id','source']]
volume_IFOF_L1 = grouped_data1.get_group('IFOF_L')[['bundle_Volume', 'subject_id','source']]
volume_ILF_L1 = grouped_data1.get_group('ILF_L')[['bundle_Volume', 'subject_id','source']]
volume_PYT_L1 = grouped_data1.get_group('PYT_L')[['bundle_Volume', 'subject_id','source']]

volume_AF_L2 = grouped_data2.get_group('AF_L')[['bundle_Volume', 'subject_id','source']]
volume_FAT_L2 = grouped_data2.get_group('FAT_L')[['bundle_Volume', 'subject_id','source']]
volume_IFOF_L2 = grouped_data2.get_group('IFOF_L')[['bundle_Volume', 'subject_id','source']]
volume_ILF_L2 = grouped_data2.get_group('ILF_L')[['bundle_Volume', 'subject_id','source']]
volume_PYT_L2 = grouped_data2.get_group('PYT_L')[['bundle_Volume', 'subject_id','source']]
# Data for plotting
x_data = ['AF_L', 'FAT_L', 'IFOF_L', 'ILF_L', 'PYT_L']
y_data = [volume_AF_L1, volume_FAT_L1, volume_IFOF_L1, volume_ILF_L1, volume_PYT_L1]
colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)']

fig = go.Figure()
for xd, yd, cls in zip(x_data, y_data, colors):
        fig.add_trace(go.Box(
                y=yd['bundle_Volume'],
                name=xd,
                boxpoints='all',
                jitter=0.3,  # Adjust jitter to reduce overlap
                whiskerwidth=0.2,
                fillcolor=cls,
                marker_size=5,  # Increase marker size for better visibility
                line_width=1,
                text=yd['subject_id'] + ' ' + yd['source'],  # Add subject_id for hover data
                hoverinfo='y+text'  # Display y value and text on hover
            ))

# Update layout with explicit y-axis range
fig.update_layout(
    title='Volume of Bundles (Replicated)',
    yaxis=dict(
        range=[0, 45000],  # Set the y-axis range
        autorange=False,
        showgrid=True,
        zeroline=True,
        tickmode='linear',  # Ensure linear tick mode
        dtick=20000,  # Set a suitable tick interval
        gridcolor='rgb(255, 255, 255)',
        gridwidth=1,
        zerolinecolor='rgb(255, 255, 255)',
        zerolinewidth=2,
    ),
    xaxis=dict(
        title='Bundles'
    ),
    margin=dict(
        l=40,
        r=30,
        b=80,
        t=100,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    showlegend=False
)

# Save the plot as HTML
fig.write_html('/home/alberto/analysis_bundle_stats/plot/interactive_plot_replicated.html')

# Save the plot as PNG

# Show the plot
fig.show()
x_data = ['AF_L', 'FAT_L', 'IFOF_L', 'ILF_L', 'PYT_L']
y_data = [volume_AF_L2, volume_FAT_L2, volume_IFOF_L2, volume_ILF_L2, volume_PYT_L2]
colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)']

fig = go.Figure()
for xd, yd, cls in zip(x_data, y_data, colors):
        fig.add_trace(go.Box(
                y=yd['bundle_Volume'],
                name=xd,
                boxpoints='all',
                jitter=0.3,  # Adjust jitter to reduce overlap
                whiskerwidth=0.2,
                fillcolor=cls,
                marker_size=5,  # Increase marker size for better visibility
                line_width=1,
                text=yd['subject_id'] + ' ' + yd['source'],  # Add subject_id for hover data
                hoverinfo='y+text'  # Display y value and text on hover
            ))

# Update layout with explicit y-axis range
fig.update_layout(
    title='Volume of Bundles (Original)',
    yaxis=dict(
        range=[0, 45000],  # Set the y-axis range
        autorange=False,
        showgrid=True,
        zeroline=True,
        tickmode='linear',  # Ensure linear tick mode
        dtick=20000,  # Set a suitable tick interval
        gridcolor='rgb(255, 255, 255)',
        gridwidth=1,
        zerolinecolor='rgb(255, 255, 255)',
        zerolinewidth=2,
    ),
    xaxis=dict(
        title='Bundles'
    ),
    margin=dict(
        l=40,
        r=30,
        b=80,
        t=100,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    showlegend=False
)

# Save the plot as HTML
fig.write_html('/home/alberto/analysis_bundle_stats/plot/interactive_plot_original.html')

# Save the plot as PNG

# Show the plot
fig.show()