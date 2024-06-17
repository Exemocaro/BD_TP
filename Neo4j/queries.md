1. Pedir o histórico de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a obter o histórico desse mesmo paciente.

> MATCH (p:Patient) WHERE p.IDPATIENT = $id_patient RETURN p.MEDICAL_HISTORY;

> Tempo de execução: 45 ms

2. Ver todas as consultas/hospitalizações/análises de um funcionário

Onde está o employee_id, substituir por um número inteiro de forma a obter os episódios do funcionário.

> MATCH (s:Staff {EMP_ID: $employee_id})<-[PERFORMED_BY]-(e:Episode) RETURN s, e;

> Tempo de execução: 10 ms

3. Verificar todos os médicos de um certo departamento

Onde está o id_department, substituir por um número inteiro de forma a obter os médicos que trabalham nesse departamento.

> MATCH (d:Department {IDDEPARTMENT: $id_department})<-[:BELONGS_TO]-(s:Staff) RETURN d, s;

> Tempo de execução: 10 ms

4. Ver todos os medicamentos que o hospital já prescreveu

> MATCH (e:Episode) WITH e, apoc.convert.fromJsonMap(e.PRESCRIPTIONS) AS prescriptions 
UNWIND prescriptions AS prescription
WITH prescription.MEDICINE_NAME AS medicine, count(prescription.MEDICINE_NAME) AS prescription_count
RETURN medicine, prescription_count
ORDER BY prescription_count DESC;

> Tempo de execução: 51 ms

5. Consultar as contas de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a obter as contas de um paciente.

> MATCH (p:Patient {IDPATIENT: $id_patient})<-[WAS_FREQUENTED_BY]-(e:Episode) RETURN e.BILL;

> Tempo de execução: 9 ms

6. Procurar o conjunto de episódios de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a obter os episódios de um paciente.

> MATCH (p:Patient {IDPATIENT: 1})<-[:WAS_FREQUENTED_BY]-(e:Episode) RETURN p, e;

> Tempo de execução: 30 ms

7. Registar um novo episódio - consulta

Onde está o new_episode_id, substituir por um número inteiro de modo a criar um novo episódio. \
Onde está o id_patient, substituir por um número inteiro. \
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

> Tempo de execução: 39 ms

9. Verificar todos os quartos de hospital onde um(a) enfermeira/o já operou

Onde está o id_nurse, substituir por um número inteiro de forma a obter os quartos de hospital onde um enfermeiro operou.

> MATCH (n:Staff {ROLE: "Nurse", EMP_ID: 20})<-[:PERFORMED_BY]-(e:Episode) RETURN DISTINCT e.IDEPISODE, e.ROOM_TYPE, e.ROOM_COST;

> Tempo de execução: 10 ms

10. Atualizar o contacto de emergência de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a atualizar o contacto de emergência do paciente. \
Onde está o contact_name, phone e relation, substituir por strings de modo a atualizar os campos do contacto de emergência.

> MATCH (p:Patient {IDPATIENT: id_patient})<-[:IS_CONTACT]-(e:EmergencyContact)
SET e.CONTACT_NAME = contact_name, e.PHONE = phone, e.RELATION = relation
RETURN p, e

> Tempo de execução: 83 ms

Os tempos de execução das queries foram obtidos ao adicionar a palavra 'PROFILE' antes da query Cypher em si, permitindo visualizar o número de acessos à base de dados e tempo de execução.