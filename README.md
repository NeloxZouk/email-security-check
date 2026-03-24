# Audit-Securite CLI

Ce projet est un outil en ligne de commande pour automatiser un audit de securite sur des dossiers. Il permet de trier des fichiers et d'analyser des emails suspects.

## Fonctions principales

* **Tri de fichiers** : Le script parcourt les dossiers pour identifier les differents types de fichiers.
* **Mise en quarantaine** : Tous les fichiers avec l'extension .exe sont automatiquement deplaces dans un dossier "quarantaine" pour eviter les risques.
* **Analyse d'emails (Niveau 7)** : 
    * Le script cherche les fichiers .eml dans tous les sous-dossiers.
    * Il recupere le domaine de l'envoyeur (ce qu'il y a apres le @).
    * Il extrait tous les liens presents dans le mail.
    * Il compare le domaine de l'envoyeur avec le domaine des liens. Si c'est different, il marque le mail comme "SUSPECT".

## Installation

1. Avoir Python sur son ordinateur.
2. Installer la bibliotheque Typer :
   pip install typer

3. Installer le script pour qu'il soit reconnu comme une commande :
   pip install -e .

## Comment l'utiliser

Il suffit d'ouvrir un terminal dans le dossier du projet et de taper la commande suivie du dossier a scanner (le point "." signifie le dossier actuel) :

audit-securite .

## Details sur le code

* **recup_domaine** : C'est une petite fonction qui nettoie les adresses pour ne garder que la fin du nom (ex : efrei.fr). Ca permet de comparer facilement les liens.
* **ScanEmails** : C'est la fonction qui fait tout le travail sur les mails. Elle utilise os.walk pour fouiller partout et re.findall pour attraper tous les liens d'un coup.
