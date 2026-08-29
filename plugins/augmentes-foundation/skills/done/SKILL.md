---
name: done
description: "Fin de session : extraction, log dans la daily note du Cerveau Privé, mise à jour des contextes dans les cerveaux concernés, signalement des écritures partagées et des notes à promouvoir."
---

# Fin de Session

Clôture la session en extrayant les informations importantes et en mettant à jour les cerveaux selon le flux de ruissellement.

## Le cadre multi-cerveaux

Une session a pu écrire dans plusieurs cerveaux (les dossiers présents sous `Cerveaux/`). La clôture doit tous les couvrir. Trois règles qui ne bougent pas :

**Le log de session va toujours dans le Cerveau Privé.** La daily note vit dans la phase de vie active, dans `Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/`. Quel que soit le cerveau où on a travaillé. Le journal est privé, point.

**Les notes de contexte se mettent à jour là où elles vivent.** Un projet qui vit dans un cerveau partagé a sa note de contexte dans ce cerveau. Balaye tous les cerveaux présents, ne cherche pas seulement dans le Privé.

**Toute écriture dans un cerveau partagé est irréversible.** Si la session a écrit dans un cerveau partagé, dis-le explicitement à l'utilisateur en fin de clôture. Il doit savoir ce qui est devenu lisible par d'autres.

## Process

### Étape 1 : Analyse de la conversation

Relis la conversation de cette session et extrais les **5 types d'information** :

1. **Décisions** : choix actés qui affectent les process ou l'organisation
   - Ex : "On part sur NocoDB pour le CRM", "J'arrête ce projet"
2. **Préférences** : feedback utilisateur sur le comportement de l'agent
   - Ex : "Sois plus direct", "Ne me demande pas de valider chaque fois"
3. **Faits** : informations factuelles nouvelles
   - Ex : "Nouveau client signé", "Le prix a changé", "Il a 30 personnes dans son équipe"
4. **Contradictions** : incohérences entre ce qui est documenté dans les cerveaux et ce qui a été dit
   - Ex : La note de projet dit "deadline mars" mais on a parlé de "deadline juin"
5. **Ressources** : liens, références, outils, concepts mentionnés à documenter

Identifie aussi :
- **Fichiers créés ou modifiés** pendant la session, **avec le cerveau de chacun** (le dossier sous `Cerveaux/`) ou `Atelier/`
- **Todos complétés** (tâches qu'on a terminées et qui sont cochables quelque part)
- **Prochaines étapes** identifiées mais pas encore réalisées

### Étape 2 : Détecter la phase active

La phase de vie est une notion du Cerveau Privé, elle n'existe nulle part ailleurs.

```bash
ls -d "Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/"*/ | sort -V | tail -1
```

### Étape 3 : Log dans la daily note (NIVEAU 2, OBLIGATOIRE)

**Toujours dans le Cerveau Privé**, phase active. Même si toute la session s'est passée dans un cerveau partagé.

- Chemin : `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/[Phase active]/[YYYY-MM-DD].md`
- Si elle n'existe pas, crée-la avec le template `Cerveaux/Cerveau Privé/4 TOOLS/Templates/Daily Note.md`

Ajoute à la fin de la note :

```markdown
---

## Logs IA / Session [HH:MM]

**Accompli :**
- [Action 1]
- [Action 2]

**Extractions :**
- Décisions : [liste des décisions actées]
- Faits : [liste des faits nouveaux appris]
- Préférences : [feedback sur le comportement IA]
- Contradictions : [incohérences détectées et résolues]
- Ressources : [liens, outils, concepts à retenir]

**Fichiers modifiés :**
- Cerveau Privé : `[chemin/fichier1.md]`
- [Cerveau partagé] : `[chemin/fichier2.md]`   ← partagé
- Atelier : `[chemin/fichier3]`

**Prochaines étapes :**
- [ ] [TODO 1]
- [ ] [TODO 2]
```

Marque toujours les fichiers d'un cerveau partagé. Dans six mois, la trace de ce qui a été rendu visible compte autant que le contenu.

### Étape 4 : Mise à jour des notes de contexte (NIVEAU 3, OBLIGATOIRE, avec validation)

Pour chaque extraction de type Décision, Fait, ou Contradiction qui concerne un projet ou une casquette :

1. **Trouve la note de contexte, dans tous les cerveaux présents.** Un projet peut vivre ailleurs qu'en Privé.

```bash
find Cerveaux -maxdepth 3 -type d \( -path "*/1 PROJETS/*" -o -path "*/2 CASQUETTES/*" \)
```

   Cherche le projet ou la casquette par son nom dans tous les cerveaux présents. Le premier trouvé est le bon : une note vit dans un seul cerveau. Si le même nom apparaît dans deux cerveaux, c'est une anomalie (une copie a été faite au lieu d'un déménagement), signale-la.

2. **Lis la note de contexte** trouvée
3. **Vérifie si l'info est déjà présente** ou si elle contredit quelque chose
4. **Mets à jour** la note :
   - `Cerveaux/[Cerveau]/1 PROJETS/[Projet]/[Projet].md` → Progression, roadmap, statut
   - `Cerveaux/[Cerveau]/2 CASQUETTES/[Casquette]/[Casquette].md` → Nouvelles infos, responsabilités

