---
name: plaud
description: Use when the user says "/plaud", "ingère mes réunions", "fais les CR de mes réunions", "traite mes derniers enregistrements", "traite mes enregistrements Plaud", or wants to turn Plaud meeting recordings into clean notes, a meeting report and the mail drafts that follow. Le pipeline enchaîne sync des enregistrements → contexte agenda → verbatim → PAGE DE CORRECTION (gate obligatoire) → note curée au coffre → compte-rendu en brouillon → brouillons de mails d'action. Jamais d'envoi, uniquement des brouillons.
---

# /plaud

Un enregistrement de réunion est une matière brute qui ment. La transcription déforme les noms et les chiffres, et le moteur qui découpe les voix attribue des phrases à des gens qui n'étaient pas là.

Cette recette part de cette matière et en tire une note propre dans le coffre, un compte-rendu et les mails qui en découlent. Entre les deux, il y a l'utilisateur.

## Les deux règles

> **Jamais d'envoi.** Cette recette ne produit que des brouillons, dans la messagerie de l'utilisateur. Il relit, il envoie.
>
> **Jamais de compte-rendu sans passage par la page de correction.** Sauf s'il dit explicitement « sans correction ».

Ces règles ne sont pas de la prudence de façade. Un compte-rendu envoyé sur la foi d'une transcription automatique, c'est un nom d'interlocuteur inventé, un montant divisé par mille, une décision attribuée à la mauvaise personne. Le coût de la relecture est de deux minutes, celui de l'erreur est un mail qui circule.

```
1. Sync            liste des enregistrements, dédup
2. Agenda          vrai titre et participants avec emails
3. Verbatim        transcript réel, un sous-agent par enregistrement
4. Correction      page HTML, un onglet par réunion   [ GATE ]
5. Coffre          note curée écrite AVEC les corrections
6. Brouillons      compte-rendu, puis mails d'action
```

## Avant de commencer

1. **Le connecteur Plaud doit être branché.** Le serveur MCP `plaud-toolkit` donne accès aux enregistrements du compte indiqué en `compte_plaud`. S'il ne répond pas, s'arrêter là et suivre `setup/SETUP.md`.
2. **`config.json` doit exister** à la racine de la recette. S'il manque, copier `config.example.json` et le remplir avec l'utilisateur, champ par champ. Ne jamais deviner les emails de son équipe : ce sont eux qui préremplissent les locuteurs et les destinataires d'un compte-rendu.
3. **Le coffre doit être identifié.** Si `coffre` est vide dans la config, demander où il se trouve.
4. **La messagerie annoncée doit répondre.** Si `messagerie` vaut `m365` ou `gmail`, le connecteur correspondant doit être branché : le vérifier avant de lancer, pas au stage 6. Si elle vaut `aucune`, annoncer d'emblée que le pipeline s'arrête au compte-rendu fichier, sans brouillon.

## Où vont les fichiers

Si le coffre est un kit cerveau (un dossier `Cerveaux/` ou `0 INBOX/` à sa racine), le brut va dans `5 ARCHIVE/raw/plaud/` et les notes dans `0 INBOX/`, d'où elles se rangent ensuite.

Sinon, tout vit sous `<coffre>/Plaud/` : le brut dans `brut/`, les notes curées à la racine.

Dans les deux cas, les pages de correction vont dans un sous-dossier `corrections/` placé à côté du brut.

Le brut ne se réécrit pas. C'est l'archive. La note curée est la version relue.

## Stage 1 : sync et dédup

`plaud_list_recordings` donne id, titre, date et durée. Si l'outil n'est pas chargé, le charger via ToolSearch.

> Les dates de l'API sont en UTC. Les convertir en heure de Paris avant tout usage : nom de fichier, frontmatter, fenêtre agenda, compte-rendu. Une réunion de 9h notée 7h fait rater son créneau d'agenda.

Puis écarter ce qui est déjà au coffre :

```bash
scripts/check_ingested.sh "<coffre>" <id1> <id2> ...
```

Il sort les ids déjà ingérés, un par ligne. Ne traiter que les autres.

Sans consigne de fenêtre, prendre les enregistrements des sept derniers jours et annoncer ce qui a été retenu.

## Stage 2 : contexte agenda

À sauter si `messagerie` vaut `aucune`.

