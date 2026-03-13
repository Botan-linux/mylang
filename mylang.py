#!/usr/bin/env python3
"""
MyLang - Modern Programming Language
Version: 1.0.0

A feature-rich programming language with:
- Variables (let, const, var)
- Functions (fn, arrow functions)
- Classes with inheritance
- Async/await
- Pattern matching
- List/Dict comprehensions
- Decorators
- Error handling (try/catch/throw)
- Module system
- GitHub-based package manager
"""

import os
import sys
import re
import json
import hashlib
import argparse
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union, Tuple
from enum import Enum, auto
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.error
import zipfile
import shutil

# =============================================================================
# CONFIGURATION
# =============================================================================

VERSION = "1.0.0"
MYLANG_DIR = Path.home() / ".mylang"
PACKAGES_DIR = MYLANG_DIR / "packages"
CACHE_DIR = MYLANG_DIR / "cache"
CONFIG_FILE = MYLANG_DIR / "config.json"

# GitHub repository for packages
GITHUB_API = "https://api.github.com"
DEFAULT_PACKAGE_REPO = "mylang-packages"  # Organization or user name

# =============================================================================
# TOKEN TYPES
# =============================================================================

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()
    IDENTIFIER = auto()

    # Keywords
    LET = auto()
    CONST = auto()
    VAR = auto()
    FN = auto()
    RETURN = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    LOOP = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    BREAK = auto()
    CONTINUE = auto()
    CLASS = auto()
    EXTENDS = auto()
    NEW = auto()
    SELF = auto()
    SUPER = auto()
    IMPORT = auto()
    FROM = auto()
    EXPORT = auto()
    ASYNC = auto()
    AWAIT = auto()
    TRY = auto()
    CATCH = auto()
    THROW = auto()
    FINALLY = auto()
    MATCH = auto()
    CASE = auto()
    DEFAULT = auto()
    DECORATOR = auto()
    WITH = auto()
    YIELD = auto()
    LAMBDA = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    POWER = auto()
    FLOOR_DIV = auto()

    # Comparison
    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()

    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()

    # Bitwise
    BIT_AND = auto()
    BIT_OR = auto()
    BIT_XOR = auto()
    BIT_NOT = auto()
    LSHIFT = auto()
    RSHIFT = auto()

    # Assignment
    ASSIGN = auto()
    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    STAR_ASSIGN = auto()
    SLASH_ASSIGN = auto()

    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    SEMICOLON = auto()
    ARROW = auto()
    FAT_ARROW = auto()
    PIPE = auto()
    QUESTION = auto()
    ELLIPSIS = auto()

    # Special
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()

    # Comments
    COMMENT = auto()

# =============================================================================
# TOKEN
# =============================================================================

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    indent: int = 0

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.column})"

# =============================================================================
# LEXER
# =============================================================================

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer Error at L{line}:C{column}: {message}")

class Lexer:
    KEYWORDS = {
        'let': TokenType.LET,
        'const': TokenType.CONST,
        'var': TokenType.VAR,
        'fn': TokenType.FN,
        'return': TokenType.RETURN,
        'if': TokenType.IF,
        'elif': TokenType.ELIF,
        'else': TokenType.ELSE,
        'loop': TokenType.LOOP,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'in': TokenType.IN,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
        'class': TokenType.CLASS,
        'extends': TokenType.EXTENDS,
        'new': TokenType.NEW,
        'self': TokenType.SELF,
        'super': TokenType.SUPER,
        'import': TokenType.IMPORT,
        'from': TokenType.FROM,
        'export': TokenType.EXPORT,
        'async': TokenType.ASYNC,
        'await': TokenType.AWAIT,
        'try': TokenType.TRY,
        'catch': TokenType.CATCH,
        'throw': TokenType.THROW,
        'finally': TokenType.FINALLY,
        'match': TokenType.MATCH,
        'case': TokenType.CASE,
        'default': TokenType.DEFAULT,
        'decorator': TokenType.DECORATOR,
        'with': TokenType.WITH,
        'yield': TokenType.YIELD,
        'lambda': TokenType.LAMBDA,
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
        'none': TokenType.NONE,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        self.tokens: List[Token] = []
        self.at_line_start = True
        self.brace_depth = 0  # Track brace nesting to disable indent tracking inside braces

    def error(self, message: str):
        raise LexerError(message, self.line, self.column)

    def peek(self, offset: int = 0) -> str:
        pos = self.pos + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]

    def advance(self) -> str:
        char = self.peek()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def skip_whitespace(self):
        while self.peek() in ' \t\r':
            self.advance()

    def skip_comment(self):
        if self.peek() == '#':
            while self.peek() not in '\n\0':
                self.advance()

    def read_string(self, quote: str) -> str:
        self.advance()  # Skip opening quote
        result = []
        while self.peek() != quote and self.peek() != '\0':
            if self.peek() == '\\':
                self.advance()
                escape = self.advance()
                escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                result.append(escape_map.get(escape, escape))
            else:
                result.append(self.advance())
        if self.peek() == '\0':
            self.error("Unterminated string")
        self.advance()  # Skip closing quote
        return ''.join(result)

    def read_number(self) -> Union[int, float]:
        result = []
        is_float = False

        while self.peek().isdigit() or self.peek() == '_':
            if self.peek() == '_':
                self.advance()
                continue
            result.append(self.advance())

        if self.peek() == '.' and self.peek(1).isdigit():
            is_float = True
            result.append(self.advance())  # .
            while self.peek().isdigit() or self.peek() == '_':
                if self.peek() == '_':
                    self.advance()
                    continue
                result.append(self.advance())

        # Scientific notation
        if self.peek() in 'eE':
            is_float = True
            result.append(self.advance())
            if self.peek() in '+-':
                result.append(self.advance())
            while self.peek().isdigit():
                result.append(self.advance())

        num_str = ''.join(result)
        return float(num_str) if is_float else int(num_str)

    def read_identifier(self) -> str:
        result = []
        while self.peek().isalnum() or self.peek() == '_':
            result.append(self.advance())
        return ''.join(result)

    def get_indent(self) -> int:
        indent = 0
        while self.peek() in ' \t':
            if self.peek() == '\t':
                indent += 4
            else:
                indent += 1
            self.advance()
        return indent

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            # Handle line start (indentation)
            if self.at_line_start:
                self.at_line_start = False
                indent = self.get_indent()

                # Skip empty lines and comments
                if self.peek() in '\n#':
                    self.skip_comment()
                    if self.peek() == '\n':
                        self.advance()
                        self.at_line_start = True
                    continue

                # Emit INDENT/DEDENT tokens ONLY if not inside braces
                if self.brace_depth == 0:
                    if indent > self.indent_stack[-1]:
                        self.indent_stack.append(indent)
                        self.tokens.append(Token(TokenType.INDENT, indent, self.line, 1, indent))
                    else:
                        while indent < self.indent_stack[-1]:
                            self.indent_stack.pop()
                            self.tokens.append(Token(TokenType.DEDENT, indent, self.line, 1, indent))

            # Skip whitespace (not at line start)
            self.skip_whitespace()

            # Comments
            if self.peek() == '#':
                self.skip_comment()
                continue

            # Newline
            if self.peek() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                self.at_line_start = True
                continue

            # EOF
            if self.peek() == '\0':
                break

            line, col = self.line, self.column
            char = self.peek()

            # String literals
            if char in '"\'':
                value = self.read_string(char)
                self.tokens.append(Token(TokenType.STRING, value, line, col))
                continue

            # Numbers
            if char.isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, col))
                continue

            # Identifiers and keywords
            if char.isalpha() or char == '_':
                value = self.read_identifier()
                token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
                if token_type == TokenType.BOOLEAN:
                    self.tokens.append(Token(TokenType.BOOLEAN, value == 'true', line, col))
                elif token_type == TokenType.NONE:
                    self.tokens.append(Token(TokenType.NONE, None, line, col))
                else:
                    self.tokens.append(Token(token_type, value, line, col))
                continue

            # Multi-character operators
            two_char = self.peek() + self.peek(1)
            three_char = two_char + self.peek(2)

            if three_char == '...':
                self.advance(); self.advance(); self.advance()
                self.tokens.append(Token(TokenType.ELLIPSIS, '...', line, col))
                continue

            operators = {
                '**': TokenType.POWER,
                '//': TokenType.FLOOR_DIV,
                '==': TokenType.EQ,
                '!=': TokenType.NE,
                '<=': TokenType.LE,
                '>=': TokenType.GE,
                '+=': TokenType.PLUS_ASSIGN,
                '-=': TokenType.MINUS_ASSIGN,
                '*=': TokenType.STAR_ASSIGN,
                '/=': TokenType.SLASH_ASSIGN,
                '->': TokenType.ARROW,
                '=>': TokenType.FAT_ARROW,
                '<<': TokenType.LSHIFT,
                '>>': TokenType.RSHIFT,
            }

            if two_char in operators:
                self.advance(); self.advance()
                self.tokens.append(Token(operators[two_char], two_char, line, col))
                continue

            # Single character operators
            single_ops = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.STAR,
                '/': TokenType.SLASH,
                '%': TokenType.PERCENT,
                '=': TokenType.ASSIGN,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                ':': TokenType.COLON,
                ';': TokenType.SEMICOLON,
                '|': TokenType.PIPE,
                '?': TokenType.QUESTION,
                '&': TokenType.BIT_AND,
                '^': TokenType.BIT_XOR,
                '~': TokenType.BIT_NOT,
            }

            if char in single_ops:
                self.advance()
                # Track brace depth
                if char == '{':
                    self.brace_depth += 1
                elif char == '}':
                    self.brace_depth -= 1
                self.tokens.append(Token(single_ops[char], char, line, col))
                continue

            self.error(f"Unexpected character: {char!r}")

        # Emit remaining DEDENT tokens
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, 0, self.line, 1, 0))

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

# =============================================================================
# AST NODES
# =============================================================================

@dataclass
class ASTNode:
    line: int = 0
    column: int = 0

@dataclass
class Program(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)

# Literals
@dataclass
class NumberLiteral(ASTNode):
    value: Union[int, float] = 0

@dataclass
class StringLiteral(ASTNode):
    value: str = ""

@dataclass
class BooleanLiteral(ASTNode):
    value: bool = False

@dataclass
class NoneLiteral(ASTNode):
    pass

@dataclass
class ListLiteral(ASTNode):
    elements: List[ASTNode] = field(default_factory=list)

@dataclass
class DictLiteral(ASTNode):
    pairs: List[Tuple[ASTNode, ASTNode]] = field(default_factory=list)

@dataclass
class Identifier(ASTNode):
    name: str = ""

# Expressions
@dataclass
class BinaryOp(ASTNode):
    left: ASTNode = None
    operator: str = ""
    right: ASTNode = None

@dataclass
class UnaryOp(ASTNode):
    operator: str = ""
    operand: ASTNode = None

@dataclass
class TernaryOp(ASTNode):
    condition: ASTNode = None
    true_expr: ASTNode = None
    false_expr: ASTNode = None

@dataclass
class CallExpression(ASTNode):
    callee: ASTNode = None
    arguments: List[ASTNode] = field(default_factory=list)

@dataclass
class MemberExpression(ASTNode):
    obj: ASTNode = None
    prop: ASTNode = None
    computed: bool = False

@dataclass
class AssignmentExpression(ASTNode):
    target: ASTNode = None
    operator: str = "="
    value: ASTNode = None

@dataclass
class SpreadExpression(ASTNode):
    argument: ASTNode = None

@dataclass
class LambdaExpression(ASTNode):
    params: List[str] = field(default_factory=list)
    body: ASTNode = None
    expression: bool = True

# Statements
@dataclass
class VariableDeclaration(ASTNode):
    kind: str = "let"  # let, const, var
    name: str = ""
    value: ASTNode = None
    type_annotation: Optional[str] = None

@dataclass
class FunctionDeclaration(ASTNode):
    name: str = ""
    params: List[Tuple[str, Optional[str]]] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    return_type: Optional[str] = None
    is_async: bool = False
    decorators: List[ASTNode] = field(default_factory=list)

@dataclass
class ReturnStatement(ASTNode):
    value: ASTNode = None

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode = None
    consequent: List[ASTNode] = field(default_factory=list)
    elif_clauses: List[Tuple[ASTNode, List[ASTNode]]] = field(default_factory=list)
    alternate: List[ASTNode] = field(default_factory=list)

@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class ForStatement(ASTNode):
    variable: str = ""
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class LoopStatement(ASTNode):
    variable: Optional[str] = None
    iterable: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class BreakStatement(ASTNode):
    pass

@dataclass
class ContinueStatement(ASTNode):
    pass

# Class
@dataclass
class ClassDeclaration(ASTNode):
    name: str = ""
    extends: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)
    decorators: List[ASTNode] = field(default_factory=list)

@dataclass
class PropertyDeclaration(ASTNode):
    name: str = ""
    value: ASTNode = None
    is_static: bool = False

@dataclass
class MethodDeclaration(ASTNode):
    name: str = ""
    params: List[Tuple[str, Optional[str]]] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    is_static: bool = False
    is_async: bool = False

