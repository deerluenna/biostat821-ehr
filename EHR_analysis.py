# --- Read and parse the data files --- #
from datetime import date, datetime
from typing import Tuple, Dict
from EHR_objects import Patient, Lab


## Data Parsing
def parse_data(
    filename_patient: str, filename_lab: str
) -> Tuple[list[Patient], list[Lab]]:
    """
    Parse the patient and lab files, return a list of patient class and a list of lab class,
    with corresponding patient and lab information.
    Input: 1. String of patient filename 2. String of lab filename
    Output: 1. List of patient information 2. List of lab information

    The computational complexity for the parser function is
    N*(1+1) + N*(1+1) + N*1 + N*1 + N + N → 8N → N.
    """

    # Open and parse patient file
    with open(filename_patient, "r", encoding="utf-8-sig") as file:
        text = file.readlines()
    patient_list_of_list = []
    for line in text:  # N times
        col_in_line = line.strip().split("\t")  # 0(1)
        patient_list_of_list.append(col_in_line)  # 0(1)

    # Open and parse lab file
    with open(filename_lab, "r", encoding="utf-8-sig") as file:
        text = file.readlines()
    lab_list_of_list = []
    for line in text:  # N times
        col_in_line = line.strip().split("\t")  # 0(1)
        lab_list_of_list.append(col_in_line)  # 0(1)

    # Dictionary with patient column index
    patient_col_idx = {}
    for idx, key in enumerate(patient_list_of_list[0]):  # N times
        patient_col_idx[key] = idx  # 0(1)

    # Dictionary with lab column index
    lab_col_idx = {}
    for idx, key in enumerate(lab_list_of_list[0]):  # N times
        lab_col_idx[key] = idx  # 0(1)

    # Loop through each row to get patient info
    patient_list = []
    for i in range(1, len(patient_list_of_list)):  # N times
        patient = Patient(
            patient_id=patient_list_of_list[i][patient_col_idx["PatientID"]],
            gender=patient_list_of_list[i][patient_col_idx["PatientGender"]],
            DOB=patient_list_of_list[i][patient_col_idx["PatientDateOfBirth"]],
            race=patient_list_of_list[i][patient_col_idx["PatientRace"]],
        )  # 0(1)
        patient_list.append(patient)

    # Loop through each row to get lab info
    lab_list = []
    for i in range(1, len(lab_list_of_list)):  # N times
        lab = Lab(
            patient_id=lab_list_of_list[i][lab_col_idx["PatientID"]],
            adm_id=lab_list_of_list[i][lab_col_idx["AdmissionID"]],
            lab_name=lab_list_of_list[i][lab_col_idx["LabName"]],
            lab_value=lab_list_of_list[i][lab_col_idx["LabValue"]],
            units=lab_list_of_list[i][lab_col_idx["LabUnits"]],
            lab_date=lab_list_of_list[i][lab_col_idx["LabDateTime"]],
        )  # 0(1)
        lab_list.append(lab)
    return patient_list, lab_list


## Number of patients older
def num_older_than(age: float, list_of_patient: list[Patient]) -> int:
    """
    Calculate the number of patients whose age are older than a certain entered age.
    Input: 1. Float of age 2. List of patient objects
    Output: Integer of number of patients

    The computational complexity for the parser function is
    N*(1+1) → 2N → N.
    """

    num = 0
    for i in range(0, len(list_of_patient)):  # N times
        p_birth = datetime.strptime(list_of_patient[i].DOB, "%Y-%m-%d %H:%M:%S.%f").year

        if datetime.now().year - p_birth > age:  # 0(1)
            num += 1

    return num


## Sick patient IDs
def sick_patients(
    lab: str, gt_lt: str, value: float, list_of_lab: list[Lab]
) -> set[str]:
    """
    Find unique patient IDs with a lab value greater or less than
    the given value of the specified lab type.

    The computational complexity is 1*N → N.
    """

    id_larger = set()
    id_smaller = set()

    if (gt_lt != ">") & (gt_lt != "<"):  # 0(1)
        raise ValueError("Operator input should be either '>' or '<'")
    elif gt_lt == ">":
        for i in range(1, len(list_of_lab)):
            if (
                lab == list_of_lab[i].lab_name
                and float(list_of_lab[i].lab_value) > value
            ):  # 0(1)
                id_larger.add(list_of_lab[i].patient_id)
    elif gt_lt == "<":
        for i in range(1, len(list_of_lab)):  # N times
            if (
                lab == list_of_lab[i].lab_name
                and float(list_of_lab[i].lab_value) < value
            ):  # 0(1)
                id_smaller.add(list_of_lab[i].patient_id)

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
    list_of_patient: list[Patient],
    list_of_lab: list[Lab],
    patient_id: str,
) -> int:

    """
    Calculate the age at first admission of the given patient.

    The computational complexity is N*N + N → N^2.
    """

    for i in range(len(list_of_lab)):  # N times
        if (
            list_of_lab[i].patient_id == patient_id and int(list_of_lab[i].adm_id) == 1
        ):  # 0(1)
            age_first_lab = 0

            for k in range(1, len(list_of_patient)):  # N times
                if list_of_patient[k].patient_id == list_of_lab[i].patient_id:  # 0(1)
                    p_birth = datetime.strptime(
                        list_of_patient[k].DOB, "%Y-%m-%d %H:%M:%S.%f"
                    ).year
                    lab_yr = datetime.strptime(
                        list_of_lab[i].lab_date, "%Y-%m-%d %H:%M:%S.%f"
                    ).year
                    age_first_lab = lab_yr - p_birth
                    return age_first_lab

    raise ValueError("No lab record or no such patient id.")


if __name__ == "__main__":
    print("Enter your patient file name:")
    filename_patient = input()
    print("Enter your lab file name")
    filename_lab = input()

    parsed_patient_data, parsed_lab_data = parse_data(filename_patient, filename_lab)

    print("Enter the age to calculate:")
    age = float(input())

    num = num_older_than(age, parsed_patient_data)
    print(num)

    print('To get the IDs of sick patient, enter the "lab test name" first:')
    lab = input()
    print('Enter either ">" or "<" for above or below:')
    gt_lt = input()
    print("Enter critical lab value:")
    value = float(input())

    result_sick_patient = sick_patients(lab, gt_lt, value, parsed_lab_data)
    print(result_sick_patient)

    print("Enter the patient ID for age at first admission")
    patient_id = input()
    result_age_first_adm = age_first_adm(
        parsed_patient_data, parsed_lab_data, patient_id
    )
    print(f"The age of patient at first admission is:", result_age_first_adm)

    # a = create_patient_class(parsed_patient_data)
    # print(a[0].patient_id, a[0].gender, a[0].DOB, a[0].age)
    # b = create_lab_class(parsed_lab_data)
    # print(b[0].patient_id, b[0].lab, b[0].value, b[0].units, b[0].lab_date)
