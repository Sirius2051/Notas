from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                            QTextEdit, QHBoxLayout, QVBoxLayout, QPushButton)
from PyQt5.QtCore import Qt

app = QApplication( [] )
window = QWidget()
window.resize(1000, 900)
window.setWindowTitle("Editor de Notas")


texto = QTextEdit()
texto.setPlaceholderText("Empieza a redactar tu contenido...")
texto.setStyleSheet("""
    QTextEdit{
        color: #E0F2FE;
        selection-background-color: #057B9E;
        font-size: 15px;
        
        border: 2px solid #444444;
        border-radius: 8px;
        padding: 10px 20px
    }
    QTextEdit:focus {
        border: 1px solid #00B4D8;
        background-color: #08232C;
    }
""")

title = QLineEdit()
title.setPlaceholderText("Escribe un título aquí...")
title.setStyleSheet("""
    QLineEdit{
        color: #E0F2FE;
        height: 20px;
        font-size: 15px;
        font-family Arial;
        border: 2px solid #444444;
        border-radius: 8px;
    }
    QLineEdit:focus {
        border: 1px solid #00B4D8;
        background-color: #08232C;
    }
""")


button1 = QPushButton("Guardar")
button1.setStyleSheet("""
    QPushButton{
        color: #011319;
        background-color:#00B4D8;
        border-radius: 10px;
        border: none;
        padding: 8px 16px;
    }

    QPushButton:hover{
        background-color:#48CAE4;
    }

    QPushButton:pressed{
        background-color:#0077B6;
    }
""")

window.setStyleSheet("""
    QWidget {
        background-color: #011319;
    }
""")


layout = QHBoxLayout()
layoutV = QVBoxLayout()
layoutV2 = QVBoxLayout()


layoutV2.addWidget(button1, alignment=Qt.AlignTop)
layoutV.addWidget(title, alignment=Qt.AlignTop)
layoutV.addWidget(texto)
layout.addLayout(layoutV)
layout.addLayout(layoutV2)
window.setLayout(layout)



window.show()
app.exec_()