from abc import ABC, abstractmethod
import logging
from pathlib import Path

from enum import Enum
import pytest
from rich.logging import RichHandler

from compiler import main as compiler
import format as formatter
import assembler


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


class TestExpectancy(Enum):
    SUCCESS = True
    FAIL = False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, bool):
            return self.value == other
        return NotImplemented

    def __bool__(self):
        return self.value
    
    def __str__(self) -> str:
        return self.name
    
    @staticmethod
    def from_bool(bool: bool):
        return SUCCESS if bool else FAIL


SUCCESS = TestExpectancy.SUCCESS
FAIL = TestExpectancy.FAIL


class Test(ABC):
    def __init__(self, *, expected: TestExpectancy = TestExpectancy.SUCCESS):
        self.expected = expected

    @abstractmethod
    def run_test(self, name: str) -> tuple[bool, str]:
        """Execute specific test logic, returning success status and output."""
        raise NotImplementedError

    def test(self, name: str) -> bool:
        """Run the test and handle output and exceptions."""
        try:
            is_success, output = self.run_test(name)
            
            formatted_output = "\n".join(output.split("\n"))
            
            if is_success == self.expected:
                logger.info(
                    "✅ Test '%sTest %s' passed as expected!",
                    self.__class__.__name__,
                    name,
                )
            else:
                pytest.fail(
                    f"❌ Test '{self.__class__.__name__} {name}' did not meet the expected outcome. \n"
                    f"(expected: {self.expected}, actual: {TestExpectancy.from_bool(is_success)})\n"
                    "========== Output ==========\n"
                    f"{formatted_output}"
                )

            if output:
                logger.debug("========== Output ==========")
                logger.debug(formatted_output)
            else:
                logger.debug("========== Output ==========")
                logger.debug("No output received.")

            return is_success
        except Exception as e:  # pylint: disable=broad-exception-caught
            pytest.fail(f"Test failed: \n{e}")


class CompilerTest(Test):
    def run_test(self, name: str):
        out, _, success = compiler.main(f"{name}.nj")
        return success, "\n".join(out)


class FormatterNJTest(Test):
    def run_test(self, name: str):

        nj_file = Path(f"{name}.nj")

        if nj_file.exists():
            formatter.main(f"{name}.nj")
        else:
            pytest.skip(f"{name}.nj not found, skipping format test.")

        return True, ""


class FormatterVMTest(Test):
    def run_test(self, name: str):

        nj_file = Path(f"{name}.vm")

        if nj_file.exists():
            formatter.main(f"{name}.vm")
        else:
            pytest.skip(f"{name}.vm not found, skipping format test.")

        return True, ""


class AssemblerO1Test(Test):
    def run_test(self, name: str):
        assembler.main(f"{name}.nj", [True, False, False])
        return True, ""

class AssemblerO2Test(Test):
    def run_test(self, name: str):
        assembler.main(f"{name}.nj", [False, True, False])
        return True, ""

class AssemblerO3Test(Test):
    def run_test(self, name: str):
        assembler.main(f"{name}.nj", [False, False, True])
        return True, ""


class TestSuite:
    """Manage all test classes."""

    Compiler = CompilerTest
    FormatterNJ = FormatterNJTest
    FormatterVM = FormatterVMTest
    AssemblerO1 = AssemblerO1Test
    AssemblerO2 = AssemblerO2Test
    AssemblerO3 = AssemblerO3Test
