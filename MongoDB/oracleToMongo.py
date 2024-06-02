import oracledb 
import pymongo

def load_Insurance(cursor, dbMongo):
    mDB_Insurance = []
    insurance = cursor.execute("select * from insurance").fetchall()
    for ins in insurance:
        newInsurance = {}
        newInsurance["_id"] = ins[0]
        newInsurance["PROVIDER"] = ins[1]
        newInsurance["INSURANCE_PLAN"] = ins[2]
        newInsurance["CO_PAY"] = ins[3]
        newInsurance["COVERAGE"] = ins[4]
        newInsurance["MATERNITY"] = ins[5]
        newInsurance["DENTAL"] = ins[6]
        newInsurance["OPTICAL"] = ins[7]
        mDB_Insurance.append(newInsurance)
    print(mDB_Insurance)
    dbMongo["Insurance"].insert_many(mDB_Insurance)

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
        newPatient["POLICY"] = patient[7]
        newPatient["BIRTHDAY"] = patient[8]
        medical_history = cursor.execute("select * from medical_history where \"IDPATIENT\" =" + str(patient[0])).fetchall()
        histories = []
        for history in medical_history:
            histories.append({"RECORD_ID": history[0], "CONDITION": history[1], "RECORD_DATE": history[2]})
        newPatient["MEDICAL_HISTORY"] = histories
        emergency_contact = cursor.execute("select * from emergency_contact where \"IDPATIENT\" =" + str(patient[0])).fetchall()
        patient_contacts = []   
        for contact in emergency_contact:
            patient_contacts.append({"CONTACT_NAME": contact[0], "RELATION": contact[2], "PHONE": contact[1]})
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

def load_Deparments(cursor, dbMongo):
    mDB_Deparments = []
    department = cursor.execute("select * from department").fetchall()
    for depart in department:
        newDepartment = {}
        newDepartment["_id"] = depart[0]
        newDepartment["DEPT_HEAD"] = depart[1]
        newDepartment["DEPT_NAME"] = depart[2]
        newDepartment["EMP_COUNT"] = depart[3]
        staff = cursor.execute("select * from staff where iddepartment = " + str(depart[0])).fetchall()
        staffList = []
        for person in staff:
            newPerson = {}
            newPerson["STAFF_ID"] = person[0]
            newPerson["FNAME"] = person[1]
            newPerson["LNAME"] = person[2]
            newPerson["DATE_JOINING"] = person[3]
            newPerson["DATE_SEPERATION"] = person[4]
            newPerson["EMAIL"] = person[5]
            newPerson["ADDRESS"] = person[6]
            newPerson["SSN"] = person[7]
            newPerson["IS_ACTIVE_STATUS"] = person[9]
            staff = cursor.execute("select * from nurse where \"STAFF_EMP_ID\" =" + str(person[0])).fetchone()
            if staff is not None:
                newPerson["QUALIFICATION"] = "NURSE"
            else:
                staff = cursor.execute("select * from doctor where \"EMP_ID\" =" + str(person[0])).fetchone()
                if staff is not None:
                    newPerson["QUALIFICATION"] = staff[1]
                else:
                    staff = cursor.execute("select * from technician where \"STAFF_EMP_ID\" =" + str(person[0])).fetchone()
                    if staff is not None:
                        newPerson["QUALIFICATION"] = "TECHNICIAN"
                    else:
                        Exception("Staff not found in any table")
            staffList.append(newPerson)
        newDepartment["STAFF"] = staffList
        mDB_Deparments.append(newDepartment)
    dbMongo["Department"].insert_many(mDB_Deparments)

def load_Appointments(cursor, dbMongo):
    mDB_Appointments = []
    appointments = cursor.execute("select * from appointment").fetchall()
    for appointment in appointments:
        newAppointment = {}
        newAppointment["_id"] = appointment[4]
        newAppointment["SCHEDULED_ON"] = appointment[0]
        newAppointment["APPOINTMENT_DATE"] = appointment[1]
        newAppointment["APPOINTMENT_TIME"] = appointment[2]
        newAppointment["RESPONSIBLE_STAFF"] = appointment[3]
        mDB_Appointments.append(newAppointment)
    dbMongo["Appointment"].insert_many(mDB_Appointments)

def load_Hospitalization(cursor, dbMongo):
    mDB_Hospitalizations = []
    hospitalizations = cursor.execute("select * from hospitalization").fetchall()
    for hospitalization in hospitalizations:
        newHospitalization = {}
        newHospitalization["_id"] = hospitalization[3]
        newHospitalization["ADMISSION_DATE"] = hospitalization[0]
        newHospitalization["DISCHARGE_DATE"] = hospitalization[1]
        room = cursor.execute("select * from room where \"IDROOM\" =" + str(hospitalization[2])).fetchone()
        newHospitalization["ROOM"] = {}
        newHospitalization["ROOM"]["ROOM_TYPE"] = room[1]
        newHospitalization["ROOM"]["ROOM_COST"] = room[2]
        newHospitalization["RESPONSIBLE_STAFF"] = hospitalization[4]
        mDB_Hospitalizations.append(newHospitalization)
    dbMongo["Hospitalization"].insert_many(mDB_Hospitalizations)

def load_Lab_Screening(cursor, dbMongo):
    mDB_Lab_Screenings = []
    lab_screenings = cursor.execute("select * from lab_screening").fetchall()
    for lab_screening in lab_screenings:
        newLab_Screening = {}
        newLab_Screening["_id"] = lab_screening[0]
        newLab_Screening["TEST_COST"] = lab_screening[1]
        newLab_Screening["TEST_DATE"] = lab_screening[2]
        newLab_Screening["RESPONSIBLE_STAFF"] = lab_screening[3]
        newLab_Screening["EPISODE"] = lab_screening[4]
        mDB_Lab_Screenings.append(newLab_Screening)
    dbMongo["Lab_Screening"].insert_many(mDB_Lab_Screenings)


connectionOracle = oracledb.connect(user="sys", password="1R2cl3!!!", dsn="localhost/xe", mode=oracledb.SYSDBA ) 
connectionMongo = pymongo.MongoClient("mongodb://localhost:27017/")
dbMongo = connectionMongo["Projeto"]
with connectionOracle.cursor() as oracleCursor:
    #load_Insurance(oracleCursor, dbMongo)
    load_Deparments(oracleCursor, dbMongo)
#    load_Patients(oracleCursor, dbMongo)
    #load_Episodes(oracleCursor, dbMongo)
    #load_Staff(oracleCursor, dbMongo)
    #load_Appointments(oracleCursor, dbMongo)
    #load_Hospitalization(oracleCursor, dbMongo)
    #load_Lab_Screening(oracleCursor, dbMongo)
connectionOracle.close()




