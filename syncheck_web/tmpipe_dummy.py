import json

class TMPipeDummy:
    def __init__(self):
        print("RUNNING DUMMY TM PIPELINE FOR TESTING PURPOSES!")

    def process_paragraph(self, paragraph_text):
        output = json.loads(open('/home/olga/Desktop/SynthesisProject/graph_example_new.json').read())

        return output

    def process_paragraph_mp(self, paragraph_text):
        pass

    def process_paragraph_batch(self, paragraphs_batch):
        pass
