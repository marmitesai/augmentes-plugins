---
name: creer-son-ontologie
description: Use when the user says "crée mon ontologie", "l'ontologie de mon entreprise", "la carte de mon métier", "structure mon second cerveau pour l'IA", "mon cerveau se noie", "l'IA ne sait pas où ranger", "quels sont mes objets métier", or asks to derive a business ontology (types, verbs, relations) from their second brain. Also when an ontology already produced looks scattered, duplicated, or unrecognizable to its owner.
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "AskUserQuestion"]
---

# creer-son-ontologie

Un second cerveau finit par se noyer. Passé quelques centaines de notes, la recherche trouve des textes qui se ressemblent, jamais des faits reliés, et l'IA répond avec assurance à côté de la question.

**Une ontologie, c'est la carte des noms et des verbes d'un métier.** « Client a signé Contrat, Contrat couvre Site, Process traite Contrat, Personne occupe Rôle. » Rien de plus savant que ça : les objets dont l'entreprise parle tous les jours, et ce qu'ils se font entre eux. C'est ce qui dit à l'IA où ranger une information et à quoi la rattacher.

Ta mission ici : **fabriquer le brouillon et ses preuves. C'est l'utilisateur qui tranche.** Le statut de sortie est toujours `draft-IA`, et rien ne se dérive d'un brouillon.

## Ce que tu livres, dans cet ordre

Une exécution complète produit exactement ces quatre choses, et rien d'autre :

1. **Un inventaire chiffré** du second cerveau, écrit par un script, jamais à la main.
2. **Des questions de compétence numérotées**, validées par l'utilisateur avant qu'un seul type existe.
3. **Un `ontologie.json`** de travail : types, verbes, questions, trous, contradictions, décisions à trancher.
4. **`ontologie.yaml` et `Ontologie.md`**, émis par un script qui refuse un brouillon fautif.

Chaque type et chaque verbe retenu porte **trois exemples réels avec leur note source**. Chaque question porte un verdict et sa preuve. Ce qui manque est livré comme trou, pas comblé.

## Geste 1 : compter avant de lire

Un second cerveau porte déjà une structure sans le savoir : ses dossiers, ses champs de frontmatter, ses tags, ses liens. Compte-la d'abord.

```bash
WS="$(pwd)"                     # la racine du workspace, celle qui contient Cerveaux/
SKILL_DIR="<dossier de ce skill>"
mkdir -p "$WS/Atelier/ontologie"
python3 "$SKILL_DIR/scripts/inventaire.py" "$WS" --sortie "$WS/Atelier/ontologie"
```

Le script écrit `inventaire.json` et `inventaire.md` : notes par cerveau et par dossier, champs de frontmatter normalisés, valeurs de `type` et `subtype`, notes les plus liées, notes orphelines, liens morts après résolution des alias, doublons entre cerveaux, gisements (dossiers dont les notes répètent les mêmes colonnes, et notes qui portent de longues tables), identifiants venus d'un logiciel externe, et le **régime**.

Lis `inventaire.md` en entier. C'est ta carte pour la suite, et la preuve que tu as lu le réel plutôt que la documentation du vault.

Lis ensuite **les documents de cadrage** qu'il liste, les `AGENTS.md` et `CLAUDE.md` à la racine de chaque cerveau. Ils ne comptent pas comme notes, et sur un cerveau jeune ce sont pourtant les seuls fichiers qui portent du contenu : les règles de rangement, celles de confidentialité, le vocabulaire maison.

**Si le second cerveau est encore vide de métier** (aucun gisement, presque tout en gabarit, les dossiers de projets vides), dis-le avant d'aller plus loin :

> Votre cerveau est installé mais pas encore nourri. Je peux poser la carte de base, tous ses types marqués `absent` : c'est un diagnostic utile, il vous dit ce qu'il reste à remplir. La carte de votre métier, elle, demande de la matière. Voulez-vous le diagnostic maintenant, ou qu'on en reparle après quelques semaines d'usage ?

S'il veut le diagnostic, déroule les cinq gestes quand même : le noyau `absent`, les questions posées, les trous nommés. C'est un livrable honnête, et il devient la feuille de route du remplissage.

| Régime | Seuil | Ce qui change au geste 3 |
|---|---|---|
| `petit` | moins de 100 notes | tu lis toutes les notes ; l'essentiel du modèle vient de l'entretien |
| `gros` | 100 notes et plus | tu lis les notes les plus liées et 5 à 10 notes par gisement, jamais tout |

