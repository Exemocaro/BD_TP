import oracledb 
import pymongo


def load_Patients(cursor, dbMongo):
    mDB_Patients = []
    patients = cursor.execute("select * from patient").fetchall()
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
        patient_policy = cursor.execute("select * from insurance where \"POLICY_NUMBER\" = \'" + str(patient[7]) + "\'").fetchone() 
        newPatient["PROVIDER"] = patient_policy[1]
        newPatient["INSURANCE_PLAN"] = patient_policy[2]
        newPatient["CO_PAY"] = patient_policy[3]
        newPatient["COVERAGE"] = patient_policy[4]
        newPatient["MATERNITY"] = patient_policy[5]
        newPatient["DENTAL"] = patient_policy[6]
        newPatient["OPTICAL"] = patient_policy[7]
        medical_history = cursor.execute("select * from medical_history where \"IDPATIENT\" =" + str(patient[0])).fetchall()
        histories = []
        for history in medical_history:
            histories.append({"RECORD_ID": history[0], "CONDITION": history[1], "RECORD_DATE": history[2]})
        newPatient["MEDICAL_HISTORY"] = histories
        emergency_contact = cursor.execute("select * from emergency_contact where \"IDPATIENT\" =" + str(patient[0])).fetchall()
        patient_contacts = []   
        for contact in emergency_contact:
            patient_contacts.append({"CONTACT_NAME": contact[1], "RELATION": contact[3], "PHONE": contact[2]})
        newPatient["EMERGENCY_CONTACT"] = patient_contacts
        mDB_Patients.append(newPatient)
    dbMongo["Patient"].insert_many(mDB_Patients)

def load_Episodes(cursor, dbMongo):
    mDB_Episodes = []
    episodes = cursor.execute("select * from episode").fetchall()
    for episode in episodes:
        newEpisode = {} 
        newEpisode["_id"] = episode[0]
        newEpisode["PATIENT_ID"] = episode[1]
        episode_prescription = cursor.execute("select * from prescription where \"IDEPISODE\" =" + str(episode[0])).fetchall()
        prescriptions = []
        for prescription in episode_prescription:
            pres = {}
            pres["IDPRESCRIPTION"] = prescription[0]
            pres["PRESCRIPTION_DATE"] = prescription[1]
            pres["DOSAGE"] = prescription[2]
            medication = cursor.execute("select * from medicine where \"IDMEDICINE\" =" + str(prescription[3])).fetchone()
            mDB_Medicine = {}
            mDB_Medicine["M_NAME"] = medication[1]
            mDB_Medicine["M_QUANTITY"] = medication[2]
            mDB_Medicine["M_COST"] = medication[3]
            pres["MEDICINE"] = mDB_Medicine
            prescriptions.append(pres)
        newEpisode["PRESCRIPTIONS"] = prescriptions
        bills = cursor.execute("select * from bill where \"IDEPISODE\" =" + str(episode[0])).fetchall()
        newEpisode["BILLS"] = []
        for bill in bills:
            newBill = {}
            newBill["ROOM_COST"] = bill[1]
            newBill["TEST_COST"] = bill[2]
            newBill["OTHER_CHARGES"] = bill[3]
            newBill["TOTAL"] = bill[4]
            newBill["REGISTERED_AT"] = bill[6]
            newBill["PAYMENT_STATUS"] = bill[7]
            newEpisode["BILLS"].append(newBill)
        mDB_Episodes.append(newEpisode)
    dbMongo["Episode"].insert_many(mDB_Episodes)

connectionOracle = oracledb.connect(user="sys", password="1R2cl3!!!", dsn="localhost/xe", mode=oracledb.SYSDBA ) 
connectionMongo = pymongo.MongoClient("mongodb://localhost:27017/")
dbMongo = connectionMongo["Projeto"]
with connectionOracle.cursor() as oracleCursor:
    #load_Patients(oracleCursor, dbMongo)
    load_Episodes(oracleCursor, dbMongo)
connectionOracle.close()




