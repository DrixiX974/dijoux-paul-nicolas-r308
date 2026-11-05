# morpion.py
import random

class Grille:
    def __init__(self):
        # on crée un tableau 2D 3x3 rempli d'espaces vides
        self.cases = [[" " for _ in range(3)] for _ in range(3)]

    def afficher(self):
        print("\n")
        for ligne in self.cases:
            # joint les cases avec des barres pour faire joli
            print(" | ".join(ligne))
            print("-" * 9)

    def jouer(self, x, y, joueur):
        # empêche de jouer en dehors de la grille
        if x < 0 or x > 2 or y < 0 or y > 2:
            return False
        # si la case est vide, on place le pion
        if self.cases[x][y] == " ":
            self.cases[x][y] = joueur
            return True
        return False

    def est_gagnant(self, j):
        # vérification des lignes et des colonnes
        for i in range(3):
            if self.cases[i][0] == self.cases[i][1] == self.cases[i][2] == j:
                return True
            if self.cases[0][i] == self.cases[1][i] == self.cases[2][i] == j:
                return True
        # vérification des deux diagonales
        if self.cases[0][0] == self.cases[1][1] == self.cases[2][2] == j:
            return True
        if self.cases[0][2] == self.cases[1][1] == self.cases[2][0] == j:
            return True
        return False

    def est_plein(self):
        # cherche s'il reste des espaces, sinon c'est plein
        for ligne in self.cases:
            if " " in ligne:
                return False
        return True

class JoueurHumain:
    def prochain_coup(self, grille, symbole):
        while True:
            try:
                # demande les coordonnées au joueur
                x = int(input("Ligne (0, 1, 2) : "))
                y = int(input("Colonne (0, 1, 2) : "))
                return x, y
            except ValueError:
                print("Merci de mettre un vrai chiffre.")

class JoueurIA:
    def prochain_coup(self, grille, symbole):
        # l'ia choisit des coordonnées complètement au pif
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        return x, y

def jouer_partie():
    g = Grille()
    j1 = JoueurHumain()
    j2 = JoueurIA()
    tour_j1 = True # on commence par le joueur 1

    # tant que la grille n'est pas remplie
    while not g.est_plein():
        g.afficher()
        if tour_j1:
            print("C'est à toi (X)")
            x, y = j1.prochain_coup(g, "X")
            # redemande tant que le coup n'est pas possible (case prise)
            while not g.jouer(x, y, "X"):
                print("Coup refusé, case occupée ou hors limites.")
                x, y = j1.prochain_coup(g, "X")
            if g.est_gagnant("X"):
                g.afficher()
                print("Tu as gagné !")
                return
        else:
            print("L'IA joue (O)")
            x, y = j2.prochain_coup(g, "O")
            while not g.jouer(x, y, "O"):
                x, y = j2.prochain_coup(g, "O")
            if g.est_gagnant("O"):
                g.afficher()
                print("L'IA a gagné !")
                return
        # on passe au tour de l'autre
        tour_j1 = not tour_j1

    g.afficher()
    print("Match nul !")

if __name__ == "__main__":
    jouer_partie()
