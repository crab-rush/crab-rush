"""
Crab Rush — Jeu éducatif développé avec Python Arcade.

Ce fichier est le point d'entrée principal du jeu.
Les jeunes développeurs sont invités à le modifier et à l'expérimenter !
"""

import arcade


class App(arcade.Window):
    """Fenêtre principale du jeu Crab Rush."""

    def __init__(self) -> None:
        super().__init__(800, 600, title="Crab Rush")
        # Initialise tes variables et sprites ici
        pass

    def on_draw(self) -> None:
        """Dessine le jeu à chaque frame."""
        self.clear()
        # Dessine tes éléments ici


def main() -> None:
    """Lance le jeu."""
    App().run()


if __name__ == "__main__":
    main()
