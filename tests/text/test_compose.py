import pytest

from outlines.text import compose, string
from outlines.text.basic import Add
from outlines.text.var import StringConstant, StringVariable


def test_template_text():
    with pytest.raises(NameError):
        compose("String ${one}", two="two")

    t = compose("Test")
    assert t == "Test"

    t = compose("Test ${variable}", variable="string")
    assert t == "Test string"

    t = compose("Test ${variable}", variable=1)
    assert t == "Test 1"

    t = compose("Test repeated ${variable} ${variable}", variable="string")
    assert t == "Test repeated string string"

    t = compose("Test ${one} ${two}", one="1", two="2")
    assert t == "Test 1 2"


def test_template_string_variable():
    variable = string()
    t = compose("Test ${variable}", variable=variable)
    assert isinstance(t.owner.op, Add)
    assert isinstance(t.owner.inputs[0], StringConstant)
    assert isinstance(t.owner.inputs[1], StringVariable)
    assert t.owner.inputs[0].value == "Test "

    variable = string()
    t = compose("${variable} test", variable=variable)
    assert isinstance(t.owner.op, Add)
    assert isinstance(t.owner.inputs[0], StringVariable)
    assert isinstance(t.owner.inputs[1], StringConstant)
    assert t.owner.inputs[1].value == " test"


def test_template_few_shots():
    wa = string()
    examples = [["here", "there"], ["this", "that"]]
    prompt = compose(
        """
        This is a test

        ${wa}

        % for s, t in examples:
        Search: ${s}
        Trap: ${t}
        % endfor
        """,
        wa=wa,
        examples=examples,
    )
    assert isinstance(prompt, StringVariable)