# Error Handling
@dataclass
class TryStatement(ASTNode):
    try_block: List[ASTNode] = field(default_factory=list)
    catch_var: Optional[str] = None
    catch_block: List[ASTNode] = field(default_factory=list)
    finally_block: List[ASTNode] = field(default_factory=list)

@dataclass
class ThrowStatement(ASTNode):
    value: ASTNode = None

# Pattern Matching
@dataclass
class MatchStatement(ASTNode):
    subject: ASTNode = None
    cases: List[Tuple[ASTNode, List[ASTNode]]] = field(default_factory=list)
    default_case: Optional[List[ASTNode]] = None

# Modules
@dataclass
class ImportStatement(ASTNode):
    module: str = ""
    names: List[Tuple[str, Optional[str]]] = field(default_factory=list)  # (name, alias)
    is_all: bool = False

@dataclass
class ExportStatement(ASTNode):
    declaration: ASTNode = None
    names: List[str] = field(default_factory=list)

# Decorators
@dataclass
class DecoratorExpression(ASTNode):
    name: str = ""
    arguments: List[ASTNode] = field(default_factory=list)

# Comprehensions
@dataclass
class ListComprehension(ASTNode):
    expression: ASTNode = None
    variable: str = ""
    iterable: ASTNode = None
    condition: Optional[ASTNode] = None

@dataclass
class DictComprehension(ASTNode):
    key_expr: ASTNode = None
    value_expr: ASTNode = None
    variable: str = ""
    iterable: ASTNode = None
    condition: Optional[ASTNode] = None

# With statement
@dataclass
class WithStatement(ASTNode):
    expression: ASTNode = None
    variable: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)

# Expression Statement
@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode = None

# =============================================================================
# PARSER
# =============================================================================

