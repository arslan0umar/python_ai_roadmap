# Day 1-2
# Q1
# for i in range(1 , 31):
#     if (i % 3 == 0) and (i % 5 == 0):
#         print(f"{i} - FizzBuzz")
#     elif i % 3 == 0:
#         print(f"{i} - Fizz")
#     elif i % 5 == 0:
#         print(f"{i} - Buzz")

#Q2
# secret = 7
# while True:
#     num = int(input("Enter a Number: "))
#     if (num == secret):
#         print("Correct")
#         break
#     elif (num - secret) > 0:
#         print("Too High")
#     else:
#         print("Too Low")

#Q3
# try:
#     n1 = int(input("Enter first number: "))
# except ValueError:
#     print("Invalid Input")
# try:
#     n2 = int(input("Enter second number: "))
# except ValueError:
#     print("Invalid Input")
# op = input("Enter the operator(+, -, * , /): ")

# match op:
#     case "+":
#         print(f"{n1} {op} {n2} = {n1 + n2}")
#     case "-":
#         print(f"{n1} {op} {n2} = {n1 - n2}")
#     case "*":
#         print(f"{n1} {op} {n2} = {n1 * n2}")
#     case "/":
#         if (n2 == 0):
#             print("Division Error (Division by zero is not possible)")
#             while True:
#                 n2 = int(input("Enter valid second number: "))
#                 if n2 != 0:
#                     break
#         print(f"{n1} {op} {n2} = {n1 / n2}")
#     case _:
#         print("Invalid operator")

# Day 3
# Q1
# student = {"Ali" : [85,95,64], "Ahmad" : [90,77,61], "Arslan" :  [75,50,88]}

# def average(marks):
#     total = 0
#     count = 0
#     for n in marks:
#         total += n
#         count += 1
#     return total/count

# std_avg = [average(student["Ali"]), average(student["Ahmad"]), average(student["Arslan"])]
# count = 0;
# high_avg_std = ""
# for key in student:
#     print(f"{key} : {std_avg[count]}")
#     count += 1
# max_avg = max(std_avg)
# count = 0
# for key in student:
#     if std_avg[count] == max_avg:
#         print(f"Highest Average Student {key} : {std_avg[count]}")
#     count += 1

# Q2
# tasks = []

# def add_tasks(tasks, name):
#     tasks.append({"Task" : name, "Done" : "False"})

# def complete_tasks(tasks, name):
#     for i in tasks:
#         if i["Task"] == name:
#             i["Done"] = "True"
#             print("Task completed Successfully")
#             return 0
#     print("Task Not Found")

# def show_tasks(tasks):
#     for i in tasks:
#         print(i)

# while True:
#     print("1. Add Task, 2. Complete Task, 3. Show Tasks, 0. Exit")
#     ch = int(input("Enter your choice: "))
#     match ch:
#         case 1:
#             task_name = input("Enter Task Name: ")
#             add_tasks(tasks, task_name)
#             print("Added Successfully")
#         case 2:
#             task_name = input("Enter Task Name: ")
#             complete_tasks(tasks, task_name)
#         case 3:
#             show_tasks(tasks)
#         case 0:
#             break
#         case _:
#             print(f"Invalid Input")
