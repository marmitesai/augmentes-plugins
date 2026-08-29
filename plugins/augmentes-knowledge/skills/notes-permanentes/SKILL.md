---
name: notes-permanentes
description: Transformer des sources (highlights, podcasts, livres) en notes atomiques permanentes (Zettelkasten), reformulées et connectées au Garden du Cerveau Privé. Repère aussi les notes mûres pour une audience plus large et propose de les promouvoir via /partager.
---

# Session Notes Permanentes

Tu guides l'utilisateur dans une session de création de notes permanentes (Zettelkasten) à partir de ses sources : highlights Readwise, podcasts déconstruits, livres, articles, ou toute autre note des cerveaux.

Une note permanente = un concept autonome, reformulé dans les mots de l'utilisateur, connecté au reste du Garden.

## Où naissent les notes permanentes

Chaque cerveau installé a son `6 GARDEN/`. Une seule règle :

**Une note permanente naît toujours dans le Garden du Cerveau Privé : `Cerveaux/Cerveau Privé/6 GARDEN/Notes/`. Toujours.** Les MOCs aussi (`.../6 GARDEN/Notes/MOC/`).

C'est le lieu de la pensée en train de se faire. On distille en Privé, on promeut ensuite.

Une note permanente qui devient utile à d'autres (un concept métier, une méthode, une doctrine, un vocabulaire commun) se **promeut** vers le `6 GARDEN/` du cerveau de son audience, quand un cerveau partagé existe. Les cerveaux présents sont les dossiers sous `Cerveaux/` ; le `AGENTS.md` à la racine du workspace dit qui lit quoi. Si ce workspace n'a que le Cerveau Privé (version Solo), il n'y a pas de promotion : la note reste privée, et c'est très bien.

La promotion passe par le skill `/partager`, qui fait le contrôle de confidentialité et le déménagement. Jamais de copie : la note **déménage**. Deux copies qui divergent, c'est deux notes fausses.

## Avant de commencer

1. Lis le contexte de l'utilisateur (`Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Moi.md`)
2. Scanne `Cerveaux/Cerveau Privé/6 GARDEN/Notes/` (notes et MOC) pour connaître les thèmes déjà documentés
3. Repère les cerveaux partagés présents (`ls Cerveaux/`, tout dossier autre que `Cerveau Privé`) et scanne leur `6 GARDEN/` : des notes déjà promues y vivent, elles sont des cibles de liens légitimes et il ne faut pas les redoubler en Privé. En version Solo, il n'y a que le Cerveau Privé : saute ce point
4. Si un dossier `Cerveaux/Cerveau Privé/3 RESSOURCES/Readwise/` existe, note les sources disponibles

## Étape 1 : Choisir la source

Demande à l'utilisateur :

```
Session Notes Permanentes

Comment tu veux procéder ?
a) Je scanne tes sources récentes (Readwise, podcasts, livres) et te propose les meilleurs concepts à extraire
b) Tu me donnes une source spécifique à traiter (note, livre, podcast, article)
c) On complète les notes en brouillon (stubs/drafts) existantes dans le Zettelkasten
d) On passe en revue le Garden privé et on regarde ce qui mérite d'être promu vers un cerveau partagé
```

## Étape 2 : Identifier les concepts

### Si option a) : Sources récentes
1. Scanne les fichiers récents dans `Cerveaux/Cerveau Privé/3 RESSOURCES/` (Readwise, Podcasts, Livres)
2. Identifie les passages riches en concepts (pas les simples citations)
3. Propose 3-5 concepts extractibles, avec pour chacun :
   - Le concept en une phrase
   - La source
   - Un lien potentiel avec une note existante

### Si option b) : Source spécifique
1. Lis la source demandée
2. Identifie TOUS les concepts extractibles
3. Propose-les groupés par thème

### Si option c) : Compléter l'existant
1. Lis les stubs et drafts du Zettelkasten
2. Cherche dans les sources des highlights pertinents pour les compléter
3. Propose du contenu pour chaque note incomplète

### Si option d) : Revue de promotion
Va directement à l'Étape 5.

**→ Attendre validation de l'utilisateur avant de créer.**

## Étape 3 : Créer les notes permanentes

Pour chaque concept validé par l'utilisateur :

### 3.1 : Créer la note

Emplacement : `Cerveaux/Cerveau Privé/6 GARDEN/Notes/`. Même quand le concept est manifestement destiné à l'équipe : on l'écrit en Privé, on le promeut après (Étape 5).

```markdown
---
type: permanent
status: complete
source: [[Nom de la source]]
MOC: [[MOC pertinente]]
created: [date]
---

# [Titre du concept]

[Le concept reformulé dans les mots de l'utilisateur - 5-10 lignes, autonome et compréhensible sans contexte]

---

## References

> [Citation originale ou passage clé de la source]
- *[Source]*

## Liens

- [[Note existante 1]] - [type de relation : renforce, nuance, contredit, complète]
- [[Note existante 2]] - [type de relation]

## Notes connexes

- [Suggestion de connexion avec d'autres thèmes du vault]
```

