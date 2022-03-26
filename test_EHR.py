"""Test navigation."""
import pytest

from EHR_analysis import (
    parse_data,
    num_older_than,
    sick_patients,
    age_first_adm,
)


def test_parse_data():
    """Test data parsing."""
    Test_Patient_1 = "Test_Patient_1.txt"
    Test_Lab_1 = "Test_Lab_1.txt"
    list_of_patient, list_of_lab = parse_data(Test_Patient_1, Test_Lab_1)
    assert list_of_lab[0].adm_id == str(1)
    assert list_of_lab[0].lab_value == str(1.8)
    assert list_of_patient[0].DOB == "1950-06-20 10:31:18.337"
    assert list_of_patient[0].patient_id == "F0B53A2C-98CA-415D-B928-E3FD0E52B22A"
    assert list_of_patient[1].patient_id == "1A8791E3-A61C-455A-8DEE-763EB90C9B2A"


def test_num_older_than():
    """Test number of patients older."""
    Test_Patient_1 = "Test_Patient_1.txt"
    Test_Lab_1 = "Test_Lab_1.txt"
    parsed_patient_data, _ = parse_data(Test_Patient_1, Test_Lab_1)
    assert num_older_than(float(60), parsed_patient_data) == 2
    assert num_older_than(float(80), parsed_patient_data) == 1


def test_sick_patients():
    """Test ids of sick patients."""
    Test_Patient_1 = "Test_Patient_1.txt"
    Test_Lab_1 = "Test_Lab_1.txt"
    _, parsed_lab_data = parse_data(Test_Patient_1, Test_Lab_1)
    assert sick_patients("METABOLIC: CALCIUM", "<", 8.5, parsed_lab_data) == {
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2A"
    }
    assert sick_patients("METABOLIC: GLUCOSE", "<", 126.0, parsed_lab_data) == {
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2A"
    }
    assert sick_patients("METABOLIC: GLUCOSE", ">", 126.0, parsed_lab_data) == set([])


def test_age_first_adm():
    """Test age at first admission."""
    Test_Patient_1 = "Test_Patient_1.txt"
    Test_Lab_1 = "Test_Lab_1.txt"
    parsed_patient_data, parsed_lab_data = parse_data(Test_Patient_1, Test_Lab_1)

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
