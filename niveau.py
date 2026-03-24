import os
import shutil
import stat
import typer
import re 
from urllib.parse import urlparse

# Configuration de Typer pour le Niveau 4 et Niveau 8
app = typer.Typer()

@app.command()
def main(chemin: str):
    # --- NIVEAU 1 : Afficher un texte "test" ---
    print(" [ NIVEAU 1 ] ")
    print("glaglagla test")
    
    # --- NIVEAU 2 : Afficher le contenu d'une liste item par item ---

    print(" \n[ NIVEAU 2 ] ")
    ma_liste = ["Initialisation", " Scan de sécurité", "    Vérification des emails"]
    for item in ma_liste:
        print(f"Étape : {item}")

    # Niveau 3 Lister les fichiers d'un chemin
    print(" \n[ NIVEAU 3 ] ")
    print(f"\n Listing des fichiers dans : {chemin}")
    if not os.path.exists(chemin):
        print("Erreur : Le dossier n'existe pas.")
        return
    
    fichiers = os.listdir(chemin)
    for f in fichiers:
        print(f"- {f}")


    dossier_quarantaine = os.path.join(chemin, "quarantaine")


    for fichier in fichiers:
        chemin_complet = os.path.join(chemin, fichier)
        
        if os.path.isdir(chemin_complet):
            continue

        # NIVEAU 5 : Lire le contenu des fichiers .TXT
      
        if fichier.lower().endswith(".txt"):
            print(f"\n [Lecture TXT] {fichier} :")
            with open(chemin_complet, "r", encoding="utf-8", errors="ignore") as f_txt:
                print(f_txt.read())

        # NIVEAU 6 : Déplacer les .EXE en quarantaine sans droits d'exécution
        
        
        if fichier.lower().endswith(".exe"):
            if not os.path.exists(dossier_quarantaine):
                os.makedirs(dossier_quarantaine)
            
            destination = os.path.join(dossier_quarantaine, fichier)
            shutil.move(chemin_complet, destination)
            
            # Enlever les droits d'exécution
            os.chmod(destination, stat.S_IREAD | stat.S_IWRITE)
            
            print(f"\n[ALERTE] {fichier} déplacé en quarantaine et désactivé.")
        

    #   NIVEAU 7 : Scan des mails


    ScanEmails(chemin)

def recup_domaine(texte: str) -> str:
    try:
        # Nettoyage pour ne garder que le domaine (ex: efrei.fr) 
        texte_nettoye = re.sub(r'[^\w\.-]', '', texte).strip()
        parsed = urlparse(f"https://{texte_nettoye}")
        hostname = parsed.hostname or texte_nettoye
        if hostname and '.' in hostname:
            parts = hostname.split('.')
            if len(parts) >= 2:
                return '.'.join(parts[-2:]).lower()
        return ""
    except:
        return ""

def ScanEmails(chemin_parent: str):
    print(f"\n--- [Niveau 7] Scan des emails dans : {chemin_parent} ---")
    
    # os.walk permet d'entrer dans dossier "mails"

    for racine, dossiers, fichiers in os.walk(chemin_parent):
        for fichier in fichiers:
            if fichier.lower().endswith(".eml"):
                chemin_complet = os.path.join(racine, fichier)
                print(f"\n Analyse de : {fichier}")
                
                with open(chemin_complet, "r", encoding="utf-8", errors="ignore") as f:
                    contenu = f.read()
                    
                    # 1. Extraction de l'expéditeur 
                    domaine_envoyeur = ""
                    for ligne in contenu.splitlines():
                        if ligne.lower().startswith("from:"):
                            parts = ligne.split('@')
                            if len(parts) > 1:
                                expediteur = parts[-1].replace('>', '').strip()
                                domaine_envoyeur = recup_domaine(expediteur)
                                break
                    
                    print(f"    Expediteur : @{domaine_envoyeur if domaine_envoyeur else 'Inconnu'}")
                    
                    # 2. Extraction des liens 

                    liens = re.findall(r'https?://[^\s<>"\']+', contenu, re.IGNORECASE)
                    liens = list(set(liens))
                    
                    if liens:
                        coherence = False
                        for lien in liens:
                            lien_domaine = recup_domaine(lien)
                            if domaine_envoyeur and lien_domaine and domaine_envoyeur != lien_domaine:
                                print(f"   coherence : {domaine_envoyeur} VS {lien_domaine}")
                                coherence = True
                            else:
                                print(f"  Coherent : {lien_domaine}")
                        
                        print(f" RESULTAT : {'SUSPECT' if coherence else 'LEGITIME'}")
                    else:
                        print("  Aucun lien trouve.")
if __name__ == "__main__":
    app()