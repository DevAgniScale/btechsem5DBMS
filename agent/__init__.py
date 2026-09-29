"""
build_graph is exposed lazily (PEP 562) so that running an individual module
directly - e.g. `python -m agent.loader` - doesn't eagerly import graph.py
and nodes.py just because it's part of the same package.
"""

__all__ = ["build_graph"]


def __getattr__(name):
    if name == "build_graph":
        from .graph import build_graph as _build_graph
        return _build_graph
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
