#!/usr/bin/env bash
#
# simple-interest.sh - work out simple interest and the total amount payable.
#
# Simple interest is charged only on the original principal:
#
#     I = P * (R / 100) * T
#     A = P + I
#
# Usage:
#   ./simple-interest.sh                 # asks for the three values
#   ./simple-interest.sh 10000 5 3       # principal, annual rate, years
#
set -euo pipefail

readonly SCRIPT_NAME=${0##*/}

usage() {
  cat <<EOF
Usage: $SCRIPT_NAME [principal rate time]

  principal  amount borrowed, lent or invested   (for example 10000)
  rate       annual interest rate in percent     (for example 5 or 7.5)
  time       time period in years                (for example 3 or 1.5)

Run without arguments to be prompted for each value, then press Enter.
EOF
}

# A plain decimal number: digits, optionally followed by a dot and more digits.
is_number() {
  [[ ${1:-} =~ ^[0-9]+([.][0-9]+)?$ ]]
}

# awk does the arithmetic because bash only knows whole numbers.
report() {
  awk -v p="$1" -v r="$2" -v t="$3" '
    function money(v,   s, neg, part, whole, frac, out, i) {
      s = sprintf("%.2f", v)
      neg = (substr(s, 1, 1) == "-")
      if (neg) s = substr(s, 2)
      split(s, part, ".")
      whole = part[1]
      frac  = part[2]
      out = ""
      for (i = 1; i <= length(whole); i++) {
        out = out substr(whole, i, 1)
        if (i < length(whole) && (length(whole) - i) % 3 == 0) out = out ","
      }
      return (neg ? "-" : "") out "." frac
    }
    BEGIN {
      interest = p * (r / 100) * t
      total    = p + interest
      printf "Principal : %s\n", money(p)
      printf "Rate      : %s%% per year\n", r + 0
      printf "Time      : %s year%s\n", t + 0, (t + 0 == 1 ? "" : "s")
      printf "Interest  : %s\n", money(interest)
      printf "Total     : %s\n", money(total)
    }'
}

main() {
  local principal rate time value name

  case $# in
    0)
      printf 'Simple interest calculator\n\n'
      read -r -p 'Principal amount : ' principal || exit 1
      read -r -p 'Annual rate (%)  : ' rate      || exit 1
      read -r -p 'Time (years)     : ' time      || exit 1
      ;;
    1)
      case $1 in
        -h|--help) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
      esac
      ;;
    3)
      principal=$1
      rate=$2
      time=$3
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac

  # Windows terminals, and pipes from Windows programs, can leave a stray CR.
  principal=${principal//$'\r'/}
  rate=${rate//$'\r'/}
  time=${time//$'\r'/}

  for value in "principal:$principal" "rate:$rate" "time:$time"; do
    name=${value%%:*}
    value=${value#*:}
    if ! is_number "$value"; then
      printf 'Error: %s must be a number, got "%s"\n' "$name" "$value" >&2
      exit 1
    fi
  done

  if awk -v p="$principal" -v r="$rate" -v t="$time" 'BEGIN { exit !(p > 0 && r >= 0 && t > 0) }'; then
    :
  else
    printf 'Error: principal and time must be greater than 0, and rate cannot be negative\n' >&2
    exit 1
  fi

  echo
  report "$principal" "$rate" "$time"
}

main "$@"
