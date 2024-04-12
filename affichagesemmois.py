from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import mysql.connector
import datetime

class CahierDeTexteViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Affichage du Cahier de Texte')
        self.layout = QVBoxLayout()
        
        # Boutons de navigation pour les semaines
        self.btn_semaine_precedente = QPushButton('Semaine précédente')
        self.btn_semaine_precedente.clicked.connect(self.afficher_semaine_precedente)
        self.layout.addWidget(self.btn_semaine_precedente)

        self.btn_semaine_suivante = QPushButton('Semaine suivante')
        self.btn_semaine_suivante.clicked.connect(self.afficher_semaine_suivante)
        self.layout.addWidget(self.btn_semaine_suivante)

        # Boutons de navigation pour les mois
        self.btn_mois_precedent = QPushButton('Mois précédent')
        self.btn_mois_precedent.clicked.connect(self.afficher_mois_precedent)
        self.layout.addWidget(self.btn_mois_precedent)

        self.btn_mois_suivant = QPushButton('Mois suivant')
        self.btn_mois_suivant.clicked.connect(self.afficher_mois_suivant)
        self.layout.addWidget(self.btn_mois_suivant)

        # Tableau pour afficher les cours
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)

        # Connexion à la base de données
        self.conn = mysql.connector.connect(
            host="localhost",
            user="votre_utilisateur",
            password="votre_mot_de_passe",
            database="votre_base_de_donnees"
        )
        self.cursor = self.conn.cursor()

        # Afficher les cours de la semaine en cours
        self.afficher_semaine_en_cours()

    def afficher_semaine_en_cours(self):
        # Récupérer la date du premier jour de la semaine en cours
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())

        # Récupérer la date du dernier jour de la semaine en cours
        sunday = monday + datetime.timedelta(days=6)

        # Récupérer les cours de la semaine en cours
        self.afficher_cours_par_periode(monday, sunday)

    def afficher_semaine_precedente(self):
        # Récupérer la date du premier jour de la semaine précédente
        monday = self.monday - datetime.timedelta(days=7)
        sunday = monday + datetime.timedelta(days=6)

        # Récupérer les cours de la semaine précédente
        self.afficher_cours_par_periode(monday, sunday)

    def afficher_semaine_suivante(self):
        # Récupérer la date du premier jour de la semaine suivante
        monday = self.monday + datetime.timedelta(days=7)
        sunday = monday + datetime.timedelta(days=6)

        # Récupérer les cours de la semaine suivante
        self.afficher_cours_par_periode(monday, sunday)

    def afficher_mois_precedent(self):
        # Récupérer la date du premier jour du mois précédent
        first_day_of_month = self.first_day_of_month - datetime.timedelta(days=1)
        last_day_of_month = first_day_of_month.replace(day=1) - datetime.timedelta(days=1)

        # Récupérer les cours du mois précédent
        self.afficher_cours_par_periode(first_day_of_month, last_day_of_month)

    def afficher_mois_suivant(self):
        # Récupérer la date du premier jour du mois suivant
        first_day_of_month = self.last_day_of_month + datetime.timedelta(days=1)
        last_day_of_month = first_day_of_month.replace(day=1) - datetime.timedelta(days=1)

        # Récupérer les cours du mois suivant
        self.afficher_cours_par_periode(first_day_of_month, last_day_of_month)

    def afficher_cours_par_periode(self, start_date, end_date):
        # Récupérer les cours dans la période spécifiée
        query = "SELECT * FROM CahierDeTexte WHERE date BETWEEN %s AND %s"
        self.cursor.execute(query, (start_date, end_date))
        cours = self.cursor.fetchall()

        # Afficher les cours dans le tableau
        self.table_widget.clear()
        self.table_widget.setRowCount(len(cours))
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['Date', 'Jour', 'Matière', 'Contenu', 'Cours a eu lieu'])
        for row, course in enumerate(cours):
            for col, data in enumerate(course):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(data)))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    viewer = CahierDeTexteViewer()
    viewer.show()
    sys.exit(app.exec_())
