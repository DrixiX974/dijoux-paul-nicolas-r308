# tp1_complet.py
import random
import os

# === PARTIE A : Dictionnaire d'étudiants ===
def ajouter_etudiant(d, nom, note):
    # on met à jour le dictionnaire avec la nouvelle note
    d[nom] = float(note)

def moyenne_classe(d):
    # si le dico est vide on renvoie 0 pour éviter la division par zéro
    if not d:
        return 0.0
    # calcul classique : somme divisée par le nombre de valeurs
    total = sum(d.values())
    return round(total / len(d), 2)

def meilleur_etudiant(d):
    if not d:
        return None
    # on cherche la clé (le nom) qui correspond à la valeur la plus haute
    meilleur = max(d, key=d.get)
    return (meilleur, d[meilleur])

def sauvegarder(d, fichier):
    # mode 'w' pour écrire, ça écrase le fichier s'il existe déjà
    try:
        with open(fichier, 'w', encoding='utf-8') as f:
            for nom, note in d.items():
                f.write(f"{nom}:{note}\n")
    except Exception:
        pass # évite que le programme plante si on a pas les droits

def charger(fichier):
    d = {}
    if not os.path.exists(fichier):
        return d
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            for ligne in f:
                # on nettoie la ligne et on sépare le nom de la note
                parts = ligne.strip().split(':')
                if len(parts) == 2:
                    try:
                        d[parts[0]] = float(parts[1])
                    except ValueError:
                        pass # on ignore si la note n'est pas un chiffre
    except Exception:
        pass
    return d

# === PARTIE B : Devine le nombre ===
def devine_le_nombre():
    secret = random.randint(1, 100)
    print("J'ai choisi un nombre entre 1 et 100.")
    # boucle pour les 10 essais max
    for essai in range(10):
        try:
            choix = int(input("Ton choix : "))
            if choix < secret:
                print("Trop petit")
            elif choix > secret:
                print("Trop grand")
            else:
                print("Gagné !")
                return
        except ValueError:
            print("Mets un vrai nombre stp.")
    print(f"Perdu, c'était {secret}")

# === PARTIE C et D : Jeu du Pendu ===
def choisir_mot(liste):
    # prend un mot au hasard et le met en majuscules
    return random.choice(liste).upper()

def masque(mot):
    # crée une liste de tirets de la longueur du mot
    return ["_"] * len(mot)

def pendu():
    mots = ["PYTHON", "RESEAU", "ROUTEUR", "FIBRE", "SWITCH"]
    mot_secret = choisir_mot(mots)
    mot_masque = masque(mot_secret)
    erreurs = 0
    lettres_testees = []

    print("C'est parti pour le pendu !")

    # on continue tant qu'on a pas 7 erreurs et qu'il reste des lettres à trouver
    while erreurs < 7 and "_" in mot_masque:
        print(" ".join(mot_masque))
        print(f"Erreurs : {erreurs}/7")
        print(f"Déjà proposé : {','.join(lettres_testees)}")

        lettre = input("Lettre : ").upper()

        # vérifie si on a pas déjà joué cette lettre
        if lettre in lettres_testees:
            print("Déjà jouée !")
            continue
        lettres_testees.append(lettre)

        if lettre in mot_secret:
            # on remplace les tirets par la lettre aux bons endroits
            for i in range(len(mot_secret)):
                if mot_secret[i] == lettre:
                    mot_masque[i] = lettre
        else:
            # si la lettre n'est pas dans le mot, on compte une erreur
            erreurs += 1

    if "_" not in mot_masque:
        print("Gagné ! Le mot était", mot_secret)
    else:
        print("Perdu, le mot était", mot_secret)

if __name__ == "__main__":
    # Décommenter pour tester les jeux
    devine_le_nombre()
    pendu()
    pass
