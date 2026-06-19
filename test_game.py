"""
Crab Rush — Prototype test (Niveau 1)

Jeu de plateforme 2D défilement latéral (gauche → droite).
- Le maître nageur traverse la plage pour sauver une personne qui se noie
- Flèches / ZQSD : déplacer
- Espace / Z : sauter
- Bas / S : se baisser
- Espace : frapper les crabes
- R : recommencer
- Echap : quitter

Niveau 1 — Première Sauveterie (Facile)
"""

import arcade
import math
from dataclasses import dataclass
from typing import List, Optional


# ─── Constantes ───────────────────────────────────────────────
TILE_SIZE = 40
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_FORCE = -10
MOVE_SPEED = 4
LEVEL_WIDTH = 30  # nombre de cases de large

# Couleurs
COULEUR_CIEL = arcade.color.AQUA
COULEUR_SABLE = arcade.color.YELLOW
COULEUR_SABLE_MOURE = arcade.color.ORANGE
COULEUR_TROU = arcade.color.BLACK
COULEUR_EAU = arcade.color.TEAL
COULEUR_CRABE = arcade.color.RED
COULEUR_JOUEUR = arcade.color.BLUE
COULEUR_TEXT = arcade.color.WHITE
COULEUR_OBSTACLE_BAS = arcade.color.BROWN
COULEUR_OBSTACLE_HAUT = arcade.color.DARK_GREEN


# ─── Données ──────────────────────────────────────────────────
@dataclass
class Position:
    x: int
    y: int


@dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int


@dataclass
class CrabeConfig:
    x: float
    y: float
    width: int
    height: int
    vitesse: float
    direction: int  # 1 = droite, -1 = gauche
    alive: bool = True
    patrol_start: int = 0
    patrol_end: int = 0


@dataclass
class ObstacleBas:
    """Obstacle qu'il faut sauter (trou, piquet)."""
    x: int
    y: int
    width: int
    height: int


@dataclass
class ObstacleHaut:
    """Obstacle qu'il faut éviter en se baissant (branche, filet bas)."""
    x: int
    y: int
    width: int
    height: int


@dataclass
class Sol:
    """Bande de sol."""
    x: int
    y: int
    width: int
    height: int


# ─── Configuration du niveau ──────────────────────────────────
def creer_niveau() -> dict:
    """Crée les données du niveau 1."""
    crabes: List[CrabeConfig] = [
        CrabeConfig(x=6.0, y=1.0, width=30, height=30, vitesse=1.5,
              direction=1, patrol_start=5, patrol_end=9),
        CrabeConfig(x=12.0, y=1.0, width=30, height=30, vitesse=2.0,
              direction=1, patrol_start=10, patrol_end=15),
        CrabeConfig(x=18.0, y=1.0, width=30, height=30, vitesse=1.8,
              direction=-1, patrol_start=16, patrol_end=21),
        CrabeConfig(x=24.0, y=1.0, width=30, height=30, vitesse=2.2,
              direction=1, patrol_start=22, patrol_end=27),
    ]

    obstacles_bas: List[ObstacleBas] = [
        ObstacleBas(x=4, y=0, width=2, height=1),   # trou 1
        ObstacleBas(x=8, y=0, width=2, height=1),   # trou 2
        ObstacleBas(x=14, y=0, width=2, height=1),  # trou 3
        ObstacleBas(x=20, y=0, width=2, height=1),  # trou 4
        ObstacleBas(x=26, y=0, width=2, height=1),  # trou 5
    ]

    obstacles_haut: List[ObstacleHaut] = [
        ObstacleHaut(x=10, y=2, width=3, height=1),  # filet bas
        ObstacleHaut(x=16, y=2, width=2, height=1),  # branche
        ObstacleHaut(x=22, y=2, width=3, height=1),  # filet bas
    ]

    sols: List[Sol] = [
        Sol(x=0, y=0, width=LEVEL_WIDTH, height=1),  # sol principal
    ]

    depart = Position(1, 0)
    arrivee = Position(LEVEL_WIDTH - 1, 0)

    return {
        "crabes": crabes,
        "obstacles_bas": obstacles_bas,
        "obstacles_haut": obstacles_haut,
        "sols": sols,
        "depart": depart,
        "arrivee": arrivee,
    }


