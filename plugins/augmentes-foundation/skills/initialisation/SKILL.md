---
name: initialisation
description: Initialiser le vault Perspectives IA via conversation guidée. Pédagogie IPCRA, décharge projets/casquettes/contexte, dépôt de documents à tout moment (CV, bios, offres écrites), création complète de la structure et des fichiers de contexte personnalisés. Écrit chaque note au fur et à mesure (à la fin de son étape, pas tout à la fin) pour garder une fidélité maximale, puis clôture par une passe de relecture qui vérifie la cohérence et génère les artefacts transversaux (daily note d'init, configs Obsidian).
---

# Initialisation du Vault Perspectives IA

Tu initialises ce vault avec les informations de l'utilisateur via une conversation guidée. En même temps, tu **expliques** ce qu'on met en place et pourquoi : l'utilisateur comprend ce qu'il fait, pas seulement ce qu'il remplit.

## Règle transversale : dépôt de documents

**À tout moment** pendant les étapes de décharge (Étapes 3 à 7), l'utilisateur peut déposer des fichiers pour compléter ou remplacer la réponse vocale/écrite : CV, bios historiques, notes de parcours, offres écrites, briefs clients, archives de réunions, journal intime, anciens coachings, etc.

À chaque grande étape, rappelle cette affordance :

> « Tu peux aussi me déposer ici des fichiers (PDF, docs, notes) qui couvrent cette section : CV, bio, historique, offres écrites, anciens docs. Je les lis et j'en extrais ce qui compte. »

Quand un fichier est déposé :
1. **Lis-le intégralement** (via Read pour les .md/.txt, via les outils PDF pour les .pdf, etc.)
2. **Extrais** les informations pertinentes pour la section en cours
3. **Résume** à l'utilisateur ce que tu as compris et demande validation ou compléments
4. **Continue** la section avec les gaps restants (si le document n'a pas tout couvert)

## Principe transversal : écrire au fur et à mesure

On écrit chaque note à la **fin de son étape**, pas tout à la fin. Ça garde une fidélité maximale : on écrit depuis la décharge fraîche et brute de chaque section, pas depuis un recap compressé 30-40 minutes plus tard (au risque d'oublier des choses).

- Les artefacts self-contained (`Mon Parcours.md`, `Moi.md`, les notes de Casquette, les notes de Projet, la Phase de vie) sont écrits à la fin de leur étape, juste après la décharge + validation de cette étape. `Moi.md` est écrit en deux temps : le gros à la fin de l'Étape 4 (Qui tu es + Vision), complété à la fin de l'Étape 8 (style IA, valeurs, rythme).
- Le patch des `AGENTS.md` (nom de l'IA + prénom) est appliqué dès l'Étape 2.
- Les artefacts transversaux (daily note d'initialisation, configs Obsidian) sont générés à la fin, pendant la passe de relecture (Étape 12), parce qu'ils agrègent ou dépendent de plusieurs sections.

Chaque étape de décharge se clôt sur une sous-étape « Écrire ». Annonce-le : « Maintenant j'écris [fichier] avec ce qu'on vient de capturer. Voilà ce que je mets dedans. » Écris, puis demande une validation rapide avant de passer à l'étape suivante. Le format exact de chaque fichier reste défini à l'Étape 12 (blocs de référence).

---

## Étape 1 : Prélude pédagogique (explique le système)

Regarde d'abord combien de cerveaux sont présents : `ls Cerveaux/`. Un (version Solo), deux (Privé plus un partagé) ou trois. Adapte le passage sur les cerveaux au nombre réel : ne présente que ceux qui sont là, et en Solo présente le Cerveau Privé comme le seul, sans parler de promotion vers d'autres. Dis à l'utilisateur (adapte le ton, ne le récite pas mot pour mot, formule en conversant) :

```
Bienvenue. On va initialiser ton second cerveau.

## Où on est

Tu es dans un WORKSPACE : un dossier parent qui héberge deux choses.

  Cerveaux/     ta mémoire. Ce qui se relit.
  Atelier/      ta production. Ce qui se lance. Code, exports, builds. Jetable.

Aujourd'hui on remplit les cerveaux.

## Tes cerveaux, une audience chacun

Selon la version installée, tu as un, deux ou trois cerveaux. Même structure
dans chacun, mais pas les mêmes lecteurs :

  Cerveau Privé        Toi seul. Personne d'autre. C'est le défaut :
                       toute note naît ici. Toujours présent.

  Cerveau Direction    Ton cercle restreint (on le renommera à ton
                       vocabulaire : CODIR, COMEX, Bureau, Associés).
                       Dossier partagé. Présent en version complète.

  Cerveau Entreprise   Toute ta boîte. Dossier partagé.
                       Présent dès que tu partages au-delà de toi.

[Un seul cerveau présent : tu es en version Solo. Un seul cerveau, le Privé.
Présente-le comme tel et saute la mécanique de promotion : tout vit ici,
on pourra ajouter un cerveau partagé plus tard.]

Pourquoi séparer. Un cerveau unique t'oblige à t'autocensurer en écrivant
(« et si quelqu'un lisait ça ? »), ou à tout garder pour toi et ne rien
transmettre. Des cerveaux séparés dissocient la question « qu'est-ce que je pense »
de la question « qui doit le lire ». Tu écris librement en privé, et tu
promeus ce qui doit l'être, quand c'est prêt.

La règle tient en une question : **qui doit pouvoir lire ça ?**
Dans le doute, c'est le Cerveau Privé. Toujours. Une note peut monter
plus tard. Elle ne peut pas redescendre : une fois lue, elle est lue.

Une note vit dans UN seul cerveau. Partager, c'est déplacer, jamais copier.
Le skill `/partager` fait ce déménagement et vérifie avant d'envoyer
(pas de mot de passe, pas de salaire, pas de chiffre d'affaires qui traîne).

## Le deal

Ce que je te propose de faire maintenant, en trois temps :

  1. Je te présente ce qu'on met en place et pourquoi (5 min)
  2. Tu décharges : tout ce qu'il faut pour peupler ton contexte (20-40 min, adaptable)
  3. Je génère la structure complète de ton vault + tes fichiers de contexte

Tu peux répondre à l'écrit, à l'oral (SuperWhisper), ou me déposer des documents
à chaque étape. On prend le temps qu'il faut.

## Pourquoi un second cerveau

La puissance de l'IA émerge de TON contexte.

  IA sans contexte    = réponses génériques, réinvente la roue à chaque prompt,
                        ne te connaît ni toi, ni tes projets, ni tes clients.

  IA avec ton contexte = extension de toi-même, connaît tes projets, tes offres,
                        ta vie. Exécute dans ton cadre, pas hors-sol.

L'équation : **Qualité IA = Qualité du contexte x Qualité du modèle**.
Le modèle, tu le choisis une fois. Le contexte, on le construit maintenant.

## IPCRA : organiser par utilité

La vraie question, c'est pas « de quoi ça parle ? » mais « à quoi ça sert ? »

  Par thématique (Marketing, Finance, Santé, Famille)
    tu cherches partout, tout se mélange, l'IA se perd.

  Par utilité (IPCRA)
    tu vois tout de suite ce qui est actionnable vs ce qui dort.

Les 7 dossiers IPCRA, identiques dans chaque cerveau :

  0 INBOX       Tout ce qui arrive, avant tri. Tampon temporaire.
  1 PROJETS     Ce sur quoi tu bosses activement (deadline, archive après).
  2 CASQUETTES  Tes rôles permanents (dirigeant, parent, santé, créateur).
  3 RESSOURCES  Référence utile mais inactive. Le brut.
  4 TOOLS       Templates, scripts, skills IA.
  5 ARCHIVE     Terminé ou inactif (mais accessible).
  6 GARDEN      Connaissance distillée. Ce que tu as digéré et reformulé.

Le squelette est le même dans chaque cerveau, et c'est voulu : déplacer
une note d'un cerveau à l'autre, c'est changer la racine du chemin. Rien d'autre.

### Projet vs Casquette : la distinction clé

  PROJET      = temporaire, a une deadline, un output défini.
                Ex : « Lancer le podcast », « Refonte site ». Deadline, puis archive.

  CASQUETTE   = permanent, une aire de responsabilité, pas de fin.
                Ex : « CEO de X », « Santé », « Finances perso ». Ça vit tout le temps.

## Le principe qu'on ne lâche jamais

**On amplifie, on ne remplace pas.**
On ne te crée pas de nouveaux usages externes. On mappe ce que tu fais déjà,
ce qui produit de la valeur, et on l'amplifie avec l'IA.

---

Des questions sur tout ça avant qu'on commence ? Sinon, on attaque avec « Qui tu es ».
```

Attends une confirmation ou une question. Réponds aux questions. Puis enchaîne sur l'Étape 2.

---

## Étape 2 : Nommer l'IA, la personne, la boîte

**Avant toutes les décharges**, pose ces questions :

```
1. Comment tu veux que je t'appelle ? (prénom ou surnom, je vais l'utiliser tout le temps)
2. Et moi, comment tu veux que je m'appelle ? (tu donnes un nom à ton IA, c'est elle
   que tu invoqueras quand tu ouvriras ton workspace)
3. Ta boîte, elle s'appelle comment ? Et toi, tu y fais quoi ?
```

Une fois les réponses recueillies :
- Le **prénom** sera aussi stocké dans `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Moi.md` (Étape 12)
- Le **nom de l'IA** vit dans l'`AGENTS.md` **à la racine du WORKSPACE** : c'est son identité globale, valable partout, pas seulement dans les cerveaux

### Écrire : patcher les AGENTS.md

Dès maintenant, patche les quatre placeholders dans chaque `AGENTS.md` présent (celui de la racine, plus un par cerveau installé). Le glob `Cerveaux/*/AGENTS.md` prend les cerveaux réellement là, qu'il y en ait un, deux ou trois :

```bash
for f in AGENTS.md Cerveaux/*/AGENTS.md; do
  sed -i '' "s/\[Nom IA\]/[Nom choisi]/g; s/\[Prénom\]/[Prénom]/g; \
             s/\[Entreprise\]/[Entreprise]/g; s/\[fonction\]/[fonction]/g" "$f"
done
```

Vérifie qu'il ne reste aucun placeholder : `grep -rn '\[Prénom\]\|\[Nom IA\]\|\[Entreprise\]\|\[fonction\]' AGENTS.md Cerveaux/*/AGENTS.md`

Dis à l'utilisateur : « J'ai enregistré ton prénom, ta boîte et le nom de l'IA (« [Nom IA] »). À partir de maintenant je me réfère à moi sous ce nom. » Puis passe à l'Étape 2 bis.

---

## Étape 2 bis : Nommer et brancher les cerveaux partagés

Regarde d'abord les cerveaux présents : `ls Cerveaux/`. À part `Cerveau Privé`, chaque dossier est un cerveau partagé. Il y en a zéro, un ou deux selon la version installée.

**Aucun cerveau partagé (version Solo)** : un seul cerveau, le Privé. Dis-le en un mot (« Ce kit est en version Solo, un seul cerveau. On passe. ») et enchaîne sur l'Étape 3. Un cerveau partagé pourra s'ajouter plus tard.

Sinon, traite CHAQUE cerveau partagé présent. Ne t'attarde pas : le montage technique peut se faire plus tard, la décharge est plus importante.

### Nommer le cerveau du cercle restreint (s'il est présent)

Le `Cerveau Direction` est le cercle avec qui l'utilisateur partage la stratégie et le pilotage. S'il est présent :

```
Ton « Cerveau Direction », c'est le cercle avec qui tu partages la stratégie
et le pilotage. Chez toi, il s'appelle comment ? CODIR, COMEX, Bureau,
Associés, autre chose ?

Et s'il ne correspond à rien chez toi (tu diriges seul, ou tout se dit devant
tout le monde) : on le retire, les autres cerveaux suffisent. On pourra
toujours l'ajouter plus tard.
```

S'il donne un nom : renomme le dossier et corrige les mentions.

```bash
mv "Cerveaux/Cerveau Direction" "Cerveaux/Cerveau [Nom]"
sed -i '' "s/Cerveau Direction/Cerveau [Nom]/g" AGENTS.md README.md "Cerveaux/Cerveau [Nom]/AGENTS.md"
```

S'il n'en veut pas : supprime `Cerveaux/Cerveau Direction/` et retire ses mentions de l'`AGENTS.md` racine (et du README). Le cerveau de toute l'entreprise suffit.

Le `Cerveau Entreprise`, lui, garde son nom : c'est le cerveau de toute la boîte.

### Brancher les cerveaux partagés

Pour chaque cerveau partagé qui reste (un ou deux) :

```
Tes cerveaux partagés sont faits pour être lus par d'autres. Ils doivent donc
vivre dans ton espace partagé (Dropbox, OneDrive, SharePoint, Drive), pas sur
ton disque à toi.

Tu veux qu'on les branche maintenant, ou plus tard ? On peut très bien
remplir d'abord et partager après. Le Cerveau Privé, lui, ne bouge jamais.
```

S'il veut le faire maintenant, demande le chemin de son espace partagé. Pour chaque cerveau partagé présent, déplace le dossier et pose un lien symbolique pour que l'IA continue de le voir sous `Cerveaux/` :

```bash
mv "Cerveaux/Cerveau Entreprise" "[chemin de l'espace partagé]/"
ln -s "[chemin de l'espace partagé]/Cerveau Entreprise" "Cerveaux/Cerveau Entreprise"
```

Répète pour chaque cerveau partagé (le cercle restreint sous le nom retenu, s'il existe). Vérifie que chaque lien répond (`ls "Cerveaux/[nom du cerveau]/"`) avant de continuer. Sur Windows, c'est `New-Item -ItemType SymbolicLink` dans un PowerShell administrateur (voir le README).

S'il préfère plus tard : note-le, tu le lui rappelleras à l'Étape 13.

---

## Étape 3 : Section 01 : Qui tu es

Annonce :

```
On attaque par « Qui tu es ». C'est la section la plus importante, prends le temps.
Tu peux me déposer des PDF, ton CV, des bios, des docs qui remontent ton parcours.
J'en extrais ce qui compte et on complète ensemble avec ce qui manque.
```

Pose ces questions **une par une**, attends la réponse entre chaque :

1. **Raconte-moi ton parcours.** Les étapes clés, les tournants, les chiffres importants. Sois précis : dates, entreprises, CA, équipes, durées. Pas « j'ai lancé une boîte » mais « J'ai lancé [Nom] en 2019, CA année 1 : 20k, année 2 : 80k, solo jusqu'en 2021 puis équipe de 3 ».

2. **Comment tu fonctionnes ?** Forces, faiblesses, façon de prendre des décisions (analyse / intuition / consultation), gestion du stress. Si tu connais ton MBTI, donne-le. Sinon [16personalities.com](https://www.16personalities.com/fr) prend 10 min.

3. **Passions, intérêts actuels, grandes convictions.** Les sujets sur lesquels tu peux passer des heures. Sois précis : pas « la tech » mais « les systèmes de pensée augmentée, les PKM, l'IA appliquée au knowledge management ».

Après chaque réponse : reformule ce que tu as compris en 2-3 phrases, demande si c'est juste, puis passe à la question suivante. Rappelle discrètement à l'utilisateur qu'il peut déposer un document ou répondre à voix haute (SuperWhisper).

### Écrire : `Mon Parcours.md`

Maintenant écris `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Mon Parcours.md` avec l'historique chronologique capturé + ce que tu as extrait des documents déposés (structure par année / grande période). Format défini à l'Étape 12.3.

Le reste de cette section (parcours en bref, forces, faiblesses, passions, MBTI) alimente `Moi.md`, qui est écrit à la fin de l'Étape 4 : garde-le en mémoire pour l'instant.

Dis à l'utilisateur : « J'ai écrit Mon Parcours.md avec ton historique. Quick check : ça matche ? Quelque chose à corriger ? » Applique les corrections, puis passe à l'Étape 4.

---

## Étape 4 : Section 02 : Ta vision

Annonce :

```
Maintenant, ta vision. Sans vision claire, tu subis les opportunités au lieu de les
choisir : la vision, c'est le phare qui guide tes décisions.

Ici aussi tu peux déposer des docs : manifeste perso, notes de vision, feuille de
route long-terme, si tu en as.
```

Pose **une par une** :

1. **Décris ta journée idéale**, du réveil au coucher. Sois concret : heures, activités, lieux, qui est avec toi, quelle énergie.

2. **Projette-toi à 12 mois.** Tout s'est bien passé. Qu'est-ce qui s'est passé ? Concrètement : métriques, événements, relations, état d'être.

3. **À 5 ans ?** Même exercice. Qu'est-ce que tu vois ?

4. **3 à 5 actions quotidiennes essentielles pour être heureux.** Pas des valeurs abstraites : des actions concrètes qui, si tu les fais, font que ta journée est bonne.

### Écrire : `Moi.md` (première passe)

Maintenant crée `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Moi.md` (format complet à l'Étape 12.2) et remplis les sections déjà capturées :
- Depuis l'Étape 3 : **Prénom**, **Qui je suis** (2-3 phrases), **Forces**, **Faiblesses**, **Passions**, **MBTI**.
- Depuis l'Étape 4 : **Vision long-terme** (12 mois + 5 ans) et **Actions essentielles quotidiennes**.

Laisse en attente les sections **Style de communication IA**, **Valeurs et principes** et **Comment je travaille** : elles seront complétées à la fin de l'Étape 8 (mets un court `_(à compléter Étape 8)_` en placeholder). Conserve la frontmatter (`type: context, status: active`). Ne mets jamais le nom de l'IA dans `Moi.md` (il va dans `AGENTS.md`).

Dis à l'utilisateur : « J'ai écrit Moi.md avec qui tu es et ta vision. Quick check : ça matche ? » Applique les corrections, puis passe à l'Étape 5.

---

## Étape 5 : Section 03 : Décharge Casquettes

Annonce :

```
On décharge tes casquettes. Rappel : une casquette = une aire de responsabilité
permanente, pas de deadline.

Exemples : CEO de [ta boîte], Papa, Santé, Finances perso, Ami proche, Créateur.
La plupart des gens ont entre 3 et 7 casquettes.

Liste-les moi d'abord, juste les noms. Ensuite on remplit 6 champs par casquette.
Et si tu as des docs pertinents (descriptions de rôle, OKR ongoing, etc.), dépose-les.
```

### 5.1 : Lister les casquettes

L'utilisateur liste ses casquettes. Tu les reformules pour validation avant d'attaquer le remplissage.

### 5.2 : Par casquette, conversation ouverte

**Pour chaque casquette, une par une**, ouvre avec cette question :

> « Parle-moi de [Casquette]. En quoi ça consiste pour toi concrètement ? Quel est ton rôle là-dedans ? »

Écoute la réponse. Pose ensuite des **questions de clarification adaptées à ce que tu entends** : pas de checklist figée. L'objectif n'est pas de remplir un formulaire mais de capturer ce qui permettra à l'IA de t'aider sur cette casquette demain.

**Banque d'inspiration** (à piocher selon ce qui manque, pas à dérouler mécaniquement) :
- Qu'est-ce que « bien tenir cette casquette » veut dire pour toi ?
- Qu'est-ce que tu fais régulièrement dans ce rôle ? (quotidien / hebdo / mensuel)
- Qui est impliqué autour de toi ? (équipe, proches, prestataires)
- Quels outils tu utilises ?
- Qu'est-ce qui est pénible ou dysfonctionnel en ce moment ?
- Qu'est-ce que tu veux changer ou améliorer dans cette zone ?

Rappelle l'affordance document : « Tu peux aussi me déposer ici des docs liés à cette casquette (descriptions de rôle, OKR, notes historiques) : je les intègre. »

**Suis l'énergie de la réponse** : si une question tombe à plat, passe à autre chose. Si une réponse ouvre une piste riche, creuse-la. Reformule brièvement à la fin pour validation, puis passe à la casquette suivante.

### Écrire : créer les notes de Casquette

À la fin de l'Étape 5, une fois toutes les casquettes déchargées et validées, crée tous les fichiers de casquette (format + cas spécial « casquette Business » à l'Étape 12.4) :

Pour chaque casquette :
```bash
mkdir -p "Cerveaux/Cerveau Privé/2 CASQUETTES/[Nom]"
```
Écris `Cerveaux/Cerveau Privé/2 CASQUETTES/[Nom]/[Nom].md` depuis le template `Cerveaux/Cerveau Privé/4 TOOLS/Templates/Casquette.md`, rempli avec les champs capturés. Si une activité indépendante a été mentionnée, crée la casquette Business dédiée (Étape 12.4).

Dis à l'utilisateur : « J'ai créé [X] notes de casquette dans 2 CASQUETTES/. Quick check : ça matche ? » Applique les corrections, puis passe à l'Étape 6.

---

## Étape 6 : Section 04 : Décharge Projets

Annonce :

```
Maintenant tes projets actifs et futurs. Rappel : un projet a une fin, une deadline
(même floue). Quand c'est fini, ça va en archive.

Liste-les d'abord. Pour chacun ensuite, 7 questions. Dépose tes docs projet existants
si tu en as (brief, roadmap, offres écrites).
```

### 6.1 : Lister les projets

### 6.2 : Par projet, conversation ouverte

**Pour chaque projet, un par un**, ouvre avec :

> « Parle-moi de [Projet]. De quoi il s'agit, où tu en es, qu'est-ce que tu vises ? »

Écoute la réponse. Pose ensuite des **questions de clarification adaptées** : pas une grille à remplir. Ce qu'on veut, c'est que l'IA puisse t'aider sur ce projet en comprenant son essence, son état, et ce qui bloque.

**Banque d'inspiration** (pioche selon ce qui manque, pas une checklist à dérouler) :
- Pourquoi tu le fais, toi personnellement ? (pas la justification publique)
- Quel est l'output concret ? Qu'est-ce que tu vends ou livres ?
- Quelle deadline ou horizon ?
- Qui bosse dessus avec toi ? Qui joue quoi ?
- Où tu en es exactement : dernières avancées, prochaine étape concrète ?
- Qu'est-ce qui te bloque actuellement ?
- Tâches récurrentes liées à ce projet ?

Rappelle l'affordance document : « Tu as des docs à rapatrier pour ce projet ? Briefs, roadmap, decks, contrats, onboarding client : dépose-les, je les intègre. »

**Creuse ce qui est riche, skip ce qui est déjà clair.** Reformule à la fin pour validation, puis passe au projet suivant.

### Écrire : créer les notes de Projet

À la fin de l'Étape 6, une fois tous les projets déchargés et validés, crée tous les fichiers de projet (format à l'Étape 12.5) :

Pour chaque projet :
```bash
mkdir -p "Cerveaux/Cerveau Privé/1 PROJETS/[Nom]"
```
Écris `Cerveaux/Cerveau Privé/1 PROJETS/[Nom]/[Nom].md` depuis le template `Cerveaux/Cerveau Privé/4 TOOLS/Templates/Projet.md`, rempli avec les champs capturés.

Dis à l'utilisateur : « J'ai créé [Y] notes de projet dans 1 PROJETS/. Quick check : ça matche ? » Applique les corrections, puis passe à l'Étape 7.

---

## Étape 7 : Section 05 : Phase de vie

Explique le concept :

```
Dans ton vault, on organise ton journaling par « phases de vie ». Une phase, c'est
une période avec un focus particulier : ça peut durer 3 semaines ou 6 mois. Quand
ton énergie/focus change (nouveau projet, déménagement, changement de cap), tu
ouvres une nouvelle phase avec /new-life-phase.

Chaque phase a son dossier avec une intention, et c'est là que vivent tes daily
notes et weekly notes. Tu retrouves exactement ce que tu faisais et pensais à une
période donnée de ta vie.

Exemples de phases : « Lancement solo », « Scale & Systems », « Reconstruction »,
« Prépa concours », « Transition pro », « Exploration créative ».
```

Pose **une par une** :

1. **Donne un nom à ta phase actuelle.** Un mot ou une expression qui résume cette période.

2. **Quand ça a commencé ?** Quelle est ton intention pour cette phase ? Tes objectifs concrets ?

3. **Tes contraintes actuelles ?** Temps disponible par semaine, niveau d'énergie, budget, obligations.

4. **Que fais-tu quand tu es surchargé / dispersé / fatigué / dans le flow ?** (stratégies personnelles, précieux pour que l'IA t'aide en contexte).

### Écrire : créer la Phase de vie

À la fin de l'Étape 7 (détail complet à l'Étape 12.6) :
1. Renomme `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/1 Phase initiale/` en `1 [Nom de la phase]/`.
2. Remplis `1 Intention.md` (template `Cerveaux/Cerveau Privé/4 TOOLS/Templates/Phase de vie.md`) : période, intention principale, journée idéale, objectifs, stratégies quand surchargé / dispersé / fatigué / dans le flow.
3. Mets à jour `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/Life Phases.md` (remplace « Phase initiale » par le vrai nom + lien vers l'intention).

Les configs Obsidian (qui pointent vers le dossier de la phase) sont mises à jour à l'Étape 12.7, une fois le nom de la phase figé.

Dis à l'utilisateur : « J'ai créé la phase « [Nom] » et son intention. Quick check : ça matche ? » Applique les corrections, puis passe à l'Étape 8.

---

## Étape 8 : Section Bonus : Contexte global (style IA, valeurs)

Annonce :

```
Dernier bloc avant qu'on crée tes fichiers : le contexte global, comment tu veux
que l'IA te parle, tes valeurs, ton rythme.
```

Pose :

1. **Valeurs & principes** : ce qui guide tes décisions, tes lignes rouges (3 à 5 lignes maximum).

2. **Style de communication IA** : tutoiement ? ton (direct/chaleureux/challengeant) ? langue ? niveau de pushback (tu veux que l'IA te challenge, ou qu'elle exécute) ?

3. **Chrono-type** : tes heures de deep work, ton rythme hebdo.

### Écrire : compléter `Moi.md`

Maintenant complète `Moi.md` (créé en première passe à l'Étape 4) avec les sections restées en attente :
- **Style de communication IA** (tutoiement, ton, langue, niveau de pushback)
- **Valeurs et principes**
- **Comment je travaille** (routines + chrono-type)

Remplace les placeholders `_(à compléter Étape 8)_`. À partir de maintenant, respecte le style de communication qui vient d'être capturé.

Dis à l'utilisateur : « J'ai complété Moi.md avec ton style IA, tes valeurs et ton rythme. Quick check : ça matche ? » Applique les corrections, puis passe à l'Étape 9.

---

## Étape 9 : Analyse et reformulation

Analyse **toutes les réponses et documents déposés** pendant les Étapes 3 à 8. Reformule ce que tu as compris :

1. **Qui est l'utilisateur** (2-3 phrases denses)
2. **Phase de vie actuelle** (nom + focus)
3. **Casquettes identifiées** (noms, 1-3 mots chacune)
4. **Projets actifs** (noms + pitch en 1 phrase)
5. **Casquette Business** (si une activité indépendante a été mentionnée dans les projets ou casquettes : elle mérite sa propre casquette dédiée, on la créera en Étape 11)
6. **Fichiers déposés** et ce que tu en as extrait

---

## Étape 10 : Questions de clarification

Pose 2 à 5 questions pour lever les dernières ambiguïtés :
- Infos manquantes ou contradictoires
- Éléments flous qui deviendront bloquants quand on créera les fichiers
- Confirmations sur les décisions (ex : « la casquette 'Santé' est vraiment distincte de 'Sport' ou on fusionne ? »)

Continue jusqu'à avoir une compréhension complète.

---

## Étape 11 : Validation finale

À ce stade, les notes self-contained sont déjà écrites au fur et à mesure (Étapes 2 à 8). Montre un récapitulatif de l'état du vault et demande une validation explicite avant la passe de relecture (Étape 12) :

```
Voici l'état du vault (déjà écrit au fil des étapes) + ce qu'il reste à générer :

- AGENTS.md (racine WORKSPACE)              <- ajout du nom de l'IA « [Nom IA] » + prénom
- Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Moi.md          <- qui tu es, style IA, valeurs, vision
- Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Mon Parcours.md <- historique chronologique

Casquettes ([X]) :
- Cerveaux/Cerveau Privé/2 CASQUETTES/[Casquette 1]/[Casquette 1].md
- Cerveaux/Cerveau Privé/2 CASQUETTES/[Casquette 2]/[Casquette 2].md
- ... (dont [Casquette Business] si applicable, remplie avec les infos business)

Projets ([Y]) :
- Cerveaux/Cerveau Privé/1 PROJETS/[Projet 1]/[Projet 1].md
- Cerveaux/Cerveau Privé/1 PROJETS/[Projet 2]/[Projet 2].md

Phase de vie :
- Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/1 [Nom phase]/1 Intention.md

Daily note du jour (log d'initialisation) :
- Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/1 [Nom phase]/YYYY-MM-DD.md

Configs Obsidian mises à jour (daily notes + weekly notes -> dossier de la phase)

Confirmes-tu ? (oui / ajustements)
```

---

## Étape 12 : Passe de relecture & génération des artefacts transversaux

À ce stade, les artefacts self-contained ont déjà été écrits au fur et à mesure : le patch des `AGENTS.md` (Étape 2), `Mon Parcours.md` (Étape 3), `Moi.md` (Étapes 4 + 8), les casquettes (Étape 5), les projets (Étape 6), la phase de vie (Étape 7). Cette étape est le **relecteur** :

1. **Relis** tout ce qui a été écrit (Moi.md, Mon Parcours.md, chaque casquette, chaque projet, l'intention de phase) et vérifie la cohérence transversale : chaque projet est-il rattaché à une casquette ? une casquette « Business » a-t-elle bien été créée si une activité indépendante existe ? la phase de vie s'aligne-t-elle avec la vision ? Signale et corrige les mismatches directement.
2. **Génère les artefacts transversaux** qui dépendent de plusieurs sections : la daily note d'initialisation (12.8) et les configs Obsidian (12.7, qui ont besoin du nom de phase figé).

Les blocs 12.1 à 12.8 ci-dessous restent la **référence du format** de chaque fichier (invoquée par les sous-étapes « Écrire » des Étapes 2 à 8). Ne réécris pas un fichier déjà écrit et validé, sauf pour appliquer une correction de cohérence.

### 12.1 : Placeholders dans les fichiers AGENTS.md

Ils ont normalement été patchés à l'Étape 2. Ici tu **vérifies** qu'il n'en reste aucun, dans chaque `AGENTS.md` présent (racine plus un par cerveau installé) et dans le `README.md` :

```bash
grep -rn '\[Nom IA\]\|\[Prénom\]\|\[Entreprise\]\|\[fonction\]' AGENTS.md README.md Cerveaux/*/AGENTS.md
```

S'il en reste, patche-les avec les valeurs recueillies à l'Étape 2, sur tous les fichiers présents :

```bash
for f in AGENTS.md README.md Cerveaux/*/AGENTS.md; do
  sed -i '' "s/\[Nom IA\]/[Nom choisi]/g; s/\[Prénom\]/[Prénom]/g; \
             s/\[Entreprise\]/[Entreprise]/g; s/\[fonction\]/[fonction]/g" "$f"
done
```

L'IA se présente et se réfère à elle-même sous ce nom dans toutes les interactions, peu importe le projet du WORKSPACE ouvert.

### 12.2 : `Moi.md` (`Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Moi.md`)

Remplis la note existante. Conserve la frontmatter (`type: context, status: active`).

```markdown
---
type: context
status: active
---

# Moi

**Prénom :** [Prénom]

## Qui je suis

[Parcours en bref : 2-3 phrases]

**Forces :**
- [Force 1]
- [Force 2]

**Faiblesses :**
- [Faiblesse 1]
- [Faiblesse 2]

**Passions :**
- [Passion 1]
- [Passion 2]

## Style de communication IA

[Tutoiement, ton, langue, niveau de pushback]

## MBTI

[Résultat si donné, sinon vide]

## Valeurs et principes

- [Valeur 1]
- [Valeur 2]

## Comment je travaille

- [Routine 1]
- [Routine 2]

## Vision long-terme

**12 mois :** [description]
**5 ans :** [description]

## Actions essentielles quotidiennes

- [Action 1]
- [Action 2]
- [Action 3]
```

### 12.3 : `Mon Parcours.md` (`Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Mon Parcours.md`)

Remplis avec l'historique chronologique recueilli + les infos extraites des documents déposés. Structure par année / grande période.

### 12.4 : Dossiers Casquettes (`Cerveaux/Cerveau Privé/2 CASQUETTES/[Nom]/[Nom].md`)

Pour chaque casquette :
1. `mkdir -p "Cerveaux/Cerveau Privé/2 CASQUETTES/[Nom]"`
2. Écris `[Nom].md` à partir du template `Cerveaux/Cerveau Privé/4 TOOLS/Templates/Casquette.md`, rempli avec les 6 champs.

**Cas spécial : casquette Business** : si l'utilisateur a une activité indépendante, crée une casquette dédiée (ex : `Cerveaux/Cerveau Privé/2 CASQUETTES/[Nom du business]/`) et remplis avec :
- Positionnement (ce qu'on vend, à qui, pourquoi)
- Offres et tarifs
- Clients et métriques
- Canaux d'acquisition
- Delivery (parcours client, process, outils)
- Équipe, stack technique, URLs

### 12.5 : Dossiers Projets (`Cerveaux/Cerveau Privé/1 PROJETS/[Nom]/[Nom].md`)

Pour chaque projet :
1. `mkdir -p "Cerveaux/Cerveau Privé/1 PROJETS/[Nom]"`
2. Écris `[Nom].md` à partir du template `Cerveaux/Cerveau Privé/4 TOOLS/Templates/Projet.md`, rempli avec les 7 champs.

### 12.6 : Première Phase de vie (`Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/1 [Nom]/`)

1. Renomme `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/1 Phase initiale/` en `1 [Nom de la phase]/`
2. Renomme `1 Intention.md` si besoin (garder le préfixe `1`)
3. Remplis `1 Intention.md` (template `Cerveaux/Cerveau Privé/4 TOOLS/Templates/Phase de vie.md`) :
   - Période estimée
   - Intention principale
   - Journée idéale pendant cette période
   - Objectifs de la phase
   - Stratégies quand surchargé / dispersé / fatigué / dans le flow
4. Mets à jour `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/Life Phases.md` (remplacer « Phase initiale » par le vrai nom, mettre à jour le lien vers l'intention)

### 12.7 : Configs Obsidian

**`.obsidian/daily-notes.json`** :
```json
{
  "folder": "2 CASQUETTES/Sur ma vie/Life Phases/1 [Nom de la phase]",
  "template": "4 TOOLS/Templates/Daily Note",
  "autorun": false
}
```

**`.obsidian/plugins/calendar/data.json`** :
```json
{
  "shouldConfirmBeforeCreate": true,
  "weekStart": "locale",
  "wordsPerDot": 250,
  "showWeeklyNote": true,
  "weeklyNoteFormat": "",
  "weeklyNoteTemplate": "4 TOOLS/Templates/Weekly Note",
  "weeklyNoteFolder": "2 CASQUETTES/Sur ma vie/Life Phases/1 [Nom de la phase]",
  "localeOverride": "system-default"
}
```

### 12.8 : Daily note du jour (log d'initialisation)

Crée `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/1 [Nom]/[YYYY-MM-DD].md` à partir du template `Cerveaux/Cerveau Privé/4 TOOLS/Templates/Daily Note.md`, puis ajoute un log initial en fin de fichier :

```markdown
---

## Logs IA / Session [HH:MM]

**Accompli :**
- Vault initialisé via `/initialisation`
- Création de `Moi.md`, `Mon Parcours.md`, casquettes, projets, phase « [Nom] »
- Nom de l'IA enregistré dans `AGENTS.md` : « [Nom IA] »

**Extractions :**
- Préférences : prénom « [Prénom] », nom IA « [Nom IA] », style de communication défini
- Faits : [X] casquettes, [Y] projets actifs, phase « [Nom] » démarrée
- Fichiers déposés et intégrés : [liste si applicable]

**Prochaines étapes :**
- [ ] Explorer le vault, tester `/welcome`
- [ ] Compléter `Mon Parcours.md` avec les docs restants
- [ ] Mapper tes process via `/map-process` et en documenter un avec `/create-skill`
```

---

## Étape 13 : Confirmation & next steps

```
Initialisation terminée !

Créé dans ton vault :
- AGENTS.md (racine WORKSPACE)                   -> nom de l'IA : [Nom] + prénom
- Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Moi.md                 -> qui tu es, style IA, valeurs
- Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Mon Parcours.md        -> historique chronologique
- [X] casquettes dans Cerveaux/Cerveau Privé/2 CASQUETTES/
- [Y] projets dans Cerveaux/Cerveau Privé/1 PROJETS/
- Phase « 1 [Nom] » avec son intention
- Daily note du jour avec le log d'initialisation

Configs Obsidian :
- Daily notes  -> Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/1 [Nom]/
- Weekly notes -> Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/1 [Nom]/

Redémarre Obsidian pour activer les configs de daily/weekly notes.

Tes cerveaux (ceux qui sont présents) :
- Cerveau Privé       -> rempli, c'est là qu'on a tout écrit aujourd'hui
- [chaque cerveau partagé présent, sous son nom retenu] -> [prêt / à brancher sur ton espace partagé]

La suite :
- `/inbox-processor` quand tu auras capturé des trucs en vrac
- `/partager` quand une note d'ici doit remonter vers ton équipe ou ton cercle
- `/daily-review` en fin de journée
```

Si les cerveaux partagés n'ont pas été branchés à l'Étape 2 bis, rappelle-le ici, en une ligne, sans insister : ça se fait quand il veut, la mécanique tourne sans.

---

## Règles

- **Écrire au fur et à mesure** : chaque artefact self-contained est écrit à la fin de son étape, depuis la décharge fraîche (voir « Principe transversal »). Ne tiens pas toute la décharge en mémoire jusqu'à la fin.
- **Demander une validation rapide** après avoir écrit chaque artefact et avant de passer à l'étape suivante (en plus de la validation finale de l'Étape 11).
- **Toujours demander validation** avant de créer des fichiers (Étape 11)
- **Reformuler** après chaque réponse pour valider la compréhension
- **Rappeler l'affordance fichier** à chaque grande section (Étapes 3-7)
- **Lire intégralement** tout fichier déposé avant d'en extraire l'info
- **Ne jamais inventer** : si une info manque et n'a pas été donnée, demande
- **Respecter le style** capturé à l'Étape 8 dès qu'il est connu (tutoiement, ton, pushback)
- **Le relecteur (Étape 12) est un check de cohérence**, pas une passe de réécriture : il relit ce qui a été écrit, corrige les mismatches, puis génère les artefacts transversaux (daily note d'init, configs Obsidian).

## Ce que tu ne fais PAS

- Tenir toute la décharge en mémoire et tout écrire à la fin : écris chaque artefact à la fin de son étape
- Sauter le prélude pédagogique (Étape 1) : l'utilisateur doit comprendre ce qu'il fait
- Créer les fichiers sans validation finale
- Mettre le nom de l'IA dans `Moi.md` (il va dans `AGENTS.md`)
- Traiter la casquette « Business » comme une section de `Moi.md` (elle mérite son propre dossier dans `Cerveaux/Cerveau Privé/2 CASQUETTES/[Nom du business]/`)
- Hardcoder les chemins Life Phases : c'est toujours `Cerveaux/Cerveau Privé/2 CASQUETTES/Sur ma vie/Life Phases/`
- Oublier de mettre à jour les configs Obsidian (Étape 12.7)
- **Écrire quoi que ce soit dans un cerveau partagé pendant l'initialisation.** Toute la décharge va dans le `Cerveau Privé`, sans exception. Les cerveaux partagés se remplissent après, note par note, via `/partager`. Une décharge est brute par nature : elle contient des jugements, des chiffres et des doutes qui n'ont rien à faire devant une équipe.
