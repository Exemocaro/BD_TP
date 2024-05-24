import oracledb 
import pymongo

connectionOracle = oracledb.connect(user="sys", password="1R2cl3!!!", dsn="localhost/xe", mode=oracledb.SYSDBA ) 
mDB_Patients = []
with connectionOracle.cursor() as oracleCursor:
    patients = oracleCursor.execute("select * from patient").fetchall()
    print(patients[0])
    for patient in patients:
        newPatient = {} 
        newPatient["_id"] = patient[0]
        newPatient["PATIENT_FNAME"] = patient[1]
        newPatient["PATIENT_LNAME"] = patient[2]
        newPatient["BLOOD_TYPE"] = patient[3]
        newPatient["PHONE"] = patient[4]
        newPatient["EMAIL"] = patient[5]
        newPatient["GENDER"] = patient[6]
        newPatient["BIRTHDAY"] = patient[8]
        patient_policy = oracleCursor.execute("select * from insurance where \"POLICY_NUMBER\" = \'" + str(patient[7]) + "\'").fetchone() 
        newPatient["PROVIDER"] = patient_policy[1]
        newPatient["INSURANCE_PLAN"] = patient_policy[2]
        newPatient["CO_PAY"] = patient_policy[3]
        newPatient["COVERAGE"] = patient_policy[4]
        newPatient["MATERNITY"] = patient_policy[5]
        newPatient["DENTAL"] = patient_policy[6]
        newPatient["OPTICAL"] = patient_policy[7]
        medical_history = oracleCursor.execute("select * from medical_history where \"IDPATIENT\" =" + str(patient[0])).fetchall()
        for history in medical_history:
            newPatient["RECORD_ID"] = history[0]
            newPatient["CONDITION"] = history[1]
            newPatient["RECORD_DATE"] = history[2]
            newPatient["IDPATIENT"] = history[3]
        emergency_contact = oracleCursor.execute("select * from emergency_contact where \"IDPATIENT\" =" + str(patient[0])).fetchall()
        for contact in emergency_contact:
            newPatient["CONTACT_NAME"] = contact[1]
            newPatient["RELATION"] = contact[3]
            newPatient["PHONE"] = contact[2]
        mDB_Patients.append(newPatient)
connectionOracle.close()
print(mDB_Patients)