### 3.2 : Mettre à jour la MOC

Si une MOC pertinente existe dans `Cerveaux/Cerveau Privé/6 GARDEN/Notes/MOC/`, ajouter la nouvelle note.
Si aucune MOC ne correspond, proposer d'en créer une.

### 3.3 : Proposer des connexions

Scanner le Garden privé et les cerveaux pour des notes liées :
- Types de relation : renforce, nuance, contredit, complète, applique
- Ne forcer aucune connexion : seulement les liens réels

## Étape 4 : Repérer ce qui mérite d'être promu

À chaque note créée ou complétée, pose-toi la question de l'audience.

Candidat à la promotion :
- un concept métier, une méthode, une doctrine, une définition qui fait vocabulaire commun
- une note que l'utilisateur va vouloir citer devant d'autres
- une note stable, aboutie, qu'il assume

Reste en Privé :
- un brouillon, une intuition, un `status: draft`
- une note qui parle de personnes nommées ou porte un jugement
- une note personnelle (santé, famille, argent, ressenti)
- tout ce sur quoi tu hésites. Le doute laisse la note en Privé.

Signale les candidats, ne les promeus pas de toi-même :

```
**Candidats à la promotion :**
- [[Nom de la note]] → [cerveau partagé de son audience] (concept de méthode, utile au-delà de toi)
- [[Autre note]]     → [cerveau partagé de son audience] (arbitrage, cercle restreint)

Lance /partager quand tu veux les faire monter.
```

## Étape 5 : Promouvoir (via /partager)

Si l'utilisateur valide une promotion, tu passes la main au skill `/partager`. Il fait le contrôle de confidentialité et le `mv`. Tu ne déplaces pas une note à la main.

Avant de lui passer la main, fais le **contrôle des wikilinks**, c'est le piège propre au Garden.

### Le piège des wikilinks morts

Une note promue **garde ses `[[wikilinks]]` tels quels**. Ceux qui pointent vers des notes restées dans le Cerveau Privé deviennent des liens morts pour les autres lecteurs : ils voient un lien, ils cliquent, il n'y a rien. Une note permanente est dense en liens, donc elle est la plus exposée. Vérifie avant, jamais après.

Pour chaque note candidate :

1. Extrais tous les `[[wikilinks]]` de la note, y compris ceux du frontmatter (`source:`, `MOC:`)
2. Pour chacun, cherche la note cible dans le cerveau de destination
3. Une cible absente du cerveau de destination = lien mort après promotion

Rends le verdict :

```
**Contrôle des liens avant promotion de [[Nom de la note]] vers [cerveau] :**

✅ 3 liens résolus dans [cerveau]
⚠️ 2 liens seront morts :
   - [[Concept X]]   (reste en Cerveau Privé)
   - [[MOC Méthode]] (reste en Cerveau Privé)

Pour chacun, deux options :
   a) Retirer le lien de la note (ou le remplacer par le texte simple)
   b) Promouvoir aussi la note cible (elle passe par le même contrôle de confidentialité)

Tu fais quoi ?
```

Si la cible d'un lien est elle-même promouvable, propose de la promouvoir dans la même passe : une grappe de notes qui se citent monte ensemble ou reste ensemble. Une MOC promue sans ses notes est une coquille vide, une note promue sans sa MOC est orpheline. Signale-le.

Attention aussi au **sens inverse** : les notes restées en Privé qui pointaient vers la note promue ont maintenant un lien mort côté privé. `/partager` le signale, garde l'info dans ton récapitulatif.

## Étape 6 : Résumé de session

```
Session terminée !

**Notes créées :** [X] (Cerveau Privé / 6 GARDEN)
**Notes complétées :** [X]
**MOC mises à jour :** [liste]
**Notes promues :** [X] → [cerveau], via /partager
**Candidats à promouvoir :** [liste, ou aucun]

Veux-tu :
a) Continuer avec d'autres concepts de la même source ?
b) Traiter une autre source ?
c) C'est bon pour maintenant ?
```

## Règles

- **Une note = un concept** (atomicité) : si une note couvre 2 idées, la découper
- **Max 1 écran** par note (~200-500 mots)
- **Toujours reformuler** dans les mots de l'utilisateur, jamais copier-coller le highlight brut
- **Toujours lier** à au moins une MOC et proposer des connexions
- **Demander validation** avant de créer chaque note (montrer le contenu proposé)
- **Style de l'utilisateur** : lire `Moi.md` et le référentiel style s'il existe
- **Toute note naît en Privé** : `Cerveaux/Cerveau Privé/6 GARDEN/Notes/`, les MOC dans `.../MOC/`
- **Promouvoir = déménager**, via `/partager`. Jamais de copie dans deux cerveaux, jamais de `mv` à la main
- **Vérifier les wikilinks avant toute promotion.** Un lien vers une note restée privée sera mort pour les autres
- **Dans le doute, la note reste en Privé.** Le partage est irréversible
