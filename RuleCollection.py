from SingleRule import SingleRule

class RuleCollection(object):

    def __init__(self):
        self.rules = []

    def addRule(self, rule):
        print('adding new rule')
        self.rules.append(rule)

    def checkRuleResultForBuilding(self, building):
        print('checking {} rules'.format(len(self.rules)))
        for f in self.rules:
            f.applyAllTests(building)
        print('done')


