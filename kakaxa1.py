from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QCheckBox, QSlider, QMessageBox, QListWidget
from random import choice, sample, randint, shuffle
from PyQt5.QtGui import QIcon, QImage, QPainter

app = QApplication([]) 
mw = QWidget() 
mw.setWindowTitle('Генератор паролів') 
mw.resize(450, 400) 
mw.setWindowIcon(QIcon("mmbth.ico"))

layout = QVBoxLayout()

background_image = QImage("pexels-lilartsy-1213447.jpg")

def pain_event(event):
    painter = QPainter(mw)
    painter.drawImage(mw.rect(), background_image)

mw.paintEvent = pain_event

lgh = QLabel("Виберіть довжину пароля:")
layout.addWidget(lgh)

slider = QSlider(Qt.Horizontal)
slider.setMinimum(4)
slider.setMaximum(48)
slider.setValue(12)
layout.addWidget(slider)

length_label = QLabel("Довжина: 12")
layout.addWidget(length_label)

def update_length_label(value):
    length_label.setText(f"Довжина: {value}")

slider.valueChanged.connect(update_length_label)


check_digits = QCheckBox("Використовувати цифри")
check_digits.setStyleSheet("color: white; font: bold;")
check_lower = QCheckBox("Використовувати малі літери")
check_upper = QCheckBox("Використовувати великі літери")
check_special = QCheckBox("Використовувати спеціальні символи")
check_spaces = QCheckBox("Дозволити пробіли")
layout.addWidget(check_digits)
layout.addWidget(check_lower)
layout.addWidget(check_upper)
layout.addWidget(check_special)
layout.addWidget(check_spaces)


check_unique = QCheckBox("Без дублікатів символів")
layout.addWidget(check_unique)


generate_button = QPushButton("Згенерувати пароль")
layout.addWidget(generate_button)


password_label = QLabel("Пароль:")
layout.addWidget(password_label)

password_list = QListWidget()
layout.addWidget(password_list)

def generate_password():
    length = slider.value()
    characters = ""
    
    if check_digits.isChecked():
        characters += "0123456789"
    if check_lower.isChecked():
        characters += "abcdefghijklmnopqrstuvwxyz"
    if check_upper.isChecked():
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if check_special.isChecked():
        characters += "!@#$%^&*()-_=+[]{}|;:,.<>?/"
    if check_spaces.isChecked():
        characters += " "
    
    if not characters:
        QMessageBox.warning(mw, "Помилка", "Будь ласка, виберіть хоча б один набір символів!")
        return

    if check_unique.isChecked() and length > len(characters):
        QMessageBox.warning(mw, "Помилка", "Довжина пароля не може бути більшою за кількість унікальних символів!")
        return

    if check_unique.isChecked():
        password = ''.join(sample(characters, length))
    else:
        password = ''.join(choice(characters) for _ in range(length))


    password_chars = list(password)
    if check_lower.isChecked() and check_upper.isChecked():
        for i in range(length):
            if randint(0, 1):
                password_chars[i] = password_chars[i].lower()
            else:
                password_chars[i] = password_chars[i].upper()
    elif check_upper.isChecked():
        password_chars = [c.upper() if randint(0, 1) else c for c in password_chars]
    
    shuffle(password_chars)  
    final_password = ''.join(password_chars)
    
    password_label.setText(f"Пароль: {final_password}")
    password_list.addItem(final_password)  

generate_button.clicked.connect(generate_password)

mw.setLayout(layout) 
mw.show() 
app.exec_()