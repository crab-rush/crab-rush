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

        # État du jeu : MENU ou JEU
        self.etaat = "MENU"

        # Bouton "Jouer"
        self.largeur_bouton = 200   # 1/4 de 800
        self.hauteur_bouton = 60
        self.bouton_x = 400         # Centré horizontalement
        self.bouton_y = 150         # 1/4 de 600

        # Titre
        self.titre_texte = "🦀 Crab Rush"

    def on_draw(self):
        """Dessine l'écran en cours."""
        self.clear()
        if self.etaat == "MENU":
            self.dessiner_menu()
        else:
            self.dessiner_jeu()

    def dessiner_menu(self):
        """Dessine l'écran de titre avec dégradé, titre et bouton."""

        # Dégradé bleu → sable
        self.dessiner_degrade()

        # Titre
        arcade.draw_text(
            self.titre_texte,
            x=400,
            y=500,
            color=arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
            anchor_y="center"
        )

        # Bouton "Jouer"
        self.dessiner_bouton_jouer()

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
            x_gauche, self.bouton_x + self.largeur_bouton // 2,
            y_bas, y_bas + self.hauteur_bouton,
            self.couleur_bouton
        )

        # Texte
        arcade.draw_text(
            "Jouer",
            x=self.bouton_x,
            y=self.bouton_y,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

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
            x=400,
            y=300,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "Appuie sur Echap pour revenir au menu",
            x=400,
            y=250,
            color=arcade.color.LIGHT_GRAY,
            font_size=16,
            anchor_x="center",
            anchor_y="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Gère les clics de souris."""
        if self.etaat == "MENU":
            # Vérifie si le clic est dans le bouton
            if (self.bouton_x - self.largeur_bouton // 2 <= x <= self.bouton_x + self.largeur_bouton // 2 and
                    self.bouton_y - self.hauteur_bouton // 2 <= y <= self.bouton_y + self.hauteur_bouton // 2):
                self.etaat = "JEU"

    def on_key_press(self, key, modifiers):
        """Gère les touches du clavier."""
        if key == arcade.esc_key and self.etaat == "JEU":
            self.etaat = "MENU"


def main():
    """Fonction principale — lance le jeu."""
    fenetre = FenetreJeu()
    arcade.run()


if __name__ == "__main__":
    main()
