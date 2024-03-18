class Selector:

    def __init__(self, source: 'Selector'=None, matcher_type: str="", matcher_value: list="") -> None:
        self.source = source
        self.matcher_type = matcher_type
        self.matcher_value = matcher_value

    def text(self, value, pattern = 1):
        return Selector(self, "text", (value, pattern))
    
    def isBefore(self, anchor: 'Selector'):
        return Selector(self, "isBefore", (anchor, ))
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        if self.source and str(self.source):
            return str(self.source) + '.' + self.matcher_type + str(self.matcher_value)
        else:
            return self.matcher_type + str(self.matcher_value)


selector = Selector().text("haha").isBefore(Selector().text("hehe"))
print(selector)





        


