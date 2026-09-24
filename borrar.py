def eliminar_nota(self):

        if not self.notas:
            QMessageBox.warning(self, "No hay nada que elminiar")
            return

        indice = self.combo_notas.currentIndex()
        if index_valido := (0 <= indice < len(self.notas)):
            nota_actual = self.notas[indice]

            # Por si hacen missclick
            respuesta = QMessageBox.question(
                self, 
                "Confirmar eliminación", 
                f"¿Estás seguro de que quieres eliminar la nota '{nota_actual['titulo']}'?",
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                self.notas.pop(indice)
                self.input_titulo.clear()
                self.input_contenido.clear()
                

                self.actualizar_combo_notas()

                QMessageBox.information(self, "La nota se ha eliminado correctamente.")