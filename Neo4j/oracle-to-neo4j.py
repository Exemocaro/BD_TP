import json
import oracledb
from py2neo import Graph, Node, Relationship

def create_node(label, properties):
    node = Node(label, **properties)
    graph.create(node)
    return node
    
def create_relationship(start_node, end_node, relationship, attributes):
    if start_node is None:
        raise ValueError("start_node is None")
    if end_node is None:
        raise ValueError("end_node is None")
    relationship = Relationship(start_node, relationship, end_node, **attributes)
    graph.create(relationship)


def delete_neo4j_data():
    delete_query = "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r"
    graph.run(delete_query)


def load_patients(cursor):
    patients_sql = cursor.execute("SELECT * FROM patient").fetchall()
    for patient in patients_sql:
        new_patient = {}
        
        new_patient["IDPATIENT"] = patient[0]
        new_patient["PATIENT_FNAME"] = patient[1]
        new_patient["PATIENT_LNAME"] = patient[2]
        new_patient["BLOOD_TYPE"] = patient[3]
        new_patient["PHONE"] = patient[4]
        new_patient["EMAIL"] = patient[5]
        new_patient["GENDER"] = patient[6]
        new_patient["POLICY_NUMBER"] = patient[7]
        new_patient["BIRTHDAY"] = patient[8].strftime("%Y-%m-%d %H:%M:%S")
        
        
        histories_sql = cursor.execute("SELECT * FROM medical_history WHERE idpatient = " + str(patient[0])).fetchall()
        medical_histories = []
        for history in histories_sql:
            # print(f"Patient {patient[0]} has history {history}")
            new_history = {}
            new_history["RECORD_ID"] = history[0]
            new_history["CONDITION"] = history[1]
            new_history["RECORD_DATE"] = history[2].strftime("%Y-%m-%d")
            medical_histories.append(new_history)
        
        new_patient["MEDICAL_HISTORY"] = json.dumps(medical_histories)
        
        contacts_sql = cursor.execute("SELECT * FROM emergency_contact WHERE idpatient = " + str(patient[0])).fetchall()
        emergency_contacts = []
        for contact in contacts_sql:
            # print(f"Patient {patient[0]} has contact {contact}")
            new_contact = {}
            new_contact["CONTACT_NAME"] = contact[0]
            new_contact["CONTACT_PHONE"] = contact[1]
            new_contact["RELATION"] = contact[2]
            emergency_contacts.append(new_contact)
        
        new_patient["EMERGENCY_CONTACTS"] = json.dumps(emergency_contacts)
        
        # print(new_patient)
        create_node("Patient", new_patient)

def load_insurances(cursor):
    insurances_sql = cursor.execute("SELECT * FROM insurance").fetchall()
    for insurance in insurances_sql:
        new_insurance = {}
        
        new_insurance["POLICY_NUMBER"] = insurance[0]
        new_insurance["PROVIDER"] = insurance[1]
        new_insurance["INSURANCE_PLAN"] = insurance[2]
        new_insurance["CO_PAY"] = insurance[3]
        new_insurance["COVERAGE"] = insurance[4]
        new_insurance["MATERNITY"] = insurance[5]
        new_insurance["DENTAL"] = insurance[6]
        new_insurance["OPTICAL"] = insurance[7]
        
        # print(new_insurance)
        insurance_node = create_node("Insurance", new_insurance)
        
        patient_nodes = list(graph.nodes.match("Patient", POLICY_NUMBER=insurance[0]))
        for patient_node in patient_nodes:
            create_relationship(patient_node, insurance_node, "HAS_INSURANCE", {})
            
def load_departments(cursor):
    departments_sql = cursor.execute("SELECT * FROM department").fetchall()
    
    for department in departments_sql:
        new_department = {}
        new_department["IDDEPARTMENT"] = department[0]
        new_department["DEPARTMENT_HEAD"] = department[1]
        new_department["DEPARTMENT_NAME"] = department[2]
        
        create_node("Department", new_department)


def load_staff(cursor):
    staff_sql = cursor.execute("SELECT * FROM staff").fetchall()
    
    for staff in staff_sql:
        new_staff = {}
        new_staff["EMP_ID"] = staff[0]
        new_staff["EMP_FNAME"] = staff[1]
        new_staff["EMP_LNAME"] = staff[2]
        new_staff["DATE_JOINING"] = staff[3].strftime("%Y-%m-%d")
        if staff[4] is not None:
            new_staff["DATE_SEPARATION"] = staff[4].strftime("%Y-%m-%d")
        else:
            new_staff["DATE_SEPARATION"] = None
        new_staff["EMAIL"] = staff[5]
        new_staff["ADDRESS"] = staff[6]
        new_staff["SSN"] = staff[7]
        new_staff["IDDEPARTMENT"] = staff[8]
        
        nurse_sql = cursor.execute("SELECT * FROM nurse WHERE staff_emp_id = " + str(staff[0])).fetchall()
        if nurse_sql:
            new_staff["ROLE"] = "Nurse"
        doctor_sql = cursor.execute("SELECT * FROM doctor WHERE emp_id = " + str(staff[0])).fetchall()
        if doctor_sql:
            new_staff["QUALIFICATIONS"] = doctor_sql[0][1]
            new_staff["ROLE"] = "Doctor"
        technician_sql = cursor.execute("SELECT * FROM technician WHERE staff_emp_id = " + str(staff[0])).fetchall()
        if technician_sql:
            new_staff["ROLE"] = "Technician"
        staff_node = create_node("Staff", new_staff)
        
        department_node = graph.nodes.match("Department", IDDEPARTMENT=staff[8]).first()
        attributes = {"IS_ACTIVE_STATUS": staff[9]}
        create_relationship(staff_node, department_node, "BELONGS_TO", attributes)
        
