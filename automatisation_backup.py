# ---Imports---
import os
import subprocess
from datetime import datetime
import mysql.connector
import time
import sys

# Variable globale pour contrôler l'exécution de la boucle du programme
running = True

# ---Fonctions---

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

# Variable globale pour stocker le dernier timestamp de création de fichier
last_log_file = None

# Fonction pour créer et écrire des fichiers de logs
def Logs(logs_path, message):
    global last_log_file  # Utiliser la variable globale
    
    # Vérifier si 5 minutes (300 secondes) se sont écoulées depuis la création du dernier fichier de logs
    if last_log_file is None or (datetime.now() - last_log_file).total_seconds() >= 300:
        # Si le dernier fichier de log est vieux de 5 minutes ou plus ou qu'aucun fichier de logs à été créé, créer un nouveau fichier de logs
        # Nom du fichier de logs
        now = datetime.now().strftime("%d_%m_%Y_%H_%M")
        logs_file = f"{now}.log"
        logs_path = f"{logs_path}\{logs_file}"
    
        # Date et heure pour dater le log
        date_time = datetime.now().strftime("%D %H:%M:%S")
    
        # Ouvrir et écrire dans le fichier de logs, le fichier est créé s'il n'éxiste pas        
        with open(logs_path, "a") as f:
            f.write(f"[{date_time}]{message}\n")
        
        # Mettre à jours le timestamp qui stock la dernière création de fichier de logs
        last_log_file = datetime.now()
    else:
        # Si non écrires dans le même fichier de logs
        # Reconstruir le nom et le chemin absolu du dernière fichier de logs créé
        logs_file = last_log_file.strftime("%d_%m_%Y_%H_%M") + ".log"
        logs_path = f"{logs_path}\{logs_file}"
        
        # Date et heure pour dater le log
        date_time = datetime.now().strftime("%D %H:%M:%S")
        
        # Ouvrir et écrire à la fin du fichier de logs
        with open(logs_path, "a") as f:
            f.write(f"[{date_time}]{message}\n")

# Fonction pour afficher un décompte
def Countdown(seconds, bar_length):
    # bar_length = longeur de la barre de progression
    for remaining in range(seconds, -1, -1):  # Changé de 0 à -1
        if not running:  # Contrôler si la touche "q" à été pressée
            print("\nProgramme arrêté.")
            return
        percent = (seconds - remaining) / seconds
        filled_length = int(bar_length * percent)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        
        # Calcul des minutes et secondes restantes
        mins, secs = divmod(remaining, 60)
        
        # Création du string pour l'affichage
        timer = f"{mins:02d}:{secs:02d}"  # Formatage du temp
        
        # Affichage de la barre de progression et du temp restant
        sys.stdout.write(f"\r|{bar}| {timer}")
        sys.stdout.flush()
        
        # Vérifier toutes le 0.1 secondes
        for _ in range(10):
            if not running:
                print("\nProgramme arrêté.")
                return
            time.sleep(0.1)
    
    #Ajouter un saut de ligne à la fin du décompte
    print()