## Geste 2 : les questions d'abord

Une ontologie se spécifie par ce qu'elle doit rendre. Avant de poser un type, écris les questions que l'utilisateur pose à son entreprise et que son cerveau ne sait pas rendre sans risque de se tromper.

Quatre amorces, à croiser avec les gisements du geste 1 : qu'est-ce que mon entreprise fait ? qui en répond ? où en est-on ? qu'est-ce qui repose sur une seule personne ? Un gisement de fiches clients appelle une question sur les clients ; un dossier de décisions appelle une question sur les décisions.

Propose 10 à 20 questions **avec AskUserQuestion**, en lots thématiques, à cocher. Elles doivent être stratifiées : des simples (« qui occupe quel rôle ? ») et des composées qui traversent plusieurs verbes (« quel contrat couvre ce site, et quel process le traite ? »).

Pour chaque question retenue, dis tout de suite **où vit sa vérité** : dans le cerveau, ou dans un logiciel externe (facturation, gestion de parc, suivi du temps). Une question dont la vérité est ailleurs passera par référence si les notes portent l'identifiant, en trou sinon. L'utilisateur doit le savoir maintenant, pas le découvrir au verdict.

Demande aussi si les **règles de la maison** entrent dans la carte : ces principes qu'on répète en réunion et qui décident vraiment. Si oui, une question de plus et un type Règle. Sinon, ils restent dans les notes.

Numérote les questions. Elles seront rejouées au geste 4.

## Geste 3 : induire, sous noyau et sous plafond

**Le noyau est toujours présent**, même vide. Six types et cinq verbes qui décrivent le fonctionnement de n'importe quelle entreprise. Les clés s'écrivent sans accent : `personne`, `role`, `equipe`, `activite`, `process`, `outil` ; `occupe` (Personne → Rôle, avec ses dates), `repond_de` (Rôle → Activité ou Process, avec les rôles R, A, C, I et un seul A par cible), `sert` (Process → Activité), `tourne_sur` (Process → Outil), `precede` (Process → Process). Le libellé, lui, s'écrit en français accentué.

Un type du noyau sans exemple se déclare à l'état `absent` : c'est un diagnostic, pas un oubli. Il dit à l'utilisateur que son cerveau ne sait rien de cette part de son entreprise.

**Aucun verbe du noyau ne vise Équipe**, et c'est voulu : l'appartenance d'un rôle à une équipe est un champ du rôle, pas une relation. Si le cerveau relie explicitement des personnes ou des rôles à des équipes, propose un verbe pour le porter et fais-le valider.

**L'extension métier s'induit du cerveau**, jamais d'un catalogue tout fait. Les candidats viennent des `subtype` normalisés, des notes les plus liées, des gisements et des mots des questions. Chaque candidat passe cinq tests, dans cet ordre :

1. **Résolution des doublons.** Fusionne les variantes de casse et d'alias, corrige le bruit d'import (un véhicule ou une salle de réunion typés `person`). Trois libellés proches de la même chose font une entrée, pas trois. C'est le premier travers d'une carte bâclée.
2. **Résolution des homonymes.** Un même mot désigne parfois trois choses : « site » peut être un lieu, un compte de facturation, un site web. Liste les homonymes et fixe un sens par type.
3. **Type ou rôle.** Si le candidat est ce qu'une chose est *pour* une autre (client, fournisseur, prospect, décideur, payeur, filiale), c'est un rôle porté par un verbe, pas un type. Une société ne cesse pas d'exister quand elle cesse d'être cliente. Écris le verbe et **fais valider la décision** : un rôle qui structure toute l'entreprise se tranche par son dirigeant, pas par toi.
4. **Né d'une question.** Un candidat qui ne sert aucune question numérotée attend. Liste-le, ne le retiens pas. Un type qui n'existe que parce que le mot revient souvent est un type de trop.
5. **Exemples gradués.** Une note ou un champ structuré vaut exemple ; une simple mention en prose ne vaut que `flou`. Trois exemples au moins pour `retenu`, chacun avec sa note source. Un candidat dont les exemples sont des identifiants d'un logiciel externe, sans note propre, est `par_reference`, avec ce logiciel nommé.

