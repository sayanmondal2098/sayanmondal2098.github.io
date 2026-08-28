# Research content

This folder is the single place for the site's publication archive, research
project pages, and BibTeX records.

## Structure

| File | Purpose |
| --- | --- |
| `index.html` | Complete publication archive and citation actions |
| `sinmuli.html` | SiNMULI research project page |
| `cairn.html` | CAIRN research project page |
| `entrourl.html` | EntroURL-Bench research project page |
| `citations/` | Downloadable BibTeX records for every publication |

Shared presentation and behavior remain in `../css/` and `../js/` so the
research pages stay consistent with the rest of the portfolio.

## Add or update research

1. Add or edit the project page in this folder.
2. Add its BibTeX file to `citations/`.
3. Add the citation key and relative file path to `../js/citations.js`.
4. Add or update the publication card in `index.html`.
5. Update the homepage, project archive, résumé, and summary counts when the
   publication changes what those pages should feature.

The old URLs under `../pages/` are compatibility redirects only. Research
content should be edited here.
