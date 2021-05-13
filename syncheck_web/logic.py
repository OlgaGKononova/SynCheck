import os
import requests as rq

from syncheck_web.components.mosy_table import mosy_layout
from syncheck_web.components.ner_text import get_styled_paragraph, get_classification_label
from syncheck_web.components.synthesis_graph import get_synthesis_graph

# from syncheck_web.tmpipe_dummy import TMPipeDummy
# tmpipe = TMPipeDummy()

tmpipe_api = os.environ.get("TMPIPE_API", "")
matbert_api = os.environ.get("MATBERT_API", "")


def __normalize_text(text):
    """
    function to normalize symbols for proper API query encoding
    :param text:
    :return:
    """
    replacements = {";": ",",
                    "&": "",
                    "+": "%2B",
                    "?": ""}
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def extract_data(text):

    if not tmpipe_api:
        print("No TMpipe API found. Check if the path exist in $TMPIPE_API")
        exit(0)

    q_text = __normalize_text(text)
    r_out = rq.get(tmpipe_api+"?paragraph="+q_text).json()
    output_data = r_out["results"]

    r_out = rq.get(matbert_api+"?paragraph="+q_text).json()
    matbert_results = r_out["scores"]

    # output_data = tmpipe.process_paragraph(text)
    # matbert_results = {}

    ner_data = []
    for sentence in output_data:
        ner_data.append({"tokens": sentence["tokens"],
                         "targets": [t for m in sentence["targets"] for t in m["token_ids"]],
                         "precursors": [t for m in sentence["precursors"] for t in m["token_ids"]],
                         "operations": [op["op_id"] for op in sentence["graph"]],
                         "temperatures": [t for op in sentence["graph"] for temp in op["temp_values"]
                                          for t in temp["tok_ids"]],
                         "times": [t for op in sentence["graph"] for time in op["time_values"] for t in
                                   time["tok_ids"]],
                         "environment": [t for op in sentence["graph"] for env in op["env_ids"] for t in env]})

    ner_layout = get_styled_paragraph(ner_data)
    matbert_label = get_classification_label(matbert_results)

    table_layout = mosy_layout

    synthesis_graph = [op for sent in output_data for op in sent["graph"] if "Start" not in op["op_type"]]
    graph_layout = get_synthesis_graph(synthesis_graph)
    export_table_btn = False
    export_graph_btn = graph_layout is None

    return matbert_label+ner_layout, table_layout, graph_layout, export_table_btn, export_graph_btn, export_graph_btn
