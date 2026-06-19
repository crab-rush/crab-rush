# 🦀 Crab Rush

Un jeu développé par et pour des jeunes apprenants. L'objectif est d'apprendre à coder, travailler en équipe, et découvrir l'intelligence artificielle appliquée au développement de jeux vidéo.

## 🛠 Stack technique

| Composant | Technologie | Documentation |
|-----------|-------------|---------------|
| Langage | Python 3.12+ | [docs.python.org](https://docs.python.org/3/) |
| Moteur de jeu | [Arcade](https://api.arcade.academy/) | [arcade.academy](https://arcade.academy/) |
| Tests | pytest | [docs.pytest.org](https://docs.pytest.org/) |
| Gestion de paquets | pip | [pip.pypa.io](https://pip.pypa.io/) |

## 🚀 Installation et lancement

### Prérequis
- Python 3.12 ou plus récent ([python.org](https://www.python.org/downloads/))
- Git — macOS/Linux : inclus avec Git ([git-scm.com](https://git-scm.com/)), Windows : [Git for Windows](https://gitforwindows.org/)
- [Agent IA Pi](https://pi.dev/) — ton assistant de développement IA (recommandé !)

### Installer les dépendances
```bash
# Crée un environnement virtuel
python -m venv .venv

# Active-le
# Sur macOS/Linux :
source .venv/bin/activate
# Sur Windows (PowerShell) :
.venv\Scripts\activate

# Installe les dépendances
pip install -r requirements.txt
```

### Lancer le jeu
```bash
python main.py
```

## 🎯 Objectifs du jeu

_Cette section sera complétée par l'équipe. Elle décrit le but du jeu, les règles, et les mécaniques principales._

## 📁 Structure du projet

```
crab-rush/
├── main.py          # Point d'entrée du jeu
├── assets/          # Sprites, sons, images
├── tests/           # Tests unitaires
├── requirements.txt # Dépendances Python
├── pyproject.toml   # Configuration du projet
├── README.md        # Ce fichier
└── AGENTS.md        # Instructions pour l'agent IA
```

## 🤝 Contribuer

Ce projet est ouvert à tous les apprenants ! Voici comment contribuer :

### 🤖 Travailler avec Pi (l'agent IA)

Pi est ton assistant de développement. Il t'aide à :

- **Comprendre le code** — pose-lui des questions sur n'importe quelle partie du jeu
- **Implémenter des features** — dis-lui ce que tu veux ajouter, il te guide étape par étape
- **Corriger des bugs** — décris le problème, il t'aide à le résoudre
- **Apprendre les bonnes pratiques** — tests, structure, nommage, tout est expliqué

**Comment commencer :**

1. Ouvre une session avec Pi (`/new`)
2. Dis-lui ce que tu veux faire, par exemple :
   - _"Je veux ajouter un score au jeu"_
   - _"Je veux créer le niveau 1"_
   - _"Il y a un bug quand je clique sur le bouton Jouer"_
3. Pi te posera des questions pour comprendre ton idée
4. Ensemble, vous planifierez les étapes, tu valideras chacune, et Pi écrira le code
5. Une fois terminé, Pi pushera les changements automatiquement (avec ton accord)

**Conseil :** Fais une chose à la fois. Une session = une feature. Si tu veux faire plusieurs trucs, termine la première, puis lance `/new` pour la suivante.

### 📋 Workflow en 6 étapes

Quand tu travailles avec Pi, voici ce qui se passe :

1. **Contexte** — Pi vérifie l'état du dépôt et te résume ce qui a été fait
2. **Cadrage** — On définit ensemble ce qu'on va faire (une seule petite chose)
3. **Spécifications** — On écrit les règles dans `GAME.md` avant de coder
4. **Implémentation** — Pi écrit le code, tu valides chaque étape
5. **Validation** — Tests + lancement du jeu + ta vérification
6. **Sync Git** — Commit et push (avec ton accord)

### 📝 Sans Pi

Si tu préfères coder toi-même :

1. Clone le dépôt
2. Lis `GAME.md` pour comprendre ce qui a déjà été fait
3. Choisis une feature dans "Fonctionnalités planifiées"
4. Crée tes modifications
5. Écris des tests pour tes nouvelles fonctionnalités
6. Lance les tests : `pytest`
7. Commit et push

Pour plus de détails sur le workflow, consulte [`AGENTS.md`](AGENTS.md).
