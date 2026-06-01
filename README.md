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

* **Application Finale (Collecte et Dimensions Réelles) :**
  * `models_dimensions.py` : Fichier principal contenant la modélisation complète de nos tables finales (Régions, Départements, Professions, Tranches d'âge, Sexe, Types d'exercice, Secteurs, Niveaux d'honoraires et Prescriptions).
  * `create_tables.py` : Permet de générer automatiquement tout le schéma relationnel final dans MySQL.
  * `exploration_api.py` : Script utilisé pour analyser la structure JSON renvoyée par l'API Ameli.
  * `utils_api.py` : Contient la fonction globale pour automatiser les appels et gérer la pagination (`offset`/`limit`) d'OpenDataSoft.
  * `collecte_dim_geo_professions.py`, `collecte_dim_activite.py` et `collecte_dim_financier.py` : Scripts ETL de production chargés de récupérer toutes les nomenclatures distinctes sur l'API et de remplir nos tables ORM de manière propre.
  * `verification.py` : Script de contrôle final qui affiche le nombre de lignes présentes dans chaque table pour vérifier que tout est bien alimenté.
  * `nettoyage_db.py` : Script outil pour vider ou supprimer proprement les tables si nécessaire.


## Fonctionnement et chaîne d'exécution

Pour déployer et alimenter la base de données, les scripts doivent être exécutés dans cet ordre précis :

### 1. Initialisation du schéma
* `nettoyage_db.py`** *(Optionnel)* : Pour partir d'une base vierge.
* `create_tables.py`** : Instancie l'ensemble de la structure relationnelle finale dans MySQL à partir des métadonnées SQLAlchemy.

### 2. Phase d'alimentation (ETL) via l'API Ameli
Une fois les tables prêtes, la collecte s'effectue par thématique, en gérant la pagination pour extraire les valeurs uniques (`group_by`) :
* `collecte_dim_geo_professions.py`**
* `collecte_dim_activite.py`**
* `collecte_dim_financier.py`**

### 3. Contrôle et Validation
* `verification.py`** : Exécute des requêtes de comptage (`COUNT`) sur chaque table pour s'assurer que le volume de données insérées est conforme aux attendus régionaux et nationaux.

---
## Conclusion technique

Cette SAE nous a permis de comprendre comment faire la transition entre du SQL classique écrit à la main et l'utilisation d'un ORM (SQLAlchemy) en Python. L'ORM rend le code beaucoup plus propre et sécurisé puisqu'il permet de manipuler les tables comme de simples objets Python tout en gérant automatiquement les clés étrangères. La principale difficulté a été d'apprivoiser l'API de l'Assurance Maladie et de programmer une pagination correcte pour être sûr de récupérer l'intégralité des données sans coupure.
