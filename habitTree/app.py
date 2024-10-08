from flask import Flask as flask, render_template, request
app = flask(__name__)
import json
import shutil as fm
import algo

# ALGO.PY ; this is the algorithm module nothing else ; 
rating = algo.levelSys()
print(rating)

taskList = []
displayTask = []
taskNo = 0
loadedTask = []
taskName = None
zenDict = {}

def zenBoards(k,v):
    print("[zenBoards DEBUG]",k,v)
    zenDict[k] = v
    print(zenDict) 

def nameDecider():
    global taskName
    try:
        taskName = taskList[-1]
        print("[nameDecider]",taskName) # NOT OPTIMAL ; but it works
    except IndexError:
        taskName = ""
        for i in range(0,1):
            print("[nameDecider] taskName error faced, handled. ; FIXED")
        errorHandling(-1)    

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
zenBoards("ford","modelt")

## use extend

def scoreAlgorithm(): # can be deprecated after algo.py is finished ; FIXME
    return "[sAlgo] 0"

def loopTask(x):
    if x == taskList:
        print("[LT] Task Safe ? Check Length")
        print(len(x))

def jsonDumpCLI():
    # a Python object (dict):
    x = {
      "name": "John",
      "age": 30,
      "city": "New York"
    }

    # convert into JSON:
    y = json.dumps(x)
    with open('data.json','w') as file:
        file.write(y)
        
    with open('data.json','r') as file:
        jstx = file.read()
        jstx_j = json.loads(jstx)
    # the result is a JSON string:

    print(y, "NON JSON FILED")  # FYI ; jstx -> is the file that has been READ, jstx_j is the READ file loaded in JSON 
    print(jstx_j,"JSON LOADEDDD WOHOOOOOOO")

jsonDumpCLI() ## USELESS ; currently dumping useless data ; zenboards will make this useful. hopefully.

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
        print("[app.py] How did we get here ? ; TEST")
    if var > 0:
        print("[app.py] Running Perfect ; FIXED")
## displayTask is ; being displayed on screen
## taskList is ; internal tasks and parsing. !!COMPLETELY UNFORMATTED!! only use for error checking.


## IMPORTANT  ; DO NOT TOUCH THIS. DATABASE IS HELD WITH THIS.

taskList.extend(loadedTask)

## END ;

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
        try:
            taskList.remove(rTask)
        except ValueError:
            for i in range(0,3):                
                print('[ValueError] CRITICAL. TASK LIST NOT UPDATED. ; FIXME')

    elif rTask not in displayTask and rTask != "":
        print("[index()] fixing function calls ; FIXME")
        taskList.append("null_3")
        taskList.remove("null_3")
        displayTask = taskList
        if rTask in displayTask:
            displayTask.remove(rTask)
            saveTasks()
            try: 
                displayTask.remove(rTask)
            except ValueError:
                print("[ValueError] TASK LIST ALREADY UPDATED")  
                displayTask = taskList
                saveTasks()
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
    nameDecider()
        
    return render_template("index.html", taskName=taskName, pName=pName, status=status, tasks=displayTask, bugfix=taskList)

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

    username = request.args.get("username","")
    usrn = json.dumps(username)
    with open('meta.json','w') as file:
        file.write(usrn)

    if username == "":
        with open('meta.json','r') as file:
            usrnRead = file.read() # FIXME ; problem writing to json ; json format has quotes for str ; RELATED to line 177
            username = usrnRead
            print(username)
            if username == "":     # this doesnt do anything to permanize ; FIXME               
                print(username)
                print("[profPage] USERNAME EMPTY, RESORTING TO USER.")
                username = "User"
            
    print(username)
    return render_template("profile.html", username=username, taskNo=taskNo, status=status)


app.run(host="0.0.0.0",port="5000")
