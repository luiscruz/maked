# Maked: A Command-Line Tool to Automate Markdown Processing

[![PyPI version](https://img.shields.io/pypi/v/maked)](https://pypi.org/project/maked/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`maked` is a CLI tool that executes shell commands embedded in the YAML front matter of Markdown files. Keep your commands co-located with your documents — no separate `Makefile` or shell script needed.

```bash
pip install maked
```

## Usage

Add a `maked` field to your Markdown file's YAML front matter:

```markdown
---
maked: 'pandoc example.md -o example.pdf'
---

# My Document

Content here.
```

Then run:

```bash
maked example.md
```

You can also pipe content via stdin:

```bash
echo -e "---\nmaked: 'pandoc example.md -o output.pdf'\n---\nSome content here" | maked
```

Preview the command without executing it:

```bash
maked --dry-run example.md
```

## Why Maked?

| | Makefile | Shell script | `maked` |
|---|---|---|---|
| Lives next to your document | ✗ | ✗ | ✓ |
| No extra syntax to learn | ✗ | ✗ | ✓ |
| Works with any shell command | ✓ | ✓ | ✓ |
| Stdin support | ✗ | ✗ | ✓ |

## Installation

```bash
pip install maked
```

Or with Poetry:

```bash
poetry add maked
```

## Contributing

1. Fork the repository and clone it locally.
2. Install dependencies: `poetry install --with dev`
3. Make your changes.
4. Run tests: `poetry run pytest`
5. Open a pull request.
