#!/bin/bash

# scrub-check.sh : garde anti-fuite des recettes livrées par learn (reprise de skills-clients)
# Détecte les références Marmites internes dans un dossier skill
# Exclusions: .distilled-from/, tests/, .git/
# Exceptions tolérées : la signature publique, « Marmites.ai » et « M:armites.ai »
#
# Note sur 'metadata': la liste brute incluait "metadata" comme terme interdit
# (police Metadata). Pour éviter faux positifs sur <meta> HTML, on utilise un
# pattern étroit: font.*metadata|metadata.*\.otf|Metadata.*Bold|metadata\.ttf

if [[ $# -lt 1 ]]; then
    echo "Usage: bash scrub-check.sh <dossier-skill>"
    exit 1
fi

SKILL_DIR="$1"
if [[ ! -d "$SKILL_DIR" ]]; then
    echo "Erreur: le répertoire '$SKILL_DIR' n'existe pas"
    exit 1
fi

# Patterns interdits avec word boundaries \b pour mots courts
# Inclusion des variantes accentuées (grep -i ne les normalise pas)
# Patterns: noms perso, équipe, domaines, outils, concepts, clients, chemins, marques
BANNED_PATTERN='(\bcedric\b|\blaurent\b|\bcédric\b|\btheo\b|\bthéo\b|\bsami\b|\bosman\b|\bmateo\b|\bcindy\b|\bclaire\b|\bcorentin\b|\bdylan\b|\bmarmites\b|\barmites\b|@marmites\.com|\bcockpit\b|\bodoo\b|\bstakeholder\b|\bdexter\b|cerveau privé|cerveau marmites|cerveau codir|\bgest\b|\bruault\b|\bmarcaillou\b|\bxefi\b|\bnegra\b|\bbatyr\b|\bneve\b|\bguerra\b|d-?bosstech|\bdcnettoyage\b|dc nettoyage|/Users/cedriclaurent|Dropbox-Marmites|\baugmentés\b|\baugmentes\b|le prompt|font.*metadata|metadata.*\.otf|Metadata.*Bold|metadata\.ttf)'

# Lancer la recherche (récursive, case-insensitive, regex étendues)
# CRUCIAL: -print0 / xargs -0 pour gérer les chemins avec espaces
# -H force le format fichier:ligne même pour les single-file batches (évite regex fail)
HITS=$(find "$SKILL_DIR" -type f \
    -not -path "*/.distilled-from/*" \
    -not -path "*/tests/*" \
    -not -path "*/.git/*" \
    -print0 | xargs -0 grep -H -inE "$BANNED_PATTERN" 2>/dev/null || true)

# Compter les fichiers réellement scannés
FILES_SCANNED=$(find "$SKILL_DIR" -type f \
    -not -path "*/.distilled-from/*" \
    -not -path "*/tests/*" \
    -not -path "*/.git/*" | wc -l)

if [[ -z "$HITS" ]]; then
    echo "✓ Kit clean: $FILES_SCANNED fichiers scannés, aucune référence Marmites détectée"
    exit 0
fi

# Filtrer les résultats
REAL_HITS=""
BINARY_HITS=""

while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    
    # Détecter les fichiers binaires ("Binary file X matches")
    if [[ "$line" =~ ^Binary\ file\ .+\ matches$ ]]; then
        BINARY_HITS+="$line"$'\n'
        continue
    fi
    
    # Parser les hits texte (format: fichier:numéro:contenu)
    if [[ "$line" =~ ^([^:]+):([0-9]+):(.*)$ ]]; then
        file="${BASH_REMATCH[1]}"
        line_num="${BASH_REMATCH[2]}"
        line_content="${BASH_REMATCH[3]}"
        
        # Masquer Marmites.ai (exception tolérée) et re-tester
        masked=$(echo "$line_content" | sed -E 's/M:?armites\.ai/<MASKED>/gi')
        
        if echo "$masked" | grep -qiE "$BANNED_PATTERN"; then
            # C'est un vrai hit (pas juste Marmites.ai)
            REAL_HITS+="$file:$line_num: $line_content"$'\n'
        fi
    fi
done <<< "$HITS"

# Synthèse
if [[ -z "$REAL_HITS" && -z "$BINARY_HITS" ]]; then
    echo "✓ Kit clean: $FILES_SCANNED fichiers scannés, aucune référence Marmites détectée"
    exit 0
fi

# Afficher les fuites
echo "✗ Fuites détectées ($FILES_SCANNED fichiers scannés):"
if [[ -n "$REAL_HITS" ]]; then
    echo "$REAL_HITS"
fi
if [[ -n "$BINARY_HITS" ]]; then
    echo "Fichiers binaires contenant un terme interdit:"
    echo "$BINARY_HITS"
fi
exit 1
