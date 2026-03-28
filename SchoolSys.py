# School System Final Project
# CMPT 120 - Intro to Programming
# Martijn van Berk, Usman Ishaq, and Wells Ely

# --- Imports ---

import hashlib
import sys

# --- Global Data Structures ---

Members = []
StudentCourse = []
StudentQuizGrades = []
StudentTestGrades = []
StudentAssignmentGrades = []

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# --- File Persistence Utilities ---

def member_exists(schoolID):
    try:
        with open("Members.csv", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 5 and parts[1].strip() == schoolID:
                    return True
    except FileNotFoundError:
        return False
    return False

def add_member_to_file(name, schoolID, accountName, password, memberType):
    if member_exists(schoolID):
        print("Error: Member ID", schoolID, "already exists.")
        return False
    with open("Members.csv", "a") as file:
        file.write(name + "," + schoolID + "," + accountName + "," + password + "," + memberType + "\n")
        print("Member", name, "with ID", schoolID, "has been added to Members.csv.")
        return True

def load_members():
    try:
        with open("Members.csv", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    Members.append([parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip()]) 
    except FileNotFoundError:
        return False
    return True

def load_student_course():
    try:
        with open("StudentCourse.csv", "r") as file:
            for line in file:
                teacherID, studentID = line.strip().split(",")
                StudentCourse.append([teacherID.strip(), studentID.strip()])
    except FileNotFoundError:
        return False
    return True

def load_grades(filename, target_list): #fully implemented by Dr. Norton
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    teacherID = parts[0].strip()
                    studentID = parts[1].strip()
                    grades = []
                    for x in parts[2:]:
                        grades.append(x.strip()) # got rid of int()
                    target_list.append([teacherID, studentID, grades])
    except FileNotFoundError:
        return False
    return True
    
# --- Class Hierarchy (unchanged except for saving new members) ---

class Member: 
    def __init__(self, schoolID, password, name="default", accountName="default", memberType="default"): 
        global Members
        self.name = None
        self.schoolID = None
        self.accountName = None
        self.password = None
        self.memberType = None

        hashed = hash_password(password)
        found = False
        for record in Members:
            if record[1] == schoolID and record[3] == hashed:
                self.name = record[0]
                self.schoolID = record[1]
                self.accountName = record[2]
                self.password = record[3]
                self.memberType = record[4]
                found = True
                break
        if not found:
            sys.exit("Login failed: Member not found or password incorrect.")
    
    def change_password(self, old_password, new_password):
        global Members
        if self.password != hash_password(old_password): # checks if old password is correct
            print("Incorrect old password.")
            return False
        self.password = hash_password(new_password) # updates password for the object
        for record in Members: # updates password in Members list
            if record[1] == self.schoolID:
                record[3] = self.password
        with open("Members.csv", "w") as file: # saves Members list to csv (data persistence)
            for record in Members:
                file.write(record[0] + "," + record[1] + "," + record[2] + "," + record[3] + "," + record[4] + "\n")
        print("Password changed.")
        return True


class Student(Member): 
    def __init__(self, schoolID, password):
        super().__init__(schoolID, password)

    def view_grades(self):
        global StudentQuizGrades, StudentTestGrades, StudentAssignmentGrades
        found = False
        for records, label in [(StudentQuizGrades, "Quiz"), (StudentTestGrades, "Test"), (StudentAssignmentGrades, "Assignment")]:
            for record in records:
                if record[1] == self.schoolID:
                    print(label + "grades:", record[2])
                    found = True
        if not found:
            print(self.name + " has no grades!")
        return found

    def compute_quiz_avg(self):
        global StudentQuizGrades
        for record in StudentQuizGrades:
            if record[1] == self.schoolID:
                grades = record[2]
                if grades: # checks if there are any grades, avoid division by zero
                    for grade in grades: # validates grades are between 0 and 100
                        if grade < 0 or grade > 100: 
                            print("Error: a quiz average can not be calculated because one or more quiz grade(s) exceed the quiz grade limits (0-100).")
                            return False
                    avg = sum(grades)/len(grades)
                    print(f"Quiz average for {self.name}: {avg}")
                    return avg
        print(f"There are no quiz grades for {self.name}.") 
        return 0
            
    def compute_test_avg(self):
        global StudentTestGrades
        for record in StudentTestGrades:
            if record[1] == self.schoolID:
                grades = record[2]
                if grades:  # checks if there are any grades, avoid division by zero
                    for grade in grades: # validates grades are between 0 and 100
                        if grade < 0 or grade > 100:
                            print("Error: a test average can not be calculated because one or more test grade(s) exceed the test grade limits (0-100).")
                            return False
                    avg = sum(grades)/len(grades)
                    print(f"Test average for {self.name}: {avg}")   
                    return avg
        print(f"There are no test grades for {self.name}.")
        return 0
    
    def compute_assignment_sum(self):
        global StudentAssignmentGrades
        for record in StudentAssignmentGrades:
            if record[1] == self.schoolID:
                grades = record[2]
                if grades: # checks if there are any grades
                    for grade in grades: # validates grades are between 0 and 1
                        if grade < 0 or grade > 1:
                            print("Error: an assignment average can not be calculated because one or more assignment grade(s) exceed the assignment grade limits (0-1).")
                            return False
                    total = sum(grades)
                    print(f"Assignment grade for {self.name}: {total} out of 10")
                    return total
        print(f"There are no assignment grades for {self.name}.")  
        return 0

    def view_final_grade(self):
        quiz_avg = self.compute_quiz_avg() 
        test_avg = self.compute_test_avg()
        assignment_sum = self.compute_assignment_sum()
        final_grade = (quiz_avg * 0.4) + (test_avg * 0.5) + (assignment_sum)
        '''if quiz_avg == False or test_avg == False or assignment_sum == False:
            print("Error: a final grade can not be calculated because one or more grade(s) exceed the grade limits.")
            return False'''
        print(f"Final grade for {self.name}: {final_grade}")
        return final_grade


class Teacher(Member):
    def __init__(self, schoolID, password): # fully implemented by Dr. Norton
        super().__init__(schoolID, password)

    def StudentAssignedToTeacher(self, studentID):
        global StudentCourse
        for record in StudentCourse:
            if record[0] == self.schoolID and record[1] == studentID:
                return True
        return False

    def add_grade(self, studentID, grade, gradeType):
        global StudentQuizGrades, StudentTestGrades, StudentAssignmentGrades
        grade_added = False
        if self.StudentAssignedToTeacher(studentID) == False: # checks if student is assigned to teacher
            print("Error: Student is not assigned to this teacher.")
            return False
        
        if gradeType.lower() == "quiz": # made case insensitive - Van, 30 Apr 25
            GradeList = StudentQuizGrades
            if float(grade) < 0 or float(grade) > 100: # grade validation updated to be gradeType specific - Van, 2 May 25
                print("Error: Grade out of range (0-100).")
                return False
        elif gradeType.lower() == "test": # made case insensitive - Van, 30 Apr 25
            GradeList = StudentTestGrades
            if float(grade) < 0 or float(grade) > 100: # grade validation updated to be gradeType specific (0-100)- Van, 2 May 25
                print("Error: Grade out of range (0-100).")
                return False
        elif gradeType.lower() == "assignment": # made case insensitive - Van, 30 Apr 25
            GradeList = StudentAssignmentGrades
            if float(grade) < 0 or float(grade) > 1: # grade validation updated to be gradeType specific (0-1) - Van, 2 May 25
                print("Error: Grade out of range (0-1).")
                return False
        else:
            print("Invalid grade type, please use 'quiz', 'test', or 'assignment'.")
            return False
        
        for record in GradeList: # adds grade as long as the student has a record in GradeList (quiz, test, or assignment)
            if record[0] == self.schoolID and record[1] == studentID:
                record[2].append(grade)
                print("Grade added.")
                grade_added = True
                break
        if [self.schoolID, studentID] in StudentCourse and not grade_added: # adds student record to GradeList if it doesn't exist yet.
            GradeList.append([self.schoolID, studentID, [grade]])
            print("Grade added.")
            grade_added = True
        if grade_added: 
            if GradeList == StudentQuizGrades: 
                with open("StudentQuizGrades.csv", "w") as file: # updates the StudentQuizGrades.csv file
                    for record in GradeList:
                        file.write(record[0] + "," + record[1] + ",")
                        for grade in record[2]:
                            file.write(str(grade) + ",")
                        file.write("\n")
            elif GradeList == StudentTestGrades:
                with open("StudentTestGrades.csv", "w") as file: # updates the StudentTestGrades.csv file
                    for record in GradeList:
                        file.write(record[0] + "," + record[1] + ",")
                        for grade in record[2]:
                            file.write(str(grade) + ",")
                        file.write("\n")
            elif GradeList == StudentAssignmentGrades:
                with open("StudentAssignmentGrades.csv", "w") as file: # updates the StudentAssignmentGrades.csv file
                    for record in GradeList:
                        file.write(record[0] + "," + record[1] + ",")
                        for grade in record[2]:
                            file.write(str(grade) + ",")
                        file.write("\n")
        return True

    def compute_student_quiz_avg(self, studentID): # Added by Usman, 1 May 25
        global StudentQuizGrades
        if self.StudentAssignedToTeacher(studentID) == False: # checks if student is assigned to teacher
            print("Student is not assigned to this teacher.")
            return False
        for record in StudentQuizGrades:
            if record[0] == self.schoolID and record[1] == studentID:
                grades = record[2]
                if grades:
                    for grade in grades: # validates grades are between 0 and 100
                        if grade < 0 or grade > 100:
                            print("Error: a quiz grade average can not be calculated because one or more quiz grade(s) exceed the quiz grade limits (0-100).")
                            return False
                    avg = sum(grades) / len(grades)
                    #print(f"Quiz average for student {studentID}: {avg}")
                    return avg
        print(f"No quiz grades for student {studentID}.")
        return 0

    def compute_student_test_avg(self, studentID):
        global StudentTestGrades
        if self.StudentAssignedToTeacher(studentID) == False: # checks if student is assigned to teacher
            print("Student is not assigned to this teacher.")
            return False
        for record in StudentTestGrades:
            if record[0] == self.schoolID and record[1] == studentID:
                grades = record[2]
                if grades:
                    for grade in grades: # validates grades are between 0 and 100
                        if grade < 0 or grade > 100: 
                            print("Error: a test grade average can not be calculated because one or more test grade(s) exceed the test grade limits (0-100).")
                            return False
                    avg = sum(grades) / len(grades)
                    #print(f"Test average for {studentID}: {avg}")
                    return avg
        print(f"No test grades for student {studentID}.")
        return 0
    
    def compute_student_assignment_sum(self, studentID):
        global StudentAssignmentGrades
        if self.StudentAssignedToTeacher(studentID) == False: # checks if student is assigned to teacher
            print("Student is not assigned to this teacher.")
            return False
        for record in StudentAssignmentGrades:
            if record[0] == self.schoolID and record[1] == studentID:
                grades = record[2]
                if grades:
                    for grade in grades: # validates grades are between 0 and 1
                        if grade < 0 or grade > 1:
                            print("Error: an assignment grade sum can not be calculated because one or more assignment grade(s) exceed the assignment grade limits (0-1).")
                            return False
                    total = sum(grades)
                    #print(f"Assignment total for {studentID}: {total}")
                    return total
        print(f"No assignment grades for student {studentID}.")
        return 0

    def compute_student_final_grade(self, studentID):
        global StudentQuizGrades, StudentTestGrades, StudentAssignmentGrades
        if self.StudentAssignedToTeacher(studentID) == False: # checks if student is assigned to teacher
            print("Student is not assigned to this teacher.")
            return False
        quiz_avg = self.compute_student_quiz_avg(studentID)
        test_avg = self.compute_student_test_avg(studentID)
        assignment_sum = self.compute_student_assignment_sum(studentID)
        final = 0.4 * quiz_avg + 0.5 * test_avg + assignment_sum
        #print(f"Final grade for {studentID}: {final}")
        return final
    
    def compute_class_quiz_avg(self):
        global StudentQuizGrades
        count = 0
        total = 0
        for record in StudentQuizGrades:
            if record[0] == self.schoolID:
                studentID = record[1]
                if self.compute_student_quiz_avg(studentID) == False:
                    print("Error: a class quiz average can not be calculated because one or more quiz grade(s) exceed the quiz grade limits (0-100).")
                    return False
                total += self.compute_student_quiz_avg(studentID)
                count += 1

        if count == 0:
            print(f"There are no quiz grades for {self.name}'s students.")
            return 0
        avg = total / count
        print(f"The class quiz average is: {avg}")
        return avg

    def compute_class_test_avg(self):
        global StudentTestGrades
        count = 0
        total = 0
        for record in StudentTestGrades:
            if record[0] == self.schoolID:
                studentID = record[1]
                if self.compute_student_test_avg(studentID) == False:
                    print("Error: a class test average can not be calculated because one or more test grade(s) exceed the test grade limits (0-100).")
                    return False
                total += self.compute_student_test_avg(studentID)
                count += 1
        if count == 0:
            print(f"There are no test grades for {self.name}'s students.")
            return 0
        avg = total / count
        print(f"The class test average is: {avg}")
        return avg

    def compute_class_assignment_sum(self):
        global StudentAssignmentGrades
        count = 0
        total = 0
        for record in StudentAssignmentGrades:
            if record[0] == self.schoolID:
                studentID = record[1]
                if self.compute_student_assignment_sum(studentID) == False:
                    print("Error: a class assignment sum can not be calculated because one or more assignment grade(s) exceed the assignment grade limits (0-1).")
                    return False
                total += self.compute_student_assignment_sum(studentID)
                count += 1
        if count == 0:
            print(f"There are no assignment grades for {self.name}'s students.")
            return 0
        avg = total / count
        print(f"The class assignment average is: {avg}")
        return avg

    def compute_class_final_grades(self):
        global StudentQuizGrades, StudentTestGrades, StudentAssignmentGrades
        count = 0
        total = 0
        for record in StudentQuizGrades:
            if record[0] == self.schoolID:
                studentID = record[1]
                if self.compute_student_final_grade(studentID) == False:
                    print("Error: a class final grade can not be calculated because one or more grade(s) exceed the grade limits.")
                    return False
                total += self.compute_student_final_grade(studentID) 
                count += 1
        if count == 0:
            print(f"There are no grades for {self.name}'s students.")
            return 0
        avg = total / count
        print(f"The class average is: {avg}")
        return avg


class Administrator(Member):
    def __init__(self, schoolID, password): # fully implemented by Dr. Norton
        super().__init__(schoolID, password)

    def assign_student_to_teacher(self, teacherID, studentID):
        global StudentCourse
        for record in StudentCourse: # checks if student is already assigned to another teacher
            if record[1] == studentID and record[0] != teacherID:
                print("Student already assigned to another teacher.")
                return False
        if [teacherID, studentID] not in StudentCourse: # updates [StudentCourse] list
            StudentCourse.append([teacherID, studentID])
            with open("StudentCourse.csv", "a") as file: # updates StudentCourse.csv
                file.write(teacherID + "," + studentID + "\n")
            print("Assigned student.")
            return True
        print("Already assigned.")
        return False

    def remove_student_from_teacher(self, teacherID, studentID): # added by Van - 30 Apr 25.
        global StudentCourse
        if [teacherID, studentID] in StudentCourse: # updates [StudentCourse] list
            StudentCourse.remove([teacherID, studentID]) 
            with open("StudentCourse.csv", "w") as file: # updates StudentCourse.csv file
                for record in StudentCourse:
                    file.write(record[0] + "," + record[1] + "\n")
            print("Removed student from teacher.")
            return True
        print("Student not found.")
        return False

    def reassign_student(self, oldTeacherID, newTeacherID, studentID): # added by Van - 30 Apr 25. needs booleans.
        global StudentCourse
        for record in StudentCourse:
            if record[1] == studentID and record[0] == oldTeacherID:
                record[0] = newTeacherID # updates [StudentCourse] list
                with open("StudentCourse.csv", "w") as file: # updates StudentCourse.csv file
                    for record in StudentCourse:
                        file.write(record[0] + "," + record[1] + "\n")
                print("Reassigned student to", newTeacherID)
                return True
        print("Student not found.")
        return False

    def display_members(self, memberType):
        for m in Members:
            if m[4] == memberType:
                print(m[0] + "/t/t (" + m[1] + ")")


class SuperAdmin(Administrator, Teacher):
    def __init__(self, schoolID, password):
        super().__init__(schoolID, password)

    def _create_member(self, name, schoolID, accountName, password, memberType):
        global Members
        if member_exists(schoolID):
            print("Error: Member already exists.")
            return None
        hashed = hash_password(password)
        Members.append([name, schoolID, accountName, hashed, memberType])
        add_member_to_file(name, schoolID, accountName, hashed, memberType)
        if memberType == "Teacher":
            return Teacher(schoolID, password)
        elif memberType == "Student":
            return Student(schoolID, password)
        elif memberType == "Administrator":
            return Administrator(schoolID, password)
        elif memberType == "SuperAdmin":
            return SuperAdmin(schoolID, password)

    def create_teacher(self, name, schoolID, accountName, password):
        return self._create_member(name, schoolID, accountName, password, "Teacher")

    def create_student(self, name, schoolID, accountName, password):
        return self._create_member(name, schoolID, accountName, password, "Student")

    def create_admin(self, name, schoolID, accountName, password):
        return self._create_member(name, schoolID, accountName, password, "Administrator")

    def create_superadmin(self, name, schoolID, accountName, password):
        return self._create_member(name, schoolID, accountName, password, "SuperAdmin")

    def reset_password(self, schoolID, new_password):
        global Members
        hashed = hash_password(new_password)
        if member_exists(schoolID) == False: # checks if member exists
            print("Error: Member not found.")
            return False
        for record in Members: # updates password in Members list
            if record[1] == schoolID:
                record[3] = hashed
        with open("Members.csv", "w") as file: # saves Members list to csv (data persistence)
            for record in Members:
                file.write(record[0] + "," + record[1] + "," + record[2] + "," + record[3] + "," + record[4] + "\n")
        print("Password reset.")
        return True

# --- Main Program ---

def main():
    load_members()
    load_student_course()
    load_grades("StudentQuizGrades.csv", StudentQuizGrades)
    load_grades("StudentTestGrades.csv", StudentTestGrades)
    load_grades("StudentAssignmentGrades.csv", StudentAssignmentGrades)
    print("System loaded. Welcome to the School System, Dr. Roger Linwood Norton!")

main()
