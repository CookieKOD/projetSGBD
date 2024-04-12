from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QLineEdit
import mysql.connector
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
from io import BytesIO

class ConnexionPage(QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.setWindowTitle('Page de connexion')
        self.layout = QVBoxLayout()
        self.nom_utilisateur_input = QLineEdit()
        self.mot_de_passe_input = QLineEdit()
        self.mot_de_passe_input.setEchoMode(QLineEdit.Password)
        
        self.connexion_button = QPushButton('Se connecter')
        self.connexion_button.clicked.connect(self.connexion)
        self.layout.addWidget(QLabel('Nom d\'utilisateur:'))
        self.layout.addWidget(self.nom_utilisateur_input)
        self.layout.addWidget(QLabel('Mot de passe:'))
        self.layout.addWidget(self.mot_de_passe_input)
        self.layout.addWidget(self.connexion_button)
        self.setLayout(self.layout)
        self.cursor = cursor
        self.resize(400, 200) # Set the width to 400 and the height to 200

    def connexion(self):
        nom_utilisateur = self.nom_utilisateur_input.text()
        mot_de_passe = self.mot_de_passe_input.text()
        self.cursor.execute("SELECT role FROM Utilisateurs WHERE nom_utilisateur=%s AND mot_de_passe=%s", (nom_utilisateur, mot_de_passe))
        utilisateur = self.cursor.fetchone()
        if utilisateur:
            role = utilisateur[0]
            if role == 'responsable_pédagogique':
                self.responsable_page = ResponsablePage()
                self.responsable_page.show()
            elif role == 'coordinateur_pédagogique':
                self.coordinateur_page = CoordinateurPage()
                self.coordinateur_page.show()
            elif role == 'membre_commission':
                self.membre_commission_page = MembreCommissionPage()
                self.membre_commission_page.show()
            elif role == 'chef_departement':
                self.chef_departement_page = ChefDepartementPage()
                self.chef_departement_page.show()
        else:
            print("Nom d'utilisateur ou mot de passe incorrect")

class ResponsablePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Page pour le responsable pédagogique')

class CoordinateurPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Page pour le coordinateur pédagogique')

class MembreCommissionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Page pour le membre de la commission')

class ChefDepartementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Page pour le chef de département')

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Ecole"
    )
    cursor = conn.cursor()
    connexion_page = ConnexionPage(cursor)
    connexion_page.show()
    sys.exit(app.exec_())
