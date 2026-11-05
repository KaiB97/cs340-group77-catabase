# Course: CS340 Fall 2026
# Project Step 3 Draft: Python Application-Tier
# Team Members: Kaia Bahar, Max Riley, Ashley Davis
# Group Number: 77
# Citation for the following code:
# Date: 11/3/2026
# Based on:
# CS340 Fall 2026 Canvas, Exploration - Connecting Python to MySQL and Build a CRUD CLI
# https://canvas.oregonstate.edu/courses/2061186/pages/exploration-connecting-python-to-mysql-and-build-a-crud-cli?module_item_id=27088391

class CatabaseDAO:
    """ Data Access Object (DAO) for Catabase. """
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
        cursor = self.db.cursor(dictionary=True)
        sql = """
        SELECT adoptionReqID, adopterID, catID, reviewedByStaffID, adoptionReqDate, adoptionReqStatus, adoptionReqNotes
        FROM AdoptionRequests
        ORDER BY adoptionReqID
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_all_foster_assignments(self):
        cursor = self.db.cursor(dictionary=True)
        sql = """
        SELECT fosterAssignmentID, fosterHomeID, catID, fosterStartDate, fosterEndDate, fosterReason
        FROM FosterAssignments
        ORDER BY fosterAssignmentID
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    def add_adoption_request(self, adopter_id, cat_id, reviewed_by_staff_id, request_date, request_status, request_notes):
        cursor = self.db.cursor()
        sql = """
        INSERT INTO AdoptionRequests (adopterID, catID, reviewedByStaffID, adoptionReqDate, adoptionReqStatus, adoptionReqNotes)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (adopter_id, cat_id, reviewed_by_staff_id, request_date, request_status, request_notes))
        self.db.commit()
        request_id = cursor.lastrowid
        cursor.close()
        return request_id

    def update_adoption_request(self, request_id, adopter_id, cat_id, reviewed_by_staff_id, request_date, request_status, request_notes):
        cursor = self.db.cursor()
        sql = """
        UPDATE AdoptionRequests
        SET adopterID = %s, catID = %s, reviewedByStaffID = %s, adoptionReqDate = %s, adoptionReqStatus = %s, adoptionReqNotes = %s
        WHERE adoptionReqID = %s
        """
        cursor.execute(sql, (adopter_id, cat_id, reviewed_by_staff_id, request_date, request_status, request_notes, request_id))
        self.db.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def delete_adoption_request(self, request_id):
        cursor = self.db.cursor()
        sql = "DELETE FROM AdoptionRequests WHERE adoptionReqID = %s"
        cursor.execute(sql, (request_id,))
        self.db.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount
