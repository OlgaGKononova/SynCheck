# -*- coding: utf-8 -*-

import dash
from dash.dependencies import ClientsideFunction, Input, Output, State
import flask
from flask_caching import Cache

import json
import random as rnd

from syncheck_web.view import core_view_html
import syncheck_web.logic as el

"""
A safe place for the dash app core instance to hang out.
Also, all high level logic for every callback in the entire dash app.
Please do not define any html-returning functions in this file. Import them
from modules like common, view, or an app"s view submodule.
Please see CONTRIBUTING.md before editing this file or callback element ids.
"""

################################################################################
# Dash app core instance
################################################################################
# Any external js scripts you need to define.
# external_scripts = [
#     "https://www.googletagmanager.com/gtag/js?id=UA-149443072-1"
# ]

server = flask.Flask(__name__)
app = dash.Dash(__name__, assets_folder="assets/", server=server)


app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "SynCheck"

app.layout = core_view_html()
cache = Cache(app.server, config={"CACHE_TYPE": "simple"})


@app.callback(
    [Output("ner_result", "children"),
     Output("mosy_result", "children"),
     Output("graph_result", "children"),
     Output("export_table_btn", "disabled"),
     Output("export_graph_btn", "disabled"),
     Output("erase_btn", "disabled"),],
    [Input("extract_btn", "n_clicks")],
    [State("extract_textarea", "value")])
def extract_synthesis(extract_clicks, text):
    if extract_clicks > 0 and text is not None:
        return el.extract_data(text)
    return "", "", "", True, True, True


@app.callback(
    Output("extract_btn", "n_clicks"),
    [Input("erase_btn", "n_clicks")])
def erase_results(erase_clicks):
    return 0


@app.callback(
     Output("extract_textarea", "value"),
    [Input("example_btn", "n_clicks")])
def get_example_paragraph(n_clicks):
    if n_clicks:
        examples_list = json.loads(open("syncheck_web/assets/examples.json").read())
        nums = len(examples_list)
        paragraph = examples_list[rnd.randint(0, nums-1)]
        return paragraph
    return ""


@app.callback(
    Output("extract_btn", "disabled"),
    [Input("extract_textarea", "value")])
def extract_synthesis(text):
    return not text


@app.callback(
    Output("synthesis-flowchart", "generateImage"),
    [Input("export_graph_btn", "n_clicks")],
    [State("export_graph_btn", "disabled")])
def get_image(n_clicks, btn_disabled):
    output = {"type": None,
              "action": "store"}
    if n_clicks and not btn_disabled:
        output["type"] = "svg"
        output["action"] = "download"
    return output


# @app.callback(
#     [Output("synthesis-flowchart", "zoom"),
#      Output("synthesis-flowchart", "elements")],
#     [Input("reset_graph_btn", "n_clicks")],
#     [State("synthesis-flowchart", "zoom"),
#      State("synthesis-flowchart", "elements")])
# def reset_graph_layout(n_clicks, zoom, elements):
#     print (zoom)
#     if n_clicks:
#         zoom = 1
#     return zoom, elements
