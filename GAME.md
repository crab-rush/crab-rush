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
- **Espace / Z / Haut / W** — Sauter
- **Bas / S** — Se baisser ( Éviter les obstacles hauts)
- **Espace** — Frapper les crabes (attaque courte portée devant le joueur)
- **R** — Recommencer le niveau (après mort ou victoire)
- **Échap** — Quitter / revenir au menu

### Système de combat
- Le joueur dispose d'une **attaque courte portée** (30px devant lui, dans la direction où il fait face)
- L'attaque dure **0.3 secondes** et se recharge immédiatement
- Un crabe touché par l'attaque est **éliminé**
- Un crabe mort reste mort (disparu du niveau)

### Système de vies et survie
- Le joueur commence chaque niveau avec **1 vie**
- Toucher un crabe ou un obstacle = **mort instantanée**
- À la mort : écran de défaite avec option de recommencer ou de revivre

### Système de pièces
- Des pièces 🪙 sont dispersées dans le niveau
- Les pièces se collectent automatiquement en les touchant
- Le nombre de pièces est affiché à l'écran
- Les pièces sont conservées entre les niveaux (monnaie persistante)

### Système de revivre
- Après la mort, le joueur peut choisir de **payer des pièces pour revivre**
- Le coût de revivre est **3 pièces**
- Si le joueur n'a pas assez de pièces, il doit recommencer le niveau
- Revivre remet le joueur à sa position de mort (pas au début du niveau)

### Niveaux et difficulté
- Le niveau 1 est un parcours simple avec 4 crabes et 5 trous
- Les niveaux futurs ajouteront : plus de crabes, plus de trous, des obstacles hauts, des pièces

## Fonctionnalités implémentées

- [x] Écran de titre avec bouton "Jouer"
- [x] Menu → transition vers le niveau 1
- [x] Déplacement du joueur (gauche / droite)
- [x] Sauter
- [x] Se baisser
- [x] Frapper les crabes
- [x] Crabes ennemis avec patrouille
- [x] Trous (obstacles bas à sauter)
- [x] Obstacles hauts (à éviter en se baissant)
- [x] Système de mort et recommencement
- [x] Timer
- [x] Victoire et défaite
- [ ] Système de pièces 🪙 (à implémenter)
- [ ] Système de revivre (à implémenter)
- [ ] Boutique d'améliorations (à implémenter)
- [ ] Écran de sélection de niveaux (à implémenter)

## Fonctionnalités planifiées

- 🪙 Pièces à collecter (Session 2)
- 🏪 Boutique d'améliorations entre les niveaux (Session 2)
- 🔄 Système de revivre — payer 3 pièces pour continuer (Session 3)
- 🗺️ Écran de sélection de niveaux (Session 4)
- ⬆️ Améliorations du personnage : vie supplémentaire, vitesse, force (Session 5)
- 🌊 Niveaux supplémentaires avec difficulté progressive
- 🔊 Sons et musique
- 🎨 Sprites et graphismes

## Notes de développement

- Le prototype `test_game.py` contient déjà la base du gameplay (déplacement, saut, combat, obstacles, caméra). Il servira de base pour l'intégration.
- `main.py` contient l'écran de titre. Il faudra relier le bouton "Jouer" au prototype.
- Les noms de variables et fonctions sont en français pour les débutants.
- Les couleurs sont utilisées à la place des sprites pour l'instant (pas d'assets graphiques).
