☕ Café Andrómeda — Order Management System

A command-line order management system for a coffee shop, built in Python as the final project for Programming Fundamentals (Software Engineering, Universidad Tecmilenio — May 2026).

The program handles the full lifecycle of an order: product selection, quantity capture, subtotal and tax calculation, session reporting, and persistence to disk.

Features
#	Option	What it does
1	Register order	Select from the product catalog or enter a custom product with its own price
2	View orders	Formatted table of all orders in memory, with timestamps
3	Show total	Subtotal, 16% VAT, grand total, order count, and highest-value order
4	Save to file	Writes all orders to pedidos.json with session metadata
5	Load from file	Reads orders back into memory, skipping duplicate IDs
6	Exit	Prompts to save any unsaved orders before closing
How to run

Requires Python 3.6 or higher. No external dependencies — standard library only.

bash
python cafe_andromeda.py

The program creates pedidos.json in the working directory the first time you save.

Technical highlights

Data structures

Product catalog stored as a tuple of tuples — immutable by design
Orders modeled as dictionaries inside a list, each with an auto-incrementing ID and timestamp
Set comprehension used to detect duplicate IDs when loading from file

Input validation

Dedicated capture functions (capturar_entero, capturar_precio) that raise ValueError with descriptive messages instead of failing silently
Menu options validated against a whitelist tuple before dispatch

Error handling

Specific except blocks for ValueError, FileNotFoundError, PermissionError, json.JSONDecodeError and KeyboardInterrupt
Generic fallback that reports the exception type, plus a finally block that always runs
The program never crashes on bad input — it reports the problem and returns to the menu

Persistence

JSON output with UTF-8 encoding and indentation, including session metadata (save date, order count, accumulated total)
File existence and empty-file checks before attempting to read

Code quality

Type hints on function signatures and constants
Docstrings documenting arguments, return values, and raised exceptions
Presentation logic separated into reusable helper functions
Concepts covered

Input/output · Conditionals · Loops · Functions · Lists · Dictionaries · Tuples · Exception handling · File handling · String formatting · Lambda functions

Author

Roberto Yair Castellanos Eguia Software Engineering student, Universidad Tecmilenio
