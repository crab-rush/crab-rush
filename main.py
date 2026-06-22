"""
Crab Rush — Point d'entrée du jeu
Jeu éducatif de programmation pour jeunes apprenants.
"""

import arcade


class FenetreJeu(arcade.Window):
    """Fenêtre principale du jeu Crab Rush."""

    def __init__(self):
        super().__init__(800, 600, "Crab Rush")

        # Couleurs
        self.couleur_bleu = (44, 95, 108)      # Océan
        self.couleur_sable = (245, 230, 211)   # Sable clair
        self.couleur_bouton = (255, 165, 0)    # Jaune/orange
        self.couleur_bouton_fonce = (230, 140, 0)

        # État du jeu : MENU, JEU ou PARAMETRES
        self.etaat = "MENU"

        # Bouton "Jouer"
        self.largeur_bouton = 200   # 1/4 de 800
        self.hauteur_bouton = 60
        self.bouton_x = 400         # Centré horizontalement
        self.bouton_y = 150         # 1/4 de 600

        # Bouton Paramètres (engrenage)
        self.largeur_param = 50
        self.hauteur_param = 50
        self.param_x = 750          # Coin supérieur droit
        self.param_y = 550

        # Flèche retour
        self.retour_x = 30
        self.retour_y = 570
        self.retour_taille = 30

        # Sliders son
        self.largeur_slider = 200
        self.hauteur_slider = 10
        self.slider_musique_x = 400
        self.slider_musique_y = 380
        self.slider_sons_x = 400
        self.slider_sons_y = 340

        # Volume (0-100)
        self.volume_musique = 70
        self.volume_sons = 50

        # Curseur en cours de déplacement
        self.curseur_en_cours = None  # "musique" ou "sons"

        # Bouton Quitter
        self.largeur_quitter = 150
        self.hauteur_quitter = 50
        self.quitter_x = 400
        self.quitter_y = 150

        # Popup confirmation
        self.popup_affiche = False
        self.popup_timer = 0
        self.largeur_popup_btn = 80
        self.hauteur_popup_btn = 40

        # Titre
        self.titre_texte = "🦀 Crab Rush"

    def on_update(self, delta_time):
        """Gère le timer du popup."""
        if self.popup_affiche:
            self.popup_timer += delta_time
            if self.popup_timer >= 3.0:
                self.close()

    def on_draw(self):
        """Dessine l'écran en cours."""
        self.clear()
        if self.etaat == "MENU":
            self.dessiner_menu()
        elif self.etaat == "JEU":
            self.dessiner_jeu()
        else:
            self.dessiner_parametres()

        # Flèche retour (sur les écrans JEU et PARAMETRES)
        if self.etaat != "MENU":
            self.dessiner_flache_retour()

    def dessiner_menu(self):
        """Dessine l'écran de titre avec dégradé, titre et bouton."""

        # Dégradé bleu → sable
        self.dessiner_degrade()

        # Titre
        arcade.draw_text(
            self.titre_texte,
            400, 500,
            color=arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
            anchor_y="center"
        )

        # Bouton "Jouer"
        self.dessiner_bouton_jouer()

        # Bouton Paramètres
        self.dessiner_bouton_parametres()

    def dessiner_degrade(self):
        """Dessine un dégradé vertical de bleu (haut) à sable (bas)."""
        bande_hauteur = 2
        nb_bandes = self.height // bande_hauteur

        for i in range(nb_bandes):
            # Y=0 est en bas dans Arcade, donc on inverse
            y_bas = i * bande_hauteur
            y_haut = y_bas + bande_hauteur
            # Ratio : 0 en bas (sable), 1 en haut (bleu)
            ratio = i / nb_bandes

            # Interpolation entre sable (bas) et bleu (haut)
            r = int(self.couleur_sable[0] * (1 - ratio) + self.couleur_bleu[0] * ratio)
            g = int(self.couleur_sable[1] * (1 - ratio) + self.couleur_bleu[1] * ratio)
            b = int(self.couleur_sable[2] * (1 - ratio) + self.couleur_bleu[2] * ratio)

            arcade.draw_lrbt_rectangle_filled(
                0, self.width,
                y_bas, y_haut,
                (r, g, b)
            )

    def dessiner_bouton_jouer(self):
        """Dessine le bouton "Jouer" (rectangle simple)."""
        x_gauche = self.bouton_x - self.largeur_bouton // 2
        y_bas = self.bouton_y - self.hauteur_bouton // 2

        # Rectangle simple
        arcade.draw_lrbt_rectangle_filled(
            x_gauche, x_gauche + self.largeur_bouton,
            y_bas, y_bas + self.hauteur_bouton,
            self.couleur_bouton
        )

        # Texte
        arcade.draw_text(
            "Jouer",
            self.bouton_x, self.bouton_y,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

    def dessiner_bouton_parametres(self):
        """Dessine le bouton paramètres (carré gris avec engrenage)."""
        x_gauche = self.param_x - self.largeur_param // 2
        y_bas = self.param_y - self.hauteur_param // 2

        # Carré gris avec coins légèrement arrondis
        arcade.draw_lrbt_rectangle_filled(
            x_gauche, x_gauche + self.largeur_param,
            y_bas, y_bas + self.hauteur_param,
            (100, 100, 100)
        )

        # Engrenage amélioré avec 8 dents
        centre_x = self.param_x
        centre_y = self.param_y
        rayon_corps = 10
        rayon_dent = 4
        longueur_dent = 8
        nb_dents = 8

        # Corps central de l'engrenage
        arcade.draw_circle_filled(centre_x, centre_y, rayon_corps, arcade.color.WHITE)

        # 8 dents réparties autour
        for i in range(nb_dents):
            angle = (2 * 3.14159 * i) / nb_dents
            x_dent = centre_x + (rayon_corps + longueur_dent / 2) * 0.7 * (angle if i % 2 == 0 else 0)
            y_dent = centre_y + (rayon_corps + longueur_dent / 2) * 0.7 * (angle if i % 2 == 0 else 0)

        # Dents horizontales et verticales (ronds)
        # Haut
        arcade.draw_circle_filled(
            centre_x, centre_y + rayon_corps + longueur_dent / 2,
            3, arcade.color.WHITE
        )
        # Bas
        arcade.draw_circle_filled(
            centre_x, centre_y - rayon_corps - longueur_dent / 2,
            3, arcade.color.WHITE
        )
        # Gauche
        arcade.draw_circle_filled(
            centre_x - rayon_corps - longueur_dent / 2, centre_y,
            3, arcade.color.WHITE
        )
        # Droite
        arcade.draw_circle_filled(
            centre_x + rayon_corps + longueur_dent / 2, centre_y,
            3, arcade.color.WHITE
        )
        # Diagonales
        arcade.draw_ellipse_filled(
            centre_x + 10, centre_y + 10,
            5, 5,
            arcade.color.WHITE
        )
        arcade.draw_ellipse_filled(
            centre_x - 10, centre_y + 10,
            5, 5,
            arcade.color.WHITE
        )
        arcade.draw_ellipse_filled(
            centre_x + 10, centre_y - 10,
            5, 5,
            arcade.color.WHITE
        )
        arcade.draw_ellipse_filled(
            centre_x - 10, centre_y - 10,
            5, 5,
            arcade.color.WHITE
        )

        # Trou central
        arcade.draw_circle_filled(centre_x, centre_y, 3, (100, 100, 100))

    def dessiner_jeu(self):
        """Dessine l'écran de jeu (vide pour l'instant)."""
        # Fond uni sombre
        arcade.draw_lrbt_rectangle_filled(
            0, self.width,
            0, self.height,
            (50, 50, 50)
        )

        arcade.draw_text(
            "Écran de jeu — à venir...",
            400, 300,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "Appuie sur Echap pour revenir au menu",
            400, 250,
            color=arcade.color.LIGHT_GRAY,
            font_size=16,
            anchor_x="center",
            anchor_y="center"
        )

    def dessiner_parametres(self):
        """Dessine l'écran des paramètres."""
        # Fond uni sombre
        arcade.draw_lrbt_rectangle_filled(
            0, self.width,
            0, self.height,
            (50, 50, 50)
        )

        # Sliders son
        self.dessiner_slider_musique()
        self.dessiner_slider_sons()

        # Bouton Quitter
        self.dessiner_bouton_quitter()

        # Popup confirmation
        if self.popup_affiche:
            self.dessiner_popup_confirmation()

    def dessiner_flache_retour(self):
        """Dessine la flèche retour (carré + triangle pointant à gauche)."""
        centre_x = self.retour_x
        centre_y = self.retour_y
        taille = self.retour_taille

        # Carré gris foncé
        arcade.draw_lrbt_rectangle_filled(
            centre_x - taille // 2, centre_x + taille // 2,
            centre_y - taille // 2, centre_y + taille // 2,
            (60, 60, 60)
        )

        # Triangle pointant vers la gauche
        arcade.draw_triangle_filled(
            centre_x + 5, centre_y - 8,
            centre_x + 5, centre_y + 8,
            centre_x - 8, centre_y,
            arcade.color.WHITE
        )

    def dessiner_slider_musique(self):
        """Dessine le slider de volume musique."""
        x_gauche = self.slider_musique_x - self.largeur_slider // 2

        # Label
        arcade.draw_text(
            "Musique",
            self.slider_musique_x - self.largeur_slider // 2 - 20, self.slider_musique_y,
            color=arcade.color.WHITE,
            font_size=14,
            anchor_x="right",
            anchor_y="center"
        )

        # Fond du slider
        arcade.draw_lrbt_rectangle_filled(
            x_gauche, x_gauche + self.largeur_slider,
            self.slider_musique_y - self.hauteur_slider // 2,
            self.slider_musique_y + self.hauteur_slider // 2,
            (60, 60, 60)
        )

        # Barre de progression
        remplissage = int(self.largeur_slider * self.volume_musique / 100)
        arcade.draw_lrbt_rectangle_filled(
            x_gauche, x_gauche + remplissage,
            self.slider_musique_y - self.hauteur_slider // 2,
            self.slider_musique_y + self.hauteur_slider // 2,
            (100, 150, 255)
        )

        # Curseur
        arcade.draw_circle_filled(
            x_gauche + remplissage,
            self.slider_musique_y,
            8,
            arcade.color.WHITE
        )

    def dessiner_slider_sons(self):
        """Dessine le slider de volume effets sonores."""
        x_gauche = self.slider_sons_x - self.largeur_slider // 2

        # Label
        arcade.draw_text(
            "Effets son",
            self.slider_sons_x - self.largeur_slider // 2 - 20, self.slider_sons_y,
            color=arcade.color.WHITE,
            font_size=14,
            anchor_x="right",
            anchor_y="center"
        )

        # Fond du slider
        arcade.draw_lrbt_rectangle_filled(
            x_gauche, x_gauche + self.largeur_slider,
            self.slider_sons_y - self.hauteur_slider // 2,
            self.slider_sons_y + self.hauteur_slider // 2,
            (60, 60, 60)
        )

        # Barre de progression
        remplissage = int(self.largeur_slider * self.volume_sons / 100)
        arcade.draw_lrbt_rectangle_filled(
            x_gauche, x_gauche + remplissage,
            self.slider_sons_y - self.hauteur_slider // 2,
            self.slider_sons_y + self.hauteur_slider // 2,
            (100, 200, 100)
        )

        # Curseur
        arcade.draw_circle_filled(
            x_gauche + remplissage,
            self.slider_sons_y,
            8,
            arcade.color.WHITE
        )

    def dessiner_bouton_quitter(self):
        """Dessine le bouton Quitter (rectangle rouge)."""
        x_gauche = self.quitter_x - self.largeur_quitter // 2
        y_bas = self.quitter_y - self.hauteur_quitter // 2

        # Rectangle rouge
        arcade.draw_lrbt_rectangle_filled(
            x_gauche, x_gauche + self.largeur_quitter,
            y_bas, y_bas + self.hauteur_quitter,
            (180, 50, 50)
        )

        # Texte
        arcade.draw_text(
            "Quitter",
            self.quitter_x, self.quitter_y,
            color=arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center"
        )

    def dessiner_popup_confirmation(self):
        """Dessine le popup de confirmation de quitter."""
        # Fond sombre
        arcade.draw_lrbt_rectangle_filled(
            0, self.width,
            0, self.height,
            (0, 0, 0)
        )

        # Boîte du popup
        popup_x = 300
        popup_y = 250
        popup_largeur = 200
        popup_hauteur = 100

        arcade.draw_lrbt_rectangle_filled(
            popup_x, popup_x + popup_largeur,
            popup_y, popup_y + popup_hauteur,
            (80, 80, 80)
        )

        # Texte de confirmation
        arcade.draw_text(
            "Vous allez quitter le jeu",
            popup_x + popup_largeur // 2, popup_y + 50,
            color=arcade.color.WHITE,
            font_size=16,
            anchor_x="center",
            anchor_y="center"
        )

        # Compteur
        reste = 3 - int(self.popup_timer)
        arcade.draw_text(
            f"Fermeture dans {reste}s...",
            popup_x + popup_largeur // 2, popup_y + 25,
            color=arcade.color.LIGHT_GRAY,
            font_size=12,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Gère les clics de souris."""
        if self.etaat == "MENU":
            # Vérifie si le clic est dans le bouton Jouer
            if (self.bouton_x - self.largeur_bouton // 2 <= x <= self.bouton_x + self.largeur_bouton // 2 and
                    self.bouton_y - self.hauteur_bouton // 2 <= y <= self.bouton_y + self.hauteur_bouton // 2):
                # Fermer le menu et lancer le jeu
                self.close()
                from test_game import PrototypeJeu
                jeu = PrototypeJeu()
                jeu.run()
            # Vérifie si le clic est dans le bouton Paramètres
            elif (self.param_x - self.largeur_param // 2 <= x <= self.param_x + self.largeur_param // 2 and
                  self.param_y - self.hauteur_param // 2 <= y <= self.param_y + self.hauteur_param // 2):
                self.etaat = "PARAMETRES"
        elif self.etaat in ["JEU", "PARAMETRES"]:
            # Vérifie si le clic est dans la flèche retour
            if (self.retour_x - self.retour_taille // 2 <= x <= self.retour_x + self.retour_taille // 2 and
                    self.retour_y - self.retour_taille // 2 <= y <= self.retour_y + self.retour_taille // 2):
                self.etaat = "MENU"
            # Vérifie si le clic est dans le bouton Quitter
            elif self.etaat == "PARAMETRES":
                if (self.quitter_x - self.largeur_quitter // 2 <= x <= self.quitter_x + self.largeur_quitter // 2 and
                        self.quitter_y - self.hauteur_quitter // 2 <= y <= self.quitter_y + self.hauteur_quitter // 2):
                    self.popup_affiche = True
            # Vérifie si le clic est sur un slider
            elif self.etaat == "PARAMETRES":
                x_gauche_musique = self.slider_musique_x - self.largeur_slider // 2
                x_gauche_sons = self.slider_sons_x - self.largeur_slider // 2
                print(f"Clic PARAMETRES: x={x}, y={y}")
                print(f"  Slider musique: x={x_gauche_musique}-{x_gauche_musique + self.largeur_slider}, y={self.slider_musique_y - 15}-{self.slider_musique_y + 15}")
                print(f"  Slider sons: x={x_gauche_sons}-{x_gauche_sons + self.largeur_slider}, y={self.slider_sons_y - 15}-{self.slider_sons_y + 15}")
                # Slider musique
                if (x_gauche_musique <= x <= x_gauche_musique + self.largeur_slider and
                        self.slider_musique_y - 15 <= y <= self.slider_musique_y + 15):
                    print("  → Slider musique cliqué")
                    self.curseur_en_cours = "musique"
                    self.volume_musique = int(((x - x_gauche_musique) / self.largeur_slider) * 100)
                # Slider sons
                elif (x_gauche_sons <= x <= x_gauche_sons + self.largeur_slider and
                      self.slider_sons_y - 15 <= y <= self.slider_sons_y + 15):
                    print("  → Slider sons cliqué")
                    self.curseur_en_cours = "sons"
                    self.volume_sons = int(((x - x_gauche_sons) / self.largeur_slider) * 100)

    def on_mouse_release(self, x, y, button, modifiers):
        """Relâche le curseur en cours."""
        self.curseur_en_cours = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Gère le déplacement des curseurs."""
        if self.curseur_en_cours == "musique":
            x_gauche = self.slider_musique_x - self.largeur_slider // 2
            self.volume_musique = max(0, min(100, int(((x - x_gauche) / self.largeur_slider) * 100)))
        elif self.curseur_en_cours == "sons":
            x_gauche = self.slider_sons_x - self.largeur_slider // 2
            self.volume_sons = max(0, min(100, int(((x - x_gauche) / self.largeur_slider) * 100)))





def main():
    """Fonction principale — lance le jeu."""
    fenetre = FenetreJeu()
    arcade.run()


if __name__ == "__main__":
    main()
