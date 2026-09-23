from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit)


app = QApplication( [] )
window = QWidget()

window.setStyleSheet("""
    QWidget {
        background-color: #181818;
    }
""")




window.show()
app.exec_()