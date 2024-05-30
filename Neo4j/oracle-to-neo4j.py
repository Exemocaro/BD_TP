import oracledb
from py2neo import Graph, Node, Relationship

# Creates a node in Neo4j
def create_node(label, properties):
    node = Node(label, **properties)
    graph.create(node)
    return node

# Creates a relationship between two nodes in Neo4j
def create_relationship(start_node, end_node, relationship):
    if start_node is None:
        raise ValueError("start_node is None")
    if end_node is None:
        raise ValueError("end_node is None")
    relationship = Relationship(start_node, relationship, end_node)
    graph.create(relationship)

def load_patients(cursor):
    patients = cursor.execute("select * from patient").fetchall()
    for patient in patients:
        new_patient = { }

        # Create a node for the patient
        new_patient["IDPATIENT"] = patient[0]
        new_patient["PATIENT_FNAME"] = patient[1]
        new_patient["PATIENT_LNAME"] = patient[2]
        new_patient["BLOOD_TYPE"] = patient[3]
        new_patient["PHONE"] = patient[4]
        new_patient["EMAIL"] = patient[5]
        new_patient["GENDER"] = patient[6]
        new_patient["POLICY_NUMBER"] = patient[7]
        new_patient["BIRTHDAY"] = patient[8]

        patient_policy = cursor.execute("select * from insurance where \"POLICY_NUMBER\" = \'" + str(patient[7]) + "\'").fetchone()
        new_patient["PROVIDER"] = patient_policy[1]
        new_patient["INSURANCE_PLAN"] = patient_policy[2]
        new_patient["CO_PAY"] = patient_policy[3]
        new_patient["COVERAGE"] = patient_policy[4]
        new_patient["MATERNITY"] = patient_policy[5]
        new_patient["DENTAL"] = patient_policy[6]
        new_patient["OPTICAL"] = patient_policy[7]

        #print(new_patient)
        create_node("Patient", new_patient)

def load_histories(cursor):
    medical_history = cursor.execute("select * from medical_history").fetchall()
    for history in medical_history:
        new_history = {}
        new_history["RECORD_ID"] = history[0]
        new_history["CONDITION"] = history[1]
        new_history["RECORD_DATE"] = history[2]
    
        #print(new_history)
        history_node = create_node("History", new_history)

        #new_history["IDPATIENT"] = episode[3]
        # create relationship between history and patient
        patient_node = graph.nodes.match("Patient", IDPATIENT=history[3]).first()
        create_relationship(history_node, patient_node, "BELONGS_TO")

def load_emergency_contacts(cursor):
    emergency_contacts = cursor.execute("select * from emergency_contact").fetchall()
    for contacts in emergency_contacts:
        new_contact = {}
        new_contact["CONTACT_NAME"] = contacts[0]
        new_contact["PHONE"] = contacts[1]
        new_contact["RELATION"] = contacts[2]

        #print(new_contact)
        contact_node = create_node("EmergencyContact", new_contact)

        #new_contact["IDPATIENT"] = episode[3]
        # create relationship between contact and patient
        patient_node = graph.nodes.match("Patient", IDPATIENT=contacts[3]).first()
        create_relationship(contact_node, patient_node, "IS_CONTACT")
        
def load_episodes(cursor):
    episodes = cursor.execute("select * from episode").fetchall()
    for episode in episodes:
        new_episode = { }
        new_episode["IDEPISODE"] = episode[0]

        #print(new_episode)
        episode_node = create_node("Episode", new_episode)
        
        # agora criamos as relações, têm sempre de vir depois do nó ser criado!

        #new_episode["PATIENT_IDPATIENT"] = episode[1]
        # create relationship between episode and patient
        patient_node = graph.nodes.match("Patient", IDPATIENT=episode[1]).first()
        create_relationship(episode_node, patient_node, "WAS_FREQUENTED_BY")