Pour chaque enregistrement retenu, chercher l'événement qui recouvre `[heure de l'enregistrement − 30 min ; heure + durée]`, avec l'outil de recherche calendrier du connecteur nommé dans la config (`outlook_calendar_search` en M365, son équivalent côté Google).

> Le titre du créneau fait foi. Le titre Plaud est déduit du contenu par la machine et se trompe souvent de sujet.

Les participants de l'événement, avec leurs emails, préremplissent les locuteurs et la liste de diffusion du stage 4. C'est autant d'adresses qu'on n'aura pas à chercher plus tard.

Pas d'événement trouvé, ou connecteur en échec : se rabattre sur le titre Plaud et le signaler dans la page de correction, pour que l'utilisateur sache que ce titre n'a pas été vérifié.

## Stage 3 : verbatim, un sous-agent par enregistrement

Le verbatim ne transite jamais par la conversation principale. Une heure de réunion pèse des dizaines de milliers de mots. Un sous-agent par enregistrement, chacun écrivant dans un dossier isolé nommé par le `plaud_id`.

Ce que fait le sous-agent :

1. `plaud_get_recording_detail`, puis dans `content_list` l'entrée `transaction_polish`, dont le champ `data_link` porte l'URL du transcript.
   > Cette URL expire en cinq minutes. Écrire le `data_link` VERBATIM dans un fichier (outil Write, zéro caractère modifié), puis `curl -s -o out.json "$(cat url.txt)"` immédiatement. Une réponse qui commence par `<?xml` est un refus de signature : refaire `plaud_get_recording_detail` pour obtenir une nouvelle URL, réécrire le fichier, relancer le curl. Trois essais au maximum. Ne jamais recopier une URL à la main.
   > Les champs `transcript` et `auto_sum` sont le résumé automatique de Plaud. Il invente. Le transcript téléchargé est la source, pas eux.
2. Écrire le brut : frontmatter avec `plaud_id`, date, heure et durée, puis le transcript diarisé intégral au format `**[MM:SS] locuteur :** texte`. Assembler le fichier en Python directement, sans faire passer le texte par le contexte.
3. Renvoyer une synthèse JSON, sans le verbatim : titre proposé, locuteurs détectés, blocs de compte-rendu (avances, sections, prochaine étape), actions au format `Action | Owner`, doutes (noms mal entendus, chiffres incertains), et cinq à dix verbatims candidats `{t:"MM:SS", speaker, texte}`. Les verbatims sont courts, une à trois phrases, fidèles au transcript, jamais reformulés.

## Stage 4 : la page de correction (le gate)

Une page par lot, un onglet par réunion, générée depuis `correction-template.html` : remplacer `/*__KIT_CONFIG__*/` par le contenu de `config.json` et `/*__PLAUD_DATA__*/` par `{"reunions": [R1, R2, ...]}`. Le schéma d'un `R` est documenté en tête du template. Si `entreprise.logo` est renseigné dans la config, lire le fichier et l'inliner en data URI dans la page avant de l'écrire : une image en chemin relatif serait cassée en `file://`. Écrire la page dans le dossier des corrections, puis l'ouvrir (`open` sur macOS, sinon le navigateur).

Le champ `type` d'une réunion vaut `interne` si tous les participants partagent le domaine de l'équipe, `externe` sinon. Ce domaine se déduit des emails de `equipe` dans la config, la partie après le `@`, la plus fréquente. Le champ ne sert qu'à afficher un badge, dans le doute mettre `externe`.

L'utilisateur y corrige les locuteurs, le texte des blocs, les actions et leur statut, la liste de diffusion À et Cc, coche les verbatims à garder, et tranche compte-rendu oui ou non.

Le retour passe par deux canaux : 💾 **Exporter** dépose un JSON dans `~/Downloads` (prendre le plus récent), 📋 **Copier** met le même JSON dans le presse-papier, à recoller dans la conversation.

**Ne rien générer tant que les corrections ne sont pas revenues.** Ni note curée, ni compte-rendu, ni brouillon.

Une réunion déjà corrigée ne se recorrige pas. Si sa note au coffre porte `corrections:` dans son frontmatter, construire l'onglet depuis cette note avec `corrected: true` : il s'affiche en relecture, et on ne redemande pas deux fois le même travail.

## Stage 5 : application des corrections, écriture au coffre

Appliquer le mapping des locuteurs, les textes corrigés et les suppressions, puis écrire la note curée avec son frontmatter :

