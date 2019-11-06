from json import load


class JSONFile:
    def __init__(self):
        self.name = None
        self.time = None
        self.questions = list()
        self.loadJSON()

    def loadJSON(self):
        with open('questions.json') as f:
            self.jsonString = load(f)
        self.name = self.jsonString['name']
        self.time = self.jsonString['time']
        self.questions = self.jsonString['questions']

    def get_question(self, number):
        return self.questions[number]['question']

    def get_answers(self, number):
        return self.questions[number]['answers']

    def __len__(self):
        return len(self.questions)
