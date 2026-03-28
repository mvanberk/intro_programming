

# --- SYSTEM POPULATION FILE ---

from SchoolSys import *

print("\n--- Logging in as SuperAdmin ---")
superadmin1 = SuperAdmin("SA100", "secret")

# --- Create SuperAdmin, Admins, Teachers, Students ---

print("\n--- Creating SuperAdmin, Admins, Teachers, and Students ---")
superadmin1.create_superadmin("Lena Powers", "SA200", "Lena.Powers", "power123")
superadmin1.create_admin("Alice Monroe", "AD300", "Alice.Monroe", "alicepwd")
superadmin1.create_admin("Bruce Wayne", "AD400", "Bruce.Wayne", "darkknight")

superadmin1.create_teacher("Tom Baker", "T500", "Tom.Baker", "teachme1")
superadmin1.create_teacher("Linda Nash", "T600", "Linda.Nash", "teachme2")
superadmin1.create_teacher("Carlos Diaz", "T700", "Carlos.Diaz", "teachme3")
superadmin1.create_teacher("Nina Hall", "T800", "Nina.Hall", "teachme4")

superadmin1.create_student("Jake Long", "S900", "Jake.Long", "pass1")
superadmin1.create_student("Mia Chen", "S901", "Mia.Chen", "pass2")
superadmin1.create_student("Omar Lee", "S902", "Omar.Lee", "pass3")
superadmin1.create_student("Sara Kim", "S903", "Sara.Kim", "pass4")
superadmin1.create_student("Leo Tran", "S904", "Leo.Tran", "pass5")
superadmin1.create_student("Nora Vance", "S905", "Nora.Vance", "pass6")
superadmin1.create_student("Zane Cruz", "S906", "Zane.Cruz", "pass7")
superadmin1.create_student("Tina Fox", "S907", "Tina.Fox", "pass8")

# --- Assign Students to Teachers ---

print("\n--- Assigning Students to Teachers ---")
superadmin1.assign_student_to_teacher("T500", "S900")
superadmin1.assign_student_to_teacher("T500", "S901")
superadmin1.assign_student_to_teacher("T600", "S902")
superadmin1.assign_student_to_teacher("T600", "S903")
superadmin1.assign_student_to_teacher("T700", "S904")
superadmin1.assign_student_to_teacher("T700", "S905")
superadmin1.assign_student_to_teacher("T800", "S906")
superadmin1.assign_student_to_teacher("T800", "S907")

# --- Teachers Adding Grades ---

print("\n--- Teachers Adding Grades ---")
teacher1 = Teacher("T500", "teachme1")
teacher1.add_grade("S900", 88, "quiz")
teacher1.add_grade("S900", 92, "test")
teacher1.add_grade("S901", 80, "quiz")
teacher1.add_grade("S901", 0.5, "assignment")

teacher2 = Teacher("T600", "teachme2")
teacher2.add_grade("S902", 76, "quiz")
teacher2.add_grade("S902", 85, "test")
teacher2.add_grade("S903", 60, "quiz")
teacher2.add_grade("S903", 72, "test")

teacher3 = Teacher("T700", "teachme3")
teacher3.add_grade("S904", 90, "quiz")
teacher3.add_grade("S904", 89, "test")
teacher3.add_grade("S905", 78, "quiz")
teacher3.add_grade("S905", 1.0, "assignment")

# --- Invalid Grade Tests (should print errors) ---

print("\n--- Testing Invalid Grades ---")
teacher1.add_grade("S900", 105, "quiz")     # Invalid
teacher1.add_grade("S900", -5, "test")       # Invalid
teacher1.add_grade("S900", 1.5, "assignment")# Invalid

# --- Students Viewing Grades and Final Grades ---

print("\n--- Students Viewing Their Grades ---")
student1 = Student("S900", "pass1")
student2 = Student("S901", "pass2")
student3 = Student("S902", "pass3")

student1.view_grades()
student2.view_grades()
student3.view_grades()

print("\n--- Students Viewing Their Final Grades ---")
student1.view_final_grade()
student2.view_final_grade()
student3.view_final_grade()

# --- Teacher Computing Student and Class Averages ---

print("\n--- Teacher Computing Student Averages ---")
teacher1.compute_student_quiz_avg("S900")
teacher1.compute_student_test_avg("S900")
teacher1.compute_student_assignment_sum("S901")
teacher1.compute_student_final_grade("S901")

print("\n--- Teacher Computing Class Averages and Totals ---")
print("Quiz Average for class:", teacher1.compute_class_quiz_avg())
print("Test Average for class:", teacher1.compute_class_test_avg())
print("Assignment Sum for class:", teacher1.compute_class_assignment_sum())

print("\n--- Teacher Computing Final Grades for Entire Class ---")
teacher1.compute_class_final_grades()

# --- Admin Testing Reassignments and Removals ---

print("\n--- Admin Testing Reassigning Students ---")
admin1 = Administrator("AD300", "alicepwd")
admin1.reassign_student("T500", "T600", "S900")  # Move Jake Long from T500 to T600

print("\n--- Admin Testing Removing Student from Course ---")
admin1.remove_student_from_teacher("T600", "S902")  # Remove Omar Lee from Linda Nash

# --- Admin Viewing Members ---

print("\n--- Admin Viewing All Current Teachers and Students ---")
admin1.display_members("Teacher")
admin1.display_members("Student")

# --- SuperAdmin Testing Password Reset ---

print("\n--- SuperAdmin Resetting Student Password ---")
superadmin1.reset_password("S901", "newpass2")

# --- Student Logging In With New Password After Reset ---

print("\n--- Student Logging In After Password Reset ---")
student_reset = Student("S901", "newpass2")
student_reset.view_grades()
student_reset.view_final_grade()

# --- Final System State Message ---

print("\n--- System Population File Complete ---")
