from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QAbstractScrollArea
import mysql.connector
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Chapitres abordés cette semaine')
        self.setGeometry(100, 100, 800, 600)

        self.table = QTableWidget()
        self.setCentralWidget(self.table)

        # Connexion à la base de données
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ecole"
        )
        self.cursor = self.conn.cursor()

        # Navigation buttons
        self.btn_prev_week = QPushButton("Previous Week")
        self.btn_next_week = QPushButton("Next Week")
        self.btn_prev_week.clicked.connect(self.load_prev_week)
        self.btn_next_week.clicked.connect(self.load_next_week)

        # Layout for navigation buttons
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn_prev_week)
        self.layout.addWidget(self.btn_next_week)
        self.layout.addWidget(self.table)

        # Initialize week number
        self.current_week = 1

        self.load_data()

    def load_data(self):
        # SQL query to fetch data for the current week
        query = f"""
           SELECT 
    date,
    jour,
    matiere.nom AS matiere,
    contenu,
    cours_a_eu_lieu
        FROM CahierDeTexte
        JOIN Matiere ON CahierDeTexte.matiere_id = Matiere.id
        WHERE jour IN ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi')
        ORDER BY date, jour;
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Configure the table to display the data
        self.table.setColumnCount(5)
        self.table.setRowCount(len(rows) + 1)
        total_cours = len(rows)

        headers = ['Date', 'Jour', 'Matière', 'Contenu', 'Cours a eu lieu']
        self.table.setHorizontalHeaderLabels(headers)

        cours_rates = 0
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                if j == 4:
                    item.setText("✅" if value else "❌")
                    cours_rates += 1 if not value else 0
                self.table.setItem(i, j, item)

        total_item = QTableWidgetItem(f"Cours ratés : {cours_rates}/{total_cours}")
        self.table.setItem(len(rows), 0, total_item)

        # Adjust the table size to fit its contents
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.resizeColumnsToContents()

    def load_prev_week(self):
        self.current_week -= 1
        self.load_data()

    def load_next_week(self):
        self.current_week += 1
        self.load_data()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
