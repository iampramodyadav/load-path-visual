"""
@Author:    Pramod Kumar Yadav
@email:     pkyadav01234@gmail.com
@Date:      March, 2025
@status:    development
@PythonVersion: python3
"""

import dash
from dash import html, dcc, Input, Output, State, dash_table
import dash_cytoscape as cyto
import json
import random

app = dash.Dash(__name__)

# Add node property input fields
node_properties = html.Div([
    html.H3("Node Properties"),
    dcc.Dropdown(
        id='node-id-input',
        placeholder='Select Node ID',
        options=[]
    ),
    dcc.Input(id='node-name-input', placeholder='Node Name'),

    html.Div([
        html.Label("Position(x,y,z): "),
        dcc.Input(id='node-trans-x-input', type='number', placeholder='X', value=0,style={'width': '50px'}),
        dcc.Input(id='node-trans-y-input', type='number', placeholder='Y', value=0,style={'width': '50px'}),
        dcc.Input(id='node-trans-z-input', type='number', placeholder='Z', value=0,style={'width': '50px'})
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),

    html.Div([
        html.Label("Rotation Order:", style={'minWidth': '100px'}),
        dcc.Dropdown(
            id='rotation-order',
            options=[
                {'label': order, 'value': order} 
                for order in ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']
            ],
            value='xyz',
            style={'width': '120px'},
            placeholder='Rotation Order'
        )
    ],style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),

    html.Div([
        html.Label("Rotation (deg):", style={'minWidth': '100px'}),
        dcc.Input(id='node-euler-x-input', type='number', placeholder='X', value=0,style={'width': '50px'}),
        dcc.Input(id='node-euler-y-input', type='number', placeholder='Y', value=0,style={'width': '50px'}),
        dcc.Input(id='node-euler-z-input', type='number', placeholder='Z', value=0,style={'width': '50px'}),
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),    


    html.Hr(),
    html.Div([
        html.Label("Mass (kg): "),
        dcc.Input(id='node-mass-input', type='number', placeholder='Mass (kg)', value=0, style={'width': '50px'}),
    ]),

    html.Div([
        html.Label("CoG L(X,Y,Z): "),
        dcc.Input(id='node-cog-x-input', type='number', placeholder='X', value=0,style={'width': '50px'}),
        dcc.Input(id='node-cog-y-input', type='number', placeholder='Y', value=0,style={'width': '50px'}), 
        dcc.Input(id='node-cog-z-input', type='number', placeholder='Z', value=0,style={'width': '50px'})
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),
    html.Hr(),

    html.Div([
        html.Label("Force L(X,Y,Z):"),
        dcc.Input(id='node-force-x-input', type='number', placeholder='X', value=0,style={'width': '50px'}),
        dcc.Input(id='node-force-y-input', type='number', placeholder='Y', value=0,style={'width': '50px'}),
        dcc.Input(id='node-force-z-input', type='number', placeholder='Z', value=0,style={'width': '50px'})
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),
    
    html.Div([
        html.Label("Moment L(X,Y,Z):"),
        dcc.Input(id='node-moment-x-input', type='number', placeholder='X', value=0,style={'width': '50px'}),
        dcc.Input(id='node-moment-y-input', type='number', placeholder='Y', value=0,style={'width': '50px'}),
        dcc.Input(id='node-moment-z-input', type='number', placeholder='Z', value=0,style={'width': '50px'})
    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),
    html.Hr(),
    html.Button('Update Node', id='update-node-btn')

], style={'padding': '10px','borderRadius': '10px',  'border': '1px solid black'})

# Interactive Graph Builder controls
graph_builder = html.Div([
    html.H3("Interactive Graph Builder"),
    html.Button("Add Node", id='add-node-btn', n_clicks=0),
    html.Button("Delete Selected Node", id='delete-node-btn', n_clicks=0, style={'margin-left': '10px'}),
    html.Div(id='click-data'),
    html.Div(id='connection-list'),
    html.Div([
        html.Button("Export to JSON", id='export-json-btn', n_clicks=0),
        html.Button("Import from JSON", id='import-json-btn', n_clicks=0),
        dcc.Upload(
            id='upload-json',
            children=html.Div(['Drag and Drop or ', html.A('Select a JSON File')]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px 0'
            }
        ),
        html.Div(id='json-output')
    ], style={'margin-top': '20px'})
], style={'padding': '10px', 'border': '1px solid black', 'borderRadius': '10px', 'margin-top': '10px'})

# Node properties table
node_properties_table = html.Div([
    #html.H3("Node Properties Table"),
    dash_table.DataTable(
        id='node-properties-table',
        columns=[
            {'name': 'ID', 'id': 'id'},
            {'name': 'Name', 'id': 'name'},
            {'name': 'Mass (kg)', 'id': 'mass'},
            {'name': 'CoG X', 'id': 'cog_x'},
            {'name': 'CoG Y', 'id': 'cog_y'},
            {'name': 'CoG Z', 'id': 'cog_z'},
            {'name': 'Force X', 'id': 'force_x'},
            {'name': 'Force Y', 'id': 'force_y'},
            {'name': 'Force Z', 'id': 'force_z'},
            {'name': 'Moment X', 'id': 'moment_x'},
            {'name': 'Moment Y', 'id': 'moment_y'},
            {'name': 'Moment Z', 'id': 'moment_z'},
            {'name': 'Euler X', 'id': 'euler_x'},
            {'name': 'Euler Y', 'id': 'euler_y'},
            {'name': 'Euler Z', 'id': 'euler_z'},
            {'name': 'Rotation Order', 'id': 'rotation_order'},
            {'name': 'Trans X', 'id': 'trans_x'},
            {'name': 'Trans Y', 'id': 'trans_y'},
            {'name': 'Trans Z', 'id': 'trans_z'}
        ],
        data=[],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'center',
            'minWidth': '80px', 
            'maxWidth': '120px',
            'whiteSpace': 'normal'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )
], style={
    #'padding': '10px', 'border': '1px solid black', 'margin-top': '10px',
    'height': '20%',
    'marginTop': '10px', 
    'padding': '10px', 
    'borderRadius': '10px',
    'backgroundColor': '#f9f9f9'
    })

app.layout = html.Div([
    # Store for graph data
    dcc.Store(id='graph-data', data={'nodes': [], 'edges': []}),
    # Store for node positions
    dcc.Store(id='node-positions', data={}),
    # Store for downloaded JSON
    dcc.Download(id='download-json'),
    # Store for selected node
    dcc.Store(id='selected-node', data=None),
    
    html.H1("Interactive Graph Builder", style={'textAlign': 'center'}),
    
    # Main layout with sidebar and plot area using CSS Grid
    html.Div([
        # Left sidebar
        html.Div([
            # Top: Node Properties
            node_properties,
            # Bottom: Interactive Graph Builder
            graph_builder
        ], style={
            #'backgroundColor': '#ecf0f1',
            #'height': '85vh',
            #'gridArea': 'sidebar',
            #'padding': '10px',
            #'overflowY': 'auto',
            #'maxHeight': 'calc(100vh - 100px)'
            'width': '25%', 
            'padding': '15px',
            'borderRadius': '10px',
            'backgroundColor': '#ecf0f1',
            'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)',
            'height': '80vh',
            # 'height': '100%',
            'overflowY': 'auto'
        }),
        
        # Right plot area
        html.Div([
            # Cytoscape component
            cyto.Cytoscape(
                id='cytoscape',
                layout={'name': 'preset'},
                style={
                    #'width': '100%', 
                    #'height': '800px',
                    'height': '80%', 
                    'borderRadius': '10px', 
                    'boxShadow': '2px 2px 15px rgba(0,0,0,0.2)',
                    'backgroundColor': 'white',
                    'padding': '10px'
                    },
                elements=[],
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'background-color': 'data(color)',
                            'label': 'data(id)',
                            'content': 'data(name)',
                            'text-valign': 'center',
                            'text-halign': 'center'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'line-color': '#555',
                            'target-arrow-color': '#555',
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier'
                        }
                    },
                    {
                        'selector': 'node:selected',
                        'style': {
                            'border-width': '3px',
                            'border-color': '#333',
                            'border-style': 'solid'
                        }
                    }
                ]
            ),
            # Node properties table below the plot
            node_properties_table,
            html.Footer('© 2025 Pramod Kumar Yadav (@iAmPramodYadav)'),
        ], style={
            'width': '75%', 'height': '80vh',
            #'gridArea': 'main',
            #'padding': '10px',
            #'backgroundColor': '#f8f9fa',
            #'borderRadius': '5px',
            #'boxShadow': '0 0 10px rgba(0,0,0,0.1)',
            #'overflowY': 'auto'
        })
    ], style={
        'display': 'flex', 
        'justifyContent': 'space-between', 
        'gap': '20px', 
        'padding': '20px',
        #'display': 'grid',
        #'gridTemplateColumns': '300px 1fr',
        #'gridTemplateAreas': '"sidebar main"',
        #'gap': '10px',
        #'height': 'calc(100vh - 100px)',
        #'width': '100%'
    })
])

# Callback to add nodes on button click
@app.callback(
    Output('graph-data', 'data'),
    Input('add-node-btn', 'n_clicks'),
    State('graph-data', 'data')
)
def add_node(n_clicks, data):
    if not n_clicks:
        return dash.no_update
    
    # Generate a unique node ID that doesn't already exist
    existing_ids = [node['data']['id'] for node in data['nodes']]
    node_id = None
    counter = 0
    while node_id is None or node_id in existing_ids:
        node_id = f'n{counter}'
        counter += 1
        
    colors = ['#FF4136', '#2ECC40', '#0074D9', '#FF851B', '#B10DC9']
    
    # Random position for button click
    pos_x = random.uniform(100, 800)
    pos_y = random.uniform(100, 500)
        
    data['nodes'].append({
        'data': {
            'id': node_id,
            'name': node_id,  # Default name same as ID
            'color': random.choice(colors),
            'mass': 0,  # Default values
            'cog': [0, 0, 0],
            'external_force': [0, 0, 0],
            'moment': [0, 0, 0],
            'euler_angles': [0, 0, 0],
            'rotation_order': 'xyz',
            'translation': [0, 0, 0]
        },
        'position': {'x': pos_x, 'y': pos_y}
    })
    return data

# Store selected node
@app.callback(
    Output('selected-node', 'data'),
    Input('cytoscape', 'tapNodeData')
)
def store_selected_node(node_data):
    if node_data:
        return node_data['id']
    return None

# Callback to delete selected node
@app.callback(
    [Output('graph-data', 'data', allow_duplicate=True),
     Output('click-data', 'children', allow_duplicate=True)],
    Input('delete-node-btn', 'n_clicks'),
    State('selected-node', 'data'),
    State('graph-data', 'data'),
    prevent_initial_call=True
)
def delete_node(n_clicks, selected_node_id, graph_data):
    if not n_clicks or not selected_node_id:
        return dash.no_update, dash.no_update
    
    # Remove the node
    graph_data['nodes'] = [node for node in graph_data['nodes'] 
                          if node['data']['id'] != selected_node_id]
    
    # Remove any edges connected to this node
    graph_data['edges'] = [edge for edge in graph_data['edges'] 
                          if edge['data']['source'] != selected_node_id and 
                             edge['data']['target'] != selected_node_id]
    
    # Reset the click state to avoid connection issues
    return graph_data, "Click a node to start new connection."

# Callback to update cytoscape with stored data while preserving positions
@app.callback(
    Output('cytoscape', 'elements'),
    [Input('graph-data', 'data')],
    [State('cytoscape', 'elements')]
)
def update_cytoscape(data, current_elements):
    # Create a dictionary of current node positions
    current_positions = {}
    if current_elements:
        for element in current_elements:
            if 'position' in element and 'data' in element and 'id' in element['data']:
                current_positions[element['data']['id']] = element['position']
    
    # Create new elements with preserved positions
    elements = []
    for node in data['nodes']:
        node_copy = node.copy()
        node_id = node['data']['id']
        # If we have a stored position for this node, use it
        if node_id in current_positions:
            node_copy['position'] = current_positions[node_id]
        elements.append(node_copy)
    
    # Add edges - only if both source and target nodes exist
    node_ids = {node['data']['id'] for node in data['nodes']}
    for edge in data['edges']:
        source = edge['data']['source']
        target = edge['data']['target']
        if source in node_ids and target in node_ids:
            elements.append(edge)
    
    return elements

# Store node positions when they are moved
@app.callback(
    Output('node-positions', 'data'),
    Input('cytoscape', 'tapNodeData'),
    Input('cytoscape', 'mouseoverNodeData'),
    State('cytoscape', 'elements'),
    State('node-positions', 'data')
)
def store_node_positions(tap_data, mouseover_data, elements, positions):
    # This callback doesn't actually update anything, it just captures positions
    # from the elements when other interactions happen
    if elements:
        for element in elements:
            if 'position' in element and 'data' in element and 'id' in element['data']:
                positions[element['data']['id']] = element['position']
    return positions

# Callback to handle node connections
@app.callback(
    [Output('graph-data', 'data', allow_duplicate=True),
     Output('click-data', 'children')],
    Input('cytoscape', 'tapNodeData'),
    State('click-data', 'children'),
    State('graph-data', 'data'),
    prevent_initial_call=True
)
def handle_node_click(node_data, click_state, graph_data):
    if not node_data:
        return dash.no_update, dash.no_update
        
    clicked_node = node_data['id']
    
    # Verify the clicked node exists in the graph data
    node_exists = any(node['data']['id'] == clicked_node for node in graph_data['nodes'])
    if not node_exists:
        return graph_data, "Node no longer exists. Click a valid node."
    
    if not click_state or 'First node:' not in click_state:
        return graph_data, f"First node: {clicked_node}. Click another node to create connection."
    else:
        first_node = click_state.split(': ')[1].split('.')[0]
        
        # Verify first node still exists
        first_node_exists = any(node['data']['id'] == first_node for node in graph_data['nodes'])
        if not first_node_exists:
            return graph_data, f"First node no longer exists. New first node: {clicked_node}. Click another node to create connection."
        
        # Don't create self-loops
        if first_node == clicked_node:
            return graph_data, f"Cannot connect a node to itself. First node: {clicked_node}. Click another node to create connection."
        
        # Check if this edge already exists
        edge_exists = any(
            (edge['data']['source'] == first_node and edge['data']['target'] == clicked_node) or
            (edge['data']['source'] == clicked_node and edge['data']['target'] == first_node)
            for edge in graph_data['edges']
        )
        
        if edge_exists:
            return graph_data, f"Connection already exists. First node: {clicked_node}. Click another node to create connection."
        
        edge_id = f'e{len(graph_data["edges"])}'
        
        graph_data['edges'].append({
            'data': {
                'id': edge_id,
                'source': first_node,
                'target': clicked_node
            }
        })
        
        return graph_data, "Click a node to start new connection."

# Callback to display connection list
@app.callback(
    Output('connection-list', 'children'),
    Input('graph-data', 'data')
)
def update_connection_list(data):
    if not data['edges']:
        return "No connections yet"
        
    connections = [
        html.Li(f"{edge['data']['source']} → {edge['data']['target']}")
        for edge in data['edges']
    ]
    return html.Div([
        html.H3("Connections:"),
        html.Ul(connections)
    ])

# Callback to handle connection deletion
@app.callback(
    Output('graph-data', 'data', allow_duplicate=True),
    Input('cytoscape', 'tapEdgeData'), 
    State('graph-data', 'data'),
    prevent_initial_call=True
)
def delete_connection(edge_data, graph_data):
    if not edge_data:
        return dash.no_update
        
    graph_data['edges'] = [edge for edge in graph_data['edges'] 
                         if edge['data']['id'] != edge_data['id']]
    return graph_data

# Callback to update node properties
@app.callback(
    Output('graph-data', 'data', allow_duplicate=True),
    Input('update-node-btn', 'n_clicks'),
    [State(f'node-{prop}-input', 'value') for prop in 
     ['id', 'name', 'mass', 
      'cog-x', 'cog-y', 'cog-z',
      'force-x', 'force-y', 'force-z',
      'moment-x', 'moment-y', 'moment-z',
      'euler-x', 'euler-y', 'euler-z',
      'trans-x', 'trans-y', 'trans-z']] +
    [State('rotation-order', 'value'),
     State('graph-data', 'data'),
     State('cytoscape', 'elements')],
    prevent_initial_call=True
)
def update_node_properties(n_clicks, node_id, name, mass, 
                         cog_x, cog_y, cog_z,
                         force_x, force_y, force_z,
                         moment_x, moment_y, moment_z,
                         euler_x, euler_y, euler_z,
                         trans_x, trans_y, trans_z,
                         rotation_order, graph_data, elements):
    if not node_id:
        return dash.no_update
    
    # Get current positions from elements
    current_positions = {}
    for element in elements:
        if 'position' in element and 'data' in element and 'id' in element['data']:
            current_positions[element['data']['id']] = element['position']
        
    for node in graph_data['nodes']:
        if node['data']['id'] == node_id:
            # Preserve the node's position
            if node_id in current_positions and 'position' in node:
                node['position'] = current_positions[node_id]
                
            node['data'].update({
                'name': name or node_id,
                'mass': float(mass) if mass else 0,
                'cog': [float(x) if x else 0 for x in [cog_x, cog_y, cog_z]],
                'external_force': [float(x) if x else 0 for x in [force_x, force_y, force_z]],
                'moment': [float(x) if x else 0 for x in [moment_x, moment_y, moment_z]],
                'euler_angles': [float(x) if x else 0 for x in [euler_x, euler_y, euler_z]],
                'rotation_order': rotation_order,
                'translation': [float(x) if x else 0 for x in [trans_x, trans_y, trans_z]]
            })
            break
            
    return graph_data

# Callback to update node ID dropdown options
@app.callback(
    Output('node-id-input', 'options'),
    Input('graph-data', 'data')
)
def update_node_dropdown(data):
    return [{'label': node['data']['id'], 'value': node['data']['id']} for node in data['nodes']]

# Callback to update node properties table
@app.callback(
    Output('node-properties-table', 'data'),
    Input('graph-data', 'data')
)
def update_node_properties_table(data):
    table_data = []
    for node in data['nodes']:
        node_data = node['data']
        table_data.append({
            'id': node_data['id'],
            'name': node_data['name'],
            'mass': node_data['mass'],
            'cog_x': node_data['cog'][0],
            'cog_y': node_data['cog'][1],
            'cog_z': node_data['cog'][2],
            'force_x': node_data['external_force'][0],
            'force_y': node_data['external_force'][1],
            'force_z': node_data['external_force'][2],
            'moment_x': node_data['moment'][0],
            'moment_y': node_data['moment'][1],
            'moment_z': node_data['moment'][2],
            'euler_x': node_data['euler_angles'][0],
            'euler_y': node_data['euler_angles'][1],
            'euler_z': node_data['euler_angles'][2],
            'rotation_order': node_data['rotation_order'],
            'trans_x': node_data['translation'][0],
            'trans_y': node_data['translation'][1],
            'trans_z': node_data['translation'][2]
        })
    return table_data

# Callback to export graph data to JSON
@app.callback(
    Output('download-json', 'data'),
    Input('export-json-btn', 'n_clicks'),
    State('graph-data', 'data'),
    prevent_initial_call=True
)
def export_json(n_clicks, data):
    if not n_clicks:
        return dash.no_update
    
    return dict(
        content=json.dumps(data, indent=2),
        filename='graph_data.json'
    )

# Callback to import graph data from JSON
@app.callback(
    [Output('graph-data', 'data', allow_duplicate=True),
     Output('json-output', 'children')],
    Input('upload-json', 'contents'),
    State('upload-json', 'filename'),
    prevent_initial_call=True
)
def import_json(contents, filename):
    if contents is None:
        return dash.no_update, dash.no_update
    
    content_type, content_string = contents.split(',')
    
    try:
        if 'json' in filename:
            # Decode the base64 string
            import base64
            decoded = base64.b64decode(content_string).decode('utf-8')
            data = json.loads(decoded)
            return data, html.Div(f"Successfully imported {filename}")
        else:
            return dash.no_update, html.Div("Please upload a JSON file", style={'color': 'red'})
    except Exception as e:
        return dash.no_update, html.Div(f"Error processing file: {str(e)}", style={'color': 'red'})

if __name__ == '__main__':
    app.run_server(port=r'8051', debug=True)
