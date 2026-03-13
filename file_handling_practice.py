# file handling Converting program into functions + File Handling
         
                 #proper FILE HANDLING
students=[]
def add_students():
    try:
        print("\nAdd Students")
        name=input("Enter student name: ")
        mark=input("Enter srudent mark: ")
        if not name or not mark:
            print("Name and Mark cant be empty")
            return
        if name.isdigit():
            print("Error:No numbers allowed in name")
            return
        if not mark.isdigit():
            print("Error:Mark must be numbers.")
            return
        with open("students.txt","a") as file:
            file.write(f"{name},{mark}\n")
        students.append({"name":name,"mark":mark})
        print(f"Student {name} added successfully")
    except Exception as e:
        print("Input error:",e)

#1
def show_students():
    try:
        print("\nStudent Lists")
        #2
        with open("students.txt","r") as file:
            lines=file.readlines()
            if not lines:
                print("No students record found")
                return
            for k,i in enumerate(lines,1):
                name,mark=i.strip().split(",")
                print(f"{k}.Name:{name} | Mark:{mark}")
    except FileNotFoundError as e:
        print("No datas found",e)

def search_students():
    name_search=input("Enter name to search: ")
    try:
        with open("students.txt","r") as file:
            lines=file.readlines()
            found=False
            for i in lines:
                name,mark=i.strip().split(",")
                if name.lower()==name_search:
                    print(f"Found→Name:{name} | Mark:{mark}")
                    found=True
                    break
            else:
                print(f"Student {name_search} not found in data")
    except FileNotFoundError as e:
        print("Error:",e)

def delete_students():
    name_del=input("Enter name to delete: ")
    found=False
    try:
        with open("students.txt","r") as file:
            lines=file.readlines()
        with open("students.txt","w") as file:
            for i in lines:
                name,mark=i.strip().split(",")
                if name.lower()==name_del:
                    found=True
                    continue
                file.write(i)
        if found:
            print(f"{name_del} deleted successfully")
        else:
            print("Student not found")
    except FileNotFoundError as e:
        print("Error:",e)

def update_students():
    name_up=input("Enter name to update: ")
    mark_new=input("Enter new mark: ")
    try:
        with open("students.txt","r") as file:
            lines=file.readlines()
            if not lines:
                print("Students data not found.")
                return
        with open("students.txt","w") as file:
            for i in lines:
                name,mark=i.strip().split(",")
                if name.lower()==name_up:
                    file.write(f"{name},{mark_new}\n")
                else:
                    file.write(i)
        print(f"Student {name_up} updated successfully")
    except FileNotFoundError as e:
        print("Error:",e)

#1
while True:
    print("\nStudent Details")
    print("1.Add Student")
    print("2.View Students")
    print("3.Search Student")
    print("4.Delete Student")
    print("5.Update Student")
    print("6.Exit")

    usr=input("Enter your choice: ")
    if usr == "1":
        add_students()
    elif usr == "2":
        show_students()
    elif usr == "3":
        search_students()
    elif usr == "4":
        delete_students()
    elif usr == "5":
        update_students()
    elif usr == "6":
        print("Exiting from program!!!.")
        break
    else:
        print("Invalid Input!.please choose right choice.")
