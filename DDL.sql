-- Course: CS340 Fall 2026
-- Project Step 3 Draft
-- Catabase Adoption & Shelter Management System
-- Team Members: Kaia Bahar, Ashley Davis, Max Riley
-- Group Number: Group 77

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- Remove request and assignment tables before the tables they reference 
DROP TABLE IF EXISTS `FosterAssignments`;
DROP TABLE IF EXISTS `AdoptionRequests`;
DROP TABLE IF EXISTS `FosterHomes`;
DROP TABLE IF EXISTS `Adopters`;
DROP TABLE IF EXISTS `StaffMembers`;
DROP TABLE IF EXISTS `Cats`;


-- Cats: object table
-- estimatedAge: is estimated age in months at intake
-- Store each cat's profile, does not need to be copied into each request
-- adoptionStatus: Available = open to applications; Pending = reserved by staff; Adopted = adoption completed. 
-- A pending request does not reserve a cat.
CREATE TABLE `Cats` (
    `catID` INT NOT NULL AUTO_INCREMENT,
    `catName` VARCHAR(50) NOT NULL,
    `estimatedAge` INT NOT NULL,
    `intakeDate` DATE NOT NULL,
    `breed` VARCHAR(50) NOT NULL,
    `temperament` VARCHAR(100) NULL,
    `adoptionStatus` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`catID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- StaffMembers: object table
-- Staff details are separate from the adoption requests that they review
CREATE TABLE `StaffMembers` (
    `staffID` INT NOT NULL AUTO_INCREMENT,
    `fName` VARCHAR(50) NOT NULL,
    `lName` VARCHAR(50) NOT NULL,
    `staffPosition` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`staffID`),
    CONSTRAINT `uq_StaffMembers_email` UNIQUE (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Adopters: object table
-- Unique phone numbers and emails follow the rules in our db outline
-- One adopter can submit several requests, but their contact details are only stored once
CREATE TABLE `Adopters` (
    `adopterID` INT NOT NULL AUTO_INCREMENT,
    `fName` VARCHAR(50) NOT NULL,
    `lName` VARCHAR(50) NOT NULL,
    `phoneNumber` VARCHAR(20) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `homeType` VARCHAR(50) NOT NULL,
    `city` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`adopterID`),
    CONSTRAINT `uq_Adopters_phoneNumber` UNIQUE (`phoneNumber`),
    CONSTRAINT `uq_Adopters_email` UNIQUE (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- FosterHomes: object table
-- fosterStatus records availability
-- maxNumberCats records a home's capacity for cat placements
CREATE TABLE `FosterHomes` (
    `fosterHomeID` INT NOT NULL AUTO_INCREMENT,
    `fosterName` VARCHAR(100) NOT NULL,
    `fosterStatus` VARCHAR(30) NOT NULL,
    `phoneNumber` VARCHAR(20) NOT NULL,
    `city` VARCHAR(50) NOT NULL,
    `maxNumberCats` INT NOT NULL,
    PRIMARY KEY (`fosterHomeID`),
    CONSTRAINT `uq_FosterHomes_phoneNumber` UNIQUE (`phoneNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- AdoptionRequests: event and intersection table
-- connects Adopters and Cats
-- adoptionReqStatus describes an individual adoption application, not cat availability
-- request CUD operations do not update Cats or competing requests automatically 
-- reviewedByStaffID can be NULL (until someone is assigned to review request)
-- ON UPDATE CASCADE keeps the FK values in sync if referenced ID changes
-- ON DELETE RESTRICT prevents deletion of parent records while dependent rows exist
CREATE TABLE `AdoptionRequests` (
    `adoptionReqID` INT NOT NULL AUTO_INCREMENT,
    `adopterID` INT NOT NULL,
    `catID` INT NOT NULL,
    `reviewedByStaffID` INT NULL,
    `adoptionReqDate` DATE NOT NULL,
    `adoptionReqStatus` VARCHAR(30) NOT NULL,
    `adoptionReqNotes` VARCHAR(255) NULL,
    PRIMARY KEY (`adoptionReqID`),
    CONSTRAINT `fk_AdoptionRequests_adopterID` FOREIGN KEY (`adopterID`)
        REFERENCES `Adopters` (`adopterID`) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT `fk_AdoptionRequests_catID` FOREIGN KEY (`catID`)
        REFERENCES `Cats` (`catID`) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT `fk_AdoptionRequests_reviewedByStaffID` FOREIGN KEY (`reviewedByStaffID`)
        REFERENCES `StaffMembers` (`staffID`) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- FosterAssignments: event and intersection table
-- each row records one cat's stay in a foster home
-- separate assignment ID allows the same cat to return to the same home at a later point
-- Foster placements represent temporary care, not completed adoptions.
-- NULL fosterEndDate means palcement is ongoing 
CREATE TABLE `FosterAssignments` (
    `fosterAssignmentID` INT NOT NULL AUTO_INCREMENT,
    `fosterHomeID` INT NOT NULL,
    `catID` INT NOT NULL,
    `fosterStartDate` DATE NOT NULL,
    `fosterEndDate` DATE NULL,
    `fosterReason` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`fosterAssignmentID`),
    CONSTRAINT `fk_FosterAssignments_fosterHomeID` FOREIGN KEY (`fosterHomeID`)
        REFERENCES `FosterHomes` (`fosterHomeID`) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT `fk_FosterAssignments_catID` FOREIGN KEY (`catID`)
        REFERENCES `Cats` (`catID`) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



-- Re-enable foreign-key checks before inserting sample data
-- COMMIT at the end saves the sample-data inserts
SET FOREIGN_KEY_CHECKS = 1;



-- Example data for Cats
INSERT INTO `Cats` (`catID`, `catName`, `estimatedAge`, `intakeDate`, `breed`, `temperament`, `adoptionStatus`) VALUES
    (1, 'Theo', 24, '2026-09-01', 'Ragdoll', 'Calm', 'Available'),
    (2, 'Jupiter', 12, '2026-09-01', 'Mainecoon', 'Playful', 'Adopted'),
    (3, 'Bella', 36, '2026-09-28', 'Domestic Longhair', NULL, 'Available'),
    (4, 'Coco', 18, '2026-10-15', 'Bengal', 'Shy', 'Pending');

-- Example data for StaffMembers
INSERT INTO `StaffMembers` (`staffID`, `fName`, `lName`, `staffPosition`, `email`) VALUES
    (1, 'Alex', 'Morgan', 'Adoption Coordinator', 'alex.morgan@example.com'),
    (2, 'Jamie', 'Patel', 'Shelter Volunteer', 'jamie.patel@example.com'),
    (3, 'Casey', 'Lee', 'Foster Coordinator', 'casey.lee@example.com');

-- Example data for Adopters
INSERT INTO `Adopters` (`adopterID`, `fName`, `lName`, `phoneNumber`, `email`, `homeType`, `city`) VALUES
    (1, 'Kaia', 'Bahar', '905-123-456', 'bahark@oregonstate.edu', 'House', 'Toronto'),
    (2, 'Jordan', 'Singh', '416-555-0102', 'jordan.singh@example.com', 'House', 'Toronto'),
    (3, 'Taylor', 'Brooks', '905-555-0103', 'taylor.brooks@example.com', 'Townhouse', 'Hamilton');

-- Example data for FosterHomes
INSERT INTO `FosterHomes` (`fosterHomeID`, `fosterName`, `fosterStatus`, `phoneNumber`, `city`, `maxNumberCats`) VALUES
    (1, 'Maple Foster Home', 'Available', '416-555-0111', 'Toronto', 3),
    (2, 'Cedar Foster Home', 'Available', '905-555-0112', 'Hamilton', 2),
    (3, 'Willow Foster Home', 'Unavailable', '905-555-0113', 'Burlington', 1);

-- Example data for AdoptionRequests
INSERT INTO `AdoptionRequests` (`adoptionReqID`, `adopterID`, `catID`, `reviewedByStaffID`, `adoptionReqDate`, `adoptionReqStatus`, `adoptionReqNotes`) VALUES
    (1, 1, 1, 1, '2026-09-05', 'Denied', 'Housing requirements not met.'),
    (2, 2, 1, NULL, '2026-10-21', 'Pending', NULL),
    (3, 1, 2, 1, '2026-10-01', 'Approved', 'Adoption completed.'),
    (4, 3, 3, 2, '2026-10-22', 'Pending', 'Initial review completed; follow-up needed.'),
    (5, 2, 4, NULL, '2026-10-23', 'Pending', NULL);

-- Example data for FosterAssignments
INSERT INTO `FosterAssignments` (`fosterAssignmentID`, `fosterHomeID`, `catID`, `fosterStartDate`, `fosterEndDate`, `fosterReason`) VALUES
    (1, 1, 1, '2026-09-01', '2026-09-10', 'Quiet environment'),
    (2, 2, 1, '2026-09-10', '2026-09-20', 'Temporary caregiver availability'),
    (3, 1, 1, '2026-09-20', NULL, 'Return to familiar home'),
    (4, 2, 2, '2026-09-01', '2026-09-25', 'Shelter capacity'),
    (5, 1, 3, '2026-10-01', NULL, 'Socialization');



COMMIT;
SET FOREIGN_KEY_CHECKS = 1;
SET AUTOCOMMIT = 1;
