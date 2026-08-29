# Gouvernance

## Périmètre

Ce dépôt public distribue les skills génériques fournis aux clients AUGMENTÉS. Son audience est `augmentes-clients`, sa classification est `public` et sa portée d'installation par défaut est `project`.

Le dépôt contient des méthodes, schémas et exemples fictifs. Les secrets, données d'exécution, noms de clients, contenus de cerveaux, adresses réelles et configurations de machines restent hors du dépôt.

## Cycle de release

1. Modifier le contenu par pull request et mettre à jour `CHANGELOG.md`.
2. Faire passer la validation des manifestes, la politique de distribution et le scan de secrets.
3. Publier une version `X.Y.Z-rc.N` sur le canal `pilot`.
4. Tester les déclenchements dans une nouvelle session Claude Code et dans Codex sur un workspace client isolé.
5. Promouvoir le même contenu en `X.Y.Z` sur le canal `stable`, sans déplacer ni réécrire un tag existant.

Le retour arrière consiste à réinstaller le dernier tag stable connu. Si une version publiée est défectueuse, elle reste immuable et reçoit une version corrective.

## Contrôle

`catalog.yaml` porte l'audience, la portée, le canal et la classification. La CI vérifie les manifestes et les règles de distribution à chaque pull request, sur `main`, manuellement et le premier jour de chaque mois. Les changements de `main` passent par une pull request et le contrôle `validate`.

