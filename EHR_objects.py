# EHR part3
from datetime import date, datetime


class Patient:
    """
    Patient class: each patient class object represents an unique patient,
    and contains information such as patient ID, gender, date of birth, and race.
    """

    def __init__(self, cursor, pat_id: str):
        """Initialize."""
        self.cursor = cursor
        self.pat_id = pat_id

    @property
    def gender(self):
        _gender = self.cursor.execute(
            f"SELECT PatientGender FROM patient WHERE PatientID = '{self.pat_id}'"
        ).fetchone()  # Fetch gender info
        return _gender[0]

    @property
    def race(self):
        _race = self.cursor.execute(
            f"SELECT PatientRace FROM patient WHERE PatientID = '{self.pat_id}'"
        ).fetchone()  # Fetch Race info
        return _race[0]

    @property
    def DOB(self):
        _DOB = self.cursor.execute(
            f"SELECT PatientDateOfBirth FROM patient WHERE PatientID = '{self.pat_id}';"
        ).fetchone()  # Fetch DOB info
        return _DOB[0]

    @property
    def age(self):
        """Function to calculate age property."""
        p_birth = datetime.strptime(self.DOB, "%Y-%m-%d %H:%M:%S.%f").year
        return datetime.now().year - p_birth


class Lab:
    """
    Lab class: each lab class object represents a lab diagnosis result of a patient,
    and contains information such as patient ID, date of diagnosis, and the name, value and units of the lab examination.
    """
    def __init__(
        self,
        cursor,
        pat_id: str,
        adm_id: str,
        lab_name: str,
    ):
        self.cursor = cursor
        self.pat_id = pat_id
        self.adm_id = adm_id
        self.lab_name = lab_name

    @property
    def lab_value(self):
        _lab_value = self.cursor.execute(
            f"SELECT LabValue FROM lab WHERE PatientID = '{self.pat_id}' \
                AND AdmissionID = '{self.adm_id}' AND LabName = '{self.lab_name}'"
        ).fetchone()
        return _lab_value[0]

    @property
    def units(self):
        _units = self.cursor.execute(
            f"SELECT LabUnits FROM lab WHERE PatientID = '{self.pat_id}' \
                AND AdmissionID = '{self.adm_id}' AND LabName = '{self.lab_name}'"
        ).fetchone()
        return _units[0]

    @property
    def lab_date(self):
        _lab_date = self.cursor.execute(
            f"SELECT lab.LabDateTime FROM lab WHERE PatientID = '{self.pat_id}' \
                AND AdmissionID = '{self.adm_id}' AND LabName = '{self.lab_name}'"
        ).fetchone()
        return _lab_date[0]
