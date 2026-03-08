My final project for Introduction to Programming.

The goal of the project was to build the administrative side of a school system. Features include a course system, members with different roles, logging in, a grade system that stored grades and is able to generate useful information like grade averages for students, courses, etc.

While I received an A for this project, it does not function 100% as intended. Rather than fix the code, I'm presenting it the way it was when it was turned in, with an explanation of what I would fix:

The system contains several functions that rely on other functions, one of which is a course GPA function that averages the GPAs of students. the course GPA function calls the student GPA function for each student in the course; however, the student GPA function does not produce an integer or float, but a string. To fix this I would've created a separate function for calculating an individual's GPA, and called that when reporting the student's GPA as a string. Then, I could use the calculate GPA function in the course GPA function.
