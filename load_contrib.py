"""
Load Path Contributor Analysis Module

This module analyzes load paths in mechanical systems by tracing the flow of forces
through connected components. It identifies which components contribute to the load
at a specific connection (edge) by traversing the graph structure upstream from the
selected edge.

The analysis helps in understanding:
- How loads are transmitted through the structure
- Which components influence a specific connection
- The path from load application points to the ground

Author: Pramod Kumar Yadav
Email: pkyadav01234@gmail.com
Date: March, 2025
"""

def find_load_contributors(json_data, selected_edge_id):
    """
    Identifies components that contribute to the load in a selected connection.

    This function analyzes a mechanical system's graph structure to find all nodes
    that can transmit forces to a specific connection (edge). It works by:
    1. Building a directed graph representation of the system
    2. Identifying the grounded (fixed) node
    3. Tracing the load path upstream from the selected connection
    4. Collecting all nodes that can contribute forces

    Args:
        json_data (dict): JSON data containing the graph structure with format:
            {
                "nodes": [
                    {
                        "data": {
                            "id": str,      # Unique node identifier
                            "name": str,    # Node name
                            ...            # Other node properties
                        }
                    },
                    ...
                ],
                "edges": [
                    {
                        "data": {
                            "id": str,      # Unique edge identifier
                            "source": str,  # Source node ID
                            "target": str   # Target node ID
                        }
                    },
                    ...
                ]
            }
        selected_edge_id (str): ID of the edge to analyze (e.g., "e0", "e1", etc.)

    Returns:
        dict or None: Dictionary containing analysis results with format:
            {
                "selected_edge": str,     # ID of analyzed edge
                "grounded_node": str,     # ID of the fixed/ground node
                "contributors": list      # List of node IDs that contribute load
            }
            Returns None if the specified edge is not found.

    Example:
        >>> with open("load_path_data.json") as f:
        ...     json_data = json.load(f)
        >>> result = find_load_contributors(json_data, "e0")
        >>> print(result)
        {
            'selected_edge': 'e0',
            'grounded_node': 'Node3',
            'contributors': ['Node0', 'Node1', 'Node2']
        }
    """
    # Step 1: Build adjacency list (source -> targets)
    graph = {}
    for edge in json_data["edges"]:
        source = edge["data"]["source"]
        target = edge["data"]["target"]
        if source not in graph:
            graph[source] = []
        graph[source].append(target)
    
    # Step 2: Identify grounded node (node with no outgoing edges)
    all_nodes = set(n["data"]["id"] for n in json_data["nodes"])
    grounded = all_nodes - set(graph.keys())  # Nodes with no outgoing edges
    grounded_node = grounded.pop() if grounded else None
    print(f"Grounded node: {grounded_node}")
    
    # Step 3: Check if the selected edge ID exists
    edges_with_id = [e["data"] for e in json_data["edges"] if e["data"]["id"] == selected_edge_id]
    if not edges_with_id:
        print(f"Error: Edge with ID '{selected_edge_id}' not found in the JSON data.")
        return None
    selected_edge = edges_with_id[0]
    
    # Step 4: Trace upstream nodes to find load contributors
    contributors = set()
    def trace_upstream(node):
        """
        Recursively traces upstream through the graph to find contributing nodes.
        
        Args:
            node (str): Current node ID to trace from
            
        Side Effects:
            Adds discovered nodes to the contributors set
        """
        contributors.add(node)
        for e in json_data["edges"]:
            if e["data"]["target"] == node:
                trace_upstream(e["data"]["source"])
    
    trace_upstream(selected_edge["source"])
    
    # Step 5: Return the result
    return {
        "selected_edge": selected_edge_id,
        "grounded_node": grounded_node,
        "contributors": list(contributors)
    }


# Example usage
if __name__ == "__main__":
    import json
    with open("load_path_data_20250321_000033.json") as f:
        json_data = json.load(f)
    result = find_load_contributors(json_data, "e20")
    print(result)