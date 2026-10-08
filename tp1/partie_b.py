import random # Module pour générer des choses au hasard

# On définit les règles de base : entre 1 et 100, et 10 essais maximum
def devine_le_nombre(borne_min=1, borne_max=100, max_essais=10):
    # L'ordinateur choisit un nombre au hasard
    secret = random.randint(borne_min, borne_max)
    print(f"\n--- Devine le nombre (entre {borne_min} et {borne_max}) ---")
    
    # Une boucle qui va tourner de 1 jusqu'au nombre d'essais max
    for essai in range(1, max_essais + 1):
        # input() permet à l'utilisateur de taper quelque chose dans le terminal
        saisie = input(f"Essai {essai}/{max_essais} - Proposition : ")
        
        try:
            # On transforme le texte tapé en un nombre entier (integer)
            prop = int(saisie)
        except ValueError:
            # Si le joueur tape des lettres, on le prévient et on relance le tour
            print("Entrée invalide. Veuillez taper un nombre.")
            continue # Passe directement au prochain tour de la boucle
            
        # Les vérifications
        if prop < secret:
            print("Trop petit !")
        elif prop > secret:
            print("Trop grand !")
        else:
            # Si ce n'est ni trop petit ni trop grand, c'est gagné !
            print("Gagné !")
            return True # Fin de la partie, on renvoie "Vrai" (victoire)
            
    # Si la boucle se termine sans qu'on ait trouvé, c'est perdu
    print(f"Perdu ! Le nombre était {secret}.")
    return False

if __name__ == "__main__":
    # "while True" crée une boucle infinie pour pouvoir rejouer à l'infini
    while True:
        devine_le_nombre() # On lance le jeu
        # On demande s'il veut rejouer. .lower() transforme la réponse en minuscules
        if input("Rejouer ? (o/n) : ").lower() != 'o':
            break # Si la réponse n'est pas 'o' (oui), on casse la boucle infinie, le jeu s'arrête