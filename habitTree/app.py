from flask import Flask as flask, render_template, request
app = flask(__name__)

taskList = []
displayTask = []
taskNo = 0
loadedTask = []

def saveTasks(filename='tasks.txt'):
    # Overwrite the file with the current list of tasks
    with open(filename, 'w') as file:
        for task in taskList:
            file.write(task + '\n')

def loadTasks(filename='tasks.txt'):
    global loadedTask
    with open(filename, 'r') as file:
        for line in file.readlines():
            loadedTask.append(line.strip())
            print(loadedTask)
loadTasks()


## use extend

def scoreAlgorithm():
    return "[sAlgo] 0"

def loopTask(x):
    if x == taskList:
        print("[LT] Task Safe ? Check Length")
        print(len(x))

def statusCall():
    global status
    if taskNo == 0:
        status = "Green"
        inStatus = "#74de6a"
    elif taskNo > 0 and taskNo < 4:
        status = "Orange"
        inStatus = "#deac6a"
    else:
        status = "Red"
        inStatus = "#de6a6a"

def errorHandling(var):
    if var < 0:
        print("[app.py] How did we get here ? ; FIXME")

## displayTask is ; being displayed on screen
## taskList is ; internal tasks and parsing. !!COMPLETELY UNFORMATTED!! only use for error checking.


## IMPORTANT  ; DO NOT TOUCH THIS. DATABASE IS HELD WITH THIS.

taskList.extend(loadedTask)

@app.route("/")
def index():
    # CASE ; declaration of globals ; NECESSARY. DO NOT REFORMAT.
    global displayTask, taskList
    pName = request.args.get("pName","")
    rTask = request.args.get("rTask","")
    
    if rTask == "":
        print("[C] 0")
    if rTask in displayTask:
        displayTask.remove(rTask)
        
    else:
        print("[C] 0")
    
    if pName == "":
        showName = "world"
    else:
        if pName not in taskList:
            taskList.append(pName)
            saveTasks()
            displayTask = taskList
        else:
            taskList.append("null_2")
            displayTask = taskList.remove("null_2") # null_2 is an internal error code ; for repeating values in taskList
            # reason for reinitiating displayTask is ; to prevent None from appearing 
            displayTask = taskList
    statusCall()
        
    return render_template("index.html", pName=pName, status=status, tasks=displayTask, bugfix=taskList)

@app.route("/app")
def appTask():
    global taskNo
    index()
    taskNo = len(taskList) # FIXED ; iteration ghosting
    statusCall()
    return render_template("app.html", taskNo=taskNo, status=status, tasks=displayTask)

@app.route("/profile")
def profilePage():
    appTask()
    global username

    username = request.args.get("username","User")

    if username == "":
        print("[profPage] USERNAME EMPTY, RESORTING TO USER.")
        username = "User"
    
    print(username)
    return render_template("profile.html", username=username, taskNo=taskNo, status=status)

app.run(host="0.0.0.0",port="5000")
