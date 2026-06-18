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
- **Explique toujours ce que tu fais.** Ce projet est un projet d'apprentissage. L'utilisateur doit comprendre ce qui se passe, pourquoi, et ce qui a changé. Pas de boîte noire.
- **Le code et GAME.md sont toujours synchronisés.** Chaque modification du code doit être reflétée dans GAME.md, et vice-versa. C'est une règle non-négociable.

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

## Workflow de développement

Ce projet est utilisé par des jeunes apprenants qui ne maîtrisent pas encore Git/GitHub. L'agent gère le workflow en **5 phases**, avec validation utilisateur aux étapes clés.

### Phase 1 — Contexte (toujours)

Au début de **chaque session**, l'agent doit :

1. Vérifier l'état du dépôt avec `git status` et afficher un rapport clair à l'utilisateur.
2. Tirer les derniers changements avec `git pull` pour travailler sur la version la plus récente.
3. **Lire `GAME.md`** — c'est la première action de compréhension du projet. Ce fichier contient les specs à jour du jeu.
4. Présenter à l'utilisateur un résumé de l'état actuel : ce qui a été fait, ce qui reste à faire, et où on en est par rapport à GAME.md.

### Phase 2 — Brainstorm (si nécessaire)

Avant d'implémenter quoi que ce soit :

1. Discuter avec l'utilisateur pour comprendre ce qu'il veut faire.
2. Proposer un plan clair et détaillé de ce qui sera fait dans la session.
3. S'assurer que tout est clair entre l'agent et l'utilisateur avant de passer à l'implémentation.
4. Adapter la profondeur de la discussion à la complexité de la tâche (une petite feature n'a pas besoin d'un long brainstorm).

### Phase 3 — Implémentation

Pendant l'implémentation :

1. **Écrire le code** avec les conventions du projet (français, lisible, tests).
2. **Écrire les tests unitaires** pour chaque nouvelle fonctionnalité.
3. **Mettre à jour `GAME.md`** en conséquence.
4. Les tests doivent passer avant de passer à la phase suivante.

### Phase 4 — Validation utilisateur

1. Demander à l'utilisateur de tester le jeu et valider les changements.
2. Si l'utilisateur demande des ajustements, retourner à la Phase 3.
3. Si l'utilisateur valide, passer à la Phase 5.

### Phase 5 — Sync Git (avec validation)

L'agent ne fait **jamais** de commit ou push sans validation explicite de l'utilisateur.

1. Proposer à l'utilisateur : "Je vais tirer les derniers changements, commit avec le message `[message]`, puis push. OK ?"
2. L'utilisateur peut :
   - **Valider** → l'agent exécute les commandes.
   - **Modifier** → l'agent ajuste le message ou le plan.
   - **Faire lui-même** → l'agent propose les commandes et l'utilisateur les tape.
3. L'agent commence par un `git pull` pour éviter les conflits.
4. Puis `git add`, `git commit` (en français, message descriptif), et `git push`.
5. En cas de conflit : l'agent résout, relance les tests, explique à l'utilisateur, puis continue après validation.
6. **Rapport final** : l'agent résume ce qui a été fait dans la session.

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
├── GAME.md          # Document de jeu — règles, mécaniques, fonctionnalités
├── CODEOWNERS       # Propriétaires des fichiers (chaque dev s'auto-assigne)
├── LICENSE          # Licence MIT
├── requirements.txt # Dépendances (pip)
├── pyproject.toml   # Configuration du projet
├── README.md        # Documentation pour les humains (vue d'ensemble)
└── AGENTS.md        # Ce fichier — instructions pour l'agent IA
```

Les jeunes développeurs peuvent commencer avec un seul fichier `main.py` et ajouter des modules progressivement. Pas besoin de structure complexe au début.

## Points d'attention pour la revue de code

Lorsque tu modifies ou reviews du code, fais particulièrement attention à :

- **Lisibilité pour les débutants** — Le code doit être compréhensible par quelqu'un qui débute en Python. Évite les patterns avancés (comprehensions complexes, metaclasses, décorateurs) sauf si explicitement demandé.
- **Chargement des assets** — Vérifie que les chemins vers `assets/` sont relatifs et robustes. Un chemin cassé est l'erreur la plus silencieuse et frustrante pour un débutant.
- **Boucle de jeu** — Assure-toi que `on_update()` et `on_draw()` restent légers. Les calculs lourds doivent être déplacés hors de ces méthodes.
- **Tests pertinents** — Les tests doivent couvrir la logique du jeu (collisions, score, états) plutôt que l'affichage Arcade (qui est difficile à tester unitairement).
- **Synchronisation GAME.md** — Vérifie toujours que GAME.md est à jour après chaque modification du code.
