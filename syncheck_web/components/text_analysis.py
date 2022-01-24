import syllables

import dash_html_components as html
import dash_core_components as dcc


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
            #html.Br()
            ]

def get_text_stats(output_data):
    sents_num = len(output_data)
    words_num = len([t for sent in output_data for t in sent["tokens"]])
    actions_num = len([op for sent in output_data for op in sent["operations"]])
    sent_action_ratio = len(output_data)/actions_num if actions_num else "N/A"
    actions_density = 1/actions_num * sum([1/len(sent["operations"]) for sent in output_data if sent["operations"]]) if actions_num else "N/A"
    paragraph = [[t for t in sent["tokens"]] for sent in output_data]
    fre = FRE(paragraph)
    fkre = FKRE(paragraph)
    return [html.Li("The text contains {} sentences, {} words, and {} synthesis actions.".format(sents_num, words_num, actions_num)),
            html.Li("The sentence/actions ratio is {} (desired value ~1.0)".format(round(sent_action_ratio, 2))),
            html.Li("The synthesis language density is {}".format(round(actions_density, 2))),
            html.Li([html.A("Flesch reading ease",
                             href="https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests",
                             target="_blank"),
                      " {} (the higher the better)".format(round(fre, 2))]),
            html.Li([html.A("Flesch–Kincaid grade level",
                             href="https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests",
                             target="_blank"),
                      " {} (the higher the better)".format(round(fkre, 2))]),
            html.Br()]