# ─── Classes du jeu ───────────────────────────────────────────
class Joueur:
    """Le maître nageur."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.largeur = 30
        self.hauteur_normale = 35
        self.hauteur_baisse = 20
        self.hauteur = self.hauteur_normale
        self.est_baisse = False
        self.est_saut = False
        self.en_attaque = False
        self.temps_attaque = 0.0
        self.facing_right = True
        self.vie = 1

    def deplacer(self, dx: int, touches: set) -> None:
        """Déplace le joueur horizontalement."""
        if arcade.key.UP in touches or arcade.key.W in touches or arcade.key.Z in touches:
            if not self.est_saut:
                self.vy = JUMP_FORCE
                self.est_saut = True
        if arcade.key.SPACE in touches:
            self.en_attaque = True
            self.temps_attaque = 0.3

        if dx > 0:
            self.vx = MOVE_SPEED
            self.facing_right = True
        elif dx < 0:
            self.vx = -MOVE_SPEED
            self.facing_right = False
        else:
            self.vx = 0

    def se_baisser(self, bas: bool) -> None:
        """Se baisser ou se relever."""
        if bas and not self.est_saut:
            self.hauteur = self.hauteur_baisse
            self.est_baisse = True
        else:
            self.hauteur = self.hauteur_normale
            self.est_baisse = False

    def update(self, dt: float, sols: List[Sol], niveau_largeur: int) -> None:
        """Met à jour la physique du joueur."""
        # Gravité
        if not self.est_baisse:
            self.vy += GRAVITY

        # Mouvement horizontal
        nouvelle_x = self.x + self.vx * dt
        if 0 <= nouvelle_x <= niveau_largeur - 1:
            self.x = nouvelle_x

        # Mouvement vertical
        nouvelle_y = self.y + self.vy * dt

        # Collision avec le sol
        on_sol = False
        for sol in sols:
            sol_rect = Rectangle(sol.x, sol.y, sol.width, sol.height)
            player_rect = Rectangle(
                int(self.x), int(nouvelle_y),
                self.largeur, self.hauteur
            )
            if self._rects_overlap(player_rect, sol_rect):
                if self.vy < 0:
                    nouvelle_y = sol.y + sol.height
                    self.vy = 0
                    on_sol = True
                    self.est_saut = False

        self.y = nouvelle_y

        # Limite droite du niveau
        if self.x >= niveau_largeur - 1:
            self.x = niveau_largeur - 1

        # Timer attaque
        if self.en_attaque:
            self.temps_attaque -= dt
            if self.temps_attaque <= 0:
                self.en_attaque = False

    def get_rect(self) -> Rectangle:
        """Retourne le rectangle du joueur."""
        return Rectangle(int(self.x), int(self.y), self.largeur, self.hauteur)

    @staticmethod
    def _rects_overlap(r1: Rectangle, r2: Rectangle) -> bool:
        """Vérifie si deux rectangles se chevauchent."""
        return not (r1.x + r1.width < r2.x or r2.x + r2.width < r1.x
                    or r1.y + r1.height < r2.y or r2.y + r2.height < r1.y)


class Crabe:
    """Un crabe ennemi."""

    def __init__(self, data: CrabeConfig) -> None:
        self.x = data.x
        self.y = data.y
        self.width = data.width
        self.height = data.height
        self.vitesse = data.vitesse
        self.direction = data.direction
        self.alive = data.alive
        self.patrol_start = data.patrol_start
        self.patrol_end = data.patrol_end

    def update(self, dt: float) -> None:
        """Met à jour la position du crabe."""
        if not self.alive:
            return
        self.x += self.direction * self.vitesse * dt
        if self.x <= self.patrol_start:
            self.direction = 1
        elif self.x >= self.patrol_end:
            self.direction = -1

    def get_rect(self) -> Rectangle:
        return Rectangle(int(self.x), int(self.y), self.width, self.height)


class PrototypeJeu(arcade.Window):
    """Fenêtre principale du prototype Crab Rush."""

    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, title="Crab Rush — Prototype",
                         resizable=False)
        self.clear_color = COULEUR_CIEL
        self.niveau = creer_niveau()
        self.joueur = Joueur(self.niveau["depart"].x, self.niveau["depart"].y)
        self.crabes = [Crabe(c) for c in self.niveau["crabes"]]
        self.sols = self.niveau["sols"]
        self.obstacles_bas = self.niveau["obstacles_bas"]
        self.obstacles_haut = self.niveau["obstacles_haut"]
        self.camera_x = 0
        self.touches: set = set()
        self.temps_ecoule = 0.0
        self.victoire = False
        self.defaite = False
        self.message = ""

    def on_key_press(self, touche: int, mod: int) -> None:
        """Gère les pressions de touche."""
        self.touches.add(touche)
        if touche == arcade.key.R:
            self.reinitialiser()
        elif touche == arcade.key.ESCAPE:
            self.close()

    def on_key_release(self, touche: int, mod: int) -> None:
        """Gère les relâchements de touche."""
        self.touches.discard(touche)

    def on_update(self, dt: float) -> None:
        """Met à jour la logique du jeu."""
        if self.victoire or self.defaite:
            return

        self.temps_ecoule += dt

        # Déplacement
        dx = 0
        if arcade.key.RIGHT in self.touches or arcade.key.D in self.touches:
            dx = 1
        elif arcade.key.LEFT in self.touches or arcade.key.Q in self.touches:
            dx = -1
        self.joueur.deplacer(dx, self.touches)
        self.joueur.se_baisser(
            arcade.key.DOWN in self.touches or arcade.key.S in self.touches
        )
        self.joueur.update(dt, self.sols, LEVEL_WIDTH)

        # Mise à jour crabes
        for crabe in self.crabes:
            crabe.update(dt)

        # Collision joueur-crabe
        joueur_rect = self.joueur.get_rect()
        for crabe in self.crabes:
            if crabe.alive:
                if self._rects_overlap(joueur_rect, crabe.get_rect()):
                    self.defaite = True
                    self.message = "🦀 Pincé par un crabe ! Appuie sur R pour réessayer."
                    return

        # Attaque joueur
        if self.joueur.en_attaque:
            for crabe in self.crabes:
                if crabe.alive:
                    crabe_rect = crabe.get_rect()
                    attack_rect = Rectangle(
                        int(self.joueur.x) + (30 if self.joueur.facing_right else -30),
                        int(self.joueur.y),
                        30, 30
                    )
                    if self._rects_overlap(attack_rect, crabe_rect):
                        crabe.alive = False

        # Collision avec obstacles bas (trous)
        for obs in self.obstacles_bas:
            obs_rect = Rectangle(obs.x, obs.y, obs.width, obs.height)
            if self._rects_overlap(joueur_rect, obs_rect):
                self.defaite = True
                self.message = "💀 Tu es tombé dans un trou ! Appuie sur R pour réessayer."
                return

        # Collision avec obstacles haut (se baisser)
        for obs in self.obstacles_haut:
            obs_rect = Rectangle(obs.x, obs.y, obs.width, obs.height)
            if self._rects_overlap(joueur_rect, obs_rect):
                self.defaite = True
                self.message = "🚧 Obstacle ! Tu devais te baisser ! Appuie sur R."
                return

        # Victoire
        if self.joueur.x >= self.niveau["arrivee"].x:
            self.victoire = True
            self.message = (
                f"🎉 Sauvetage réussi !\n"
                f"Temps : {self.temps_ecoule:.1f}s\n"
                f"Appuie sur R pour recommencer."
            )

        # Camera suit le joueur
        self.camera_x = self.joueur.x - SCREEN_WIDTH / (2 * TILE_SIZE)

    def on_draw(self) -> None:
        """Dessine le jeu."""
        self.clear()
        arcade.draw_text(
            f"❤️ 1  |  ⏱ {self.temps_ecoule:.1f}s",
            10, SCREEN_HEIGHT - 30,
            color=COULEUR_TEXT, font_size=18, anchor_x="left"
        )
        arcade.draw_text(
            "Niveau 1 — Première Sauveterie",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30,
            color=COULEUR_TEXT, font_size=16, anchor_x="center"
        )
        arcade.draw_text(
            "Flèches=déplacer | Espace=sauter/attaquer | Bas=se baisser | R=recommencer",
            SCREEN_WIDTH // 2, 20,
            color=COULEUR_TEXT, font_size=12, anchor_x="center"
        )

        # Dessiner le niveau avec camera
        self._dessiner_niveau()

        # Messages de fin
        if self.victoire:
            self._dessiner_texte_centre(self.message, COULEUR_TEXT, 28)
        elif self.defaite:
            self._dessiner_texte_centre(self.message, arcade.color.RED, 28)

    def _dessiner_niveau(self) -> None:
        """Dessine le niveau avec défilement."""
        # Ciel (fond)
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH,
            0, SCREEN_HEIGHT,
            COULEUR_CIEL
        )

        # Sols
        for sol in self.sols:
            px = sol.x * TILE_SIZE - self.camera_x * TILE_SIZE
            py = sol.y * TILE_SIZE
            arcade.draw_lrbt_rectangle_filled(
                px, px + sol.width * TILE_SIZE,
                py, py + sol.height * TILE_SIZE,
                COULEUR_SABLE
            )

        # Trous (obstacles bas)
        for obs in self.obstacles_bas:
            px = obs.x * TILE_SIZE - self.camera_x * TILE_SIZE
            py = obs.y * TILE_SIZE
            arcade.draw_lrbt_rectangle_filled(
                px, px + obs.width * TILE_SIZE,
                py, py + obs.height * TILE_SIZE,
                COULEUR_TROU
            )

        # Obstacles haut
        for obs in self.obstacles_haut:
            px = obs.x * TILE_SIZE - self.camera_x * TILE_SIZE
            py = obs.y * TILE_SIZE
            arcade.draw_lrbt_rectangle_filled(
                px, px + obs.width * TILE_SIZE,
                py, py + obs.height * TILE_SIZE,
                COULEUR_OBSTACLE_HAUT
            )

        # Arrivée (eau)
        arr_x = self.niveau["arrivee"].x * TILE_SIZE - self.camera_x * TILE_SIZE
        arr_y = self.niveau["arrivee"].y * TILE_SIZE
        arcade.draw_lrbt_rectangle_filled(
            arr_x, arr_x + TILE_SIZE,
            arr_y, arr_y + TILE_SIZE,
            COULEUR_EAU
        )
        arcade.draw_text("🏊", arr_x + TILE_SIZE // 2, arr_y + TILE_SIZE // 2 + 5,
                         color=COULEUR_TEXT, font_size=20, anchor_x="center")

        # Départ
        dep_x = self.niveau["depart"].x * TILE_SIZE - self.camera_x * TILE_SIZE
        dep_y = self.niveau["depart"].y * TILE_SIZE
        arcade.draw_lrbt_rectangle_filled(
            dep_x, dep_x + TILE_SIZE,
            dep_y, dep_y + TILE_SIZE,
            arcade.color.GREEN_YELLOW
        )

        # Crabes
        for crabe in self.crabes:
            if crabe.alive:
                px = crabe.x * TILE_SIZE - self.camera_x * TILE_SIZE
                py = crabe.y * TILE_SIZE
                arcade.draw_circle_filled(
                    px + crabe.width // 2, py + crabe.height // 2,
                    crabe.width // 2, COULEUR_CRABE
                )
                arcade.draw_text("🦀", px + crabe.width // 2, py + crabe.height // 2 + 5,
                                 color=COULEUR_TEXT, font_size=16, anchor_x="center")

        # Joueur
        px_j = self.joueur.x * TILE_SIZE - self.camera_x * TILE_SIZE
        py_j = self.joueur.y * TILE_SIZE
        arcade.draw_lrbt_rectangle_filled(
            px_j, px_j + self.joueur.largeur,
            py_j, py_j + self.joueur.hauteur,
            COULEUR_JOUEUR
        )
        # Icône joueur
        arcade.draw_text("🏊‍♂️", px_j + self.joueur.largeur // 2,
                         py_j + self.joueur.hauteur // 2 + 5,
                         color=COULEUR_TEXT, font_size=16, anchor_x="center")

        # Indicateur d'attaque
        if self.joueur.en_attaque:
            attack_x = px_j + (self.joueur.largeur if self.joueur.facing_right else 0)
            attack_y = py_j
            arcade.draw_lrbt_rectangle_filled(
                attack_x, attack_x + 30,
                attack_y, attack_y + 30,
                arcade.color.YELLOW
            )

    def _rects_overlap(self, r1: Rectangle, r2: Rectangle) -> bool:
        """Vérifie si deux rectangles se chevauchent."""
        return not (r1.x + r1.width < r2.x or r2.x + r2.width < r1.x
                    or r1.y + r1.height < r2.y or r2.y + r2.height < r1.y)

    def _dessiner_texte_centre(self, texte: str, couleur, taille_font: int) -> None:
        """Dessine un texte centré."""
        lignes = texte.split("\n")
        y = SCREEN_HEIGHT // 2
        for ligne in lignes:
            arcade.draw_text(
                ligne,
                SCREEN_WIDTH // 2, y,
                color=couleur, font_size=taille_font, anchor_x="center"
            )
            y -= taille_font + 10

    def reinitialiser(self) -> None:
        """Réinitialise le jeu."""
        self.niveau = creer_niveau()
        self.joueur = Joueur(self.niveau["depart"].x, self.niveau["depart"].y)
        self.crabes = [Crabe(c) for c in self.niveau["crabes"]]
        self.sols = self.niveau["sols"]
        self.obstacles_bas = self.niveau["obstacles_bas"]
        self.obstacles_haut = self.niveau["obstacles_haut"]
        self.camera_x = 0
        self.temps_ecoule = 0.0
        self.victoire = False
        self.defaite = False
        self.message = ""


def main() -> None:
    """Lance le prototype."""
    jeu = PrototypeJeu()
    jeu.run()


if __name__ == "__main__":
    main()
