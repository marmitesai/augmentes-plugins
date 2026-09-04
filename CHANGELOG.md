# Journal des versions

## 1.0.0-rc.4 - 2026-09-04

- `creer-son-ontologie` rejoint AUGMENTÉS Knowledge, qui passe en 1.0.0-rc.3. Le skill dérive la carte des noms et des verbes d'un métier depuis un second cerveau : il compte le vault, fait valider les questions auxquelles la carte devra répondre, induit les types et les verbes sous un socle fixe et un plafond de vingt, prouve chaque question sur de vraies notes, puis rend un brouillon avec ses trous et ses contradictions. L'utilisateur tranche, le skill ne décide jamais.
- Deux scripts en bibliothèque standard accompagnent le skill, sans rien à installer. Le premier compte le second cerveau avant qu'on le lise, ce qui évite de tout ingérer et de laisser une erreur de lien se propager. Le second valide le brouillon avant d'écrire : il refuse un plafond dépassé, une relation vers un type non déclaré ou un type retenu sans ses trois exemples, et nomme la règle violée plutôt que d'écrire une carte fausse.
- Sur un second cerveau fraîchement installé, le skill rend une carte entièrement marquée « absent » au lieu d'inventer des objets métier. C'est le diagnostic attendu, et il devient la feuille de route du remplissage.

## 1.0.0-rc.3 - 2026-08-31

- Validation des références de skills et d'outils MCP à chaque pull request. Aucun contenu de plugin ne change : les six plugins restent en 1.0.0-rc.2, rien n'est rechargé chez les clients. Cette version existe pour que le dépôt porte un tag à jour, le travail d'outillage étant sinon invisible au suivi.

## 1.0.0-rc.2 - 2026-08-29

- Ajout d'une installation Codex à portée projet avec lock de version et contrôle de dérive.
- Mise à jour atomique des skills gérés sans toucher aux skills tiers du projet.

## 1.0.0-rc.1 - 2026-08-29

- Première version pilote des six plugins AUGMENTÉS.
- Ajout des manifestes Claude Code et Codex générés depuis `catalog.yaml`.
- Publication avec licence propriétaire, politique de confidentialité et scan de secrets.
