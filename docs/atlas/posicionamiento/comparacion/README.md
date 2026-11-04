# Positioning and traversal: reading comparison

4 November 2026.

Positioning combines an entry document, its cards, each card's percentage composition, the visitor's chosen weights and a token budget. This test compared the explanation produced by its readings with that of the previous hop-based traversal.

## Result

In the last independent evaluation of six questions, positioning was preferred in three and tied in three. The reading path combines a base close to the document with expansion by thematic affinity. Connections retain their meaning and selected pieces remain when the budget is increased.

| Reading question | Previous traversal /20 | Positioning /20 | Evaluator's preference |
| --- | ---: | ---: | --- |
| What the architect contributes between trades and mathematical formulation | 18 | 20 | Positioning |
| Human contribution, compensatory work and improvement decisions | 20 | 20 | Tie |
| Signal, authorisation and shared liquidity in Phylons | 20 | 20 | Tie |
| From the JubAp.eu landing page to an intervention and its readings | 14 | 20 | Positioning |
| Business capability distributed across territories | 19 | 20 | Positioning |
| An expressed solution that still goes unheard | 20 | 20 | Tie |

## How they were compared

Both variants received the same question, budget and text blocks from the same source edition. The traversal that selects the pieces was changed. The previous algorithm was taken from commit `f269656e8e6ce937f833bb7946430d654d6e0356`, with radius four and up to sixty pieces; its reading was packed into complete blocks up to the common budget. Positioning applied the percentages and budget directly. The A/B presentation order alternated between questions.

Readers began without the author's history and worked exclusively with their packages. They produced an independent answer for each variant. Another reader judged the answers and received texts, without knowing which method corresponded to A/B and without using the scores proposed by their authors. Each answer received five scores from zero to four: mechanism, question coverage, documentary support, fluency for a third party, and temporal and attribution accuracy.

## What the tests changed

The first independent evaluation gave positioning three preferences, the previous traversal two and one tie. It showed two specific improvements:

1. Some website cards had a title and references but little reading text. Literal extracts from the Abstract or opening paragraphs were incorporated into 154 cards. Each extract identifies its source and hash; it also improves its thematic composition.
2. High thematic affinity could bring general indexes forward and displace concepts needed to explain the entry document. The traversal now retains up to four concepts directly supported by the article, ordered by affinity with its own composition. The visitor's weighted expansion follows. A documented-use relationship also incorporates the reading that develops that mechanism.

Two specific blind tests of the extracts preferred the corrected reading of Human Intelligence Debt and Phylons. The six questions were repeated with the same extracts available to both variants; the comparison was then repeated with the conceptual base close to the document. The table records the independent judgement from this last round.

The final version incorporated a documented-use reading before thematic expansion. Another new reader repeated the two affected questions: it maintained the tie in Human Intelligence Debt (19/19) and preferred positioning in distributed business capability (19/17). This test retained the same budgets and sources.

The small card records include their neighbours' percentages, clusters and costs. A reader can choose the next reading using those data. The 83 biographical passages share their source document and retain specific card entry points; the document URL opens the collection.

## Test of a configured URL

A new visitor used only web tools, with T874 as the entry point, 2,400 tokens, closed scope within Tegrity.AI and 70:30 human capability and AI integrity weights. The first manual reading showed that the selection and complete accounting needed to be delivered together. The cluster rule was strengthened and seven calculated configurations were added.

Another new reader found the matching package, retained the consultant role and answered in two paragraphs and one example. It recovered exactly 1,755 tokens used, 645 remaining and a next block of 726. It used T874, G21, T1400, T897 and T1425; all five pieces belong exclusively to Tegrity.AI. Web reading worked through GitHub's text mirror. The buttons for copying the assistant entry prioritise that text URL.

In the continuation of the dialogue, the visitor asked whether every human hour was debt. The reader explained the difference between necessary supervision and avoidable compensation and corrected the example's classification. The test thus checks configuration reading, use of its sources and development of a conceptual distinction in conversation.

## Test materials

- [Final comparison packages: group 1](paquetes-1.json) and [group 2](paquetes-2.json).
- [Group 1 answers](respuestas-1.json) and [group 2 answers](respuestas-2.json).
- [Independent judgement](evaluacion-independiente.json) and [variant key](clave.json).
- [Results of the first comparison](evaluacion-inicial.json).
- [Human Intelligence Debt extract test](extracto-hid.json) and [Phylons](extracto-phylons.json).
- [Final packages](paquetes-cierre.json), [final answers](respuestas-cierre.json) and [final key](clave-cierre.json).
- [Positioning protocol](../README.md), [functional tests](../pruebas-funciones.json) and [token check](../pruebas-tokens.json).

The code and test materials are versioned in this repository. Original article texts, source records and conceptual relationships retained their content.
