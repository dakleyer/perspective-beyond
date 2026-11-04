# Positioning · reading tests

4 November 2026.

## Comparison of reading paths and final round

The [blind comparison of six questions](comparacion/README.md) gave positioning three preferences and three ties in the last independent evaluation. Literal extracts from public sources were incorporated into 154 cards, together with a base of concepts directly supported by the document before expanding through the visitor's tags. The final version also retains a documented-use reading when one exists. Another new reader repeated the two affected questions and maintained the tie and the preference for positioning.

The final version passes 36 functional tests and 48 exact token checks. The protocol and card records allow the next reading to be chosen using the percentages and costs of neighbouring cards. Seven calculated configurations also deliver the context and complete accounting to readers who use only the web. Each package's selection matches the engine's selection, and closed packages retain only their own cluster. The original article texts and conceptual relationships retain their content.

A public test from a configured URL, without running code, recovered the closed selection of five Tegrity.AI pieces and the complete accounting of 1,755/2,400 tokens. It retained the 70:30 weights, consultant role and response instruction. The subsequent conversation distinguished avoidable compensatory work from necessary supervision. The [comparison record](comparacion/README.md) describes that test.

## What was checked

Positioning opens a source document. Its cards have a percentage composition of tags; the visitor supplies another combination that guides the reading path. The token budget includes complete pieces and their incoming relationships. Increasing it preserves the previous reading prefix.

The checks covered 1,209 documents, 1,291 cards and 272 concepts. Every card retains a source document and all compositions add up to 100%. The biographical document contains several cards, which can also be selected as specific entry points. Landing pages link their readings through navigation observed in the body of the websites.

The 30 functional tests cover document resolution, percentages, affinity, budget growth, connection continuity, filters, Closed and Porous scopes, normalised weights, absence of duplicates, compatibility with previous entries, and preservation of the role and instructions in the URL. The 48 test readings were encoded again with `tiktoken 0.12.0`, `o200k_base`: the resulting count matched the declared count and remained within each budget.

[Functional results](pruebas-funciones.json) · [Token check](pruebas-tokens.json) · [Reproducible tests](pruebas.mjs).

To repeat the tests, from the repository root:

```sh
node docs/atlas/posicionamiento/pruebas.mjs
```

## Two readers without project history

One reader received only the public URLs, protocol and published modules. It independently ran the same positioning, D-285, with 50:50 business and mathematics weights. At 2,000 tokens it obtained 1,721 reading tokens and four selected pieces. At 4,000 it obtained 3,790 and ten pieces. The first four retained their order; the maximum number of traversed connections remained three. The increase also expanded lateral reading. The entry document is displayed as an additional node.

The reader recovered the composition of 35% business, 25% transformation, 20% representation, 10% mathematics, 5% learning and 5% evidence. It calculated the affinity with the selected combination: `0.5 × 0.35 + 0.5 × 0.10 = 0.225`. It explained the relationship between context translation, observation limits and representation using the public texts of D-285, D-216 and D-265.

The second reader used only web tools and the public 2,000-token JubAp.eu package. It recognised the landing page as the entry document, its card and the connected readings from Field Notes, the framework and Reframing Value Creation. The package included 1,969 tokens, left 31 and stopped before a next block of 124. It interpreted the 45% business share as the card's thematic composition. It explained the mechanism through an example of exceptions between departments and consulted the cited public sources.

## Publication

The model, calculation, percentages and entry documents are in this repository. There are 33 prepared readings: eleven initial positionings with budgets of 1,000, 2,000 and 4,000 tokens. The browser allows other documents, tags and budgets to be combined and the result to be downloaded.

Previous source records, article texts and conceptual relationships retained their content. Landing-page navigation is recorded separately. The canonical catalogue `docs/data/atlas.json` retains SHA-256 `5e37a308dc5d57011d4884dc95dcc7b26223f1c383ad9c3a8bf2367e15a7fb49`.
