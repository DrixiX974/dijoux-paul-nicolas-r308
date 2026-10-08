import random
import os
import unicodedata # Module pour gérer les caractères spéciaux (comme les accents)

# --- PARTIE C : Manipulation des mots ---

def normaliser_mot(mot):
    # Cette technique un peu complexe sert à enlever tous les accents d'un mot (ex: ÉLÉPHANT -> ELEPHANT)
    sans_accent = ''.join(c for c in unicodedata.normalize('NFD', mot) 
                          if unicodedata.category(c) != 'Mn')
    # .upper() met tout le mot en MAJUSCULES
    return sans_accent.upper()

def choisir_mot(liste):
    # Choisit un mot au hasard dans une liste et le met en majuscules sans accent
    return normaliser_mot(random.choice(liste))

def masque(mot):
    # Crée une liste contenant autant de tirets '_' qu'il y a de lettres dans le mot
    # Ex: pour "PYTHON" (6 lettres), ça crée ['_', '_', '_', '_', '_', '_']
    return ['_'] * len(mot)


# --- PARTIE D & BONUS : Jeu du Pendu et Scores ---

def charger_scores(fichier="scores.txt"):
    scores = {}
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                parts = ligne.strip().split(":") # Sépare le nom et le score
                if len(parts) == 2:
                    scores[parts[0]] = float(parts[1])
    return scores

def sauvegarder_scores(scores, fichier="scores.txt"):
    with open(fichier, "w", encoding="utf-8") as f:
        for nom, victoires in scores.items():
            f.write(f"{nom}:{victoires}\n")

def afficher_ascii(erreurs):
    # Une liste contenant les dessins du pendu. L'index correspond au nombre d'erreurs.
    etapes = [
        "", 
        "\n\n\n\n\n___|___", 
        "\n |\n |\n |\n |\n |\n_|___",
        " ____\n |\n |\n |\n |\n |\n_|___", 
        " ____\n |   |\n |\n |\n |\n |\n_|___",
        " ____\n |   |\n |   O\n |\n |\n |\n_|___",
        " ____\n |   |\n |   O\n |  /|\\\n |\n |\n_|___",
        " ____\n |   |\n |   O\n |  /|\\\n |  / \\\n |\n_|___"
    ]
    print(etapes[erreurs]) # Affiche le dessin correspondant au nombre de fautes

def jouer_pendu(mode_2_joueurs=False):
    if mode_2_joueurs:
        # Mode où ton voisin choisit le mot
        mot_choisi = input("Joueur 1, tapez un mot pour le Joueur 2 : ")
        print("\n" * 50)  # Fait défiler l'écran vers le bas pour cacher le mot au Joueur 2
        mot = normaliser_mot(mot_choisi)
    else:
        # Mode solo avec des mots par défaut
        mots_possibles = ["PYTHON", "ÉLÉPHANT", "ORDINATEUR"]
        mot = choisir_mot(mots_possibles)
        
    mot_masque = masque(mot)
    erreurs = 0
    lettres_proposees = set() # Un "set" est comme une liste, mais sans doublons possibles
    
    # La partie continue tant qu'on a moins de 7 erreurs ET qu'il reste des lettres à trouver ('_')
    while erreurs < 7 and '_' in mot_masque:
        afficher_ascii(erreurs)
        # .join colle les éléments d'une liste ensemble avec un espace entre chaque
        print(f"\nMot : {' '.join(mot_masque)}") 
        print(f"Erreurs : {erreurs}/7")
        print(f"Proposées : {', '.join(sorted(lettres_proposees))}")
        
        lettre = normaliser_mot(input("Lettre : "))
        
        # On vérifie si l'utilisateur a bien tapé UNE SEULE lettre, et pas un chiffre
        if len(lettre) != 1 or not lettre.isalpha():
            print("Veuillez taper une seule lettre.")
            continue
            
        # On vérifie si la lettre n'a pas déjà été jouée
        if lettre in lettres_proposees:
            print("Déjà proposée !")
            continue
            
        # On ajoute la lettre à la liste des lettres jouées
        lettres_proposees.add(lettre)
        
        # Si la lettre est dans le mot
        if lettre in mot:
            # On parcourt le mot lettre par lettre pour voir où remplacer les tirets
            for i in range(len(mot)):
                if mot[i] == lettre:
                    mot_masque[i] = lettre # Révèle la lettre dans le masque
        else:
            erreurs += 1 # Sinon, on ajoute une erreur
            
    # Fin de la boucle : on vérifie pourquoi on est sorti de la boucle
    if '_' not in mot_masque: # S'il n'y a plus de tirets, on a tout trouvé
        print(f"Gagné ! Le mot était {mot}.")
        return True
    else: # Sinon, c'est qu'on a fait 7 erreurs
        afficher_ascii(erreurs)
        print(f"Perdu... Le mot était {mot}.")
        return False

# Lancement du jeu
if __name__ == "__main__":
    scores = charger_scores() # On charge l'historique des parties depuis le fichier texte
    joueur = input("Votre nom : ")
    
    if joueur not in scores:
        scores[joueur] = 0.0 # Si c'est un nouveau joueur, son score est de 0
    print(f"Bienvenue {joueur}, victoires: {scores[joueur]}")
    
    while True:
        # On demande si on veut jouer à 2
        mode = input("Mode 2 joueurs (tournoi) ? (o/n) : ").lower() == 'o'
        
        # Si on gagne la partie, on ajoute 1 point
        if jouer_pendu(mode):
            scores[joueur] += 1.0
            
        if input("Rejouer ? (o/n) : ").lower() != 'o':
            break
            
    # Quand on quitte, on sauvegarde le nouveau score dans le fichier texte
    sauvegarder_scores(scores)
    print("Scores enregistrés.")