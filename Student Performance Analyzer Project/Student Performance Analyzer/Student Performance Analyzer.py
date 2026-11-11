import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
SCH_FILE = os.path.join(script_dir, 'school_data.json')

def load_data():
    if os.path.exists(SCH_FILE):
        with open(SCH_FILE, 'r') as f:
            return json.load(f)
    return {'Grade 1':{}, 'Grade 2': {}, 'Grade 3': {}, 'Grade 4': {}, 'Grade 5': {}, 'Grade 6': {}, 'Grade 7': {}, 'Grade 8': {}}

def save_data(school):
    with open(SCH_FILE, 'w') as f:
        json.dump(school, f, indent=2)

school = load_data()

def add_student_data(name, ID, class1, subjects, marks):
    blank=[]

    fields=[
        ('name', name),
        ('ID', ID),
        ('class', class1),
        ('subjects', subjects),
        ('marks', marks)
    ]    

    for names, value in fields:
        if value==None or (isinstance(value, str) and value.strip()==""):
            blank.append(names)

    if blank:
        return f"The following fields are empty: {", ".join(blank)}.\n"

    for existing_class, students in school.items():
        if ID in students:
            if existing_class!=class1:
                return f"Error: ID '{ID}' is already assigned to a student in {existing_class}. Please use a unique ID.\n"
            break

    if len(ID)!=5:
        return "The ID is invalid. Must have 5 characters and start with a letter followed by numbers.\n"

    majina=name.strip().replace(" ","")
    if majina.isdigit():
        return "The name has to be in letters.\n"
    
    try:
        int(ID[1:])
    except ValueError:
        return "The ID has to have numbers for the second character onwards.\n"

    subject_list = subjects.split(',')
    marks_list = marks.split(',')

    if len(subject_list)!=len(marks_list):
        return "The number of subjects and marks have to match and be comma separated!\n"

    for i in subject_list:
        if not i.strip().replace(" ","").isalpha():
            return "The subjects have to be in letters.\n"
        
    try:
        for i in marks_list:
            float(i)
    except ValueError:
        return "The marks have to be valid numbers.\n"
    
    for mark in marks_list:
        if float(mark)>100 or float(mark)<0:
            return "The marks have to be positive numbers between 0-100.\n"

    new_subjects=[]
    new_marks_indices=[]
    new_marks=[]
    redundant_items =[]

    if class1 in school:
        if ID in school[class1]:
            if school[class1][ID].get('name')==name:
                original_sub_list=school[class1][ID]['subjects']
                
                for subject in subject_list:
                    if subject not in original_sub_list and subject not in new_subjects:
                        new_subjects.append(subject)
                    else:
                        redundant_items.append(subject)

                if redundant_items:
                    print(f"These subjects are already in the records: {", ".join(redundant_items)}")

                if new_subjects:
                    for i in new_subjects:
                        new_marks_indices.append(subject_list.index(i))

                    for i in new_marks_indices:
                        new_marks.append(marks_list[i])

                    school[class1][ID]['subjects'].extend(new_subjects)
                    school[class1][ID]['marks'].extend(new_marks)
                    save_data(school)

                else:
                    return "The subject and its marks are already in the record.\n"
            else:
                return "The ID is in use by another student. Please double check and try again.\n"
        else:
            school[class1][ID]={
                'name': name,
                'subjects': (subjects).split(','),
                'marks':(marks).split(',')
                }
            save_data(school)
    else:
        school[class1] = {}
        school[class1][ID] = {
            'name': name, 
            'subjects': (subjects).split(','),
            'marks': (marks).split(',')
        }
        save_data(school)
        
    return f"Student data has been saved, {school[class1][ID]}.\n"

def display_marks_individual(name, ID, class1):
    blank =[]

    field = [
        ('name', name),
        ('ID', ID),
        ('class', class1)
    ]

    for names, values in field:
        if values==None or isinstance(values, str) and values.strip()=="":
            blank.append(names)

    if blank:
        return f"The following fields are empty: {(', '.join(blank))}.\n"

    if class1 in school:
        if ID in school[class1]:
            if school[class1][ID].get('name')==name:
                subject_list=school[class1][ID]['subjects']
                marks_list=school[class1][ID]['marks']

                print(f"These are the marks attained by {name}")
                print(f"{'No.':<3} {'Subject':<20}{'Marks'}")
                    
                for index, (subject, mark) in enumerate(zip(subject_list, marks_list), 1):
                    print(f"{index:<3}. {subject:<20}: {mark}")
                return f"Thank you.\n"

            else:
                return "The ID is in use by another student. Please double check and try again.\n"
        else:
            return "The ID is not in the class indicated.\n"
    else:
        return "The class is not in the school records.\n"

