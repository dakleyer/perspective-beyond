# Iterative source review and node discovery

The Atlas grows through repeated comparison between source items and their conceptual cards. Each cycle returns to an identified source revision, reads the argument in context and asks whether the current nodes preserve its useful distinctions, mechanisms, conditions and questions. The resulting change can be a new node, a richer existing card, a new relationship, or a recorded decision that the present representation already does the work.

This procedure implements an incremental review cycle within Perspective Beyond. It uses the shared item, node and edge vocabulary of the [Atlas phase 2 procedure](https://github.com/dakleyer/structural-awareness-contributions/blob/atlas/phase-2-epistemic-distance-20261104/research/structural-awareness/atlas-phase-2/PROCEDIMIENTO_LENGUAJE_Y_RECORRIDOS_v0.2.md) and its versioned tag dictionary. Its outputs feed the existing Atlas; stable identities and earlier relationships continue through each cycle.

## The objects being reviewed

An **item** identifies something that can be revisited: a paper, webpage, dialogue, repository file, paragraph or other anchored source. Its hook states where to find it and which revision was read. A **node** expresses a conceptual position or unit of explanation linked to one or more items. One paper can support several nodes; the same node can draw on several papers. An **edge** explains a specific relationship between two nodes, with a predicate, direction, rationale and source references.

A paragraph is a candidate reading unit. It becomes a node when it supports an intelligible question and a useful conceptual distinction. A table row, heading, repeated disclaimer, source-control instruction or sentence fragment remains contextual material when it has no independent conceptual function. A short source can support an important node, and a long source can be adequately represented by relatively few well-developed nodes.

## 1 Establish the cycle boundary

Record the current item inventory, active node IDs, active edge IDs, dictionary version and relevant source revisions. Record counts and content hashes as comparison metadata. Use existing version history for historical comparisons. The working policy of the source environment governs storage; the review process does not require new backups or copies of source trees.

Separate three activities in the cycle record:

- Inventory inspection identifies items and existing card links.
- Resource parsing obtains the text, formulae, tables or other content returned by a reader.
- Semantic review compares a source argument with the cards that claim to represent it.

Each activity has its own completion state. A successful download or a valid JSON record establishes only the activity it actually completed.

## 2 Select sources by the question they leave open

Scan the full inventory and current card library to find useful review priorities. Examples include an item with no conceptual cards, a card that merely lists section titles, a mathematical result represented without its assumptions, several distinct questions compressed into one vague description, an altered source revision, or a source that could explain a mechanism mentioned elsewhere.

Treat these signals as prompts for rereading. A source-entry card can appropriately provide a short orientation, and a supporting image or administrative record may need no new conceptual node. The review decision depends on the source's function and on what its current cards already explain.

Declare the selected item revisions and sections for the cycle. Keep inaccessible sources in the queue with their attempted routes and retrieval result. Preserve the work that can proceed on other sources.

## 3 Read the source as an argument

Read the selected source from its definitions through its mechanisms, examples, conditions and conclusions. For a mathematical paper, follow the objects, quantifiers, domains, transformations and proof dependencies. For a case, follow the problem, actors, operating constraints, intervention, observed result and chronology. For a dialogue, preserve who speaks, what is recollected and which statements are later editorial interpretations.

Use the original source passage to settle a claim. Another Atlas card can suggest where to look, but its paraphrase cannot silently become the original evidence. When the source is itself a synthesis, retain that role and follow upstream references when the proposed claim depends on them.

Keep the following distinctions visible when they matter:

- Definition, derivation, working hypothesis, operating proposal and observed use.
- Existence of a mathematical object and effective access to it.
- Information available to a process and distinctions required by its target question.
- A result's source date, the date of a field event and a later conceptual interpretation.
- An entity's own work and a comparison with another entity's method.

## 4 Compare each useful idea with the existing nodes

Formulate the source idea as a question before deciding whether to create a card. Retrieve nearby existing nodes by their meanings, questions, references and terminology. Search and similarity ranking help find candidates; the source comparison decides what to do.

For each candidate, inspect the existing card's full description, formulations, conditions and sources. A title alone is insufficient for the comparison. Then choose a disposition:

| Disposition | Use it when | Result |
| --- | --- | --- |
| Covered | An existing card already explains the same question at the needed scope | Record its ID and supporting source passage |
| Enrich existing | The question is the same, but an explanation, condition, example or source role is missing | Add a located revision or explanatory facet under the existing ID |
| Add node | The source supplies a distinct mechanism, question, result, counterexample or scope worth following independently | Create a source-linked card and explain its difference from its nearest neighbours |
| Retain overlap | Two useful facets overlap while answering different questions | Keep both cards and record the specific relation |
| Record discrepancy | The source and card differ, or a source's own formulations conflict | Locate both formulations and record the comparison and correction decision |
| Defer | Access, meaning or source support remains unresolved | Keep the candidate and the reason it awaits review |

Different wording alone does not justify a new identity. Conversely, a broad node that names an entire research programme does not automatically explain each result within that programme.

## 5 Develop the card

Write a self-contained explanation that answers the node's question. Introduce the objects it uses, explain how the mechanism or argument works, and state the conditions that change its meaning. Add a worked example, formula or comparison where that makes the idea easier to use. Length follows the idea's needs.

Use the existing dictionary keys with their declared types. Typical useful properties are `node:role`, `node:mechanism`, `node:scope`, `node:distinction`, `node:observable` and `node:condition`. Existing explanatory extensions can carry a question, local terminology, derivation or worked example. A new tag proposal describes the distinction it adds, the closest existing keys, its value type and an example; translations and synonyms reuse stable keys.

Every source reference states its role and a locator. A paper may supply a definition, an earlier case may supply an operating example, and a later paper may supply an analytical comparison. Those roles belong to the relevant claims in the card.

### Explicit node-to-item hooks

Every node's `item_refs` entry includes an explicit resolution hook to the registered item card. The item card owns the original-source hook. The resulting path is **node → item card → source**, with the node reference also preserving the particular source selection used for its explanation.

The reference hook records the existing `item_id`, the item-card file URI and an exact JSON pointer to that card. Its `source_selection` keeps the original passage locator and the recorded revision or observation state. A reference that selects the entire item uses `{"kind":"whole_item"}`; adding the hook does not invent a paragraph or a more precise source claim. The role, source URI, revision and locator already recorded in `item_refs` remain intact.

This is a resolved representation of `trace:item_refs`. It introduces no new conceptual node, relationship or taxonomy key. Existing IDs and source hooks continue to identify the same objects. Loaders can expose `resolve_item_ref(node_id, reference_index)`, and human readers provide an **Open item card** link beside each source reference.

Validate the complete path: the reference resolves to its named item, the item resolves to its inventory record, and the selected URI and locator match the recorded source reference. Check local source targets where available. Report remote retrieval separately from identity resolution.

Keep existing IDs. A newly separated facet receives a new stable ID and a relationship to the earlier card. An enriched card retains its prior wording or revision through the established record history. Additions preserve earlier item, node and edge identities.

## 6 Search for relationships after the node is understood

Compare the developed idea with its nearest conceptual neighbours and with useful neighbours in other parts of the corpus. Ask what, specifically, travels between them. A relationship might specialize a definition, supply a mechanism, expose a missing condition, provide a counterexample, apply a method, compare operating settings, or connect a later formal account with an earlier field observation.

For each accepted edge, record:

1. The existing source and target node IDs.
2. A meaningful predicate and its semantic direction.
3. A short explanation of why these two particular nodes belong together.
4. The source passages or declared editorial comparison supporting that explanation.
5. Any time, scope or receiving-condition dependency.

Read both ends before accepting the edge. Shared tags or vocabulary provide a search route, while the rationale explains the relationship. Keep the network varied where the ideas justify it; every source need not lead to the same framework or central programme card.

Use chronology in the predicate. An earlier field case can motivate a later formalization; a later theory can offer a retrospective reading of that case. Claim historical use only when the source records that use.

Level 1 edges retain conceptual semantics. A/B/C/D and Jumps & Falls assessments belong to later situated walks under their own position, question and capability. This review cycle creates no universal epistemic score for a node or edge.

## 7 Keep a passage coverage ledger

For each reviewed source section, record the useful units considered, their dispositions and their output IDs. The ledger makes it possible to revisit why an idea became a new node, why another remained part of an existing card, and which questions await further work.

A practical cycle record contains:

```json
{
  "cycle_id": "source-review-001",
  "dictionary_version": "identified-version",
  "item_id": "existing-item-id",
  "source_revision": "commit-or-observed-revision",
  "resource_read": "complete_returned_resource",
  "reviewed_sections": ["section-5", "section-6"],
  "decisions": [
    {
      "source_locator": "section-6 theorem and proof",
      "question": "Which certified restriction preserves the search answer?",
      "existing_neighbours": ["existing-node-id"],
      "disposition": "add_node",
      "output_node_ids": ["new-stable-node-id"],
      "reason": "The existing card describes openness; this facet gives the exact condition for task-preserving pruning."
    }
  ],
  "unreviewed_sections": ["remaining-declared-section"],
  "reviewer": "identified-reviewer"
}
```

An unsuccessful retrieval remains a retrieval result. A parsed source awaiting semantic comparison remains in that state. Coverage counts report items, candidate units, reviewed nodes and accepted relationships separately.

## 8 Verify the actual integration

Validate the merged product, rather than only the additions file. Check that all earlier node IDs and edge IDs remain resolvable; sources, endpoint order, predicates and conditions remain recoverable; new item references resolve; and each accepted edge appears in the active relation indexes.

Check card quality separately from JSON structure. Re-read the new explanation against its source, examine its nearest neighbours for accidental duplication, test numerical examples and inspect formula conventions. If a derived balance equation and the surrounding prose disagree, retain the precise equation and locate the discrepancy for review.

Exercise the reader and loader. Open new and old cards, traverse accepted edges in their defined directions, and test search and narrow-screen presentation. Repeat the merge to verify that it does not multiply records or overwrite later editorial work.

## 9 Close the declared cycle and open the next one

A cycle closes when the selected source units have recorded dispositions, accepted changes are integrated and checked, and the remaining queue has an explicit state. Report the source revisions reviewed, nodes added or enriched, relationships accepted, duplicate candidates avoided and unresolved items.

The next cycle can start from the remaining queue, a changed source, an unexpected relationship or a question raised by a newly developed card. Source review and relation discovery therefore reinforce each other: a new relationship can expose a missing distinction, and a newly distinguished node can make a previously vague relationship precise.

## A source-grounded example

The [meta-existence and evaluability calculus](https://github.com/dakleyer/structural-awareness-contributions/blob/51fc686f45b6ef10c53b69f4c26d0e381b007ff8/research/structural-awareness/SA_METAEXISTENCE_CONTEXT_AND_EVALUABILITY_CALCULUS_v0.1.md), section 6, considers a search over a set S and a subset T. A qualified proof that the target property is false on S outside T preserves the existential answer when searching only T. Its finite-work comparison additionally prices certificate verification.

The review can therefore distinguish the logical preservation condition from the cost condition. A broad card about an open frontier supplies context; a focused card about certified pruning explains the equivalence; a reusable-proof card explains acquisition and repeated verification costs. The relationships between them state exactly which condition each contributes.

The [two-phase contextual requalification note](https://github.com/dakleyer/structural-awareness-contributions/blob/51fc686f45b6ef10c53b69f4c26d0e381b007ff8/research/structural-awareness/SA_META_VALUE_AND_CONTEXT_SYNTAX_REQUALIFICATION_TWO_PHASE_v0.1.md), section 6, adds a different question: whether eligible supplementary observations and an effective decoder can produce a revised executable answer. The shared vocabulary helps locate the connection, while the distinct source questions determine the cards and edges.

## Run the implementation example

The [example bundle](examples/source-review-cycle.json) uses illustrative IDs and the public exclusion proof above. It retains two earlier cards and their relationship, then adds a logical-preservation card, a separate cost card and their explained relationships. Baseline hashes make changes to earlier records visible.

Run the [standard-library checker](verify_source_review.py) from the repository root:

```text
python methodology/verify_source_review.py methodology/examples/source-review-cycle.json --self-test
```

The checker exercises identity preservation, recorded enrichment, source resolution, explicit node-to-item hooks, endpoint integrity, relationship explanations and the separation of level 1 edges from situated walk assessments. Its eight negative cases remove an earlier node, alter an earlier predicate, erase a rationale, break a source reference, place a global A/B/C/D label on an edge, remove a node-to-item hook, redirect that hook to a node, and remove the item's source hook. Apply this structural check after the semantic source comparison described above.

The example serializes endpoint IDs as `from` and `to`. An adapter can also read `source` and `target` with the same meaning and checks for conflicting aliases. The conceptual predicate and its direction remain explicit in either encoding.
