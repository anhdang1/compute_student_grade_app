"""Anh Dang
App that take student inputs and compute grades.

input: name(str), score (int), grade status (int), division (int)
output: name(str), score (int), grade status (str - Graded or Pass/Fail), division (str - Upper or Lower) - all store in a text file

Note: download the input.text file in the same folder to load the data.
"""

student_list = []

need_to_save = False #boolean to prevent duplicate in saving values
filename = ''  #allow users to input filename if it was not determined

class Student:
    count = 0
    total_score = 0
    graded_count = 0
    total_graded_score = 0
    count_100 = 0
    count_A = 0

    def __init__(self,name,score,status,division):
       self.name = name
       self.score = score
       self.status = status  
       self.division = division
       self.grade = self.compute_grade()


       #update totals
       Student.count += 1
       Student.total_score += self.score
       if self.score == 100:
           Student.count_100 += 1 
       if self.grade == 'A':
           Student.count_A += 1 
       


    def compute_grade(self):
        if self.status == 'PassFail':
            if self.score >= 40:
                return 'Pass'
            else:
                return 'Fail'
        else:
            Student.total_graded_score += self.score
            Student.graded_count += 1
            if self.division == 'Upper':
                cutoff = 90   
            else:
                cutoff = 80
            if self.score >= cutoff:
                return 'A'
            else:
                return 'B'
        
    def __str__(self):
        return f'{"Name":s}:{self.name:>12s}|{"Score":s}:{self.score:>12d}|{"Status":s}:{self.status:>12s}|{"Division":s}:{self.division:>12s}|{"Grade":s}:{self.grade:^7s}|'


    def displaystr(self):
        return f'|{self.name:^12s}|{self.score:^12d}|{self.status:^12s}|{self.division:^12s}|{self.grade:^6s}|'
    

    def savestr(self):
        return f'{self.name:s},{self.score:d},{self.status:s},{self.division:s},{self.grade:s}'

    @classmethod
    def compute_average_score(cls):
        if cls.count > 0:
            return cls.total_score / cls.count
        else:
            return None


    @classmethod
    def compute_average_graded(cls):
        if cls.graded_count > 0:
            return cls.total_graded_score /cls.graded_count
        else:
            return None
    
    @classmethod
    def resetstats(cls):
        cls.total_graded_score = cls.total_score = 0
        cls.count = cls.graded_count = 0
        cls.count_A = cls.count_100 = 0

    @classmethod
    def summary_string(cls):
        summaryinfo = ''
        average = cls.compute_average_score()
        average_graded = cls.compute_average_graded()

        if average is not None:
            summaryinfo += f'{"Number of scores":<25s}:{cls.count:>5d}\n{"Average Score":<25s}:{average:5.2f}\n'
            summaryinfo += f'{"Number of perfect scores":<25s}:{cls.count_100:>5d}\n'
            if average_graded is not None:
                summaryinfo += f'{"Number of graded scores":<25s}:{cls.graded_count:>5d}\n{"Average Score for Graded":<25s}:{average_graded:5.2f}\n'
                summaryinfo += f'{"Number of A Grades":<25s}:{cls.count_A:>5d}\n' 
            else:
                summaryinfo += f'{"No students on grade basis":<25s}\n'
        else:
            summaryinfo += f'{"No Student Data to compute summary info":<25s}\n'
        
        return summaryinfo

    @staticmethod
    def line():
        return '-'*60
    @staticmethod
    def caption():
        return f'|{"Name":^12s}|{"Score":^12s}|{"Status":^12s}|{"Division":^12s}|{"Grade":^6s}|')

#end class
def processline(line,separator = None):   #process data from submit()
    global student_list, student_dict,need_to_save

    in_list = line.split(separator)  
    name = in_list[0]
    score = int(in_list[1])

    while not is_valid_score(score):
       print('Error.Enter score in range 0..100')
       score = int(input('Try again >>'))

    graded = int(in_list[2])
    while not is_valid_graded(graded):
       print('Error.Enter 1 or 0 only for grade status')
       graded = int(input('1 for graded 0 for pass/fail >>'))
   
    div = int(in_list[3])
    while not is_valid_division(div):
       print('Error.Enter 1 or 0 only for division')
       div = int(input('1 for upper 0 for lower >>'))
    
    status = 'Graded' if graded else 'PassFail'  #convert 1/0 to string
    division = 'Upper' if div else 'Lower'

    student = Student(name,score,status,division) 
    student_list.append(student)
    

    need_to_save = True  #prevent duplication

    return student

def is_valid_score(sc):
    return sc >= 0 and sc <= 100

def is_valid_graded(graded):

    return graded == 1 or graded == 0

def is_valid_division(division):
    return division == 1 or division == 0

def submit():  #take input from users
    
    line = input('Name, score, graded/not, upper/lower division, latter two as 1/0 >>')
    
    student = processline(line)
    print(student)
    

def load():  #load data from a specified file

   with open('input.txt', 'r') as infile:
       lines = infile.readlines()
    
   for line in lines:
       processline(line, ',')   
   
   print(len(lines), 'student records loaded')  


def summary():  #output summary
   global student_list
   if student_list:  
       print(Student.summary_string())  
   else:
       print('No data in system')
    
def reset():  #reset data
   global need_to_save,filename

   if not student_list:    
       Student.resetstats()  
       print('No student records to reset')

   if need_to_save:  
       save()
   clear_data()
   Student.resetstats()  
   filename = ''  
   need_to_save = False   

def display():  
   global student_list
   if student_list:
       print(Student.line())
       print(Student.caption())
       print(Student.line())
       for student in student_list:
           print(student.displaystr())  
       print(Student.line())
   else:
    print('No students in system')


def save():
   global student_list,need_to_save,filename

   if not student_list:
       print('No data to save..')
       return
    
   if need_to_save:   
        if not filename:
            filename = input('Enter filename to save to: >>')
        
        with open('out.txt','w') as outfile:
            for student in student_list:
                outfile.write(student.savestr() + '\n')
        print(len(student_list) , 'records saved to file.')

        need_to_save = False   
   else:
       print('No data needs to be saved..')

def search(): 
    global student_list
    if not student_list:  
        print('No Student data available to search..')
        return
    key = input('Enter name to search for: >>')
    found = False
    for student in student_list:  
        if student.name == key:
            print('Found ' + key)
            print(student)
            found = True
            break    

    if not found:
        print(key + ' was not found.')
    
def clear_data():
   global student_list

   student_list.clear()
   

#optional function. placing the code in main is fine.
def exit_app():
    if need_to_save:
        save()
    clear_data()
    print('Bye..')
 
quit = False
while not quit:
 print('1.Submit 2.Load 3. Summary 4.Display 5. Save 6.Search 7.Reset 8.Exit')
 choice = int(input('Enter choice:  '))
 if choice == 1:
     submit()
 elif choice == 2:
     load()  
 elif choice == 3:
     summary()
 elif choice == 4:
     display()
 elif choice == 5:
     save()
 elif choice == 6:
     search()
 elif choice == 7:  
     reset()
     print("Ready for a new series..")
 elif choice == 8:
     exit_app()  
     quit = True  
 else:
     print('Invalid Choice!')
