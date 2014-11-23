# Sample data lists and dictionaries to be inserted in datastore

### Doctors ###
doctor_list = []

doctor = {}
doctor['email'] = 'strahald@gmail.com'
doctor['first_name'] = 'Smeagol'
doctor['last_name'] = 'Trahald'
doctor['phone'] = '696-969-6969'
doctor['hospital'] = 'Misty Mountains Hospital'
doctor_list.append(doctor)

doctor = {}
doctor['email'] = 'dccorona@gmail.com'
doctor['first_name'] = 'Dominic'
doctor['last_name'] = 'Corona'
doctor['phone'] = '248-622-7708'
doctor['hospital'] = 'Detroit Mafia Medical Center'
doctor_list.append(doctor)

### Patients ###
patient_list = []

patient = {}
patient['email'] = 'frodo@lotr.com'
patient['doctor_email'] = 'strahald@gmail.com'
patient['first_name'] = 'Frodo'
patient['last_name'] = 'Baggins'
patient['phone'] = '555-555-5555'
patient['diagnosis'] = 'Yes'
patient['septic_risk'] = -1.0
patient['basis_pass'] = 'password'
patient_list.append(patient)

patient = {}
patient['email'] = 'sam@lotr.com'
patient['doctor_email'] = 'strahald@gmail.com'
patient['first_name'] = 'Samwise'
patient['last_name'] = 'Gamgee'
patient['phone'] = '555-555-5555'
patient['diagnosis'] = 'No'
patient['septic_risk'] = -1.0
patient['basis_pass'] = 'password'
patient_list.append(patient)

patient = {}
patient['email'] = 'pippin@lotr.com'
patient['doctor_email'] = 'strahald@gmail.com'
patient['first_name'] = 'Peregrin'
patient['last_name'] = 'Took'
patient['phone'] = '555-555-5555'
patient['diagnosis'] = 'Maybe'
patient['septic_risk'] = -1.0
patient['basis_pass'] = 'password'
patient_list.append(patient)

patient = {}
patient['email'] = 'seedsystem00@gmail.com'
patient['doctor_email'] = 'strahald@gmail.com'
patient['first_name'] = 'Andy'
patient['last_name'] = 'Lee'
patient['phone'] = '734-834-9095'
patient['diagnosis'] = 'No'
patient['septic_risk'] = -1.0
patient['basis_pass'] = 'eecs481seed'
patient_list.append(patient)

### PQuantData ###
# The following measurements represent ranges of values for both 
# septic patients and normal patients.  Values come from multiple
# sources of research

# Blood Pressure
sbp_low = [110, 95, 80]
dbp_low = [70, 60, 50]
sbp_high = [120, 110, 100]
dbp_high = [80, 75, 70]
# Body Temp
bt_low = [97.0, 99.0, 101.3]
bt_high = [99.0, 100.5, 102.2]
# GSR
gsr_low = [0.00, 0.15, 0.2]
gsr_high = [0.10, 0.25, 0.35]
# Skin Temp
st_low = [89.6, 79.4, 68.0]
st_high = [95.0, 87.0, 79.0]
# Heart Rate
hr_low = [60, 75, 90]
hr_high = [90, 105, 120]
# Air Temp (room temp)
at_low = 68.0
at_high = 73.0
# Sleep patterns
sleep_list = [['Light', 'Deep', 'Light', 'Rem', 'Light', 'Deep', 'Light', 'Rem', 'Light', 'Deep', 'Light', 'Rem', 'Light', 'Rem', 'Light', 'Light'],
	['Still', 'Light', 'Light', 'Deep', 'Light', 'Light', 'Light', 'Still', 'Light', 'Light', 'Rem', 'Light', 'Light', 'Deep', 'Light', 'Still'],
	['Still', 'Still', 'Light', 'Light', 'Still', 'Light', 'Rem', 'Light', 'Light', 'Deep', 'Light', 'Still', 'Light', 'Light', 'Still', 'Still']]

active_list = []
for i in range(70):
	active_list.append('Still')
for i in range(20):
	active_list.append('Walk')
for i in range(5):
	active_list.append('Run')
for i in range(5):
	active_list.append('Bike')

### Watson ###
watson_list = []

