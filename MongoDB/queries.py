from pymongo import MongoClient
import datetime


# 1 pedir o historico de um paciente
def get_medical_history_by_id(patient_id, db):
    collection = db['Patient']  #Replace with your actual collection name

    # Perform the query
    result = collection.find_one({'_id': patient_id}, {'_id': 0, 'MEDICAL_HISTORY': 1})

    return result

# 2 ver todas as consultas/hospitalizações/análises de um funcionário
def get_staff_related_records(staff_id, db):

    collection = db['Department']  #Replace with your actual collection name

    pipeline = [
        {
            "$match": {
                "STAFF.STAFF_ID": staff_id
            }
        },
        {
            "$project": {
                "staff": {
                    "$filter" : {
                        "input": "$STAFF",
                        "as": "staff",
                        "cond": {  "$eq" : [ "$$staff.STAFF_ID", 14]}
                    }
                }
            }

        },
        {
            "$lookup": {
                "from": "Lab_Screening",  # The collection to join
                "localField": "staff.STAFF_ID",  # Field from the current collection
                "foreignField": "RESPONSIBLE_STAFF",  # Field from the Lab_Screening collection
                "as": "Lab_Screenings"  # Output array field
            }
        },
        {
            "$lookup": {
                "from": "Appointment",  # The collection to join
                "localField": "staff.STAFF_ID",  # Field from the current collection
                "foreignField": "RESPONSIBLE_STAFF",  # Field from the Appointment collection
                "as": "Appointments"  # Output array field
            }
        },
        {
            "$lookup": {
                "from": "Hospitalization",  # The collection to join
                "localField": "staff.STAFF_ID",  # Field from the current collection
                "foreignField": "RESPONSIBLE_STAFF",  # Field from the Appointment collection
                "as": "Hospitalization"  # Output array field
            }
        }
        ]

    results = list(collection.aggregate(pipeline))[0]
    
    return results['Lab_Screenings'] + results['Appointments'] + results['Hospitalization']



# 3 verificar todos os médicos de uma certa especialidade
def get_doctors_by_specialty(specialty, db):
    collection = db['Department']  #Replace with your actual collection name

    # Perform the query
    result = list(collection.find({'DEPT_NAME': specialty}))

    return result

# 4 ver todas as medicines que o hospital já prescreveu para um paciente
def get_all_prescribed_medicines(patient_id, db):
    collection = db['Episode']  #Replace with your actual collection name

    # Perform the query
    result = list(collection.find({'PATIENT_ID': patient_id}, {'_id': 0, 'PRESCRIPTIONS.MEDICINE': 1}))

    ret = []
    for res in result:
        if len(res['PRESCRIPTIONS']) > 0:
            ret += res['PRESCRIPTIONS']

    return ret

# 5 consultar as contas de um paciente
def get_patient_bills(patient_id, db):
    collection = db['Episode']  #Replace with your actual collection name

    #Perform the query
    result = list(collection.find({'PATIENT_ID': patient_id}, {'_id': 0, 'BILLS': 1}))

    ret = []
    for res in result:
        if len(res['BILLS']) > 0:
            ret += res['BILLS']

    return ret

# 6 Procurar o conjunto de episódios de um paciente
# TODO

# 7 registar um novo episodio (funçao)
def register_new_episode(patient_id, prescriptions, bills, db):
    collection = db['Episode']  # Replace with your actual collection name

    # Perform the query
    result = collection.insert_one({'PATIENT_ID': patient_id, 'PRESCIPTIONS': prescriptions, 'BILLS': bills})

    return result

# 8 registar um novo paciente
def register_new_patient(patient_name, blood_type, phone, email, gender, birthday, insurance_plan, emergency_contacts, db):
    collection = db['Patient']  # Replace with your actual collection name
    newPatient = {}
    nameSplit = patient_name.split(' ')
    newPatient["PATIENT_FNAME"] = nameSplit[0]
    newPatient["PATIENT_LNAME"] = nameSplit[-1]
    newPatient["BLOOD_TYPE"] = blood_type
    newPatient["PHONE"] = phone
    newPatient["EMAIL"] = email
    newPatient["GENDER"] = gender
    newPatient["POLICY"] = insurance_plan
    newPatient["BIRTHDAY"] = birthday
    newPatient['EMERGENCY_CONTACT'] = emergency_contacts
    newPatient['MEDICAL_HISTORY'] = []

    # Perform the query
    result = collection.insert_one(newPatient)

    return result

# 9 verificar todos os quartos de hospital onde um(a) enfermeira/o já operou
# TODO


# 10 update do contacto de emergencia do paciente
def update_emergency_contact(patient_id, new_contact_list, db):
    collection = db['Patient']  # Replace with your actual collection name

    collection.update_one({'_id': patient_id}, {"$set": {'EMERGENCY_CONTACT': new_contact_list}})

    return True



# Replace the URI string with your MongoDB deployment's connection string.
client = MongoClient("mongodb://localhost:27017/")
db = client['Projeto'] 
print(get_staff_related_records(14, db))
#print(get_medical_history_by_id(1, db))
#print(get_doctors_by_specialty('Cardiology', db))
#print(get_all_prescribed_medicines(1, db))
#print(get_patient_bills(3, db))
print(register_new_patient("John Doe", "O-", "111-222-3333", "doe@mail.com", "M", datetime.datetime(1990, 1, 1), "POL004", [], db))
#update_emergency_contact(1, [{'CONTACT_NAME' : "John Doe", "RELATION": "Father", "PHONE": "111-222-3333"}], db)