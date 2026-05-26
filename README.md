# SAE 2.04 – Exploitation d'une base de données

**BUT Informatique · IUT de Créteil-Vitry · Département Informatique**

---

## Contexte du projet

Cette SAE (2.04 : Exploitation d'une base de données) vise à concevoir
et alimenter une base de données relationnelle à partir de données publiques
publiées par AMELI sur le portail [data.ameli.fr](https://data.ameli.fr).

### Objectif pédagogique

Le projet entre dans la **Compétence 4** du référentiel du BUT Informatique :
*Concevoir et mettre en place une base de données à partir d'un cahier des charges*, avec trois apprentissages critiques :

- **AC1** – Mettre à jour et interroger une base de données relationnelle (en requêtes directes ou via une application)
- **AC2** – Visualiser des données
- **AC3** – Concevoir une base de données relationnelle à partir d'un cahier des charges

### Provenance des données

L'Assurance Maladie publie en open data des informations sur les professionnels
de santé libéraux via le portail data.ameli.fr, qui s'appuie sur la plateforme
**OpenDataSoft**.
Ces données couvrent une trentaine de professions et spécialités médicales,
de 2010 jusqu'à aujourd'hui.

---

## Architecture des fichiers du projet

Le code est structuré en plusieurs scripts PHP/Python qui correspondent à la progression des séances (tutoriels de test puis application finale) :

* **Tutoriels et Tests (SQL brut / Premier ORM) :**
  * `connexion.py` : Script de test pour valider la connexion à notre base MySQL distante.
  * `create_table_sql.py`, `insert_table_sql.py` et `select_table_sql.py` : Première manipulation de la base en écrivant directement du SQL brut (via la méthode `text()` de SQLAlchemy).
  * `model.py` : Premier essai de modèle ORM avec les tables de test `departement` et `formation`.
  * `create_tables_orm.py`, `insert_tables_orm.py`, `select_tables_orm.py` et `requetes_orm.py` : Scripts pour apprendre à insérer, lier et requêter les données avec la logique d'objets de SQLAlchemy.

* **Application Finale (Collecte et Dimensions Réelles) :**
  * `models_dimensions.py` : Fichier principal contenant la modélisation complète de nos tables finales (Régions, Départements, Professions, Tranches d'âge, Sexe, Types d'exercice, Secteurs, Niveaux d'honoraires et Prescriptions).
  * `create_tables.py` : Permet de générer automatiquement tout le schéma relationnel final dans MySQL.
  * `exploration_api.py` : Script utilisé pour analyser la structure JSON renvoyée par l'API Ameli.
  * `utils_api.py` : Contient la fonction globale pour automatiser les appels et gérer la pagination (`offset`/`limit`) d'OpenDataSoft.
  * `collecte_dim_geo_professions.py`, `collecte_dim_activite.py` et `collecte_dim_financier.py` : Scripts ETL de production chargés de récupérer toutes les nomenclatures distinctes sur l'API et de remplir nos tables ORM de manière propre.
  * `verification.py` : Script de contrôle final qui affiche le nombre de lignes présentes dans chaque table pour vérifier que tout est bien alimenté.
  * `nettoyage_db.py` : Script outil pour vider ou supprimer proprement les tables si nécessaire.


## Fonctionnement et chaîne d'exécution

Le projet s'est déroulé autour de trois grands axes (Administration, Programmation, et Exploitation de l'API) qui suivent cet ordre d'exécution :

1. Phase de test et de transition (Tutoriels)
Avant de lancer l'application finale, les premiers scripts permettent de prendre en main la base MySQL et de comparer les méthodes d'accès :

Test de connexion : Lancement de `connexion.py` pour valider les accès à la base de données distante.

Approche SQL brut : Utilisation de `create_table_sql.py` et `insert_table_sql.py` pour tester la création et l'insertion en écrivant directement des requêtes SQL.

Prise en main de l'ORM : Déploiement du premier modèle de test `(model.py)` via `create_tables_orm.py` pour comprendre la logique d'objets de SQLAlchemy et tester les requêtes d'insertion/sélection `(insert_tables_orm.py, select_tables_orm.py)`.

2. Initialisation du schéma final
`create_tables.py` : Ce script génère automatiquement l'ensemble de la structure relationnelle finale (les 9 tables de dimensions) dans MySQL à partir des métadonnées du fichier `models_dimensions.py`.

3. Phase d'alimentation (ETL) via l'API Ameli
Une fois les tables prêtes, la collecte de données se fait de manière ciblée :

`exploration_api.py` : Analyse préliminaire de la structure des réponses JSON fournies par l'API OpenDataSoft de l'Assurance Maladie.

`collecte_dim_geo_professions.py`, `collecte_dim_activite.py` et `collecte_dim_financier.py` : Scripts principaux qui appellent l'API, gèrent la pagination (offset/limit) via les fonctions de `utils_api.py`, extraient les nomenclatures distinctes et effectuent les commits par lots pour remplir proprement la base.

4. Contrôle et Validation
`verification.py` : Script final qui exécute des requêtes de comptage (COUNT) sur chaque table pour s'assurer que le volume de données insérées est conforme aux attendus (ex: ~101 départements, ~18 régions, etc.).

## Conclusion technique

Cette SAE nous a permis de comprendre comment faire la transition entre du SQL classique écrit à la main et l'utilisation d'un ORM (SQLAlchemy) en Python. L'ORM rend le code beaucoup plus propre et sécurisé puisqu'il permet de manipuler les tables comme de simples objets Python tout en gérant automatiquement les clés étrangères. La principale difficulté a été d'apprivoiser l'API de l'Assurance Maladie et de programmer une pagination correcte pour être sûr de récupérer l'intégralité des données sans coupure.