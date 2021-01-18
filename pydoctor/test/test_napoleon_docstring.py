
"""
Forked from the tests for :mod:`sphinx.ext.napoleon.docstring` module.
:copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""
import unittest
from unittest import TestCase

from pydoctor.napoleon.docstring import GoogleDocstring
from pydoctor.napoleon import Config


class BaseDocstringTest(TestCase):
    maxDiff = None
class InlineAttributeTest(BaseDocstringTest):

    def test_class_data_member(self):
        docstring = """\
data member description:
- a: b
"""
        actual = str(GoogleDocstring(docstring, is_attribute = True))
        expected = """\
data member description:
- a: b"""   

        self.assertEqual(expected.rstrip(), actual)

    def test_class_data_member_inline(self):
        docstring = """b: data member description with :ref:`reference`"""
        actual = str(GoogleDocstring(docstring, is_attribute = True))
        expected = ("""\
data member description with :ref:`reference`

:type: b""")
        self.assertEqual(expected.rstrip(), actual)

    def test_class_data_member_inline_no_type(self):
        docstring = """data with ``a : in code`` and :ref:`reference` and no type"""
        actual = str(GoogleDocstring(docstring, is_attribute = True))
        expected = """data with ``a : in code`` and :ref:`reference` and no type"""

        self.assertEqual(expected.rstrip(), actual)

    def test_class_data_member_inline_ref_in_type(self):
        docstring = """:class:`int`: data member description"""
        actual = str(GoogleDocstring(docstring, is_attribute = True))
        expected = ("""\
data member description

:type: :class:`int`""")
        self.assertEqual(expected.rstrip(), actual)


class GoogleDocstringTest(BaseDocstringTest):
    docstrings = [(
        """Single line summary""",
        """Single line summary"""
    ), (
        """
Single line summary
Extended description
""",
"""
Single line summary
Extended description
"""
    ), (
        """
Single line summary
Args:
    arg1(str):Extended
        description of arg1
""",
"""
Single line summary
:Parameters: **arg1** (*str*) -- Extended
             description of arg1
        """
    ), (
        """
Single line summary
Args:
    arg1(str):Extended
        description of arg1
    arg2 ( int ) : Extended
        description of arg2
Keyword Args:
    kwarg1(str):Extended
        description of kwarg1
    kwarg2 ( int ) : Extended
        description of kwarg2""",
"""
Single line summary
:Parameters: * **arg1** (*str*) -- Extended
               description of arg1
             * **arg2** (*int*) -- Extended
               description of arg2

:Keyword Arguments: * **kwarg1** (*str*) -- Extended
                      description of kwarg1
                    * **kwarg2** (*int*) -- Extended
                      description of kwarg2
"""
    ), (
        """
Single line summary
Arguments:
    arg1(str):Extended
        description of arg1
    arg2 ( int ) : Extended
        description of arg2
Keyword Arguments:
    kwarg1(str):Extended
        description of kwarg1
    kwarg2 ( int ) : Extended
        description of kwarg2""",
"""
Single line summary
:Parameters: * **arg1** (*str*) -- Extended
               description of arg1
             * **arg2** (*int*) -- Extended
               description of arg2

:Keyword Arguments: * **kwarg1** (*str*) -- Extended
                      description of kwarg1
                    * **kwarg2** (*int*) -- Extended
                      description of kwarg2
        """
    ), (
        """
Single line summary
Return:
    str:Extended
    description of return value
""",
"""
Single line summary
:returns: *str* -- Extended
          description of return value
"""
    ), (
        """
Single line summary
Returns:
    str:Extended
    description of return value
""",
"""
Single line summary
:returns: *str* -- Extended
          description of return value
"""
    ), (
        """
Single line summary
Returns:
    Extended
    description of return value
""",
"""
Single line summary
:returns: Extended
          description of return value
"""
    ), (
        """
Single line summary
Args:
    arg1(str):Extended
        description of arg1
    *args: Variable length argument list.
    **kwargs: Arbitrary keyword arguments.
""",
"""
Single line summary
:Parameters: * **arg1** (*str*) -- Extended
               description of arg1
             * **\\*args** -- Variable length argument list.
             * **\\*\\*kwargs** -- Arbitrary keyword arguments.
"""
    ), (
        """
Single line summary
Args:
    arg1 (list(int)): Description
    arg2 (list[int]): Description
    arg3 (dict(str, int)): Description
    arg4 (dict[str, int]): Description
