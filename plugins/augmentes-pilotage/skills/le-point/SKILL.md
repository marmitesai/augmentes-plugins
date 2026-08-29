---
name: le-point
description: Use when the user says "/le-point", "fais le point", "fais le point sur ma boîte", "qu'est-ce que j'ai raté cette semaine", "qui attend une réponse de moi", "ingère mes mails", or wants to turn a window of email (7 to 30 days) into durable notes in their vault plus a decision report. Récolte les mails reçus ET envoyés sur la fenêtre, sépare le signal du bruit, croise les deux pour ne jamais accuser à tort d'un silence, range les faits durables dans le coffre, puis sort un rapport HTML d'arbitrage avec zone de correction.
---

# /le-point

Une boîte mail, ce sont deux choses mélangées : des faits qui méritent d'être gardés, et des décisions qui attendent. `/le-point` sépare les deux.

Ce qui mérite mémoire part dans le coffre. Ce qui demande un arbitrage revient dans un rapport où l'on tranche d'un clic.

## Le principe fondateur

> **Une boîte de réception ment.** Un fil sans réponse visible dans les reçus n'est pas un fil sans réponse : il y a les envoyés, et il y a ce que le coffre sait déjà. Tant que les trois ne sont pas croisés, chaque « il attend depuis douze jours » est une accusation non vérifiée.

Cette règle n'est pas théorique. Sur la première fenêtre traitée avec cette recette, trois « sans réponse » se sont révélés faux : un contrat signé le soir même, un contact qui avait reçu un lien et ne l'avait pas utilisé, un dossier envoyé huit jours plus tôt. Les trois venaient de la même erreur, lire les reçus sans les envoyés.

## Avant de commencer

1. **Le connecteur mail doit être branché.** Microsoft 365 ou Gmail, dans les connecteurs. Sans lui, il n'y a rien à lire.
2. **`config.json` doit exister** à la racine de la recette. S'il manque, copier `config.example.json` et le remplir avec l'utilisateur, champ par champ. Ne jamais inventer ses domaines proches à sa place : lui demander qui compte, ce sont ses clients et ses conseils.
3. **Le coffre doit être identifié.** Si `coffre` est vide dans la config, demander où il se trouve.

## Procédure

### 1. Récolter

Demander la fenêtre si elle n'est pas précisée. Défaut raisonnable : **15 jours**.

Lire les mails **reçus** et **envoyés** sur la fenêtre, via le connecteur disponible, et écrire deux fichiers au format ci-dessous dans un dossier de travail (`<coffre>/archive/mails/<date>-<N>j/`).

**Récolter les envoyés n'est pas optionnel.** C'est la moitié du travail : sans eux, le croisement est impossible et le rapport accuse à tort.

Si le connecteur plafonne le nombre de résultats, paginer par tranches de dates plutôt que de tronquer. Un mois récolté à moitié vaut moins qu'une semaine récoltée en entier : dans ce cas, réduire la fenêtre et le dire.

### 2. Le format d'échange

Les deux scripts ne parlent qu'à ce format. Peu importe d'où viennent les mails.

`inbox.json` et `sent.json` : une liste d'objets.

```json
[{
  "id": "identifiant du message",
  "fil": "identifiant de la conversation (conversationId, threadId)",
  "sujet": "l'objet du mail",
  "expediteur": "qui.ecrit@example.com",
  "nom": "Qui Écrit",
  "a": ["destinataire@example.com"],
  "copie": ["copie@example.com"],
  "date": "2026-07-18T09:14:00Z",
  "extrait": "les premières lignes du corps"
}]
```

`fil` est le champ décisif : c'est lui qui permet de savoir qu'un mail reçu a reçu une réponse. Si la source ne fournit pas d'identifiant de conversation, utiliser le sujet normalisé (sans les `Re:` et `TR:`) et le dire dans le rapport, parce que le croisement sera moins fiable.

### 3. Trier

```bash
python3 scripts/triage.py --dir "<dossier de travail>" --config config.json
```

Sort `triage.json`, `digest-signal.txt`, `digest-envois.txt`. **Lire les deux digests, jamais les JSON bruts** : ils tiennent en deux lectures et suffisent à comprendre la période.

Sur quinze jours, une boîte de dirigeant donne typiquement quelques centaines de mails dont une petite moitié de signal. Un fil n'est marqué `en_attente` que si aucun envoi ne le touche, ni par fil ni par destinataire, et qu'il dépasse le seuil.

**Lire par grappes, pas en liste plate.** Ce qui compte : plusieurs fils du même expéditeur sur la fenêtre, plusieurs fils de la même société la même semaine, et les formules dures (« relance », « dernière relance », « comme convenu », « merci de me confirmer »).

### 4. Approfondir là où ça compte

L'extrait s'arrête vite, souvent juste avant l'information utile. Pour les huit à quinze fils qui portent une décision, un chiffre, une rupture ou une échéance, aller chercher le corps complet via le connecteur.

Ne pas le faire pour cent trente fils. Le temps de lecture se dépense sur ce qui change une décision.

### 5. Croiser avec le coffre, avant d'écrire

Pour chaque fait sur le point d'être rangé, vérifier ce que le coffre dit déjà. C'est là que se trouvent les meilleures trouvailles, parce que **la contradiction entre un mail et une note est plus informative que le mail seul**.

