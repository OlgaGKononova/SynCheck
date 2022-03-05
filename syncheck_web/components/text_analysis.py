import syllables

import dash_html_components as html
import dash_core_components as dcc

from pprint import pprint

def FRE(paragraph):
    words_count = len([t for sent in paragraph for t in sent])
    sents_count = len(paragraph)
    syllables_count = sum([syllables.estimate(t) for sent in paragraph for t in sent])

    return 206.835 - 1.015 * (words_count / sents_count) - 84.6 * (syllables_count / words_count)


def FKRE(paragraph):
    words_count = len([t for sent in paragraph for t in sent])
    sents_count = len(paragraph)
    syllables_count = sum([syllables.estimate(t) for sent in paragraph for t in sent])

    return 0.39 * (words_count / sents_count) + 11.8 * (syllables_count / words_count) - 15.59


# def get_text_score(paragraph):
#     fre = FRE(paragraph)
#     fkre = FKRE(paragraph)
#     return [html.Label("FRE score: {}; FKRE score {}".format(round(fre, 2), round(fkre, 2)),
#                        style={"font-weight": "bold"}),
#             html.Br()]


def get_classification_label(classification_results):
    syntype = max(classification_results, key=lambda key: classification_results[key])
    if syntype == "something_else":
        return [html.Label("The paragraph sounds ambiguous. The synthesis type cannot be identified.",
                           style={"font-weight": "bold"}),
                html.Br()]
    return [html.Label("This paragraph is determined as a " + " ".join(syntype.split("_")),
                       #style={"font-weight": "bold"}
                       ),
            html.Br()
            ]

def get_text_stats(output_data):
    sents_num = len(output_data)
    words_num = len([t for sent in output_data for t in sent["tokens"]])
    actions_num = len([op for sent in output_data for op in sent["operations"]])
    sents_with_actions_num = len([sent for sent in output_data if sent["operations"]])
    actions_density = sents_with_actions_num / actions_num if actions_num != 0 else "N/A"
    paragraph = [[t for t in sent["tokens"]] for sent in output_data]
    fre = FRE(paragraph)
    fkre = FKRE(paragraph)
    return [html.Li("The text contains {} sentences, {} words, and {} synthesis actions.".format(sents_num, words_num, actions_num)),
            html.Li(["The synthesis actions density", html.Sup("*"), " is {}".format(round(actions_density, 2))]),
            html.Li(["Flesch reading ease", html.Sup("**"), " is {}".format(round(fre, 2))]),
            html.Br()]

def get_missing_attributes(syn_graph):
    attr_missing = {}
    for op in syn_graph:
        if op["op_type"] in ["Mixing", "Heating", "Cooling"] or any(w in op["op_token"] for w in ["dry", "evaporat"]):
            attr_missing[op["op_token"]] = set()
            if not op["time_values"]:
                attr_missing[op["op_token"]].add("time")
            if not op["temp_values"]:
                attr_missing[op["op_token"]].add("temperature")
            if all(not e for e in op["env_toks"]):
                attr_missing[op["op_token"]].add("environment")

    if all(not v for k, v in attr_missing.items()):
        return ["No missing synthesis action attributes. Good job!"]

    div_output = ["There are {} missing attributes for the synthesis actions:".format(len(attr_missing))]
    for op, attr in attr_missing.items():
        if attr:
            div_output.append(html.Li("\"{}\" is missing {}".format(op, ", ".join(list(attr)))))
    return div_output


                 