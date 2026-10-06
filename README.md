# Password Strength Checker

https://password-strength-checker-mhwmtmvg3nhlfouqhgjefk.streamlit.app/ <-- Link

A Python tool that checks password strength and gives users specific
feedback to improve weak passwords — built to understand how real attackers
guess/crack passwords and how to defend against it.

🔗 **Live demo:** [add your Streamlit Cloud link here once deployed]

## What it does

- Checks a password against 4 criteria: length (12+ chars), uppercase,
  lowercase, numbers, and special characters
- Checks the password against a list of 100k commonly used/breached passwords
- Gives a Weak / Moderate / Strong rating with specific, actionable feedback
- Estimates crack time based on character set size and password length
- Live, per-keystroke feedback (no need to press Enter) with a password
  show/hide toggle

## Why these design choices

- **12-character minimum, not 8.** NIST SP 800-63B and most modern guidance
  treat 8 characters as weak by current standards; length matters more than
  arbitrary complexity rules.
- **Common-password match overrides the score entirely.** A 12-character
  password that's already in a breach list is weak regardless of how many
  other rules it satisfies — length and complexity don't help if the exact
  password is already known to attackers.
- **The common-password list is loaded into a `set`, not a list.** Set lookups
  are O(1) regardless of list size, versus scanning a 100k-line list linearly.
- **Checks the breach list twice** (once for scoring, once for feedback) for
  simplicity, since each run only checks one password — the cost is
  negligible at this scale.

## Tech stack

- Python
- Streamlit
- A custom-patched fork of `streamlit-keyup` ([original](https://github.com/blackary/streamlit-keyup)),
  modified to add password masking and a custom eye-icon show/hide toggle,
  since the original component supported live typing but not masking

## Running locally

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Known limitations / future improvements

- Doesn't catch leetspeak substitutions of common passwords (e.g.
  `P@ssw0rd123` passes the rule checks but is still a predictable pattern)
- No real breach-database check (e.g. Have I Been Pwned's API) yet — current
  check is against a static downloaded list
- Crack-time estimate is a simplified brute-force calculation, not based on
  real-world hashing/cracking tool speeds