import sqlite3

DB_NAME = "university.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        major TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        instructor TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(course_id) REFERENCES courses(course_id)
    );
    """)

    conn.commit()
    conn.close()


# -----------------------------
# ОПЕРАЦІЇ ЗІ СТУДЕНТАМИ
# -----------------------------
def add_student():
    name = input("Ім'я студента: ")
    age = int(input("Вік студента: "))
    major = input("Спеціальність: ")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
    conn.commit()
    conn.close()
    print("Студента додано!\n")

def view_students():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()

    print("\n--- СПИСОК СТУДЕНТІВ ---")
    for r in rows:
        print(r)
    print()


def edit_student():
    student_id = input("Введіть ID студента для редагування: ")

    new_name = input("Нове ім'я (або Enter, щоб не змінювати): ")
    new_age = input("Новий вік (або Enter): ")
    new_major = input("Нова спеціальність (або Enter): ")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if new_name:
        cur.execute("UPDATE students SET name=? WHERE id=?", (new_name, student_id))
    if new_age:
        cur.execute("UPDATE students SET age=? WHERE id=?", (new_age, student_id))
    if new_major:
        cur.execute("UPDATE students SET major=? WHERE id=?", (new_major, student_id))

    conn.commit()
    conn.close()
    print("Дані оновлено!\n")


# -----------------------------
# ОПЕРАЦІЇ З КУРСАМИ
# -----------------------------
def add_course():
    course_name = input("Назва курсу: ")
    instructor = input("Викладач: ")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (course_name, instructor))
    conn.commit()
    conn.close()
    print("Курс додано!\n")

def view_courses():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    conn.close()

    print("\n--- СПИСОК КУРСІВ ---")
    for r in rows:
        print(r)
    print()


# -----------------------------
# MANY-TO-MANY: реєстрація студентів на курси
# -----------------------------
def register_student_to_course():
    student_id = input("ID студента: ")
    course_id = input("ID курсу: ")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
    conn.commit()
    conn.close()
    print("Студента зареєстровано на курс!\n")


def view_students_in_course():
    course_id = input("Введіть ID курсу: ")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT students.id, students.name, students.major
        FROM students
        JOIN student_courses ON students.id = student_courses.student_id
        WHERE student_courses.course_id = ?
    """, (course_id,))

    rows = cur.fetchall()
    conn.close()

    print("\n--- СТУДЕНТИ НА КУРСІ ---")
    for r in rows:
        print(r)
    print()


# -----------------------------
# МЕНЮ
# -----------------------------
def menu():
    init_db()

    while True:
        print("""
1. Додати студента
2. Переглянути студентів
3. Редагувати студента
4. Додати курс
5. Переглянути курси
6. Зареєструвати студента на курс
7. Показати студентів курсу
0. Вихід
""")

        choice = input("Ваш вибір: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            edit_student()
        elif choice == "4":
            add_course()
        elif choice == "5":
            view_courses()
        elif choice == "6":
            register_student_to_course()
        elif choice == "7":
            view_students_in_course()
        elif choice == "0":
            print("Вихід...")
            break
        else:
            print("Невірний вибір, спробуйте ще.\n")


if __name__ == "__main__":
    menu()
