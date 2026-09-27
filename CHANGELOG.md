# Journal des versions

## 1.0.0-rc.6 - 2026-09-27

- `augmentes-pilotage` monte en 1.0.0-rc.3 : la fixture de test de `le-point` s'appelait `tests/config.json`, le nom exact que les Recettes du Garde Manger refusent dans un paquet distribuable (configuration privée). Le paquet était bloqué à l'import depuis le 08/09 et la collection n'a jamais été publiée. Elle devient `tests/fixtures/config-exemple.json`, comme dans `augmentes-meetings`.
- `augmentes-automation` monte en 1.0.0-rc.3 : `connect-mcp` conseillait `type: "sse"` pour un serveur MCP distant dans Claude Desktop, forme qui ne marche pas. Le conseil donne maintenant la forme de chaque client : `claude mcp add --transport http` pour Claude Code, `mcp-remote --transport http-only` pour Claude Desktop, `type: "remote"` pour OpenCode. Reprise du correctif de la version Dexter du 26/09.

## 1.0.0-rc.5 - 2026-09-13

- `/done` ne coche plus des cases n'importe où. L'étape 5 disait de chercher les todos réalisés « dans les notes de tous les cerveaux présents » : une recherche sans borne, capable de cocher dans un cerveau partagé, sans montrer ce qu'elle avait modifié. Elle se limite désormais à la weekly note active et aux notes de contexte des projets touchés, ne coche que ce qui est réellement fini, suit la règle des écritures partagées quand la note l'est, et liste dans le log ce qu'elle a coché.

## 1.0.0-rc.4 - 2026-09-13

- `/done` ne tranche plus une contradiction tout seul. Il résolvait l'écart entre une note documentée et ce qui venait d'être dit « en faveur de l'info la plus récente », appliqué directement en Cerveau Privé sans validation et sans garder l'ancienne valeur : une phrase de conversation effaçait un fait écrit, sans trace. Il montre maintenant l'écart et demande, avec trois issues. C'est la seule exception à l'écriture directe en Privé ; les ajouts et la progression ne demandent toujours rien.

## 1.0.0-rc.3 - 2026-08-31

- Validation des références de skills et d'outils MCP à chaque pull request. Aucun contenu de plugin ne change : les six plugins restent en 1.0.0-rc.2, rien n'est rechargé chez les clients. Cette version existe pour que le dépôt porte un tag à jour, le travail d'outillage étant sinon invisible au suivi.

## 1.0.0-rc.2 - 2026-08-29

- Ajout d'une installation Codex à portée projet avec lock de version et contrôle de dérive.
- Mise à jour atomique des skills gérés sans toucher aux skills tiers du projet.

## 1.0.0-rc.1 - 2026-08-29

- Première version pilote des six plugins AUGMENTÉS.
- Ajout des manifestes Claude Code et Codex générés depuis `catalog.yaml`.
- Publication avec licence propriétaire, politique de confidentialité et scan de secrets.
