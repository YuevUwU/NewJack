import logging

import pytest
from rich.logging import RichHandler

from compiler import main as compiler
import format

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


def builder(name: str, will_err: bool = False) -> bool:
    errout, _, success = compiler.main(f"{name}/test.nj")

    errout_str = "\n".join(errout)
    if not (success ^ will_err):
        pytest.fail(errout_str)

    try:
        format.main(f"{name}/test.vm", "vm")
    except Exception as e:
        pytest.fail("Formatter Error:\n" + str(e))

    logger.info(f"✅ Test '{name}' passed successfully!")

    if errout_str:
        logger.debug(
            "============================== Output ==============================="
        )
        for out in errout_str.split("\n"):
            logger.debug(out)

    return True


def test_test2():
    assert builder("test2")


def test_test3():
    assert builder("test3")


def test_test4():
    assert builder("test4")
