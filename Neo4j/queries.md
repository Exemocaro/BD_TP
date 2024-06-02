1. Pedir o histórico de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a obter o histórico desse mesmo paciente.

> MATCH (p:Patient {IDPATIENT: id_patient})-[:BELONGS_TO]-(h:History)
RETURN p, h

2. Ver todas as consultas/hospitalizações/análises de um funcionário

Onde está o employee_id, substituir por um número inteiro de forma a obter os episódios do funcionário.

> MATCH (s:Staff {EMP_ID: employee_id})-[:PERFORMED_BY]-(event)
RETURN s, event

3. Verificar todos os médicos de um certo departamento

Onde está o id_department, substituir por um número inteiro de forma a obter os médicos que trabalham nesse departamento.

> MATCH (d:Department {IDDEPARTMENT: id_department})<-[:WORKS_IN]-(s:Staff)
RETURN d, s

4. Ver todos os medicamentos que o hospital já prescreveu

> MATCH (p:Prescription)
RETURN p.MEDICINE_M_NAME AS MedicineName, COUNT(p) AS TimesPrescribed
ORDER BY TimesPrescribed DESC

5. Consultar as contas de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a obter as contas de um paciente.

> MATCH (p:Patient {IDPATIENT: id_patient})<-[:WAS_FREQUENTED_BY]-(e:Episode)-[:HAS_BILL]-(b:Bill)
RETURN p, e, b

6. Procurar o conjunto de episódios de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a obter os episódios de um paciente.

> MATCH (p:Patient {IDPATIENT: id_patient})<-[:WAS_FREQUENTED_BY]-(e:Episode)
RETURN p, e

7. Registar um novo episódio   *(adicionar consulta/hospitalização/análise?)

Onde está o id_patient, substituir por um número inteiro. \
Onde está o new_episode_id, substituir por um número inteiro de modo a criar um novo episódio.

> CREATE (e:Episode {IDEPISODE: new_episode_id})
    WITH e
    MATCH (p:Patient {IDPATIENT: id_patient})
    CREATE (e)-[:WAS_FREQUENTED_BY]->(p)
    RETURN p, e

8. Registar um novo paciente   *(adicionar contacto de emergência?)

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


9. Verificar todos os quartos de hospital onde um(a) enfermeira/o já operou

Onde está o id_nurse, substituir por um número inteiro de forma a obter os quartos de hospital onde um enfermeiro operou.

> MATCH (n:Staff {QUALIFICATION: 'NURSE', EMP_ID: $nurseId})-[:PERFORMED_BY]-(h:Hospitalization)-[:IS_IN_EPISODE]-(e:Episode)
RETURN DISTINCT h.ROOM_ROOM_TYPE, h.ROOM_ROOM_COST


10. Atualizar o contacto de emergência de um paciente

Onde está o id_patient, substituir por um número inteiro de forma a atualizar o contacto de emergência do paciente. \
Onde está o contact_name, phone e relation, substituir por strings de modo a atualizar os campos do contacto de emergência.

> MATCH (p:Patient {IDPATIENT: id_patient})<-[:IS_CONTACT]-(e:EmergencyContact)
SET e.CONTACT_NAME = contact_name, e.PHONE = phone, e.RELATION = relation
RETURN p, e