def student_average_marks(name, ID, class1):
    blank=[]

    fields=[
        ('name', name),
        ('ID', ID),
        ('class', class1)
    ]

    for names, values in fields:
        if values==None or isinstance(values, str) and values.strip()=="":
            blank.append(names)

    if blank:
        return f"The following fields are empty: {", ".join(blank)}.\n"

    if class1 in school:
        if ID in school[class1]:
            if school[class1][ID].get('name')==name:
                total=0
                marks_list=school[class1][ID]['marks']
                for i in marks_list:
                    total+=float(i)
                no_subjects=len(marks_list)
                average_marks=total/no_subjects
                return f"The average marks attained by {name} are {average_marks}.\n"
            
            else:
                return "The ID is in use by another student. Please double check and try again.\n"
        else:
            return "The ID is not in the class indicated.\n"
    else:
        return "The class is not in the school records.\n"

def class_average(class1):
    if class1==None or isinstance(class1, str) and class1.strip()=="":
            return "The class field is empty."

    if class1 in school:
        class_marks=[]
        for student_id, student_data in school[class1].items():
            total=sum(float(mark) for mark in student_data['marks'])

            student_avg=total/len(student_data['marks'])
            class_marks.append(student_avg)
            print(f"{student_id:<5}. {school[class1][student_id]['name']:<30}:{student_avg:.2f}")

        class_total=sum(float(i) for i in class_marks)
        class_avg = class_total/len(class_marks)
        print(f"{class1:<37} {class_avg:.2f}")
        return f'Average marks scored by {class1}.\n'
    
    else:
        return "The class is not in the school records.\n"

def delete_student_marks(name, ID, class1, subjects):
    blank=[]

    fields=[
        ('name', name),
        ('ID', ID),
        ('class', class1),
        ('subjects', subjects)
    ]

    for names, values in fields:
        if values==None or isinstance(values, str) and values.strip()=="":
            blank.append(names)

    if blank:
        return f"The following fields are empty: {", ".join(blank)}.\n"
    
    subjects_Q=subjects.split(',')

    unavailable_entries = []

    if class1 in school:
        if ID in school[class1]:
            if school[class1][ID].get('name')==name:
                subject_list=school[class1][ID]['subjects']
                marks_list=school[class1][ID]['marks']

            for sub in subjects_Q:
                if sub not in subject_list:
                    unavailable_entries.append(sub)

                if unavailable_entries:
                    return f"The following subjects are not in the records therefore cannot be deleted: {', '.join(unavailable_entries)}.\n"
                
                new_subjects=[]
                for sub in subject_list:
                    if sub not in subjects_Q:
                        new_subjects.append(sub)

                new_indices=[]
                for i in new_subjects:
                    new_indices.append(subject_list.index(i))

                new_marks=[]
                for i in new_indices:
                    new_marks.append(marks_list[i])

                print(f"These are the marks obtained by {name}")
                for index, (sub, mark) in enumerate(zip(new_subjects, new_marks), 1):
                    print(f"{index:<3}. {sub:<20} {mark}")

                school[class1][ID]['subjects'] = new_subjects
                school[class1][ID]['marks'] = new_marks
                save_data(school)

                return f"The subject(s) as well as the corresponding marks have been deleted.\n"
            else:
                return "The ID is in use by another student. Please double check and try again.\n"
        else:
            return "The ID is not in the class indicated.\n"
    else:
        return "The class is not in the school records.\n"
            
def remove_student_from_records(name, ID, class1):
    blank=[]

    fields = [
        ('name', name),
        ('ID', ID),
        ('class', class1)
    ]

    for names, values in fields:
        if values==None or isinstance(values, str) and values=="":
            blank.append(names)

    if blank:
        return f"The following fields are blank: {", ".join(blank)}.\n"

    if class1 in school:
        if ID in school[class1]:
            if school[class1][ID].get('name')==name:
                del school[class1][ID]
                save_data(school)
                return f"{name}, {ID} of {class1} has been deleted from the records.\n"
            else:
                return "The ID is in use by another student. Please double check and try again.\n"
        else:
            return "The ID is not in the class indicated.\n"
    else:
        return "The class is not in the school records.\n"