def load_prescriptions(cursor):
    prescriptions = cursor.execute("select * from prescription").fetchall()
    for prescription in prescriptions:
        new_prescription = {}
        new_prescription["IDPRESCRIPTION"] = prescription[0]
        new_prescription["PRESCRIPTION_DATE"] = prescription[1]
        new_prescription["DOSAGE"] = prescription[2]
        medication = cursor.execute("select * from medicine where \"IDMEDICINE\" =" + str(prescription[3])).fetchone()
        new_prescription["MEDICINE_M_NAME"] = medication[1]
        new_prescription["MEDICINE_M_QUANTITY"] = medication[2]
        new_prescription["MEDICINE_M_COST"] = medication[3]
        
        #print(new_prescription)
        prescription_node = create_node("Prescription", new_prescription)

        # create relationship between prescription and episode
        #new_prescription["IDEPISODE"] = prescription[4] # TODO RELATIONSHIP
        episode_node = graph.nodes.match("Episode", IDEPISODE=prescription[4]).first()
        create_relationship(episode_node, prescription_node, "HAS_PRESCRIPTION")

def load_bills(cursor):
    bills = cursor.execute("select * from bill").fetchall()
    for bill in bills:
        new_bill = {}
        new_bill["IDBILL"] = bill[0]
        new_bill["ROOM_COST"] = bill[1]
        new_bill["TEST_COST"] = bill[2]
        new_bill["OTHER_CHARGES"] = bill[3]
        new_bill["TOTAL"] = bill[4]
        new_bill["REGISTERED_AT"] = bill[6]
        new_bill["PAYMENT_STATUS"] = bill[7]
        
        #print(new_bill)
        bill_node = create_node("Bill", new_bill)

        # create relationship between bill and episode
        #new_bill["IDEPISODE"] = bill[6] # TODO RELATIONSHIP
        episode_node = graph.nodes.match("Episode", IDEPISODE=bill[5]).first()
        create_relationship(episode_node, bill_node, "HAS_BILL")

def load_departments(cursor):
    departments = cursor.execute("select * from department").fetchall()
    for department in departments:
        new_department = {}
        new_department["IDDEPARTMENT"] = department[0]
        new_department["DEPT_HEAD"] = department[1]
        new_department["DEPT_NAME"] = department[2]
        new_department["EMP_COUNT"] = department[3]

        #print(new_department)
        create_node("Department", new_department)

def load_staff(cursor):
    staff = cursor.execute("select * from staff").fetchall()
    for person in staff:
        new_person = { }
        new_person["EMP_ID"] = person[0]
        new_person["EMP_FNAME"] = person[1]
        new_person["EMP_LNAME"] = person[2]
        new_person["DATE_JOINING"] = person[3]
        new_person["DATE_SEPERATION"] = person[4]
        new_person["EMAIL"] = person[5]
        new_person["ADDRESS"] = person[6]
        new_person["SSN"] = person[7]
        new_person["IS_ACTIVE_STATUS"] = person[9]
        staff = cursor.execute("select * from nurse where \"STAFF_EMP_ID\" =" + str(person[0])).fetchone()
        if staff is not None:
            new_person["QUALIFICATION"] = "NURSE"
        else:
            staff = cursor.execute("select * from doctor where \"EMP_ID\" =" + str(person[0])).fetchone()
            if staff is not None:
                new_person["QUALIFICATION"] = staff[1]
            else:
                staff = cursor.execute("select * from technician where \"STAFF_EMP_ID\" =" + str(person[0])).fetchone()
                if staff is not None:
                    new_person["QUALIFICATION"] = "TECHNICIAN"
                else:
                    Exception("Staff not found in any table")
                    
        #print(new_person)
        person_node = create_node("Staff", new_person)
        
        # create relationship between staff and department
        #new_person["IDDEPARTMENT"] = person[8] # TODO RELATIONSHIP
        department_node = graph.nodes.match("Department", IDDEPARTMENT=person[8]).first()
        create_relationship(person_node, department_node, "WORKS_IN")
    
def load_appointments(cursor):
    appointments = cursor.execute("select * from appointment").fetchall()
    for appointment in appointments:
        new_appointment = {}
        new_appointment["SCHEDULED_ON"] = appointment[0]
        new_appointment["APPOINTMENT_DATE"] = appointment[1]
        new_appointment["APPOINTMENT_TIME"] = appointment[2]
        
        #print(new_appointment)
        appointment_node = create_node("Appointment", new_appointment)

        # create relationship between appointment and doctor
        #new_appointment["ID_DOCTOR"] = appointment[3] # TODO RELATIONSHIP
        doctor_node = graph.nodes.match("Staff", EMP_ID=appointment[3]).first()
        #create_relationship(doctor_node, appointment_node, "RESPONSIBLE_DOCTOR")
        create_relationship(appointment_node, doctor_node, "PERFORMED_BY")

        # create relationship between appointment and episode
        #new_appointment["ID_EPISODE"] = appointment[4] # TODO RELATIONSHIP
        episode_node = graph.nodes.match("Episode", IDEPISODE=appointment[4]).first()
        create_relationship(appointment_node, episode_node, "IS_IN_EPISODE")
        