""",
"""
Single line summary
:Parameters: * **arg1** (*list(int)*) -- Description
             * **arg2** (*list[int]*) -- Description
             * **arg3** (*dict(str, int)*) -- Description
             * **arg4** (*dict[str, int]*) -- Description
"""
    ), (
        """
Single line summary
Receive:
    arg1 (list(int)): Description
    arg2 (list[int]): Description
""",
"""
Single line summary
:Receives: * **arg1** (*list(int)*) -- Description
           * **arg2** (*list[int]*) -- Description
"""
    ), (
        """
Single line summary
Receives:
    arg1 (list(int)): Description
    arg2 (list[int]): Description
""",
"""
Single line summary
:Receives: * **arg1** (*list(int)*) -- Description
           * **arg2** (*list[int]*) -- Description
"""
    ), (
        """
Single line summary
Yield:
    str:Extended
    description of yielded value
""",
"""
Single line summary
:Yields: *str* -- Extended
         description of yielded value
"""
    ), (
        """
Single line summary
Yields:
    Extended
    description of yielded value
""",
"""
Single line summary
:Yields: Extended
         description of yielded value
"""
    )]

    def test_sphinx_admonitions(self):
        admonition_map = {
            'Attention': 'attention',
            'Caution': 'caution',
            'Danger': 'danger',
            'Error': 'error',
            'Hint': 'hint',
            'Important': 'important',
            'Note': 'note',
            'Tip': 'tip',
            'Warning': 'warning',
            'Warnings': 'warning',
        }
        config = Config()
        for section, admonition in admonition_map.items():
            # Multiline
            actual = str(GoogleDocstring(("{}:\n"
                                          "    this is the first line\n"
                                          "\n"
                                          "    and this is the second line\n"
                                          ).format(section), config))
            expect = (".. {}::\n"
                      "\n"
                      "   this is the first line\n"
                      "   \n"
                      "   and this is the second line\n"
                      ).format(admonition)
            self.assertEqual(expect.rstrip(), actual)

            # Single line
            actual = str(GoogleDocstring(("{}:\n"
                                          "    this is a single line\n"
                                          ).format(section), config))
            expect = (".. {}:: this is a single line\n"
                      ).format(admonition)
            self.assertEqual(expect.rstrip(), actual)

    def test_docstrings(self):
        config = Config(
            napoleon_use_param=False,
            napoleon_use_rtype=False,
            napoleon_use_keyword=False
        )
        for docstring, expected in self.docstrings:
            actual = str(GoogleDocstring(docstring, config))
            expected = expected
            self.assertEqual(expected.rstrip(), actual)

    def test_parameters_with_class_reference(self):
        docstring = """\
Construct a new XBlock.
This class should only be used by runtimes.
Arguments:
    runtime (:class:`~typing.Dict`\\[:class:`int`,:class:`str`\\]): Use it to
        access the environment. It is available in XBlock code
        as ``self.runtime``.
    field_data (:class:`FieldData`): Interface used by the XBlock
        fields to access their data from wherever it is persisted.
    scope_ids (:class:`ScopeIds`): Identifiers needed to resolve scopes.
"""

        actual = str(GoogleDocstring(docstring))
        expected = """\
Construct a new XBlock.
This class should only be used by runtimes.
:param runtime: Use it to
                access the environment. It is available in XBlock code
                as ``self.runtime``.
:type runtime: :class:`~typing.Dict`\\[:class:`int`,:class:`str`\\]
:param field_data: Interface used by the XBlock
                   fields to access their data from wherever it is persisted.
:type field_data: :class:`FieldData`
:param scope_ids: Identifiers needed to resolve scopes.
:type scope_ids: :class:`ScopeIds`
"""
        self.assertEqual(expected.rstrip(), actual)

    def test_attributes_with_class_reference(self):
        docstring = """\
Attributes:
    in_attr(:class:`numpy.ndarray`): super-dooper attribute
"""

        actual = str(GoogleDocstring(docstring))
        expected = """\
:ivar in_attr: super-dooper attribute
:type in_attr: :class:`numpy.ndarray`
"""
        self.assertEqual(expected.rstrip(), actual)

        docstring = """\
Attributes:
    in_attr(numpy.ndarray): super-dooper attribute
"""

        actual = str(GoogleDocstring(docstring))
        expected = """\
:ivar in_attr: super-dooper attribute
:type in_attr: numpy.ndarray
"""
        self.assertEqual(expected.rstrip(), actual)

    def test_code_block_in_returns_section(self):
        docstring = """
Returns:
    foobar: foo::
        codecode
        codecode
"""
        expected = """
