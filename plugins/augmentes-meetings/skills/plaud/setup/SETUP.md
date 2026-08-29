# Installation du kit Plaud

Cette procédure installe tout ce qu'il faut pour que `/plaud` fonctionne : le pont technique vers Plaud (`plaud-toolkit`), la connexion au compte du client, et sa configuration. Elle se déroule à deux, toi (l'assistant) et le client, devant le même terminal.

Suis les 7 étapes dans l'ordre. Chacune a sa commande, ce que tu dois voir si ça marche, et ce qu'il faut faire si ça ne marche pas. Ne saute pas une étape en échec : la suivante en dépend presque toujours.

`plaud-toolkit` est un outil communautaire encore jeune (statut alpha). Une erreur inattendue n'est pas forcément un vrai problème : relance la commande une fois avant de creuser plus loin.

## 1. Node.js

```bash
node --version
```

Attendu : une version 18 ou plus (`v18.x.x`, `v20.x.x`, `v22.x.x`...).

Si la commande est introuvable, ou si la version affichée est inférieure à 18 : arrête-toi là. Renvoie le client vers nodejs.org, fais-lui installer la version LTS, puis reprends cette étape depuis le début. Tout le reste du kit dépend de Node.

## 2. plaud-toolkit

```bash
mkdir -p ~/Tools
git clone https://github.com/sergivalverde/plaud-toolkit.git ~/Tools/plaud-toolkit
cd ~/Tools/plaud-toolkit
npm install
```

Attendu : `npm install` se termine sans ligne rouge. Des avertissements (`npm warn`) sont normaux, ce n'est pas un échec.

Si `~/Tools/plaud-toolkit` existe déjà (installation précédente) : ne clone pas par-dessus, fais plutôt `cd ~/Tools/plaud-toolkit && git pull && npm install`.

Si `npm install` échoue avec une erreur liée à la version de Node : retourne à l'étape 1. Si l'erreur vient du réseau ou d'une permission, relance la commande ; si ça persiste, note le message d'erreur exact et arrête-toi là, ce n'est pas à deviner.

## 3. Connexion au compte Plaud

```bash
cd ~/Tools/plaud-toolkit
npx tsx packages/cli/bin/plaud.ts login
```

La commande demande un email, un mot de passe, et une région. Pour un client européen, réponds `eu` à la région.

Attention : si le client s'est toujours connecté à Plaud avec « Se connecter avec Google », il n'a pas de mot de passe classique et le login CLI échouera. Envoie-le sur web.plaud.ai, fais-lui cliquer sur « Forgot Password », fais-lui définir un mot de passe, puis relance la commande de login avec ce mot de passe.

Vérification :

```bash
npx tsx packages/cli/bin/plaud.ts list
```

Attendu : une liste d'enregistrements (titre, date). Une liste vide n'est pas un échec si le compte n'a encore aucun enregistrement.

Si le login est refusé : vérifie l'email et le mot de passe avec le client, et vérifie que la région choisie correspond bien à son compte. Une mauvaise région peut faire échouer l'authentification.

## 4. Serveur MCP

```bash
claude mcp add plaud -s user -- npx tsx ~/Tools/plaud-toolkit/packages/mcp/src/index.ts
```

Le `-s user` inscrit le serveur au niveau utilisateur : il sera disponible dans tous les projets Claude, pas seulement celui-ci.

Vérification :

```bash
claude mcp list
```

Attendu : une ligne `plaud` avec un statut connecté.

Si le statut affiche une erreur ou une déconnexion : vérifie que `~/Tools/plaud-toolkit` existe bien (étape 2), fais `claude mcp remove plaud` puis relance la commande d'ajout. Si ça persiste, ouvre une nouvelle session Claude Code : l'enregistrement d'un serveur MCP demande parfois un redémarrage pour être pris en compte.

## 5. Configuration

Depuis le dossier de la recette (celui qui contient `config.example.json`, `SETUP.md` et `correction-template.html`) :

```bash
cp config.example.json config.json
```

Remplis `config.json` **avec le client**, champ par champ : son adresse Plaud, les personnes qui participent souvent à ses réunions (nom et email, jamais devinés), le chemin de son coffre s'il en a un, sa messagerie (`m365`, `gmail` ou `aucune`), et son identité visuelle (nom d'entreprise, logo, couleur) si elle est déjà arrêtée. Un champ que le client ne sait pas encore remplir reste vide, il se complète plus tard.

Vérification : `config.json` se lit comme du JSON valide, sans les valeurs d'exemple du modèle (`prenom@example.com`, `Mon Entreprise`) restées telles quelles là où le client avait une vraie réponse à donner.

Si le client hésite sur un champ (équipe pas encore définie, coffre pas encore choisi) : laisse-le vide plutôt que d'inventer, et signale-le avant de passer à l'étape 7.

## 6. Messagerie

Vérifie que le connecteur annoncé en `messagerie` dans `config.json` est bien branché dans Claude : Microsoft 365 ou Gmail selon la valeur choisie.

Si le connecteur n'est pas branché : soit tu le branches maintenant avec le client, dans les réglages des connecteurs Claude, soit tu repasses `messagerie` à `"aucune"` dans `config.json` et tu le dis clairement au client. Le kit s'arrêtera alors au compte-rendu en fichier, sans brouillon de mail, tant que le connecteur n'est pas ajouté.

Vérification : le connecteur choisi répond. Une recherche simple dans le calendrier ou la boîte suffit à le confirmer.

## 7. Test de bout en bout

Lance `/plaud` sur le dernier enregistrement du client. Déroule jusqu'à la page de correction, fais au moins une correction avec lui (un locuteur, un texte, une action), puis termine le passage.

Attendu : une note apparaît dans son coffre, et un brouillon de compte-rendu apparaît dans sa messagerie. Si `messagerie` vaut `aucune`, un fichier de compte-rendu HTML est écrit à côté de la note à la place, avec son chemin annoncé.

Si le pipeline s'arrête avant la page de correction : reviens aux étapes 3 et 4, le connecteur Plaud doit répondre. Si la page de correction ne s'ouvre pas dans le navigateur : vérifie le chemin annoncé et ouvre-le à la main. Si aucun brouillon n'apparaît après une correction validée : reviens à l'étape 6, le connecteur messagerie n'est probablement pas branché.

## Une fois les 7 étapes passées

Le kit est installé. Dis-le au client simplement : `/plaud` est prêt, ses prochains enregistrements Plaud passeront par la page de correction avant tout compte-rendu, et rien ne part jamais tout seul, il valide et il envoie.
