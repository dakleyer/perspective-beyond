# Preserving the Atlas

The graph is the shared substrate. A page map, a tag weighting or a reading budget is a view of that substrate. Editing the view must preserve its cards, concepts, relationships, full source texts and provenance.

The historical comparison dated 4 November 2026 inspects six graph editions, eleven catalogue editions and five editions of the original corpus data. It finds no missing stable IDs, no missing relationships, no dangling endpoints and no deleted Atlas data files. The 298 published dialogue bodies are present in their individual text entries. All 1,359 source payload files remain byte-identical; ten generated assistant reading bundles have been regenerated as the product evolved.

Earlier editorial releases changed reading summaries, opening questions, twenty concept definitions and some tag classifications. The audit records these separately from source text. Full dialogue texts remain intact, and the earlier editorial wording remains addressable through its Git commit. The recent website integration leaves all four protected data files unchanged.

## Release check

Run with exact existing Git commits:

```sh
python3 scripts/atlas_preservation.py --base BASE_SHA --head HEAD_SHA
PYTHONPATH=scripts python3 -m unittest discover -s tests -p test_atlas_preservation.py
```

The release check detects removed IDs, truncated or replaced text, missing provenance, removed tags, changed relationship direction, duplicate IDs, dangling endpoints and deleted Atlas files. Tag proportions and calculated reading costs may change independently. An append to a source passage retains the earlier passage; a separate annotation retains the original record.

The GitHub workflow runs the check on changes to the Atlas and its tests. It reads existing Git objects and emits a report; it creates no backup payload. A detected difference requires an explicit editorial resolution in source control rather than an unnoticed replacement.

Machine-readable historical results are in `historical-preservation-20261104.json`.
