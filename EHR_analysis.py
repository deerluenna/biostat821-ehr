from datetime import datetime
from typing import List, Dict
from EHR_objects import Patient, Lab
import sqlite3
import os

conn = sqlite3.connect("EHR.db")
cur = conn.cursor()


def parse_patient_data(filename_patient: str):
    """
    Parse the patient data file, create a table with patient information in the database.
    Input: String of patient filename
    Output: None

    The computational complexity for the parser function is
    N*(1+1) + N*(1+1) + N*1 + N*1 + N + N → 8N → N.
    """
    # Create patient and lab tables in database
    cur.execute("DROP TABLE IF EXISTS patient")  # Drop the table if exists
    cur.execute(
        "CREATE TABLE IF NOT EXISTS patient(PatientID TEXT, PatientGender TEXT, PatientDateOfBirth TEXT, \
        PatientRace TEXT, PatientMaritalStatus TEXT, PatientLanguage TEXT, PatientPopulationPercentageBelowPoverty REAL)"
    )
    with open(filename_patient, "r", encoding="utf-8-sig") as patient_file:
        text = patient_file.readlines()
        for line in text:
            col_in_line = line.strip().split("\t")
            a, b, c, d, e, f, g = col_in_line
            # print(a, b, c, d, e, f, g)
            cur.execute(
                f"INSERT INTO patient VALUES('{a}','{b}','{c}','{d}','{e}','{f}','{g}')"
            )
    # selected = cur.execute("SELECT PatientID FROM patient WHERE PatientDateOfBirth = '1947-12-28 02:45:40.547'").fetchall()
    # print(selected)
    conn.commit()


def parse_lab_data(filename_lab: str):
    """
    Parse the lab data file, create a table with lab information in the database.
    Input: String of lab filename
    Output: None

    The computational complexity for the parser function is
    N*(1+1) + N*(1+1) + N*1 + N*1 + N + N → 8N → N.
    """
    cur.execute(
        "CREATE TABLE IF NOT EXISTS lab(PatientID TEXT, AdmissionID INT, LabName TEXT, \
        LabValue REAL, LabUnits STR, LabDateTime STR)"
    )

    with open(filename_lab, "r", encoding="utf-8-sig") as lab_file:
        text = lab_file.readlines()
        for line in text:
            col_in_line = line.strip().split("\t")
            a, b, c, d, e, f = col_in_line
            # print(a, b, c, d, e, f)
            cur.execute(f"INSERT INTO lab VALUES('{a}','{b}','{c}','{d}','{e}','{f}')")
    conn.commit()


# class Patient:
#     """
#     Patient class: each patient class object represents an unique patient,
#     and contains information such as patient ID, gender, date of birth, and race.
#     """

#     def __init__(self, cursor, pat_id: str):
#         """Initialize."""
#         self.cursor = cursor
#         self.pat_id = pat_id

#     @property
#     def gender(self):
#         _gender = self.cursor.execute(
#             f"SELECT PatientGender FROM patient WHERE PatientID = '{self.pat_id}'"
#         ).fetchone()  # Fetch gender info
#         return _gender[0]

#     @property
#     def race(self):
#         _race = self.cursor.execute(
#             f"SELECT PatientRace FROM patient WHERE PatientID = '{self.pat_id}'"
#         ).fetchone()  # Fetch Race info
#         return _race[0]

#     @property
#     def DOB(self):
#         _DOB = self.cursor.execute(
#             f"SELECT PatientDateOfBirth FROM patient WHERE PatientID = '{self.pat_id}';"
#         ).fetchone() # Fetch DOB info
#         return _DOB[0]

#     @property
#     def age(self):
#         """Function to calculate age property."""
#         p_birth = datetime.strptime(self.DOB, "%Y-%m-%d %H:%M:%S.%f").year
#         return datetime.now().year - p_birth


# class Lab:
#     """
#     Lab class: each lab class object represents a lab diagnosis result of a patient,
#     and contains information such as patient ID, date of diagnosis, and the name, value and units of the lab examination.
#     """

#     def __init__(
#         self,
#         cursor,
#         pat_id: str,
#         adm_id: str,
#         lab_name: str,
#     ):
#         self.cursor = cursor
#         self.pat_id = pat_id
#         self.adm_id = adm_id
#         self.lab_name = lab_name

#     @property
#     def lab_value(self):
#         _lab_value = self.cursor.execute(
#             f"SELECT LabValue FROM lab WHERE PatientID = '{self.pat_id}' \
#                 AND AdmissionID = '{self.adm_id}' AND LabName = '{self.lab_name}'"
#         ).fetchone()
#         return _lab_value[0]

#     @property
#     def units(self):
#         _units = self.cursor.execute(
#             f"SELECT LabUnits FROM lab WHERE PatientID = '{self.pat_id}' \
#                 AND AdmissionID = '{self.adm_id}' AND LabName = '{self.lab_name}'"
#         ).fetchone()
#         return _units[0]

#     @property
#     def lab_date(self):
#         _lab_date = self.cursor.execute(
#             f"SELECT lab.LabDateTime FROM lab WHERE PatientID = '{self.pat_id}' \
#                 AND AdmissionID = '{self.adm_id}' AND LabName = '{self.lab_name}'"
#         ).fetchone()
#         return _lab_date[0]


