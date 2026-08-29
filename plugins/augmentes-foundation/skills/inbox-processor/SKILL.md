---
name: inbox-processor
description: Traiter les items de l'inbox et les router vers le bon cerveau
---

# Inbox Processor

Tu aides l'utilisateur à vider son inbox. Chaque item reçoit deux décisions : **quel dossier** (IPCRA) et **quel cerveau** (audience).

## Contexte

Les inbox (`Cerveaux/<cerveau>/0 INBOX/`) sont des points de capture temporaires. Rien n'y reste plus de quelques jours.

Par défaut on traite l'inbox du `Cerveau Privé`. Si l'utilisateur travaille dans un cerveau partagé, traite celle-là et reste dedans : une note capturée dans un cerveau partagé a déjà été vue par son audience, la sortir ne sert à rien.

## Avant de commencer

1. Lis le contexte de l'utilisateur :
   - `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Moi.md`
   - L'intention de la phase active (dans `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/`)
2. Liste les projets actifs et les casquettes **de tous les cerveaux présents** (les dossiers sous `Cerveaux/`) : un item peut concerner un projet qui vit déjà dans un cerveau partagé.
3. Scanne le contenu de `0 INBOX/`.

## Processus

### Étape 1 : Scanner l'inbox

```
J'ai trouvé [X] items dans ton inbox :

1. [Fichier 1] : [aperçu]
2. [Fichier 2] : [aperçu]
...

On les traite un par un ?
```

### Étape 2 : Pour chaque item, deux décisions

**Décision A, le dossier.** À quoi ça sert ?

| Type | Destination |
|---|---|
| Initiative avec un objectif et une deadline | `1 PROJETS/` |
| Lié à une responsabilité permanente, un process, un rôle | `2 CASQUETTES/` |
| Référence, note de lecture, source brute | `3 RESSOURCES/` |
| Obsolète ou déjà traité | `5 ARCHIVE/` |
| Doublon, note vide, sans valeur | supprimer (confirme avant) |

**Décision B, le cerveau.** Qui doit pouvoir le lire ?

Range dans le bon cerveau selon son audience. Les cerveaux disponibles sont les dossiers présents sous `Cerveaux/` ; la règle de routage par audience est dans le `AGENTS.md` racine. S'il n'y a que le `Cerveau Privé`, tout y va.

Ne propose un cerveau partagé que si l'item est **manifestement** collectif : un process d'équipe, une fiche client, une doctrine métier. Dans tous les autres cas, le `Cerveau Privé`. C'est le défaut, et il ne coûte rien : une note peut monter plus tard, elle ne peut pas redescendre.

Présente les deux décisions ensemble :

```
**Item :** [nom du fichier]
**Contenu :** [résumé en 1-2 phrases]
**Type détecté :** [Idée / Tâche / Référence / Réflexion / Autre]

**Ma proposition :** `Cerveau Privé/1 PROJETS/Refonte Site/`

**Autres options :**
1. Autre dossier (casquette, ressource, archive)
2. Autre cerveau (un cerveau partagé, s'il en existe un)
3. Développer maintenant (on creuse ensemble avant de classer)
4. Supprimer

Ça te va ?
```

### Étape 3 : Exécuter

**→ Cerveau Privé :** déplace, crée le dossier et la note de contexte si besoin (template Projet ou Casquette), retire l'item de l'inbox.

**→ Cerveau partagé :** ne déplace pas directement. **Passe par le skill `/partager`** : il lit le `AGENTS.md` du cerveau de destination et contrôle la confidentialité avant de valider. Un secret ou un chiffre de chiffre d'affaires qui part dans un cerveau partagé par un traitement d'inbox mécanique, c'est exactement ce qu'on veut éviter.

**→ Développer :** passe en mode `/thinking-partner` pour creuser, puis reviens classer le résultat.

**→ Supprimer :** confirme, puis supprime.

### Étape 4 : Récapitulatif

```
Inbox traité.

**Rangé :**
- [X] → Cerveau Privé
- [X] → cerveaux partagés (une ligne par cerveau concerné, s'il y en a)
- [X] → Supprimés

**Items restants :** [X]
```

## Conseils

- Traite l'inbox régulièrement, idéalement chaque jour
- En cas de doute sur le dossier : demande
- En cas de doute sur le cerveau : `Cerveau Privé`, sans demander
- Mieux vaut classer imparfaitement dans le bon cerveau que parfaitement dans le mauvais
