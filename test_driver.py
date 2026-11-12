# Course: CS340 Fall 2026
# Project Step 3 FINAL: Python Test/Driver
# Team Members: Kaia Bahar, Max Riley, Ashley Davis
# Group Number: 77
# Date: 11/11/2026
# Citation for the following code: CS340 course materials used as guidelines for the code below (the full list of sources is in README.md).
# Curry, M. (November 2026). CS340 Fall 2026 Canvas: Activity 2 - Python App to Demo 3-Tier [Course material]. https://canvas.oregonstate.edu/courses/2061186/assignments/10623022?module_item_id=27088329
# Curry, M. (November 2026). CS340 Fall 2026 Canvas: Python CRUD Query App Assignment [Course material]. https://canvas.oregonstate.edu/courses/2061186/assignments/10623045?module_item_id=27088392
# Citation for use of AI Tools:
# Date: 11/11/2026
# Prompts used to revise test_driver.py: Help me develop environmental variables for log in. 
# Anthropic. (November 2026). Claude [Large language model]. https://claude.ai.

import getpass
import os

import mysql.connector
from catabase_dao import CatabaseDAO


# Creates environmental variables for log in
# Protects sensitive data and prevents credentials from being accidentally committed

def get_connection():
    host = os.environ.get("CATABASE_DB_HOST", "localhost")
    database = os.environ.get("CATABASE_DB_NAME", "Catabase")
    user = os.environ.get("CATABASE_DB_USER") or input("MySQL username: ")
    password = os.environ.get("CATABASE_DB_PASSWORD") or getpass.getpass("MySQL password: ")
    return mysql.connector.connect(host=host, user=user, password=password, database=database)


#  Creates banners for each demo step so CLI_OUT.txt can be checked without reading the code.
def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# Every table prints its name and row count
def show_rows(heading, rows):
    print(f"\n{heading} ({len(rows)} rows):")
    for row in rows:
        print(row)


def show_requests(dao, heading):
    show_rows(heading, dao.get_all_adoption_requests())


