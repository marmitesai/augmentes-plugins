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

## Données et accès

Le dépôt ne contient aucun secret. Les accès aux services externes sont configurés localement par chaque utilisateur. Consultez [PRIVACY.md](PRIVACY.md) et la licence avant installation.

## Maintenance

`catalog.yaml` est la source des manifestes Claude Code et Codex. Toute contribution doit passer les validateurs du dépôt et le scan de secrets.
