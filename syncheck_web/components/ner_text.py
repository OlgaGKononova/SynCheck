import dash_html_components as html
import dash_core_components as dcc


def get_styled_paragraph(text_data):
    paragraph_layout = []
    for sentence in text_data:
        labels_map = __get_labels_map(sentence)
        paragraph_layout.append(html.Div([build_paragraph(sentence["tokens"], labels_map)],
                                         className="row", style={"margin": "10px"}))

    return paragraph_layout


def __get_labels_map(sentence_data):
    labels_map = {}
    for i, token in enumerate(sentence_data["tokens"]):
        labels_map[i] = ""
        for l in ["targets", "precursors", "operations"]:
            if i in sentence_data[l]:
                labels_map[i] = l[:-1]
        for l in ["temperatures", "times", "environment"]:
            if i in sentence_data[l]:
                labels_map[i] = "condition"
    return labels_map


def build_paragraph(tokens, labels):
    span_tokens = []
    for i, token in enumerate(tokens):
        span_tokens.append(html.Span(token, className=labels[i]))
        span_tokens.append(html.Span(" "))
    return html.Div(span_tokens, className="row")


def get_classification_label(classification_results):
    syntype = max(classification_results, key=lambda key: classification_results[key])
    if syntype == "something_else":
        return [html.Label("The paragraph sounds ambiguous. The synthesis type cannot be identified.",
                           style={"font-weight": "bold"}),
                html.Br()]
    return [html.Label("This paragraph sounds as a " + " ".join(syntype.split("_")),
                       style={"font-weight": "bold"}),
            html.Br()]