def main():
    db = get_connection()
    dao = CatabaseDAO(db)

    # try/finally (see bottom of main) guarantees db.close() runs.
    try:
        print("Catabase test run")
        print("Group 77 - CS340 Project Step 3 FINAL")
        print("Dates appear as datetime.date(...); None means SQL NULL.")

        # ------------------------------------------------------------------
        section("PART 1 - READ (SELECT) via get_all_cats, get_all_adopters, get_all_staff_members, "
                "get_all_foster_homes, get_all_adoption_requests, get_all_foster_assignments")
        # ------------------------------------------------------------------
        cats = dao.get_all_cats()
        show_rows("Cats", cats)

        adopters = dao.get_all_adopters()
        show_rows("Adopters", adopters)

        staff_members = dao.get_all_staff_members()
        show_rows("StaffMembers", staff_members)

        show_rows("FosterHomes", dao.get_all_foster_homes())

        # The two intersection-table reads use JOINs (see DML.sql), so each row shows adopter, cat,
        # reviewer, and foster home names next to the IDs. The driver code does not change; only the DAO queries do.
        show_requests(dao, "AdoptionRequests - intersection table Adopters <-> Cats, with names from JOINs - before testing")

        show_rows("FosterAssignments - intersection table Cats <-> FosterHomes, with names from JOINs", dao.get_all_foster_assignments())

        # Use the sample rows; this needs at least 2 cats, 2 adopters, and 1 staff member from DDL.sql
        cat_id = cats[0]["catID"]
        new_cat_id = cats[1]["catID"]
        adopter_id = adopters[0]["adopterID"]
        new_adopter_id = adopters[1]["adopterID"]
        staff_id = staff_members[0]["staffID"]

        # ------------------------------------------------------------------
        section("PART 2 - CREATE (INSERT) via add_adoption_request: 4 NULL / non-NULL combinations")
        # ------------------------------------------------------------------

        print(f"Test cat: {cats[0]['catName']} (catID {cat_id}); test adopter: {adopters[0]['fName']} (adopterID {adopter_id})")

        # Save the new request IDs; the update and delete tests use them.
        print("\nCREATE 1: NULL reviewer, NULL notes")
        request_id_1 = dao.add_adoption_request(adopter_id, cat_id, None, "2026-11-03", "Pending", None)
        print(f"Created request ID: {request_id_1}")

        print("\nCREATE 2: NULL reviewer, supplied notes")
        request_id_2 = dao.add_adoption_request(
            adopter_id, cat_id, None, "2026-11-03", "Pending",
            "Applicant asked about allowing cat outdoors."
        )
        print(f"Created request ID: {request_id_2}")

        print("\nCREATE 3: supplied reviewer, NULL notes")
        request_id_3 = dao.add_adoption_request(adopter_id, cat_id, staff_id, "2026-11-03", "Pending", None)
        print(f"Created request ID: {request_id_3}")

        print("\nCREATE 4: supplied reviewer, supplied notes")
        request_id_4 = dao.add_adoption_request(
            adopter_id, cat_id, staff_id, "2026-11-03", "Pending",
            "Staff to arrange a meet and greet with small children in the home."
        )
        print(f"Created request ID: {request_id_4}")

        show_requests(dao, "AdoptionRequests after CREATE (original 5 plus 4 new)")

        # ------------------------------------------------------------------
        section("PART 3 - UPDATE via update_adoption_request and update_request_status: "
                "move the 4 test requests to a different cat and adopter")
        # ------------------------------------------------------------------
        print(f"New cat: {cats[1]['catName']} (catID {new_cat_id}); new adopter: {adopters[1]['fName']} (adopterID {new_adopter_id})")

        print("\nUPDATE 1: supplied reviewer, supplied notes")
        rowcount = dao.update_adoption_request(
            request_id_1, new_adopter_id, new_cat_id, staff_id,
            "2026-11-04", "Denied", "Apartment website states no pets"
        )
        print(f"Request {request_id_1}: {rowcount} row(s) affected.")

        print("\nUPDATE 2: supplied reviewer, NULL notes (notes cleared)")
        rowcount = dao.update_adoption_request(
            request_id_2, new_adopter_id, new_cat_id, staff_id,
            "2026-11-04", "Denied", None
        )
        print(f"Request {request_id_2}: {rowcount} row(s) affected.")

        print("\nUPDATE 3: NULL reviewer (reviewer cleared), supplied notes")
        rowcount = dao.update_adoption_request(
            request_id_3, new_adopter_id, new_cat_id, None,
            "2026-11-04", "Pending", "Pending second review."
        )
        print(f"Request {request_id_3}: {rowcount} row(s) affected.")

        print("\nUPDATE 4: NULL reviewer, NULL notes")
        rowcount = dao.update_adoption_request(
            request_id_4, new_adopter_id, new_cat_id, None,
            "2026-11-04", "Pending", None
        )
        print(f"Request {request_id_4}: {rowcount} row(s) affected.")

        show_requests(dao, "AdoptionRequests after UPDATE")

        print("\nUPDATE (status only) using the update_request_status helper:")
        rowcount = dao.update_request_status(request_id_4, "Approved")
        print(f"Request {request_id_4}: status changed to 'Approved', {rowcount} row(s) affected.")
        show_requests(dao, "AdoptionRequests after status-only UPDATE")

        # ------------------------------------------------------------------
        section("PART 4 - FAILED OPERATIONS: the DAO rolls back and the driver keeps running")
        # ------------------------------------------------------------------

        print("Attempt to CREATE a request for catID 9999, which does not exist:")
        try:
            dao.add_adoption_request(adopter_id, 9999, None, "2026-11-05", "Pending", "Should fail.")
            print("Unexpected: the INSERT succeeded.")
        except mysql.connector.Error as error:
            print(f"Rejected as expected: {error}")

        print("\nAttempt to UPDATE request ID 9999, which does not exist:")
        rowcount = dao.update_adoption_request(9999, adopter_id, cat_id, None, "2026-11-05", "Pending", None)
        print(f"Request 9999: {rowcount} row(s) affected (no such request).")

        show_requests(dao, "AdoptionRequests after the failed operations (unchanged)")

        # ------------------------------------------------------------------
        section("PART 5 - DELETE via delete_adoption_request: remove only the 4 test requests")
        # ------------------------------------------------------------------
        for request_id in [request_id_1, request_id_2, request_id_3, request_id_4]:
            rowcount = dao.delete_adoption_request(request_id)
            print(f"Request {request_id}: {rowcount} row(s) affected.")

        show_requests(dao, "AdoptionRequests after DELETE (back to the original 5)")

        print("\nCats, Adopters, and StaffMembers after DELETE (deleting requests keeps their parent rows):")
        print(f"Cats: {len(dao.get_all_cats())} rows, Adopters: {len(dao.get_all_adopters())} rows, "
              f"StaffMembers: {len(dao.get_all_staff_members())} rows")

    finally:
        # DAO handles its own cursors and commits; close the connection here
        db.close()

    print("\nFinished testing Catabase. Connection now closed.")


if __name__ == "__main__":
    main()
