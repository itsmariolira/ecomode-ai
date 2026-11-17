"""EcoMode: compact terminal output without hiding important messages."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable

__version__ = "0.1.0"

DEFAULT_MAX_LINES = 200

_IMPORTANT_RE = re.compile(
    r"(?:\berror\b|\berro\b|\bwarning\b|\bwarn\b|\baviso\b|"
    r"\bcritical\b|\bcr[ií]tico\b|\bfatal\b|\bfailed\b|\bfalha\b|"
    r"\bexception\b|\btraceback\b|\bpanic\b|\bassertionerror\b|"
    r"\b[a-z_][a-z0-9_]*error\b)",
    re.IGNORECASE,
)
_TRACEBACK_FRAME_RE = re.compile(r'^\s*File ".+", line \d+')


def is_important(line: str) -> bool:
    """Return True for errors, warnings, and common traceback lines."""

    return bool(_IMPORTANT_RE.search(line) or _TRACEBACK_FRAME_RE.search(line))


def compact_lines(lines: Iterable[str], max_lines: int = DEFAULT_MAX_LINES) -> list[str]:
    """Remove duplicate normal lines and cap them, always keeping important lines.

    Exact duplicate non-important lines are kept once. Important lines are never
    removed, even when repeated or found after the normal-line limit.
    """

    if max_lines < 0:
        raise ValueError("max_lines must be zero or greater")

    output: list[str] = []
    seen_normal: set[str] = set()
    kept_normal = 0
    duplicate_count = 0
    limited_count = 0

    for raw_line in lines:
        line = raw_line.rstrip("\r\n")

        if is_important(line):
            output.append(line)
            continue

        if line in seen_normal:
            duplicate_count += 1
            continue

        seen_normal.add(line)
        if kept_normal < max_lines:
            output.append(line)
            kept_normal += 1
        else:
            limited_count += 1

    summaries = []
    if duplicate_count:
        summaries.append(f"{duplicate_count} linha(s) repetida(s)")
    if limited_count:
        summaries.append(f"{limited_count} linha(s) excedente(s)")
    if summaries:
        output.append("[EcoMode] Omitidas: " + "; ".join(summaries) + ".")

    return output


def compact_text(text: str, max_lines: int = DEFAULT_MAX_LINES) -> str:
    """Compact a text block and return it with a final newline when non-empty."""

    compacted = compact_lines(text.splitlines(), max_lines=max_lines)
    return "\n".join(compacted) + ("\n" if compacted else "")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ecomode",
        description=(
            "Remove linhas repetidas e limita saídas longas, preservando erros "
            "e avisos. Lê um arquivo ou a entrada padrão."
        ),
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Arquivo de texto. Se omitido, lê da entrada padrão.",
    )
    parser.add_argument(
        "-n",
        "--max-lines",
        type=int,
        default=DEFAULT_MAX_LINES,
        metavar="N",
        help=f"Máximo de linhas normais únicas (padrão: {DEFAULT_MAX_LINES}).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.max_lines < 0:
        parser.error("--max-lines deve ser zero ou maior")

    try:
        if args.file:
            with open(args.file, encoding="utf-8", errors="replace") as stream:
                result = compact_lines(stream, max_lines=args.max_lines)
        else:
            result = compact_lines(sys.stdin, max_lines=args.max_lines)
    except OSError as exc:
        print(f"ecomode: erro ao ler a entrada: {exc}", file=sys.stderr)
        return 1

    if result:
        sys.stdout.write("\n".join(result) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
