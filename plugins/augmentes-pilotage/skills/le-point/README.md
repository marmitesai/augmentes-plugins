# Le Point

Une recette pour votre assistant. Elle transforme quinze jours de boîte mail en deux choses utiles : des notes rangées dans votre coffre, et un rapport où vous tranchez ce qui attend une décision.

## Ce qu'elle fait

Elle lit vos mails **reçus et envoyés** sur la période, écarte le bruit, et croise les deux. Ce croisement est le cœur : sans lui, un fil auquel vous avez répondu depuis un autre mail ressort comme un silence de votre part. Vous vous retrouvez à relancer quelqu'un que vous avez déjà relancé.

Ensuite elle range ce qui mérite mémoire dans votre coffre, et vous rend un rapport HTML : les décisions qui attendent, les échéances à ne pas rater, les gens qui attendent une réponse.

## Installation

1. Dézippez ce dossier dans `~/.claude/skills/` :

```
~/.claude/skills/le-point/
```

2. Copiez la configuration et remplissez-la :

```bash
cd ~/.claude/skills/le-point
cp config.example.json config.json
```

Ouvrez `config.json` et renseignez votre adresse, votre domaine, et surtout **vos domaines proches** : vos clients, votre expert-comptable, votre avocat, vos partenaires. Ce sont les gens dont un mail compte toujours, même envoyé depuis un `contact@`.

3. Vérifiez que votre messagerie est branchée dans les connecteurs (Microsoft 365 ou Gmail).

C'est tout. Rien à installer d'autre : les scripts n'utilisent que ce que Python fournit d'origine.

## Utilisation

Dans votre assistant :

```
/le-point
```

ou simplement « fais le point sur ma boîte », « qu'est-ce que j'ai raté cette semaine », « qui attend une réponse de moi ».

La période par défaut est de quinze jours. Vous pouvez demander autre chose : « fais le point sur les 30 derniers jours ».

## Le rapport

Il s'ouvre dans votre navigateur. Chaque élément porte une case à cocher, et les décisions proposent des options cliquables.

**Corrigez-le.** Survolez une carte, cliquez le `+` qui apparaît, écrivez ce qui est faux. Le bouton **Corriger** en bas à droite exporte vos remarques et vos choix d'un seul coup : recollez-les dans la conversation, et la passe suivante corrige vos notes.

C'est le point important. Une IA qui lit votre boîte se trompera, sur un nom, sur une date, sur une intention. La question n'est pas de l'éviter mais de pouvoir la reprendre en trois secondes.

Vos cases cochées et vos commentaires restent dans votre navigateur, sur votre machine.

## Vos données

Les scripts de cette recette ne font **aucun appel réseau**. Ils lisent des fichiers, écrivent des fichiers, rien d'autre. Vos mails récoltés restent dans votre coffre. Le rapport HTML est autonome : il s'ouvre hors ligne et ne charge rien depuis Internet.

La lecture de votre messagerie passe par le connecteur que vous avez vous-même autorisé.

## Réglages utiles

Dans `config.json` :

- **`domaines_proches`** : le réglage qui compte le plus. Trop court, vous ratez des mails ; trop long, vous laissez rentrer du bruit. Complétez-le au fil des passes.
- **`sujets_automatiques`** : les débuts de sujet de vos propres automatismes (tickets, confirmations de commande, acceptations de réunion). Ils partent souvent de vraies adresses d'équipe, donc seul le sujet permet de les écarter.
- **`seuil_jours`** : à partir de combien de jours un fil sans réponse est signalé. Deux par défaut.

## Si quelque chose cloche

**Des mails importants sont classés en bruit** : ajoutez leur domaine dans `domaines_proches`.

**Trop de bruit passe** : regardez qui, et ajoutez le motif dans `sujets_automatiques` si c'est un automatisme, ou signalez-le, la liste universelle peut être complétée.

**On vous dit « sans réponse » alors que vous avez répondu** : c'est que le lien entre le mail reçu et votre réponse n'a pas été fait. Signalez-le, avec le nom de la personne.

---

Le Point, une recette M:armites.ai