def load_hospitalization(cursor):
    hospitalizations = cursor.execute("select * from hospitalization").fetchall()
    for hospitalization in hospitalizations:
        new_hospitalization = {}
        new_hospitalization["ADMISSION_DATE"] = hospitalization[0]
        new_hospitalization["DISCHARGE_DATE"] = hospitalization[1]
        room = cursor.execute("select * from room where \"IDROOM\" =" + str(hospitalization[2])).fetchone()
        new_hospitalization["ROOM_ROOM_TYPE"] = room[1]
        new_hospitalization["ROOM_ROOM_COST"] = room[2]
        
        #print(new_hospitalization)
        hospitalization_node = create_node("Hospitalization", new_hospitalization)
        
        # create relationship between hospitalization and nurse
        #new_hospitalization["RESPONSIBLE_NURSE"] = hospitalization[4] # TODO RELATIONSHIP
        nurse_node = graph.nodes.match("Staff", EMP_ID=hospitalization[4]).first()
        #create_relationship(nurse_node, hospitalization_node, "RESPONSIBLE_NURSE")
        create_relationship(hospitalization_node, nurse_node, "PERFORMED_BY")

        # create relationship between hospitalization and episode
        #new_hospitalization["ID_EPISODE"] = hospitalization[3] # TODO RELATIONSHIP
        episode_node = graph.nodes.match("Episode", IDEPISODE=hospitalization[3]).first()
        create_relationship(hospitalization_node, episode_node, "IS_IN_EPISODE")

def load_screenings(cursor):
    screenings = cursor.execute("select * from lab_screening").fetchall()
    for screening in screenings:
        new_screening = {}
        new_screening["LAB_ID"] = screening[0]
        new_screening["TEST_COST"] = screening[1]
        new_screening["TEST_DATE"] = screening[2]
        
        #print(new_screening)
        screening_node = create_node("Screening", new_screening)

        # create relationship between screening and technician
        #new_screening["IDTECHNICIAN"] = screening[3] # TODO RELATIONSHIP
        technician_node = graph.nodes.match("Staff", EMP_ID=screening[3]).first()
        create_relationship(screening_node, technician_node, "PERFORMED_BY")

        # create relationship between screening and episode
        #new_screening["EPISODE"] = screening[4] # TODO RELATIONSHIP
        episode_node = graph.nodes.match("Episode", IDEPISODE=screening[4]).first()
        create_relationship(screening_node, episode_node, "IS_IN_EPISODE")

# Estabelecer conexão ao Neo4j
uri = "neo4j://localhost:7687"
auth = ("neo4j", "password")

graph = Graph(uri=uri, auth=auth)

def delete_neo4j_data():
    delete_query = "MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r"
    graph.run(delete_query)

# Estabelecer conexão ao OracleDB
username = "nosql"
password = "nosql2024"
dsn = "localhost/xe"

print("Establishing connection to Oracle...")

connection = oracledb.connect(user=username, password=password, dsn=dsn)

print("Connection established!")

print("Deleting all data from Neo4j...")
delete_neo4j_data()

# load all data from OracleDB to Neo4j
print("Loading patients...")
load_patients(connection.cursor())
print("Loading medical histories...")
load_histories(connection.cursor())
print("Loading emergency contacts...")
load_emergency_contacts(connection.cursor())
print("Loading episodes...")
load_episodes(connection.cursor())
print("Loading prescriptions...")
load_prescriptions(connection.cursor())
print("Loading bills...")
load_bills(connection.cursor())
print("Loading departments...")
load_departments(connection.cursor())
print("Loading staff...")
load_staff(connection.cursor())
print("Loading appointments...")
load_appointments(connection.cursor())
print("Loading hospitalizations...")
load_hospitalization(connection.cursor())
print("Loading screenings...")
load_screenings(connection.cursor())

print("Data loaded successfully!")

connection.close()
