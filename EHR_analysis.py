# --- Read and parse the data files --- #
from datetime import *
from multiprocessing.sharedctypes import Value
from typing import Tuple

"""I chose a list of lists for my data structure for the following reason:
A list can hold a mix of different kinds of data types, including multiple 
charatcteristics and test information of the same patient, even though 
they are not in the same format. Hence, a list of lists can save patient data 
in the same format for different information, and we can use the same index 
to access the same type of data.
"""

"""The computational complexity for the parser function is N*(1+1) → 2N → N."""


def parse_data(filename: str) -> list[list[str]]:
    with open(filename, "r", encoding="utf-8-sig") as file:
        text = file.readlines()

    list_of_list = []

    for line in text:  # N times
        line = line.strip().split("\t")  # 0(1)
        list_of_list.append(line)  # 0(1)
    return list_of_list


# --- Return the number of patients older than a given age (years) --- #


def num_older_than(age: str, list_of_list_patient: list[list[str]]) -> int:

    age_col_idx = 0
    for j in range(len(list_of_list_patient[0])):
        if list_of_list_patient[0][j] == "PatientDateOfBirth":
            age_col_idx = j

    num = 0
    for i in range(1, len(list_of_list_patient)):
        p_birth = datetime.strptime(
            list_of_list_patient[i][age_col_idx], "%Y-%m-%d %H:%M:%S.%f"
        ).year

        if datetime.now().year - p_birth > float(age):
            num += 1

    return num


# --- Return a (unique) list of patients
# who have a given test with value above (">") or below ("<") a given level --- #


def sick_patients(
    lab: str, gt_lt: str, value: str, list_of_list_lab: list[list[str]]
) -> set[str]:
    lab_col_idx = 0
    value_col_idx = 0

    for j in range(len(list_of_list_lab[0])):
        if list_of_list_lab[0][j] == "LabName":
            lab_col_idx = j
        if list_of_list_lab[0][j] == "LabValue":
            value_col_idx = j

    id_larger = set()
    id_smaller = set()
    for i in range(1, len(list_of_list_lab)):
        if list_of_list_lab[i][lab_col_idx] == lab:
            if gt_lt == ">" and list_of_list_lab[i][value_col_idx] > value:
                id_larger.add(list_of_list_lab[i][0])
            elif gt_lt == "<" and list_of_list_lab[i][value_col_idx] < value:
                id_smaller.add(list_of_list_lab[i][0])

    if id_larger:
        return id_larger
    elif gt_lt == ">":
        return set([])

    if id_smaller:
        return id_smaller
    elif gt_lt == "<":
        return set([])


def age_first_adm(
    list_of_list_patient: list[list[str]],
    list_of_list_lab: list[list[str]],
    patient_id: str,
) -> int:
    labdate_col_idx = 0
    for j in range(len(list_of_list_lab[0])):
        if list_of_list_lab[0][j] == "LabDateTime":
            labdate_col_idx = j
            break

    for i in range(len(list_of_list_lab)):
        if list_of_list_lab[i][0] == patient_id and int(list_of_list_lab[i][1]) == 1:
            age_first_lab = 0
            # visited_id.append(list_of_list_lab[i][0])
            for k in range(1, len(list_of_list_patient)):
                if list_of_list_patient[k][0] == list_of_list_lab[i][0]:
                    p_birth = datetime.strptime(
                        list_of_list_patient[k][2], "%Y-%m-%d %H:%M:%S.%f"
                    ).year
                    lab_yr = datetime.strptime(
                        list_of_list_lab[i][labdate_col_idx], "%Y-%m-%d %H:%M:%S.%f"
                    ).year
                    age_first_lab = lab_yr - p_birth
                    return age_first_lab

    raise ValueError("No lab record or no such patient id.")


if __name__ == "__main__":
    print("Enter your patient file name:")
    filename_patient = input()
    print("Enter your lab file name")
    filename_lab = input()

    parsed_patient_data = parse_data(filename_patient)
    parsed_lab_data = parse_data(filename_lab)

    print("Enter the age to calculate:")
    age = input()

    num = num_older_than(age, parsed_patient_data)
    print(num)

    print('To get the IDs of sick patient, enter the "lab test name" first:')
    lab = input()
    print('Enter either ">" or "<" for above or below:')
    gt_lt = input()
    print("Enter critical lab value:")
    value = input()

    result_sick_patient = sick_patients(lab, gt_lt, value, parsed_lab_data)
    print(result_sick_patient)

    print("Enter the patient ID for age at first admission")
    patient_id = input()
    result_age_first_adm = age_first_adm(
        parsed_patient_data, parsed_lab_data, patient_id
    )
    print(result_age_first_adm)
