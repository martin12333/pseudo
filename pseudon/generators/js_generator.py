import re
from pseudon.code_generator import CodeGenerator, switch
from pseudon.middlewares import DeclarationMiddleware

JS_NAME = re.compile(r'[a-zA-Z][a-zA-Z_0-9]*')

class JSGenerator(CodeGenerator):
    '''JS generator'''

    indent = 2
    use_spaces = True
    middlewares = [DeclarationMiddleware]

    def handler_(self, node, indent):
        if node.handlers:
            return node.handlers[0].instance
        else:
            return '_e'

    templates = dict(
        module     = "%<dependencies:lines>%<constants:lines>%<definitions:lines>%<main:semi>",

        function_definition   = '''
            function %<name>(%<params:join ','>) {
              %<block:semi>
            }''',

        method_definition =     '''
            %<this>.prototype.%<name> = function (%<params:join ', '>) {
              %<block:semi>
            }''',

        class_definition = '''
              %<.constructor>
              %<.base>
              %<methods:lines>''',

        class_definition_base = ('%<name>.prototype = _.create(%<base>.prototype, {constructor: %<name>})', ''),

        class_definiton_constructor = ('%<constructor>', ''),

        dependency = switch('name',
            lodash = "var _ = require('%<name>');",
            _otherwise = "var %<name> = require('%<name>');"
        ),

        anonymous_function = '''
            function (%<params:join ', '>) {
              %<block:semi>
            }''',

        constructor = '''
            function %<this>(%<params:join ', '>) {
              %<block:semi>
            }''',

        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_single>',
        boolean     = '%<value>',
        null        = 'null',

        list        = "[%<elements:join ', '>]",
        dictionary  = "{%<pairs:join ', '>}",
        pair        = switch(lambda p: p.key.type == 'string' and JS_NAME.match(p.key.value) is not None,
                true = '%<key.value>: %<value>',
                _otherwise = '%<key>: %<value>'
        ),
        attr        = "%<object>.%<attr>",

        custom_exception = '''
            function %<name>(message) {
              this.message = message;
            }

            %<name>.prototype = _.create(%<.base>.prototype, {constructor: %<name>});''',        

        custom_exception_base = ('%<base>', 'Error'),

        assignment    = switch('first_mention',
            true = 'var %<target> = %<value>',
            _otherwise = '%<target> = %<value>'
        ),

        binary_op   = '%<left> %<op> %<right>',
        unary_op    = '%<op>%<value>',
        comparison  = '%<left> %<op> %<right>',

        static_call = "%<receiver>.%<message>(%<args:join ', '>)",
        call        = "%<function>(%<args:join ', '>)",
        method_call = "%<receiver>.%<message>(%<args:join ', '>)",

        this        = 'this',

        instance_variable = 'this.%<name>',

        throw_statement = 'throw new %<exception>(%<value>)',

        if_statement    = '''
            if (%<test>) {
              %<block:semi>
            } %<.otherwise>''',

        if_statement_otherwise = (' %<otherwise>', ''),

        elseif_statement = '''
            else if (%<test>) {
              %<block:semi>
            } %<.otherwise>''',

        elseif_statement_otherwise = (' %<otherwise>', ''),

        else_statement = '''
            else {
              %<block:semi>
            }''',
            

        while_statement = '''
            while (%<test>) {
                %<block:semi>
            }''',

        try_statement = '''
            try {
              %<block:semi>
            } catch(%<#handler_>) {
              if %<handlers:join_depth_aware ' else if '> else {
                throw %<#handler_>;
              }
            }''',

        exception_handler = '''
            (%<instance> isinstanceof %<.is_builtin>) {
              %<block:semi>
            }''', # obvsly its an Error, but we'll have other builtin errors in next versions

        exception_handler_is_builtin = ('Error', '%<exception>'),

        for_statement = '''
            _.forEach(%<sequences>, function (%<iterators>) {
              %<block:semi>
            })''',

        for_range_statement = '''
            for(var %<index> = %<.first>;%<index> != %<last>;%<index> += %<.step>) {
              %<block:semi>
            }''',

        for_range_statement_first = ('%<first>', '0'),

        for_range_statement_step = ('%<step>', '1'),

        for_iterator = '%<iterator>',

        for_iterator_zip = "%<iterators:join ', '>",

        for_iterator_with_index = '%<iterator>, %<index>',

        for_iterator_with_items = '%<value>, %<key>',

        for_sequence = '%<sequence>',

        for_sequence_zip = "_.zip(%<sequences:join ', '>)",

        for_sequence_with_index = '%<sequence>',

        for_sequence_with_items = '%<sequence>',

        tuple = "[%<elements:join ', '>]",

        array = "[%<elements:join ', '>]",

        set   = "{%<.elements>}",

        set_elements = ("%<elements:join ': true, '>: true", ''),

        regex = '/%<value>/',

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>',

        index = switch(
            lambda i: i.index.type == 'string' and JS_NAME.match(i.index.value),
              true       = '%<sequence>.%<index.value>',
              _otherwise = '%<sequence>[%<index>]'
        ),

        constant = '%<constant> = %<init>',

        block = '%<block:semi>'
    )
