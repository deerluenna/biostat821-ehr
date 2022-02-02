# --- Read and parse the data files --- #
from datetime import * 
from typing import Tuple


print('Enter your patient file name:')
filename_patient = input()
print('Enter your lab file name')
filename_lab = input()

"""I chose a list of lists for the following reasons:
A list can hold a mix of different kinds of data types, including multiple charatcteristics and test information of the same patient, even though they are not in the same format. Hence, a list of lists can.
"""

"""The computational complexity for the parser function is N*(1+1) + N*(1+1) → 2N → N, thus is N
"""

def parse_data(filename_patient : str, filename_lab : str) -> Tuple[list, list]:
  file_patient = open(filename_patient, 'r')
  file_lab = open(filename_lab, "r")
  text_patient = file_patient.readlines()
  text_lab = file_lab.readlines()
  # print(text_patient)
  # print(text_lab)
  
  list_of_list_patient = []
  list_of_list_lab = []

  for line_patient in text_patient: # N times
    line_patient = line_patient.strip().split('\t') # 0(1)
    list_of_list_patient.append(line_patient) # 0(1)
  file_patient.close()

  for line_lab in text_lab: # N times
    line_lab = line_lab.strip().split('\t') # 0(1)
    list_of_list_lab.append(line_lab) # 0(1)
  file_lab.close()

  return list_of_list_patient, list_of_list_lab



parsed_patient_data, parsed_lab_data = parse_data(filename_patient, filename_lab)


# --- Return the number of patients older than a given age (years) --- #
print('Enter the age to calculate:')
age = input()

def num_older_than(age, list_of_list_patient):
  age_col_idx = 0
  #print(list_of_list_patient[0])
  for j in range(len(list_of_list_patient[0])):
    if list_of_list_patient[0][j] == 'PatientDateOfBirth':
      #print(j)
      age_col_idx = j

  num = 0
  for i in range(1, len(list_of_list_patient)):
    p_birth = datetime.strptime(list_of_list_patient[i][age_col_idx], "%Y-%m-%d %H:%M:%S.%f").year
    #print(p_birth)
 
    if 2022-p_birth > float(age):
      num += 1
    
  print(f'Number of patients older than {age} is {num}')
  return num
  

num_older_than(age, parsed_patient_data)  


# --- Return a (unique) list of patients who have a given test with value above (">") or below ("<") a given level --- #

print('To get the IDs of sick patient, enter the "lab test name" first:')
lab = input()
print('Enter either ">" or "<" for above or below:')
gt_lt = input()
print('Enter critical lab value:')
value = input()


def sick_patients(lab, gt_lt, value, list_of_list_lab):
  lab_col_idx = 0
  for j in range(len(list_of_list_lab[0])):
    if list_of_list_lab[0][j] == 'LabName':
      #print(j)
      lab_col_idx = j
    if list_of_list_lab[0][j] == 'LabValue':
      value_col_idx = j

  ID_larger = []
  ID_smaller = []
  for i in range(1, len(list_of_list_lab)):
    if list_of_list_lab[i][lab_col_idx] == lab:
      if gt_lt == '>' and list_of_list_lab[i][value_col_idx] > value:
        ID_larger.append(list_of_list_lab[i][0])
      elif gt_lt == '<' and list_of_list_lab[i][value_col_idx] < value:
        ID_smaller.append(list_of_list_lab[i][0])

  if ID_larger != []: 
    print(ID_larger)
  if ID_smaller != []: 
    print(ID_smaller)
  
  if gt_lt == '>':
    return ID_larger
  else:
    return ID_smaller 
   
sick_patients(lab, gt_lt, value, parsed_lab_data)