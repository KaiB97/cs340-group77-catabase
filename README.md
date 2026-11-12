# Catabase

### Cat Adoption & Shelter Management System

CS340 Fall 2026 · Project Step 3 FINAL · Group 77  
Kaia Bahar · Max Riley · Ashley Davis

![Kitten eating from a bowl](assets/kitten1.png)



## Project Description

**Catabase** is a database system for managing a cat shelter's adoption requests and foster placements. It uses six tables: Cats, Adopters, StaffMembers, FosterHomes, AdoptionRequests, and FosterAssignments. The two intersection tables represent M:N (many-to-many) relationships between adopters and cats (AdoptionRequests), and between cats and foster homes (FosterAssignments).

This project follows a three-tier structure:
1) a MySQL database (`DDL.sql` creates the tables and sample data; `DML.sql` lists the queries)
2) a Python application-tier class (`CatabaseDAO` in `catabase_dao.py`)
3) a Python client/test driver (`test_driver.py`)

The class provides READ operations for all six tables, and CREATE, UPDATE, and DELETE operations for the intersection table AdoptionRequests. All SQL lives inside the class methods and uses parameterized queries (`%s`) for supplied values. The test driver only calls those methods; it never issues SQL itself. It demonstrates each operation and prints the results.


## Requirements

- **Python 3** 
- **mysql-connector-python** (Python library; installed with pip in the steps below)
- **A local MySQL server** that is running, plus your MySQL username and password
- `DDL.sql`, `catabase_dao.py` and `test_driver.py` must stay together in the same project folder



## Setup

Complete these four steps in order. Steps 1 and 2 differ by operating system; steps 3 and 4 are the same everywhere.

### Step 1. Create and activate a Python virtual environment

**macOS / Linux** (Terminal, opened in this project folder):
```sh
python3 -m venv venv
source venv/bin/activate
```

**Windows** (PowerShell, opened in this project folder):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

When the environment is active, your prompt starts with `(venv)`.

### Step 2. Install the required library

With the virtual environment active, run:

**macOS / Linux**
```sh
python3 -m pip install mysql-connector-python
```

**Windows**
```powershell
python -m pip install mysql-connector-python
```

### Step 3. Create the Catabase database and import the DDL

Start your local MySQL server. While in your project folder, log in to MySQL, replacing YOUR_USERNAME with your MySQL username (likely `root`):

```sh
mysql -u YOUR_USERNAME -p
```

After you press enter, you will be prompted for your MySQL password.Type your MySQL password when prompted. If you get `command not found: mysql` and MySQL is installed at `/usr/local/mysql`, use the command `/usr/local/mysql/bin/mysql -u YOUR_USERNAME -p` instead.

When you see the `mysql>` prompt, run:
```sql
CREATE DATABASE IF NOT EXISTS Catabase;
USE Catabase;
SOURCE DDL.sql;
SHOW TABLES;
EXIT;
```

This creates and selects the Catabase database, creates its six tables, and loads the sample data (4 cats, 3 staff members, 3 adopters, 3 foster homes, 5 adoption requests, 5 foster assignments). `SHOW TABLES;` should list all six tables. Importing the DDL will replace any existing project tables, thus use a test database. `SOURCE DDL.sql;` assumes you started the MySQL client from the project folder.

### Step 4. Provide your MySQL login (no passwords are stored in the code)

`test_driver.py` reads your MySQL login from environment variables, so you do not have to edit any file. In the same terminal where you will run the program, set:

**macOS / Linux**
```sh
export CATABASE_DB_USER="YOUR_MYSQL_USERNAME"
export CATABASE_DB_PASSWORD="YOUR_MYSQL_PASSWORD"
```

**Windows PowerShell**
```powershell
$env:CATABASE_DB_USER = "YOUR_MYSQL_USERNAME"
$env:CATABASE_DB_PASSWORD = "YOUR_MYSQL_PASSWORD"
```

Optional variables: `CATABASE_DB_HOST` (default `localhost`) and `CATABASE_DB_NAME` (default `Catabase`). If the username or password variables are not set, the program asks for them when it starts.



## Run the Application

With the virtual environment active, the login variables set, and the terminal open in the project folder, run:

**macOS / Linux**
```sh
python3 test_driver.py
```

**Windows PowerShell**
```powershell
python test_driver.py
```

The driver runs automatically from start to finish; nothing needs to be typed while it runs. It expects the unchanged sample data from `DDL.sql` (at least two cats, two adopters, and one staff member). Re-run Step 3 to reset the database before running the driver again.



## Expected Output & CLI Output

The driver prints five labeled parts, each introduced by a banner line (`PART 1 - ...`):

