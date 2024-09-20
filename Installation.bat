@echo off
cls

REM Se déplacer dans le C:\
cd C:\DatabasesBackup

REM Installer les dépendances python
python -m ensurepip
python -m pip install --upgrade pip

REM Installation des packages pour le bon fonctionnements du script
pip install -r requirements.txt

REM Créer la tâche planifiée
schtasks /create /tn "DatabasesBackup" /xml "C:\DatabasesBackup\DatabasesBackup.xml"

echo L'installation est terminee.
echo Pressez sur Enter pour fermer la fenetre.
PAUSE
