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
- [Agent IA Pi](https://pi.dev/) (optionnel, pour l'aide au développement)

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

1. Clone le dépôt
2. Crée tes modifications
3. Écris des tests pour tes nouvelles fonctionnalités
4. Lance les tests : `pytest`
5. Commit et push

Pour plus de détails sur le workflow, consulte [`AGENTS.md`](AGENTS.md).
