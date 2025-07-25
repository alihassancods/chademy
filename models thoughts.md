# Django Models we have to make

- Lecture(Tutorial)
    - Title : Char Field
    - Date Uploaded : `datetime.now` set automatically 
    - Description : Text Field
    - View Count : Integer Field
    - Is Private : Boolean Field
    - Private People Who Have Access : Many(`Lecture`)-to-Many(`Student`)
    - Which Course, this tutorial is part of: Many(`Lecture`)-to-One(`Course`) : `Foreign Key`
    - Video(recommended: MP4) : File Field
    - Uploaded By Teacher: Many(`Lecture`)-to-One(`Teacher`) `Foreign Key`

- Course(Playlist)
    - Title : Char Field
    - Date Created(`datetime.now` automatically set)
    - Created By Teacher : Many(`Course`)-to-One(`Teacher`) `Foreign Key`
    - Videos in this course : One(`Course`)-to-Many(`Lectures`) `Foreign Key`
    - Is Private : Boolean Field
    - Students who have access : Many(`Course`)-to-Many(`Student`)
    - Price : Integer Field

- Student(derivedFrom : `django.contrib.auth.models.AbstractBaseUser`)
    - Username `unique`
    - Email : Email Field : `Must be validated and tempmail must be blocked`
    - Name : Char Field : `Must be checked for spam and even wrong characters which display poorly(huge whatever) on screen`
    - Date of Birth 
    - Age
    - Courses He Own : Many(`Student`)-to-Many(`Course`)
    - Profile Picture : ImageField
    
- Teacher(derivedFrom : `django.contrib.auth.models.AbstractBaseUser`)
    - Username `unique`
    - Email : Email Field
    - Name : Char Field
    - Profile Picture : ImageField
    - Date of Birth
    - Courses he created : One(`Teacher`)-to-Many(`Course`) : `Foreign Key`
    - Lectures he uploaded : One(`Teacher`)-to-Many(`Lecture`) : `Foreign Key`

