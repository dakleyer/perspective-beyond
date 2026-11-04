# Mind Atlas: public reading on the institutional domain

Entry: https://integralmanagement.ch/atlas-reader/

A single URL discovers the guide, clusters, tags, cards, concepts, documents, relationships, UTF-8 texts and JSON records. Each response links the guide through the HTTP Link describedby header. The HTML already contains the text and its links; the reader requires no JavaScript, cookies, credentials or special headers.

The component only handles GET and HEAD under /atlas-reader/. Its manifest lists the public files of an immutable repository revision and their SHA-256 hashes. The first reading retrieves the public resource from that revision, verifies its hash and retains it as a local publication asset in uploads/mind-atlas-reader. Subsequent readings are served from that copy. The visitor navigates only through the institutional domain.

The fields of the cards, relationships and graph remain identical; the transport adapts the HTML and text navigation URLs to the reading domain. Each card's JSON record retains the complete node and its relationships. The JSON graph retains the same hash as the source.

The package is built with package.py from an already published revision. It requires and contains no private material, credentials or workspace copies. It does not modify articles, users, capabilities, editorial content, themes or security settings. The resource is published as a component belonging to the project.
