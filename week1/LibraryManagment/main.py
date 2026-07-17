import json
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False
    
class Library:
    def __init__(self):
        self.book_list = []
    
    def add_book(self, title, author):
        self.book_list.append(Book(title, author))
    
    def borrow_book(self, title):
        for b in self.book_list:
            if title == b.title:
                if not b.is_borrowed:
                    b.is_borrowed = True
                    print("Book Borrowed Succesfull")
                else:
                    print("Book Already Booked")
            else:
                print("Book Not Found")
    
    def return_book(self, title):
        for b in self.book_list:
            if title == b.title:
                if b.is_borrowed:
                    b.is_borrowed = False
                    print("Book Returned Succesfull")
                else:
                    print("Book Not Borrowed")
            else:
                print("Book Not Found")
    
    def show_books(self):
        for b in self.book_list:
            print(f"Title: {b.title}, Author: {b.author}, Is_Borrowed: {b.is_borrowed}")

    def save_to_file(self, filename):
        try:
            serializable_books = [b.__dict__ for b in self.book_list]
            with open(filename, "w") as f:
                json.dump(serializable_books, f, indent=4)
            print("Data Saved Successfully")
        except PermissionError:
            print("Unable to save in the file")
    
    def load_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            self.book_list = []
            for item in data:
                book = Book(item['title'], item['author'])
                book.is_borrowed = item['is_borrowed']
                self.book_list.append(book)
                
            print("Data Loaded Successfully")
        except FileNotFoundError:
            print("File Not Found")


print("Library Management System")
lib = Library()
while True:
    try:
        ch = int(input("1. Add Book, 2. Borrow Book, 3. Return Book, 4. Show Books, 5. Save, 6. Load, 0. Exit\nEnter Your Choice: "))
    except ValueError:
        print("Invalid Input")
        continue
    match ch:
        case 1:
            title = input("Enter the Title: ")
            author = input("Enter the Authhor Name: ")
            lib.add_book(title, author)
            print("Book Added Successfully")
        case 2:
            title = input("Enter the Title: ")
            lib.borrow_book(title)
        case 3:
            title = input("Enter the Title: ")
            lib.return_book(title)
        case 4:
            lib.show_books()
        case 5:
            file = input("Enter Filename: ")
            file += ".json"
            lib.save_to_file(file)
        case 6:
            file = input("Enter Filename: ")
            file += ".json"
            lib.load_from_file(file)
        case 0:
            print("GoodBye Thank you for using Library Managment System")
            break
        case _:
            print("Invalid Choice")