class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Parse Error at L{token.line}:C{token.column}: {message}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_decorator: List[DecoratorExpression] = []

    def peek(self, offset: int = 0) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[pos]

    def advance(self) -> Token:
        token = self.peek()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token

    def check(self, *types: TokenType) -> bool:
        return self.peek().type in types

    def match(self, *types: TokenType) -> Optional[Token]:
        if self.check(*types):
            return self.advance()
        return None

    def expect(self, type: TokenType, message: str = None) -> Token:
        if self.check(type):
            return self.advance()
        token = self.peek()
        msg = message or f"Expected {type.name}, got {token.type.name}"
        raise ParseError(msg, token)

    def error(self, message: str):
        raise ParseError(message, self.peek())

    # Main parse function
    def parse(self) -> Program:
        statements = []
        while not self.check(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements=statements, line=1, column=1)

    # Statement parsing
    def parse_statement(self) -> Optional[ASTNode]:
        # Skip newlines
        while self.match(TokenType.NEWLINE):
            pass

        # Skip INDENT/DEDENT at statement level
        self.match(TokenType.INDENT, TokenType.DEDENT)

        if self.check(TokenType.EOF):
            return None

        # Return None for closing braces (handled by parse_block)
        if self.check(TokenType.RBRACE):
            return None

        # Decorators
        if self.check(TokenType.DECORATOR) or (self.check(TokenType.IDENTIFIER) and self.peek().value == '@'):
            return self.parse_decorator_statement()

        # Variable declarations
        if self.check(TokenType.LET, TokenType.CONST, TokenType.VAR):
            return self.parse_variable_declaration()

        # Function declaration
        if self.check(TokenType.FN):
            return self.parse_function_declaration()

        # Class declaration
        if self.check(TokenType.CLASS):
            return self.parse_class_declaration()

        # If statement
        if self.check(TokenType.IF):
            return self.parse_if_statement()

        # While statement
        if self.check(TokenType.WHILE):
            return self.parse_while_statement()

        # For statement
        if self.check(TokenType.FOR):
            return self.parse_for_statement()

        # Loop statement
        if self.check(TokenType.LOOP):
            return self.parse_loop_statement()

        # Break/Continue
        if self.check(TokenType.BREAK):
            self.advance()
            return BreakStatement(line=self.peek().line)
        if self.check(TokenType.CONTINUE):
            self.advance()
            return ContinueStatement(line=self.peek().line)

        # Return statement
        if self.check(TokenType.RETURN):
            return self.parse_return_statement()

        # Try statement
        if self.check(TokenType.TRY):
            return self.parse_try_statement()

        # Throw statement
        if self.check(TokenType.THROW):
            return self.parse_throw_statement()

        # Match statement
        if self.check(TokenType.MATCH):
            return self.parse_match_statement()

        # Import statement
        if self.check(TokenType.IMPORT):
            return self.parse_import_statement()

        # Export statement
        if self.check(TokenType.EXPORT):
            return self.parse_export_statement()

        # With statement
        if self.check(TokenType.WITH):
            return self.parse_with_statement()

        # Expression statement
        return self.parse_expression_statement()

    def parse_decorator_statement(self) -> DecoratorExpression:
        decorators = []
        while self.check(TokenType.DECORATOR) or (self.check(TokenType.IDENTIFIER) and self.peek().value == '@'):
            if self.peek().value == '@':
                self.advance()
            else:
                self.advance()
            name = self.expect(TokenType.IDENTIFIER, "Expected decorator name").value
            args = []
            if self.match(TokenType.LPAREN):
                if not self.check(TokenType.RPAREN):
                    args = self.parse_argument_list()
                self.expect(TokenType.RPAREN)
            decorators.append(DecoratorExpression(name=name, arguments=args))

        self.current_decorator = decorators

        # Parse the decorated statement
        stmt = self.parse_statement()
        if stmt:
            if hasattr(stmt, 'decorators'):
                stmt.decorators = decorators
            self.current_decorator = []
        return stmt

    def parse_variable_declaration(self) -> VariableDeclaration:
        kind = self.advance().value  # let, const, var
        name_token = self.expect(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value

        type_annotation = None
        if self.match(TokenType.COLON):
            type_annotation = self.parse_type_annotation()

        value = None
        if self.match(TokenType.ASSIGN):
            value = self.parse_expression()

        return VariableDeclaration(
            kind=kind, name=name, value=value,
            type_annotation=type_annotation,
            line=name_token.line, column=name_token.column
        )

    def parse_function_declaration(self) -> FunctionDeclaration:
        fn_token = self.advance()

        is_async = False
        if self.check(TokenType.ASYNC):
            is_async = True
            self.advance()

        name = ""
        if self.check(TokenType.IDENTIFIER):
            name = self.advance().value

        self.expect(TokenType.LPAREN, "Expected '(' after function name")
        params = self.parse_parameter_list()
        self.expect(TokenType.RPAREN, "Expected ')' after parameters")

        return_type = None
        if self.match(TokenType.ARROW):
            return_type = self.parse_type_annotation()

        body = self.parse_block()

        return FunctionDeclaration(
            name=name, params=params, body=body,
            return_type=return_type, is_async=is_async,
            decorators=self.current_decorator.copy(),
            line=fn_token.line, column=fn_token.column
        )

    def parse_parameter_list(self) -> List[Tuple[str, Optional[str]]]:
        params = []
        while not self.check(TokenType.RPAREN):
            name = self.expect(TokenType.IDENTIFIER, "Expected parameter name").value
            type_annotation = None
            if self.match(TokenType.COLON):
                type_annotation = self.parse_type_annotation()
            params.append((name, type_annotation))
            if not self.match(TokenType.COMMA):
                break
        return params

    def parse_type_annotation(self) -> str:
        types = []
        while self.check(TokenType.IDENTIFIER, TokenType.LBRACKET):
            if self.match(TokenType.LBRACKET):
                types.append('[')
                while not self.check(TokenType.RBRACKET):
                    types.append(self.parse_type_annotation())
                    if not self.match(TokenType.COMMA):
                        break
                self.expect(TokenType.RBRACKET)
                types.append(']')
            else:
                types.append(self.advance().value)
            if self.match(TokenType.PIPE):
                types.append('|')
        return ' '.join(str(t) for t in types)

    def parse_block(self) -> List[ASTNode]:
        statements = []

        # Handle brace-based block { ... }
        if self.match(TokenType.LBRACE):
            while not self.check(TokenType.RBRACE, TokenType.EOF):
                # Skip newlines inside braces
                if self.match(TokenType.NEWLINE):
                    continue
                # Check if we're stuck
                if self.check(TokenType.RBRACE):
                    break
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
                elif self.check(TokenType.RBRACE):
                    break
            self.expect(TokenType.RBRACE, "Expected '}' to close block")
            return statements

        # Handle INDENT-based block
        if self.match(TokenType.INDENT):
            while not self.check(TokenType.DEDENT, TokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            self.expect(TokenType.DEDENT, "Expected dedent")
            return statements

        # Single statement block (no braces, no indent)
        stmt = self.parse_statement()
        if stmt:
            statements.append(stmt)

        return statements

    def parse_class_declaration(self) -> ClassDeclaration:
        class_token = self.advance()
        name = self.expect(TokenType.IDENTIFIER, "Expected class name").value

        extends = None
        if self.check(TokenType.EXTENDS):
            self.advance()
            extends = self.expect(TokenType.IDENTIFIER, "Expected parent class name").value

        body = self.parse_class_body()

        return ClassDeclaration(
            name=name, extends=extends, body=body,
            decorators=self.current_decorator.copy(),
            line=class_token.line, column=class_token.column
        )

    def parse_class_body(self) -> List[ASTNode]:
        members = []

        # Handle brace-based class body { ... }
        if self.match(TokenType.LBRACE):
            while not self.check(TokenType.RBRACE, TokenType.EOF):
                if self.match(TokenType.NEWLINE):
                    continue

                # Static modifier
                is_static = False
                if self.check(TokenType.IDENTIFIER) and self.peek().value == 'static':
                    is_static = True
                    self.advance()

                # Method (fn keyword)
                if self.check(TokenType.FN):
                    method = self.parse_method_declaration(is_static=is_static)
                    members.append(method)
                # Property or method (identifier)
                elif self.check(TokenType.IDENTIFIER):
                    name = self.peek().value

                    if self.peek(1).type == TokenType.LPAREN:
                        # Method
                        method = self.parse_method_declaration(name, is_static)
                        members.append(method)
                    else:
                        # Property
                        self.advance()
                        value = None
                        if self.match(TokenType.ASSIGN):
                            value = self.parse_expression()
                        members.append(PropertyDeclaration(
                            name=name, value=value, is_static=is_static
                        ))
                else:
                    # Skip unknown tokens
                    self.advance()

                self.match(TokenType.NEWLINE)
            self.expect(TokenType.RBRACE)
            return members

        # Handle INDENT-based class body
        if self.match(TokenType.INDENT):
            while not self.check(TokenType.DEDENT, TokenType.EOF):
                self.match(TokenType.NEWLINE)

                # Static modifier
                is_static = False
                if self.check(TokenType.IDENTIFIER) and self.peek().value == 'static':
                    is_static = True
                    self.advance()

                # Property or method
                if self.check(TokenType.IDENTIFIER):
                    name = self.peek().value

                    if self.peek(1).type == TokenType.LPAREN:
                        # Method
                        method = self.parse_method_declaration(name, is_static)
                        members.append(method)
                    else:
                        # Property
                        self.advance()
                        value = None
                        if self.match(TokenType.ASSIGN):
                            value = self.parse_expression()
                        members.append(PropertyDeclaration(
                            name=name, value=value, is_static=is_static
                        ))

                self.match(TokenType.NEWLINE)
            self.expect(TokenType.DEDENT)

        return members

    def parse_method_declaration(self, name: str = None, is_static: bool = False) -> MethodDeclaration:
        # If name not provided, parse from token stream (fn keyword case)
        if name is None:
            self.expect(TokenType.FN)  # Consume 'fn'
            name = self.expect(TokenType.IDENTIFIER, "Expected method name").value

        is_async = False
        if self.check(TokenType.ASYNC):
            is_async = True
            self.advance()

        self.expect(TokenType.LPAREN)
        params = self.parse_parameter_list()
        self.expect(TokenType.RPAREN)

        body = self.parse_block()

        return MethodDeclaration(
            name=name, params=params, body=body,
            is_static=is_static, is_async=is_async
        )

    def parse_if_statement(self) -> IfStatement:
        if_token = self.advance()
        condition = self.parse_expression()
        consequent = self.parse_block()

        elif_clauses = []
        while self.check(TokenType.ELIF):
            self.advance()
            elif_cond = self.parse_expression()
            elif_body = self.parse_block()
            elif_clauses.append((elif_cond, elif_body))

        alternate = []
        if self.check(TokenType.ELSE):
            self.advance()
            alternate = self.parse_block()

        return IfStatement(
            condition=condition, consequent=consequent,
            elif_clauses=elif_clauses, alternate=alternate,
            line=if_token.line, column=if_token.column
        )

    def parse_while_statement(self) -> WhileStatement:
        while_token = self.advance()
        condition = self.parse_expression()
        body = self.parse_block()

        return WhileStatement(
            condition=condition, body=body,
            line=while_token.line, column=while_token.column
        )

    def parse_for_statement(self) -> ForStatement:
        for_token = self.advance()
        variable = self.expect(TokenType.IDENTIFIER, "Expected variable name").value
        self.expect(TokenType.IN, "Expected 'in'")
        iterable = self.parse_expression()
        body = self.parse_block()

        return ForStatement(
            variable=variable, iterable=iterable, body=body,
            line=for_token.line, column=for_token.column
        )

    def parse_loop_statement(self) -> LoopStatement:
        loop_token = self.advance()

        variable = None
        iterable = None

        if self.check(TokenType.IDENTIFIER):
            variable = self.advance().value
            if self.check(TokenType.IN):
                self.advance()
                iterable = self.parse_expression()

        body = self.parse_block()

        return LoopStatement(
            variable=variable, iterable=iterable, body=body,
            line=loop_token.line, column=loop_token.column
        )

    def parse_return_statement(self) -> ReturnStatement:
        return_token = self.advance()
        value = None
        if not self.check(TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT):
            value = self.parse_expression()
        return ReturnStatement(value=value, line=return_token.line)

    def parse_try_statement(self) -> TryStatement:
        try_token = self.advance()
        try_block = self.parse_block()

        # Skip newlines between try block and catch
        while self.match(TokenType.NEWLINE):
            pass

        catch_var = None
        catch_block = []
        if self.check(TokenType.CATCH):
            self.advance()
            # Check for catch variable in parentheses: catch(e) or catch e
            if self.match(TokenType.LPAREN):
                if self.check(TokenType.IDENTIFIER):
                    catch_var = self.advance().value
                self.expect(TokenType.RPAREN)
            elif self.check(TokenType.IDENTIFIER):
                catch_var = self.advance().value
            catch_block = self.parse_block()

        # Skip newlines between catch block and finally
        while self.match(TokenType.NEWLINE):
            pass

        finally_block = []
        if self.check(TokenType.FINALLY):
            self.advance()
            finally_block = self.parse_block()

        return TryStatement(
            try_block=try_block, catch_var=catch_var,
            catch_block=catch_block, finally_block=finally_block,
            line=try_token.line
        )

    def parse_throw_statement(self) -> ThrowStatement:
        throw_token = self.advance()
        value = self.parse_expression()
        return ThrowStatement(value=value, line=throw_token.line)

    def parse_match_statement(self) -> MatchStatement:
        match_token = self.advance()
        subject = self.parse_expression()

        cases = []
        default_case = None

        if self.match(TokenType.INDENT):
            while not self.check(TokenType.DEDENT, TokenType.EOF):
                self.match(TokenType.NEWLINE)

                if self.check(TokenType.CASE):
                    self.advance()
                    pattern = self.parse_expression()
                    body = self.parse_block()
                    cases.append((pattern, body))
                elif self.check(TokenType.DEFAULT):
                    self.advance()
                    default_case = self.parse_block()

                self.match(TokenType.NEWLINE)
            self.expect(TokenType.DEDENT)

        return MatchStatement(
            subject=subject, cases=cases, default_case=default_case,
            line=match_token.line
        )

    def parse_import_statement(self) -> ImportStatement:
        import_token = self.advance()

        # from X import Y
        if self.check(TokenType.IDENTIFIER) and self.peek().value != 'from':
            # import X
            module = self.advance().value
            return ImportStatement(module=module, is_all=True, line=import_token.line)

        # from X import ...
        if self.check(TokenType.FROM):
            self.advance()

        module = ""
        if self.check(TokenType.STRING):
            module = self.advance().value
        elif self.check(TokenType.IDENTIFIER):
            module = self.advance().value

        names = []
        is_all = False

        if self.check(TokenType.IMPORT):
            self.advance()

            if self.match(TokenType.STAR):
                is_all = True
            else:
                self.expect(TokenType.LPAREN)
                while not self.check(TokenType.RPAREN):
                    name = self.expect(TokenType.IDENTIFIER).value
                    alias = None
                    if self.check(TokenType.AS):
                        self.advance()
                        alias = self.expect(TokenType.IDENTIFIER).value
                    names.append((name, alias))
                    if not self.match(TokenType.COMMA):
                        break
                self.expect(TokenType.RPAREN)

        return ImportStatement(module=module, names=names, is_all=is_all, line=import_token.line)

    def parse_export_statement(self) -> ExportStatement:
        export_token = self.advance()
        declaration = self.parse_statement()
        return ExportStatement(declaration=declaration, line=export_token.line)

    def parse_with_statement(self) -> WithStatement:
        with_token = self.advance()
        expression = self.parse_expression()

        variable = None
        if self.check(TokenType.AS):
            self.advance()
            variable = self.expect(TokenType.IDENTIFIER).value

        body = self.parse_block()

        return WithStatement(
            expression=expression, variable=variable, body=body,
            line=with_token.line
        )

    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        return ExpressionStatement(expression=expr, line=expr.line if hasattr(expr, 'line') else 0)

    # Expression parsing (Pratt parser)
    def parse_expression(self) -> ASTNode:
        return self.parse_assignment()

    def parse_assignment(self) -> ASTNode:
        expr = self.parse_ternary()

        if self.check(TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
                      TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN):
            op = self.advance().value
            value = self.parse_assignment()
            return AssignmentExpression(
                target=expr, operator=op, value=value,
                line=expr.line if hasattr(expr, 'line') else 0
            )

        return expr

    def parse_ternary(self) -> ASTNode:
        condition = self.parse_or()

        if self.match(TokenType.QUESTION):
            true_expr = self.parse_expression()
            self.expect(TokenType.COLON, "Expected ':' in ternary expression")
            false_expr = self.parse_ternary()
            return TernaryOp(
                condition=condition, true_expr=true_expr, false_expr=false_expr,
                line=condition.line if hasattr(condition, 'line') else 0
            )

        return condition

    def parse_or(self) -> ASTNode:
        left = self.parse_and()
        while self.match(TokenType.OR):
            right = self.parse_and()
            left = BinaryOp(
                left=left, operator='or', right=right,
                line=left.line if hasattr(left, 'line') else 0
            )
        return left

    def parse_and(self) -> ASTNode:
        left = self.parse_equality()
        while self.match(TokenType.AND):
            right = self.parse_equality()
            left = BinaryOp(
                left=left, operator='and', right=right,
                line=left.line if hasattr(left, 'line') else 0
            )
        return left

    def parse_equality(self) -> ASTNode:
        left = self.parse_comparison()
        while self.check(TokenType.EQ, TokenType.NE):
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryOp(
                left=left, operator=op, right=right,
                line=left.line if hasattr(left, 'line') else 0
            )
        return left

    def parse_comparison(self) -> ASTNode:
        left = self.parse_bitwise()
        while self.check(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE, TokenType.IN):
            op = self.advance().value
            right = self.parse_bitwise()
            left = BinaryOp(
                left=left, operator=op, right=right,
                line=left.line if hasattr(left, 'line') else 0
            )
        return left

    def parse_bitwise(self) -> ASTNode:
        left = self.parse_term()
        while self.check(TokenType.BIT_AND, TokenType.BIT_OR, TokenType.BIT_XOR,
                         TokenType.LSHIFT, TokenType.RSHIFT):
            op = self.advance().value
            right = self.parse_term()
            left = BinaryOp(
                left=left, operator=op, right=right,
                line=left.line if hasattr(left, 'line') else 0
            )
        return left

    def parse_term(self) -> ASTNode:
        left = self.parse_factor()
        while self.check(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_factor()
            left = BinaryOp(
                left=left, operator=op, right=right,
                line=left.line if hasattr(left, 'line') else 0
            )
        return left

    def parse_factor(self) -> ASTNode:
        left = self.parse_power()
        while self.check(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT, TokenType.FLOOR_DIV):
            op = self.advance().value
            right = self.parse_power()
            left = BinaryOp(
                left=left, operator=op, right=right,
                line=left.line if hasattr(left, 'line') else 0
            )
        return left

    def parse_power(self) -> ASTNode:
        left = self.parse_unary()
        if self.match(TokenType.POWER):
            right = self.parse_power()  # Right associative
            return BinaryOp(
                left=left, operator='**', right=right,
                line=left.line if hasattr(left, 'line') else 0
            )
        return left

    def parse_unary(self) -> ASTNode:
        if self.check(TokenType.MINUS, TokenType.NOT, TokenType.BIT_NOT):
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(
                operator=op, operand=operand,
                line=operand.line if hasattr(operand, 'line') else 0
            )
        return self.parse_postfix()

    def parse_postfix(self) -> ASTNode:
        expr = self.parse_primary()

        while True:
            # Function call
            if self.match(TokenType.LPAREN):
                args = self.parse_argument_list()
                self.expect(TokenType.RPAREN)
                expr = CallExpression(
                    callee=expr, arguments=args,
                    line=expr.line if hasattr(expr, 'line') else 0
                )
            # Member access
            elif self.match(TokenType.DOT):
                prop = self.expect(TokenType.IDENTIFIER, "Expected property name")
                expr = MemberExpression(
                    obj=expr, prop=StringLiteral(value=prop.value),
                    computed=False, line=expr.line if hasattr(expr, 'line') else 0
                )
            # Computed member
            elif self.match(TokenType.LBRACKET):
                prop = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = MemberExpression(
                    obj=expr, prop=prop, computed=True,
                    line=expr.line if hasattr(expr, 'line') else 0
                )
            else:
                break

        return expr

    def parse_primary(self) -> ASTNode:
        token = self.peek()

        # Literals
        if self.match(TokenType.NUMBER):
            return NumberLiteral(value=token.value, line=token.line, column=token.column)

        if self.match(TokenType.STRING):
            return StringLiteral(value=token.value, line=token.line, column=token.column)

        if self.match(TokenType.BOOLEAN):
            return BooleanLiteral(value=token.value, line=token.line, column=token.column)

        if self.match(TokenType.NONE):
            return NoneLiteral(line=token.line, column=token.column)

        # Self / Super
        if self.match(TokenType.SELF):
            return Identifier(name='self', line=token.line, column=token.column)

        if self.match(TokenType.SUPER):
            return Identifier(name='super', line=token.line, column=token.column)

        # Identifier
        if self.match(TokenType.IDENTIFIER):
            return Identifier(name=token.value, line=token.line, column=token.column)

        # Parenthesized expression or tuple
        if self.match(TokenType.LPAREN):
            if self.check(TokenType.RPAREN):
                self.expect(TokenType.RPAREN)
                return NoneLiteral(line=token.line)

            expr = self.parse_expression()

            # Tuple or grouped expression
            if self.match(TokenType.COMMA):
                elements = [expr]
                while not self.check(TokenType.RPAREN):
                    elements.append(self.parse_expression())
                    if not self.match(TokenType.COMMA):
                        break
                self.expect(TokenType.RPAREN)
                return ListLiteral(elements=elements, line=token.line)

            self.expect(TokenType.RPAREN)
            return expr

        # List literal
        if self.match(TokenType.LBRACKET):
            return self.parse_list_literal(token)

        # Dict literal
        if self.match(TokenType.LBRACE):
            return self.parse_dict_literal(token)

        # Lambda expression
        if self.match(TokenType.LAMBDA):
            return self.parse_lambda(token)

        # Spread expression
        if self.match(TokenType.ELLIPSIS):
            expr = self.parse_postfix()
            return SpreadExpression(argument=expr, line=token.line)

        # Await expression
        if self.match(TokenType.AWAIT):
            expr = self.parse_postfix()
            return UnaryOp(operator='await', operand=expr, line=token.line)

        self.error(f"Unexpected token: {token.type.name}")

    def parse_list_literal(self, start_token: Token) -> ASTNode:
        elements = []

        # Check for list comprehension
        if not self.check(TokenType.RBRACKET):
            first = self.parse_expression()

            if self.check(TokenType.FOR):
                # List comprehension
                self.advance()
                variable = self.expect(TokenType.IDENTIFIER).value
                self.expect(TokenType.IN)
                iterable = self.parse_expression()
                condition = None
                if self.check(TokenType.IF):
                    self.advance()
                    condition = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                return ListComprehension(
                    expression=first, variable=variable,
                    iterable=iterable, condition=condition,
                    line=start_token.line
                )

            elements.append(first)
            while self.match(TokenType.COMMA):
                if self.check(TokenType.RBRACKET):
                    break
                elements.append(self.parse_expression())

        self.expect(TokenType.RBRACKET)
        return ListLiteral(elements=elements, line=start_token.line)

    def parse_dict_literal(self, start_token: Token) -> ASTNode:
        pairs = []

        if not self.check(TokenType.RBRACE):
            # Check for dict comprehension
            first_key = self.parse_expression()

            if self.check(TokenType.FOR):
                # Dict comprehension
                self.advance()
                self.expect(TokenType.COLON)
                first_value = self.parse_expression()
                variable = self.expect(TokenType.IDENTIFIER).value
                self.expect(TokenType.IN)
                iterable = self.parse_expression()
                condition = None
                if self.check(TokenType.IF):
                    self.advance()
                    condition = self.parse_expression()
                self.expect(TokenType.RBRACE)
                return DictComprehension(
                    key_expr=first_key, value_expr=first_value,
                    variable=variable, iterable=iterable, condition=condition,
                    line=start_token.line
                )

            self.expect(TokenType.COLON)
            first_value = self.parse_expression()
            pairs.append((first_key, first_value))

            while self.match(TokenType.COMMA):
                if self.check(TokenType.RBRACE):
                    break
                key = self.parse_expression()
                self.expect(TokenType.COLON)
                value = self.parse_expression()
                pairs.append((key, value))

        self.expect(TokenType.RBRACE)
        return DictLiteral(pairs=pairs, line=start_token.line)

    def parse_lambda(self, start_token: Token) -> ASTNode:
        params = []

        if not self.check(TokenType.ARROW, TokenType.FAT_ARROW):
            if self.check(TokenType.IDENTIFIER):
                params.append(self.advance().value)
                while self.match(TokenType.COMMA):
                    params.append(self.expect(TokenType.IDENTIFIER).value)
            elif self.match(TokenType.LPAREN):
                if not self.check(TokenType.RPAREN):
                    params.append(self.expect(TokenType.IDENTIFIER).value)
                    while self.match(TokenType.COMMA):
                        params.append(self.expect(TokenType.IDENTIFIER).value)
                self.expect(TokenType.RPAREN)

        if self.check(TokenType.ARROW):
            self.advance()
        elif self.check(TokenType.FAT_ARROW):
            self.advance()

        body = self.parse_expression()
        return LambdaExpression(params=params, body=body, expression=True, line=start_token.line)

    def parse_argument_list(self) -> List[ASTNode]:
        args = []
        while not self.check(TokenType.RPAREN, TokenType.EOF):
            args.append(self.parse_expression())
            if not self.match(TokenType.COMMA):
                break
        return args

# =============================================================================
# RUNTIME VALUES
# =============================================================================

class MyLangError(Exception):
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Runtime Error at L{line}:C{column}: {message}")

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

@dataclass
class MyLangFunction:
    name: str
    params: List[str]
    body: List[ASTNode]
    closure: Dict[str, Any]
    is_async: bool = False

    def __repr__(self):
        return f"<function {self.name}>"

@dataclass
class MyLangClass:
    name: str
    extends: Optional[str]
    methods: Dict[str, Any]
    properties: Dict[str, Any]
    static_methods: Dict[str, Any]
    static_properties: Dict[str, Any]

    def __repr__(self):
        return f"<class {self.name}>"

@dataclass
class MyLangInstance:
    class_def: MyLangClass
    properties: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self):
        return f"<{self.class_def.name} instance>"

@dataclass
class BoundMethod:
    """A method bound to an instance, automatically passes 'self' when called."""
    instance: MyLangInstance
    method: MyLangFunction

    def __repr__(self):
        return f"<bound method {self.method.name}>"



# =============================================================================
# ENVIRONMENT
# =============================================================================

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.constants: set = set()
        self.parent = parent

    def define(self, name: str, value: Any, is_const: bool = False):
        self.variables[name] = value
        if is_const:
            self.constants.add(name)

    def get(self, name: str, line: int = 0) -> Any:
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name, line)
        raise MyLangError(f"Undefined variable: {name}", line)

    def set(self, name: str, value: Any, line: int = 0):
        if name in self.variables:
            if name in self.constants:
                raise MyLangError(f"Cannot reassign constant: {name}", line)
            self.variables[name] = value
            return
        if self.parent:
            self.parent.set(name, value, line)
            return
        raise MyLangError(f"Undefined variable: {name}", line)

    def has(self, name: str) -> bool:
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False

# =============================================================================
# BUILT-IN FUNCTIONS
# =============================================================================

class Builtins:
    @staticmethod
    def print(*args, **kwargs):
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        print(*args, sep=sep, end=end)
        return None

    @staticmethod
    def input(prompt: str = ""):
        return input(prompt)

    @staticmethod
    def len(obj):
        return len(obj)

    @staticmethod
    def range(*args):
        return list(range(*args))

    @staticmethod
    def type(obj):
        return type(obj).__name__

    @staticmethod
    def str(obj):
        return str(obj)

    @staticmethod
    def int(obj, base=10):
        return int(obj, base)

    @staticmethod
    def float(obj):
        return float(obj)

    @staticmethod
    def bool(obj):
        return bool(obj)

    @staticmethod
    def list(obj):
        return list(obj)

    @staticmethod
    def dict(obj):
        return dict(obj)

    @staticmethod
    def abs(obj):
        return abs(obj)

    @staticmethod
    def min(*args):
        return min(*args)

    @staticmethod
    def max(*args):
        return max(*args)

    @staticmethod
    def sum(iterable, start=0):
        return sum(iterable, start)

    @staticmethod
    def sorted(iterable, reverse=False, key=None):
        return sorted(iterable, reverse=reverse, key=key)

    @staticmethod
    def reversed(iterable):
        return list(reversed(iterable))

    @staticmethod
    def enumerate(iterable, start=0):
        return list(enumerate(iterable, start))

    @staticmethod
    def zip(*iterables):
        return list(zip(*iterables))

    @staticmethod
    def map(func, iterable):
        return list(map(func, iterable))

    @staticmethod
    def filter(func, iterable):
        return list(filter(func, iterable))

    @staticmethod
    def reduce(func, iterable, initial=None):
        from functools import reduce
        return reduce(func, iterable, initial)

    @staticmethod
    def all(iterable):
        return all(iterable)

    @staticmethod
    def any(iterable):
        return any(iterable)

    @staticmethod
    def round(number, ndigits=None):
        return round(number, ndigits) if ndigits else round(number)

    @staticmethod
    def floor(number):
        import math
        return math.floor(number)

    @staticmethod
    def ceil(number):
        import math
        return math.ceil(number)

    @staticmethod
    def sqrt(number):
        import math
        return math.sqrt(number)

    @staticmethod
    def pow(base, exp):
        return pow(base, exp)

    @staticmethod
    def log(number, base=None):
        import math
        return math.log(number, base) if base else math.log(number)

    @staticmethod
    def sin(x):
        import math
        return math.sin(x)

    @staticmethod
    def cos(x):
        import math
        return math.cos(x)

    @staticmethod
    def tan(x):
        import math
        return math.tan(x)

    @staticmethod
    def random():
        import random
        return random.random()

    @staticmethod
    def randint(a, b):
        import random
        return random.randint(a, b)

    @staticmethod
    def choice(seq):
        import random
        return random.choice(seq)

    @staticmethod
    def shuffle(seq):
        import random
        random.shuffle(seq)
        return seq

    @staticmethod
    def time():
        return time.time()

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)

    @staticmethod
    def json_parse(s):
        return json.loads(s)

    @staticmethod
    def json_stringify(obj, indent=None):
        return json.dumps(obj, indent=indent, ensure_ascii=False)

    @staticmethod
    def hash(obj):
        if isinstance(obj, (str, int, float, bool, tuple)):
            return hash(obj)
        return hash(str(obj))

    @staticmethod
    def id(obj):
        return id(obj)

    @staticmethod
    def isinstance(obj, classinfo):
        if isinstance(classinfo, str):
            return type(obj).__name__ == classinfo
        return isinstance(obj, classinfo)

    @staticmethod
    def hasattr(obj, name):
        return hasattr(obj, name)

    @staticmethod
    def getattr(obj, name, default=None):
        return getattr(obj, name, default)

    @staticmethod
    def setattr(obj, name, value):
        setattr(obj, name, value)

    @staticmethod
    def open(filename, mode='r', encoding='utf-8'):
        return open(filename, mode, encoding=encoding)

    @staticmethod
    def read(filename, encoding='utf-8'):
        with open(filename, 'r', encoding=encoding) as f:
            return f.read()

    @staticmethod
    def write(filename, content, encoding='utf-8'):
        with open(filename, 'w', encoding=encoding) as f:
            f.write(str(content))

    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def mkdir(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def rmdir(path):
        os.rmdir(path)

    @staticmethod
    def listdir(path='.'):
        return os.listdir(path)

    @staticmethod
    def remove(path):
        os.remove(path)

    @staticmethod
    def rename(src, dst):
        os.rename(src, dst)

    @staticmethod
    def copy(src, dst):
        shutil.copy(src, dst)

    @staticmethod
    def cwd():
        return os.getcwd()

    @staticmethod
    def exit(code=0):
        sys.exit(code)

    @staticmethod
    def exec(code):
        exec(code, {})

    @staticmethod
    def eval(code):
        return eval(code)

    @staticmethod
    def format_string(template, *args, **kwargs):
        return template.format(*args, **kwargs)

    @staticmethod
    def split(s, sep=None, maxsplit=-1):
        return s.split(sep, maxsplit)

    @staticmethod
    def join(sep, iterable):
        return sep.join(str(x) for x in iterable)

    @staticmethod
    def replace(s, old, new, count=-1):
        return s.replace(old, new, count)

    @staticmethod
    def strip(s, chars=None):
        return s.strip(chars)

    @staticmethod
    def lower(s):
        return s.lower()

    @staticmethod
    def upper(s):
        return s.upper()

    @staticmethod
    def capitalize(s):
        return s.capitalize()

    @staticmethod
    def title(s):
        return s.title()

    @staticmethod
    def find(s, sub, start=0, end=None):
        return s.find(sub, start, end if end else len(s))

    @staticmethod
    def count(s, sub, start=0, end=None):
        return s.count(sub, start, end)

    @staticmethod
    def startswith(s, prefix):
        return s.startswith(prefix)

    @staticmethod
    def endswith(s, suffix):
        return s.endswith(suffix)

    @staticmethod
    def reverse(seq):
        return list(reversed(seq))

    @staticmethod
    def sort(seq, reverse=False, key=None):
        return sorted(seq, reverse=reverse, key=key)

    @staticmethod
    def append(lst, item):
        lst.append(item)
        return lst

    @staticmethod
    def extend(lst, items):
        lst.extend(items)
        return lst

    @staticmethod
    def pop(lst, index=-1):
        return lst.pop(index)

    @staticmethod
    def insert(lst, index, item):
        lst.insert(index, item)
        return lst

    @staticmethod
    def remove_item(lst, item):
        lst.remove(item)
        return lst

    @staticmethod
    def index(lst, item, start=0, end=None):
        return lst.index(item, start, end if end else len(lst))

    @staticmethod
    def keys(d):
        return list(d.keys())

    @staticmethod
    def values(d):
        return list(d.values())

    @staticmethod
    def items(d):
        return list(d.items())

    @staticmethod
    def get(d, key, default=None):
        return d.get(key, default)

    @staticmethod
    def update(d, other):
        d.update(other)
        return d

    @staticmethod
    def pop_key(d, key, default=None):
        return d.pop(key, default)

    @staticmethod
    def clear(d):
        d.clear()
        return d

def create_builtins() -> Dict[str, Any]:
    import inspect
    builtins = {}
    for name, method in inspect.getmembers(Builtins, predicate=inspect.isfunction):
        if not name.startswith('_'):
            builtins[name] = method

    # Aliases
    builtins['println'] = Builtins.print
    builtins['log'] = Builtins.print
    builtins['len'] = Builtins.len
    builtins['typeof'] = Builtins.type
    builtins['parseInt'] = Builtins.int
    builtins['parseFloat'] = Builtins.float
    builtins['parseJSON'] = Builtins.json_parse
    builtins['stringifyJSON'] = Builtins.json_stringify

    return builtins

# =============================================================================
# INTERPRETER
# =============================================================================

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.setup_builtins()
        self.modules: Dict[str, Any] = {}

    def setup_builtins(self):
        builtins = create_builtins()
        for name, func in builtins.items():
            self.global_env.define(name, func)

        # Constants
        self.global_env.define('PI', 3.141592653589793, is_const=True)
        self.global_env.define('E', 2.718281828459045, is_const=True)
        self.global_env.define('True', True, is_const=True)
        self.global_env.define('False', False, is_const=True)
        self.global_env.define('None', None, is_const=True)
        self.global_env.define('__version__', VERSION, is_const=True)

    def run(self, source: str, filename: str = "<stdin>") -> Any:
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            return self.execute(ast)
        except (LexerError, ParseError, MyLangError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return None

    def execute(self, node: ASTNode, env: Environment = None) -> Any:
        if env is None:
            env = self.global_env

        method_name = f'eval_{node.__class__.__name__}'
        method = getattr(self, method_name, None)

        if method is None:
            raise MyLangError(f"Unknown node type: {node.__class__.__name__}",
                             getattr(node, 'line', 0))

        return method(node, env)

    def eval_Program(self, node: Program, env: Environment) -> Any:
        result = None
        for stmt in node.statements:
            result = self.execute(stmt, env)
        return result

    def eval_NumberLiteral(self, node: NumberLiteral, env: Environment) -> Union[int, float]:
        return node.value

    def eval_StringLiteral(self, node: StringLiteral, env: Environment) -> str:
        return node.value

    def eval_BooleanLiteral(self, node: BooleanLiteral, env: Environment) -> bool:
        return node.value

    def eval_NoneLiteral(self, node: NoneLiteral, env: Environment) -> None:
        return None

    def eval_ListLiteral(self, node: ListLiteral, env: Environment) -> list:
        return [self.execute(elem, env) for elem in node.elements]

    def eval_DictLiteral(self, node: DictLiteral, env: Environment) -> dict:
        result = {}
        for key, value in node.pairs:
            k = self.execute(key, env)
            v = self.execute(value, env)
            result[k] = v
        return result

    def eval_Identifier(self, node: Identifier, env: Environment) -> Any:
        return env.get(node.name, node.line)

    def eval_BinaryOp(self, node: BinaryOp, env: Environment) -> Any:
        left = self.execute(node.left, env)

        # Short-circuit evaluation
        if node.operator == 'and':
            if not left:
                return left
            return self.execute(node.right, env)

        if node.operator == 'or':
            if left:
                return left
            return self.execute(node.right, env)

        right = self.execute(node.right, env)

        op = node.operator
        ops = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '//': lambda a, b: a // b,
            '%': lambda a, b: a % b,
            '**': lambda a, b: a ** b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<': lambda a, b: a < b,
            '>': lambda a, b: a > b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
            'in': lambda a, b: a in b,
            '&': lambda a, b: a & b,
            '|': lambda a, b: a | b,
            '^': lambda a, b: a ^ b,
            '<<': lambda a, b: a << b,
            '>>': lambda a, b: a >> b,
        }

        if op in ops:
            return ops[op](left, right)

        raise MyLangError(f"Unknown operator: {op}", node.line)

    def eval_UnaryOp(self, node: UnaryOp, env: Environment) -> Any:
        operand = self.execute(node.operand, env)

        ops = {
            '-': lambda x: -x,
            'not': lambda x: not x,
            '~': lambda x: ~x,
            'await': lambda x: x,  # Simplified await
        }

        if node.operator in ops:
            return ops[node.operator](operand)

        raise MyLangError(f"Unknown unary operator: {node.operator}", node.line)

    def eval_TernaryOp(self, node: TernaryOp, env: Environment) -> Any:
        condition = self.execute(node.condition, env)
        if condition:
            return self.execute(node.true_expr, env)
        return self.execute(node.false_expr, env)

    def eval_CallExpression(self, node: CallExpression, env: Environment) -> Any:
        callee = self.execute(node.callee, env)
        args = [self.execute(arg, env) for arg in node.arguments]

        if callable(callee) and not isinstance(callee, (MyLangFunction, MyLangClass, BoundMethod)):
            try:
                return callee(*args)
            except Exception as e:
                raise MyLangError(f"Error calling function: {e}", node.line)

        if isinstance(callee, BoundMethod):
            # Prepend the instance as 'self' to the arguments
            return self.call_function(callee.method, [callee.instance] + args, node.line)

        if isinstance(callee, MyLangFunction):
            return self.call_function(callee, args, node.line)

        if isinstance(callee, MyLangClass):
            return self.instantiate(callee, args, node.line)

        raise MyLangError(f"Cannot call {type(callee).__name__}", node.line)

    def call_function(self, func: MyLangFunction, args: List[Any], line: int) -> Any:
        # Check if first param is 'self' or if we have an implicit self
        params = func.params
        actual_args = args

        # If we have more args than params and first arg is an instance,
        # it's a method call with implicit self
        if len(args) > len(params) and len(params) > 0 and params[0] == 'self':
            # Method with explicit self parameter
            pass
        elif len(args) > len(params) and isinstance(args[0], MyLangInstance):
            # Method call with implicit self - define 'self' separately
            local_env = Environment(func.closure)
            local_env.define('self', args[0])
            actual_args = args[1:]
            if len(actual_args) != len(params):
                raise MyLangError(
                    f"Expected {len(params)} arguments, got {len(actual_args)}", line
                )
            for param, arg in zip(params, actual_args):
                local_env.define(param, arg)

            try:
                for stmt in func.body:
                    self.execute(stmt, local_env)
            except ReturnValue as rv:
                return rv.value

            return None

        if len(actual_args) != len(params):
            raise MyLangError(
                f"Expected {len(params)} arguments, got {len(actual_args)}", line
            )

        local_env = Environment(func.closure)
        for param, arg in zip(params, actual_args):
            local_env.define(param, arg)

        try:
            for stmt in func.body:
                self.execute(stmt, local_env)
        except ReturnValue as rv:
            return rv.value

        return None

    def instantiate(self, class_def: MyLangClass, args: List[Any], line: int) -> MyLangInstance:
        instance = MyLangInstance(class_def=class_def)

        # Copy properties
        for name, value in class_def.properties.items():
            instance.properties[name] = value

        # Call constructor
        if '__init__' in class_def.methods:
            constructor = class_def.methods['__init__']
            self.call_method(constructor, [instance] + args, line)

        return instance

    def call_method(self, method: MyLangFunction, args: List[Any], line: int) -> Any:
        local_env = Environment(method.closure)

        # First argument is 'self' for instance methods
        if args and len(method.params) > 0 and method.params[0] == 'self':
            # Method has explicit 'self' parameter
            for param, arg in zip(method.params, args):
                local_env.define(param, arg)
        elif args:
            # Method without explicit 'self', but we pass instance
            # Define 'self' first, then the rest of the parameters
            if len(args) > len(method.params):
                # Instance method: first arg is self
                local_env.define('self', args[0])
                for param, arg in zip(method.params, args[1:]):
                    local_env.define(param, arg)
            else:
                # Just parameters
                for param, arg in zip(method.params, args):
                    local_env.define(param, arg)

        try:
            for stmt in method.body:
                self.execute(stmt, local_env)
        except ReturnValue as rv:
            return rv.value

        return None

    def eval_MemberExpression(self, node: MemberExpression, env: Environment) -> Any:
        obj = self.execute(node.obj, env)

        if node.computed:
            prop = self.execute(node.prop, env)
        else:
            prop = node.prop.value

        # Instance property/method
        if isinstance(obj, MyLangInstance):
            if prop in obj.properties:
                return obj.properties[prop]
            if prop in obj.class_def.methods:
                # Return a bound method that includes the instance as 'self'
                method = obj.class_def.methods[prop]
                return BoundMethod(instance=obj, method=method)

        # Class static members
        if isinstance(obj, MyLangClass):
            if prop in obj.static_properties:
                return obj.static_properties[prop]
            if prop in obj.static_methods:
                return obj.static_methods[prop]

        # Built-in types
        if hasattr(obj, prop):
            attr = getattr(obj, prop)
            if callable(attr):
                return lambda *args, **kwargs: attr(*args, **kwargs)
            return attr

        # Dictionary
        if isinstance(obj, dict):
            if prop in obj:
                return obj[prop]

        # List
        if isinstance(obj, list) and isinstance(prop, int):
            return obj[prop]

        raise MyLangError(f"'{type(obj).__name__}' has no attribute '{prop}'", node.line)

    def eval_AssignmentExpression(self, node: AssignmentExpression, env: Environment) -> Any:
        value = self.execute(node.value, env)

        if isinstance(node.target, Identifier):
            if node.operator == '=':
                if env.has(node.target.name):
                    env.set(node.target.name, value, node.line)
                else:
                    env.define(node.target.name, value)
            else:
                current = env.get(node.target.name, node.line)
                ops = {
                    '+=': lambda a, b: a + b,
                    '-=': lambda a, b: a - b,
                    '*=': lambda a, b: a * b,
                    '/=': lambda a, b: a / b,
                }
                value = ops[node.operator](current, value)
                env.set(node.target.name, value, node.line)
            return value

        if isinstance(node.target, MemberExpression):
            obj = self.execute(node.target.obj, env)

            if node.target.computed:
                prop = self.execute(node.target.prop, env)
            else:
                prop = node.target.prop.value

            if isinstance(obj, MyLangInstance):
                obj.properties[prop] = value
            elif isinstance(obj, dict):
                obj[prop] = value
            elif isinstance(obj, list) and isinstance(prop, int):
                obj[prop] = value
            else:
                setattr(obj, prop, value)

            return value

        raise MyLangError("Invalid assignment target", node.line)

    def eval_SpreadExpression(self, node: SpreadExpression, env: Environment) -> Any:
        return self.execute(node.argument, env)

    def eval_LambdaExpression(self, node: LambdaExpression, env: Environment) -> MyLangFunction:
        params = [p for p in node.params] if isinstance(node.params, list) else [node.params]

        return MyLangFunction(
            name='<lambda>',
            params=params,
            body=[ExpressionStatement(expression=node.body)],
            closure=env.variables.copy()
        )

    def eval_VariableDeclaration(self, node: VariableDeclaration, env: Environment) -> None:
        value = None
        if node.value:
            value = self.execute(node.value, env)

        is_const = node.kind == 'const'
        env.define(node.name, value, is_const)
        return None

    def eval_FunctionDeclaration(self, node: FunctionDeclaration, env: Environment) -> None:
        params = [p[0] for p in node.params]

        # Create closure from current environment
        closure = env.variables.copy()

        func = MyLangFunction(
            name=node.name,
            params=params,
            body=node.body,
            closure=closure,
            is_async=node.is_async
        )

        # Add function to both the environment and its own closure for recursion
        env.define(node.name, func)
        closure[node.name] = func  # Enable recursion
        return None

    def eval_ReturnStatement(self, node: ReturnStatement, env: Environment) -> None:
        value = None
        if node.value:
            value = self.execute(node.value, env)
        raise ReturnValue(value)

    def eval_IfStatement(self, node: IfStatement, env: Environment) -> Any:
        condition = self.execute(node.condition, env)

        if condition:
            for stmt in node.consequent:
                self.execute(stmt, env)
        else:
            executed = False
            for elif_cond, elif_body in node.elif_clauses:
                if self.execute(elif_cond, env):
                    for stmt in elif_body:
                        self.execute(stmt, env)
                    executed = True
                    break

            if not executed and node.alternate:
                for stmt in node.alternate:
                    self.execute(stmt, env)

        return None

    def eval_WhileStatement(self, node: WhileStatement, env: Environment) -> None:
        while self.execute(node.condition, env):
            try:
                for stmt in node.body:
                    self.execute(stmt, env)
            except BreakException:
                break
            except ContinueException:
                continue
        return None

    def eval_ForStatement(self, node: ForStatement, env: Environment) -> None:
        iterable = self.execute(node.iterable, env)

        for item in iterable:
            env.define(node.variable, item)
            try:
                for stmt in node.body:
                    self.execute(stmt, env)
            except BreakException:
                break
            except ContinueException:
                continue
        return None

    def eval_LoopStatement(self, node: LoopStatement, env: Environment) -> None:
        if node.variable and node.iterable:
            iterable = self.execute(node.iterable, env)
            for item in iterable:
                env.define(node.variable, item)
                try:
                    for stmt in node.body:
                        self.execute(stmt, env)
                except BreakException:
                    break
                except ContinueException:
                    continue
        else:
            while True:
                try:
                    for stmt in node.body:
                        self.execute(stmt, env)
                except BreakException:
                    break
                except ContinueException:
                    continue
        return None

    def eval_BreakStatement(self, node: BreakStatement, env: Environment) -> None:
        raise BreakException()

    def eval_ContinueStatement(self, node: ContinueStatement, env: Environment) -> None:
        raise ContinueException()

    def eval_ClassDeclaration(self, node: ClassDeclaration, env: Environment) -> None:
        methods = {}
        properties = {}
        static_methods = {}
        static_properties = {}

        # Handle inheritance - copy parent class methods and properties
        if node.extends:
            try:
                parent_class = env.get(node.extends, 0)
                if isinstance(parent_class, MyLangClass):
                    # Copy parent methods (child can override)
                    methods.update(parent_class.methods)
                    properties.update(parent_class.properties)
                    static_methods.update(parent_class.static_methods)
                    static_properties.update(parent_class.static_properties)
            except:
                pass  # Parent class not found, continue without inheritance

        for member in node.body:
            if isinstance(member, PropertyDeclaration):
                value = self.execute(member.value, env) if member.value else None
                if member.is_static:
                    static_properties[member.name] = value
                else:
                    properties[member.name] = value
            elif isinstance(member, MethodDeclaration):
                params = [p[0] for p in member.params]
                method = MyLangFunction(
                    name=member.name,
                    params=params,
                    body=member.body,
                    closure=env.variables.copy(),
                    is_async=member.is_async
                )
                if member.is_static:
                    static_methods[member.name] = method
                else:
                    methods[member.name] = method

        class_def = MyLangClass(
            name=node.name,
            extends=node.extends,
            methods=methods,
            properties=properties,
            static_methods=static_methods,
            static_properties=static_properties
        )

        env.define(node.name, class_def)
        return None

    def eval_TryStatement(self, node: TryStatement, env: Environment) -> Any:
        try:
            for stmt in node.try_block:
                self.execute(stmt, env)
        except ReturnValue:
            raise
        except MyLangError as e:
            if node.catch_block:
                local_env = Environment(env)
                if node.catch_var:
                    local_env.define(node.catch_var, str(e))
                for stmt in node.catch_block:
                    self.execute(stmt, local_env)
        except Exception as e:
            if node.catch_block:
                local_env = Environment(env)
                if node.catch_var:
                    local_env.define(node.catch_var, str(e))
                for stmt in node.catch_block:
                    self.execute(stmt, local_env)
        finally:
            if node.finally_block:
                for stmt in node.finally_block:
                    self.execute(stmt, env)

        return None

    def eval_ThrowStatement(self, node: ThrowStatement, env: Environment) -> None:
        value = self.execute(node.value, env)
        raise MyLangError(str(value), node.line)

    def eval_MatchStatement(self, node: MatchStatement, env: Environment) -> Any:
        subject = self.execute(node.subject, env)

        for pattern, body in node.cases:
            if self.match_pattern(pattern, subject, env):
                for stmt in body:
                    self.execute(stmt, env)
                return None

        if node.default_case:
            for stmt in node.default_case:
                self.execute(stmt, env)

        return None

    def match_pattern(self, pattern: ASTNode, value: Any, env: Environment) -> bool:
        if isinstance(pattern, Identifier):
            env.define(pattern.name, value)
            return True

        if isinstance(pattern, NumberLiteral):
            return pattern.value == value

        if isinstance(pattern, StringLiteral):
            return pattern.value == value

        if isinstance(pattern, BooleanLiteral):
            return pattern.value == value

        if isinstance(pattern, NoneLiteral):
            return value is None

        if isinstance(pattern, ListLiteral):
            if not isinstance(value, list) or len(pattern.elements) != len(value):
                return False
            for p, v in zip(pattern.elements, value):
                if not self.match_pattern(p, v, env):
                    return False
            return True

        return False

    def eval_ImportStatement(self, node: ImportStatement, env: Environment) -> Any:
        module_name = node.module

        # Check if already loaded
        if module_name in self.modules:
            module = self.modules[module_name]
        else:
            # Try to load from packages
            module = self.load_module(module_name)
            self.modules[module_name] = module

        if node.is_all:
            for name, value in module.items():
                env.define(name, value)
        else:
            for name, alias in node.names:
                if name in module:
                    env.define(alias or name, module[name])

        return None

    def load_module(self, name: str) -> Dict[str, Any]:
        # Standard library modules
        std_modules = {
            'math': {
                'PI': 3.141592653589793,
                'E': 2.718281828459045,
                'sqrt': Builtins.sqrt,
                'pow': Builtins.pow,
                'log': Builtins.log,
                'sin': Builtins.sin,
                'cos': Builtins.cos,
                'tan': Builtins.tan,
                'floor': Builtins.floor,
                'ceil': Builtins.ceil,
            },
            'random': {
                'random': Builtins.random,
                'randint': Builtins.randint,
                'choice': Builtins.choice,
                'shuffle': Builtins.shuffle,
            },
            'time': {
                'time': Builtins.time,
                'sleep': Builtins.sleep,
            },
            'json': {
                'parse': Builtins.json_parse,
                'stringify': Builtins.json_stringify,
            },
            'os': {
                'cwd': Builtins.cwd,
                'exists': Builtins.exists,
                'mkdir': Builtins.mkdir,
                'rmdir': Builtins.rmdir,
                'listdir': Builtins.listdir,
                'remove': Builtins.remove,
                'rename': Builtins.rename,
                'copy': Builtins.copy,
            },
            'io': {
                'open': Builtins.open,
                'read': Builtins.read,
                'write': Builtins.write,
            },
            'string': {
                'split': Builtins.split,
                'join': Builtins.join,
                'replace': Builtins.replace,
                'strip': Builtins.strip,
                'lower': Builtins.lower,
                'upper': Builtins.upper,
                'capitalize': Builtins.capitalize,
                'title': Builtins.title,
                'find': Builtins.find,
                'count': Builtins.count,
                'startswith': Builtins.startswith,
                'endswith': Builtins.endswith,
            },
            'list': {
                'append': Builtins.append,
                'extend': Builtins.extend,
                'pop': Builtins.pop,
                'insert': Builtins.insert,
                'remove': Builtins.remove_item,
                'index': Builtins.index,
                'reverse': Builtins.reverse,
                'sort': Builtins.sort,
            },
            'dict': {
                'keys': Builtins.keys,
                'values': Builtins.values,
                'items': Builtins.items,
                'get': Builtins.get,
                'update': Builtins.update,
                'pop': Builtins.pop_key,
                'clear': Builtins.clear,
            },
        }

        if name in std_modules:
            return std_modules[name]

        # Try to load from file
        file_path = Path(name.replace('.', '/') + '.ml')
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            module_env = Environment(self.global_env)
            self.run(source)
            return module_env.variables

        raise MyLangError(f"Module not found: {name}")

    def eval_ExportStatement(self, node: ExportStatement, env: Environment) -> Any:
        return self.execute(node.declaration, env)

    def eval_WithStatement(self, node: WithStatement, env: Environment) -> Any:
        value = self.execute(node.expression, env)

        local_env = Environment(env)
        if node.variable:
            local_env.define(node.variable, value)

        # Simple context manager simulation
        try:
            for stmt in node.body:
                self.execute(stmt, local_env)
        finally:
            if hasattr(value, 'close'):
                value.close()

        return None

    def eval_ListComprehension(self, node: ListComprehension, env: Environment) -> list:
        result = []
        iterable = self.execute(node.iterable, env)

        for item in iterable:
            local_env = Environment(env)
            local_env.define(node.variable, item)

            if node.condition:
                if self.execute(node.condition, local_env):
                    result.append(self.execute(node.expression, local_env))
            else:
                result.append(self.execute(node.expression, local_env))

        return result

    def eval_DictComprehension(self, node: DictComprehension, env: Environment) -> dict:
        result = {}
        iterable = self.execute(node.iterable, env)

        for item in iterable:
            local_env = Environment(env)
            local_env.define(node.variable, item)

            if node.condition:
                if self.execute(node.condition, local_env):
                    key = self.execute(node.key_expr, local_env)
                    value = self.execute(node.value_expr, local_env)
                    result[key] = value
            else:
                key = self.execute(node.key_expr, local_env)
                value = self.execute(node.value_expr, local_env)
                result[key] = value

        return result

    def eval_ExpressionStatement(self, node: ExpressionStatement, env: Environment) -> Any:
        return self.execute(node.expression, env)

# =============================================================================
# PYTHON COMPILER
# =============================================================================

class PythonCompiler:
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "

    def compile(self, ast: Program) -> str:
        lines = [
            '#!/usr/bin/env python3',
            '# Generated by MyLang Compiler',
            'from typing import *',
            'import math',
            'import random',
            'import time',
            'import json',
            'import os',
            'import sys',
            'from functools import reduce',
            '',
        ]

        for stmt in ast.statements:
            compiled = self.compile_statement(stmt)
            if compiled:
                lines.append(compiled)

        return '\n'.join(lines)

    def indent(self) -> str:
        return self.indent_str * self.indent_level

    def compile_statement(self, node: ASTNode) -> str:
        method_name = f'compile_{node.__class__.__name__}'
        method = getattr(self, method_name, None)

        if method is None:
            return f'# Unknown statement: {node.__class__.__name__}'

        return method(node)

    def compile_VariableDeclaration(self, node: VariableDeclaration) -> str:
        value = self.compile_expression(node.value) if node.value else 'None'

        if node.kind == 'const':
            return f'{self.indent()}{node.name}: Final = {value}'
        else:
            return f'{self.indent()}{node.name} = {value}'

    def compile_FunctionDeclaration(self, node: FunctionDeclaration) -> str:
        # params is a list of (name, type) tuples
        params = ', '.join(p[0] if isinstance(p, tuple) else p for p in node.params)
        async_kw = 'async ' if node.is_async else ''

        lines = [f'{self.indent()}{async_kw}def {node.name}({params}):']

        self.indent_level += 1

        if node.body:
            for stmt in node.body:
                lines.append(self.compile_statement(stmt))
        else:
            lines.append(f'{self.indent()}pass')

        self.indent_level -= 1
        return '\n'.join(lines)

    def compile_ClassDeclaration(self, node: ClassDeclaration) -> str:
        extends = f'({node.extends})' if node.extends else ''

        lines = [f'{self.indent()}class {node.name}{extends}:']

        self.indent_level += 1

        if node.body:
            for member in node.body:
                lines.append(self.compile_statement(member))
        else:
            lines.append(f'{self.indent()}pass')

        self.indent_level -= 1
        return '\n'.join(lines)

    def compile_MethodDeclaration(self, node: MethodDeclaration) -> str:
        params = ['self'] + [p[0] for p in node.params]
        params_str = ', '.join(params)
        async_kw = 'async ' if node.is_async else ''
        static_kw = '@staticmethod\n' if node.is_static else ''

        lines = [f'{self.indent()}{static_kw}{async_kw}def {node.name}({params_str}):']

        self.indent_level += 1

        if node.body:
            for stmt in node.body:
                lines.append(self.compile_statement(stmt))
        else:
            lines.append(f'{self.indent()}pass')

        self.indent_level -= 1
        return '\n'.join(lines)

    def compile_PropertyDeclaration(self, node: PropertyDeclaration) -> str:
        value = self.compile_expression(node.value) if node.value else 'None'
        return f'{self.indent()}{node.name} = {value}'

    def compile_IfStatement(self, node: IfStatement) -> str:
        condition = self.compile_expression(node.condition)
        lines = [f'{self.indent()}if {condition}:']

        self.indent_level += 1
        for stmt in node.consequent:
            lines.append(self.compile_statement(stmt))
        if not node.consequent:
            lines.append(f'{self.indent()}pass')
        self.indent_level -= 1

        for elif_cond, elif_body in node.elif_clauses:
            condition = self.compile_expression(elif_cond)
            lines.append(f'{self.indent()}elif {condition}:')
            self.indent_level += 1
            for stmt in elif_body:
                lines.append(self.compile_statement(stmt))
            if not elif_body:
                lines.append(f'{self.indent()}pass')
            self.indent_level -= 1

        if node.alternate:
            lines.append(f'{self.indent()}else:')
            self.indent_level += 1
            for stmt in node.alternate:
                lines.append(self.compile_statement(stmt))
            if not node.alternate:
                lines.append(f'{self.indent()}pass')
            self.indent_level -= 1

        return '\n'.join(lines)

    def compile_WhileStatement(self, node: WhileStatement) -> str:
        condition = self.compile_expression(node.condition)
        lines = [f'{self.indent()}while {condition}:']

        self.indent_level += 1
        for stmt in node.body:
            lines.append(self.compile_statement(stmt))
        if not node.body:
            lines.append(f'{self.indent()}pass')
        self.indent_level -= 1

        return '\n'.join(lines)

    def compile_ForStatement(self, node: ForStatement) -> str:
        iterable = self.compile_expression(node.iterable)
        lines = [f'{self.indent()}for {node.variable} in {iterable}:']

        self.indent_level += 1
        for stmt in node.body:
            lines.append(self.compile_statement(stmt))
        if not node.body:
            lines.append(f'{self.indent()}pass')
        self.indent_level -= 1

        return '\n'.join(lines)

    def compile_LoopStatement(self, node: LoopStatement) -> str:
        if node.variable and node.iterable:
            iterable = self.compile_expression(node.iterable)
            lines = [f'{self.indent()}for {node.variable} in {iterable}:']
        else:
            lines = [f'{self.indent()}while True:']

        self.indent_level += 1
        for stmt in node.body:
            lines.append(self.compile_statement(stmt))
        if not node.body:
            lines.append(f'{self.indent()}pass')
        self.indent_level -= 1

        return '\n'.join(lines)

    def compile_ReturnStatement(self, node: ReturnStatement) -> str:
        value = self.compile_expression(node.value) if node.value else 'None'
        return f'{self.indent()}return {value}'

    def compile_BreakStatement(self, node: BreakStatement) -> str:
        return f'{self.indent()}break'

    def compile_ContinueStatement(self, node: ContinueStatement) -> str:
        return f'{self.indent()}continue'

    def compile_TryStatement(self, node: TryStatement) -> str:
        lines = [f'{self.indent()}try:']

        self.indent_level += 1
        for stmt in node.try_block:
            lines.append(self.compile_statement(stmt))
        if not node.try_block:
            lines.append(f'{self.indent()}pass')
        self.indent_level -= 1

        if node.catch_block:
            catch_var = node.catch_var or 'e'
            lines.append(f'{self.indent()}except Exception as {catch_var}:')
            self.indent_level += 1
            for stmt in node.catch_block:
                lines.append(self.compile_statement(stmt))
            if not node.catch_block:
                lines.append(f'{self.indent()}pass')
            self.indent_level -= 1

        if node.finally_block:
            lines.append(f'{self.indent()}finally:')
            self.indent_level += 1
            for stmt in node.finally_block:
                lines.append(self.compile_statement(stmt))
            if not node.finally_block:
                lines.append(f'{self.indent()}pass')
            self.indent_level -= 1

        return '\n'.join(lines)

    def compile_ThrowStatement(self, node: ThrowStatement) -> str:
        value = self.compile_expression(node.value)
        return f'{self.indent()}raise Exception({value})'

    def compile_ExpressionStatement(self, node: ExpressionStatement) -> str:
        return f'{self.indent()}{self.compile_expression(node.expression)}'

    def compile_expression(self, node: ASTNode) -> str:
        if node is None:
            return 'None'

        method_name = f'compile_expr_{node.__class__.__name__}'
        method = getattr(self, method_name, None)

        if method is None:
            return f'# Unknown expression: {node.__class__.__name__}'

        return method(node)

    def compile_expr_NumberLiteral(self, node: NumberLiteral) -> str:
        return str(node.value)

    def compile_expr_StringLiteral(self, node: StringLiteral) -> str:
        return repr(node.value)

    def compile_expr_BooleanLiteral(self, node: BooleanLiteral) -> str:
        return 'True' if node.value else 'False'

    def compile_expr_NoneLiteral(self, node: NoneLiteral) -> str:
        return 'None'

    def compile_expr_Identifier(self, node: Identifier) -> str:
        if node.name == 'self':
            return 'self'
        return node.name

    def compile_expr_ListLiteral(self, node: ListLiteral) -> str:
        elements = ', '.join(self.compile_expression(e) for e in node.elements)
        return f'[{elements}]'

    def compile_expr_DictLiteral(self, node: DictLiteral) -> str:
        pairs = []
        for key, value in node.pairs:
            k = self.compile_expression(key)
            v = self.compile_expression(value)
            pairs.append(f'{k}: {v}')
        return '{' + ', '.join(pairs) + '}'

    def compile_expr_BinaryOp(self, node: BinaryOp) -> str:
        left = self.compile_expression(node.left)
        right = self.compile_expression(node.right)
        op = node.operator

        if op == 'and':
            return f'({left} and {right})'
        if op == 'or':
            return f'({left} or {right})'
        if op == 'in':
            return f'({left} in {right})'

        return f'({left} {op} {right})'

    def compile_expr_UnaryOp(self, node: UnaryOp) -> str:
        operand = self.compile_expression(node.operand)
        return f'({node.operator} {operand})'

    def compile_expr_TernaryOp(self, node: TernaryOp) -> str:
        condition = self.compile_expression(node.condition)
        true_expr = self.compile_expression(node.true_expr)
        false_expr = self.compile_expression(node.false_expr)
        return f'({true_expr} if {condition} else {false_expr})'

    def compile_expr_CallExpression(self, node: CallExpression) -> str:
        callee = self.compile_expression(node.callee)
        args = ', '.join(self.compile_expression(a) for a in node.arguments)
        return f'{callee}({args})'

    def compile_expr_MemberExpression(self, node: MemberExpression) -> str:
        obj = self.compile_expression(node.obj)

        if node.computed:
            prop = self.compile_expression(node.prop)
            return f'{obj}[{prop}]'
        else:
            prop = node.prop.value
            return f'{obj}.{prop}'

    def compile_expr_AssignmentExpression(self, node: AssignmentExpression) -> str:
        target = self.compile_expression(node.target)
        value = self.compile_expression(node.value)

        if node.operator == '=':
            return f'{target} = {value}'

        return f'{target} {node.operator} {value}'

    def compile_expr_LambdaExpression(self, node: LambdaExpression) -> str:
        params = ', '.join(node.params)
        body = self.compile_expression(node.body)
        return f'lambda {params}: {body}'

    def compile_expr_ListComprehension(self, node: ListComprehension) -> str:
        expr = self.compile_expression(node.expression)
        iterable = self.compile_expression(node.iterable)

        if node.condition:
            condition = self.compile_expression(node.condition)
            return f'[{expr} for {node.variable} in {iterable} if {condition}]'

        return f'[{expr} for {node.variable} in {iterable}]'

# =============================================================================
# PACKAGE MANAGER
# =============================================================================

class PackageManager:
    """MyLang Package Manager - Port/Repository System"""
    
    # Default repositories - including user's repo
    DEFAULT_REPOS = [
        {
            'name': 'mylang-official',
            'url': 'https://github.com/Botan-linux/mylang',
            'branch': 'main',
            'repo_path': 'repo',  # Path to packages inside repo
            'description': 'Official MyLang Package Repository',
            'priority': 1
        },
        {
            'name': 'pypi',
            'url': 'https://pypi.org',
            'description': 'Python Package Index (fallback)',
            'priority': 100
        }
    ]
    
    def __init__(self):
        self.ensure_directories()
        self.config = self.load_config()
        self.repo_cache = {}  # Cache for repository indexes
        
    def ensure_directories(self):
        MYLANG_DIR.mkdir(parents=True, exist_ok=True)
        PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        if not CONFIG_FILE.exists():
            self.save_config({
                'version': VERSION,
                'packages': {},
                'repositories': self.DEFAULT_REPOS.copy(),
                'settings': {
                    'auto_update': False,
                    'cache_ttl': 3600,  # 1 hour cache
                }
            })

    def load_config(self) -> dict:
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Ensure default repos exist
                if 'repositories' not in config:
                    config['repositories'] = self.DEFAULT_REPOS.copy()
                return config
        except:
            return {
                'version': VERSION, 
                'packages': {}, 
                'repositories': self.DEFAULT_REPOS.copy(),
                'settings': {'auto_update': False, 'cache_ttl': 3600}
            }

    def save_config(self, config: dict):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    # =========================================================================
    # REPOSITORY MANAGEMENT
    # =========================================================================
    
    def add_repo(self, name: str, url: str, branch: str = 'main', repo_path: str = 'repo') -> bool:
        """Add a new repository"""
        for repo in self.config.get('repositories', []):
            if repo['name'] == name:
                print(f"Repository '{name}' already exists.")
                return False
        
        new_repo = {
            'name': name,
            'url': url,
            'branch': branch,
            'repo_path': repo_path,
            'description': f'Custom repository: {name}',
            'priority': len(self.config.get('repositories', [])) + 1
        }
        
        self.config.setdefault('repositories', []).append(new_repo)
        self.save_config(self.config)
        print(f"Added repository: {name}")
        return True
    
    def remove_repo(self, name: str) -> bool:
        """Remove a repository"""
        repos = self.config.get('repositories', [])
        for i, repo in enumerate(repos):
            if repo['name'] == name:
                del repos[i]
                self.save_config(self.config)
                print(f"Removed repository: {name}")
                return True
        print(f"Repository '{name}' not found.")
        return False
    
    def list_repos(self) -> List[dict]:
        """List all repositories"""
        return self.config.get('repositories', [])
    
    def update_repos(self) -> bool:
        """Update repository indexes"""
        print("Updating repository indexes...")
        for repo in self.config.get('repositories', []):
            if repo['name'] == 'pypi':
                continue
            print(f"  Updating {repo['name']}...")
            try:
                index_url = self._get_repo_index_url(repo)
                # In a real implementation, we'd fetch and cache the index
                print(f"    ✓ {repo['name']} updated")
            except Exception as e:
                print(f"    ✗ Failed to update {repo['name']}: {e}")
        return True
    
    def _get_repo_index_url(self, repo: dict) -> str:
        """Get the index URL for a repository"""
        if 'github.com' in repo.get('url', ''):
            # GitHub raw content URL
            url = repo['url'].replace('github.com', 'raw.githubusercontent.com')
            branch = repo.get('branch', 'main')
            repo_path = repo.get('repo_path', 'repo')
            return f"{url}/{branch}/{repo_path}/index.json"
        return f"{repo['url']}/index.json"

    # =========================================================================
    # PACKAGE OPERATIONS
    # =========================================================================
    
    def fetch_repo_index(self, repo: dict) -> dict:
        """Fetch package index from a repository"""
        cache_key = repo['name']
        cache_file = CACHE_DIR / f"index_{cache_key}.json"
        
        # Check cache
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    # Check if cache is still valid
                    cache_time = cached.get('cached_at', 0)
                    ttl = self.config.get('settings', {}).get('cache_ttl', 3600)
                    if time.time() - cache_time < ttl:
                        return cached.get('packages', {})
            except:
                pass
        
        # Fetch from GitHub
        packages = {}
        try:
            if 'github.com' in repo.get('url', ''):
                # Try to fetch package list from GitHub API
                api_url = f"{GITHUB_API}/repos/{self._extract_github_repo(repo['url'])}/contents/{repo.get('repo_path', 'repo')}"
                req = urllib.request.Request(api_url)
                req.add_header('Accept', 'application/vnd.github.v3+json')
                
                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode())
                    
                    for item in data:
                        if item['type'] == 'file' and item['name'].endswith('.ml'):
                            pkg_name = item['name'][:-3]  # Remove .ml extension
                            packages[pkg_name] = {
                                'name': pkg_name,
                                'download_url': item.get('download_url', ''),
                                'sha': item.get('sha', ''),
                                'size': item.get('size', 0),
                            }
                        elif item['type'] == 'dir':
                            # Package directory
                            pkg_name = item['name']
                            packages[pkg_name] = {
                                'name': pkg_name,
                                'path': item['path'],
                                'type': 'directory',
                            }
        except Exception as e:
            print(f"Warning: Could not fetch index from {repo['name']}: {e}")
        
        # Cache the result
        try:
            with open(cache_file, 'w') as f:
                json.dump({'packages': packages, 'cached_at': time.time()}, f)
        except:
            pass
        
        return packages
    
    def _extract_github_repo(self, url: str) -> str:
        """Extract repo owner/name from GitHub URL"""
        # Handle various GitHub URL formats
        url = url.rstrip('/')
        if 'github.com' in url:
            parts = url.split('github.com/')[-1].split('/')
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"
        return ""
    
    def search(self, query: str) -> List[dict]:
        """Search for packages in all repositories"""
        print(f"Searching for '{query}'...")
        results = []
        query_lower = query.lower()
        
        for repo in sorted(self.config.get('repositories', []), key=lambda r: r.get('priority', 99)):
            if repo['name'] == 'pypi':
                continue
            
            packages = self.fetch_repo_index(repo)
            for pkg_name, pkg_info in packages.items():
                if query_lower in pkg_name.lower():
                    results.append({
                        'name': pkg_name,
                        'repository': repo['name'],
                        'url': repo['url'],
                        'installed': pkg_name in self.config.get('packages', {}),
                        **pkg_info
                    })
        
        if not results:
            print("No packages found.")
        else:
            print(f"\nFound {len(results)} package(s):\n")
            for r in results:
                status = "✓ installed" if r['installed'] else "○ available"
                print(f"  [{status}] {r['name']} ({r['repository']})")
        
        return results
    
    def install(self, package: str, version: str = None, repo: str = None) -> bool:
        """Install a package from repositories"""
        print(f"Installing {package}...")
        
        # Check if already installed
        if package in self.config.get('packages', {}):
            print(f"Package '{package}' is already installed.")
            print(f"  Use 'mylang --update {package}' to update.")
            return True
        
        # Search in repositories
        found = None
        found_repo = None
        
        repos = self.config.get('repositories', [])
        # Sort by priority
        repos_sorted = sorted(repos, key=lambda r: r.get('priority', 99))
        
        for r in repos_sorted:
            if repo and r['name'] != repo:
                continue
                
            if r['name'] == 'pypi':
                # Try PyPI
                try:
                    result = subprocess.run(
                        [sys.executable, '-m', 'pip', 'install', package],
                        capture_output=True, text=True, timeout=60
                    )
                    if result.returncode == 0:
                        self.config.setdefault('packages', {})[package] = {
                            'source': 'pypi',
                            'version': version or 'latest',
                            'installed_at': datetime.now().isoformat(),
                        }
                        self.save_config(self.config)
                        print(f"✓ Installed {package} from PyPI.")
                        return True
                except:
                    pass
                continue
            
            # Try to fetch from GitHub repo
            packages = self.fetch_repo_index(r)
            if package in packages:
                found = packages[package]
                found_repo = r
                break
        
        if not found:
            print(f"✗ Package '{package}' not found in any repository.")
            return False
        
        # Download and install
        try:
            package_dir = PACKAGES_DIR / package
            package_dir.mkdir(parents=True, exist_ok=True)
            
            if found.get('type') == 'directory':
                # Download directory contents
                self._download_package_dir(found_repo, found['path'], package_dir)
            else:
                # Download single file
                download_url = found.get('download_url', '')
                if not download_url:
                    # Construct download URL
                    download_url = self._construct_download_url(found_repo, package)
                
                package_file = package_dir / f"{package}.ml"
                self._download_file(download_url, package_file)
            
            # Save to config
            self.config.setdefault('packages', {})[package] = {
                'source': found_repo['name'],
                'version': version or 'latest',
                'installed_at': datetime.now().isoformat(),
                'repository_url': found_repo['url'],
            }
            self.save_config(self.config)
            
            print(f"✓ Successfully installed {package} from {found_repo['name']}.")
            return True
            
        except Exception as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    
    def _construct_download_url(self, repo: dict, package: str) -> str:
        """Construct download URL for a package"""
        if 'github.com' in repo.get('url', ''):
            base = repo['url'].replace('github.com', 'raw.githubusercontent.com')
            branch = repo.get('branch', 'main')
            repo_path = repo.get('repo_path', 'repo')
            return f"{base}/{branch}/{repo_path}/{package}.ml"
        return ""
    
    def _download_file(self, url: str, dest: Path):
        """Download a file from URL"""
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _download_package_dir(self, repo: dict, path: str, dest: Path):
        """Download a package directory from GitHub"""
        api_url = f"{GITHUB_API}/repos/{self._extract_github_repo(repo['url'])}/contents/{path}"
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            
            for item in data:
                if item['type'] == 'file':
                    file_path = dest / item['name']
                    self._download_file(item['download_url'], file_path)
                elif item['type'] == 'dir':
                    sub_dir = dest / item['name']
                    sub_dir.mkdir(exist_ok=True)
                    self._download_package_dir(repo, item['path'], sub_dir)

    def uninstall(self, package: str) -> bool:
        """Uninstall a package"""
        if package not in self.config.get('packages', {}):
            print(f"Package '{package}' is not installed.")
            return False

        pkg_info = self.config['packages'][package]

        if pkg_info.get('source') == 'pypi':
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'uninstall', '-y', package],
                capture_output=True, text=True
            )

        # Remove package directory
        package_dir = PACKAGES_DIR / package
        if package_dir.exists():
            shutil.rmtree(package_dir)

        # Remove from config
        del self.config['packages'][package]
        self.save_config(self.config)

        print(f"✓ Uninstalled {package}.")
        return True

    def list_packages(self) -> List[dict]:
        """List installed packages"""
        packages = []
        for name, info in self.config.get('packages', {}).items():
            packages.append({
                'name': name,
                'source': info.get('source', 'unknown'),
                'version': info.get('version', 'unknown'),
                'installed_at': info.get('installed_at', 'unknown'),
            })
        return packages
    
    def update(self, package: str = None) -> bool:
        """Update a package or all packages"""
        if package:
            if package not in self.config.get('packages', {}):
                print(f"Package '{package}' is not installed.")
                return False

            pkg_info = self.config['packages'][package]
            print(f"Updating {package}...")

            if pkg_info.get('source') == 'pypi':
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '--upgrade', package],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    print(f"✓ Updated {package}.")
                    return True
            else:
                # Reinstall from repository
                self.uninstall(package)
                return self.install(package)
        else:
            # Update all packages
            for pkg in list(self.config.get('packages', {}).keys()):
                self.update(pkg)
            return True

        return False

    def info(self, package: str) -> dict:
        """Get information about a package"""
        if package not in self.config.get('packages', {}):
            # Try to find in repositories
            for repo in self.config.get('repositories', []):
                if repo['name'] == 'pypi':
                    continue
                packages = self.fetch_repo_index(repo)
                if package in packages:
                    return {
                        'name': package,
                        'installed': False,
                        'repository': repo['name'],
                        'url': repo['url'],
                        **packages[package]
                    }
            return {'error': f"Package '{package}' not found."}

        info = self.config['packages'][package]
        package_dir = PACKAGES_DIR / package

        return {
            'name': package,
            'installed': True,
            'source': info.get('source'),
            'version': info.get('version'),
            'installed_at': info.get('installed_at'),
            'repository_url': info.get('repository_url'),
            'path': str(package_dir),
            'files': list(str(f) for f in package_dir.glob('**/*')) if package_dir.exists() else [],
        }

