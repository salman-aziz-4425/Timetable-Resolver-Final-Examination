import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog, ttk

FileReadDict={
    'courses':pd.read_csv("courses.csv"),
     'teachers':pd.read_csv("teachers.csv"),
     'student':pd.read_csv("studentCourse.csv"),
     'rooms':pd.read_csv("rooms.csv"),
    'StudentsCourse':pd.read_csv("studentCourse.csv")
}
globalSchedule=[]
Schedule={}
Std={}
first_item=[]
StoreCost=[]
Neighbour=[]
min=0

FileReadDict.get('courses').columns=['Course code','Courses']
FileReadDict.get('teachers').columns=['Teachers']
FileReadDict.get('rooms').columns=['Room no','Rooms']

FilterFileDict={
    'CourseCode':list(FileReadDict.get('courses')['Course code']),
    'Courses':list(FileReadDict.get('courses')['Courses']),
    'Teachers':list(FileReadDict.get('teachers')['Teachers']),
    'Rooms':list(FileReadDict.get('rooms')['Room no']),
    'Students':list(FileReadDict.get('StudentsCourse')['Student Name']),
    'StudentCode':list(FileReadDict.get('StudentsCourse')['Course Code']),
    'Timings':['9:00 am-10:00 am','10:00 am-11:00 am','11:00 am-12:00 pm','12:00 pm-1:00 pm','1:00 pm-2:00 pm','2:00 pm-3:00 pm','3:00 pm-4:00 pm','4:00 pm-5:00 pm'],
    'Days':['Monday','Tuesday','Wednesday','Thursday','Friday']
}

