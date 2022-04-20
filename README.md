# EHR_analysis
## Setup
This project is written in Python3. Some packages used in the scripts include:
- typing
- datetime

The EHR_analysis,py module contains several functions to process and analyze EHR data. The inputs are a patient file and a lab file, which are in formats of txt files. The former has 7 columns and the latter has 6 columns. They shoulde be in the same folder as the EHR_analysis.py file to work properly. 
- Patient data: Contains patient demographics data
- Lab data: Contains laboratory results of patients

Some requirements of the data files are:
- The first row is a header containing column names
- Every column is separated by tabs

In the EHR_analysis module, we also included a Patient and a Lab class to help store information needed. The descriptions are in the following.

## Class Descriptions
### Lab Class
The Lab class has instance attributes including:
- PatientID
- PatientGender
- PatientDateOfBirth
- PatientRace

## Patient Class
The Patient class has instance attributes including:
- PatientID
- LabName
- LabValue
- LabUnit
- LabDateTime

## For End Users
The EHR_analysis module has 6 main functions:
- `parse_data` contains a function to parse patient and lab data.
    Inputs include patient file name with file type (e.g. "Patient.txt") and lab file name with file type (e.g. "Lab.txt") to allow further analysis.
- `num_older_than` contains a function to calculate the number of patients older than the age entered.
    Inputs include age (int) and the patient file previously entered.
- `sick_patients` contains the IDs of patients who are sick based on the diagnostic criteria entered.
    Inputs include lab test name (e.g. "CBC: MCH"), boolean operation (e.g. ">" or "<"), critical value (e.g. "35.8"), and the previously entered lab file.
- `age_first_adm` contains the age of entered patient at his/her first lab data.
    Inputs include patient id (e.g. "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"), previously entered patient and lab files.
- `create_patient_class` contains a function to create patient objects with attributes including patient ID, gender, date of birth, and race.
- `create_lab_class` contains a function to create lab objects with attributes including patient ID, lab name, value, units, and lab date.

## For Contributors Running Tests
Test modules are placed in the `test_EHR.py`. Importation of `pytest` is required for testing. The files `Test_Patient_1.txt`, `Test_Patient_2.txt`, `Test_Lab_1`, and `Test_Lab_2` are included to be used for testing.

pytest has many command line options with a powerful discovery mechanism:
- `python pytest test_EHR.py` to run test on EHR_analysis.
- `python -m pytest` to discover and run all tests from the current directory.
- `python -m pytest -v` to explicitly print the result of each test as it is run.
- `python -m pytest -h` for command line help.
It is also possible to run pytest directly with the "pytest" or "py.test" command.