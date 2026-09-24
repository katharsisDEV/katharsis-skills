# Skills Claude — Katharsis Event

Marketplace privée de plugins Claude Code. Un plugin, `katharsis`, regroupe les skills
internes :

| Skill | Rôle |
|---|---|
| `slides-katharsis` | Créer toute présentation / tout dossier en slides à la charte Katharsis (thème, gabarit, contrôles, graphiques, bonnes pratiques de rédaction) |
| `reprise-presentation` | Reprendre une présentation client (PDF/PPTX) : compléter, vectoriser les schémas, vérifier les références matériel, version client / interne |

## Installer sur une machine

Prérequis : Claude Code, et un accès au dépôt privé (`gh auth login` ou clé SSH GitHub).

Dans Claude Code :

```
/plugin marketplace add gulrupa/katharsis-skills
/plugin install katharsis@katharsis
```

En ligne de commande, c'est équivalent :

```bash
claude plugin marketplace add gulrupa/katharsis-skills
claude plugin install katharsis@katharsis
```

Les skills apparaissent sous la forme `katharsis:slides-katharsis` et
`katharsis:reprise-presentation`, et se déclenchent automatiquement.

## Mettre à jour

Après un `git push` sur ce dépôt, sur chaque machine :

```
/plugin marketplace update katharsis
```

(ou activer la mise à jour automatique de la marketplace dans `/plugin` → Marketplaces).
**Penser à incrémenter `version`** dans `.claude-plugin/marketplace.json` et
`plugins/katharsis/.claude-plugin/plugin.json` : c'est ce qui signale la nouvelle version.

## Ajouter un skill

1. Créer `plugins/katharsis/skills/<nom-du-skill>/SKILL.md` (+ `references/`, `scripts/`, `assets/`).
2. `claude plugin validate .` puis incrémenter la version.
3. Commit, push, `/plugin marketplace update katharsis`.

Pour un ensemble de skills sans rapport avec la charte, créer un second plugin sous
`plugins/<autre>/` et l'ajouter à la liste `plugins` de `marketplace.json`.

## Autres modes d'installation

- **Développement / sans marketplace** : `./install.sh` crée des liens symboliques de
  chaque skill vers `~/.claude/skills/` ; toute modification du dépôt est prise en compte
  immédiatement. `./install.sh --remove` pour les retirer.
  Ne pas combiner avec le plugin sur la même machine (skills en double).
- **claude.ai (web / app)** : `./pack.sh` produit un `.zip` par skill dans `dist/`, à
  téléverser dans les paramètres Skills de claude.ai.
