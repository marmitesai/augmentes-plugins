# Plugins AUGMENTÉS

Plugins Claude Code et Codex fournis aux clients AUGMENTÉS. Les skills utilisent d’abord le Garde-Manger connecté de l’utilisateur, puis un répertoire local en secours. Ils n’embarquent aucun identifiant d’accès.

## Stockage et reprise

Le [contrat commun de stockage](references/storage-contract.md) s’applique aux 18 skills. Le connecteur et le répertoire de secours appartiennent à l’utilisateur ; aucun domaine ni client n’est imposé. Une panne permet de conserver le travail localement, avec un état à synchroniser. Un refus d’accès ne se contourne pas par une copie locale. Une écriture distante n’est annoncée qu’après confirmation et relecture.

Le contrat est généré dans chaque skill pour rester disponible lors d’une installation individuelle ou d’un export ZIP. Modifier sa source, puis lancer `python3 scripts/generate_catalog.py` ; `--check` détecte les copies périmées. Les scripts de travail (Plaud, tri des mails, rapports) restent locaux sans devenir une source de vérité parallèle.

## Plugins

- `augmentes-foundation` : fondations et organisation du second cerveau ;
- `augmentes-routines` : revues et transitions ;
- `augmentes-knowledge` : ingestion, recherche et connaissance ;
- `augmentes-automation` : processus, connexions et automatisations ;
- `augmentes-meetings` : traitement des réunions Plaud ;
- `augmentes-pilotage` : pilotage depuis les échanges email.

## Installation avec Claude Code

```bash
claude plugin marketplace add marmitesai/augmentes-plugins --scope project
claude plugin install augmentes-foundation@augmentes --scope project
```

Installez ensuite les plugins prévus par votre accompagnement. La portée `project` garde la configuration attachée au second cerveau concerné.

## Installation avec Codex

Codex ne propose pas encore de portée projet dans `codex plugin add`. Clonez la release voulue, puis installez la sélection dans le projet :

```bash
git clone --branch v1.0.0-rc.2 --depth 1 https://github.com/marmitesai/augmentes-plugins.git augmentes-plugins-rc.2
python3 augmentes-plugins-rc.2/scripts/install_codex_project.py install \
  --source-root augmentes-plugins-rc.2 \
  --target /chemin/vers/le-projet \
  --ref v1.0.0-rc.2 \
  --plugins augmentes-foundation augmentes-routines augmentes-knowledge
```

Le lock créé dans `.agents/plugins/augmentes.lock.json` enregistre le tag, le commit et les hashes. Relancez avec `check` pour détecter une dérive.

## Données et accès

Le dépôt ne contient aucun secret. Les accès aux services externes sont configurés localement par chaque utilisateur. Consultez [PRIVACY.md](PRIVACY.md) et la licence avant installation.

## Maintenance

`catalog.yaml` est la source des manifestes Claude Code et Codex. Toute contribution doit passer les validateurs du dépôt et le scan de secrets.

Les recettes maison servies par learn (`kit-plaud`, `le-point`) se construisent ici, à un tag : `python3 scripts/build_learn_zip.py <slug> <tag> <version>` écrit `dist/<slug>-v<version>.zip` et affiche son empreinte SHA-256. `bash scripts/scrub-check.sh <dossier de la skill>` doit être vert avant.
