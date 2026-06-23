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
GRAVITY = 1.5          # pixels/frame, tir vers le bas (vy diminue) - gravité augmentée
JUMP_FORCE = 30        # pixels/frame, vers le haut (vy positif = monter) - saut plus haut
MOVE_SPEED = 72        # pixels/frame (x3 vitesse)
LEVEL_WIDTH = 30       # nombre de cases de large

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

    # Sols : segments continus avec des trous (gaps) entre eux
    sols: List[Sol] = [
        Sol(x=0, y=0, width=4, height=1),   # sol 0-3 (y=0 à 40px)
        Sol(x=6, y=0, width=2, height=1),   # sol 6-7
        Sol(x=9, y=0, width=5, height=1),   # sol 9-13
        Sol(x=15, y=0, width=5, height=1),  # sol 15-19
        Sol(x=21, y=0, width=5, height=1),  # sol 21-25
        Sol(x=27, y=0, width=3, height=1),  # sol 27-29
    ]
    # Note : le sol va de y=0 à y=40px. Le joueur se pose SUR le sol (y=40px = tile 1)

    # Trous : positions des gaps dans le sol (pour le dessin uniquement)
    obstacles_bas: List[ObstacleBas] = [
        ObstacleBas(x=4, y=0, width=2, height=1),   # trou entre sol 0-3 et 6-7
        ObstacleBas(x=8, y=0, width=1, height=1),   # trou entre sol 6-7 et 9-13
        ObstacleBas(x=14, y=0, width=1, height=1),  # trou entre sol 9-13 et 15-19
        ObstacleBas(x=20, y=0, width=1, height=1),  # trou entre sol 15-19 et 21-25
        ObstacleBas(x=26, y=0, width=1, height=1),  # trou entre sol 21-25 et 27-29
    ]

    obstacles_haut: List[ObstacleHaut] = [
        ObstacleHaut(x=10, y=4, width=3, height=1),  # filet bas (à hauteur de tête)
        ObstacleHaut(x=16, y=4, width=2, height=1),  # branche (à hauteur de tête)
        ObstacleHaut(x=22, y=4, width=3, height=1),  # filet bas (à hauteur de tête)
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
        # Position en unités de tuiles (tiles)
        self.x = x
        self.y = y
        # Vitesse en pixels/frame
        self.vx = 0
        self.vy = 0
        # Dimensions en pixels
        self.largeur = 30
        self.hauteur_normale = 35
        self.hauteur_baisse = 20
        self.hauteur = self.hauteur_normale
        self.est_baisse = False
        self.est_saut = False
        self.est_sol = False  # Indique si le joueur est posé au sol
        self.en_attaque = False
        self.temps_attaque = 0.0
        self.facing_right = True
        self.vie = 1

    def deplacer(self, dx: int, touches: set, dt: float = 1.0) -> None:
        """Déplace le joueur horizontalement."""
        # Sauter uniquement si on est au sol
        if arcade.key.UP in touches or arcade.key.W in touches or arcade.key.Z in touches:
            if self.est_sol:
                self.vy = JUMP_FORCE  # Positif = monter (y augmente vers le haut)
                self.est_saut = True
                self.est_sol = False

        # Attaque
        if arcade.key.SPACE in touches and not self.en_attaque:
            self.en_attaque = True
            self.temps_attaque = 0.3

        # Mouvement horizontal (vx en pixels/frame)
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
        # Mouvement horizontal (convertir pixels en tiles)
        nouvelle_x = self.x + (self.vx * dt) / TILE_SIZE
        if 0 <= nouvelle_x <= niveau_largeur - 1:
            self.x = nouvelle_x

        # Vérifier si le joueur est au-dessus d'un segment de sol (horizontalement)
        centre_x_pixel = self.x * TILE_SIZE + self.largeur / 2
        on_sol = False
        sol_actif = None
        sol_haut_pixel = 0
        for sol in sols:
            sol_gauche = sol.x * TILE_SIZE
            sol_droite = (sol.x + sol.width) * TILE_SIZE
            sol_haut = (sol.y + sol.height) * TILE_SIZE
            if sol_gauche <= centre_x_pixel < sol_droite:
                on_sol = True
                sol_actif = sol
                sol_haut_pixel = sol_haut
                break

        # Vérifier le contact vertical avec le sol
        joueur_bas_pixel = self.y * TILE_SIZE

        if on_sol and sol_actif:
            if joueur_bas_pixel < sol_haut_pixel:
                # Joueur EN DESSOUS ou DANS le sol → le remonter dessus
                self.y = sol_haut_pixel / TILE_SIZE
                self.vy = 0
                self.est_sol = True
                self.est_saut = False
            elif joueur_bas_pixel < sol_haut_pixel + 10:
                # Joueur proche du sol (contact)
                if self.vy <= 0:
                    # Ne monte pas → reste au sol
                    self.vy = 0
                    self.est_sol = True
                    self.est_saut = False
                else:
                    # Monte (saut) → en l'air
                    self.est_sol = False
                    self.vy -= GRAVITY
            else:
                # Trop loin du sol → en l'air
                self.est_sol = False
                self.vy -= GRAVITY
        else:
            # Pas de sol sous le joueur (trou ou bord)
            self.est_sol = False
            self.vy -= GRAVITY

        # Mouvement vertical (convertir pixels en tiles)
        nouvelle_y = self.y + (self.vy * dt) / TILE_SIZE
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
        """Retourne le rectangle du joueur en pixels."""
        return Rectangle(
            int(self.x * TILE_SIZE),
            int(self.y * TILE_SIZE),
            self.largeur,
            self.hauteur
        )

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
        # Hitbox très réduite (cercle visuel vs rectangle)
        # Le crabe est dessiné en cercle, hitbox ~30% de la taille
        marge = int(self.width * 0.35)  # 35% de marge de chaque côté
        return Rectangle(
            int(self.x) * TILE_SIZE + marge,
            int(self.y) * TILE_SIZE + marge,
            self.width - 2 * marge,
            self.height - 2 * marge
        )


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
        self.joueur.deplacer(dx, self.touches, dt)
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
                    attack_x = int(self.joueur.x * TILE_SIZE) + (self.joueur.largeur if self.joueur.facing_right else -30)
                    attack_rect = Rectangle(attack_x, int(self.joueur.y * TILE_SIZE), 30, self.joueur.hauteur)
                    if self._rects_overlap(attack_rect, crabe_rect):
                        crabe.alive = False

        # Le joueur tombe dans un trou automatiquement via la physique
        if self.joueur.y * TILE_SIZE < -200:
            self.defaite = True
            self.message = "💀 Tu es tombé dans un trou ! Appuie sur R pour réessayer."

        # Collision avec obstacles haut (se baisser pour passer dessous)
        for obs in self.obstacles_haut:
            centre_x_pixel = self.joueur.x * TILE_SIZE + self.joueur.largeur / 2
            obs_gauche = obs.x * TILE_SIZE
            obs_droite = (obs.x + obs.width) * TILE_SIZE
            if obs_gauche <= centre_x_pixel < obs_droite:
                obs_haut_pixel = (obs.y + obs.height) * TILE_SIZE
                joueur_haut_pixel = self.joueur.y * TILE_SIZE + self.joueur.hauteur
                if joueur_haut_pixel > obs_haut_pixel:
                    if not self.joueur.est_baisse:
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
        self.camera_x = (self.joueur.x * TILE_SIZE - SCREEN_WIDTH / 2) / TILE_SIZE

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
