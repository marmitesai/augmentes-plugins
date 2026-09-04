# Le format du brouillon d'ontologie

Le skill écrit un `ontologie.json` de travail dans `Atelier/ontologie/`, puis `scripts/rendre.py` le valide et émet `ontologie.yaml` (la source de vérité du modèle, dans un format ouvert et réimportable) et `Ontologie.md` (la version lisible) dans `Cerveaux/Cerveau Privé/4 TOOLS/ontologie/`. Le JSON et le YAML portent la même structure ; seul `rendre.py` écrit le YAML.

## Énumérations

| Champ | Valeurs | Sens |
|---|---|---|
| `ontologie.statut` | `draft-IA`, `approved` | sortie du skill, puis après validation par l'utilisateur |
| `etat` (types et verbes) | `retenu`, `par_reference`, `flou`, `absent` | trois exemples au moins ; vérité dans un logiciel externe avec son identifiant ; moins de trois exemples structurés ; type attendu sans aucun exemple |
| `provenance` | commence par `lu`, `dit` ou `deduit` | `lu (auto)` pour une fiche générée par un import |
| `questions[].verdict` | `passe`, `partiel`, `par_reference`, `trou`, `a_jouer` | une question `passe`, `partiel` ou `par_reference` porte une `preuve` |

## Règles que `rendre.py` refuse

- plafond dépassé (`ontologie.plafond`, 20 et 20 par défaut) ;
- noyau incomplet : les six types `personne, role, equipe, activite, process, outil` et les cinq verbes `occupe, repond_de, sert, tourne_sur, precede` sont toujours déclarés, à l'état `absent` s'il le faut ;
- une combinaison dont la source ou la cible n'est pas un type déclaré, ou un verbe sans combinaison ;
- un type `retenu` avec moins de trois `exemples` portant `nom` et `source`, un verbe `retenu` avec moins de trois `exemples` portant `note` ;
- une valeur hors énumération, une provenance qui ne commence pas par `lu`, `dit` ou `deduit` ;
- un `sert` qui cite une question absente de `questions` ;
- un `chemin` de question qui cite un type ou un verbe non déclaré.

Quand une règle est violée, rien n'est écrit et chaque refus nomme la règle. Corriger le JSON, relancer. Ne jamais corriger le script pour faire passer un brouillon.

## Le chemin typé d'une question

Le chemin se lit comme au tableau. Chaque étape qui prétend nommer un type ou un verbe est contrôlée ; les annotations ne le sont pas.

| Écriture | Sens | Contrôlé |
|---|---|---|
| `organisation` | un type | oui |
| `a_signe` | un verbe | oui |
| `occupe (dates)` | un verbe et ce qu'il porte | oui, sur `occupe` |
| `repond_de⁻¹ (A)` | le verbe en sens inverse, avec son rôle | oui, sur `repond_de` |
| `¬ repond_de⁻¹ (R)` | l'absence de cette relation | oui, sur `repond_de` |
| `contrat \| machine` | une alternative | oui, sur les deux |
| `champ tutoiement` | un champ, pas une relation | non |
| `⚠ manque: suit` | une étape que le vocabulaire n'a pas encore | non |

Une question dont le chemin porte un `⚠ manque:` ne peut pas valoir `passe` : c'est au mieux `partiel`.

## Structure

L'exemple ci-dessous est fictif, avec une entreprise imaginaire. Les chemins de notes suivent la structure du second cerveau.

