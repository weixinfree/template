#!/usr/bin/env python3

import functools
import itertools
import os
import re
import math
from functools import lru_cache
from typing import Sequence, Tuple

'''
template 
'''

DEBUG_TEMPLATE = False

BUILT_IN_ENV = {
    'os': os,
    're': re,
    'itertools': itertools,
    'functools': functools,
    'math': math
}


class _CodeGenerator:
    def __init__(self):

        self.indent = 0
        self.code = []

        self.code.append('_result = []')
        self.code.append('_append = _result.append')

    @staticmethod
    def _is_control_statement(code):
        code = code.strip()
        control_flags = [
            lambda: code.startswith('if '),
            lambda: code.startswith('elif '),
            lambda: code.startswith('else'),
            lambda: code.startswith('try '),
            lambda: code.startswith('except '),
            lambda: code.startswith('finnaly '),
            lambda: code.startswith('with '),
            lambda: code.startswith('for '),
            lambda: code.startswith('while '),
            lambda: code.startswith('class '),
            lambda: code.startswith('def ')
        ]
        return any([is_control() for is_control in control_flags])

    def add_code(self, _code):
        if _code.strip() == 'end':
            self.indent -= 4
        else:
            self.code.append('\n')
            self.code.append(' ' * self.indent + _code.strip())

            if _CodeGenerator._is_control_statement(_code):
                self.indent += 4

    def add_text(self, text):
        self.code.append(' ' * self.indent + f'_append("""{text}""")')

    def add_data(self, data):
        self.code.append(' ' * self.indent + f'_append({data})')

    def handle(self, _type, _data):
        getattr(self, f'add_{_type}')(_data)

    def end(self):
        self.code.append('TMPL_EVAL_RESULT = "".join(_result)')

    def compile(self):
        raw_code = '\n'.join(self.code)

        if DEBUG_TEMPLATE:
            print('>>' * 10, 'start generated code', '<<' * 10)
            print(raw_code)
            print('>>' * 10, 'end generated code', '<<' * 10)

        return compile(raw_code, f'tmpl_{abs(id(self))}.py', 'exec')


class Template:
    def __init__(self, tmpl: str):
        self.tmpl = tmpl

    @staticmethod
    def _split_template(tmpl: str) -> Sequence[Tuple[str, str]]:

        segments = re.finditer(
            r'(?<=\n).*?%\{(?P<code>.*?)\}%.*?\n|\{\{(?P<data>.*?)\}\}', tmpl)

        last_end = 0
        for seg in segments:

            start, end = seg.span()

            if start > last_end:
                text = tmpl[last_end:start]
                yield 'text', text

            code, data = seg.groups()

            if code:
                yield 'code', code
            if data:
                yield 'data', data

            last_end = end

        yield 'text', tmpl[last_end:]

    @lru_cache(maxsize=128)
    def _gen_code(self):
        code_gen = _CodeGenerator()

        [code_gen.handle(_type, _data)
         for _type, _data in Template._split_template(self.tmpl)]

        code_gen.end()

        return code_gen.compile()

    def render(self, eval_env=None):
        compiled_code = self._gen_code()

        env = {**BUILT_IN_ENV}

        if eval_env:
            env.update(eval_env)

        exec(compiled_code, env)

        return env['TMPL_EVAL_RESULT']

        
