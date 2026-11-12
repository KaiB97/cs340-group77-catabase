-- Course: CS340 Fall 2026
-- Project Step 3 Draft: Catabase
-- Team Members: Kaia Bahar, Max Riley, Ashley Davis
-- Group Number: 77
-- Citation for the following code: 
-- Date: 11/3/2026
-- Adapted from the CS340 sample data manipulation queries.
-- See README Acknowledgements for full course material citations.


-- These are the Database Manipulation queries for the Catabase's application tier-class.
-- Using the Catabase database.
-- These queries read all six tables, and add, update, and delete records in the AdoptionRequests intersection table.
-- Many-to-Many relationship: AdoptionRequests connects Adopters and Cats.


-- Variables that will be supplied by the application use descriptive :name placeholder; each name identifies the value to supply.
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
SELECT AdoptionRequests.adoptionReqID,
       AdoptionRequests.adopterID,
       AdoptionRequests.catID,
       AdoptionRequests.reviewedByStaffID,
       AdoptionRequests.adoptionReqDate,
       AdoptionRequests.adoptionReqStatus,
       AdoptionRequests.adoptionReqNotes,
       Adopters.fName AS adopterFirstName,
       Adopters.lName AS adopterLastName,
       Cats.catName
FROM AdoptionRequests
INNER JOIN Adopters ON AdoptionRequests.adopterID = Adopters.adopterID
INNER JOIN Cats ON AdoptionRequests.catID = Cats.catID
ORDER BY AdoptionRequests.adoptionReqID;



-- get all foster assignments to display current and previous foster placements
-- Application method: get_all_foster_assignments
-- NULL end date indicates the foster placement is ongoing
SELECT FosterAssignments.fosterAssignmentID,
       FosterAssignments.fosterHomeID,
       FosterAssignments.catID,
       FosterAssignments.fosterStartDate,
       FosterAssignments.fosterEndDate,
       FosterAssignments.fosterReason,
       Cats.catName,
       FosterHomes.fosterName
FROM FosterAssignments
INNER JOIN Cats ON FosterAssignments.catID = Cats.catID
INNER JOIN FosterHomes ON FosterAssignments.fosterHomeID = FosterHomes.fosterHomeID
ORDER BY FosterAssignments.fosterAssignmentID;



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



-- delete the selected adopter-cat request (M:N deletion)
-- Application method: delete_adoption_request
-- Param: 1) request_id
-- delete only this adoption request; the adopter, cat, and staff records remain in their tables
DELETE FROM AdoptionRequests
WHERE adoptionReqID = :request_id;