**Les verbes se déclarent** avec leurs combinaisons (type source vers type cible), leurs capacités (rôles, dates, sens unique) et leurs trois exemples. Une relation lue hors combinaison se note comme candidate et se refuse : c'est ce qui empêche la carte de partir en toile d'araignée.

**Plafond : 20 types et 20 verbes**, noyau compris. Au-delà, fusionne. Une carte qui ne tient pas sur deux pages ne sera ni lue ni entretenue.

**Provenance sur chaque élément** : `lu` (une note écrite le dit), `lu (auto)` (une fiche générée par un import le dit, ce n'est pas la même chose), `dit` (l'utilisateur l'a dit en séance), `deduit` (tu l'infères). Ce qui n'est pas documenté n'est pas inventé : il est `absent` ou `flou`, et c'est justement ce que la carte doit montrer.

Écris le résultat dans `Atelier/ontologie/ontologie.json`. Le schéma complet, les énumérations et un exemple sont dans `$SKILL_DIR/reference/format-ontologie.md` : lis ce fichier avant d'écrire le JSON.

## Geste 4 : prouver sur de vraies notes

Rejoue chaque question. Fixe d'abord l'exemple à suivre parmi les notes les plus liées du geste 1 : elles seules portent un chemin entier, et varier les exemples double le coût pour rien.

Une note ne mérite ce statut qu'à partir d'une dizaine de liens entrants. Sur un cerveau jeune, les premières du classement sont des gabarits à un ou deux liens : en suivre une fabriquerait une preuve fausse. Dans ce cas il n'y a pas d'exemple à suivre, et le verdict est `trou`.

Pour chaque question, écris le chemin typé, un exemple réel qui le parcourt, la note source de chaque étape, et le verdict : `passe`, `partiel`, `par_reference` ou `trou`.

Le chemin ne cite que des types et des verbes déclarés, et le script d'émission le vérifie. Une étape qui manque encore s'écrit `⚠ manque: <nom>`, une étape qui est un champ s'écrit `champ <nom>`, et les annotations usuelles restent lisibles : `occupe (dates)`, `repond_de⁻¹ (A)` pour le sens inverse, `contrat | machine` pour une alternative.

Une question dont tu ne trouves aucun chemin est un `trou`. Ne le comble pas : c'est un résultat, il dit à l'utilisateur ce que son cerveau ne sait pas encore.

Quand deux notes se contredisent sur le chemin d'une preuve, écris-le dans `contradictions` au lieu de choisir. Une preuve qui tombe sur deux vérités a trouvé quelque chose.

## Geste 5 : émettre, puis passer la main

```bash
python3 "$SKILL_DIR/scripts/rendre.py" "$WS/Atelier/ontologie/ontologie.json" \
  --sortie "$WS/Cerveaux/Cerveau Privé/4 TOOLS/ontologie"
```

Le script valide avant d'écrire. Il refuse un plafond dépassé, un noyau incomplet, une relation vers un type non déclaré, un élément `retenu` avec moins de trois exemples, une valeur inconnue, une question qui cite un mot absent du vocabulaire. Quand il refuse, il nomme la règle et n'écrit rien : corrige le JSON, relance. Ne corrige jamais le script pour faire passer un brouillon.

Les deux fichiers naissent dans le **Cerveau Privé**. C'est l'invariant du second cerveau : on écrit en privé, on promeut ensuite. Un brouillon ne circule pas.

Rends la main en trois points : ce que la carte dit, ce qu'elle ne sait pas encore, ce qui reste à trancher. Cette dernière liste est l'ordre du jour de la prochaine séance de travail.

## Ce que tu ne décides jamais

Un type contre un rôle quand le rôle structure l'entreprise. Le sens à garder pour un homonyme. Si les règles de la maison entrent dans la carte. Si une question dont la vérité vit dans un logiciel externe mérite qu'on pose l'identifiant dans les notes. Tout cela va dans `a_trancher_au_tableau`, avec ton avis et sa raison.

## Ce qui reste dehors

Remplir la carte de toutes ses données : trois exemples suffisent à la preuve, le reste est un autre chantier. Recopier un logiciel externe : on référence son identifiant, on ne duplique pas ses données, sinon deux vérités divergent. La vie personnelle de l'utilisateur : cette carte est celle de son entreprise, dis-le lui. Et toute inférence : un trou reste un trou.
