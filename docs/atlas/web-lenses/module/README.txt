MIND ATLAS — NUEVA PERSPECTIVA

One shared graph. One reading window for each page.

OPEN THE PROJECT
https://integralmanagement.ch/nueva-perspectiva/atlas-mental/
https://perspective-beyond-atlas.carvedgem.chatgpt.site/mind-atlas/
Canonical source: https://github.com/dakleyer/perspective-beyond/tree/main/docs/atlas/web-lenses

STRUCTURE
Source document → cards → tag compositions → explained relationships with other cards and concepts.
A web page retains its text and visual map. The designer selects the entry point, tag weights and a small reading budget. The expanded view reproduces that same configuration over the shared graph.

PUBLISHED CRITERIA
profiles.json contains each page's URL, starting cards, weights, budget, scope and reproducible URL. selections/ contains the JSON result and the text reading prepared for assistants. All selected nodes and relationships retain their canonical graph identifiers.
Pages with their own cards start from those cards. Other entries publish the designer's starting selection, connecting that reading with existing cards. This configuration is a navigation layer; the graph substrate is retained.

CALCULATION
docs/atlas/positioning.mjs is used: readPosition, positionMap and positionParams.
Each card's percentage composition allows affinity with the chosen weights to be calculated. Traversal follows existing relationships and retains the paths to each addition. The budget counts the text of selected cards and relationships with o200k_base. A card is not split when the limit is reached. The mini-map shows a connected prefix; the downloadable reading retains the complete selection.
A weight does not grant access or modify a source. Closed, porous or federated scope determines which clusters may participate.

CONFIGURED URL EXAMPLE
https://perspective-beyond-atlas.carvedgem.chatgpt.site/perspective-beyond/atlas/posicionamiento/?posicionamiento=E1628&tokens=2200&max=11&modo=federated&site=eu&peso=tema%3Aperspectiva%3A45&peso=tema%3Atransformacion%3A30&peso=tema%3Aaprendizaje%3A15&peso=tema%3Adecision%3A10

COMPLETE EXAMPLE FOR UNDERSTANDING
Open the text entry for The JUBAP Framework page: selections/eu-1628.txt. Start from its source document. Explain the UP movement and how it relates to JUMP. Choose two connections from the reading that help understand the mechanism. Explain what each contributes and retain source links. Ask what situation I want to examine.

COMPLETE EXAMPLE FOR COMPARISON
Read selections/net-1287.txt. I want to compare tacit knowledge transmission in Tiger Teams with another learning experience from the same Atlas. Distinguish the knowledge being transmitted, who can exercise it and what conditions allow it to continue. Explain one useful similarity and one difference that changes its application. Retain the texts' dates and contexts and link their originals.

CONFIGURE A QUESTION
1. Identify the entry document or card.
2. Choose the purpose: understand, compare, solve, teach or develop.
3. Retain any configuration already in the URL. Ask only for what is missing.
4. Choose tag weights: for example aprendizaje 50, perspectiva 30, encuentros 20.
5. Choose scope and budget. Increase the budget when the question needs more reading.
6. Read the relationships, explain the mechanisms and return to the original sources.

SHARED ASSISTANT PROTOCOL
https://tegrity.ai/wp-content/uploads/2026/11/atlas-web-entry-2884295fa843.txt
UPPER-LEVEL ORIENTATION
https://perspective-beyond-atlas.carvedgem.chatgpt.site/orientacion/
CLUSTERS
https://perspective-beyond-atlas.carvedgem.chatgpt.site/clusters/
CARDS
https://perspective-beyond-atlas.carvedgem.chatgpt.site/fichas/

MAINTENANCE
Update the public inventory and designer profiles. Run build_selections.mjs with the same graph and positioning module. Verify identifiers, relationships, budgets and links. Publish the profiles, selections and their integration. Regeneration does not rewrite articles, methodological notes, field notes or Related; it retains the design of existing maps.
