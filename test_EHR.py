import pytest
import sqlite3
import os

from EHR_analysis import (
    parse_patient_data,
    parse_lab_data,
    create_patient_class,
    num_older_than,
    sick_patients,
    age_first_adm,
)


from EHR_objects import Patient, Lab


def test_parse_patient_data():
    """Test patient data parsing."""
    # os.remove("EHR_test.db")
    conn = sqlite3.connect("EHR.db")
    cur = conn.cursor()
    Test_Patient_1 = "Test_Patient_1.txt"
    parsed_patient_data = parse_patient_data(Test_Patient_1)
    a = Patient(cur, "F0B53A2C-98CA-415D-B928-E3FD0E52B22A")
    assert a.pat_id == "F0B53A2C-98CA-415D-B928-E3FD0E52B22A"
    assert a.gender == "Male"
    assert a.age == 72
    assert a.race == "African American"
    assert parsed_patient_data[1] == "F0B53A2C-98CA-415D-B928-E3FD0E52B22A"
    conn.close()


def test_parse_lab_data():
    """Test lab data parsing."""
    conn = sqlite3.connect("EHR.db")
    cur = conn.cursor()
    Test_Lab_1 = "Test_Lab_1.txt"
    parse_lab_data(Test_Lab_1)
    output = cur.execute(
        "SELECT LabValue FROM lab WHERE PatientID == '1A8791E3-A61C-455A-8DEE-763EB90C9B2C' AND LabName =='CBC: MCH'"
    ).fetchone()
    assert output[0] == 35.8
    conn.close()


def test_num_older_than():
    """Test number of patients older."""
    conn = sqlite3.connect("EHR.db")
    cur = conn.cursor()
    Test_Patient_1 = "Test_Patient_1.txt"
    pat_id_list = parse_patient_data(Test_Patient_1)
    assert num_older_than(float(60), create_patient_class(pat_id_list)) == 2
    assert num_older_than(float(80), create_patient_class(pat_id_list)) == 1
    conn.close()


def test_sick_patients():
    """Test ids of sick patients."""
    conn = sqlite3.connect("EHR.db")
    cur = conn.cursor()
    Test_Patient_1 = "Test_Patient_1.txt"
    Test_Lab_1 = "Test_Lab_1.txt"
    parse_patient_data(Test_Patient_1)
    parse_lab_data(Test_Lab_1)
    assert sick_patients("METABOLIC: CALCIUM", ">", 8.5) == {
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
    }
    assert sick_patients("METABOLIC: GLUCOSE", "<", 126.0) == {
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
    }
    assert sick_patients("CBC: MCH", ">", 36.0) == set([])


def test_age_first_adm():
    """Test age at first admission."""
    conn = sqlite3.connect("EHR.db")
    cur = conn.cursor()
    # pat1 = Patient(cursor=cur, pat_id="1A8791E3-A61C-455A-8DEE-763EB90C9B2C")
    # pat2 = Patient(cursor=cur, pat_id="220C8D43-1322-4A9D-B890-D426942A3649")
    assert age_first_adm("1A8791E3-A61C-455A-8DEE-763EB90C9B2C") == 19
    assert age_first_adm("220C8D43-1322-4A9D-B890-D426942A3649") == 24
    conn.close()
