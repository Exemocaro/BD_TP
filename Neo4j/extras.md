> View

MATCH (e:Episode)-[:PERFORMED_BY {TYPE: 'Appointment'}]->(s:Staff)-[:BELONGS_TO]->(d:Department),
      (e)-[:WAS_FREQUENTED_BY]->(p:Patient)
RETURN 
    e.scheduled_on AS appointment_scheduled_date,
    e.appointment_datetime AS appointment_datetime,
    s.emp_id AS doctor_id,
    s.qualifications AS doctor_qualifications,
    d.dept_name AS department_name,
    p.patient_fname AS patient_first_name,
    p.patient_lname AS patient_last_name,
    p.blood_type AS patient_blood_type,
    p.phone AS patient_phone,
    p.email AS patient_email,
    p.gender AS patient_gender;

> Procedure

CALL apoc.periodic.iterate(
  "MATCH (e:Episode) 
   WHERE e.bill.idbill = $p_bill_id 
   RETURN e",
  "WITH e, $p_paid_value AS p_paid_value
   WITH e, apoc.convert.fromJsonMap(e.bill) AS bill, p_paid_value
   SET bill.payment_status = CASE 
                              WHEN p_paid_value < bill.total THEN 'FAILURE' 
                              ELSE 'PROCESSED' 
                            END
   SET e.bill = apoc.convert.toJson(bill)
   WITH e, p_paid_value, bill
   WHERE p_paid_value < bill.total
   CALL apoc.util.validate(p_paid_value < bill.total, 'Paid value is inferior to the total value of the bill.', [0]) 
   RETURN e",
  {batchSize:1, parallel:false, params: {p_bill_id: yourBillId, p_paid_value: yourPaidValue}}
);

> Trigger

CALL apoc.periodic.iterate(
  "MATCH (e:Episode) WHERE e.discharge_date IS NOT NULL AND e.processed IS NULL RETURN e",
  "WITH e
   WITH e, apoc.convert.fromJsonMap(e.bill) AS bill, apoc.convert.fromJsonList(e.PRESCRIPTIONS) AS prescriptions
   
   UNWIND prescriptions AS prescription
   WITH e, bill, prescription, 
        COALESCE(e.ROOM_COST, 0) AS room_cost, 
        COALESCE(e.TEST_COST, 0) AS test_cost, 
        COALESCE(prescription.MEDICINE_COST * prescription.DOSAGE, 0) AS medicine_cost
   WITH e, bill, room_cost, test_cost, COLLECT(medicine_cost) AS medicine_costs
   WITH e, bill, room_cost, test_cost, REDUCE(total=0, cost IN medicine_costs | total + cost) AS other_charges
   WITH e, bill, room_cost + test_cost + other_charges AS total_cost

   SET bill.room_cost = room_cost,
       bill.test_cost = test_cost,
       bill.other_charges = other_charges,
       bill.total = total_cost,
       bill.payment_status = 'PENDING',
       bill.registered_at = date()

   // Update the episode node with the new bill and processed status
   SET e.bill = apoc.convert.toJson(bill),
       e.processed = true",
  {batchSize:1, parallel:false}
);

