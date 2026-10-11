"""Patch best-of 0.8.5 to read GitHub stars via the scalar `stargazerCount`.

GitHub now returns FORBIDDEN for `repository.stargazers` to app and
personal tokens, which nulls the whole repository in best-of's query.
"""
import pathlib

import best_of.integrations.github_integration as module

path = pathlib.Path(module.__file__)
source = path.read_text()
replacements = [
    ("    stargazers {\n      totalCount\n    }\n", "    stargazerCount\n"),
    (
        "github_info.stargazers and github_info.stargazers.totalCount",
        "github_info.stargazerCount",
    ),
    ("int(github_info.stargazers.totalCount)", "int(github_info.stargazerCount)"),
]
for old, new in replacements:
    if old not in source:
        raise SystemExit(f"best-of patch failed, pattern not found: {old!r}")
    source = source.replace(old, new)
path.write_text(source)
print(f"Patched {path}")
