# 🦀 Crab Rush — Document de jeu

## Vue d'ensemble

Jeu de plateforme 2D défilement latéral. Le joueur incarne un maître nageur qui doit traverser une plage pour sauver une personne qui se noie. Il affronte des crabes ennemis, collecte des pièces et utilise ses ressources pour survivre.

## Règles du jeu

- Le joueur a **une seule vie**. Toucher un crabe ou un obstacle = mort = recommencer le niveau.
- Le joueur peut **tuer les crabes** en les frappant (touche Espace).
- Le joueur peut **collecter des pièces** 🪙 pour les dépenser plus tard.
- Le joueur peut **acheter des améliorations** dans une boutique entre les niveaux.
- Le joueur peut **payer des pièces pour revivre** après la mort (sans recommencer le niveau).
- Le niveau se termine quand le joueur atteint l'arrivée (personne à sauver).
- Le temps est affiché — plus le joueur est rapide, mieux c'est.

## Mécaniques

### Contrôles
- **Flèches / ZQSD** — Se déplacer (gauche / droite)
- **Z / Haut / W** — Sauter (uniquement quand au sol)
- **Bas / S** — Se baisser (éviter les obstacles hauts)
- **Espace** — Frapper les crabes (attaque courte portée devant le joueur, dure 0.3s)
- **R** — Recommencer le niveau (après mort ou victoire)
- **Échap** — Revenir au menu (depuis le jeu ou les paramètres)

### Système de saut
- Le joueur **saute** avec Z / Haut / W
- La montée et la descente sont à la **même vitesse** (gravité constante)
- Le saut est **court** — pas trop haut, pour garder le jeu rythmé
- Le joueur peut sauter uniquement quand il est au sol

### Système de combat
- Le joueur dispose d'une **attaque courte portée** (30px devant lui, dans la direction où il fait face)
- L'attaque dure **0.3 secondes** et se recharge immédiatement
- Un crabe touché par l'attaque est **éliminé**
- Un crabe mort reste mort (disparu du niveau)

### Système de vies et survie
- Le joueur commence chaque niveau avec **1 vie**
- Toucher un crabe ou un obstacle = **mort instantanée**
- À la mort : écran de défaite avec option de recommencer (touche R)

### Système de pièces
- Des pièces 🪙 sont dispersées dans le niveau
- Les pièces se collectent automatiquement en les touchant
- Le nombre de pièces est affiché à l'écran
- Les pièces sont conservées entre les niveaux (monnaie persistante)

### Système de revivre
- **Non implémenté.** Sera ajouté ultérieurement.
- Prévu : le joueur pourra payer des pièces pour revivre à sa position de mort.

### Niveaux et difficulté
- Le niveau 1 est un parcours simple avec 4 crabes et 5 trous
- Les niveaux futurs ajouteront : plus de crabes, plus de trous, des obstacles hauts, des pièces

## Fonctionnalités implémentées

- [x] Écran de titre avec bouton "Jouer"
- [x] Écran de titre avec fond d'image jungle (`background_jungle.png`)
- [x] Écran de paramètres (sliders musique/effets sonores, bouton quitter)
- [x] Menu → transition vers le niveau 1
- [x] Déplacement du joueur (gauche / droite)
- [x] Sauter
- [x] Se baisser
- [x] Frapper les crabes
- [x] Crabes ennemis avec patrouille
- [x] Trous (gaps dans le sol — le joueur tombe par gravité)
- [x] Obstacles hauts (à éviter en se baissant)
- [x] Système de mort et recommencement
- [x] Timer
- [x] Victoire et défaite
- [x] Écran de retour au menu (flèche en haut à gauche)
- [x] Écran de jeu avec fond d'image jungle défilant avec la caméra
- [x] Système de pièces 🪙 (2 pièces dans le niveau 1, collecte automatique, compteur persistant)
- [ ] Système de revivre (à implémenter)
- [ ] Boutique d'améliorations (à implémenter)
- [ ] Écran de sélection de niveaux (à implémenter)

## Fonctionnalités planifiées
- 🏪 Boutique d'améliorations entre les niveaux (Session 2)
- 🔄 Système de revivre — payer 3 pièces pour continuer (Session 3)
- 🗺️ Écran de sélection de niveaux (Session 4)
- ⬆️ Améliorations du personnage : vie supplémentaire, vitesse, force (Session 5)
- 🌊 Niveaux supplémentaires avec difficulté progressive
- 🔊 Sons et musique
- 🎨 Sprites et graphismes

## Notes de développement

- `game.py` contient le gameplay complet du niveau 1 (déplacement, saut, combat, obstacles, caméra, victoire/défaite).
- `main.py` contient l'écran de titre et l'écran de paramètres. Le bouton "Jouer" lance le jeu via `game.py`.
- `niveau.py` est une version antérieure du gameplay, conservée à titre de référence.
- Les noms de variables et fonctions sont en français pour les débutants.
- `main.py` contient l'écran de titre et l'écran de paramètres. Le bouton "Jouer" lance le jeu via `game.py`.
- `game.py` contient le gameplay complet du niveau 1 (déplacement, saut, combat, obstacles, caméra, victoire/défaite).
- Le fond d'écran `assets/background_jungle.png` est utilisé sur le menu et l'écran de jeu (défilement avec la caméra).