# ---Programme---
# Début du programme principale
if __name__ == "__main__":
    try:
                # Afficher un message au lancement du programme de backup
        print("\033[33m[program info] \033[0mLancement du programme de backup")

        # ---Créer les dossier qui vont contenir les backups et les logs---
        folder_path = "C:\Backup_databases"  # Dossier contenant le dossier de logs et de backups (dossier parent)
        backup_path = "C:\Backup_databases\Backups"  # Dossier contenant les backups
        logs_path = "C:\Backup_databases\Logs"  # Dossier contenant le logs

        # Créer le dossier parent, Backups et Logs s'ils n'éxistent pas
        if not os.path.exists(folder_path):
            # Création du dossier parent
            os.mkdir(folder_path)
            print(f"\033[32m[folder success] \033[0mDossier : {folder_path} créé avec succès.")
            # Création du dossier Backups
            os.mkdir(backup_path)
            print(f"\033[32m[folder success] \033[0mDossier : {backup_path} créé avec succès.")
            # Création du dossier Logs
            os.mkdir(logs_path)
            print(f"\033[32m[folder success] \033[0mDossier : {logs_path} créé avec succès.")
            # Écrir dans le fichier de logs
            Logs(logs_path, "[program info] Lancement du programme de backup")
            Logs(logs_path, f"[folder success] Dossier : {folder_path} créé avec succès.")
            Logs(logs_path, f"[folder success] Dossier : {backup_path} créé avec succès.")
            Logs(logs_path, f"[folder success] Dossier : {logs_path} créé avec succès.")
        else:
            print(f"\033[32m[folder info] \033[0mLe dossier {folder_path} éxiste déjà.")
            print(f"\033[32m[folder info] \033[0mLe dossier : {backup_path} éxiste déjà.")
            print(f"\033[32m[folder info] \033[0mLe dossier : {logs_path} éxiste déjà.")
            # Écrir dans le fichier de logs
            Logs(logs_path, "[program info] Lancement du programme de backup")
            Logs(logs_path, f"[folder info] Le dossier {folder_path} éxiste déjà.")
            Logs(logs_path, f"[folder info] Le dossier : {backup_path} éxiste déjà.")
            Logs(logs_path, f"[folder info] Le dossier : {logs_path} éxiste déjà.")

        # Variable stockant l'intervalle des backup (secondes)
        print("Appuyer sur la touche 'Ctrl+C' pour arrêter proprement le programme de backup")
        backup_interval = 0
        while backup_interval < 1:
            backup_interval = int(input("Veuillez indiquer une intervalle de backup en secondes plus grand que 0 : "))
        print(f"\033[33m[backup info] \033[0mIntervalle de backup définit à {backup_interval} secondes")
        # Écrir dans le fichier de logs
        Logs(logs_path, f"[backup info] Intervalle de backup définit à {backup_interval} secondes")

        while running:
            # Vérifier la connexion au serveur MySQL
            if ChechMySQLConnexion():
                print("\033[32m" + "[MySQL success] " + "\033[0m" "Vous êtes connecté au serveur MySQL")
                # Écrir dans le fichier de logs
                Logs(logs_path, "[MySQL success] Vous êtes connecté au serveur MySQL")
                
                # Nom du fichier de backup
                now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
                backup_file = f"db_dump_{now}.sql"

                # Construire la commande de backup
                mysqldump_cmd = f"mysqldump --user=root --databases sakila world menagerie > {backup_path}\{backup_file}"

                # Exécuter la commande de backup
                try:
                    subprocess.run(mysqldump_cmd, shell=True, check=True)
                    print(f"\033[32m[backup success] \033[0mSauvegarde des bases de données : sakila, world, menagerie créé avec succès : {backup_path}\{backup_file}")
                    # Écrir dans le fichier de logs
                    Logs(logs_path, f"[backup success] Sauvegarde des base de données : sakila, world, menagerie crée avec succès : {backup_path}\{backup_file}")
                except subprocess.CalledProcessError as e:
                    print(f"\033[31m[backup error] \033[0mUne erreur est survenue lors de la sauvegarde : {e}")
                    # Écrir dans le fichier de logs
                    Logs(logs_path, f"[backup error] Une erreur est survenue lors de la sauvegarde : {e}")
                
                # Mettre en pause le programe 10 secondes avant la prochaine backup
                print(f"\033[33m[timer info] \033[0mProchaine backup dans {backup_interval} secondes")
                # Écrir dans le fichier de logs
                Logs(logs_path, f"[timer info] Prochaine backup dans {backup_interval} secondes")
                
                # Contrôller si q à été pressé pour arrêter le programme
                if not running:
                    break
                Countdown(backup_interval, backup_interval)  # Remplace le time.sleep(n) --> pause de n secondes
            else:
                print("\033[31m" + "[MySQL error] " + "\033[0m" + "Impossible de se connecter au serveur MySQL. Vérifiez que le serveur est en cours d'exécution.")
                # Écrir dans le ficher de logs
                Logs(logs_path, "[MySQL error] Impossible de se connecter au serveur MySQL. Vérifiez que le serveur est en cours d'exécution.")
                print("\033[33m[timer info] \033[0mProchain essai dans 5 secondes")
                # Écrir dans le fichier de logs
                Logs(logs_path, f"[timer info] Prochain essai dans 5 secondes")
                
                # Contrôller si q à été pressé pour arrêter le programme
                if not running:
                    break
                Countdown(5, 5)  # Remplace le time.slepp(5) --> pause de 5 secondes
    except KeyboardInterrupt:
        # Gérer l'interruption avec Ctrl+C
        print("\n\033[33m[program info] \033[0mProgramme interrompu par l'utilisateur.")
        Logs(logs_path, "[program info] Programme interrompu par l'utilisateur.")
