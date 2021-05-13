syngraph_stylesheet = {
    "nodes": {
        "content": "data(label)",
        "text-halign": "center",
        "text-valign": "center",
        "width": "label",
        "height": "label",
        "shape": "rectangle",
    },
    "operation": {
        "background-color": "#0070C0",
        "background-opacity": 1.0,
        "border-width": 0.3,
        "border-color": "#1F497D",
        "border-opacity": 1.0,
        "padding": "2px",
        "font-size": 2,
        "font-weight": "bold",
        "color": "white",
        "text-halign": "center",
        "text-valign": "center"
    },
    "operation_term": {
        "color": "#F79646"
    },
    "operation_ref": {
        "background-opacity": 0.3,
        "border-opacity": 0.5,
    },
    "operation_edges": {
        "curve-style": "bezier",
        "target-arrow-shape": "triangle",
        "arrow-scale": 0.15,
        "target-arrow-color": "#1F497D",
        "width": 0.3,
        "line-color": "#1F497D",
        "source-distance-from-node": 0.0,
        "target-distance-from-node": 0.0
    },
    "operation_edges_loop": {
        "curve-style": "unbundled-bezier",
        "target-arrow-shape": "vee",
        "arrow-scale": 0.15,
        "width": 0.3,
        "source-distance-from-node": 0.0,
        "target-distance-from-node": 0.0,
        "source-endpoint": "270deg",
        "target-endpoint": "270deg",
        "control-point-distances": "-25",
        "edge-distances": "node-position",
    },
    "subject": {
        "background-color": "#F79646",
        "background-opacity": 1.0,
        "border-width": 0.3,
        "border-color": "#E46C0A",
        "padding": "1px",
        "font-size":1.5,
        "shape": "roundrectangle",
        "width": "15px",
        "text-wrap": "wrap",
        "text-max-width": "15px",
        "text-halign": "center",
        "text-valign": "center",
        "line-height": 2.0
    },
    "subject_edges": {
        "curve-style": "bezier",
        "target-arrow-shape": "triangle",
        "target-arrow-color": "#E46C0A",
        "source-distance-from-node": 0.0,
        "target-distance-from-node": 0.0,
        "line-color": "#E46C0A",
        "width": 0.3,
        "arrow-scale": 0.15
    },
    "condition_edges": {
        "curve-style": "bezier",
        "target-arrow-color": "#4A7F12",
        "target-arrow-shape": "triangle",
        "line-color": "#4A7F12",
        "width": 0.3,
        "arrow-scale": 0.15
    },
    "condition_nodes": {
        "content": "data(label)",
        "text-halign": "center",
        "text-valign": "center",
        "height": "label",
        "width": "15px",
        "background-color": "#7FC337",
        "background-opacity": 1.0,
        "padding": "1px",
        "font-size": 1.5,
        "shape": "rectangle",
        "border-width": 0.3,
        "border-color": "#4A7F12",
        "text-wrap": "wrap",
        "text-max-width": "15px",
        "line-height": 2.0
    }
}