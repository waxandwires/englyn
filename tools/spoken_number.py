#!/usr/bin/env python3
# A5 scope (2026-08-17): digits stay digits in accessible names; only units and
# suffixes are spelled ("2.4 million dollars", "12 percent"). This script's spoken
# NUMBER output is for the rare TTS-ambiguous case (year vs quantity, phone number)
# and goes into prose or aria-describedby, never into the name and never beside digits.
"""spoken_number.py — Rule 1 (Numbers, currency, and percentages) converter.

Pure stdlib. No dependencies. Converts a raw numeric string into spoken
English. As of the A5 rescope (2026-08-17), an accessible name never carries
this output — digits stay digits there, with only units and suffixes spelled
("2.4 million dollars", "12 percent"). This script is for the narrower case
where a digit string is ambiguous to TTS (a year read as a quantity, a phone
number): run it and place the output in prose or `aria-describedby`, never in
the accessible name and never beside the digits.

Usage:
    python3 spoken_number.py <value> [--currency|--plain] [--percent]

Examples (these are the exact contract documented in
references/englyn-narration-reference.md — do not change this behavior without
updating that file too):

    python3 spoken_number.py 14200000     -> fourteen point two million dollars
    python3 spoken_number.py 2.4M         -> two point four million dollars
    python3 spoken_number.py '$1,234,567' -> one point two million dollars
    python3 spoken_number.py 42%          -> forty-two percent
    python3 spoken_number.py 4.5          -> four point five
    python3 spoken_number.py 325000       -> three hundred twenty-five thousand dollars

Heuristic (override with --currency / --plain / --percent):
    - Trailing '%' -> percent mode, never currency.
    - Leading '$', or magnitude >= 1000 with no other signal -> currency
      (dollars appended). A bare number under 1000 (e.g. "4.5" minutes,
      "87" percent-less score) is read plain, matching how this script is
      used elsewhere in the skill for non-monetary stats.
    - Magnitude >= 1,000,000 -> scaled reading ("fourteen point two
      million") rather than the fully spelled-out integer. Below that,
      the full integer is spelled out ("three hundred twenty-five
      thousand"). This matches the two worked examples above.
    - K/M/B/T suffix (e.g. "2.4M") is an explicit scale multiplier.
"""
import sys
from typing import Optional

ONES = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]
TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
    "eighty", "ninety",
]
SCALES = ["", "thousand", "million", "billion", "trillion", "quadrillion"]

SCALE_SUFFIXES = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}
# Largest-first: the biggest scale name that fits the magnitude wins.
SCALE_NAMES = [(1e12, "trillion"), (1e9, "billion"), (1e6, "million")]


def _three_digit_words(n: int) -> str:
    """n in 0..999 -> words, e.g. 325 -> 'three hundred twenty-five'."""
    parts = []
    hundreds, remainder = divmod(n, 100)
    if hundreds:
        parts.append(f"{ONES[hundreds]} hundred")
    if remainder:
        if remainder < 20:
            parts.append(ONES[remainder])
        else:
            tens_digit, ones_digit = divmod(remainder, 10)
            parts.append(
                f"{TENS[tens_digit]}-{ONES[ones_digit]}" if ones_digit
                else TENS[tens_digit]
            )
    return " ".join(parts)


def int_to_words(n: int) -> str:
    """Full integer -> spelled-out English words."""
    if n == 0:
        return "zero"
    neg = n < 0
    n = abs(n)
    groups = []
    while n > 0:
        n, rem = divmod(n, 1000)
        groups.append(rem)
    parts = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        scale = SCALES[i] if i < len(SCALES) else ""
        chunk = f"{_three_digit_words(g)} {scale}".strip()
        parts.append(chunk)
    result = " ".join(parts)
    return f"negative {result}" if neg else result


def number_to_spoken(value: float) -> str:
    """int or float -> words, with '.5' style fractions read as 'point five'."""
    # Fixed-point formatting avoids float repr artifacts (e.g. 4.5 -> 4.4999999...)
    s = f"{value:.6f}".rstrip("0").rstrip(".")
    int_part, _, frac_part = s.partition(".")
    neg = int_part.startswith("-")
    if neg:
        int_part = int_part[1:]
    words = int_to_words(int(int_part or "0"))
    if neg and not words.startswith("negative"):
        words = f"negative {words}"
    if frac_part:
        digit_words = " ".join(ONES[int(d)] for d in frac_part)
        words += f" point {digit_words}"
    return words


def spoken_number(raw: str, currency: Optional[bool] = None, percent: Optional[bool] = None) -> str:
    """Convert a raw value string (see module docstring) to spoken English."""
    s = raw.strip()

    ends_percent = s.endswith("%")
    if ends_percent:
        s = s[:-1]
    is_percent = ends_percent if percent is None else percent

    starts_dollar = s.startswith("$")
    if starts_dollar:
        s = s[1:]
    s = s.replace(",", "").strip()

    scale_suffix = None
    if s and s[-1].upper() in SCALE_SUFFIXES:
        scale_suffix = s[-1].upper()
        s = s[:-1]

    value = float(s)
    multiplier = SCALE_SUFFIXES.get(scale_suffix, 1.0)
    actual = value * multiplier

    if is_percent:
        return f"{number_to_spoken(value)} percent"

    use_currency = (starts_dollar or abs(actual) >= 1000) if currency is None else currency

    abs_actual = abs(actual)
    words = None
    if abs_actual >= 1_000_000:
        for factor, name in SCALE_NAMES:
            if abs_actual >= factor:
                scaled = round(actual / factor, 1)
                words = f"{number_to_spoken(scaled)} {name}"
                break
    if words is None:
        words = number_to_spoken(actual)

    if use_currency:
        words += " dollars"
    return words


def _selftest() -> None:
    assert int_to_words(0) == "zero"
    assert int_to_words(19) == "nineteen"
    assert int_to_words(100) == "one hundred"
    assert int_to_words(325) == "three hundred twenty-five"
    assert int_to_words(1_000_000_000) == "one billion"

    assert spoken_number("14200000") == "fourteen point two million dollars"
    assert spoken_number("2.4M") == "two point four million dollars"
    # gate-annotation: check6 -- test fixture, not a business figure. This case
    # exists to pin the millions-scale comma path, which no other assertion covers.
    assert spoken_number("$1,234,567") == "one point two million dollars"  # gate-annotation: check6 -- fixture value, see above
    assert spoken_number("42%") == "forty-two percent"
    assert spoken_number("4.5") == "four point five"
    assert spoken_number("325000") == "three hundred twenty-five thousand dollars"
    assert spoken_number("0") == "zero"
    assert spoken_number("87", currency=False) == "eighty-seven"
    assert spoken_number("1000000", currency=False) == "one million"


if __name__ == "__main__":
    _selftest()  # ponytail: gate on every invocation, not just CI — cheap and load-bearing

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    flags = sys.argv[2:]
    currency_flag = True if "--currency" in flags else (False if "--plain" in flags else None)
    percent_flag = True if "--percent" in flags else None
    print(spoken_number(sys.argv[1], currency=currency_flag, percent=percent_flag))