def ConvertDataIntoExcel(df):
    root = tk.Tk()

    root.geometry("800x400")
    root.pack_propagate(False)
    root.resizable(0, 0)

    frame1 = tk.LabelFrame(root, text="Exam Time Table")
    frame1.place(height=330, width=800)

    file_frame = tk.LabelFrame(root, text="Open File")
    file_frame.place(height=100, width=400, rely=0.45, relx=0.25)

    button1 = tk.Button(file_frame, text="Browse A File", command=lambda: File_dialog())
    button1.place(rely=0.65, relx=0.50)

    button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
    button2.place(rely=0.65, relx=0.30)

    label_file = ttk.Label(file_frame, text="No File Selected")
    label_file.place(rely=0, relx=0)

    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1, relwidth=1)

    treescrolly = tk.Scrollbar(frame1, orient="vertical",
                               command=tv1.yview)
    treescrollx = tk.Scrollbar(frame1, orient="horizontal",
                               command=tv1.xview)
    tv1.configure(xscrollcommand=treescrollx.set,
                  yscrollcommand=treescrolly.set)
    treescrollx.pack(side="bottom", fill="x")
    treescrolly.pack(side="right", fill="y")

    def File_dialog():
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select A File",
                                              filetype=(("CSV files", ".csv"), ("All Files", ".*")))
        label_file["text"] = filename
        return None

    def Load_excel_data():
        clear_data()
        tv1["column"] = list(df.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            tv1.insert("", "end", values=row)
        return None

    def clear_data():
        tv1.delete(*tv1.get_children())
        return None

    root.mainloop()

def Assigning_Student():
    for i in range(0,len(FilterFileDict['Students'])):
        Std[FilterFileDict['Students'][i]]={}
        first_item= Std[FilterFileDict['Students'][i]]
        first_item['Code']=[]
        first_item['Code'].append(FilterFileDict['StudentCode'][i])
        Name=FilterFileDict['Students'][i]
        Course=FilterFileDict['StudentCode'][i]
        for j in range(0,len(FilterFileDict['Students'])):
            if Name==FilterFileDict['Students'][j] and FilterFileDict['StudentCode'][j]!=Course:
                first_item['Code'].append(FilterFileDict['StudentCode'][j])


def Assigning_Random_TimeTable():
    for i in range(0,len(FilterFileDict['Courses'])):
        Schedule[FilterFileDict['Courses'][i]]={}
        first_item=Schedule[FilterFileDict['Courses'][i]]
        first_item['Rooms']=FilterFileDict['Rooms'][random.randrange(0,len(FilterFileDict['Rooms']))]
        index=random.randrange(0,len(FilterFileDict['Timings']))
        if FilterFileDict['Timings'][index]=='1:00 pm-2:00 pm':
            while (FilterFileDict['Timings'][index]=='1:00 pm-2:00 pm'):
                index=random.randrange(0,len(FilterFileDict['Timings']))
        first_item['Timings']=FilterFileDict['Timings'][index]
        first_item['Teacher']=FilterFileDict['Teachers'][random.randrange(0,len(FilterFileDict['Teachers']))]
        first_item['Days']=FilterFileDict['Days'][random.randrange(0,len(FilterFileDict['Days']))]
        first_item['Code']=FilterFileDict['CourseCode'][i]
        first_item['Name']=FilterFileDict['Courses'][i]
def isStudentExamAssigned(Assigned,j,second_item):
    return j==second_item['Code'] and second_item['Name'] not in Assigned
def AssignedExam(Assigned,j,second_item,first_item):
    if isStudentExamAssigned(Assigned, j, second_item):
        Assigned.append(second_item['Name'])
        first_item['exam'].append(second_item)
def AssigningStudentsExams(ExamSchedule):
    Assigned=[]
    for i in Std:
        first_item=Std[i]
        first_item['exam']=[]
        for j in first_item['Code']:
            for k in ExamSchedule:
                second_item=ExamSchedule[k]
                AssignedExam(Assigned,j,second_item,first_item)
        Assigned=[]
    return Std
Assigning_Student()
Assigning_Random_TimeTable()
AssigningStudentsExams(Schedule)



def checkTwoCourseClashes(first_item,CourseSchedule,Examday,ExamRoom,Clashes,Examdaytiming,courseClash,j,i):
    second_item = CourseSchedule[j]
    if second_item['Name'] != first_item['Name']:
        OtherExamday = second_item['Days']
        OtherRoom = second_item['Rooms']
        OtherExamdaytiming = second_item['Timings']
        if Examday == OtherExamday:
            if ExamRoom == OtherRoom:
                if Examdaytiming == OtherExamdaytiming:
                    courseClash = courseClash + 1
                    Clashes[i].append(second_item['Name'])
    return courseClash

def CalculateCourseClashes(CourseSchedule):
    Clashes = {}
    courseClash = 0
    for i in CourseSchedule:
        first_item = CourseSchedule[i]
        Clashes[i] = []
        Examday = first_item['Days']
        ExamRoom = first_item['Rooms']
        Examdaytiming = first_item['Timings']
        for j in CourseSchedule:
            courseClash = checkTwoCourseClashes(first_item, CourseSchedule, Examday, ExamRoom, Clashes, Examdaytiming,
                                                courseClash, j, i)
    return courseClash


def CalculateStudentExamClashes(StduentClash):
    clash = 0
    for i in StduentClash:
        first_item = StduentClash[i]
        for j in first_item['exam']:
            second_item = j
            Examday = second_item['Days']
            Examdaytiming = second_item['Timings']
            for k in first_item['exam']:
                clash = comparingStudentCourseClashes(second_item, k, Examday, Examdaytiming, clash)
    return clash



def comparingStudentCourseClashes(second_item,k,Examday,Examdaytiming,clash):
    third_item = k
    if second_item['Name'] != third_item['Name']:
        OtherExamday = third_item['Days']
        OtherExamdaytiming = third_item['Timings']
        if Examday == OtherExamday:
            if (Examdaytiming == OtherExamdaytiming):
                clash = clash + 1
    return clash


def StudentExamclashes(CourseSchedule,StduentClash):
    return int((CalculateStudentExamClashes(StduentClash)/2)+int(CalculateCourseClashes(CourseSchedule))/2 )

def checkIsBreakTime(index):
    return FilterFileDict['Timings'][index]=='1:00 pm-2:00 pm'


def  ReplacePreviousScheduleAndGenerateNew(previousSchedule):
    first_item=previousSchedule[FilterFileDict['Courses'][random.randrange(0,len(FilterFileDict['Courses']))]]
    index=random.randrange(0,len(FilterFileDict['Timings']))
    if checkIsBreakTime(index):
        while checkIsBreakTime(index):
            index=random.randrange(0,len(FilterFileDict['Timings']))
    first_item['Timings']=FilterFileDict['Timings'][index]
    return previousSchedule

def RandomlyReplaceTheCourses(currentSchedule,StoreCost):

    for i in range(0,30):
        newSchedule= ReplacePreviousScheduleAndGenerateNew(currentSchedule)
        Neighbour.append(newSchedule)
        StudentofSchewdule=AssigningStudentsExams(newSchedule)
        newCost=StudentExamclashes(newSchedule,StudentofSchewdule)
        StoreCost.append(newCost)

def GetTheMinimumCostofNeighbour(min):
    index = 0
    for i in range(0,((len(Neighbour)-1) and len(StoreCost))):
        if min>int(StoreCost[i]):
            min=int(StoreCost[i])
            index=i
    return index,min


def PrintTimeTable(currentSchedule,currentClashes):
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Course\t\t\t\t\t\t\tRoom No \t\t  Day\t\t   Timing\t\t\t\tInvigilator ")
    print(
        "----------------------------------------------------------------------------------------------------------------------")
    for course in currentSchedule:
        print(course, end="\t\t\t\t")
        print(currentSchedule[course]['Rooms'], end="     ")
        print(currentSchedule[course]['Days'], end="     ")
        print(currentSchedule[course]['Timings'], end="\t\t\t\t")
        print(currentSchedule[course]['Teacher'])
    print(
        "----------------------------------------------------------------------------------------------------------------------")
    print("Total Number Of Clashes :- ", end="")
    print(currentClashes)
    print("-----------------------------------------------------------------------------------------------------------------------")


def hillClimb():
    StoreCost = []
    Neighbour = []
    min_cost = float('inf')
    currentSchedule = Schedule

    while True:
        StudentofSchedule = AssigningStudentsExams(currentSchedule)
        currentClashes = StudentExamclashes(currentSchedule, StudentofSchedule)
        RandomlyReplaceTheCourses(currentSchedule, StoreCost)

        index, min_cost = GetTheMinimumCostofNeighbour(min_cost)

 
        if currentClashes <= min_cost:
            PrintTimeTable(currentSchedule, currentClashes)
            return [currentClashes, currentSchedule]

    
        currentSchedule = Neighbour[index]
        Neighbour = []


def hillClimbRecursion(listHill):
    if listHill[0] == 0:
        df = pd.DataFrame(listHill[1])
        ConvertDataIntoExcel(df)
        return
    return hillClimbRecursion(hillClimb())

# Call hillClimb only once
result = hillClimb()


hillClimbRecursion(result)

print(result[0])