Un mail présente quelqu'un comme un candidat qui ne rappelle pas, alors qu'une note dit que son contrat est signé : ce n'est plus un candidat tiède, c'est un futur collaborateur qui décroche. Chercher aussi les doublons de personnes, deux adresses et deux sociétés pour un seul interlocuteur.

### 6. Demander les arbitrages

Poser les questions structurantes **avant** d'écrire, avec des options cliquables (`AskUserQuestion`).

Ce qui se demande : créer un projet, rattacher un fait sensible à un dossier plutôt qu'un autre, déclencher un travail lourd. Ce qui ne se demande pas : où ranger un fait évident. La structure du coffre suffit.

### 7. Ranger dans le coffre

Les faits durables vont dans la note du projet ou du domaine concerné. **Modification ciblée, jamais de réécriture** d'une note existante. Mettre à jour la date de mise à jour.

Ce qui n'a pas vocation à durer ne va pas dans le coffre. Une confirmation de commande, un accusé de réception, une facture de routine se comptent, ne se consignent pas.

### 8. Sortir le rapport

Construire un `constat.json` (schéma ci-dessous), puis :

```bash
python3 scripts/rapport.py --input constat.json --output "<chemin>/le-point-<date>.html"
```

Livrer le fichier à l'utilisateur.

## Le rapport

Cinq sections, du plus engageant au plus froid :

1. **Décisions en attente** : ce que l'IA ne peut pas trancher, avec des options.
2. **Ce qui a une date** : rien à arbitrer, juste à ne pas rater.
3. **Silences à trancher** : qui attend, et pourquoi le silence dure.
4. **Ce que j'ai rangé** : les notes touchées.
5. **Incohérences trouvées** : ce que le croisement a révélé, **et ce que l'IA avait mal lu**.

La cinquième section n'est pas optionnelle. Un rapport qui n'affiche jamais ses propres erreurs n'est pas relu, il est cru.

### Schéma du constat.json

```json
{
  "titre": "Le Point, 3 au 18 juillet",
  "h1": "Quinze jours de mails, ce qu'il en reste",
  "periode": "3 → 18 juillet 2026",
  "run": "2026-07-18",
  "chapo": "Reçus et envoyés. Le bruit est filtré.",
  "stats": [{"n": "805", "l": "reçus"}, {"n": "178", "l": "envoyés"}],
  "sections": [
    {"id": "decisions", "nav": "Décisions", "titre": "Décisions en attente", "lede": "…",
     "cartes": [{
        "id": "d1", "titre": "…", "tag": "avant le 30/07", "niveau": "now",
        "corps": ["Le HTML simple est autorisé : <strong>, <em>, <code>."],
        "why": "<b>Pourquoi c'est bloquant :</b> …",
        "options": ["Première option", "Deuxième option"],
        "src": "Source : mail du 16/07 à 12h25"}]},
    {"id": "range", "nav": "Ce que j'ai rangé", "titre": "Ce que j'ai rangé",
     "rows": [{"etat": "créé", "quoi": "Nom de la note", "detail": "…"}]}
  ],
  "foot": "Généré le …"
}
```

`niveau` vaut `now` (rouge), `soon` (ocre), `open` (gris) ou `ok` (vert). `run` sert de clé de sauvegarde locale : le garder stable d'une génération à l'autre, sinon les cases cochées sont perdues.

### La zone de correction

Le rapport embarque une zone de commentaire branchée sur **chaque carte** : un `+` au survol, un compteur sur les cartes annotées, sauvegarde dans le navigateur, export en markdown.

Le bouton **Exporter** copie d'un coup les arbitrages cliqués et les corrections écrites. L'utilisateur recolle dans la conversation, et la passe suivante corrige le coffre.

C'est le canal de retour. **Ne jamais lui demander de retaper une correction qu'il a déjà écrite dans la page.**

## Règles

- **Jamais d'envoi, jamais de brouillon** sans demande explicite. Cette recette lit les mails et écrit dans le coffre, rien d'autre.
- **Chaque fait daté cite sa source** dans le rapport. Un fait sans source est une hypothèse et se présente comme telle.
- **Ne jamais écrire « sans réponse »** sans avoir vérifié les envoyés et le coffre.
- **Rien ne sort de la machine.** Les scripts ne font aucun appel réseau. Les mails récoltés restent dans le coffre.
- Les mails bruts vont dans l'archive, jamais dans un dossier de projet.

## Pièges

- **Les automatismes maison partent de vraies boîtes d'équipe.** Un ticket ou une confirmation de commande arrive depuis `support@` ou `commercial@`, adresses par ailleurs légitimes. Seul le sujet les trahit : c'est le rôle de `sujets_automatiques` dans la config.
- **Un `noreply` reste un `noreply` même préfixé.** `securite-noreply@` et `sc-noreply@` sont filtrés comme les autres.
- **Un proche sur une boîte grand public** ne fait pas de `gmail.com` un domaine proche. La liste est nettoyée automatiquement.
- **Un fil gardé peut afficher un dernier sujet de bruit** si un message plus ancien portait le signal. Lire le fil, pas le sujet.
- **Le compteur de fils en attente n'est pas un tableau de bord.** Quelques dizaines sur quinze jours, c'est le régime normal. Ne remonter que ceux qui coûtent quelque chose.
- **Une fenêtre trop large dilue.** Au-delà de trente jours, le rapport devient un inventaire que personne ne lit. Mieux vaut deux passes de quinze jours.
