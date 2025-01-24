from pycallgraph2 import PyCallGraph
from pycallgraph2 import Config
from pycallgraph2 import GlobbingFilter
from pycallgraph2.output import GraphvizOutput

from compiler import main as compiler_main
import format


def run(path: str, trace_filter=None, config=None, comment=None) -> None:
    if not config:
        config = Config()

    if trace_filter:
        config.trace_filter = trace_filter

    graphviz = GraphvizOutput()
    graphviz.output_type = "svg"
    graphviz.output_file = f'{path.removesuffix("/test.nj")}.svg'

    if comment:
        graphviz.graph_attributes["graph"]["label"] = comment

    with PyCallGraph(config=config, output=graphviz):
        compiler_main.main(path)

    format.main(path.replace("test.nj", "test.vm"), "vm")


def main() -> None:
    trace_filter = GlobbingFilter(include=["compiler.*"])

    tests = ["test2/test.nj", "test3/test.nj", "test4/test.nj"]

    for path in tests:
        run(path, trace_filter=trace_filter, comment="Should show secret_function.")


if __name__ == "__main__":
    main()
