def stylesheet():
    return """
        
        QWidget {
            background-color: #1e1e2e;
            color: #cdd6f4;
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
        }

        QGroupBox {
            border: 1px solid #45475a;
            border-radius: 8px;
            margin-top: 12px;
            font-weight: bold;
            color: #89b4fa;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
        }

        QLineEdit, QTextEdit, QComboBox {
            background-color: #313244;
            border: 1px solid #45475a;
            border-radius: 6px;
            padding: 6px;
            color: #cdd6f4;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border: 1px solid #89b4fa;
        }

        /* Menú desplegable (QComboBox) */
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        QComboBox QAbstractItemView {
            background-color: #313244;
            color: #cdd6f4;
            selection-background-color: #45475a;
        }

        /* Botones generales */
        QPushButton {
            background-color: #45475a;
            color: #cdd6f4;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #585b70;
        }
        QPushButton:pressed {
            background-color: #313244;
        }

        /* Separador entre paneles */
        QSplitter::handle {
            background-color: #181825;
        }
    """

def apply_style(app_o_widget):
    app_o_widget.setStyleSheet(stylesheet())