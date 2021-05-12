space_available = int(input())  # the number of applicants that can be accepted for each department

with open("applicants.txt", encoding='utf-8') as f:
    applicant_keys = ['f_name', 'l_name', 'physics', 'chemistry', 'math', 'CS', 'spec_ex', '1_prior', '2_prior',
                      '3_prior']
    applicants = []
    for line in f:
        applicant = {key: value for key, value in zip(applicant_keys, line.split())}
        applicant['mean_eng'] = (float(applicant['math']) + float(applicant['CS'])) / 2
        applicant['mean_bio'] = (float(applicant['chemistry']) + float(applicant['physics'])) / 2
        applicant['mean_phy'] = (float(applicant['math']) + float(applicant['physics'])) / 2
        applicants.append(applicant)

departments = {'Biotech': "mean_bio", 'Chemistry': 'chemistry', 'Engineering': "mean_eng",
               'Mathematics': 'math', 'Physics': "mean_phy"}

applied_students = {key: [] for key in departments}


for chosen_dept in ('1_prior', '2_prior', '3_prior'):
    for dep, exams in departments.items():
        for i in applicants:
            if float(i['spec_ex']) > float(i[exams]):
                i['best_score'] = float(i['spec_ex'])
            else:
                i['best_score'] = float(i[exams])
        applicants = sorted(applicants, key=lambda x: (x[chosen_dept], -float(x['best_score']),
                                                       x['f_name'], x['l_name']))
        for applicant in applicants[:]:
            if len(applied_students[dep]) < space_available and applicant[chosen_dept] == dep:
                applied_students[dep].append(applicant)
                applicants.remove(applicant)

print(applied_students)
for dep, students in applied_students.items():
    students.sort(key=lambda x: (-float(x['best_score']), x['f_name'], x['l_name']))
    with open(f"{dep}.txt", 'w') as f:
        for student in students:
            f.write(f"{student['f_name']} {student['l_name']} {student['best_score']}\n")