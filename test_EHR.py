"""Test navigation."""
import pytest

from HW3 import (
    parse_data,
    num_older_than,
    sick_patients,
    age_first_adm,
    create_patient_class,
    create_lab_class,
)


def test_parse_data():
    """Test data parsing."""
    Test_Lab_1 = "Test_Lab_1.txt"
    Test_Patient_1 = "Test_Patient_1.txt"
    filename_patient = Test_Patient_1
    filename_lab = Test_Lab_1

    # parsed_patient_data = parse_data(filename_patient)
    # parsed_lab_data = parse_data(filename_lab)

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


def test_create_patient_class():
    Test_Patient_1 = "Test_Patient_1.txt"
    parsed_patient_data = parse_data(Test_Patient_1)
    assert (
        create_patient_class(parsed_patient_data)[0].patient_id
        == "F0B53A2C-98CA-415D-B928-E3FD0E52B22A"
    )
    assert create_patient_class(parsed_patient_data)[0].gender == "Male"
    assert create_patient_class(parsed_patient_data)[0].DOB == "1950-06-20 10:31:18.337"
    assert create_patient_class(parsed_patient_data)[0].race == "African American"
    assert create_patient_class(parsed_patient_data)[0].age == 72
    assert create_patient_class(parsed_patient_data)[2].gender == "Female"
    assert create_patient_class(parsed_patient_data)[2].race == "Hispanic"

    Test_Patient_2 = "Test_Patient_2.txt"
    parsed_patient_data = parse_data(Test_Patient_2)
    assert (
        create_patient_class(parsed_patient_data)[2].patient_id
        == "1A9487E3-A61C-455A-8DEE-763EB90C9B2B"
    )
    assert create_patient_class(parsed_patient_data)[2].race == "White"
    assert create_patient_class(parsed_patient_data)[3].age == 90


def test_create_lab_class():
    Test_Lab_1 = "Test_Lab_1.txt"
    parsed_lab_data = parse_data(Test_Lab_1)
    assert (
        create_lab_class(parsed_lab_data)[3].patient_id
        == "1A8791E3-A61C-455A-8DEE-763EB90C9B2B"
    )
    assert create_lab_class(parsed_lab_data)[3].lab == "METABOLIC: CALCIUM"
    assert create_lab_class(parsed_lab_data)[2].value == "7.8"
    assert create_lab_class(parsed_lab_data)[2].units == "mg/dL"

    Test_Lab_2 = "Test_Lab_2.txt"
    parsed_lab_data = parse_data(Test_Lab_2)
    assert create_lab_class(parsed_lab_data)[1].lab == "METABOLIC: GLUCOSE"
    assert create_lab_class(parsed_lab_data)[1].value == "103.3"
    assert create_lab_class(parsed_lab_data)[3].value == "15.8"
    assert create_lab_class(parsed_lab_data)[3].units == "%"