**Si la note de contexte est dans un cerveau partagé**, tu écris pour un public. Avant d'écrire, applique la règle du `AGENTS.md` du cerveau concerné, et retire de ta mise à jour ce qui n'a rien à y faire : secret technique, donnée personnelle de tiers, jugement sur quelqu'un, chiffre financier interdit à cette audience. Un fait appris en session n'est pas automatiquement publiable dans le cerveau où vit le projet.

Si tu dois écrire dans un cerveau partagé, montre d'abord ce que tu comptes ajouter :

```
Le projet [X] vit dans le [cerveau partagé].
Je vais y écrire (lisible par [audience]) :

- [contenu]

OK ?
```

Dans le Cerveau Privé, tu appliques directement, sans validation.

Si une **contradiction** est détectée : résous-la en faveur de ce qui a été dit pendant la session (l'info la plus récente gagne).

### Étape 5 : Cocher les todos complétés

Cherche dans les notes de tous les cerveaux présents (weekly notes, notes de projet) les todos réalisés pendant cette session. Coche-les (`- [x]`). Les weekly notes sont toujours dans le Cerveau Privé, les todos de projet sont là où vit le projet.

### Étape 6 : Mise à jour contexte personnel (NIVEAU 4, avec validation)

Si des extractions de type Préférence ou des infos personnelles importantes ont émergé :

Vérifie si des mises à jour sont nécessaires dans (toujours en Cerveau Privé) :
- `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Moi.md` → Style IA, valeurs, nouvelles infos personnelles
- `Life Phases/[Active]/[N] Intention.md` → Progression sur les objectifs

Si des changements sont pertinents, montre le diff et demande validation :

```
Je propose de mettre à jour [fichier] :

- Ajouter : [contenu]
- Modifier : [ancien] → [nouveau]

OK ?
```

Si aucun changement n'est nécessaire, ne rien proposer.

### Étape 7 : Ce qui a été écrit en partagé (OBLIGATOIRE si applicable)

Reprends la liste des fichiers touchés dans les cerveaux partagés pendant la session. C'est irréversible, l'utilisateur doit le voir noir sur blanc.

```
⚠️ **Écrit dans un cerveau partagé pendant cette session :**

[Une section par cerveau partagé touché (les dossiers partagés sous
`Cerveaux/`), avec son audience :]

[Cerveau partagé] (lisible par [audience]) :
  - `1 PROJETS/Cession/Note de cadrage.md`   (créée)
  - `1 PROJETS/Cession/Cession.md`           (contexte mis à jour)

C'est en place et considéré comme lu. Si quelque chose n'aurait pas dû sortir, dis-le maintenant.
```

Si rien n'a été écrit en partagé, une ligne suffit : `Aucune écriture en cerveau partagé.`

### Étape 8 : Ce qui mériterait d'être partagé (proposition, jamais d'action)

S'il n'existe aucun cerveau partagé (seul le `Cerveau Privé` est présent sous `Cerveaux/`), saute cette étape.

Passe en revue les notes **créées ou nettement enrichies en Cerveau Privé** pendant la session. Repère celles qui gagneraient à changer d'audience.

Candidat au partage :
- une note utile à d'autres pour faire leur travail (méthode, doctrine, cadrage, compte-rendu, décision qui les concerne)
- une note aboutie, que l'utilisateur assume
- un concept du Garden qui fait vocabulaire commun

Reste en Privé, ne le propose même pas :
- brouillon, intuition, note en cours
- personnel (santé, famille, argent, ressenti)
- jugement sur une personne nommée, information reçue en confidence
- tout ce sur quoi tu hésites

```
**Notes créées en Privé qui mériteraient peut-être une audience :**

- `1 PROJETS/Refonte Site/Brief.md`
  → [cerveau partagé] : l'équipe qui exécute a besoin du brief

- `6 GARDEN/Notes/Coût réel d'une réunion.md`
  → [cerveau partagé] : c'est un argument d'arbitrage, pas un sujet pour tout le monde

Lance `/partager` si tu veux les faire monter. Je ne déplace rien tout seul.
```

Tu **proposes**. Tu ne déplaces jamais une note ici. Le déménagement passe par `/partager`, qui fait le contrôle de confidentialité et le contrôle des wikilinks.

### Étape 9 : Confirmation

```
Session loggée !

NIVEAU 2 : Daily note (Cerveau Privé) : [date] mise à jour
NIVEAU 3 : Contextes mis à jour : [liste des fichiers, avec leur cerveau]
NIVEAU 4 : Contexte personnel : [mis à jour / pas de changement]

Écritures en cerveau partagé : [X] fichiers ([liste courte] / aucune)
Notes proposées au partage : [X] (via /partager)

Extractions :
- X décisions
- X faits
- X préférences
- X contradictions résolues
- X ressources

À la prochaine !
```

## Notes

- Le log de session est **toujours** dans le Cerveau Privé, jamais ailleurs
- NIVEAU 3 en Cerveau Privé : appliqué directement, pas de validation
- NIVEAU 3 en cerveau partagé : montrer avant d'écrire, l'audience change tout
- NIVEAU 4 (Moi.md, intention) nécessite validation
- Étape 7 (écritures partagées) est obligatoire dès qu'un fichier partagé a bougé
- Étape 8 propose, elle n'exécute pas. Le partage passe par `/partager`
- Être concis dans les logs (pas de blabla)
- Utiliser des liens `[[wikilinks]]` quand pertinent
- Si la session a été très courte (juste une question), faire un log minimal
