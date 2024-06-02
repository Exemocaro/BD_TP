1. Pedir o histórico de um paciente

> SELECT p.*, mh.*
FROM patient p
JOIN MEDICAL_HISTORY mh ON p.idpatient = mh.idpatient
WHERE p.idpatient = :id_patient;

> Tempo de execução: 24 ms

2. Ver todas as consultas/hospitalizações/análises de um funcionário

> SELECT s.*, e.*
FROM staff s
JOIN hospitalization h ON s.emp_id = h.responsible_nurse
JOIN episode e ON h.idepisode = e.idepisode
WHERE s.emp_id = :employee_id;


> Tempo de execução: 29 ms

3. Verificar todos os médicos de um certo departamento

> SELECT d.*, s.*
FROM department d
JOIN staff s ON d.iddepartment = s.iddepartment
WHERE d.iddepartment = :id_department;

> Tempo de execução: 33 ms

4. Ver todos os medicamentos que o hospital já prescreveu

> SELECT m.m_name AS MedicineName, COUNT(p.idprescription) AS TimesPrescribed
FROM prescription p
JOIN medicine m ON p.idmedicine = m.idmedicine
GROUP BY m.m_name
ORDER BY TimesPrescribed DESC;

> Tempo de execução: 20 ms

5. Consultar as contas de um paciente

> SELECT p.*, e.*, b.*
FROM patient p
JOIN episode e ON p.idpatient = e.patient_idpatient
JOIN bill b ON e.idepisode = b.idepisode
WHERE p.idpatient = :id_patient;

> Tempo de execução: 10 ms

6. Procurar o conjunto de episódios de um paciente

> SELECT p.*, e.*
FROM patient p
JOIN episode e ON p.idpatient = e.patient_idpatient
WHERE p.idpatient = :id_patient;

> Tempo de execução: 1 ms

7. Registar um novo episódio

> INSERT INTO episode (idepisode, patient_idpatient) VALUES (:new_episode_id, :id_patient);
INSERT INTO hospitalization (admission_date, discharge_date, room_idroom, idepisode, responsible_nurse)
VALUES (:admission_date, :discharge_date, :room_type, :new_episode_id, :nurse_id);
SELECT p.*, e.*, h.*
FROM patient p
JOIN episode e ON p.idpatient = e.patient_idpatient
JOIN hospitalization h ON e.idepisode = h.idepisode
WHERE e.idepisode = :new_episode_id;

> Tempo de execução: 28 ms

> INSERT INTO episode (idepisode, patient_idpatient) VALUES (:new_episode_id, :id_patient);
INSERT INTO appointment (scheduled_on, appointment_date, appointment_time, iddoctor, idepisode)
VALUES (:scheduled_on, :appointment_date, :appointment_time, :doctor_id, :new_episode_id);
SELECT p.*, e.*, a.*
FROM patient p
JOIN episode e ON p.idpatient = e.patient_idpatient
JOIN appointment a ON e.idepisode = a.idepisode
WHERE e.idepisode = :new_episode_id;

> Tempo de execução: 10 ms

> INSERT INTO episode (idepisode, patient_idpatient) VALUES (:new_episode_id, :id_patient);
INSERT INTO lab_screening (lab_id, test_cost, test_date, idtechnician, episode_idepisode)
VALUES (:lab_id, :test_cost, :test_date, :technician_id, :new_episode_id);
SELECT p.*, e.*, s.*
FROM patient p
JOIN episode e ON p.idpatient = e.patient_idpatient
JOIN lab_screening s ON e.idepisode = s.episode_idepisode
WHERE e.idepisode = :new_episode_id;

> Tempo de execução: 9 ms

8. Registar um novo paciente

> INSERT INTO patient (idpatient, patient_fname, patient_lname, blood_type, phone, email, gender, policy_number, birthday)
VALUES (:id_patient, :patient_firstname, :patient_lastname, :blood_type, :phone, :email, :gender, :policy_number, :birthday);
SELECT *
FROM patient
WHERE idpatient = :id_patient;

> Tempo de execução: 16 ms

9. Verificar todos os quartos de hospital onde um(a) enfermeira/o já operou

> SELECT DISTINCT r.room_type, r.room_cost
FROM hospitalization h
JOIN nurse n ON h.responsible_nurse = n.staff_emp_id
JOIN room r ON h.room_idroom = r.idroom
WHERE n.staff_emp_id = :id_nurse;

> Tempo de execução: 33 ms

10. Atualizar o contacto de emergência de um paciente

> UPDATE emergency_contact
SET contact_name = :contact_name, phone = :phone, relation = :relation
WHERE idpatient = :id_patient;
SELECT p.*, e.*
FROM patient p
JOIN emergency_contact e ON p.idpatient = e.idpatient
WHERE p.idpatient = :id_patient;

> Tempo de execução: 8 ms

Os tempos de execução das queries foram obtidos ao adicionar 'SET TIMING ON' e 'SET TIMING OFF' para a sua medição.