:returns:
          foo::
              codecode
              codecode
:rtype: foobar
"""
        actual = str(GoogleDocstring(docstring))
        self.assertEqual(expected.rstrip(), actual)

    def test_colon_in_return_type(self):
        docstring = """Example property.
Returns:
    :py:class:`~.module.submodule.SomeClass`: an example instance
    if available, None if not available.
"""
        expected = """Example property.
:returns: an example instance
          if available, None if not available.
:rtype: :py:class:`~.module.submodule.SomeClass`
"""
        actual = str(GoogleDocstring(docstring))
        self.assertEqual(expected.rstrip(), actual)

    def test_xrefs_in_return_type(self):
        docstring = """Example Function
Returns:
    :class:`numpy.ndarray`: A :math:`n \\times 2` array containing
    a bunch of math items
"""
        expected = """Example Function
:returns: A :math:`n \\times 2` array containing
          a bunch of math items
:rtype: :class:`numpy.ndarray`
"""
        actual = str(GoogleDocstring(docstring))
        self.assertEqual(expected.rstrip(), actual)

    def test_raises_types(self):
        docstrings = [("""
Example Function
Raises:
    RuntimeError:
        A setting wasn't specified, or was invalid.
    ValueError:
        Something something value error.
    :py:class:`AttributeError`
        errors for missing attributes.
    ~InvalidDimensionsError
        If the dimensions couldn't be parsed.
    `InvalidArgumentsError`
        If the arguments are invalid.
    :exc:`~ValueError`
        If the arguments are wrong.
""", """
Example Function
:raises RuntimeError: A setting wasn't specified, or was invalid.
:raises ValueError: Something something value error.
:raises AttributeError: errors for missing attributes.
:raises ~InvalidDimensionsError: If the dimensions couldn't be parsed.
:raises InvalidArgumentsError: If the arguments are invalid.
:raises ~ValueError: If the arguments are wrong.
"""),
                      ################################
                      ("""
Example Function
Raises:
    InvalidDimensionsError
""", """
Example Function
:raises InvalidDimensionsError:
"""),
                      ################################
                      ("""
Example Function
Raises:
    Invalid Dimensions Error
""", """
Example Function
:raises Invalid Dimensions Error:
"""),
                      ################################
                      ("""
Example Function
Raises:
    Invalid Dimensions Error: With description
""", """
Example Function
:raises Invalid Dimensions Error: With description
"""),
                      ################################
                      ("""
Example Function
Raises:
    InvalidDimensionsError: If the dimensions couldn't be parsed.
""", """
Example Function
:raises InvalidDimensionsError: If the dimensions couldn't be parsed.
"""),
                      ################################
                      ("""
Example Function
Raises:
    Invalid Dimensions Error: If the dimensions couldn't be parsed.
""", """
Example Function
:raises Invalid Dimensions Error: If the dimensions couldn't be parsed.
"""),
                      ################################
                      ("""
Example Function
Raises:
    If the dimensions couldn't be parsed.
""", """
Example Function
:raises If the dimensions couldn't be parsed.:
"""),
                      ################################
                      ("""
Example Function
Raises:
    :class:`exc.InvalidDimensionsError`
""", """
Example Function
:raises exc.InvalidDimensionsError:
"""),
                      ################################
                      ("""
Example Function
Raises:
    :class:`exc.InvalidDimensionsError`: If the dimensions couldn't be parsed.
""", """
Example Function
:raises exc.InvalidDimensionsError: If the dimensions couldn't be parsed.
"""),
                      ################################
                      ("""
Example Function
Raises:
    :class:`exc.InvalidDimensionsError`: If the dimensions couldn't be parsed,
       then a :class:`exc.InvalidDimensionsError` will be raised.
""", """
Example Function
:raises exc.InvalidDimensionsError: If the dimensions couldn't be parsed,
    then a :class:`exc.InvalidDimensionsError` will be raised.
"""),
                      ################################
                      ("""
Example Function
Raises:
    :class:`exc.InvalidDimensionsError`: If the dimensions couldn't be parsed.
    :class:`exc.InvalidArgumentsError`: If the arguments are invalid.
""", """
Example Function
:raises exc.InvalidDimensionsError: If the dimensions couldn't be parsed.
:raises exc.InvalidArgumentsError: If the arguments are invalid.
"""),
                      ################################
                      ("""
Example Function
Raises:
    :class:`exc.InvalidDimensionsError`
    :class:`exc.InvalidArgumentsError`
