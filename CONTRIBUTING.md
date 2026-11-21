# Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

This project is small, so there is no heavy process — open an issue, or send a pull
request if you already know what you want to change. Please be kind; this project
follows the [Contributor Covenant](CODE_OF_CONDUCT.md).

## Reporting a bug

Open an issue and include:

- what you did (the numbers you typed, and whether you used the CLI or `index.html`),
- what you expected to happen,
- what actually happened,
- your Python version (`python --version`) or browser and version.

A copy of the output or a screenshot helps a lot. If the wrong value appears, say
what value you expected and how you worked it out.

## Suggesting an enhancement

Ideas are welcome, including small ones: a clearer error message, another rounding
convention, a currency, a command-line flag. Describe the problem the change solves
rather than only the change itself, and say whether you would like to implement it.

## Improving the documentation

Typos, unclear sentences, missing examples and better screenshots are all useful
contributions. Editing `README.md`, `CONTRIBUTING.md` or `CODE_OF_CONDUCT.md` needs
no discussion beforehand — just open a pull request.

## Sending a pull request

1. Fork the repository and create a branch with a descriptive name:
   `git checkout -b fix-rounding-error`.
2. Keep the change focused; one topic per pull request is easier to review.
3. Make sure the tests still pass:

   ```bash
   python -m unittest -v
   ```

4. If you change behaviour, add or update a test in `test_simple_interest.py`.
5. If you change the web version, open `index.html` and check the normal cases by
   hand — the default example should still give 1,500.00 interest on 10,000 at 5%
   for 3 years.
6. Describe in the pull request what changed and why.

## Code style

- Python: keep to the standard library, use type hints on new functions, and follow
  the existing layout (`simple_interest.py` keeps the formula in one function so it
  can be tested independently of the command line).
- Money must keep using `Decimal`, rounded half-up to two places, so results are not
  distorted by binary floating point.
- HTML/JavaScript: no external libraries or CDN links; `index.html` must keep working
  when opened straight from disk, with no server.

## Questions

If anything is unclear, open an issue with the `question` label rather than guessing.
