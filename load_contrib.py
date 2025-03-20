def find_load_contributors(json_data, selected_edge_id):
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