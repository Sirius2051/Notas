import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, 
    QSplitter, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt


class VentanaVerNotas(QWidget):
    def __init__(self):
        super().__init__()
        # Lista en memoria para almacenar las notas guardadas
        self.notas = [
            {"titulo": "Nota de ejemplo", "contenido": "Esta es una nota que viene por defecto."}
        ]
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Bloc de Notas - Crear y Ver Notas (PyQt5)")
        self.resize(750, 500)

        # Layout Principal
        main_layout = QVBoxLayout()

        # Título principal
        lbl_titulo_app = QLabel("📝 Gestor de Notas")
        lbl_titulo_app.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 5px;")
        main_layout.addWidget(lbl_titulo_app)

        # Panel dividido en dos columnas (Crear Nota a la Izquierda | Ver Nota a la Derecha)
        splitter = QSplitter(Qt.Horizontal)

        # ==========================================
        # COLUMNA IZQUIERDA: CREAR Y GUARDAR NOTAS
        # ==========================================
        box_crear = QGroupBox("Crear Nueva Nota")
        layout_crear = QVBoxLayout()

        layout_crear.addWidget(QLabel("Título:"))
        self.input_titulo = QLineEdit()
        self.input_titulo.setPlaceholderText("Escribe el título aquí...")
        layout_crear.addWidget(self.input_titulo)

        layout_crear.addWidget(QLabel("Contenido:"))
        self.input_contenido = QTextEdit()
        self.input_contenido.setPlaceholderText("Escribe el texto de la nota...")
        layout_crear.addWidget(self.input_contenido)

        # Botón para GUARDAR la nota
        self.btn_guardar = QPushButton("💾 Guardar Nota")
        self.btn_guardar.setStyleSheet("background-color: #2b78e4; color: white; font-weight: bold; padding: 6px;")
        self.btn_guardar.clicked.connect(self.guardar_nota)
        layout_crear.addWidget(self.btn_guardar)

        box_crear.setLayout(layout_crear)
        splitter.addWidget(box_crear)

        # ==========================================
        # COLUMNA DERECHA: APARTADO "VER NOTAS"
        # ==========================================
        box_ver = QGroupBox("Ver Notas Guardadas")
        layout_ver = QVBoxLayout()

        layout_ver.addWidget(QLabel("Selecciona una nota para leer:"))
        
        # Desplegable (Menú/Selector) con los títulos
        self.combo_notas = QComboBox()
        self.combo_notas.currentIndexChanged.connect(self.mostrar_contenido_nota)
        layout_ver.addWidget(self.combo_notas)

        # Área de solo lectura para visualizar el contenido
        self.visor_contenido = QTextEdit()
        self.visor_contenido.setReadOnly(True)
        self.visor_contenido.setPlaceholderText("El contenido de la nota aparecerá aquí...")
        layout_ver.addWidget(self.visor_contenido)

        box_ver.setLayout(layout_ver)
        splitter.addWidget(box_ver)

        # Ajustar proporciones de la ventana (50% cada lado)
        splitter.setSizes([375, 375])
        main_layout.addWidget(splitter)

        # Botón inferior para volver al menú general (útil para tu proyecto en grupo)
        self.btn_volver = QPushButton("Volver al Menú Principal")
        main_layout.addWidget(self.btn_volver)

        # Cargar las notas iniciales en el menú desplegable
        self.actualizar_combo_notas()

        self.setLayout(main_layout)

    def guardar_nota(self):
        """Lee los campos de entrada, valida y guarda la nota en la lista."""
        titulo = self.input_titulo.text().strip()
        contenido = self.input_contenido.toPlainText().strip()

        # Validación sencilla
        if not titulo or not contenido:
            QMessageBox.warning(self, "Campos vacíos", "Por favor ingresa tanto el título como el contenido de la nota.")
            return

        # Añadir la nueva nota a nuestra lista
        nueva_nota = {"titulo": titulo, "contenido": contenido}
        self.notas.append(nueva_nota)

        # Limpiar los campos para volver a escribir
        self.input_titulo.clear()
        self.input_contenido.clear()

        # Actualizar la lista en el menú de "Ver Notas"
        self.actualizar_combo_notas()

        # Seleccionar automáticamente la nota recién guardada
        self.combo_notas.setCurrentIndex(len(self.notas) - 1)

        QMessageBox.information(self, "¡Éxito!", "La nota ha sido guardada correctamente.")

    def actualizar_combo_notas(self):
        """Actualiza las opciones del desplegable con los títulos guardados."""
        self.combo_notas.clear()
        if not self.notas:
            self.combo_notas.addItem("No hay notas disponibles")
            return

        for nota in self.notas:
            self.combo_notas.addItem(nota["titulo"])

    def mostrar_contenido_nota(self, index):
        """Muestra el contenido de la nota seleccionada en el combo."""
        if index >= 0 and index < len(self.notas):
            nota = self.notas[index]
            texto_formateado = f"=== {nota['titulo']} ===\n\n{nota['contenido']}"
            self.visor_contenido.setText(texto_formateado)
        else:
            self.visor_contenido.clear()


# --- CÓDIGO DE PRUEBA ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaVerNotas()
    ventana.show()
    sys.exit(app.exec_())