# Complete public reading of the Atlas

The web entry is https://integralmanagement.ch/atlas-reader/ . It includes the assistant guide, indexes, the text of every card and concept, their relationships in both directions, sources and perspectives by tag. The visitor can give that single URL to their assistant. The URL configuration is retained in the guide itself.

The HTML is served in full: the reader receives content and links before executing JavaScript. Each card also publishes lectura.txt and registro.json. The inventory associates each identifier with its HTML, text and data URLs. sitemap.xml allows the pages to be discovered; the root llms.txt publishes the reading entry. The projection uses the graph records without creating or deleting cards or relationships.

Generate: `python scripts/build_atlas_public_reader.py`. Check currency: `python scripts/build_atlas_public_reader.py --check`. Check links: `python scripts/check_atlas_public_reader.py`.

The repository retains the graph and versions. The HTML delivery is a projection of the same content for people and assistants. Existing visual interfaces retain their function and design; this route adds public reading and discovery of the complete corpus.

The institutional-domain reader serves the pages on its own domain and retains a copy of every public resource with SHA-256 verification. The source corresponds to a specific repository commit. The visitor and their assistant explore the cards and relationships without accessing the repository. Every public response links the guide through Link: describedby. Card records and the graph retain their original fields.
