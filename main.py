import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, 
    QPushButton, QListWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QTableWidget, QHeaderView, QAbstractItemView
)

class BlocDeNotas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Bloc de Notas")
        self.resize(850, 480)
        self.setStyleSheet("background-color: white;")
        
        self.notas_guardadas = {}
        self.contador_notas = 1
        self.nota_actual_titulo = None
        
        # Estructura principal: Tabla de 1 fila y 2 columnas (Texto | Barra Lateral)
        self.tabla_layout = QTableWidget(1, 2, self)
        self.tabla_layout.setShowGrid(False)
        self.tabla_layout.horizontalHeader().setVisible(False)
        self.tabla_layout.verticalHeader().setVisible(False)
        self.tabla_layout.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabla_layout.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.tabla_layout.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_layout.setColumnWidth(1, 240)  # Ancho fijo para la barra lateral
        self.tabla_layout.verticalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(5, 5, 5, 5)
        layout_principal.addWidget(self.tabla_layout)

        # -------------------------------------------------------------
        # 1. PANEL IZQUIERDO (Editor de texto)
        # -------------------------------------------------------------
        widget_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout(widget_izquierdo)
        
        self.area_texto = QTextEdit()
        self.area_texto.setPlaceholderText("Escribe tu nota aquí...")
        self.area_texto.setStyleSheet("background-color: white; color: black; border: 1px solid #ccc; font-size: 14px;")
        
        self.boton_guardar = QPushButton("Guardar Nota")
        self.boton_guardar.setStyleSheet("""
            QPushButton {
                background-color: #007bff; 
                color: white; 
                border: none; 
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.boton_guardar.clicked.connect(self.guardar_nota)
        
        layout_izquierdo.addWidget(self.area_texto)
        layout_izquierdo.addWidget(self.boton_guardar)

        # -------------------------------------------------------------
        # 2. PANEL DERECHO (Barra Lateral de Notas)
        # -------------------------------------------------------------
        widget_derecho = QWidget()
        layout_derecho = QVBoxLayout(widget_derecho)
        
        etiqueta_barra = QLabel("Notas Guardadas")
        etiqueta_barra.setStyleSheet("color: black; font-weight: bold; font-size: 14px;")
        
        # Botón para crear nueva nota limpia
        self.boton_nueva = QPushButton("+ Nueva Nota")
        self.boton_nueva.setStyleSheet("""
            QPushButton {
                background-color: #28a745; 
                color: white; 
                border: none; 
                padding: 6px;
                font-weight: bold;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.boton_nueva.clicked.connect(self.nueva_nota)

        # Lista lateral donde se muestran las notas
        self.lista_notas = QListWidget()
        self.lista_notas.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa; 
                color: black; 
                border: 1px solid #ccc;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 6px;
            }
            QListWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
        """)
        self.lista_notas.itemClicked.connect(self.cargar_nota)
        
        # Botón para eliminar la nota seleccionada
        self.boton_eliminar = QPushButton("Eliminar Nota")
        self.boton_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #dc3545; 
                color: white; 
                border: none; 
                padding: 6px;
                font-weight: bold;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.boton_eliminar.clicked.connect(self.eliminar_nota)

        layout_derecho.addWidget(etiqueta_barra)
        layout_derecho.addWidget(self.boton_nueva)
        layout_derecho.addWidget(self.lista_notas)
        layout_derecho.addWidget(self.boton_eliminar)

        # Ubicar ambos paneles en la tabla
        self.tabla_layout.setCellWidget(0, 0, widget_izquierdo)
        self.tabla_layout.setCellWidget(0, 1, widget_derecho)

    def guardar_nota(self):
        contenido = self.area_texto.toPlainText().strip()
        if not contenido:
            return
            
        # Generar título basado en la primera línea
        lineas = contenido.split("\n")
        titulo_base = lineas[0].strip()
        if len(titulo_base) > 20:
            titulo_base = titulo_base[:20] + "..."
            
        if not titulo_base:
            titulo_base = f"Nota {self.contador_notas}"
            self.contador_notas += 1

        # Si estamos editando una nota cargada anteriormente
        if self.nota_actual_titulo and self.nota_actual_titulo in self.notas_guardadas:
            del self.notas_guardadas[self.nota_actual_titulo]
            # Eliminar item anterior de la lista
            items = self.lista_notas.findItems(self.nota_actual_titulo, sys.modules['PyQt5.QtCore'].Qt.MatchExactly)
            for item in items:
                self.lista_notas.takeItem(self.lista_notas.row(item))

        # Evitar títulos duplicados
        titulo_definitivo = titulo_base
        version = 1
        while titulo_definitivo in self.notas_guardadas:
            titulo_definitivo = f"{titulo_base} ({version})"
            version += 1
            
        self.notas_guardadas[titulo_definitivo] = contenido
        self.lista_notas.addItem(titulo_definitivo)
        self.nota_actual_titulo = titulo_definitivo

    def cargar_nota(self, elemento):
        titulo_seleccionado = elemento.text()
        if titulo_seleccionado in self.notas_guardadas:
            self.area_texto.setText(self.notas_guardadas[titulo_seleccionado])
            self.nota_actual_titulo = titulo_seleccionado

    def nueva_nota(self):
        self.area_texto.clear()
        self.nota_actual_titulo = None
        self.lista_notas.clearSelection()

    def eliminar_nota(self):
        item_actual = self.lista_notas.currentItem()
        if item_actual:
            titulo = item_actual.text()
            if titulo in self.notas_guardadas:
                del self.notas_guardadas[titulo]
            self.lista_notas.takeItem(self.lista_notas.row(item_actual))
            self.nueva_nota()

# Ejecución
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

ventana = BlocDeNotas()
ventana.show()