# =============================================================================
# PROJECT INITIALIZER
# =============================================================================

def init_project(name: str):
    """Initialize a new MyLang project"""
    project_dir = Path(name)
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create directory structure
    (project_dir / 'src').mkdir(exist_ok=True)
    (project_dir / 'lib').mkdir(exist_ok=True)
    (project_dir / 'tests').mkdir(exist_ok=True)

    # Create main file
    main_file = project_dir / 'src' / 'main.ml'
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(f'''# {name} - MyLang Project
# Version: 0.1.0

# Main entry point
fn main() {{
    print("Hello from {name}!")
}}

# Run main
main()
''')

    # Create config file
    config_file = project_dir / 'mylang.json'
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump({
            'name': name,
            'version': '0.1.0',
            'main': 'src/main.ml',
            'dependencies': {},
            'author': '',
            'description': '',
        }, f, indent=2)

    # Create README
    readme_file = project_dir / 'README.md'
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(f'''# {name}

A MyLang project.

## Usage

```bash
python3 mylang.py --run src/main.ml
```

## Build

```bash
python3 mylang.py --compile src/main.ml
```
''')

    # Create test file
    test_file = project_dir / 'tests' / 'test.ml'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(f'''# Tests for {name}

fn test_example() {{
    let result = 1 + 1
    assert(result == 2, "1 + 1 should equal 2")
    print("Test passed!")
}}

test_example()
''')

    print(f"Created project: {name}")
    print(f"\nProject structure:")
    print(f"  {name}/")
    print(f"  ├── src/")
    print(f"  │   └── main.ml")
    print(f"  ├── lib/")
    print(f"  ├── tests/")
    print(f"  │   └── test.ml")
    print(f"  ├── mylang.json")
    print(f"  └── README.md")
    print(f"\nRun with: python3 mylang.py --run {name}/src/main.ml")