def get_specific_subject(name, class1, ID, subjects):
    blank = []

    fields = [
        ('name', name),
        ('class', class1),
        ('ID', ID),
        ('subjects', subjects)
    ]

    for names, values in fields:
        if values==None or isinstance(values, str) and values=="":
            blank.append(names)

    if blank:
        return f"The following fields are blank: {", ".join(blank)}.\n"

    subject_Q=subjects.split(',')

    if class1 in school:
        if ID in school[class1]:
            if school[class1][ID].get('name')==name:
                subject_list=school[class1][ID]['subjects']
                marks_list=school[class1][ID]['marks']

                final_subjects=[]
                marks_indices=[]
                unavailable=[]

                for i in subject_Q:
                    if i in subject_list:
                        final_subjects.append(i)
                    else:
                        unavailable.append(i)

                if unavailable:
                    print(f"These subjects are not in the records: {", ".join(unavailable)}.\n")

                for i in final_subjects:
                    marks_indices.append(subject_list.index(i))

                final_marks=[]
                for i in marks_indices:
                    final_marks.append(marks_list[i])
                for index, (subject, marks) in enumerate(zip(final_subjects, final_marks), 1):
                    print(f"{index:<3}. {subject:<20}: {marks}")
                return f"The marks obtained by {name} in {subjects}"
            else:
                return "The ID is in use by another student. Please double-check and try again.\n"
        else:
            return "THe ID is not in the class indicated.\n"
    else:
        return "The class is not in the school records.\n"

def main():
    while True:
        print("---Welcome to the Student Performance Analyzer---")
        print("1. Add student data.")
        print("2. Display marks and grades for a student.")
        print("3. Display average grade for a student.")
        print("4. Display average marks for an entire class.")
        print("5. Delete specific grades for a student.")
        print("6. Remove a student's records entirely.")
        print("7. Search for a specific subject grade for a student.")
        print("8. Exit.")

        try:
            choice=int(input("Enter a number from 1-8 to choose what to do next: "))
        except ValueError:
            print("Please enter a valid choice.")
            choice=None

        if choice==1:
            name=input("Enter the student name in full: ")
            ID=input("Enter the student ID number in full(5 characters, 1st is a letter then numbers): ")
            class1=input("Enter the class the student is attending: ")
            subjects=input("Enter the subjects the student is attempting(comma separated): ")
            marks=input("Enter the marks the student achieved(comma separated): ")
            result=add_student_data(name, ID, class1, subjects, marks)
            print(result)
            continue

        if choice==2:
            name=input("Enter the student name in full: ")
            ID=input("Enter the student ID number in full: ")
            class1=input("Enter the class the student is attending: ")
            result=display_marks_individual(name, ID, class1)
            print(result)
            continue

        if choice==3:
            name=input("Enter the student name in full: ")
            ID=input("Enter the student ID number in full: ")
            class1=input("Enter the class the student is attending: ")
            result=student_average_marks(name, ID, class1)
            print(result)
            continue

        if choice==4:
            class1=input("Enter the class whose average you wish to see: ")
            result=class_average(class1)
            print(result)
            continue

        if choice==5:
            name=input("Enter the names of the student whose marks you wish to expunge: ")
            ID=input("Enter the ID number of the student in question: ")
            class1=input("Enter the class of the student in question: ")
            subjects=input("Enter the subjects whose grades you wish to expunge: ")
            result=delete_student_marks(name, ID, class1, subjects)
            print(result)
            continue

        if choice==6:
            name=input("Enter the name of the student whose records you want to clear entirely: ")
            ID=input("Enter the ID of the student whose records you want to clear entirely: ")
            class1=input("Enter the class of the student whose records you want to clear entirely: ")
            result=remove_student_from_records(name, ID, class1)
            print(result)
            continue

        if choice==7:
            name=input("Enter the name of the student in question: ")
            ID=input("Enter the ID of the student in question: ")
            class1=input("Enter the class of the student in question: ")
            subjects=input("Enter the subject/(s) in question: ")
            result=get_specific_subject(name, class1, ID, subjects)
            print(result)
            continue

        if choice==8:
            print("You are exiting the Student Performance Analyzer. Good Bye!")
            break

        else:
            print("Invalid choice. Choose a number between 1-8.")

if __name__ =='__main__':
    main()