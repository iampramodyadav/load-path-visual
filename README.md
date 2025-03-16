# Load Path Visual Tool

An interactive web-based tool for creating and visualizing load path graphs with node properties and connections. Built with Dash and Cytoscape.js.

## Overview

Load Path Visual is a powerful tool designed for engineers and analysts to create, visualize, and analyze load path diagrams. It provides an intuitive interface for building node-based graphs with detailed mechanical properties such as mass, center of gravity, forces, and moments.

## Features

- **Interactive Graph Building**
  - Add and delete nodes with drag-and-drop functionality
  - Create connections between nodes
  - Visual node selection and connection management
  - Real-time graph updates

- **Node Properties Management**
  - Mass configuration
  - Center of Gravity (CoG) coordinates (X,Y,Z)
  - Position/Translation coordinates
  - Rotation angles with customizable order (Euler angles)
  - Force vectors (X,Y,Z)
  - Moment vectors (X,Y,Z)

- **Data Management**
  - Export graph data to JSON
  - Import graph data from JSON files
  - Real-time property table view
  - Persistent node positioning

- **Visual Features**
  - Color-coded nodes
  - Directional arrows for connections
  - Node selection highlighting
  - Clean and modern UI design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/load-path-visual.git
cd load-path-visual
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Dependencies

- dash
- dash-cytoscape
- dash-html-components
- dash-core-components
- dash-table

## Usage

1. Start the application:
```bash
python load-visual.py
```

2. Open your web browser and navigate to:
```
http://localhost:8051
```

### Creating a Graph

1. **Adding Nodes**
   - Click the "Add Node" button to create a new node
   - Nodes will appear with random colors and positions

2. **Creating Connections**
   - Click on a source node
   - Click on a target node to create a connection
   - Connections are displayed with directional arrows

3. **Modifying Node Properties**
   - Select a node from the dropdown
   - Update properties in the side panel:
     - Mass
     - Center of Gravity
     - Position
     - Rotation
     - Forces
     - Moments
   - Click "Update Node" to save changes

4. **Managing Data**
   - Export: Click "Export to JSON" to save your graph
   - Import: Use "Import from JSON" to load a saved graph
   - View all node properties in the table below the graph

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Pramod Kumar Yadav  
Email: pkyadav01234@gmail.com

## Acknowledgments

- Built with [Dash](https://dash.plotly.com/)
- Graph visualization powered by [Cytoscape.js](https://js.cytoscape.org/)
