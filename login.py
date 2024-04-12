# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 700)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

class ConnexionPage(QtWidgets.QWidget):
    def __init__(self,cursor):
        super().__init__()
        self.setWindowTitle('Page de connexion')
        self.layout = QtWidgets.QVBoxLayout()
        self.nom_utilisateur_input = QtWidgets.QLineEdit()
        self.mot_de_passe_input = QtWidgets.QLineEdit()
        self.mot_de_passe_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.connexion_button = QtWidgets.QPushButton('Se connecter')
        self.connexion_button.clicked.connect(self.connexion)
        self.layout.addWidget(QtWidgets.QLabel('Nom d\'utilisateur:'))
        self.layout.addWidget(self.nom_utilisateur_input)
        self.layout.addWidget(QtWidgets.QLabel('Mot de passe:'))
        self.layout.addWidget(self.mot_de_passe_input)
        self.layout.addWidget(self.connexion_button)
        self.setLayout(self.layout)

    def connexion(self):
        nom_utilisateur = self.nom_utilisateur_input.text()
        mot_de_passe = self.mot_de_passe_input.text()
        cursor.execute("SELECT role FROM Utilisateurs WHERE nom_utilisateur=%s AND mot_de_passe=%s", (nom_utilisateur, mot_de_passe))
        utilisateur = cursor.fetchone()
        if utilisateur:
            role = utilisateur[0]
            if role == 'responsable_pédagogique':
                # Afficher l'interface pour le responsable pédagogique
                print("Interface pour le responsable pédagogique")
            elif role == 'coordinateur_pédagogique':
                # Afficher l'interface pour le coordinateur pédagogique
                print("Interface pour le coordinateur pédagogique")
            elif role == 'membre_commission':
                # Afficher l'interface pour le membre de la commission
                print("Interface pour le membre de la commission")
            elif role == 'chef_departement':
                # Afficher l'interface pour le chef de département
                print("Interface pour le chef de département")
        else:
            print("Nom d'utilisateur ou mot de passe incorrect")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Ecole"
    )
    cursor = conn.cursor()
    # Form = QtWidgets.QWidget()
    # ui = Ui_Form()
    # ui.setupUi(Form)
    connexion_page = ConnexionPage(cursor)
    connexion_page.show() # Show the connexion_page instead of Form
    sys.exit(app.exec_())
