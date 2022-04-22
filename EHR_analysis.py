from EHR_objects import Patient, Lab
from datetime import datetime
from typing import List, Dict
import sqlite3
import os

conn = sqlite3.connect("EHR.db")
cur = conn.cursor()

## Data Parsing
def parse_patient_data(filename_patient: str):
    """
    Parse the patient data file, create a table with patient information in the database.
    Input: String of the patient filename
    Output: List of patient ids

    The computational complexity for the parser function is
    N*(1+1+1) → N.
    """
    # Create patient and lab tables in database
    cur.execute("DROP TABLE IF EXISTS patient")  # Drop the table if exists
    cur.execute(
        "CREATE TABLE IF NOT EXISTS patient(PatientID TEXT, PatientGender TEXT, PatientDateOfBirth TEXT, \
        PatientRace TEXT, PatientMaritalStatus TEXT, PatientLanguage TEXT, PatientPopulationPercentageBelowPoverty REAL)"
    )
    with open(filename_patient, "r", encoding="utf-8-sig") as patient_file:
        text = patient_file.readlines()
        line_info = []
        pat_id_list = []
        for line in text:  # N times
            col_in_line = line.strip().split("\t")  # 0(1)
            line_info.append(col_in_line)
            pat_id_list.append(col_in_line[0])  # 0(1) # Get the 0th col
        cur.executemany(
            "INSERT INTO patient VALUES(?, ?, ?, ?, ?, ?, ?)",
            line_info[1:],  # Don't want col name
        )

    conn.commit()
    return pat_id_list[1:]


def parse_lab_data(filename_lab: str):
    """
    Parse the lab data file, create a table with lab information in the database.
    Input: String of the lab filename
    Output: None

    The computational complexity for the parser function is
    N*(1+1+1) → N.
    """
    cur.execute(
        "CREATE TABLE IF NOT EXISTS lab(PatientID TEXT, AdmissionID INT, LabName TEXT, \
        LabValue REAL, LabUnits STR, LabDateTime STR)"
    )

    with open(filename_lab, "r", encoding="utf-8-sig") as lab_file:
        text = lab_file.readlines()
        line_info = []
        for line in text:  # N times
            col_in_line = line.strip().split("\t")  # 0(1)
            line_info.append(col_in_line)  # 0(1)
        cur.executemany(
            "INSERT INTO lab VALUES(?, ?, ?, ?, ?, ?)", line_info[1:]
        )  # 0(1)
    conn.commit()


def create_patient_class(pat_id_list: list[str]) -> list[Patient]:
    """
    Create a list of patient objects based on a list of patient ids.
    Input: List of patient ids
    Output: List of patient objects

    The computational complexity is N*(1+1) → N.
    """
    list_of_patient_object = []
    for pat_id in pat_id_list:  # N times
        patient_object = Patient(cursor=cur, pat_id=pat_id)  # 0(1)
        list_of_patient_object.append(patient_object)  # 0(1)
    return list_of_patient_object


## Number of patients older
def num_older_than(age: float, list_of_patient_object: list[Patient]) -> int:
    """
    Calculate the number of patients whose age are older than a certain entered age.
    Input: 1. Float of age 2. List of patient objects
    Output: Integer of number of patients

    The computational complexity is N*1 → N.
    """
    num = 0
    for patient_object in list_of_patient_object:  # N times
        if patient_object.age > age:  # 0(1)
            num += 1
    return num


## Sick patient IDs
def sick_patients(lab: str, gt_lt: str, value: float) -> set[str]:
    """
    Find unique patient IDs with a lab value greater or less than
    the given value of the specified lab type.

    Input: 1. String of lab name 2. String of operator 3.String of critical value
    Output: Set of string of sick patient IDs

    The computational complexity is 1 + N*1 + N*1 → 2N → N.
    """

    id_larger: set[str] = set()
    id_smaller: set[str] = set()

    if (gt_lt != ">") & (gt_lt != "<"):  # 0(1)
        raise ValueError("Operator input should be either '>' or '<'")

    elif gt_lt == ">":  # 0(1)
        id_larger = cur.execute(
            "SELECT distinct PatientID FROM lab WHERE (LabName = ?) AND (LabValue > ?)",
            (lab, value),
        ).fetchall()
        output_id_larger = set()
        for id in id_larger:  # N times
            output_id_larger.add(id[0])
    elif gt_lt == "<":  # 0(1)
        id_smaller = cur.execute(
            "SELECT distinct PatientID FROM lab WHERE (LabName = ?) AND (LabValue < ?)",
            (lab, value),
        ).fetchall()
        output_id_smaller = set()
        for id in id_smaller:  # N times
            output_id_smaller.add(id[0])

    if id_larger:  # 0(1)
        return output_id_larger
    elif gt_lt == ">":
        return set([])

    if id_smaller:  # 0(1)
        return output_id_smaller
    elif gt_lt == "<":
        return set([])

    raise ValueError("Please enter as specified")


## Age at first admission
def age_first_adm(
    patient_id: str,
) -> int:

    """
    Calculate the age at first admission of the given patient.

    Input: Patient ID
    Output: Integer of age at first admission

    The computational complexity is N*N + N → N^2.
    """

    p_birth = cur.execute(
        "SELECT PatientDateOfBirth FROM patient WHERE (PatientID = ?)", (patient_id,)
    ).fetchone()
    # p_birth = Patient(cur, patient_id).DOB
    adm_date = cur.execute(
        "SELECT MIN(LabDateTime) FROM lab WHERE (PatientID = ?)", (patient_id,)
    ).fetchone()
    birth_yr = datetime.strptime(p_birth[0], "%Y-%m-%d %H:%M:%S.%f").year
    lab_yr = datetime.strptime(adm_date[0], "%Y-%m-%d %H:%M:%S.%f").year
    age_first_lab = lab_yr - birth_yr

    if p_birth == [] or adm_date == []:
        raise ValueError("No lab record or no such patient id.")
    return age_first_lab


if __name__ == "__main__":
    print("Enter your patient file name:")
    filename_patient = input()
    print("Enter your lab file name")
    filename_lab = input()

    pat_id_list = parse_patient_data(filename_patient)
    parse_lab_data(filename_lab)
    list_of_patient_object = create_patient_class(pat_id_list)

    print("Enter the age to calculate:")
    age = float(input())

    num = num_older_than(age, list_of_patient_object)
    print(num)

    print('To get the IDs of sick patient, enter the "lab test name" first:')
    lab = input()
    print('Enter either ">" or "<" for above or below:')
    gt_lt = input()
    print("Enter critical lab value:")
    value = float(input())

    result_sick_patient = sick_patients(lab, gt_lt, value)
    print(result_sick_patient)

    print("Enter the patient ID for age at first admission")
    patient_id = input()
    result_age_first_adm = age_first_adm(patient_id)
    print(f"The age of patient at first admission is:", result_age_first_adm)

    conn.close()
    os.remove("EHR.db")
