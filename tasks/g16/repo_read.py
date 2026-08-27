"""저장소 하나를 5분에 훑는 순서.

읽는 것이 아니라 세는 것이다. 5분에 읽을 수 있는 코드는 없고, 5분에 셀 수 있는 것은 있다.
세는 대상은 이 책의 과제 코드베이스 자체다. 독자가 받아서 그대로 돌려 볼 수 있다.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

# 훑는 대상은 12장에서 완성한 꾸러미 하나다. 저장소 전체가 아니라 한 꾸러미를 잡는다.
# 5분에 볼 수 있는 크기가 그 정도이고, 크기를 먼저 정하는 것이 이 절차의 첫 줄이다.
TARGET = Path(__file__).resolve().parent.parent / "g12"


@dataclass(frozen=True)
class RepoView:
    code_files: int
    test_files: int
    code_lines: int
    asserts: int
    documented: int
    undocumented: int
    marked_defects: int


def python_files(target: Path = TARGET) -> list[Path]:
    return sorted(
        p for p in target.rglob("*.py")
        if "__pycache__" not in p.parts and p.name != "__init__.py"
    )


def _functions(tree: ast.AST) -> list[ast.FunctionDef]:
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def look(target: Path = TARGET) -> RepoView:
    code = tests = lines = asserts = documented = undocumented = defects = 0
    for path in python_files(target):
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        is_test = path.name.startswith("test_")
        if is_test:
            tests += 1
            asserts += sum(1 for n in ast.walk(tree) if isinstance(n, ast.Assert))
        else:
            code += 1
            lines += len(text.splitlines())
            for func in _functions(tree):
                if ast.get_docstring(func):
                    documented += 1
                else:
                    undocumented += 1
        if "일부러" in text:
            defects += 1
    return RepoView(code, tests, lines, asserts, documented, undocumented, defects)


def doc_rate(view: RepoView) -> float:
    total = view.documented + view.undocumented
    return round(view.documented / total, 3) if total else 0.0


def asserts_per_test_file(view: RepoView) -> float:
    return round(view.asserts / view.test_files, 1) if view.test_files else 0.0
