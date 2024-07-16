import pandas as pd
import plotly.graph_objects as go

# Load data
stats = pd.read_csv('/home/alberto/analysis_bundle_stats/tract_info_csv/tract_info_dff.csv')
source_grouping = stats.groupby('source')
replicated = source_grouping.get_group('replicated_tractograms')
original = source_grouping.get_group('original_tractograms')

# Group data by bundle name and compute the mean volume for each bundle
mean_volumes_r = replicated.groupby('bundle_name')['bundle_Volume'].mean().reset_index()
std_volumes_r = replicated.groupby('bundle_name')['bundle_Volume'].std()
colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)','rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)']
# Create a bar graph

x_data = ['AF_L', 'FAT_L', 'IFOF_L', 'ILF_L', 'PYT_L']
fig = go.Figure()

fig.add_trace(go.Bar(
    x=mean_volumes_r['bundle_name'],
    y=mean_volumes_r['bundle_Volume'],
        error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=std_volumes_r*2,
            color='lightgray',
            visible=True),
    marker_color=colors,
    text=[f"{x:.2e}" for x in mean_volumes_r['bundle_Volume']],  #Add volume values as text labels
    textposition='auto',  #Position text labels automatically

    ))

# Update layout
fig.update_layout(
    title='Mean Volume of Bundles (replicated)',
    xaxis=dict(
        title='Bundle Name'
    ),
    yaxis=dict(
        title='Mean Volume',
        range=[0, 45000]  # Adjust y-axis range for better visualization
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
fig.write_html('/home/alberto/analysis_bundle_stats/plot/mean_volume_bar_graph_r.html')
# Show the plot
fig.show()

mean_volumes_o = original.groupby('bundle_name')['bundle_Volume'].mean().reset_index()
std_volumes_o = original.groupby('bundle_name')['bundle_Volume'].std()



fig = go.Figure()

fig.add_trace(go.Bar(
    x=mean_volumes_o['bundle_name'],
    y=mean_volumes_o['bundle_Volume'],
        error_y=dict(
            type='data', # value of error bar given in data coordinates
            array=std_volumes_o,
            color='lightgray',
            visible=True),
    marker_color=colors,
    text=[f"{x:.2e}" for x in mean_volumes_o['bundle_Volume']],  # Add volume values as text labels
    textposition='auto',  #Position text labels automatically

    ))

# Update layout
fig.update_layout(
    title='Mean Volume of Bundles (original)',
    xaxis=dict(
        title='Bundle Name'
    ),
    yaxis=dict(
        title='Mean Volume',
        range=[0, 45000]  # Adjust y-axis range for better visualization
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
fig.write_html('/home/alberto/analysis_bundle_stats/plot/mean_volume_bar_graph_o.html')
# Show the plot
fig.show()
