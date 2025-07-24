# Django Models we have to make

- Lecture(Tutorial)
    - Title : Char Field
    - Date Uploaded : `datetime.now` set automatically 
    - Description : Text Field
    - View Count : Integer Field
    - Is Private : Boolean Field
    - Private People Who Have Access : Many(Lecture)-to-Many(Student)
    - Which Course, this tutorial is part of: Many(Lecture)-to-One(Course) : `Foreign Key`
    - Video(recommended: MP4) : File Field
    - Uploaded By Teacher: Many(Lecture)-to-One(Teacher) `Foreign Key`

- Course(Playlist)
    - Title : Char Field
    - Date Created(`datetime.now` automatically set)
    - Created By Teacher : Many(Course)-to-One(Teacher) `Foreign Key`
    - Videos in this course : One(Course)-to-Many(Lectures) `Foreign Key`
    - Is Private : Boolean Field
    - Students who have access : Many(Course)-to-Many(Student)
    - Price : Integer Field
    