```json
{
  "ontologie": {
    "organisation": "atelier-durand",
    "version": "0.1.0",
    "date": "2026-09-04",
    "statut": "draft-IA",
    "cerveaux": ["Cerveau Privé", "Cerveau Entreprise"],
    "plafond": {"types": 20, "verbes": 20}
  },
  "types": [
    {
      "cle": "organisation",
      "libelle": "Organisation",
      "noyau": false,
      "porte_maturite": false,
      "etat": "retenu",
      "definition": "Une société, quelle que soit sa relation à l'entreprise",
      "champs": ["identifiant_facturation", "siren", "secteur"],
      "cerveau": "Cerveau Entreprise",
      "cerveaux_autres": ["Cerveau Privé"],
      "instances": 42,
      "identifiant_externe": {"identifiant_facturation": 31},
      "verite": "le logiciel de facturation",
      "exemples": [
        {"nom": "Société Alpha", "source": "Cerveau Entreprise/2 CASQUETTES/Commerce/clients/Societe Alpha.md"},
        {"nom": "Société Beta", "source": "Cerveau Entreprise/2 CASQUETTES/Commerce/clients/Societe Beta.md"},
        {"nom": "Holding Gamma", "source": "Cerveau Privé/6 GARDEN/Notes/entities/Holding Gamma.md"}
      ],
      "provenance": "lu (auto)",
      "sert": [1, 2, 10],
      "note": "absorbe les sept façons d'écrire « société » trouvées dans les frontmatters",
      "homonymes": [],
      "decision": ""
    }
  ],
  "verbes": [
    {
      "cle": "est_client_de",
      "libelle": "est client de",
      "porte_role": true,
      "porte_dates": true,
      "sens_unique": true,
      "etat": "retenu",
      "roles": [{"role": "actif", "exclusif": false}, {"role": "prospect", "exclusif": false}],
      "combinaisons": [{"source": "organisation", "cible": "organisation"}],
      "champs": [],
      "exemples": [
        {"source": "Société Alpha", "cible": "Atelier Durand", "role": "actif", "note": "Cerveau Entreprise/2 CASQUETTES/Commerce/clients/Societe Alpha.md"}
      ],
      "provenance": "lu (auto)",
      "sert": [1, 2, 10],
      "note": "",
      "a_trancher": "Client : un type à part, ou un rôle porté par ce verbe ? Décision du dirigeant."
    }
  ],
  "questions": [
    {"id": 10, "question": "Quelle offre s'applique à quel client, depuis quel devis ?", "chemin": ["organisation", "a_signe", "contrat", "instancie", "offre"], "verdict": "passe", "preuve": "Société Alpha → devis D-2026-014 → forfait annuel", "manque": ""}
  ],
  "trous": [{"type": "machine", "motif": "aucune note par machine", "verite": "le logiciel de gestion de parc, dont aucun identifiant n'apparaît dans les notes"}],
  "contradictions": [{"sujet": "Un collaborateur", "a": "promesse d'embauche dans sa fiche", "b": "en poste dans l'organigramme", "notes": ["...", "..."]}],
  "candidats_refuses": [{"candidat": "prospect", "motif": "statut du verbe est_client_de, pas un type"}],
  "decisions": [{"date": "2026-09-04", "par": "le dirigeant", "sujet": "Client", "decision": "rôle porté par est_client_de"}],
  "a_trancher_au_tableau": ["Le mot « site » désigne un lieu et un compte de facturation : lequel garde-t-on ?"]
}
```

Les champs `note`, `homonymes`, `decision`, `a_trancher`, `champs`, `cerveaux_autres`, `identifiant_externe`, `verite`, `manque` sont facultatifs. Les `trous` acceptent `type`, `verbe`, `champ` ou `question` comme sujet.

## Pourquoi ce format

Le YAML émis est un fichier texte, lisible sans outil, versionnable dans un dépôt et réimportable ailleurs. C'est délibéré : une carte du métier enfermée dans un logiciel propriétaire ne vous appartient plus. Trois questions valent d'être posées à quiconque vous vend une ontologie : dans quel format est-elle stockée et puis-je l'exporter, combien coûte l'année deux, et qui la met à jour quand mon métier change.

La partie modèle (types, verbes, rôles, combinaisons, champs) est ce qui s'importe dans un outil de graphe. Le reste, les exemples, la provenance, les questions, les trous et les contradictions, est la preuve : elle accompagne le modèle et se relit, elle ne s'importe pas.
