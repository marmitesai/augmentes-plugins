# Garde-Manger d’abord, répertoire local en secours

Ce contrat gouverne les lectures et écritures de connaissance de la skill. Les chemins `Cerveaux/…`, « vault », « coffre » et les exemples de commandes de fichiers dans sa méthode décrivent une organisation logique. Ils ne rendent pas le disque prioritaire. Les sources importées, scripts, configurations techniques, pièces jointes et pages HTML de travail peuvent rester locaux ; ils ne sont pas une deuxième base de connaissance.

## Choisir la source avant de lire

1. Découvrir les outils réellement disponibles du connecteur Garde-Manger de l’utilisateur. Ne pas imposer un nom de serveur MCP ni une instance de l’éditeur. Si plusieurs instances peuvent correspondre, faire préciser la cible avant toute lecture métier ou écriture.
2. Lire le statut et les espaces autorisés, puis rechercher la note dans cette instance. Utiliser les schémas exposés par les outils ; ne pas inventer une opération. Un dossier local ou un cache existant ne remplace pas ce contrôle.
3. Associer les noms de cerveaux de la méthode aux espaces effectivement renvoyés. Ne pas déduire des droits du nom « Privé », « Direction » ou « Entreprise ». Si le Privé n’est pas accessible, ne pas déposer un journal personnel dans un espace partagé.

| Résultat | Suite |
|---|---|
| Garde-Manger disponible | Lire et écrire par le connecteur, même si une copie locale existe. |
| Recherche vide ou note absente | Vérifier la cible ; créer une note seulement si la tâche et les droits le permettent. Ce n’est pas une panne. |
| Connecteur absent, panne réseau, délai dépassé ou indisponibilité du service | Une seule nouvelle tentative de lecture au maximum, puis secours local annoncé. Pas de boucle de tentatives. |
| Connexion expirée, refus d’accès, espace interdit | Demander la reconnexion ou signaler le droit manquant. Ne pas lire une copie locale de la ressource refusée pour contourner ce refus. Le nouveau contenu fourni par l’utilisateur peut être conservé en brouillon privé si son stockage local est autorisé. |
| Conflit de révision ou contenu refusé | Relire et résoudre dans le Garde-Manger ; ne pas tenter de faire accepter le même changement via le secours. |

## Écrire dans le Garde-Manger

Rechercher avant de créer. Pour une note existante, conserver son identifiant et utiliser sa révision ou son empreinte fraîche. Quand ils sont exposés, `write_note` sert à créer ou compléter, `replace_note` à modifier avec contrôle de révision, `restore_note` à restaurer, `note_versions` à lire l’historique. Ce sont des exemples de capacités, pas des noms MCP à supposer présents.

Une correction ciblée peut nécessiter de relire le texte complet, d’y appliquer le seul changement autorisé, puis de soumettre le texte résultant par un remplacement conditionnel. Ne pas recréer une note sous un autre identifiant pour éviter un conflit. Si aucune opération compatible n’est exposée, conserver une proposition non appliquée et dire laquelle manque.

Vérifier le reçu, puis relire la note ou sa révision avant d’annoncer « enregistré ». Une réponse asynchrone `pending` n’est pas une publication confirmée. Si la réponse se perd après une écriture, son résultat est **incertain** : rechercher le reçu avec la même clé d’idempotence et relire avant de retenter. Ne jamais rejouer avec une nouvelle clé pour forcer le passage. Si le connecteur ne permet ni de consulter un reçu ni de vérifier l’effet de façon fiable, garder l’état incertain et demander une vérification ; ne pas déclarer la synchronisation faite.

Lister, lire, ranger, renommer, archiver ou partager une note distante passe par les capacités autorisées du connecteur. Ne pas exécuter `ls`, `find`, `mv`, `sed` ou un script de scan local sur un prétendu miroir pour réaliser ces opérations. Les réglages Obsidian, les fichiers de code et les configurations de connecteurs restent des opérations locales lorsqu’ils sont demandés.

## Répertoire de secours

Réutiliser le répertoire de secours configuré pour **cette instance et cet utilisateur**. À défaut, proposer un répertoire privé dans l’espace de travail courant et faire confirmer son emplacement ; ne pas deviner un dossier personnel global ou celui d’un autre client. Si l’utilisateur travaille déjà avec un coffre local et qu’aucun Garde-Manger n’est configuré, ce coffre reste utilisable en mode local annoncé.

Lire uniquement les notes ou exports locaux que l’utilisateur est autorisé à consulter. Signaler leur date connue et le fait que leur fraîcheur distante n’est pas vérifiée. Ne pas aspirer tout le serveur pour constituer un cache. Ne pas déposer de contenu privé dans un dossier partagé ou synchronisé vers une audience plus large.

En cas de panne d’une instance configurée, placer les nouvelles contributions dans un dossier privé `secours-garde-manger/<instance>/<utilisateur>/<operation-id>/`, sous la racine choisie. L’instance et l’utilisateur sont des identifiants locaux sans séparateurs de chemin ; ne pas utiliser des valeurs non vérifiées comme chemins. Conserver :

- `contenu.md` : contribution ou proposition de modification, sans secret technique ;
- `operation.json` : date, instance, utilisateur, espace cible, chemin logique, identifiant de note connu, type d’opération, révision/empreinte de départ connue, clé d’idempotence stable et état `a_synchroniser` ou `resultat_incertain`. Une valeur inconnue reste inconnue, jamais inventée.

Ce dossier est une file de secours, pas une publication dans le cerveau cible. Les contenus déjà confirmés sur le serveur ne sont pas remis dans cette file. Ne pas modifier un export marqué en lecture seule. Dans un coffre purement local sans instance configurée, appliquer les changements autorisés directement aux notes locales, en les déclarant locaux ; ne pas inventer une destination de synchronisation.

Si aucun stockage local approprié n’est disponible, fournir le texte ou un fichier téléchargeable à l’utilisateur et dire explicitement qu’il n’est sauvegardé ni sur le serveur ni dans un répertoire durable. Un fichier temporaire de session n’est pas un secours persistant confirmé.

## Reprendre après la panne

À la prochaine utilisation du connecteur, ou sur demande de synchronisation :

1. Vérifier l’instance, l’identité et les droits actuels. Relire la cible et ses révisions.
2. Pour un résultat incertain, rechercher d’abord le reçu ou la contribution déjà appliquée. Ne pas dupliquer une création ou un append.
3. Comparer les changements locaux aux changements distants. Présenter les contradictions et conflits ; ne pas écraser automatiquement le serveur avec une copie locale. Une cible inconnue doit être résolue avant écriture.
4. Appliquer seulement les contributions toujours autorisées, avec leurs clés et contrôles de concurrence. Une publication partagée garde les validations d’audience prévues par la skill, même si la préparation était locale.
5. Après reçu et relecture, marquer l’opération `synchronisee` avec l’identifiant et la révision obtenus. Conserver la trace locale ; ne pas la supprimer automatiquement.

Pas de tâche de fond implicite ni de promesse de reprise automatique après fermeture de la conversation. La reprise nécessite une session active ou une automatisation explicitement configurée.

## Bilan à donner

Séparer les écritures **confirmées dans le Garde-Manger**, **enregistrées localement seulement**, **à synchroniser**, **au résultat incertain** et **bloquées par les droits**. Donner les références distantes ou les chemins locaux correspondants. Pour `/done`, un journal local signifie « clôture conservée localement, synchronisation en attente », jamais « journal écrit dans le Garde-Manger ».
