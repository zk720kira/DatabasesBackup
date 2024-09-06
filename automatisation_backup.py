# ---Imports---
import os
import subprocess
from datetime import datetime
import mysql.connector

# Fonction pour vérifier la connexion MySQL
def ChechMySQLConnexion():
    try:
        # Connexion au serveur MySQL
        connexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = ""
        )
        connexion.close()  # Fermer la connexion
        return True  # Retourner True si la connexion à pu être établie
    except mysql.connector.Error:
        return False  # Retourner False si la connexion à crée une erreur

# ---Créer les dossier qui vont contenir les backups et les logs---
folder_path = "C:\Backup_databases"  # Dossier contenant le dossier de logs et de backups (dossier parent)
backup_path = "C:\Backup_databases\Backups"  # Dossier contenant les backups
logs_path = "C:\Backup_databases\Logs"  # Dossier contenant le logs

# Créer le dossier parent, Backups et Logs s'ils n'éxistent pas
if not os.path.exists(folder_path):
    # Création du dossier parent
    os.mkdir(folder_path)
    print(f"[success] Dossier : {folder_path} créé avec succès.")
    # Création du dossier Backups
    os.mkdir(backup_path)
    print(f"[success] Dossier : {backup_path} créé avec succès.")
    # Création du dossier Logs
    os.mkdir(logs_path)
    print(f"[success] Dossier : {logs_path} créé avec succès.")
else:
    print(f"[already exists] Le dossier {folder_path} éxiste déjà.")
    print(f"[already exists] Le dossier : {backup_path} éxiste déjà.")
    print(f"[already exists] Le dossier : {logs_path} éxiste déjà.")

# Vérifier la connexion au serveur MySQL
if ChechMySQLConnexion():
    print("[success] Vous êtes connecté au serveur MySQL")
    
    # Nom du fichier de backup
    now = datetime.now().strftime("%d_%m_%Y_%H_%M")
    backup_file = f"db_dump_{now}.sql"

    # Construire la commande de backup
    mysqldump_cmd = f"mysqldump --user=root --databases sakila world menagerie > {backup_path}\{backup_file}"

    # Exécuter la commande de backup
    try:
        subprocess.run(mysqldump_cmd, shell=True, check=True)
        print(f"[backup success] Sauvegarde des bases de données : sakila, world, menagerie créé avec succès : {backup_path}\{backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"[error] Une erreur est survenue lors de la sauvegarde : {e}")
else:
    print("[error] Impossible de se connecter au serveur MySQL. Vérifiez que le serveur est en cours d'exécution.")