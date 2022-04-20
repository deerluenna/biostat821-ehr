# EHR part3
from datetime import date, datetime


class Patient:
    def __init__(self, patient_id: str, gender: str, DOB: str, race: str):
        self.patient_id = patient_id
        self.gender = gender
        self.DOB = DOB
        self.race = race

    @property
    def age(self):
        p_birth = datetime.strptime(self.DOB, "%Y-%m-%d %H:%M:%S.%f").year
        return datetime.now().year - p_birth


class Lab:
    def __init__(
        self,
        patient_id: str,
        adm_id: str,
        lab_name: str,
        lab_value: str,
        units: str,
        lab_date: str,
    ):
        self.patient_id = patient_id
        self.adm_id = adm_id
        self.lab_name = lab_name
        self.lab_value = lab_value
        self.units = units
        self.lab_date = lab_date
