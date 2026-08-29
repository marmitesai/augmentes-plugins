---
name: partager
description: Déménage une note du Cerveau Privé vers un cerveau partagé (son audience), après contrôle de confidentialité. Utiliser quand l'utilisateur dit "partage cette note", "ça peut aller au CODIR", "rends ça visible pour l'équipe", "/partager".
---

# Partager une note

Tu déménages une note d'un cerveau vers un autre. C'est une action **irréversible** : une fois lue par d'autres, elle ne se dé-partage pas. Tu contrôles avant, tu déplaces ensuite.

## Le principe

Une note vit dans **un seul** cerveau. Partager, c'est **déplacer**, jamais copier. Deux copies qui divergent, c'est deux notes fausses.

Le sens de circulation est toujours le même :

```
Cerveau Privé  →  un cerveau partagé
```

On monte vers une audience plus large. On ne redescend pas : une note déjà partagée ne redevient pas privée.

## Processus

### Étape 0 : Un cerveau partagé existe-t-il ?

Regarde les cerveaux présents : `ls Cerveaux/`. Tout dossier autre que `Cerveau Privé` est un cerveau partagé, cible de promotion possible.

Si le seul cerveau est `Cerveau Privé` (version Solo), il n'y a nulle part où promouvoir. Dis-le et arrête-toi :

> Ce workspace n'a pas de cerveau partagé, rien à promouvoir. Tout vit dans le Cerveau Privé. Tu pourras ajouter un cerveau partagé plus tard, et à ce moment-là les notes pourront monter.

Sinon, continue.

### Étape 1 : Identifier la note

Si l'utilisateur ne l'a pas nommée, demande. S'il désigne un dossier entier (un projet), traite les notes une par une : le contrôle de confidentialité est par note, pas par lot.

Lis la note **intégralement**. Tu ne peux pas contrôler ce que tu n'as pas lu.

### Étape 2 : Déterminer l'audience

Propose les cerveaux partagés présents (repérés à l'Étape 0) comme options. Sers-toi du `AGENTS.md` à la racine du workspace pour dire quelle audience lit quel cerveau.

```
**Note :** [nom]
**Contenu :** [résumé en 2 lignes]

Qui doit pouvoir la lire ?

1. [Cerveau partagé]                     → [son audience, d'après le AGENTS.md racine]
2. [Autre cerveau partagé, s'il existe]  → [son audience]
3. Finalement personne                   → elle reste où elle est
```

### Étape 3 : Contrôle de confidentialité

Lis le `AGENTS.md` du cerveau de destination. Applique **sa** règle, pas une règle générique.

Puis passe la note au crible. Signale tout ce qui accroche :

**Bloquant, quel que soit le cerveau de destination :**
- mot de passe, clé d'API, identifiant, secret technique en clair
- donnée personnelle de tiers (santé, RH nominative, dossier de personne)

**Bloquant pour un cerveau lu par toute l'entreprise** (le `AGENTS.md` de destination fait foi) **:**
- salaires, données RH, contrats de personnes
- finances de l'entreprise (chiffre d'affaires, marges, comptes)
- poids d'un client dans le CA, ou tout chiffre qui permet de le reconstituer
- sujets qui relèvent d'un cercle plus restreint (stratégie, cession, arbitrages de direction)

**À signaler dans tous les cas :**
- jugement sur une personne nommée
- information obtenue en confidence
- brouillon non abouti que l'utilisateur n'assume peut-être pas encore

Rends le verdict :

```
**Contrôle avant partage vers [cerveau] :**

✅ Rien de bloquant
   ou
⚠️ [X] point(s) à traiter :
   - Ligne 12 : le mot de passe du serveur en clair
   - Ligne 30 : « ALPHA pèse 18% de notre CA »

**Ce que je propose :**
   - Ligne 12 → remplacer par une référence au gestionnaire de secrets
   - Ligne 30 → retirer la phrase (elle permet de reconstituer le CA)

Je corrige et je partage, ou tu préfères revoir la note d'abord ?
```

**Ne déplace jamais une note qui a un point bloquant non traité.** Corrige d'abord, ou renonce.

### Étape 4 : Déplacer

1. Calcule le chemin de destination : **même chemin relatif, autre racine**. Le squelette IPCRA est identique dans chaque cerveau, le rangement se conserve.
   `Cerveau Privé/1 PROJETS/Refonte Site/Brief.md` → `Cerveau Entreprise/1 PROJETS/Refonte Site/Brief.md`
2. Si le dossier parent n'existe pas dans le cerveau de destination, crée-le.
3. **Déplace** le fichier (`mv`). Ne le copie pas.
4. Vérifie les `[[wikilinks]]` de la note : si elle pointe vers des notes restées dans le `Cerveau Privé`, ces liens seront morts pour les autres lecteurs. Signale-les et propose soit de les retirer, soit de partager aussi les notes cibles.
5. Cherche qui pointait vers la note déplacée (`grep -r "[[nom de la note]]"`) et signale les liens désormais cassés côté privé.

### Étape 5 : Récapituler

```
**Partagé.**

[Nom de la note]
  Cerveau Privé/1 PROJETS/Refonte Site/Brief.md
  → Cerveau Entreprise/1 PROJETS/Refonte Site/Brief.md

**Corrections avant partage :** [X]
**Liens à surveiller :** [X] wikilinks pointent encore vers des notes privées

Rappel : c'est irréversible. La note est lisible par [audience].
```

## Ce que tu ne fais jamais

- Copier au lieu de déplacer
- Partager un lot sans lire chaque note
- Descendre une note vers une audience plus restreinte en pensant « annuler » un partage
- Partager une note qui contient un secret, même « juste pour dépanner »
- Décider seul quand tu hésites : dans le doute, la note reste où elle est
