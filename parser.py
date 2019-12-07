from dataclasses import dataclass
from typing import List
from rply.token import BaseBox
from lexer import lexer
from rply import ParserGenerator


@dataclass
class Block:
    statements: List[str]
    
    
@dataclass
class Statement(BaseBox):
    expression: str
        
    def eval(self):
        return self.expression
        
        
@dataclass
class Number(BaseBox):
    value: float
    
    def eval(self):
        return self.value
    
@dataclass
class BinaryOp(BaseBox):
    left: int
    right: int
    
    
class Add(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()

class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()

class Mul(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()

class Div(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()

pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    [
     'LPAREN', 'RPAREN',
     'PLUS', 'MINUS', 'MUL', 'DIV', 'NAME', 'NUMBER',
     'EQUAL', 'GREATER_EQUAL',
     'LBRACE', 'RBRACE', 'SEMICOLON',
     'IF', 'ELSE', 'PRINT',
     'STRING', 
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV'])
    ]
)

@pg.production('expression : NUMBER')
def expression_number(p):
    # p is a list of the pieces matched by the right hand side of the
    # rule
    return Number(int(p[0].getstr()))


@pg.production('expression : NAME')
def expression_statement(p):
    return Statement(str(p[0].getstr()))


@pg.production('expression : LPAREN expression RPAREN')
def expression_parens(p):
    return p[1]

@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(p):
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == 'PLUS':
        return Add(left, right)
    elif p[1].gettokentype() == 'MINUS':
        return Sub(left, right)
    elif p[1].gettokentype() == 'MUL':
        return Mul(left, right)
    elif p[1].gettokentype() == 'DIV':
        return Div(left, right)
    else:
        raise AssertionError('Oops, this should not be possible!')


@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())
        
parser = pg.build()


value = parser.parse(lexer.lex('variable')).eval()
print(value)
