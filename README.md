# Plugins AUGMENTÉS

Plugins Claude Code et Codex fournis aux clients AUGMENTÉS. Les skills travaillent sur les fichiers locaux de l'utilisateur et n'embarquent aucun identifiant d'accès.

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
