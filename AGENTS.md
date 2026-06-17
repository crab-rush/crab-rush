# Instructions pour l'agent IA — Crab Rush

## Principes fondamentaux

Ces principes guident la façon dont tu travailles et ce que tu écris. Ils s'appliquent à toutes tes interactions avec ce dépôt.

- **Uniquement l'essentiel.** Ne répète pas ce qui est déjà dans le code, le README ou les commentaires. Documente uniquement ce qui n'est pas directement observable.
- **Quoi et pourquoi, pas comment.** Décris les objectifs et les contraintes. Fais confiance au lecteur (humain ou IA) pour trouver l'approche.
- **Renforce ce qui compte, reste souple sur le reste.** Sois explicite sur les choses qui causeraient de vraies erreurs si elles étaient ignorées. Ignore tout le reste.
- **Adapte-toi à la complexité.** Un petit projet mérite un fichier court. Ne remplis pas avec des conseils génériques.
- **Vérifie avec des preuves.** Ne documente rien que tu n'as pas confirmé avec le code ou les outils.
- **Itère, ne génère pas.** Échange → affine. Préfère les petites questions fréquentes aux longs développements autonomes.
- **Sois opinionné.** Conteste, suggère des alternatives, signale les risques — avec des raisons. Sois un collaborateur, pas un secrétaire.

## Aperçu du projet

**Crab Rush** est un jeu éducatif développé avec [Python Arcade](https://arcade.academy/). Il est conçu pour de jeunes apprenants francophones qui découvrent la programmation, le travail d'équipe et l'utilisation de l'IA dans le développement.

- **Langage :** Python 3.12+
- **Moteur de jeu :** Arcade (`pip install arcade`)
- **Tests :** pytest
- **Langue du code :** Tout commentaire, docstring et texte du jeu (UI, messages) doit être en **français**.

## Commandes clés

```bash
# Installer les dépendances (pip)
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# ou .venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Lancer le jeu
python main.py

# Lancer les tests
pytest

# Lancer les tests avec sortie détaillée
pytest -v
```

## Workflow Git

Ce projet est utilisé par des jeunes apprenants qui ne maîtrisent pas encore Git/GitHub. Le workflow est volontairement simple :

1. **Toujours commencer par tirer les changements :** `git pull`
2. **Travailler directement sur `main`** — pas de branches, pas de PR
3. **Avant de commit : toujours lancer les tests**
   ```bash
   pytest
   ```
4. **Commit en français, avec un message descriptif :**
   ```bash
   git add .
   git commit -m "ajout: écran de titre du jeu"
   ```
5. **Pousser les changements :** `git push`

### En cas de conflit de fusion

Si `git pull` génère un conflit :
1. Résoudre automatiquement le conflit dans les fichiers concernés
2. Relancer les tests : `pytest`
3. Expliquer à l'utilisateur quel était le problème et comment il a été résolu, puis lui demander une validation manuelle
4. Ajouter une note dans le commit expliquant le conflit résolu :
   ```bash
   git commit -m "correction: résolution de conflit dans main.py (fusion des écrans de titre et de jeu)"
   ```
5. Pousser : `git push`

## Conventions de code

- **Commentaires et docstrings en français.** Chaque fonction et classe doit avoir une docstring descriptive.
- **Code simple et lisible.** Privilégie la clarté sur l'élégance. Ce code est lu par des débutants.
- **Nommage :** Utilise des noms explicites en français pour les variables et fonctions liées au jeu (ex: `deplacer_crabe`, `verifier_collision`). Les noms techniques en anglais sont acceptés (ex: `on_draw`, `__init__`).
- **Gestion d'erreurs :** Utilise des `try/except` pour les opérations critiques (chargement de fichiers, réseau). Affiche des messages en français.
- **Fichiers de jeu :** Place les sprites, sons et images dans le dossier `assets/`.

## Structure du projet

```
crab-rush/
├── main.py          # Point d'entrée — la fenêtre du jeu et la boucle principale
├── assets/          # Ressources du jeu (images, sons)
├── tests/           # Tests pytest
├── requirements.txt # Dépendances (pip)
├── pyproject.toml   # Configuration du projet
├── README.md        # Documentation pour les humains
└── AGENTS.md        # Ce fichier — instructions pour l'IA
```

Les jeunes développeurs peuvent commencer avec un seul fichier `main.py` et ajouter des modules progressivement. Pas besoin de structure complexe au début.

## Points d'attention pour la revue de code

Lorsque tu modifies ou reviews du code, fais particulièrement attention à :

- **Lisibilité pour les débutants** — Le code doit être compréhensible par quelqu'un qui débute en Python. Évite les patterns avancés (comprehensions complexes, metaclasses, décorateurs) sauf si explicitement demandé.
- **Chargement des assets** — Vérifie que les chemins vers `assets/` sont relatifs et robustes. Un chemin cassé est l'erreur la plus silencieuse et frustrante pour un débutant.
- **Boucle de jeu** — Assure-toi que `on_update()` et `on_draw()` restent légers. Les calculs lourds doivent être déplacés hors de ces méthodes.
- **Tests pertinents** — Les tests doivent couvrir la logique du jeu (collisions, score, états) plutôt que l'affichage Arcade (qui est difficile à tester unitairement).
