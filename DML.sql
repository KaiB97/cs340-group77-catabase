-- Course: CS340 Fall 2026
-- Project Step 3 FINAL: Catabase
-- Team Members: Kaia Bahar, Max Riley, Ashley Davis
-- Group Number: 77
-- Citation for the following code: CS340 course materials used as guidelines for the code below (the full list of sources is in README.md).
-- Curry, M. (November 2026). CS340 Fall 2026 Canvas: Project Step 3 Draft Version: Design Python Class Application + DML SQL - sample_data_manipulation_queries.sql [Course material]. https://canvas.oregonstate.edu/courses/2061186/files/119792862?wrap=1
-- Curry, M. (November 2026). CS340 Fall 2026 Canvas: What is CRUD? [Course material]. https://canvas.oregonstate.edu/courses/2061186/pages/what-is-crud-2?module_item_id=27088389


-- These are the Database Manipulation queries for the Catabase's application tier-class.
-- Using the Catabase database.
-- These queries read all six tables, and add, update (all fields or status only), and delete records in the AdoptionRequests intersection table.
-- Many-to-Many relationship: AdoptionRequests connects Adopters and Cats.


-- Variables that will be supplied by the application use descriptive :name placeholders (a colon followed by the name); each name identifies the value to supply.
-- In catabase_dao.py these markers become %s parameters, so values are never pasted into the SQL text.
-- Dates use YYYY-MM-DD.
-- Missing notes or a missing reviewer is supplied as SQL NULL.
-- For purposes of MySQL testing, replace markers :name with the test values.
-- Method comments correspond to CatabaseDAO in the catabase_dao.py python module



-- get all cats and their corresponding IDs to display cat profiles and select a cat for a request
-- Application method: get_all_cats
SELECT catID, catName, estimatedAge, intakeDate, breed, temperament, adoptionStatus
FROM Cats
ORDER BY catID;


-- get all adopters and their corresponding IDs to display applicants and select an adopter for a request
-- Application method: get_all_adopters
SELECT adopterID, fName, lName, phoneNumber, email, homeType, city
FROM Adopters
ORDER BY adopterID;


-- get all staff members and their corresponding IDs to display staff and select a request reviewer
-- Application method: get_all_staff_members
SELECT staffID, fName, lName, staffPosition, email
FROM StaffMembers
ORDER BY staffID;


-- get all foster homes, including their availability status and maximum cat capacity
-- Application method: get_all_foster_homes
SELECT fosterHomeID, fosterName, fosterStatus, phoneNumber, city, maxNumberCats
FROM FosterHomes
ORDER BY fosterHomeID;


-- get all adoption requests to display their details, and their corresponding IDs for update/delete
-- Application method: get_all_adoption_requests 
-- Requests without a reviewer included
SELECT ar.adoptionReqID, ar.adopterID, CONCAT(a.fName, ' ', a.lName) AS adopterName,
       ar.catID, c.catName,
       ar.reviewedByStaffID, CONCAT(s.fName, ' ', s.lName) AS reviewerName,
       ar.adoptionReqDate, ar.adoptionReqStatus, ar.adoptionReqNotes
FROM AdoptionRequests ar
JOIN Adopters a ON ar.adopterID = a.adopterID
JOIN Cats c ON ar.catID = c.catID
LEFT JOIN StaffMembers s ON ar.reviewedByStaffID = s.staffID
ORDER BY ar.adoptionReqID;



-- get all foster assignments to display current and previous foster placements
-- Application method: get_all_foster_assignments
-- NULL end date indicates the foster placement is ongoing
SELECT fa.fosterAssignmentID, fa.fosterHomeID, fh.fosterName,
       fa.catID, c.catName,
       fa.fosterStartDate, fa.fosterEndDate, fa.fosterReason
FROM FosterAssignments fa
JOIN FosterHomes fh ON fa.fosterHomeID = fh.fosterHomeID
JOIN Cats c ON fa.catID = c.catID
ORDER BY fa.fosterAssignmentID;



-- add an adoption request to associate an adopter with a cat (M:N addition)
-- Application method: add_adoption_request
-- Params: 1) adopter_id
--         2) cat_id
--         3) reviewed_by_staff_id
--         4) request_date
--         5) request_status
--         6) request_notes
-- MySQL will generate adoptionReqID
-- Adopter and cat must already exist; if a reviewer is given, this staff member must already exist as well
INSERT INTO AdoptionRequests (adopterID, catID, reviewedByStaffID, adoptionReqDate, adoptionReqStatus, adoptionReqNotes)
VALUES (:adopter_id, :cat_id, :reviewed_by_staff_id, :request_date, :request_status, :request_notes);



-- update the selected adoption request, including the adopter, cat, and review information
-- Application method: update_adoption_request
-- Params: 1) adopter_id
--         2) cat_id
--         3) reviewed_by_staff_id
--         4) request_date
--         5) request_status
--         6) request_notes
--         7) request_id
-- Provide six new field values and ensure to pass any existing values kept the same (can correct the adopter/cat relationship and update review details)
-- Although SQL needs request_id last for WHERE, the method will take request_id first
-- Updating a request will not change the Cats.adoptionStatus field - separate
UPDATE AdoptionRequests
SET adopterID = :adopter_id,
    catID = :cat_id,
    reviewedByStaffID = :reviewed_by_staff_id,
    adoptionReqDate = :request_date,
    adoptionReqStatus = :request_status,
    adoptionReqNotes = :request_notes
WHERE adoptionReqID = :request_id;



-- DAO method update_request_status runs this query.
-- updates only the status of the selected adoption request (helper so callers do not pass all seven values)
-- Application method: update_request_status
-- Params: 1) request_status
--         2) request_id
-- Although SQL needs request_id last for WHERE, the method takes request_id first
UPDATE AdoptionRequests
SET adoptionReqStatus = :request_status
WHERE adoptionReqID = :request_id;



-- delete the selected adopter-cat request (M:N deletion)
-- Application method: delete_adoption_request
-- Param: 1) request_id
-- delete only this adoption request; the adopter, cat, and staff records remain in their tables
DELETE FROM AdoptionRequests
WHERE adoptionReqID = :request_id;
