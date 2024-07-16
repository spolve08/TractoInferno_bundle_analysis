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
bundles = ['AF_L', 'FAT_L', 'IFOF_L', 'ILF_L', 'PYT_L']
replicated_data = {bundle: grouped_data1.get_group(bundle)[['bundle_Volume', 'subject_id', 'source']] for bundle in bundles}
original_data = {bundle: grouped_data2.get_group(bundle)[['bundle_Volume', 'subject_id', 'source']] for bundle in bundles}

# Data for plotting
x_data = [f'{bundle}_r' for bundle in bundles] + [f'{bundle}_o' for bundle in bundles]
y_data = [replicated_data[bundle] for bundle in bundles] + [original_data[bundle] for bundle in bundles]
colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)', 'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)'] * 2

fig = go.Figure()

# Add box plots
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
        hoverinfo='y+text'
    ))

# Add scatter plot for means and standard deviations
for xd, yd in zip(x_data, y_data):
    mean = yd['bundle_Volume'].mean()
    std_dev = yd['bundle_Volume'].std()
    
    fig.add_trace(go.Scatter(
        x=[xd],
        y=[mean],
        mode='markers',
        marker=dict(color='black', size=10),
        error_y=dict(
            type='data',
            array=[2 * std_dev],
            visible=True
        ),
        showlegend=False,
        hoverinfo='y+text',
        text=f'Mean: {mean:.2f}<br>Std Dev: {std_dev:.2f}'
    ))

# Update layout with explicit y-axis range
fig.update_layout(
    title='Distribution of Volume of the Bundles (Original + Replicated)',
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

fig.write_html('/home/alberto/analysis_bundle_stats/plot/interactive_plot_outlier.html')
fig.show()
