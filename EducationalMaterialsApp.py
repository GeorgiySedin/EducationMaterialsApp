import sys
import sqlite3
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDateTime

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            registration_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY,
            category TEXT,
            name TEXT,
            material_type TEXT,
            creation_date TEXT,
            author TEXT
        )
    ''')
    conn.commit()
    conn.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор роли")
        self.setGeometry(650, 300, 300, 150)
        layout = QVBoxLayout()
        self.label = QLabel("Выберите роль:")
        layout.addWidget(self.label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Администратор", "Преподаватель", "Студент"])
        layout.addWidget(self.role_combo)
        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.open_login_window)
        layout.addWidget(self.next_button)
        self.setLayout(layout)
        self.setStyleSheet('background: rgb(135, 206, 250);')
        self.next_button.setStyleSheet('background: rgb(218, 165, 32);')
        self.role_combo.setStyleSheet('background: rgb(218, 165, 32);')

    def open_login_window(self):
        role = self.role_combo.currentText()
        self.login_window = LoginWindow(role)
        self.login_window.show()
        self.close()

class LoginWindow(QWidget):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setWindowTitle("Логин")
        self.setGeometry(650, 300, 300, 150)
        layout = QVBoxLayout()
        self.label = QLabel(f"Вход для {role}")
        layout.addWidget(self.label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)
        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.open_registration_window)
        layout.addWidget(self.register_button)
        self.setLayout(layout)
        self.setStyleSheet('background: rgb(135, 206, 250);')
        self.username_input.setStyleSheet('background: rgb(218, 165, 32);')
        self.register_button.setStyleSheet('background: rgb(218, 165, 32);')
        self.password_input.setStyleSheet('background: rgb(218, 165, 32);')
        self.login_button.setStyleSheet('background: rgb(218, 165, 32);')

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        if result:
            if result[0] == "Студент":
                self.student_window = StudentWindow(username)
                self.student_window.show()
            elif result[0] == "Преподаватель":
                self.teacher_window = TeacherWindow(username)
                self.teacher_window.show()
            elif result[0] == "Администратор":
                self.admin_window = AdminWindow(username)
                self.admin_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные логин или пароль.")
        conn.close()

    def open_registration_window(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(650, 300, 300, 150)
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Студент", "Преподаватель", "Администратор"])
        layout.addWidget(self.role_combo)
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)
        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)
        self.setLayout(layout)
        self.setStyleSheet('background: rgb(135, 206, 250);')
        self.username_input.setStyleSheet('background: rgb(218, 165, 32);')
        self.register_button.setStyleSheet('background: rgb(218, 165, 32);')
        self.password_input.setStyleSheet('background: rgb(218, 165, 32);')
        self.role_combo.setStyleSheet('background: rgb(218, 165, 32);')
        self.logout_button.setStyleSheet('background: rgb(255, 70, 70);')

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()
        registration_date = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role, registration_date) VALUES (?, ?, ?, ?)",
                           (username, password, role, registration_date))
            conn.commit()
            QMessageBox.information(self, "Успех", "Пользователь успешно зарегистрирован.")
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует.")
        conn.close()

    def logout(self):
        self.login_window = MainWindow()
        self.login_window.show()
        self.close()

class AdminWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Панель администратора")
        self.setGeometry(650, 300, 300, 150)
        layout = QVBoxLayout()
        label = QLabel("Панель администратора")
        layout.addWidget(label)
        users_label = QLabel("Список пользователей:")
        layout.addWidget(users_label)
        self.users_list = QListWidget()
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, registration_date FROM users")
        users = cursor.fetchall()
        for user in users:
            self.users_list.addItem(f"{user[0]} (Дата регистрации: {user[1]})")
        conn.close()
        layout.addWidget(self.users_list)
        self.delete_user_button = QPushButton("Удалить выбранного пользователя")
        self.delete_user_button.clicked.connect(self.delete_user)
        layout.addWidget(self.delete_user_button)
        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)
        self.setLayout(layout)
        self.setStyleSheet('background: rgb(135, 206, 250);')
        self.users_list.setStyleSheet('background: rgb(175, 238, 238);')
        self.delete_user_button.setStyleSheet('background: rgb(218, 165, 32);')
        self.logout_button.setStyleSheet('background: rgb(255, 70, 70);')

    def delete_user(self):
        selected_items = self.users_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            user_info = item.text()
            username = user_info.split(" (")[0]  # Извлекаем имя пользователя
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Удаление пользователя", f"Пользователь {username} удален. Время удаления: {QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')}.")
            self.users_list.takeItem(self.users_list.row(item))

    def logout(self):
        self.login_window = MainWindow()
        self.login_window.show()
        self.close()

class TeacherWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Преподаватель")
        self.setGeometry(650, 300, 300, 150)
        layout = QVBoxLayout()
        self.label = QLabel("Добавить новый учебный материал:")
        self.material_name_input = QLineEdit()
        self.material_name_input.setPlaceholderText("Введите название материала")
        self.material_category_input = QLineEdit()
        self.material_category_input.setPlaceholderText("Введите категорию материала")
        self.material_type_input = QLineEdit()
        self.material_type_input.setPlaceholderText("Введите тип материала")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Введите имя автора")
        self.add_material_button = QPushButton("Добавить материал")
        self.add_material_button.clicked.connect(self.add_material)
        layout.addWidget(self.label)
        layout.addWidget(self.material_name_input)
        layout.addWidget(self.material_category_input)
        layout.addWidget(self.material_type_input)
        layout.addWidget(self.author_input)
        layout.addWidget(self.add_material_button)
        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)
        self.setStyleSheet('background: rgb(135, 206, 250);')
        self.material_name_input.setStyleSheet('background: rgb(175, 238, 238);')
        self.material_category_input.setStyleSheet('background: rgb(175, 238, 238);')
        self.material_type_input.setStyleSheet('background: rgb(175, 238, 238);')
        self.author_input.setStyleSheet('background: rgb(175, 238, 238);')
        self.add_material_button.setStyleSheet('background: rgb(218, 165, 32);')
        self.logout_button.setStyleSheet('background: rgb(255, 70, 70);')
        self.setLayout(layout)

    def add_material(self):
        name = self.material_name_input.text()
        category = self.material_category_input.text()
        material_type = self.material_type_input.text()
        creation_date = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        author = self.author_input.text()

        if not name or not category or not material_type or not author:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO materials (category, name, material_type, creation_date, author) VALUES (?, ?, ?, ?, ?)",
            (category, name, material_type, creation_date, author)
        )
        connection.commit()
        connection.close()
        QMessageBox.information(self, "Успех", "Материал успешно добавлен.")
        self.material_name_input.clear()
        self.material_category_input.clear()
        self.material_type_input.clear()
        self.author_input.clear()

    def logout(self):
        self.login_window = MainWindow()
        self.login_window.show()
        self.close()

class StudentWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Студент")
        self.setGeometry(650, 300, 300, 150)
        layout = QVBoxLayout()
        self.label = QLabel("Выберите категорию учебного материала:")
        self.category_selector = QComboBox()
        self.category_selector.addItems(["Химия", "Математика", "Литература"])
        self.view_materials_button = QPushButton("Просмотр материалов")
        self.view_materials_button.clicked.connect(self.view_materials)
        layout.addWidget(self.label)
        layout.addWidget(self.category_selector)
        layout.addWidget(self.view_materials_button)
        self.setLayout(layout)
        self.faq_button = QPushButton("FAQ")
        self.faq_button.clicked.connect(self.open_faq_window)
        self.comments_button = QPushButton("Комментарии")
        self.comments_button.clicked.connect(self.open_comments_window)
        layout.addWidget(self.faq_button)
        layout.addWidget(self.comments_button)
        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)
        self.setStyleSheet('background: rgb(135, 206, 250);')
        self.category_selector.setStyleSheet('background: rgb(175, 238, 238);')
        self.view_materials_button.setStyleSheet('background: rgb(218, 165, 32);')
        self.faq_button.setStyleSheet('background: rgb(218, 165, 32);')
        self.comments_button.setStyleSheet('background: rgb(218, 165, 32);')
        self.logout_button.setStyleSheet('background: rgb(255, 70, 70);')
        self.setLayout(layout)

    def open_faq_window(self):
        faq_window = FAQWindow()
        faq_window.exec()

    def open_comments_window(self):
        comments_window = CommentsWindow()
        comments_window.exec()

    def view_materials(self):
        selected_category = self.category_selector.currentText()
        connection = sqlite3.connect("users.db")  # Используем ту же базу, что и при добавлении материала
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM materials WHERE category=?", (selected_category,))
        materials = cursor.fetchall()
        connection.close()
        material_list = "\n".join([f"{m[2]} - {m[3]} (Автор: {m[5]}, Дата: {m[4]})" for m in materials])
        QMessageBox.information(self, "Материалы",
                                f"Материалы для категории '{selected_category}':\n{material_list if material_list else 'Нет материалов.'}")

    def logout(self):
        self.login_window = MainWindow()
        self.login_window.show()
        self.close()

class CommentsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Комментарии к материалам")
        self.setGeometry(650, 300, 300, 150)
        layout = QVBoxLayout()
        self.comment_input = QTextEdit()
        self.comment_input.setPlaceholderText("Введите ваш комментарий...")
        self.comments_list = QListWidget()
        submit_button = QPushButton("Отправить комментарий")
        submit_button.clicked.connect(self.submit_comment)
        layout.addWidget(self.comment_input)
        layout.addWidget(submit_button)
        layout.addWidget(self.comments_list)
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        self.setLayout(layout)

    def submit_comment(self):
        comment_text = self.comment_input.toPlainText().strip()
        if comment_text:
            self.comments_list.addItem(comment_text)
            self.comment_input.clear()

class FAQWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно часто задаваемых вопросов")
        self.setGeometry(650, 300, 300, 150)
        layout = QVBoxLayout()
        faq_items = {
            "Как зарегистрироваться?": "Чтобы зарегистрироваться, нажмите на кнопку 'Регистрация' на экране входа.",
            "Как восстановить пароль?": "Если вы забыли пароль, свяжитесь с администратором.",
            "Как оставить комментарий?": "Выберите материал и нажмите на кнопку 'Комментарии'."
        }
        for question, answer in faq_items.items():
            layout.addWidget(QLabel(f"<b>{question}</b>: {answer}"))
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        self.setLayout(layout)

if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


