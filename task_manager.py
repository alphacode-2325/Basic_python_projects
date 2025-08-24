"""
    Welcome to AlphaCode.
    
    -->What is this program?<--
        This is a simple CLI based task manager program.
    
    -->What people can do on it?<--
        people can:
            1. Add their tasks.
            2. View their tasks.
            3. Mark their tasks as completed.
            4. Delete tasks
    
    -->Some additional features<--
        1. All the tasks will be stored in sqlite3 database.
        2. All the tasks will be stored date wise.
        3. User can see any task of his past dates.
        

"""

#importing the required libraries
import sqlite3
from colorama import Fore, Style, init
from datetime import date

init(autoreset=True)

#connecting to the databse
database = sqlite3.connect("task_manager_db.db")
cursor = database.cursor()
#creating table for tasks
cursor.execute("CREATE TABLE IF NOT EXISTS tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, date TEXT NOT NULL, status TEXT NOT NULL)")
database.commit()

#function to write task
def wrtie_task(task:str):
    try:
        #accessing and storing today's date
        date_today = date.today().strftime("%d/%m/%Y")
        status = "not completed"
        #writing the task in the database
        cursor.execute("INSERT INTO tasks(task, date, status) VALUES(?, ?, ?)", (task, date_today, status))
        database.commit()
        print(Fore.GREEN + f"Your task:{task} is stored in the database...")
    except Exception as e:
        print(Fore.RED + str(e))

# function to read tasks
def read_task(read_date:str="today"):
    try:
        #control statements for fetching correct statement
        
        #if date is today
        if read_date == "today":
            read_date = date.today().strftime("%d/%m/%Y")
            #fetching tasks for today's date
            tasks = cursor.execute("SELECT * FROM tasks WHERE date = ?", (read_date,)).fetchall()
            #if tasks are available for today
            if tasks:
                print(Fore.YELLOW + "Below are your tasks:\nTASK ID | TASK NAME | DATE | STATUS")
                for task in tasks:
                    print(Fore.GREEN + str(task))
                else:
                    print(Fore.YELLOW + "End of the record...")
                    
            #if there is no task for today
            else:
                print(Fore.YELLOW + "You have no tasks for today.")
        
        #else date will be entered by user
        else:
            #fetching the tasks for the date user entered
            tasks = cursor.execute("SELECT * FROM tasks WHERE date = ?", (read_date,)).fetchall()
            #if tasks are available for today
            if tasks:
                print(Fore.YELLOW + "Below are your tasks:\nTASK ID | TASK NAME | DATE | STATUS")
                for task in tasks:
                    print(Fore.GREEN + str(task))
                else:
                    print(Fore.YELLOW + "End of the record...")
                    
            #if there is no task for today
            else:
                print(Fore.YELLOW + f"You had no tasks for date:{read_date}.")
                    
    except Exception as e:
        print(Fore.RED + str(e))

#function to mark tasks as completed (only current date's tasks can be marked as completed)
def mark_task(task:str):
    try:
        #checking the presence of task in the database
        task = cursor.execute("SELECT task FROM tasks WHERE task = ?",(task,)).fetchone()[0]
        if task:
            #marking the task as completed
            status = "completed"
            cursor.execute("UPDATE tasks SET status = ? WHERE task = ?", (status, task))
            database.commit()
            print(Fore.GREEN + f"The task:{task} is marked as completed.")
        else:
            print(Fore.YELLOW + "The task not found. Please enter a valid task or check spellings of task...")
            
    except Exception as e:
        print(Fore.RED + str(e))

#function to delete task from the database
def delete_task(task:str):
    try:
        #checking the presence of the task in the database.
        task = cursor.execute("SELECT task FROM tasks WHERE task = ?",(task,)).fetchone()[0]
        if task:
            #taking confirmation from user
            confirm = input("Are you sure to delete this task (y/n): ").strip().lower()
            if confirm == "y"or"yes":
                #deleting the task
                cursor.execute("DELETE FROM tasks WHERE task = ?",(task,))
                database.commit()
                print(Fore.GREEN + f"The task:{task} is deleted.")
            elif confirm == "n"or"no":
                print(Fore.YELLOW + f"The task:{task} is not deleted.")
            else:
                print(Fore.RED + "invalid input! please enter a valid input.")
        
    except Exception as e:
        print(Fore.RED + str(e))

# putting it all together
print(Fore.YELLOW + "Welcome to AlphaCode's task manager...\n\n")

while True:
    print("What do you want to do:\n1. Add a task.\n2. View your tasks.\n3. Mark a task as completed.\n4. Delete a task.\n5. exit.")
    choice = input("Enter your chocie here: ").strip()
    #add a task
    if choice == "1":
        task = input("Enter your task: ").strip().lower()
        wrtie_task(task)
    #view your tasks
    elif choice == "2":
        read_date = input("Type 'today' or a specific date(DD/MM/YYYY): ").strip().lower()
        read_task(read_date)
    #mark a task as completed
    elif choice == "3":
        task = input("Enter the task: ").strip().lower()
        mark_task(task)
    #delete a task
    elif choice == "4":
        task = input("Enter the task: ").strip().lower()
        delete_task(task)
    #exit
    elif choice == "5":
        print(Fore.YELLOW + "Exiting the software...")
        exit()
    else:
        print(Fore.RED + "invlid input! please enter a valid input...")
        
