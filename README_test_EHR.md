# EHR_analysis
The EHR_analysis contains several functions to process and analyze EHR data. The inputs are a patient file and a lab file, which are in formats of txt files. The former has 7 columns and the latter has 6 columns.

## For End Users
This project has four modules:
- `parse_data` contains a function to parse lab and patient data.
    Inputs include patient file name with file type (e.g. "Patient.txt") and lab file name with file type (e.g. "Lab.txt") to allow further analysis.
- `num_older_than` contains a function to calculate the number of patients older than the age entered.
    Inputs include age (int) and the patient file previously entered.
- `sick_patients` contains the IDs of patients who are sick based on the diagnostic criteria entered.
    Inputs include lab test name (e.g. "CBC: MCH"), boolean operation (e.g. ">" or "<"), critical value (e.g. "35.8"), and the previously entered lab file.
- `age_first_adm` contains the age of entered patient at his/her first lab data.
    Inputs include patient id (e.g. "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"), previously entered patient and lab files.

## For Contributors Running Tests
Test modules are placed in the `test_EHR.py`. Importation of `pytest` is required for testing. Note that tests is not a Python package and has no "__init__.py" file.

pytest has many command line options with a powerful discovery mechanism:
- `python pytest test_EHR.py` to run test on EHR_analysis.
- `python -m pytest` to discover and run all tests from the current directory.
- `python -m pytest -v` to explicitly print the result of each test as it is run.
- `python -m pytest -h` for command line help.
It is also possible to run pytest directly with the "pytest" or "py.test" command.