from enum import Enum
from typing import Iterable
from treeify.node import Node
from treeify.options import Options

def prefix_with(prefix: str, lines: list[str]) -> Iterable[str]:
    for line in lines:
        yield prefix + line

class NodeKind(Enum):
    DEFAULT = 0
    LAST = 1
    ROOT = 2

def generate_node(node: Node, opts: Options, kind: NodeKind=NodeKind.DEFAULT) -> Iterable[str]:
    # Compute prefix
    if kind == NodeKind.ROOT:
        prefix = ''
    else:
        if kind == NodeKind.DEFAULT:
            prefix = '-' if opts.ascii_only else '├─'
        elif kind == NodeKind.LAST:
            prefix = '-' if opts.ascii_only else '└─'
        else:
            raise ValueError(f'Unimplemented node kind: {kind}')
        prefix = f'{prefix} '

    # Compute indent
    if kind == NodeKind.ROOT:
        indent = ''
    elif opts.ascii_only or kind == NodeKind.LAST:
        indent = ' ' * len(prefix)
    else:
        indent = '│' + (' ' * (len(prefix) - 1))

    # Assemble lines
    yield prefix + node.name
    for i, child in enumerate(node.children):
        child_kind = NodeKind.LAST if i == len(node.children) - 1 else NodeKind.DEFAULT
        yield from prefix_with(indent, list(generate_node(child, opts, child_kind)))

def generate(node: Node, opts: Options) -> str:
    return '\n'.join(generate_node(node, opts, NodeKind.ROOT))
