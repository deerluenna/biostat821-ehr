"""Test navigation."""
import pytest

from EHR_analysis import parse_data, num_older_than, sick_patients, age_first_adm


def test_parse_data():
    """Test data parsing."""
    filename_patient = "Test_Patient_1.txt"
    filename_lab = T"Test_Lab_1.txt"

    assert parse_data(filename_lab)[1][1] == str(1)
    assert parse_data(filename_lab)[1][3] == str(1.8)
    assert parse_data(filename_patient)[1][2] == "1950-06-20 10:31:18.337"
    assert parse_data(filename_patient)[1][0] == "F0B53A2C-98CA-415D-B928-E3FD0E52B22A"
    assert parse_data(filename_patient)[2][0] == "1A8791E3-A61C-455A-8DEE-763EB90C9B2A"


def test_num_older_than():
    """Test number of patients older."""
    Test_Patient_1 = "Test_Patient_1.txt"
    parsed_patient_data = parse_data(Test_Patient_1)
    assert num_older_than("70", parsed_patient_data) == 2
    assert num_older_than("80", parsed_patient_data) == 1


def test_sick_patients():
    """Test ids of sick patients."""
    Test_Lab_1 = "Test_Lab_1.txt"
    parsed_lab_data = parse_data(Test_Lab_1)
    assert sick_patients("METABOLIC: CALCIUM", "<", "8.5", parsed_lab_data) == [
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2A"
    ]
    assert sick_patients("METABOLIC: GLUCOSE", "<", "126.0", parsed_lab_data) == [
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2A"
    ]
    assert (
        sick_patients("METABOLIC: GLUCOSE", ">", "126.0", parsed_lab_data)
        == "No one is larger"
    )


def test_age_first_adm():
    """Test age at first admission."""
    Test_Lab_1 = "Test_Lab_1.txt"
    parsed_lab_data = parse_data(Test_Lab_1)
    Test_Patient_1 = "Test_Patient_1.txt"
    parsed_patient_data = parse_data(Test_Patient_1)
    assert (
        age_first_adm(
            parsed_patient_data, parsed_lab_data, "1A8791E3-A61C-455A-8DEE-763EB90C9B2A"
        )
        == 12
    )
    assert (
        age_first_adm(
            parsed_patient_data, parsed_lab_data, "1A8791E3-A61C-455A-8DEE-763EB90C9B2B"
        )
        == 22
    )
