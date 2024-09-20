@echo off
cls

REM Démarrer le script de backup, définir l'intéravlle de backups à 10 secondes
(echo 10) | python C:\DatabasesBackup\automatisation_backup.py