```yaml
type: source
subtype: plaud
plaud_id: "<id>"
date: 2026-07-24
heure: "14h30"
duree: "52 min"
titre_reunion: "Point produit"
participants: ["Prénom NOM", "Autre PERSONNE"]
corrections: appliquées le 24/07/2026
```

Les participants sont ceux de la page, pas ceux détectés au stage 3. Si des locuteurs ont été renommés, ajouter `speakers_corriges` au frontmatter du brut : le transcript, lui, ne bouge pas.

Les verbatims cochés 📥 partent dans `Verbatims.md`, à côté des notes, les plus récents en haut :

```markdown
> « le texte de la citation »
> **Prénom NOM** · 24/07/2026 14h30 (+12:04) · réunion : [[<note>|Point produit]]
```

## Stage 6 : compte-rendu et mails d'action, en brouillon

Ce stage n'a lieu que si l'utilisateur a coché compte-rendu oui et que `messagerie` n'est pas `aucune`.

Le compte-rendu est un HTML sobre aux couleurs de la config : `entreprise.couleur` en accent, `entreprise.nom` et `entreprise.logo` en tête, « powered by Marmites.ai » en pied. Fond blanc, styles en ligne, les messageries ignorent les feuilles de style. Un logo désigné par un chemin local ne s'affiche pas dans un mail : l'attacher en image inline, ou s'en tenir au nom en texte.

Objet : `📝 CR : <sujet court> · JJ/MM/AAAA`

Sections, dans l'ordre : une ligne méta (participants, date, heure, durée), **Avances**, **À faire** (un tableau `Action | Owner`, les actions clôturées barrées avec ✅), **Compte-rendu** (les blocs corrigés), **Prochaine étape**.

Le brouillon se crée avec l'outil du connecteur nommé dans la config (`outlook_create_draft` en M365, son équivalent côté Gmail). Les destinataires sont EXACTEMENT ceux marqués À et Cc dans la page, personne d'autre. Une ligne marquée ⚠ sans email ne reçoit pas de brouillon : la lister à la fin et demander l'adresse. Jamais l'inventer.

Restent les actions ni clôturées ni supprimées. Celles qui appellent un mail (une relance, une réponse promise, un envoi à faire) donnent chacune un brouillon court, avec la même règle sur les destinataires.

Si `messagerie` vaut `aucune`, écrire le compte-rendu en HTML dans le coffre, à côté de la note, et donner son chemin.

## Ce qu'on annonce à la fin

Court. Ce qui a été ingéré, ce qui était déjà fait, et le chemin de la page de correction.

Puis, après corrections : les notes écrites, les compte-rendus et brouillons créés avec leurs destinataires, et ce qui attend une adresse.

Terminer en rappelant que **tout est en brouillon**. Rien n'est parti.

## Pièges

- **Un nom de locuteur Plaud n'est jamais une source.** Le moteur colle un profil de voix connu sur un inconnu, et la phrase change de bouche. Ne retenir un nom que s'il tient à une auto-présentation, à un prénom prononcé dans la réunion, à l'agenda, ou à une correction de l'utilisateur. Ne jamais bâtir une conclusion sur une étiquette de diarisation : c'est ainsi qu'on inverse l'acheteur et le vendeur dans une synthèse.
- **Le résumé automatique invente.** Des noms, des dates, des montants, des unités (l'euro pour le millier d'euros). Curer depuis le transcript, jamais depuis le résumé.
- **Un chiffre dit à l'oral n'est pas fiable.** Un montant, un pourcentage, une échéance entendus une seule fois se mettent en doute dans la page de correction, pas dans le compte-rendu.
- **Les URLs de transcript tiennent cinq minutes.** Écriture verbatim, curl dans la foulée, `<?xml` égale nouvelle URL.
- **Le titre Plaud n'est pas le titre de la réunion.** Il est déduit du contenu. L'agenda tranche.
- **Un brouillon supprimé est un rejet.** Ne jamais le recréer sans demander ce qui n'allait pas.
- **Les gros transcripts passent par des sous-agents**, avec des fichiers isolés par `plaud_id`. Deux sous-agents qui écrivent au même endroit, et le verbatim d'une réunion se retrouve dans la note d'une autre.
- **Une seule fenêtre de correction ouverte à la fois.** La même page ouverte deux fois, et les corrections finissent dans l'onglet qu'on ne relit pas.