qa_pair = {}
qa_pair['question'] = 'What initiates sepsis?'
qa_pair['answer'] = 'Sepsis can initiate not only through the direct dissemination of pathogens into the bloodstream but also indirectly as a result of postsurgical complications, traumas, burn, hemorrhages, and gut IR-mediated bacterial translocations.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What is the cause of organ failure in severe sepsis?'
qa_pair['answer'] = 'The cause of the organ failure in severe sepsis is unknown, but it resembles the multiple organ dysfunction syndrome (MODS) seen in patients who survive serious traumatic injury.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What is the cause of death in patients dying of sepsis?'
qa_pair['answer'] = 'The real cause of death and organ failure in most patients dying of sepsis is unknown.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What do patients with sepsis present?'
qa_pair['answer'] = 'Patients with sepsis often present with high spiking fevers, shock, and respiratory failures'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What is sepsis?'
qa_pair['answer'] = 'Sepsis is a heightened systemic immune response state due to an infection. It is defined as a combination of Systemic Inflammatory Response Syndrome (SIRS), and a confirmed or suspected infection, usually caused by bacteria.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What are common indications for ICU admission?'
qa_pair['answer'] = 'Pulmonary complications, sepsis, neurological disorders, and cardiovascular problems'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'Is Serum interleukin-8 serum level a valuable predictive metric for sepsis?'
qa_pair['answer'] = 'Yes, it has a 95% negative predictive value.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'Is there a biomarker model that can be used to predict the mortality of children with septic shock?'
qa_pair['answer'] = 'The PERSEVERE biomarker model reliably predicts mortality of children with septic shock.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What proportion of sepsis patients have cancer?'
qa_pair['answer'] = 'Up to 1 in 5 patients admitted into an ICU with sepsis also have cancer.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What is the mortality rate for severe sepsis?'
qa_pair['answer'] = 'Hospital mortality rates for severe sepsis are estimated at 4.2%'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What types of cancer patients have a higher risk of infection?'
qa_pair['answer'] = 'Hematologic cancer patients have significantly higher admission illness severity, rates of infections, and PICU mortality than solid cancer patients.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'Are infants more at risk of sepsis?'
qa_pair['answer'] = 'Infants have also been shown to have a higher incidence or organ dysfunction in the setting of severe sepsis'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What is severe sepsis or septic shock?'
qa_pair['answer'] = 'Severe sepsis was defined as sepsis plus evidence of organ dysfunction defined around pediatric parameters (Table 2), whereas septic shock was defined as meeting sepsis criteria plus the presence of "cardiovascular dysfunction" present after the administration of at least 40 mL/kg in 1 hour of fluid.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'Can sepsis in children lead to death?'
qa_pair['answer'] = 'The incidence of sepsis continues to increase with a mortality rate (both early and late) that positions it among the leading causes of death for children.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'Is sepsis hereditary?'
qa_pair['answer'] = 'Susceptibility to sepsis and the clinical course of patients with sepsis are both highly heterogeneous, which raises the strong possibility that the host response to infection is, at least in part, influenced by heritable factors.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What are the symptoms of Systemic Inflammatory Response Syndrome (SIRS)'
qa_pair['answer'] = 'Body temperature below 36 C (degrees Celsius) or above 38 C. Tachycardia, with heart rate above 90 beats per minute. Tachypea (increased respiratory rate), with respiratory rate above 20 per minute, or arterial partial pressure of carbon dioxide (PaCO2) less than 4.3 kPa (kilo Pascals), equivalent to 32 mmHg (millimeters of mercury). White blood cell (WBC) count less than 4,000/mm3(cubic millimeter) or above 12,000/mm3, or the presence of more than 10% immature neutrophils (band forms).'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What does severe sepsis cause?'
qa_pair['answer'] = 'When sepsis causes Multiple Organ Dysfunction Syndrome (MODS), such as damage to vital organs, decreased perfusion, or hypotension, it is termed severe sepsis.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What are the indicators of growing sepsis?'
qa_pair['answer'] = 'Several growth factors and hormones are up-regulated to play crucial roles in sepsis by promoting immunomodulatory, antiapoptotic, and neoangiogenesis effects to the immune-reactive cells of inflamed and ischemic tissues.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'Can a new antibiotic reduce the mortality rate of sepsis?'
qa_pair['answer'] = 'A second important implication of this novel immunosuppression paradigm is that newer antibiotics alone are unlikely to substantially improve sepsis mortality because the major underlying  defect is impaired patient immunity.'
watson_list.append(qa_pair)

qa_pair = {}
qa_pair['question'] = 'What is the average cost of treating sepsis?'
qa_pair['answer'] = 'Direct costs per sepsis patient for ICU treatment in the United States have been estimated at more than $40,000.'
watson_list.append(qa_pair)
