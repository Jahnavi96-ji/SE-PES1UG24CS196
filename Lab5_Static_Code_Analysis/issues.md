

\# Lab 5: Static Code Analysis — Issue Report



\## Objective



To improve code quality, security, and formatting in `theater\_system.py` using Pylint, Bandit, and Flake8.



\## Issues Identified and Fixes Applied



| Issue | Type | Original Line(s) | Description | Fix Approach |

|---|---|---:|---|---|

| Mutable default argument | Code quality / Bug | 9 | `system\_logs=\[]` shares the same list between calls. | Changed the default to `None` and initialized a new list inside the function. |

| Bare exception | Code quality | 21 | A bare `except` catches errors without identifying their type. | Caught the specific `ValueError` exception. |

| Weak MD5 hash | Security | 25 | MD5 is unsuitable for security-sensitive token generation. | Replaced the MD5-based ticket code with `secrets.token\_hex(4)`. |

| File handling without context managers | Code quality | 28, 33 | Files were opened without explicitly closing them. | Used `with open(...)` context managers. |

| Missing file encoding | Code quality | 28, 33 | Text file operations did not specify an encoding. | Added `encoding="utf-8"`. |

| Permissive file permissions | Security | 55 | `os.chmod("seats.json", 0o777)` grants unnecessarily broad permissions. | Removed the permission change. |

| Missing docstrings | Code quality | Multiple | The module and functions lacked documentation. | Added module and function docstrings. |

| Incorrect function naming | Style | 37 | `printSeatingSummary()` did not follow snake\_case naming conventions. | Renamed it to `print\_seating\_summary()`. |

| Long lines and formatting violations | Style | Multiple | Several lines exceeded the recommended length and functions lacked required spacing. | Reformatted the code and corrected blank-line spacing. |

| Unused import | Code quality / Style | 3 | The `hashlib` import was no longer required. | Removed the unused import. |

| Unused function parameters | Code quality | Ticket-code function | The show and seat parameters were not used in token generation. | Prefixed the intentionally unused parameters with underscores. |

| Invalid seat input | Logic / Validation | Multiple | Invalid seat numbers could be accepted, and nonnumeric user input could cause an error. | Added seat-range validation and handled invalid numeric input. |



\## Final Verification



\- Pylint score: 10.00/10

\- Bandit: No issues identified

\- Flake8: No violations reported



\## Conclusion



Static code analysis helped identify code-quality problems, insecure coding practices, and formatting violations. After making the corrections, the program achieved a Pylint score of 10.00/10, Bandit reported no issues, and Flake8 reported no violations.



