

\# Lab 5: Static Code Analysis — Reflection



\## 1. What is static code analysis?



Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, code-quality issues, and formatting problems.



\## 2. What did Pylint, Bandit, and Flake8 identify?



Pylint identified missing docstrings, a mutable default argument, a bare exception, unused imports, and code-quality issues.



Bandit identified a weak MD5 hash, overly permissive file permissions, and a try-except-pass pattern.



Flake8 identified long lines, missing blank lines, and formatting violations.



\## 3. How did you fix the identified issues?



I replaced the mutable default argument with None, used specific exception handling, added file context managers and UTF-8 encoding, replaced MD5-based ticket-code generation with secure random tokens, removed unnecessary file-permission changes, and corrected naming and formatting issues.



\## 4. What did you learn from this lab?



I learned that static analysis tools complement one another. Pylint checks code quality, Bandit identifies potential security problems, and Flake8 checks coding style. Running these tools before and after making changes helps verify improvements.



\## Final Results



\- Pylint: 10.00/10

\- Bandit: No issues identified

\- Flake8: No violations reported



