# Course: CS340 Fall 2026
# Project Step 3 Draft: Python Test/Driver
# Team Members: Kaia Bahar, Max Riley, Ashley Davis
# Group Number: 77
# Citation for the following code:
# Date: 11/3/2026
# Citation for the following code: CS340 course materials used; the following lectures and activities were used as guidelines for the code below.
# Curry, M. (November 2026). CS340 Fall 2026 Canvas: Activity 2 - Python App to Demo 3-Tier [Course material]. https://canvas.oregonstate.edu/courses/2061186/assignments/10623022?module_item_id=27088329
# Curry, M. (November 2026). CS340 Fall 2026 Canvas: Python CRUD Query App Assignment [Course material]. https://canvas.oregonstate.edu/courses/2061186/assignments/10623045?module_item_id=27088392
# Curry, M. (November 2026). CS340 Fall 2026 Canvas: Exploration - Connecting Python to MySQL and Build a CRUD CLI [Course material]. https://canvas.oregonstate.edu/courses/2061186/pages/exploration-connecting-python-to-mysql-and-build-a-crud-cli?module_item_id=27088391
# Curry, M. (October 2026). CS340 Fall 2026 Canvas: Exploration - Designing a Python Class for Database CRUD Operations [Course material]. https://canvas.oregonstate.edu/courses/2061186/pages/exploration-designing-a-python-class-for-database-crud-operations?module_item_id=27088390



import mysql.connector
from catabase_dao import CatabaseDAO



def show_requests(dao, heading):
    print(heading)

    for request in dao.get_all_adoption_requests():
        print(request)


def main():
    # Replace following values with your MySQL credentials/db name
    db = mysql.connector.connect(
        host="localhost",
        user="YOUR_MYSQL_USERNAME",
        password="YOUR_MYSQL_PASSWORD",
        database="Catabase"
    )

    dao = CatabaseDAO(db)

    print("Catabase test run")

    # 1) Check we can read all six tables
    print("\nCats:")
    cats = dao.get_all_cats()
    for cat in cats:
        print(cat)


    print("\nAdopters:")
    adopters = dao.get_all_adopters()
    for adopter in adopters:
        print(adopter)


    print("\nStaffMembers:")
    staff_members = dao.get_all_staff_members()
    for staff_member in staff_members:
        print(staff_member)


    print("\nFosterHomes:")
    for home in dao.get_all_foster_homes():
        print(home)


    show_requests(dao, "\nAdoptionRequests before testing:")


    print("\nFosterAssignments:")
    for assignment in dao.get_all_foster_assignments():
        print(assignment)



    # Use the sample rows; this needs at least 2 cats, 2 adopters, and 1 staff member from DDL.sql
    cat_id = cats[0]["catID"]
    new_cat_id = cats[1]["catID"]
    adopter_id = adopters[0]["adopterID"]
    new_adopter_id = adopters[1]["adopterID"]
    staff_id = staff_members[0]["staffID"]



    # Add four requests to try reviewer and notes with/without NULL.
    # Save request IDs for the update and delete tests.
    print(f"\nTest cat: {cats[0]['catName']}")
    print("\nCREATE: NULL reviewer and NULL notes")
    request_id_1 = dao.add_adoption_request(
        adopter_id, cat_id, None, "2026-11-03", "Pending", None
    )
    print(f"Created request ID: {request_id_1}")

    print("\nCREATE: NULL reviewer and supplied notes")
    request_id_2 = dao.add_adoption_request(
        adopter_id, cat_id, None, "2026-11-03", "Pending",
        "Applicant asked about indoor-only care."
    )
    print(f"Created request ID: {request_id_2}")

    print("\nCREATE: supplied reviewer and NULL notes")
    request_id_3 = dao.add_adoption_request(
        adopter_id, cat_id, staff_id, "2026-11-03", "Pending", None
    )

    print(f"Created request ID: {request_id_3}")

    print("\nCREATE: supplied reviewer and supplied notes")
    request_id_4 = dao.add_adoption_request(
        adopter_id, cat_id, staff_id, "2026-11-03", "Pending",
        "Staff will arrange a meet-and-greet."
    )
    print(f"Created request ID: {request_id_4}")

    show_requests(dao, "\nAdoptionRequests after CREATE:")



    # Change test requests to the second cat and adopter
    # Attempt to add and clear reviewer/notes
    print(f"\nChanging test requests to cat: {cats[1]['catName']}")
    print("\nUPDATE: supplied reviewer and supplied notes")
    rowcount = dao.update_adoption_request(
        request_id_1, new_adopter_id, new_cat_id, staff_id,
        "2026-11-04", "Denied", "Housing requirements not met."
    )
    print(f"Request {request_id_1}: {rowcount} row(s) affected.")

    print("\nUPDATE: supplied reviewer and NULL notes")
    rowcount = dao.update_adoption_request(
        request_id_2, new_adopter_id, new_cat_id, staff_id,
        "2026-11-04", "Denied", None
    )
    print(f"Request {request_id_2}: {rowcount} row(s) affected.")

    print("\nUPDATE: NULL reviewer and supplied notes")
    rowcount = dao.update_adoption_request(
        request_id_3, new_adopter_id, new_cat_id, None,
        "2026-11-04", "Pending", "Waiting for a new reviewer."
    )

    print(f"Request {request_id_3}: {rowcount} row(s) affected.")

    print("\nUPDATE: NULL reviewer and NULL notes")
    rowcount = dao.update_adoption_request(
        request_id_4, new_adopter_id, new_cat_id, None,
        "2026-11-04", "Pending", None
    )
    print(f"Request {request_id_4}: {rowcount} row(s) affected.")

    show_requests(dao, "\nAdoptionRequests after UPDATE:")

    # Remove our test requests, and leave the original sample requests
    print("\nDELETE: remove the four test requests")
    for request_id in [request_id_1, request_id_2, request_id_3, request_id_4]:
        rowcount = dao.delete_adoption_request(request_id)
        print(f"Request {request_id}: {rowcount} row(s) affected.")

    show_requests(dao, "\nAdoptionRequests after DELETE:")

    # DAO will handle its cursors and commits; close connection here
    db.close()

    print("\nFinished testing Catabase. Connection now closed.")


if __name__ == "__main__":
    main()






