##Student Performance Analyzer
A Python based Command Line Inteface(CLI) application designed to help teachers or administrators manage student records and analyze academic performance.

##Features
* **Student Management:**Add new students with strict validation for names and unique IDs(e.g a 5 character ID that starts with a letter then numbers)
* **Grade Tracking:** Adds new subjects and marks to existing students, with built-in checks to prevent duplicate entries.
* **Performance Analsis:**
    *View individual subject marks for specific student.
    *Calculate individual student average marks.
    *Calculate the overall average for an entire class.
* **Record Deletion:** Remove specific subject marks or delete a students entire records.
* **Data Persistence:** All data is automatically saved and loaded using a local JSON file("school_data.json"), ensuring records are kept between sessions.


##How to Run
1. Ensure you have Python installed in your computer.
2. Clone this repository or download the files.
3. Open your terminal in the project folder and run:
'''bash
python "Student Perfomance Analyzer.py"

