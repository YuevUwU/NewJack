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
            success, output = self.run_test(name)

            if success == self.expected:
                logger.info(
                    "✅ Test '%sTest %s' passed as expected!",
                    self.__class__.__name__,
                    name,
                )
            else:
                pytest.fail(
                    f"❌ Test '{self.__class__.__name__} {name}' did not meet the expected outcome. \n"
                    f"(expected: {self.expected}, actual: {success})"
                )

            if output:
                logger.debug("========== Output ==========")
                logger.debug("\n".join(output.split("\n")))

            return success
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


class AssemblerTest(Test):
    def run_test(self, name: str):
        assembler.main(f"{name}.nj")
        return True, ""


class TestSuite:
    """Manage all test classes."""

    Compiler = CompilerTest
    FormatterNJ = FormatterNJTest
    FormatterVM = FormatterVMTest
    Assembler = AssemblerTest
