class SingleRule(object):

    def __init__(self, ruleName = 'DefaultSingleRule', paragraphNumber = None, title = None, text = None ):
        self.ruleName = ruleName
        self.tests = []
        self.paragraphNumber = paragraphNumber
        self.title = title
        self.text = text

    def registerTest(self, test):
        print('[{}] registering test'.format(self.ruleName))
        self.tests.append(test)

    def reportInformation(self, text):
        print('[inf][§{} {}] {}'.format(self.paragraphNumber, self.ruleName, text))
                                                                            
    def reportAnnotation(self, text):                                       
        print('[anm][§{} {}] {}'.format(self.paragraphNumber, self.ruleName, text))
                                                                            
    def reportIllegal(self, text):                                          
        print('[err][§{} {}] {}'.format(self.paragraphNumber, self.ruleName, text))

    def applyAllTests(self, building):
        print('rule {} appyling {} tests'.format(self.ruleName, len(self.tests)))
        for test in self.tests:
            test(building)


