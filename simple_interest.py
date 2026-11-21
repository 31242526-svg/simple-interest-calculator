"""Simple Interest Calculator.

Computes simple interest with the standard formula

    I = P * (R / 100) * T

where P is the principal, R the annual rate in percent, and T the time in
years. The total amount is A = P + I.

The script works two ways:

    python simple_interest.py --principal 10000 --rate 5 --time 3
    python simple_interest.py            # asks for the three values

Money is handled with Decimal so results are not affected by floating point
rounding.
"""

from __future__ import annotations

import argparse
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

TWO_PLACES = Decimal("0.01")


def simple_interest(principal: Decimal, rate: Decimal, time: Decimal) -> tuple[Decimal, Decimal]:
    """Return (interest, total_amount) for the given values.

    principal: amount borrowed or invested
    rate:      annual rate in percent, e.g. Decimal("5") for 5%
    time:      duration in years
    """
    interest = principal * (rate / Decimal(100)) * time
    total = principal + interest
    return interest.quantize(TWO_PLACES, ROUND_HALF_UP), total.quantize(TWO_PLACES, ROUND_HALF_UP)


def parse_decimal(value: str, name: str) -> Decimal:
    """Convert user input to a Decimal, rejecting anything that is not a number."""
    try:
        number = Decimal(value.strip())
    except (InvalidOperation, AttributeError):
        raise argparse.ArgumentTypeError(f"{name} must be a number, got {value!r}") from None
    if not number.is_finite():
        raise argparse.ArgumentTypeError(f"{name} must be a finite number, got {value!r}")
    return number


def validate(principal: Decimal, rate: Decimal, time: Decimal) -> None:
    """Stop with a clear message if a value is outside a sensible range."""
    problems = []
    if principal <= 0:
        problems.append("principal must be greater than 0")
    if rate < 0:
        problems.append("rate cannot be negative")
    if time <= 0:
        problems.append("time must be greater than 0")
    if problems:
        raise SystemExit("Error: " + "; ".join(problems))


def prompt(label: str, default: str | None = None) -> str:
    """Ask for a value interactively, offering a default in brackets."""
    suffix = f" [{default}]" if default else ""
    try:
        answer = input(f"{label}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        raise SystemExit("Cancelled.")
    return answer or default or ""


def format_money(value: Decimal) -> str:
    return f"{value:,.2f}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="simple_interest.py",
        description="Calculate simple interest and the total amount payable.",
        epilog="Run without arguments to be prompted for each value.",
    )
    parser.add_argument("-p", "--principal", type=lambda v: parse_decimal(v, "principal"),
                        help="principal amount, e.g. 10000")
    parser.add_argument("-r", "--rate", type=lambda v: parse_decimal(v, "rate"),
                        help="annual interest rate in percent, e.g. 5 or 7.5")
    parser.add_argument("-t", "--time", type=lambda v: parse_decimal(v, "time"),
                        help="time in years, e.g. 3 or 1.5")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    principal = args.principal if args.principal is not None else parse_decimal(prompt("Principal", "10000"), "principal")
    rate = args.rate if args.rate is not None else parse_decimal(prompt("Annual rate (%)", "5"), "rate")
    time = args.time if args.time is not None else parse_decimal(prompt("Time (years)", "3"), "time")

    validate(principal, rate, time)
    interest, total = simple_interest(principal, rate, time)

    print()
    print(f"Principal : {format_money(principal)}")
    print(f"Rate      : {rate.normalize():f}% per year")
    print(f"Time      : {time.normalize():f} years")
    print(f"Interest  : {format_money(interest)}")
    print(f"Total     : {format_money(total)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