# =============================================================================
# CLI INTERFACE
# =============================================================================

def create_parser():
    parser = argparse.ArgumentParser(
        description='MyLang - Modern Programming Language',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 mylang.py --version                 Show version
  python3 mylang.py --init myproject          Create new project
  python3 mylang.py --run app.ml              Run MyLang file
  python3 mylang.py --compile app.ml          Compile to Python
  
Package Management:
  python3 mylang.py --install requests        Install package
  python3 mylang.py --uninstall requests      Uninstall package
  python3 mylang.py --list                    List installed packages
  python3 mylang.py --search http             Search packages
  
Repository Management:
  python3 mylang.py --repo-add name url       Add repository
  python3 mylang.py --repo-remove name        Remove repository
  python3 mylang.py --repo-list               List repositories
  python3 mylang.py --repo-update             Update repository indexes
        '''
    )

    # Main commands
    parser.add_argument('--version', '-v', action='store_true',
                        help='Show MyLang version')
    parser.add_argument('--init', metavar='NAME',
                        help='Initialize a new project')
    parser.add_argument('--run', metavar='FILE',
                        help='Run a MyLang file')
    parser.add_argument('--compile', metavar='FILE',
                        help='Compile MyLang to Python')
    parser.add_argument('--output', '-o', metavar='FILE',
                        help='Output file for compilation')

    # Package management
    pkg_group = parser.add_argument_group('Package Management')
    pkg_group.add_argument('--install', metavar='PACKAGE',
                           help='Install a package')
    pkg_group.add_argument('--uninstall', metavar='PACKAGE',
                           help='Uninstall a package')
    pkg_group.add_argument('--update', nargs='?', const='all', metavar='PACKAGE',
                           help='Update package(s)')
    pkg_group.add_argument('--list', action='store_true',
                           help='List installed packages')
    pkg_group.add_argument('--search', metavar='QUERY',
                           help='Search for packages')
    pkg_group.add_argument('--info', metavar='PACKAGE',
                           help='Show package information')

    # Repository management
    repo_group = parser.add_argument_group('Repository Management')
    repo_group.add_argument('--repo-add', nargs=2, metavar=('NAME', 'URL'),
                           help='Add a package repository')
    repo_group.add_argument('--repo-remove', metavar='NAME',
                           help='Remove a repository')
    repo_group.add_argument('--repo-list', action='store_true',
                           help='List all repositories')
    repo_group.add_argument('--repo-update', action='store_true',
                           help='Update repository indexes')
    repo_group.add_argument('--repo-path', metavar='PATH', default='repo',
                           help='Path to packages in repository (default: repo)')
    repo_group.add_argument('--repo-branch', metavar='BRANCH', default='main',
                           help='Repository branch (default: main)')

    # REPL
    parser.add_argument('--repl', action='store_true',
                        help='Start interactive REPL')

    # Additional options
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')

    return parser

def run_file(filename: str, debug: bool = False):
    """Run a MyLang file"""
    filepath = Path(filename)

    if not filepath.exists():
        print(f"Error: File not found: {filename}", file=sys.stderr)
        return 1

    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    interpreter = Interpreter()

    try:
        start_time = time.time()
        result = interpreter.run(source, filename)
        end_time = time.time()

        if debug:
            print(f"\n[Debug] Execution time: {(end_time - start_time) * 1000:.2f}ms")

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if debug:
            import traceback
            traceback.print_exc()
        return 1

def compile_file(filename: str, output: str = None, debug: bool = False):
    """Compile MyLang to Python"""
    filepath = Path(filename)

    if not filepath.exists():
        print(f"Error: File not found: {filename}", file=sys.stderr)
        return 1

    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        compiler = PythonCompiler()
        python_code = compiler.compile(ast)

        if output:
            output_path = Path(output)
        else:
            output_path = filepath.with_suffix('.py')

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(python_code)

        print(f"Compiled to: {output_path}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if debug:
            import traceback
            traceback.print_exc()
        return 1

def start_repl():
    """Start interactive REPL"""
    print(f"MyLang {VERSION}")
    print("Type 'exit' to quit, 'help' for more information.\n")

    interpreter = Interpreter()
    line_number = 1

    while True:
        try:
            line = input(f"mylang:{line_number}> ")

            if line.strip() == 'exit':
                print("Goodbye!")
                break

            if line.strip() == 'help':
                print("""
MyLang REPL Commands:
  exit     - Exit the REPL
  help     - Show this help
  clear    - Clear the screen
  reset    - Reset the environment

Language Features:
  let x = 10                  Variable declaration
  const PI = 3.14             Constant declaration
  fn greet(name) { ... }      Function definition
  if x > 0 { ... }            Conditional
  loop i in range(10) { ... } For loop
  while x > 0 { ... }         While loop
  class Person { ... }        Class definition

Built-in Functions:
  print, input, len, range, type, str, int, float
  list, dict, map, filter, reduce, sorted, reversed
  min, max, sum, abs, round, floor, ceil, sqrt
  random, randint, choice, shuffle
  time, sleep, json_parse, json_stringify
  open, read, write, exists, mkdir, listdir
""")
                continue

            if line.strip() == 'clear':
                os.system('clear' if os.name != 'nt' else 'cls')
                continue

            if line.strip() == 'reset':
                interpreter = Interpreter()
                print("Environment reset.")
                continue

            # Handle multi-line input
            if line.strip().endswith('{'):
                while True:
                    next_line = input("... ")
                    line += '\n' + next_line
                    if next_line.strip() == '}' or (next_line.strip() and not next_line.strip().endswith('{')):
                        break

            result = interpreter.run(line)
            if result is not None:
                print(f"=> {result}")

            line_number += 1

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

    return 0

def main():
    parser = create_parser()
    args = parser.parse_args()

    # Version
    if args.version:
        print(f"MyLang {VERSION}")
        print("A modern programming language with Python interoperability.")
        return 0

    # Initialize project
    if args.init:
        init_project(args.init)
        return 0

    # Run file
    if args.run:
        return run_file(args.run, args.debug)

    # Compile file
    if args.compile:
        return compile_file(args.compile, args.output, args.debug)

    # Package management
    pkg_manager = PackageManager()

    if args.install:
        success = pkg_manager.install(args.install)
        return 0 if success else 1

    if args.uninstall:
        success = pkg_manager.uninstall(args.uninstall)
        return 0 if success else 1

    if args.update is not None:
        if args.update == 'all':
            success = pkg_manager.update()
        else:
            success = pkg_manager.update(args.update)
        return 0 if success else 1

    if args.list:
        packages = pkg_manager.list_packages()
        if packages:
            print("Installed packages:\n")
            for pkg in packages:
                print(f"  {pkg['name']}")
                print(f"    Source: {pkg['source']}")
                print(f"    Version: {pkg['version']}")
                print(f"    Installed: {pkg['installed_at']}")
                print()
        else:
            print("No packages installed.")
        return 0

    if args.search:
        pkg_manager.search(args.search)
        return 0

    if args.info:
        info = pkg_manager.info(args.info)
        if 'error' in info:
            print(info['error'])
            return 1
        print(f"Package: {info['name']}")
        print(f"Installed: {info.get('installed', False)}")
        if info.get('installed'):
            print(f"Source: {info['source']}")
            print(f"Version: {info['version']}")
            print(f"Installed at: {info['installed_at']}")
            print(f"Path: {info['path']}")
        else:
            print(f"Repository: {info.get('repository', 'unknown')}")
        return 0

    # Repository management
    if args.repo_add:
        name, url = args.repo_add
        success = pkg_manager.add_repo(
            name, 
            url, 
            branch=getattr(args, 'repo_branch', 'main'),
            repo_path=getattr(args, 'repo_path', 'repo')
        )
        return 0 if success else 1

    if args.repo_remove:
        success = pkg_manager.remove_repo(args.repo_remove)
        return 0 if success else 1

    if args.repo_list:
        repos = pkg_manager.list_repos()
        print("Configured repositories:\n")
        for i, repo in enumerate(repos, 1):
            priority = repo.get('priority', 99)
            print(f"  [{i}] {repo['name']}")
            print(f"      URL: {repo.get('url', 'N/A')}")
            if repo.get('branch'):
                print(f"      Branch: {repo.get('branch', 'main')}")
            if repo.get('repo_path'):
                print(f"      Path: {repo.get('repo_path', 'repo')}")
            print(f"      Priority: {priority}")
            print()
        return 0

    if args.repo_update:
        pkg_manager.update_repos()
        return 0

    # REPL
    if args.repl:
        return start_repl()

    # No arguments - show help
    parser.print_help()
    return 0

if __name__ == '__main__':
    sys.exit(main())
