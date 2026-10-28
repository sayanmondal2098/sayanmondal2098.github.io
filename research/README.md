# Research content

This folder is the single place for the site's publication archive, research
project pages, and BibTeX records.

## Structure

| File | Purpose |
| --- | --- |
| `index.html` | Complete publication archive and citation actions |
| `cyberhull.html` | CyberHull geometric URL detection research page |
| `astria.html` | ASTriA semi-supervised tri-learning research page |
| `carbon-loss.html` | Little Andaman carbon-loss estimation research page |
| `sinmuli.html` | SiNMULI research project page |
| `cairn.html` | CAIRN research project page |
| `entrourl.html` | EntroURL-Bench research project page |
| `railway.html` | GPS-based automated railway crossing paper |
| `dimensionality.html` | Text dimensionality-reduction technical report |
| `streetlight.html` | Adaptive street-lighting preprint |
| `citations/` | Downloadable BibTeX records for every publication |
| `SOURCES.md` | Source records, verification date, and counting conventions |

Shared presentation and behavior remain in `../css/` and `../js/` so the
research pages stay consistent with the rest of the portfolio.

## Add or update research

1. Add or edit the project page in this folder.
2. Add its BibTeX file to `citations/`.
3. Put the BibTeX download and copy button in the same `.profile-actions` or
   `.citation-actions` container. `../js/citations.js` reads the download link;
   there is no separate JavaScript registry to maintain.
4. Add or update the publication card in `index.html`.
5. Update the homepage, project archive, résumé, and summary counts when the
   publication changes what those pages should feature.

Research content and canonical URLs live in this folder.

Every archived work has a stable anchor in `index.html`, a dedicated research
page, and a BibTeX record. Keep the archive index and the “Explore the research”
links on each page complete when adding work. Pages are static HTML, so these
links work without JavaScript.

Run `python scripts/check_site.py` from the repository root to check internal
links and fragments, structured metadata, and research/citation coverage.
Run `node scripts/check_citations.cjs` to check clipboard success, fallback,
failure feedback, and button recovery.
