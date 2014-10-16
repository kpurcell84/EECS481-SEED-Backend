# Sample data lists and dictionaries to be inserted in datastore

# Doctors
doctor_list = []
doctor = {}

doctor['email'] = 'smeagol@lotr.com'
doctor['first_name'] = 'Smeag'
doctor['last_name'] = 'Ol'
doctor['phone'] = '696-969-6969'
doctor['hospital'] = 'Misty Mountains Hospital'
doctor_list.append(doctor)

doctor['email'] = 'sauron@lotr.com'
doctor['first_name'] = 'Saur'
doctor['last_name'] = 'On'
doctor['phone'] = '555-555-5555'
doctor['hospital'] = 'Mordor Healthcare Associates'
doctor_list.append(doctor)

doctor['email'] = 'gothmog@lotr.com'
doctor['first_name'] = 'Goth'
doctor['last_name'] = 'Mog'
doctor['phone'] = '555-555-5555'
doctor['hospital'] = 'Pelennor Field Emergency Clinic'
doctor_list.append(doctor)

# Patients
patient_list = []
patient = {}

patient['email'] = 'frodo@lotr.com'
patient['doctor_email'] = 'smeagol@lotr.com'
patient['first_name'] = 'Frodo'
patient['last_name'] = 'Baggins'
patient['phone'] = '555-555-5555'
patient['diagnosis'] = 'Yes'
patient['septic_risk'] = 82
patient_list.append(patient)

patient['email'] = 'sam@lotr.com'
patient['doctor_email'] = 'smeagol@lotr.com'
patient['first_name'] = 'Samwise'
patient['last_name'] = 'Gamgee'
patient['phone'] = '555-555-5555'
patient['diagnosis'] = 'No'
patient['septic_risk'] = 4
patient_list.append(patient)

patient['email'] = 'merry@lotr.com'
patient['doctor_email'] = 'smeagol@lotr.com'
patient['first_name'] = 'Merrywine'
patient['last_name'] = 'Brandybuck'
patient['phone'] = '555-555-5555'
patient['diagnosis'] = 'Maybe'
patient['septic_risk'] = 56
patient_list.append(patient)

patient['email'] = 'grima@lotr.com'
patient['doctor_email'] = 'sauron@lotr.com'
patient['first_name'] = 'Grima'
patient['last_name'] = 'Wormtongue'
patient['phone'] = '555-555-5555'
patient['diagnosis'] = 'Yes'
patient['septic_risk'] = 89
patient_list.append(patient)