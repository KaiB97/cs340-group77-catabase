# Course: CS340 Fall 2026
# Project Step 3 FINAL: Python Application-Tier
# Team Members: Kaia Bahar, Max Riley, Ashley Davis
# Group Number: 77
# Date: 11/9/2026 
# Citation for the following code:
# CS340 Fall 2026 Canvas, Exploration - Connecting Python to MySQL and Build a CRUD CLI
# https://canvas.oregonstate.edu/courses/2061186/pages/exploration-connecting-python-to-mysql-and-build-a-crud-cli?module_item_id=27088391
# CS340 Fall 2026 Canvas, Exploration - Designing a Python Class for Database CRUD Operations
# https://canvas.oregonstate.edu/courses/2061186/pages/exploration-designing-a-python-class-for-database-crud-operations?module_item_id=27088390

import mysql.connector


class CatabaseDAO:
    """
    Data Access Object (DAO) for Catabase.

    This class is the application tier. Client code (test_driver.py) only calls
    these methods and never writes SQL. Every method uses parameterized SQL (%s),
    so values are passed separately from the query text.

    READ:   all six tables
    CREATE / UPDATE / DELETE: the AdoptionRequests intersection table (Adopters <-> Cats)

    The create, update, and delete methods commit on success. If MySQL rejects the
    statement (for example, a catID that does not exist), the transaction is rolled
    back and the mysql.connector.Error is re-raised so the caller can decide what to do.
    """

    def __init__(self, db_connection):
        self.db = db_connection


    def get_all_cats(self):
        cursor = self.db.cursor(dictionary=True)
        sql = """
        SELECT catID, catName, estimatedAge, intakeDate, breed, temperament, adoptionStatus
        FROM Cats
        ORDER BY catID
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_all_adopters(self):
        cursor = self.db.cursor(dictionary=True)
        sql = """
        SELECT adopterID, fName, lName, phoneNumber, email, homeType, city
        FROM Adopters
        ORDER BY adopterID
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_all_staff_members(self):
        cursor = self.db.cursor(dictionary=True)
        sql = """
        SELECT staffID, fName, lName, staffPosition, email
        FROM StaffMembers
        ORDER BY staffID
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_all_foster_homes(self):
        cursor = self.db.cursor(dictionary=True)
        sql = """
        SELECT fosterHomeID, fosterName, fosterStatus, phoneNumber, city, maxNumberCats
        FROM FosterHomes
        ORDER BY fosterHomeID
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_all_adoption_requests(self):
        """READ for the AdoptionRequests intersection table (includes requests with no reviewer)."""
        cursor = self.db.cursor(dictionary=True)
        sql = """
        SELECT ar.adoptionReqID, ar.adopterID, CONCAT(a.fName, ' ', a.lName) AS adopterName,
               ar.catID, c.catName,
               ar.reviewedByStaffID, CONCAT(s.fName, ' ', s.lName) AS reviewerName,
               ar.adoptionReqDate, ar.adoptionReqStatus, ar.adoptionReqNotes
        FROM AdoptionRequests ar
        JOIN Adopters a ON ar.adopterID = a.adopterID
        JOIN Cats c ON ar.catID = c.catID
        LEFT JOIN StaffMembers s ON ar.reviewedByStaffID = s.staffID
        ORDER BY ar.adoptionReqID
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_all_foster_assignments(self):
        """READ for the FosterAssignments intersection table (NULL end date = ongoing placement)."""
        cursor = self.db.cursor(dictionary=True)
        sql = """
        SELECT fa.fosterAssignmentID, fa.fosterHomeID, fh.fosterName,
               fa.catID, c.catName,
               fa.fosterStartDate, fa.fosterEndDate, fa.fosterReason
        FROM FosterAssignments fa
        JOIN FosterHomes fh ON fa.fosterHomeID = fh.fosterHomeID
        JOIN Cats c ON fa.catID = c.catID
        ORDER BY fa.fosterAssignmentID
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results


    def add_adoption_request(self, adopter_id, cat_id, reviewed_by_staff_id, request_date, request_status, request_notes):
        """Insert one adoption request. Returns the new adoptionReqID."""
        cursor = self.db.cursor()
        sql = """
        INSERT INTO AdoptionRequests (adopterID, catID, reviewedByStaffID, adoptionReqDate, adoptionReqStatus, adoptionReqNotes)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (adopter_id, cat_id, reviewed_by_staff_id, request_date, request_status, request_notes))
            self.db.commit()
            return cursor.lastrowid
        except mysql.connector.Error:
            self.db.rollback()
            raise
        finally:
            cursor.close()

    def update_adoption_request(self, request_id, adopter_id, cat_id, reviewed_by_staff_id, request_date, request_status, request_notes):
        """Update every editable field of one request. Returns the number of rows changed (0 or 1)."""
        cursor = self.db.cursor()
        sql = """
        UPDATE AdoptionRequests
        SET adopterID = %s, catID = %s, reviewedByStaffID = %s, adoptionReqDate = %s, adoptionReqStatus = %s, adoptionReqNotes = %s
        WHERE adoptionReqID = %s
        """
        try:
            cursor.execute(sql, (adopter_id, cat_id, reviewed_by_staff_id, request_date, request_status, request_notes, request_id))
            self.db.commit()
            return cursor.rowcount
        except mysql.connector.Error:
            self.db.rollback()
            raise
        finally:
            cursor.close()

    def update_request_status(self, request_id, request_status):
        """
        Helper: change only adoptionReqStatus, so callers do not have to pass all
        seven values to update_adoption_request. Returns the number of rows changed (0 or 1).
        """
        cursor = self.db.cursor()
        sql = """
        UPDATE AdoptionRequests
        SET adoptionReqStatus = %s
        WHERE adoptionReqID = %s
        """
        try:
            cursor.execute(sql, (request_status, request_id))
            self.db.commit()
            return cursor.rowcount
        except mysql.connector.Error:
            self.db.rollback()
            raise
        finally:
            cursor.close()

    def delete_adoption_request(self, request_id):
        """Delete one request only; the related adopter, cat, and staff rows are untouched. Returns rows deleted (0 or 1)."""
        cursor = self.db.cursor()
        sql = "DELETE FROM AdoptionRequests WHERE adoptionReqID = %s"
        try:
            cursor.execute(sql, (request_id,))
            self.db.commit()
            return cursor.rowcount
        except mysql.connector.Error:
            self.db.rollback()
            raise
        finally:
            cursor.close()