def load_episodes(cursor):
    episodes_sql = cursor.execute("SELECT * FROM episode").fetchall()
    for episode in episodes_sql:
        new_episode = {}
        new_episode["IDEPISODE"] = episode[0]
        
        prescriptions_sql = cursor.execute("SELECT * FROM prescription WHERE idepisode = " + str(episode[0])).fetchall()
        prescriptions = []
        for prescription in prescriptions_sql:
            new_prescription = {}
            new_prescription["IDPRESCRIPTION"] = prescription[0]
            new_prescription["PRESCRIPTION_DATE"] = prescription[1].strftime("%Y-%m-%d")
            new_prescription["DOSAGE"] = prescription[2]
            
            medicines_sql = cursor.execute("SELECT * FROM medicine WHERE idmedicine = " + str(prescription[3])).fetchone()
            new_prescription["IDMEDICINE"] = medicines_sql[0]
            new_prescription["MEDICINE_NAME"] = medicines_sql[1]
            new_prescription["MEDICINE_QUANTITY"] = medicines_sql[2]
            new_prescription["MEDICINE_COST"] = medicines_sql[3]
            
            prescriptions.append(new_prescription)
            # print(new_prescription)
            
        new_episode["PRESCRIPTIONS"] = json.dumps(prescriptions)
        
        appointments_sql = cursor.execute("SELECT * FROM appointment WHERE idepisode = " + str(episode[0])).fetchall()
        for appointment in appointments_sql:
            new_episode["SCHEDULED_ON"] = appointment[0].strftime("%Y-%m-%d %H:%M:%S")
            new_episode["APPOINTMENT_DATETIME"] = f"{appointment[1].strftime('%Y-%m-%d')} {appointment[2]}"
            # print(new_episode)
            episode_node = create_node("Episode", new_episode)
            
            staff_node = graph.nodes.match("Staff", EMP_ID=appointment[3]).first()
            attributes = {"TYPE": "appointment"}
            create_relationship(episode_node, staff_node, "PERFORMED_BY", attributes)
        
        hospitalizations_sql = cursor.execute("SELECT * FROM hospitalization WHERE idepisode = " + str(episode[0])).fetchall()
        for hospitalization in hospitalizations_sql:
            new_episode["ADMISSION_DATE"] = hospitalization[0].strftime("%Y-%m-%d")
            if hospitalization[1] is not None:
                new_episode["DISCHARGE_DATE"] = hospitalization[1].strftime("%Y-%m-%d")
            else:
                new_episode["DISCHARGE_DATE"] = None
            new_episode["ROOM_NUMBER"] = hospitalization[2]
            
            rooms_sql = cursor.execute("SELECT * FROM room WHERE idroom = " + str(hospitalization[2])).fetchall()
            for room in rooms_sql:
                new_episode["ROOM_TYPE"] = room[1]
                new_episode["ROOM_COST"] = room[2]
            
            # print(new_episode)
            episode_node = create_node("Episode", new_episode)
            
            staff_node = graph.nodes.match("Staff", EMP_ID=hospitalization[4]).first()
            attributes = {"TYPE": "hospitalization"}
            create_relationship(episode_node, staff_node, "PERFORMED_BY", attributes)
            
        screenings_sql = cursor.execute("SELECT * FROM lab_screening WHERE episode_idepisode = " + str(episode[0])).fetchall()
        for screening in screenings_sql:
            new_episode["LAB_ID"] = screening[0]
            new_episode["TEST_COST"] = screening[1]
            new_episode["TEST_DATE"] = screening[2].strftime("%Y-%m-%d")
            
            # print(new_episode)
            episode_node = create_node("Episode", new_episode)
            
            staff_node = graph.nodes.match("Staff", EMP_ID=screening[3]).first()
            attributes = {"TYPE": "lab_screening"}
            create_relationship(episode_node, staff_node, "PERFORMED_BY", attributes)
            
        patient_nodes = list(graph.nodes.match("Patient", IDPATIENT=episode[1]))
        for patient_node in patient_nodes:
            create_relationship(episode_node, patient_node, "WAS_FREQUENTED_BY", {})
            


# Estabelecer conexão ao Neo4j
uri = "neo4j://localhost:7687"
auth = ("neo4j", "password")

graph = Graph(uri=uri, auth=auth)

# Estabelecer conexão ao OracleDB
username = "nosql"
password = "nosql2024"
dsn = "localhost/xe"

print("Deleting all data from Neo4j...")
delete_neo4j_data()

print("Establishing connection to Oracle...")

connection = oracledb.connect(user=username, password=password, dsn=dsn)

print("Connection established!\n")

print("Loading patient data...\n")
load_patients(connection.cursor())

print("Loading insurance data...\n")
load_insurances(connection.cursor())

print("Loading department data...\n")
load_departments(connection.cursor())

print("Loading staff data...\n")
load_staff(connection.cursor())

print("Loading episode data...\n")
load_episodes(connection.cursor())

print("Data loaded successfully! Closing connection...")
connection.close()