def create_patient_class() -> list[Patient]:
    patient_id_list = cur.execute("SELECT patient.PatientID FROM patient").fetchall()
    # print(patient_id_list)
    list_of_patient_object = []
    for patient_id in patient_id_list[1:]:  # N times
        patient_object = Patient(cursor=cur, pat_id=patient_id[0])  # 0(1)
        list_of_patient_object.append(patient_object)
    #print(list_of_patient_object[0].pat_id, list_of_patient_object[0].gender)
    return list_of_patient_object


def create_lab_class() -> list[Lab]:
    lab_info_list = cur.execute(
        "SELECT lab.PatientID, lab.AdmissionID, lab.LabName FROM lab"
    ).fetchall()
    list_of_lab_object = []
    # print(lab_info_list[1])
    for PatientID, AdmissionID, LabName in lab_info_list[1:]:  # N times
        lab_object = Lab(
            cursor=cur, pat_id=PatientID, adm_id=AdmissionID, lab_name=LabName
        )  # 0(1)
        list_of_lab_object.append(lab_object)
    #print(list_of_lab_object[0].pat_id, list_of_lab_object[0].lab_name)
    return list_of_lab_object


## Number of patients older
def num_older_than(age: float, list_of_patient_object: list[Patient]) -> int:
    """
    Calculate the number of patients whose age are older than a certain entered age.
    Input: 1. Float of age 2. List of patient objects
    Output: Integer of number of patients

    The computational complexity for the parser function is
    N*(1+1) → 2N → N.
    """
    num = 0
    for patient_object in list_of_patient_object:  # N times
        # print(patient_object.gender)
        if patient_object.age > age:  # 0(1)
            num += 1
    return num


## Sick patient IDs
def sick_patients(
    lab: str, gt_lt: str, value: float, list_of_lab_object: list[Lab]
) -> set[str]:
    """
    Find unique patient IDs with a lab value greater or less than
    the given value of the specified lab type.

    The computational complexity is N*1 + N*1 → N.
    """

    id_larger = set()
    id_smaller = set()

    if (gt_lt != ">") & (gt_lt != "<"):  # 0(1)
        raise ValueError("Operator input should be either '>' or '<'")
    elif gt_lt == ">":  # 0(1)
        for lab_object in list_of_lab_object:  # N times
            if (
                lab == lab_object.lab_name and float(lab_object.lab_value) > value
            ):  # 0(1)
                id_larger.add(lab_object.pat_id)
    elif gt_lt == "<":  # 0(1)
        for lab_object in list_of_lab_object:  # N times
            if (
                lab == lab_object.lab_name and float(lab_object.lab_value) < value
            ):  # 0(1)
                id_smaller.add(lab_object.pat_id)

    if id_larger:  # 0(1)
        return id_larger
    elif gt_lt == ">":
        return set([])

    if id_smaller:  # 0(1)
        return id_smaller
    elif gt_lt == "<":
        return set([])

    raise ValueError("Please enter as specified")


## Age at first admission
def age_first_adm(
    list_of_patient_object: list[Patient],
    list_of_lab_object: list[Lab],
    patient_id: str,
) -> int:

    """
    Calculate the age at first admission of the given patient.

    The computational complexity is N*N + N → N^2.
    """

    for lab_object in list_of_lab_object:  # N times
        if lab_object.pat_id == patient_id and int(lab_object.adm_id) == 1:  # 0(1)
            age_first_lab = 0

            for patient_object in list_of_patient_object:  # N times
                if patient_object.pat_id == lab_object.pat_id:  # 0(1)
                    p_birth = datetime.strptime(
                        patient_object.DOB, "%Y-%m-%d %H:%M:%S.%f"
                    ).year
                    lab_yr = datetime.strptime(
                        lab_object.lab_date, "%Y-%m-%d %H:%M:%S.%f"
                    ).year
                    age_first_lab = lab_yr - p_birth
                    return age_first_lab

    raise ValueError("No lab record or no such patient id.")


if __name__ == "__main__":
    print("Enter your patient file name:")
    filename_patient = input()
    print("Enter your lab file name")
    filename_lab = input()

    parse_patient_data(filename_patient)
    parse_lab_data(filename_lab)

    list_patient = create_patient_class()
    list_lab = create_lab_class()
    # a = Patient(cur, "A50BE9B4-8A0B-4169-B894-F7BD86D7D90B")
    # print(a.age, a.gender, a.race, a.DOB)
    b = Lab(cur, "1A8791E3-A61C-455A-8DEE-763EB90C9B2C", 1, "CBC: MCH")
    print(b.pat_id,b.lab_value, b.units, b.lab_date)

    print("Enter the age to calculate:")
    age = float(input())

    num = num_older_than(age, list_patient)
    print(num)

    print('To get the IDs of sick patient, enter the "lab test name" first:')
    lab = input()
    print('Enter either ">" or "<" for above or below:')
    gt_lt = input()
    print("Enter critical lab value:")
    value = float(input())

    result_sick_patient = sick_patients(lab, gt_lt, value, list_lab)
    print(result_sick_patient)

    print("Enter the patient ID for age at first admission")
    patient_id = input()
    result_age_first_adm = age_first_adm(list_patient, list_lab, patient_id)
    print(f"The age of patient at first admission is:", result_age_first_adm)

    conn.close()
    os.remove("EHR.db")
