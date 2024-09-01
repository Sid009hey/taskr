from flask import Flask as flask, render_template, request
app = flask(__name__)
import json
import shutil as fm
import algo

# ALGO.PY ; this is the algorithm module nothing else ; 
rating = algo.levelSys()
print(rating) # FIXME ; do algo.py

taskList = []
displayTask = []
taskNo = 0
loadedTask = []

taskName = None
zenDict = {}

def zenBoards(k,v):
    print("[zenBoards DEBUG]",k,v)
    zenDict[k] = v
    print(zenDict,"ZENBOARD FNC, GLOBAL")

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

def jsonDumpCLI(): # TODO ; Break this function into dataLoad and dataSave with one necessary arg each
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
    print(jstx_j,"JSON LOADED")
    
def metaDump(dict):
    global exportedDict
    print("[metaDump] log, function start")
    exportedDict = json.dumps(dict)
    with open('meta.json','w') as file:
        file.write(exportedDict)

def metaLoad(): # untested code. 
    global exportedDictRead, dictable
    try:
        with open('meta.json', 'r') as file:
            exportedDictRead = file.read()
            dictable = json.loads(exportedDictRead)
    except FileNotFoundError:
        print("[metaLoad] meta.json not found, initializing with an empty dictionary.")
        dictable = {}  # Initialize dictable as an empty dictionary
    except json.JSONDecodeError:
        print("[metaLoad] meta.json is empty or corrupted, initializing with an empty dictionary.")
        dictable = {}  # Initialize dictable as an empty dictionary

jsonDumpCLI() ## USELESS ; currently dumping useless data ; zenboards will make this useful. hopefully.

def statusCall(): ## Rename ; FIXME
    global status
    if taskNo == 0:
        status = "Free"
        inStatus = "#74de6a"
    elif taskNo > 0 and taskNo < 4:
        status = "Progress"
        inStatus = "#deac6a"
    else:
        status = "Busy"
        inStatus = "#de6a6a"

def errorHandling(var):
    if var < 0:
        print("[app.py] How did we get here ? ; TEST")
    if var > 0:
        print("[app.py] Running Perfect ; FIXED")

## zenBoard has current use ; 
## displayTask is ; being displayed on screen
## taskList is ; internal tasks and parsing. !!COMPLETELY UNFORMATTED!! only use for error checking.


## IMPORTANT  ; DO NOT TOUCH THIS. DATABASE IS HELD WITH THIS.

taskList.extend(loadedTask)

## END ;

@app.route("/")
def index():

    # CASE ; declaration of globals ; NECESSARY. DO NOT REFORMAT.
    global displayTask, taskList, taskNo
    pName = request.args.get("pName","")
    rTask = request.args.get("rTask","")
    
    if rTask == "":
        print("[C] 0 rTask is nullified")
        displayTask = taskList
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
        print("[C] 0 ; else for rTask executed")
        displayTask = taskList
    
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
    taskNo = len(displayTask)
    statusCall()
    nameDecider()
        
    return render_template("index.html", taskNo=taskNo, taskName=taskName, pName=pName, status=status, tasks=displayTask, bugfix=taskList)

@app.route("/app")
def appTask():
    global taskNo, metaTask
    metaTask = request.args.get("mTask")
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
    if username == "":
        username="User"
            
    print(username)
    return render_template("profile.html", username=username, taskNo=taskNo, status=status)

@app.route("/zen")
def zen(): ## do not change ; reformat is not worth it.
    global settedTask, metaTask, zenValue
    settedTask = metaTask
    zenValue = request.args.get("zenValue")
    if metaTask != None or "":
        settedTask = metaTask
    try: # rewritten ; fully fixed. pushing to dev.
        print(settedTask)
        if zenValue != None or "":
            zenValue = request.args.get("zenValue")
        elif zenValue == None or "":
            zenValue = zenDict[settedTask]
        
        print("[zen] working")
        zenBoards(settedTask,zenValue) # TODO ; this is probably the problem. resetting due to zenVal being Null ??
        print(zenDict)
        metaDump(zenDict)
    except KeyError:
        print("[KeyError] womp womp")
        
    return render_template("zen.html",zenValue=zenValue,mTask=settedTask)

app.run(host="0.0.0.0",port="5000") ## if port 5000 is taken then except it please. ; exception code
