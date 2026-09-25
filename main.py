import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton,
    QSplitter, QMessageBox, QGroupBox, QListWidget
)
from PyQt5.QtCore import Qt

try:
    from style import apply_style
except ImportError:
    apply_style = None

ARCHIVO_NOTAS = "notas.json"

class VentanaVerNotas(QWidget):
    def __init__(self):
        super().__init__()
        
        self.notas = self.cargar_notas_desde_archivo()
        self.init_ui()

    def cargar_notas_desde_archivo(self):
        
        if os.path.exists(ARCHIVO_NOTAS):
            try:
                with open(ARCHIVO_NOTAS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        return [
            {
                "titulo": "Escribe un titulo aqui...", 
                "contenido": "Empieza a redactar tu contenido aqui..."
            }
        ]

    def guardar_notas_en_archivo(self):
        try:
            with open(ARCHIVO_NOTAS, "w", encoding="utf-8") as f:
                json.dump(self.notas, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "Error de Guardado", f"No se pudieron guardar los datos: {e}")

    def init_ui(self):
        self.setWindowTitle("Bloc de Notas - Crear y Ver Notas (PyQt5)")
        self.resize(750, 500)

        main_layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        box_mis_notas = QGroupBox("Mis Notas")
        layout_mis_notas = QVBoxLayout()

        self.lista_notas = QListWidget()
        self.lista_notas.currentRowChanged.connect(self.cargar_nota_seleccionada)
        layout_mis_notas.addWidget(self.lista_notas)

        self.btn_nueva = QPushButton("+ Nueva Nota")
        self.btn_nueva.setStyleSheet("padding: 8px; font-weight: bold;")
        self.btn_nueva.clicked.connect(self.preparar_nueva_nota)
        layout_mis_notas.addWidget(self.btn_nueva)

        box_mis_notas.setLayout(layout_mis_notas)
        splitter.addWidget(box_mis_notas)

        box_editor = QGroupBox("Editor de Nota")
        layout_editor = QVBoxLayout()

        layout_editor.addWidget(QLabel("Título:"))
        self.input_titulo = QLineEdit()
        self.input_titulo.setPlaceholderText("Escribe un titulo aqui...")
        layout_editor.addWidget(self.input_titulo)

        layout_editor.addWidget(QLabel("Contenido:"))
        self.input_contenido = QTextEdit()
        self.input_contenido.setPlaceholderText("Empieza a redactar tu contenido aqui...")
        layout_editor.addWidget(self.input_contenido)

        
        layout_botones = QHBoxLayout()

        self.btn_guardar = QPushButton("Guardar / Actualizar Nota")
        self.btn_guardar.setStyleSheet("""
        QPushButton {
            background-color: #728ADA;
            color: white;
            font-weight: bold;
            padding: 8px;
            border: none;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #233685;
        }
    """)
        self.btn_guardar.clicked.connect(self.guardar_nota)
        layout_botones.addWidget(self.btn_guardar)

        self.btn_eliminar = QPushButton("Eliminar Nota")
        self.btn_eliminar.setStyleSheet("""
        QPushButton {
            background-color: #d9534f;
            color: white;
            font-weight: bold;
            padding: 8px;
            border: none;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #610A10;
        }
    """)
        self.btn_eliminar.clicked.connect(self.eliminar_nota)
        layout_botones.addWidget(self.btn_eliminar)

        layout_editor.addLayout(layout_botones)

        box_editor.setLayout(layout_editor)
        splitter.addWidget(box_editor)

        splitter.setSizes([220, 530])
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

        self.actualizar_lista_notas()
        if self.notas:
            self.lista_notas.setCurrentRow(0)

    def actualizar_lista_notas(self):
        
        self.lista_notas.blockSignals(True)
        self.lista_notas.clear()
        for nota in self.notas:
            self.lista_notas.addItem(nota["titulo"])
        self.lista_notas.blockSignals(False)

    def cargar_nota_seleccionada(self, index):
        if 0 <= index < len(self.notas):
            nota = self.notas[index]
            self.input_titulo.setText(nota["titulo"])
            self.input_contenido.setText(nota["contenido"])

    def preparar_nueva_nota(self):
        self.lista_notas.setCurrentRow(-1)
        self.input_titulo.clear()
        self.input_contenido.clear()
        self.input_titulo.setFocus()

    def guardar_nota(self):
        titulo = self.input_titulo.text().strip()
        contenido = self.input_contenido.toPlainText().strip()

        if not titulo or not contenido:
            QMessageBox.warning(self, "Campos vacíos", "Por favor ingresa tanto el título como el contenido de la nota.")
            return

        indice_seleccionado = self.lista_notas.currentRow()

        if 0 <= indice_seleccionado < len(self.notas):
            self.notas[indice_seleccionado] = {"titulo": titulo, "contenido": contenido}
        else:
            nueva_nota = {"titulo": titulo, "contenido": contenido}
            self.notas.append(nueva_nota)
            indice_seleccionado = len(self.notas) - 1

        self.guardar_notas_en_archivo()
        self.actualizar_lista_notas()
        self.lista_notas.setCurrentRow(indice_seleccionado)

        QMessageBox.information(self, "¡Éxito!", "La nota ha sido guardada correctamente.")

    def eliminar_nota(self):
        indice = self.lista_notas.currentRow()

        if indice < 0 or indice >= len(self.notas):
            QMessageBox.warning(self, "Atención", "Selecciona una nota de la lista para eliminar.")
            return

        nota_actual = self.notas[indice]

        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar la nota '{nota_actual['titulo']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            self.notas.pop(indice)
            self.guardar_notas_en_archivo()
            self.actualizar_lista_notas()

            if self.notas:
                nuevo_indice = max(0, indice - 1)
                self.lista_notas.setCurrentRow(nuevo_indice)
            else:
                self.preparar_nueva_nota()

            QMessageBox.information(self, "Eliminado", "La nota ha sido eliminada correctamente.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaVerNotas()
    apply_style(app)
    ventana.show()
    sys.exit(app.exec_())