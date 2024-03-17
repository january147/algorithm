
import re
express = r'text("hello").isBefore(text("haha", isAfter(isBefore(text("he\"he").type("haha")))))'


def is_alpha(_char):
    if (ord('a') <=  ord(_char) <= ord('z')) or ord('A') <=  ord(_char) <= ord('Z'):
        return True
    else:
        return False

# def remove_escaping_char(string):
#     return re.sub(r"\\(.)", r"\1", string)


def remove_escaping_char(string):
    return re.sub(r"\\\"", "\"", string)

class SelectorParser:

    def __init__(self, text) -> None:
        self.text = text
        self.call_stack = []
        self.start_index = 0
        self.current_index = 0
    
    def parse(self):
        self.parse_func_chain()
        for item in self.call_stack:
            print(item)
        # print(self.call_stack)
    
    def parse_func_chain(self):
        self.skip_blank()
        self.parse_func_call(0)
        while self.current_index < len(self.text):
            current_char: str = self.text[self.current_index]
            if current_char == ".":
                self.current_index += 1
                self.parse_func_call(len(self.call_stack))
            elif current_char == " ":
                self.skip_blank()
            else:
                break
        return len(self.call_stack)


    def parse_func_call(self, source):
        name = self.parse_func_name()
        params = self.parse_func_param()
        self.call_stack.append((source, name, params))
        return len(self.call_stack)
    
    def parse_string_literal(self):
        result = ""
        self.start_index = self.current_index
        has_escaping = False
        while self.current_index < len(self.text):
            current_char: str = self.text[self.current_index]
            if current_char == "\"":
                if self.current_index != 0 and self.text[self.current_index-1] != "\\":
                    result = self.text[self.start_index: self.current_index]
                    self.current_index += 1
                    if has_escaping:
                        return remove_escaping_char(result)
                    else:
                        return result
                else:
                    has_escaping = True
                    self.current_index += 1
            else:
                self.current_index += 1
        raise RuntimeError("invalid string literal")

    
    def parse_func_param(self):
        params = []
        self.skip_blank()
        while self.current_index < len(self.text):
            current_char: str = self.text[self.current_index]
            if current_char == "\"":
                self.current_index += 1
                param = self.parse_string_literal()
                params.append(param)
            elif current_char == ",":
                self.current_index += 1
                self.skip_blank()
            elif is_alpha(current_char):
                param = self.parse_func_chain()
                params.append(param)
                self.skip_blank()
            elif current_char == ")":
                self.current_index += 1
                return params
            else:
                break
        raise RuntimeError("invalid function param: %s" % self.text[self.start_index: self.current_index])


    def skip_blank(self):
        self.start_index = self.current_index
        while self.current_index < len(self.text) and self.text[self.current_index] == " ":
            self.current_index += 1
            self.start_index = self.current_index


    def parse_func_name(self):
        name = ""
        self.start_index = self.current_index
        while self.current_index < len(self.text):
            current_char: str = self.text[self.current_index]
            if is_alpha(current_char):
                self.current_index += 1
                continue
            elif current_char == "(":
                name = self.text[self.start_index: self.current_index]
                self.current_index += 1
                return name
            elif current_char == " ":
                self.current_index += 1
            else:
                break
        return name
            

SelectorParser(express).parse()