""", """
Example Function
:raises exc.InvalidDimensionsError:
:raises exc.InvalidArgumentsError:
""")]
        for docstring, expected in docstrings:
            actual = str(GoogleDocstring(docstring))
            self.assertEqual(expected.rstrip(), actual)

    def test_kwargs_in_arguments(self):
        docstring = """Allows to create attributes binded to this device.
Some other paragraph.
Code sample for usage::
  dev.bind(loopback=Loopback)
  dev.loopback.configure()
Arguments:
  **kwargs: name/class pairs that will create resource-managers
    bound as instance attributes to this instance. See code
    example above.
"""
        expected = """Allows to create attributes binded to this device.
Some other paragraph.
Code sample for usage::
  dev.bind(loopback=Loopback)
  dev.loopback.configure()
:param \\*\\*kwargs: name/class pairs that will create resource-managers
                   bound as instance attributes to this instance. See code
                   example above.
"""
        actual = str(GoogleDocstring(docstring))
        self.assertEqual(expected.rstrip(), actual)

    def test_section_header_formatting(self):
        docstrings = [("""
Summary line
Example:
    Multiline reStructuredText
    literal code block
""", """
Summary line
.. admonition:: Example

   Multiline reStructuredText
   literal code block
"""),
                      ################################
                      ("""
Summary line
Example::
    Multiline reStructuredText
    literal code block
""", """
Summary line
Example::
    Multiline reStructuredText
    literal code block
"""),
                      ################################
                      ("""
Summary line
:Example:
    Multiline reStructuredText
    literal code block
""", """
Summary line
:Example:
    Multiline reStructuredText
    literal code block
""")]
        for docstring, expected in docstrings:
            actual = str(GoogleDocstring(docstring))
            self.assertEqual(expected.rstrip(), actual)

    def test_list_in_parameter_description(self):
        docstring = """One line summary.
Parameters:
    no_list (int):
    one_bullet_empty (int):
        *
    one_bullet_single_line (int):
        - first line
    one_bullet_two_lines (int):
        +   first line
            continued
    two_bullets_single_line (int):
        -  first line
        -  second line
    two_bullets_two_lines (int):
        * first line
          continued
        * second line
          continued
    one_enumeration_single_line (int):
        1.  first line
    one_enumeration_two_lines (int):
        1)   first line
             continued
    two_enumerations_one_line (int):
        (iii) first line
        (iv) second line
    two_enumerations_two_lines (int):
        a. first line
           continued
        b. second line
           continued
    one_definition_one_line (int):
        item 1
            first line
    one_definition_two_lines (int):
        item 1
            first line
            continued
    two_definitions_one_line (int):
        item 1
            first line
        item 2
            second line
    two_definitions_two_lines (int):
        item 1
            first line
            continued
        item 2
            second line
            continued
    one_definition_blank_line (int):
        item 1
            first line
            extra first line
    two_definitions_blank_lines (int):
        item 1
            first line
            extra first line
        item 2
            second line
            extra second line
    definition_after_inline_text (int): text line
        item 1
            first line
    definition_after_normal_text (int):
        text line
        item 1
            first line
"""

        expected = """One line summary.
:param no_list:
:type no_list: int
:param one_bullet_empty:
                         *
:type one_bullet_empty: int
:param one_bullet_single_line:
                               - first line
:type one_bullet_single_line: int
:param one_bullet_two_lines:
                             +   first line
                                 continued
:type one_bullet_two_lines: int
:param two_bullets_single_line:
                                -  first line
                                -  second line
:type two_bullets_single_line: int
:param two_bullets_two_lines:
                              * first line
                                continued
                              * second line
                                continued
:type two_bullets_two_lines: int
:param one_enumeration_single_line:
                                    1.  first line
:type one_enumeration_single_line: int
:param one_enumeration_two_lines:
                                  1)   first line
                                       continued
:type one_enumeration_two_lines: int
:param two_enumerations_one_line:
                                  (iii) first line
                                  (iv) second line
:type two_enumerations_one_line: int
:param two_enumerations_two_lines:
                                   a. first line
                                      continued
                                   b. second line
                                      continued
:type two_enumerations_two_lines: int
:param one_definition_one_line:
                                item 1
                                    first line
:type one_definition_one_line: int
:param one_definition_two_lines:
                                 item 1
                                     first line
                                     continued
:type one_definition_two_lines: int
:param two_definitions_one_line:
                                 item 1
                                     first line
                                 item 2
                                     second line
:type two_definitions_one_line: int
:param two_definitions_two_lines:
                                  item 1
                                      first line
                                      continued
                                  item 2
                                      second line
                                      continued
