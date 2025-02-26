# Digital Obsidian Garden

This is the template to be used together with the [Digital Garden Obsidian Plugin](https://github.com/oleeskild/Obsidian-Digital-Garden).
See the README in the plugin repo for information on how to set it up.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/oleeskild/digitalgarden)

---

## Docs

Docs are available at [dg-docs.ole.dev](https://dg-docs.ole.dev/)

# Sugar-Docs Sync

The Python sync script (`backend/sync.py`) synchronizes content from the official [Sugar Labs documentation repository](https://github.com/sugarlabs/sugar-docs) to this Digital Garden. This helps maintain consistency between the main documentation and this web interface.

## What the sync script does:

1. Clones the official sugar-docs repository to a temporary directory
2. Processes all Markdown files:
   - Converts file names to web-friendly format (lowercase, hyphenated)
   - Adds Digital Garden frontmatter (YAML metadata)
   - Fixes internal markdown links to match our web format
   - Preserves external links
3. Copies processed files to `src/site/notes/src/`
4. Copies images to the appropriate directory
5. Cleans up temporary files

## Usage:

```bash
pip install python-frontmatter
```

```bash
python backend/sync.py
```

After syncing, you can review and commit the changes to this repository.
