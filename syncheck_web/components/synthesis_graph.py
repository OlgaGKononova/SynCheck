import dash_html_components as html
import dash_core_components as dcc
import dash_cytoscape as cyto
from syncheck_web.components.cytoscape_styles import syngraph_stylesheet

import regex as re


cyto.load_extra_layouts() # needed to export svg


def get_synthesis_graph(syn_data_flatten):

    operation_elements, operation_edges = [], []
    subject_elements, subject_edges = [], []
    condition_elements, condition_edges, condition_style = [], [], []

    if syn_data_flatten:
        operation_elements, operation_edges = get_operations_elements(syn_data_flatten)
        subject_elements, subject_edges = get_subjects_elements(syn_data_flatten)
        condition_elements, condition_edges, condition_style = get_condition_elements(syn_data_flatten)

    style_sheet = [{"selector": "." + c,
                    "style": s} for c, s in syngraph_stylesheet.items()] + condition_style

    graph = cyto.Cytoscape(id="synthesis-flowchart",
                          layout={"name": "preset",
                                  "fit": True,
                                  "padding": "5px"},
                          style={"width": "100%",
                                 "height": "500px",
                                 "background-color": "white"},
                          elements=operation_elements + operation_edges +
                                   subject_elements + subject_edges +
                                   condition_elements + condition_edges,
                          stylesheet=style_sheet
                          )
    return graph


def __get_operation_node(operation):
    op = operation["op_type"]
    op_id = op.replace("Operation", "").replace("ingSynthesis", "")
    op_label = op_id.upper()
    op_id = op_id.lower()
    classes = "nodes operation"
    if op == "StartingSynthesis":
        classes = classes + " operation_term"
    if operation["ref_op"]:
        classes = classes + " operation_ref"

    return op_id, op_label, classes


def get_operations_elements(synthesis_graph):
    elements, edges = [], []
    position_x = 0
    dx = 20

    # start synthesis
    elements.append(
        {"data": {"id": "start",
                  "label": "Start"},
         "renderedPosition": {"x": position_x,
                      "y": 0},
         "classes": "nodes operation operation_term"}
    )
    prev_op_id = "start"
    position_x = position_x + dx

    for num, data in enumerate(synthesis_graph):
        op_id, op_label, classes = __get_operation_node(data)
        op_id = op_id + str(num)
        elements.append(
            {"data": {"id": op_id,
                      "label": op_label},
             "renderedPosition": {"x": position_x,
                          "y": 0},
             "classes": classes,
             "pannable": True}
        )
        if prev_op_id != "":
            edges.append(
                {"data": {"source": prev_op_id,
                          "target": op_id,
                          "id": prev_op_id + op_id},
                 "classes": "operation_edges"}
            )

        # TODO: loop for regrinding
        # if "re" in data["op_token"][0:2] and not "react" in data["op_token"][0:2]:
        #     edges.append(
        #         {"data": {"source": op_id, "target": prev_op_id, "id": "loop" + op_id+prev_op_id},
        #          "classes": "operation_edges operation_edges_loop"}
        #     )
        position_x = position_x + dx
        prev_op_id = op_id

    elements.append(
        {"data": {"id": "finish",
                  "label": "END"},
         "renderedPosition": {"x": position_x,
                      "y": 0},
         "classes": "nodes operation operation_term",
         "pannable": True}
    )
    edges.append(
        {"data": {"source": prev_op_id,
                  "target": "finish",
                  "id": prev_op_id + "finish"},
         "classes": "operation_edges"}
    )

    return elements, edges


def __prettify_subject_str(text):
    text_output = text[0].lower() + text[1:]

    # remove articles and other descriptive keywords
    words_to_remove = ["the", "a", "an", "stoichiometric", "amount", "starting", "materials"]
    for s in words_to_remove:
        text_output = re.sub("\s*" + s + "\s+", " ", text_output)
    text_output = text_output.replace(" and ", ",").replace(",,", ",")

    return text_output


def get_subjects_elements(synthesis_graph):
    elements, edges = [], []
    position_y = -15
    position_x = 20
    dx = 20

    for num, data in enumerate(synthesis_graph):
        if data["subject"] != "" and data["op_type"] != "StartingSynthesis":
            s_id = "subject" + str(num)
            s_label = __prettify_subject_str(data["subject"])
            elements.append(
                {"data": {"id": s_id,
                          "label": s_label},
                 "renderedPosition": {"x": position_x,
                              "y": position_y},
                 "classes": "nodes subject"}
            )
            op_id = data["op_type"].replace("Operation", "").replace("ingSynthesis", "").lower() + str(num)
            edges.append(
                {"data": {"source": s_id,
                          "target": op_id,
                          "id": s_id + op_id},
                 "classes": "subject_edges"}
            )
        position_x = position_x + dx

    return elements, edges


def __value2string(t_value):
    if not t_value["values"]:
        if t_value["min"]:
            return str(t_value["min"]) + "-" + str(t_value["max"]) + t_value["units"]
        else:
            return "up to" + str(t_value["max"]) + t_value["units"]
    return ", ".join([str(t) for t in sorted(t_value["values"])]) + t_value["units"]


def get_condition_elements(synthesis_graph):
    elements, edges, style = [], [], []
    position_y = 15
    position_x = 20
    dx = 20
    c_dy = 3

    for num, data in enumerate(synthesis_graph):
        if data["time_values"] + data["temp_values"] != [] or "".join(data["env_toks"]) != "":
            class_name = "condition_nodes condition" + str(num)
            temps_str = "Temperature: " + ", ".join([__value2string(t) for t in data["temp_values"]])
            times_str = "Time: " + ", ".join([__value2string(t) for t in data["time_values"]])

            env_in_str = "in " + data["env_toks"][0] if data["env_toks"][0] else ""
            env_with_str = "with " + data["env_toks"][1] if data["env_toks"][1] else ""
            env_str = "Environment: " + env_in_str + " " + env_with_str

            elements.append(
                {"data": {"id": "temp" + str(num),
                          "label": temps_str + "\n" + times_str + "\n" + env_str
                          },
                 "renderedPosition": {"x": position_x,
                              "y": position_y - c_dy},
                 "classes": class_name}
            )
            labels_str = [len(temps_str), len(times_str)]
            # style.append(
            #     {
            #         "selector": ".condition" + str(num),
            #         "style": {
            #             "width": max(labels_str) * 0.8 if labels_str != [] else "label",
            #             "text-max-width": max(labels_str) * 0.8 if not env_in_str + env_with_str else len(
            #                 "Environment: ")
            #         }
            #     }
            # )
            op_id = data["op_type"].replace("Operation", "").replace("ingSynthesis", "").lower() + str(num)
            edges.append(
                {"data": {"source": "temp" + str(num),
                          "target": op_id,
                          "id": "time" + str(num) + op_id},
                 "classes": "condition_edges"}
            )
        position_x = position_x + dx

    return elements, edges, style