:type two_definitions_two_lines: int
:param one_definition_blank_line:
                                  item 1
                                      first line
                                      extra first line
:type one_definition_blank_line: int
:param two_definitions_blank_lines:
                                    item 1
                                        first line
                                        extra first line
                                    item 2
                                        second line
                                        extra second line
:type two_definitions_blank_lines: int
:param definition_after_inline_text: text line
                                     item 1
                                         first line
:type definition_after_inline_text: int
:param definition_after_normal_text: text line
                                     item 1
                                         first line
:type definition_after_normal_text: int
"""
        config = Config(napoleon_use_param=True)
        actual = str(GoogleDocstring(docstring, config))
        self.assertEqual(expected.rstrip(), actual)

        expected = """One line summary.
:Parameters: * **no_list** (*int*)
             * **one_bullet_empty** (*int*) --
               *
             * **one_bullet_single_line** (*int*) --
               - first line
             * **one_bullet_two_lines** (*int*) --
               +   first line
                   continued
             * **two_bullets_single_line** (*int*) --
               -  first line
               -  second line
             * **two_bullets_two_lines** (*int*) --
               * first line
                 continued
               * second line
                 continued
             * **one_enumeration_single_line** (*int*) --
               1.  first line
             * **one_enumeration_two_lines** (*int*) --
               1)   first line
                    continued
             * **two_enumerations_one_line** (*int*) --
               (iii) first line
               (iv) second line
             * **two_enumerations_two_lines** (*int*) --
               a. first line
                  continued
               b. second line
                  continued
             * **one_definition_one_line** (*int*) --
               item 1
                   first line
             * **one_definition_two_lines** (*int*) --
               item 1
                   first line
                   continued
             * **two_definitions_one_line** (*int*) --
               item 1
                   first line
               item 2
                   second line
             * **two_definitions_two_lines** (*int*) --
               item 1
                   first line
                   continued
               item 2
                   second line
                   continued
             * **one_definition_blank_line** (*int*) --
               item 1
                   first line
                   extra first line
             * **two_definitions_blank_lines** (*int*) --
               item 1
                   first line
                   extra first line
               item 2
                   second line
                   extra second line
             * **definition_after_inline_text** (*int*) -- text line
               item 1
                   first line
             * **definition_after_normal_text** (*int*) -- text line
               item 1
                   first line
"""
        config = Config(napoleon_use_param=False)
        actual = str(GoogleDocstring(docstring, config))
        self.assertEqual(expected.rstrip(), actual)

    def test_custom_generic_sections(self):

        docstrings = (("""\
Really Important Details:
    You should listen to me!
""", """.. admonition:: Really Important Details

   You should listen to me!
"""),
                      ("""\
Sooper Warning:
    Stop hitting yourself!
""", """:Warns: **Stop hitting yourself!**
"""))

        testConfig = Config(napoleon_custom_sections=['Really Important Details',
                                                      ('Sooper Warning', 'warns')])

        for docstring, expected in docstrings:
            actual = str(GoogleDocstring(docstring, testConfig))
            self.assertEqual(expected.rstrip(), actual)

    def test_attr_with_method(self):
        docstring = """
Attributes:
    arg : description

Methods:
    func(i, j): description
"""

        expected = """
:ivar arg: description

.. method:: func(i, j)

   description
"""  # NOQA
        config = Config()
        actual = str(GoogleDocstring(docstring, config=config))
        self.assertEqual(expected.rstrip(), actual)

    def test_return_formatting_indentation(self):

        docstring = """
Returns:
    bool: True if successful, False otherwise.

    The return type is optional and may be specified at the beginning of
    the ``Returns`` section followed by a colon.

    The ``Returns`` section may span multiple lines and paragraphs.
    Following lines should be indented to match the first line.

    The ``Returns`` section supports any reStructuredText formatting,
    including literal blocks::

        {
            'param1': param1,
            'param2': param2
        }
"""

        expected = """
:returns: True if successful, False otherwise.

          The return type is optional and may be specified at the beginning of
          the ``Returns`` section followed by a colon.

          The ``Returns`` section may span multiple lines and paragraphs.
          Following lines should be indented to match the first line.

          The ``Returns`` section supports any reStructuredText formatting,
          including literal blocks::

              {
                  'param1': param1,
                  'param2': param2
              }
:rtype: bool
""" 

        config = Config()
        actual = str(GoogleDocstring(docstring, config=config))
        self.assertEqual(expected.rstrip(), actual)

if __name__ == "__main__":
    unittest.main()