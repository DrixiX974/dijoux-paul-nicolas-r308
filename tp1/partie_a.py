import os # Ce module permet à Python d'interagir avec ton Mac (ex: vérifier si un fichier existe)

def ajouter_etudiant(d, nom, note):
    # 'try' essaie d'exécuter ce code. C'est utile pour éviter que le programme plante
    try:
        # On essaie de convertir la note en nombre à virgule (float)
        d[nom] = float(note)
    # Si la note n'est pas un nombre (ex: "A+"), on attrape l'erreur (ValueError)
    except ValueError:
        print(f"Erreur : La note '{note}' de {nom} n'est pas un nombre valide.")

def moyenne_classe(d):
    # Si le dictionnaire 'd' est vide, la moyenne est 0
    if not d:
        return 0.0
    # sum() additionne toutes les notes, len() compte le nombre d'étudiants
    return sum(d.values()) / len(d)

def meilleur_etudiant(d):
    if not d:
        return None
    # max() cherche la valeur la plus grande. 
    # 'key=lambda item: item[1]' dit à Python de regarder la note (position 1) et non le nom (position 0)
    return max(d.items(), key=lambda item: item[1])

def sauvegarder_dictionnaire(d, nom_fichier):
    try:
        # 'w' signifie 'write' (écrire). Cela crée ou écrase le fichier.
        # encoding='utf-8' gère les accents français (é, à, etc.)
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            for nom, note in d.items():
                f.write(f"{nom}: {note}\n") # \n permet de passer à la ligne suivante
    except IOError as e:
        print(f"Erreur de sauvegarde : {e}")

def charger_dictionnaire(nom_fichier):
    d = {} # On crée un dictionnaire vide
    # Si le fichier n'existe pas sur ton Mac, on s'arrête là et on renvoie le dico vide
    if not os.path.exists(nom_fichier):
        print("Fichier absent, démarrage avec un dictionnaire vide.")
        return d
        
    try:
        # 'r' signifie 'read' (lire). On ouvre le fichier pour le lire.
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            for ligne in f:
                ligne = ligne.strip() # Enlève les espaces invisibles et les sauts de ligne
                if not ligne: continue # Si la ligne est vide, on passe à la suivante
                
                # On coupe la ligne en deux au niveau des deux-points ":"
                parts = ligne.split(':')
                if len(parts) == 2:
                    # On ajoute l'étudiant (parts[0] = nom, parts[1] = note)
                    ajouter_etudiant(d, parts[0].strip(), parts[1].strip())
                else:
                    print("Ligne mal formée ignorée.")
    except IOError as e:
        print(f"Erreur de chargement : {e}")
    return d

# Cette condition vérifie si on lance ce fichier directement
if __name__ == "__main__":
    d = {} # Dictionnaire de base
    ajouter_etudiant(d, "Alice", 12)
    ajouter_etudiant(d, "Bob", 15)
    ajouter_etudiant(d, "Claire", 9.5)
    
    # :.2f permet d'arrondir la moyenne à 2 chiffres après la virgule
    print(f"Moyenne : {moyenne_classe(d):.2f}")
    print(f"Meilleur : {meilleur_etudiant(d)}")