1. **READ:** every row of all six tables (Cats, Adopters, StaffMembers, FosterHomes, AdoptionRequests, FosterAssignments), each with a row count. The two intersection tables are read with JOINs, so each AdoptionRequests row also shows the adopter, cat and reviewer names (`reviewerName` is `None` when no reviewer is assigned) and each FosterAssignments row shows the foster home and cat names, next to the IDs.
2. **CREATE:** four new adoption requests, covering every combination of supplied/NULL reviewer and supplied/NULL notes, followed by the AdoptionRequests table with 9 rows.
3. **UPDATE:** four updates that move the new requests to a different cat and adopter and add or clear the reviewer and notes (each prints `1 row(s) affected`), then one status-only update using the `update_request_status` helper.
4. **FAILED OPERATIONS:** an INSERT for a cat ID that does not exist is rejected by MySQL's foreign-key constraint and rolled back, and an UPDATE of a request ID that does not exist affects 0 rows. The driver keeps running, and the table is unchanged.
5. **DELETE:** the four test requests are deleted (each prints `1 row(s) affected`) and the table returns to the original 5 requests. The driver also confirms the Cats, Adopters and StaffMembers tables kept all of their rows.

The output ends with `Finished testing Catabase. Connection now closed.`

Notes on reading the output:
- Dates appear as `datetime.date(...)`.
- `None` represents SQL NULL.
- The new request IDs (6 to 9 on a freshly imported database) can differ between runs. The exact error text in part 4 depends on your MySQL version.

To save the CLI output, set the login variables (Step 4) first, because prompts would otherwise be hidden in the file. Then run:

**macOS / Linux**
```sh
python3 test_driver.py > CLI_OUT.txt 2>&1
```

**Windows PowerShell**
```powershell
python test_driver.py > CLI_OUT.txt 2>&1
```


## Originality

The database design, SQL, and most of the Python code are our team's own work, adapted from the OSU CS340 course materials cited below. Each source file also carries its own citation comment block.

## AI Disclosure

Claude. (11-11-26). Claude (Sonnet 5.5) [Large language model]. https://claude.ai. Used to help develop environmental variables to remove hard-coded credentials.


## Citations
Our team designed and adapted our project using OSU CS340 lectures and activities.
The highlighted course materials used were the following:

- Curry, M. (November 2026). *Activity 2 — Python App to Demo 3-Tier*. CS340, Oregon State University. [Course Material]. https://canvas.oregonstate.edu/courses/2061186/assignments/10623022?module_item_id=27088329 
- Curry, M. (November 2026). *Python CRUD Query App Assignment — Local Testing Example*. CS340, Oregon State University. [Course Material]. https://canvas.oregonstate.edu/courses/2061186/assignments/10623045?module_item_id=27088392 
- Curry, M. (November 2026). *Exploration — Designing a Python Class for Database CRUD Operations*. CS340, Oregon State University.[Course Material]. https://canvas.oregonstate.edu/courses/2061186/pages/exploration-designing-a-python-class-for-database-crud-operations?module_item_id=27088390
- Curry, M. (November 2026). *Exploration — Connecting Python to MySQL and Build a CRUD CLI*. CS340, Oregon State University. [Course Material]. https://canvas.oregonstate.edu/courses/2061186/pages/exploration-connecting-python-to-mysql-and-build-a-crud-cli?module_item_id=27088391 
- Curry, M. (November 2026). *Exploration — Intro to SQL*. CS340, Oregon State University. [Course Material]. https://canvas.oregonstate.edu/courses/2061186/pages/exploration-intro-to-sql-2?module_item_id=27088352
- Curry, M. (November 2026). *Activity 4 — Creating a Customer Object Table*. CS340, Oregon State University. [Course Material]. https://canvas.oregonstate.edu/courses/2061186/pages/activity-4-creating-a-customer-object-table?module_item_id=27088357
- Curry, M. (November 2026). *Activity 7 — Creating Database Intersection Tables*. CS340, Oregon State University. [Course Material]. https://canvas.oregonstate.edu/courses/2061186/pages/activity-7-creating-database-intersection-tables?module_item_id=27088368
- Curry, M. (November 2026). *Activity 8 — SQL Queries of Multiple Tables (JOINS)*. CS340, Oregon State University. [Course Material]. https://canvas.oregonstate.edu/courses/2061186/pages/activity-8-sql-queries-of-multiple-tables-joins?module_item_id=27088370
- Curry, M. (November 2026). *What is CRUD?* and *Sample Data Manipulation Queries*. CS340, Oregon State University. [Course Material]. https://canvas.oregonstate.edu/courses/2061186/pages/what-is-crud-2?module_item_id=27088389 

Images:
- Reding, M. (November 2026)  Black and White Cat Eating on Bowl, Pexels. [Online]. https://www.pexels.com/photo/black-and-white-cat-eating-on-bowl-12467776/
