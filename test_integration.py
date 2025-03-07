from typing import Sequence, Iterable

import pytest
from _pytest.mark.structures import ParameterSet
from utils.testsuite import TestSuite

INTEGRATION_TEST_CASES = ["test2/test", "test3/test", "test4/test"]
ASSEMBLIED_TEST_CASES = ["o0", "o1", "o2"]


def parametrize(
    arg_name: str | Sequence[str],
    test_cases: Iterable[ParameterSet | Sequence[object] | object],
    target: str,
):
    return pytest.mark.parametrize(
        argnames=arg_name,
        argvalues=test_cases,
        ids=[f"{target}_{name}" for name in test_cases],
    )


# @pytest.mark.depends()
@parametrize("name", INTEGRATION_TEST_CASES, "formatter_nj")
def test_formatter_nj_success(name: str):
    assert TestSuite.FormatterNJ().test(name)


# @pytest.mark.depends(on=["test_formatter_nj_success"])
@parametrize("name", INTEGRATION_TEST_CASES, "compiler")
def test_compiler_success(name: str):
    assert TestSuite.Compiler().test(name)


# @pytest.mark.depends(on=["test_compiler_success"])
@parametrize("name", INTEGRATION_TEST_CASES, "formatter_vm")
def test_formatter_vm_success(name: str):
    assert TestSuite.FormatterVM().test(name)


# @pytest.mark.depends(on=["test_formatter_nj_success"])
@parametrize("name", INTEGRATION_TEST_CASES, "assembler_o1")
def test_assembler_o1_success(name: str):
    assert TestSuite.AssemblerO1().test(name)


# @pytest.mark.depends(on=["test_formatter_nj_success"])
@parametrize("name", INTEGRATION_TEST_CASES, "assembler_o2")
def test_assembler_o2_success(name: str):
    assert TestSuite.AssemblerO2().test(name)


# @pytest.mark.depends(on=["test_formatter_nj_success"])
@parametrize("name", INTEGRATION_TEST_CASES, "assembler_o3")
def test_assembler_o3_success(name: str):
    assert TestSuite.AssemblerO3().test(name)


# @pytest.mark.depends(on=["test_formatter_nj_success"])
# @parametrize("name", ASSEMBLIED_TEST_CASES, "format_assemblied")
# def test_format_assemblied_success(name: str):
#     assert TestSuite.FormatterVM().test(name)

# TODO: Group by test case
