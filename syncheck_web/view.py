# coding=utf-8
import dash_core_components as dcc
import dash_html_components as html

"""
Defining the core view (layout) component for the entire app.
Please do not define any callback logic in this file.
"""


def core_view_html():
    core_view = html.Div([draw_header(),
                          draw_separator("20px"),
                          draw_intro_text(),
                          html.Div([html.Div([], className="one column"),
                                    html.Div([draw_text_input(),
                                              draw_disclaimer(),
                                              draw_separator("20px"),
                                              draw_text_stat(),
                                              draw_separator("10px"),
                                              draw_extraction_labels(),
                                              draw_separator("10px"),
                                              dcc.Loading([html.Div([draw_ner_results(),
                                                                     draw_table()],
                                                                    id="extract_result",
                                                                    className="row"),
                                                          draw_separator("30px"),
                                                          draw_synthesis_graph_labels()],
                                                          type="dot",
                                                          color="#c00000"
                                                          ),
                                              draw_separator("10px"),
                                              draw_synthesis_graph(),
                                              draw_separator("10px"),
                                              ],
                                             className="ten columns"),
                                    html.Div([], className="one column")],
                                   className="row"),
                          draw_about_text(),
                          draw_separator("10px"),
                          draw_footnotes_text(),
                          draw_separator("120px"),
                          draw_footer()
                          ])
    return core_view


def draw_header():
    return html.Div([html.Div([html.Img(src="assets/SynCheck_logo.png",
                                        width="250 px",
                                        style={"align": "left"})],
                              className="nine columns",
                              style={"padding-top": "1%",
                                     "padding-left": "3%",
                                     "align-items": "left"}),
                     html.Div([html.Img(src="assets/GENESIS-CEDER_logo_250px.png",
                                        width="250 px",
                                        style={"align": "right"})],
                              className="three columns",
                              style={"align-items": "right",
                                     "padding-top": "1%",
                                     "padding-right": "1%"})],
                    className="row")


def draw_intro_text():
    return html.Div([html.Div(className="one column"),
                     html.Label("Check how accurate AI interprets your description of synthesis procedure. "
                                "Modify the text to obtain the best result.",
                                className="ten columns label-h1"),
                     html.Div(className="one column")],
                    className="row"
                    )


def draw_about_text():
    return html.Div([html.Div(className="one column"),
                     html.Div([html.Label("About", className="label-h1"),
                               "SynCheck applies natural language processing methodology to interpret a human-written "
                               "text and to convert information about material synthesis into machine-readable format. "
                               "Implementation details of the pipeline are described in our recent papers: ",
                               html.A("Kononova et al. Scientific Data (2019)",
                                      href="https://www.nature.com/articles/s41597-019-0224-1"),
                               " - general description of the pipeline; ",
                               html.A("He et al. Chemistry of Materials (2020)",
                                      href="https://pubs.acs.org/doi/abs/10.1021/acs.chemmater.0c02553"),
                               " - materials entities recognition engine; ",
                               html.A("Huo et al. npj Computational Materials (2019)",
                                      href="https://www.nature.com/articles/s41524-019-0204-1"),
                               " - classification of synthesis procedures.",
                               html.Br(),
                               "If you use SynCheck in your work, please cite: "
                               "Kononova et al. \"Text-mined dataset of inorganic materials synthesis recipes\", ",
                               html.Em("Scientific Data"), " 6, 203 (2019)"],
                              className="ten columns"),
                     html.Div(className="one column")],
                    className="row",
                    style={"line-height": "170%"}
                    )

def draw_footnotes_text():
    return html.Div([html.Div(className="one column"),
                     html.Div([html.Label("[*]Relative ratio of number of sentences with synthesis actions "
                                          "to total number of synthesis actions. Should be close to 1.0."),
                               html.Label("[**]Higher score indicates text that is easier to read.")],
                              className="ten columns"),
                     html.Div(className="one column")])


def draw_text_input():
    return html.Div([dcc.Textarea(id="extract_textarea",
                                  placeholder="Input synthesis paragraph to extract information.",
                                  style={"resize": "vertical",
                                         "height": "200px"},
                                  className="eleven columns"),
                     html.Div([html.Button("EXTRACT",
                                           className="button-primary",
                                           id="extract_btn",
                                           disabled=True),
                               html.Tr(html.Td(style={"height": "2px"})),
                               html.Button("CLEAR RESULTS",
                                           className="button-primary",
                                           id="erase_btn",
                                           disabled=True),
                               html.Tr(html.Td(style={"height": "2px"})),
                               html.Button("SAVE",
                                           className="button-primary",
                                           id="save_btn",
                                           disabled=True),
                               html.Tr(html.Td(style={"height": "2px"})),
                               html.Button("EXAMPLE",
                                           className="button-primary",
                                           id="example_btn"),
                               ],
                              className="one column",
                              style={"verticalAlign": "middle",
                                     "align-items": "center"})],
                    className="row",
                    style={"marginTop": "10px"})


def draw_disclaimer():
    return html.Div(html.Em("Disclaimer: The information extracted from the paragraph "
                            "will NOT be saved anywhere on the server"),
                    className="row",
                    style={"font-size": "11pt"})

def draw_text_stat():
    return html.Div([html.Label("Text statistics",
                                className="label-h1"),
                     html.Div(id="text-stat",
                              style={"font-weight": "bold"})],
                    className="row")


def draw_extraction_labels():
    return html.Div([html.Label("Extraction results",
                                className="six columns label-h1"),
                     html.Label("MOSY data table",
                                className="five columns label-h1"),
                     html.Div(html.Button("EXPORT TABLE",
                                          className="button-primary",
                                          id="export_table_btn",
                                          disabled=True),
                              className="one column")],
                    className="row")


def draw_separator(size_str):
    return html.Tr(html.Td(style={"height": size_str}))


def draw_ner_results():
    return html.Div(id="ner_result",
                    className="six columns extraction-output"
                    )


def draw_table():
    return html.Div(id="mosy_result",
                    className="six columns extraction-output",
                    # TODO: this is a placeholder, remove when table extraction is implemented
                    )


def draw_synthesis_graph_labels():
    return html.Div([html.Label("Synthesis graph",
                                className="eleven columns label-h1"),
                     html.Div(html.Button("EXPORT GRAPH",
                                          className="button-primary",
                                          id="export_graph_btn",
                                          disabled=True),
                              className="one column")],
                    className="row")


def draw_synthesis_graph():
    return html.Div([html.Div(id="graph_result",
                              className="row",
                              style={"border": "1.5px solid #97A5B9"})])


def draw_footer():
    return html.Div([html.Div([html.Div(["Designed by ",
                                         html.A("Olga Kononova", href="https://olgakononova.com/", target="_blank")]),
                               html.Label("SYNthesis Check © 2021 "),
                               html.Div([html.A("CEDER Research Group", href="http://ceder.berkeley.edu/", target="_blank"),
                                         " (Lawrence Berkeley National Laboratory, Berkeley, CA, USA)"]),
                               html.Div([html.A("GENESIS Research Center", href="https://www.stonybrook.edu/genesis/", target="_blank"),
                                         " (Stony Brook University, New York, NY, USA)"])],
                              className="nine columns",
                              style={"font-size": "12px"}
                              ),
                     html.Div([html.P("\n"),
                               html.A("Send your questions and feedback", href="mailto:syncheck@googlegroups.com")],
                              className="three columns")],
                    className="row footer")
