# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER = 1
MINIUS = '-'
PLUS = '+'
MUTIPLY = '*'
DIVIDE = '/'
MATH_OPERATOR = 2
EOF = 3


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self, error):
        raise Exception(error)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        if current_char == ' ':
            self.pos += 1
            return self.get_next_token()

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            number = 0
            while True:
                if self.pos > len(text) - 1:
                    return Token(INTEGER, number)
                current_char = text[self.pos]
                if current_char.isdigit():
                    number = int(current_char) + number * 10
                    self.pos += 1
                else:
                    return Token(INTEGER, number)

        if current_char == '+' or current_char == '-' or current_char == '*' or current_char == '/':
            token = Token(MATH_OPERATOR, current_char)
            self.pos += 1
            return token

        self.error('Error parsing input')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error('Error parsing input')

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        head = self.current_token
        self.eat(INTEGER)
        result = self.mathOperation(head.value)
        # after the above call the self.current_token is set to
        # EOF token

        return result

    def mathOperation(self, value):
        # we expect the current token to be a '+' token
        op = self.current_token
            
        # at this point INTEGER PLUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectively interpreting client input
        result = value
        if op.type == MATH_OPERATOR:
            self.eat(MATH_OPERATOR)
        
            # we expect the current token to be a single-digit integer
            right = self.current_token
            self.eat(INTEGER)     
        
            if op.value == '+':       
                result = value + right.value
            if op.value == '-':
                result = value - right.value
            if op.value == '*':
                result = value * right.value
            if op.value == '/':
                result = head.value / right.value

            if self.current_token.type == EOF:
                return result
            if self.current_token.type == MATH_OPERATOR:
                return self.mathOperation(result)

            self.error('Error Math parsing')

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()