# bibliotheque.py
import csv
import os

class Livre:
    def __init__(self, titre, auteur, annee):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        # par défaut un nouveau livre est disponible
        self.disponible = True
        self.emprunteur = None

    def emprunter(self, nom):
        # si personne ne l'a, on le prête
        if self.disponible:
            self.disponible = False
            self.emprunteur = nom
            return True
        return False

    def rendre(self):
        # on le remet disponible dans les rayons
        self.disponible = True
        self.emprunteur = None
        return True

    def afficher(self):
        # petit affichage conditionnel
        if self.disponible:
            etat = "Dispo"
        else:
            etat = f"Emprunté par {self.emprunteur}"
        print(f"- {self.titre} ({self.auteur}, {self.annee}) : {etat}")

class Utilisateur:
    def __init__(self, nom):
        self.nom = nom
        # liste pour stocker les livres qu'il garde
        self.emprunts = []

    def emprunter_livre(self, livre):
        self.emprunts.append(livre)

    def rendre_livre(self, titre):
        # on cherche le livre dans sa liste et on l'enlève
        for l in self.emprunts:
            if l.titre == titre:
                self.emprunts.remove(l)
                return True
        return False

class Bibliotheque:
    def __init__(self):
        # dictionnaire pour retrouver vite les trucs
        self.livres = {}
        self.utilisateurs = {}

    def ajouter_livre(self, livre):
        self.livres[livre.titre] = livre

    def ajouter_utilisateur(self, u):
        self.utilisateurs[u.nom] = u

    def emprunter(self, nom, titre):
        # on vérifie que l'utilisateur et le livre existent bien
        if nom in self.utilisateurs and titre in self.livres:
            user = self.utilisateurs[nom]
            livre = self.livres[titre]
            # si l'emprunt passe, on donne le livre à l'utilisateur
            if livre.emprunter(nom):
                user.emprunter_livre(livre)
                print("Emprunt réussi.")
            else:
                print("Livre déjà pris.")
        else:
            print("Utilisateur ou livre introuvable.")

    def rendre(self, nom, titre):
        if nom in self.utilisateurs and titre in self.livres:
            user = self.utilisateurs[nom]
            livre = self.livres[titre]
            # sécurité : on vérifie que c'est bien lui qui l'a emprunté
            if livre.emprunteur == nom:
                livre.rendre()
                user.rendre_livre(titre)
                print("Livre rendu avec succès.")
            else:
                print("Ce n'est pas lui qui l'a emprunté.")
        else:
            print("Erreur de nom ou de livre.")

    def afficher_livres(self):
        for l in self.livres.values():
            l.afficher()

    def sauvegarder(self, fic):
        # écrit l'état actuel en csv
        try:
            with open(fic, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for l in self.livres.values():
                    # gère le champ vide si y'a pas d'emprunteur
                    emp = l.emprunteur if l.emprunteur else ""
                    writer.writerow([l.titre, l.auteur, l.annee, l.disponible, emp])
        except Exception:
            print("Erreur de sauvegarde.")

    def charger(self, fic):
        if not os.path.exists(fic):
            return
        try:
            with open(fic, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for ligne in reader:
                    if len(ligne) == 5:
                        l = Livre(ligne[0], ligne[1], ligne[2])
                        l.disponible = (ligne[3] == 'True')
                        l.emprunteur = ligne[4] if ligne[4] else None
                        self.ajouter_livre(l)
                        
                        # recrée l'utilisateur s'il existe pas
                        if l.emprunteur and l.emprunteur not in self.utilisateurs:
                            self.ajouter_utilisateur(Utilisateur(l.emprunteur))
                        # lui redonne son livre
                        if l.emprunteur:
                            self.utilisateurs[l.emprunteur].emprunter_livre(l)
        except Exception:
            pass

def menu():
    bib = Bibliotheque()
    bib.charger("biblio.csv")

    while True:
        print("\n--- MENU ---")
        print("1. Ajouter livre | 2. Ajouter utilisateur | 3. Emprunter")
        print("4. Rendre | 5. Afficher | 6. Quitter")
        choix = input("Choix : ")
        
        if choix == '1':
            t = input("Titre : ")
            a = input("Auteur : ")
            an = input("Année : ")
            bib.ajouter_livre(Livre(t, a, an))
        elif choix == '2':
            n = input("Nom : ")
            bib.ajouter_utilisateur(Utilisateur(n))
        elif choix == '3':
            n = input("Nom : ")
            t = input("Titre : ")
            bib.emprunter(n, t)
        elif choix == '4':
            n = input("Nom : ")
            t = input("Titre : ")
            bib.rendre(n, t)
        elif choix == '5':
            bib.afficher_livres()
        elif choix == '6':
            bib.sauvegarder("biblio.csv")
            print("Sauvegardé. Tchao !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()
    pass
