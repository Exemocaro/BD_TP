1. Pedir o histórico de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a obter o histórico desse mesmo paciente.

> MATCH (p:Patient {IDPATIENT: id_patient})-[:BELONGS_TO]-(h:History)
RETURN p, h

> Tempo de execução: 16 ms

2. Ver todas as consultas/hospitalizações/análises de um funcionário

Onde está o employee_id, substituir por um número inteiro de forma a obter os episódios do funcionário.

> MATCH (s:Staff {EMP_ID: employee_id})-[:PERFORMED_BY]-(event)
RETURN s, event

> Tempo de execução: 55 ms

3. Verificar todos os médicos de um certo departamento

Onde está o id_department, substituir por um número inteiro de forma a obter os médicos que trabalham nesse departamento.

> MATCH (d:Department {IDDEPARTMENT: id_department})<-[:WORKS_IN]-(s:Staff)
RETURN d, s

> Tempo de execução: 67 ms

4. Ver todos os medicamentos que o hospital já prescreveu

> MATCH (p:Prescription)
RETURN p.MEDICINE_M_NAME AS MedicineName, COUNT(p) AS TimesPrescribed
ORDER BY TimesPrescribed DESC

> Tempo de execução: 51 ms

5. Consultar as contas de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a obter as contas de um paciente.

> MATCH (p:Patient {IDPATIENT: id_patient})<-[:WAS_FREQUENTED_BY]-(e:Episode)-[:HAS_BILL]-(b:Bill)
RETURN p, e, b

> Tempo de execução: 100 ms

6. Procurar o conjunto de episódios de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a obter os episódios de um paciente.

> MATCH (p:Patient {IDPATIENT: id_patient})<-[:WAS_FREQUENTED_BY]-(e:Episode)
RETURN p, e

> Tempo de execução: 67 ms

7. Registar um novo episódio

Onde está o id_patient, substituir por um número inteiro. \
Onde está o new_episode_id, substituir por um número inteiro de modo a criar um novo episódio. \
Onde está o admission_date, discharge_date, room_type, room_cost e nurse_id, substituir por strings e um float de modo a inserir os detalhes de uma hospitalização.

> CREATE (e:Episode {IDEPISODE: new_episode_id})
WITH e
MATCH (p:Patient {IDPATIENT: id_patient})
CREATE (e)-[:WAS_FREQUENTED_BY]->(p)
WITH e, p
CREATE (h:Hospitalization {ADMISSION_DATE: admission_date, DISCHARGE_DATE: discharge_date, ROOM_ROOM_TYPE: room_type, ROOM_ROOM_COST: room_cost})
CREATE (h)-[:IS_IN_EPISODE]->(e)
WITH e, p, h
MATCH (n:Staff {EMP_ID: nurse_id})
CREATE (h)-[:PERFORMED_BY]->(n)
RETURN p, e, h

> Tempo de execução: 498 ms

Onde está o scheduled_on, appointment_date, appointment_time e doctor_id, substituir por strings de modo a inserir os detalhes de uma consulta.

> CREATE (e:Episode {IDEPISODE: new_episode_id})
WITH e
MATCH (p:Patient {IDPATIENT: id_patient})
CREATE (e)-[:WAS_FREQUENTED_BY]->(p)
WITH e, p
CREATE (a:Appointment {SCHEDULED_ON: scheduled_on, APPOINTMENT_DATE: appointment_date, APPOINTMENT_TIME: appointment_time})
CREATE (a)-[:IS_IN_EPISODE]->(e)
WITH e, p, a
MATCH (n:Staff {EMP_ID: doctor_id})
CREATE (a)-[:PERFORMED_BY]->(n)
RETURN p, e, a

> Tempo de execução: 172 ms

Onde está o lab_id, test_cost, test_date e technician_id, substituir por inteiros, um float e uma string de modo a inserir os detalhes de uma análise.

> PROFILE 
CREATE (e:Episode {IDEPISODE: new_episode_id})
WITH e
MATCH (p:Patient {IDPATIENT: id_patient})
CREATE (e)-[:WAS_FREQUENTED_BY]->(p)
WITH e, p
CREATE (s:Screening {LAB_ID: lab_id, TEST_COST: test_cost, TEST_DATE: test_date})
CREATE (s)-[:IS_IN_EPISODE]->(e)
WITH e, p, s
MATCH (n:Staff {EMP_ID: technician_id})
CREATE (s)-[:PERFORMED_BY]->(n)
RETURN p, e, s

> Tempo de execução: 142 ms

8. Registar um novo paciente

Onde está o id_patient, patient_firstname, patient_lastname, blood_type, phone, email, gender, policy_number e birthday, substituir por strings ou inteiros de modo a introduzir os campos do novo paciente.

> CREATE (p:Patient {
    IDPATIENT: id_patient,
    PATIENT_FNAME: patient_firstname,
    PATIENT_LNAME: patient_lastname,
    BLOOD_TYPE: blood_type,
    PHONE: phone,
    EMAIL: email,
    GENDER: gender,
    POLICY_NUMBER: policy_number,
    BIRTHDAY: birthday
})
RETURN p

> Tempo de execução: 26 ms

9. Verificar todos os quartos de hospital onde um(a) enfermeira/o já operou

Onde está o id_nurse, substituir por um número inteiro de forma a obter os quartos de hospital onde um enfermeiro operou.

> MATCH (n:Staff {QUALIFICATION: 'NURSE', EMP_ID: id_nurse})-[:PERFORMED_BY]-(h:Hospitalization)-[:IS_IN_EPISODE]-(e:Episode)
RETURN DISTINCT h.ROOM_ROOM_TYPE, h.ROOM_ROOM_COST

> Tempo de execução: 97 ms

10. Atualizar o contacto de emergência de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a atualizar o contacto de emergência do paciente. \
Onde está o contact_name, phone e relation, substituir por strings de modo a atualizar os campos do contacto de emergência.

> MATCH (p:Patient {IDPATIENT: id_patient})<-[:IS_CONTACT]-(e:EmergencyContact)
SET e.CONTACT_NAME = contact_name, e.PHONE = phone, e.RELATION = relation
RETURN p, e

> Tempo de execução: 83 ms

Os tempos de execução das queries foram obtidos ao adicionar a palavra 'PROFILE' antes da query Cypher em si, permitindo visualizar o número de acessos à base de dados e tempo de execução.