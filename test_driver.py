# Course: CS340 Fall 2026
# Project Step 3 Draft: Python Test/Driver
# Team Members: Kaia Bahar, Max Riley, Ashley Davis
# Group Number: 77
# Citation for the following code:
# Date: 11/3/2026
# Adapted from the CS340 3-tier and Python CRUD testing examples.
# See README Acknowledgements for full course material citations.


import os
import mysql.connector
from catabase_dao import CatabaseDAO



def show_requests(dao, heading):
    print(f"{heading} [READ via get_all_adoption_requests()]")

    for request in dao.get_all_adoption_requests():
        print(request)


def main():
    # Replace following values with your MySQL credentials/db name
    if "DB_USER" not in os.environ or "DB_PASSWORD" not in os.environ:
        raise RuntimeError("Set DB_USER and DB_PASSWORD in your terminal first.")

    db = mysql.connector.connect(
        host="localhost",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database="Catabase"
    )

    dao = CatabaseDAO(db)

    print("Catabase test run")

    # 1) Check we can read all six tables
    print("\nREAD Cats - get_all_cats()")
    cats = dao.get_all_cats()
    for cat in cats:
        print(cat)


    print("\nREAD Adopters - get_all_adopters()")
    adopters = dao.get_all_adopters()
    for adopter in adopters:
        print(adopter)


    print("\nREAD StaffMembers - get_all_staff_members()")
    staff_members = dao.get_all_staff_members()
    for staff_member in staff_members:
        print(staff_member)


    print("\nREAD FosterHomes - get_all_foster_homes()")
    for home in dao.get_all_foster_homes():
        print(home)


    show_requests(dao, "\nAdoptionRequests before testing:")


    print("\nREAD FosterAssignments - get_all_foster_assignments()")
    for assignment in dao.get_all_foster_assignments():
        print(assignment)



    # Use the sample rows; this needs at least 2 cats, 2 adopters, and 1 staff member from DDL.sql
    cat_id = cats[0]["catID"]
    new_cat_id = cats[1]["catID"]
    adopter_id = adopters[0]["adopterID"]
    new_adopter_id = adopters[1]["adopterID"]
    staff_id = staff_members[0]["staffID"]

    # Test adoption request: must reference an existing cat.
    # get_all_cats() orders by catID, so first cat has lowest ID and last cat has highest ID.
    invalid_cat_id = cats[-1]["catID"] + 1
    requests_before = dao.get_all_adoption_requests()

    print(f"\nEXPECTED FOREIGN-KEY REJECTION - add_adoption_request() with nonexistent catID {invalid_cat_id}")

    try:
        unexpected_request_id = dao.add_adoption_request(
            adopter_id, invalid_cat_id, None, "2026-11-03", "Pending", None
        )
    except mysql.connector.IntegrityError as error:
        if error.errno != 1452:
            raise
        print("MySQL rejected the request because the cat does not exist.")
    else:
        dao.delete_adoption_request(unexpected_request_id)
        raise RuntimeError("The invalid request was accepted. Check the foreign key.")

    requests_after = dao.get_all_adoption_requests()

    if requests_after != requests_before:
        raise RuntimeError("The adoption requests changed after the rejected INSERT.")

    print("Verified that the existing requests are intact. Continuing with the valid tests.")

    # Add four requests to try reviewer and notes with/without NULL.
    # Save request IDs for the update and delete tests.
    print(f"\nTest cat: {cats[0]['catName']}")
    print("\nCREATE add_adoption_request(): NULL reviewer and NULL notes")
    request_id_1 = dao.add_adoption_request(
        adopter_id, cat_id, None, "2026-11-03", "Pending", None
    )
    print(f"Created request ID: {request_id_1}")

    print("\nCREATE add_adoption_request(): NULL reviewer and supplied notes")
    request_id_2 = dao.add_adoption_request(
        adopter_id, cat_id, None, "2026-11-03", "Pending",
        "Applicant asked about indoor-only care."
    )
    print(f"Created request ID: {request_id_2}")

    print("\nCREATE add_adoption_request(): supplied reviewer and NULL notes")
    request_id_3 = dao.add_adoption_request(
        adopter_id, cat_id, staff_id, "2026-11-03", "Pending", None
    )

    print(f"Created request ID: {request_id_3}")

    print("\nCREATE add_adoption_request(): supplied reviewer and supplied notes")
    request_id_4 = dao.add_adoption_request(
        adopter_id, cat_id, staff_id, "2026-11-03", "Pending",
        "Staff will arrange a meet-and-greet."
    )
    print(f"Created request ID: {request_id_4}")

    show_requests(dao, "\nAdoptionRequests after CREATE:")



    # Change test requests to the second cat and adopter
    # Attempt to add and clear reviewer/notes
    print(f"\nChanging test requests to cat: {cats[1]['catName']}")
    print("\nUPDATE update_adoption_request(): supplied reviewer and supplied notes")
    rowcount = dao.update_adoption_request(
        request_id_1, new_adopter_id, new_cat_id, staff_id,
        "2026-11-04", "Denied", "Housing requirements not met."
    )
    print(f"Request {request_id_1}: {rowcount} row(s) affected.")

    print("\nUPDATE update_adoption_request(): supplied reviewer and NULL notes")
    rowcount = dao.update_adoption_request(
        request_id_2, new_adopter_id, new_cat_id, staff_id,
        "2026-11-04", "Denied", None
    )
    print(f"Request {request_id_2}: {rowcount} row(s) affected.")

    print("\nUPDATE update_adoption_request(): NULL reviewer and supplied notes")
    rowcount = dao.update_adoption_request(
        request_id_3, new_adopter_id, new_cat_id, None,
        "2026-11-04", "Pending", "Waiting for a new reviewer."
    )

    print(f"Request {request_id_3}: {rowcount} row(s) affected.")

    print("\nUPDATE update_adoption_request(): NULL reviewer and NULL notes")
    rowcount = dao.update_adoption_request(
        request_id_4, new_adopter_id, new_cat_id, None,
        "2026-11-04", "Pending", None
    )
    print(f"Request {request_id_4}: {rowcount} row(s) affected.")

    show_requests(dao, "\nAdoptionRequests after UPDATE:")

    # Remove our test requests, and leave the original sample requests
    print("\nDELETE delete_adoption_request(): remove the four test requests")
    for request_id in [request_id_1, request_id_2, request_id_3, request_id_4]:
        rowcount = dao.delete_adoption_request(request_id)
        print(f"Request {request_id}: {rowcount} row(s) affected.")

    show_requests(dao, "\nAdoptionRequests after DELETE:")

    # DAO will handle its cursors and commits; close connection here
    db.close()

    print("\nFinished testing Catabase. Connection now closed.")


if __name__ == "__main__":
    main()






