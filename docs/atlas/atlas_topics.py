"""Cross-cutting reading labels. A label changes priority, not source permissions."""
import re
import unicodedata


# Match the subject of a card through its title, scope summary and existing concept names.
# Narrow labels can overlap. The three requested lenses require their own subject evidence.
TOPICS = {
    "matematicas": ("Mathematics", r"mathemat|matematic|teorem|theorem|probabilit|proof(?![ -]of[ -]concept)|prueba formal|combinatori|axioma|axiom|formal core|analisis formal|computability|indecidib|undecidab|boolean|arithmetic|primality|primalidad|finite.state|information theory|logica formal|\bproof reuse\b"),
    "empresa": ("Business and management", r"enterprise|empresar|empresa|organizaci[oó]n|organizativ|organizational|business|company|industria|rationaliz|racionaliz|management|gestion|supplier|luxury|manufactur|reestructur|operating model|modelo operativo|operational continuity|continuidad operativa"),
    "espiritualidad": ("Spirituality and inner life", r"\b(?:espiritual\w*|spiritual\w*|transpersonal\w*|religio\w*|meditacion|meditation|mistic\w*|mystic\w*|contemplacion|contemplative|interioridad|oracion|monasterio|fe)\b|vida interior|consciencia plena|inner life"),
    "perspectiva": ("Change of perspective", r"perspective|perspectiv|marco mental|punto de observacion|epistemic distance|semantic window|ventana semantica|encuadre|reframing"),
    "representacion": ("Representation and formal boundaries", r"metasynt|metasint|semantic transfer|representaci|representation|scope|model.theoretic|restriccion|context restriction|syntactic|sintact"),
    "mundo-abierto": ("Open world and indeterminacy", r"open.world|open universe|mundo abierto|aprime|indetermin|undecid|indecid|non.closure|residual|unresolved frontier|outside the sampling frame|blind.spot"),
    "evidencia": ("Evidence, provenance and attribution", r"evidence|evidencia|provenance|procedencia|attribution|atribucion|traceab|trazabilidad|source.qualif|source.anchored|certificat|fuente primaria"),
    "autoridad": ("Authority, permissions and delegation", r"authorit|autoridad|delegat|delegaci|permission|permiso|privilege|privilegio|decision rights|least privilege|citizenship|identity binding|legitimidad"),
    "control-minimo": ("Minimum control and sufficiency", r"minimum sufficient|control min|msca|bounded effort|presupuesto epistemico|sufficien|suficien|limited control|requalification|recalificaci|guard scope"),
    "cambio-regimen": ("Regime changes and early warning", r"regime|regimen|early.warning|alerta temprana|concept drift|mission drift|semantic toctou|state transition|cambio de contexto|context change"),
    "agentes": ("Agents and distributed coordination", r"agentic|agentico|multi.agent|cross.agent|agent architecture|agentes|orchestrat|orquestaci|coordinacion distribu|distributed coordination|participant.local|collective residual"),
    "cartografia": ("Cartography and ecosystem signals", r"cartograph|cartograf|ecosystem awareness|ecosystem positioning|ecosystem signall?ing|reposition|reposicion|signal|shared maps|mapa y flujo"),
    "capacidad-humana": ("Human capability and intelligence debt", r"human intelligence|inteligencia humana|human capacity|capacidad humana|human escalation|compensatory|attribution gap|tacit knowledge|saber tacito|conocimiento tacito"),
    "experimentacion": ("Experimentation, falsification and counterexamples", r"falsif|countermodel|contraejemplo|ablation|ablacion|fixture|harness|experiment|benchmark|trial|reproduc|regression|regresion|oracle|oraculo|validation profile"),
    "integridad-ia": ("AI integrity and security", r"ai integrity|integridad de ia|integridad operacional|security|seguridad|attack|ataque|safety|prompt injection|agentic threat|agentic integrity|nist ai|00k|00l"),
    "economia": ("Economics, costs and liquidity", r"econom|cost|liquidity|liquidez|capital|money|dinero|financial|financ|incentiv|exergy|exergia|utility|utilidad|allocation|asignacion"),
    "movilidad": ("Mobility and infrastructure", r"mobility|movilidad|transport|logistic|logistic|aicm|airport|aeropuerto|smart city|car evolution|xseil|tuxpan|infrastruct|infraestruct"),
    "estandares": ("Standards and interoperability", r"standards|estandar|fg.tida|fg.ai4ssc|itu.t|un cstd|unece|nist|interoperab|normativ"),
    "transformacion": ("Transformation and operational continuity", r"transformat|transformaci|continuity|continuidad|rationaliz|racionaliz|integration|integracion|tiger team|jump up|implementation|implementacion"),
    "memoria-territorio": ("Memory, community and territory", r"totonacapan|territor|comunidad|community|biograf|biograph|memoria|legado|archivo|archival|custodi|transmisi"),
    "aprendizaje": ("Learning and capability transmission", r"learn|aprendiz|taller|mentoria|mentoring|capability transfer|transferencia de capacidades|formacion|training|practica de libertad|atencion y sentido"),
    "decision": ("Decisions and responsibility", r"decision|responsabilidad|responsibility|confianza y equipos|judgment|juicio|solidaridad"),
    "geopolitica": ("Geopolitics and borders", r"geopoliti|conflict|conflicto|cross.border|fronteras|sarajevo|tuzla|bosnia|papantla"),
    "casos": ("Use cases and applications", r"case stud|caso de uso|model case|use case|aplicacion|scenario|escenario|case notes"),
    "documentacion": ("Research and technical documentation", r"research portfol|research initiative|annex|anexo|verification|verificacion|reconciliation|conciliacion|revision|review|documen|source and concordance|corpus|working note"),
    "navegacion": ("Indexes, contact and policies", r"^(?:privacy policy|legal notice|contact|case studies|field notes|jubap(?:\.(?:eu|us|net))?|tegrity\.ai)$"),
    "compromisos": ("Commitments and available capability", r"committed capacity|capacidad comprometida|capacidad disponible|organizational encumbrance|liquidez compartida|shared.liquidity|obligaciones futuras|garantia.*promesa"),
    "legitimidad": ("Legitimacy and principles", r"legitimidad|legitimacy|impugn|principios.*requisitos|razones.*examinar|consentimiento|consent"),
    "encuentros": ("Encounter infrastructure", r"infraestructura.*encuentro|curaduria.*encuentro|posada|hospitalidad|hospitality|agoras|microengagement|perfiles de frontera"),
}


def plain(text):
    folded = unicodedata.normalize("NFD", text.casefold())
    return "".join(char for char in folded if not unicodedata.combining(char))


RULES = {key: re.compile(rule) for key, (_, rule) in TOPICS.items()}
EDITORIAL_TAGS = {
    "E1874": {"transformacion"}, "E1706": {"empresa", "transformacion"},
    "N1265": {"empresa", "transformacion"}, "T1411": {"transformacion"},
    "T1491": {"perspectiva"}, "T1494": {"cartografia"}, "T2931": {"control-minimo"},
    "S23": {"estandares"}, "T1726": {"estandares", "integridad-ia"},
    "np-entrada": {"perspectiva"}, "np-experiencia": {"perspectiva", "aprendizaje"},
    "np-lectura-manifiesto": {"perspectiva", "decision"}, "D-019": {"empresa", "transformacion"},
    "D-029": {"empresa", "perspectiva"}, "D-078": {"aprendizaje", "decision"},
}


def classify(text):
    value = plain(text).strip()
    return {key for key, rule in RULES.items() if rule.search(value)}


def build_topics(records, concepts, notes, membership, curated):
    concepts_by_source = {record["id"]: [] for record in records}
    for concept in concepts:
        for sid in concept["sources"]:
            if sid in concepts_by_source:
                concepts_by_source[sid].append(concept.get("original_label") or concept["label"])
    source_tags = {}
    for record in records:
        sid = record["id"]
        note = notes.get(sid, {})
        fields = [record["title"], note.get("summary", ""), *concepts_by_source[sid]]
        tags = classify(" ".join(fields)) | set(curated.get(sid, ())) | EDITORIAL_TAGS.get(sid, set())
        if RULES["navegacion"].fullmatch(plain(record["title"]).strip()):
            tags.add("navegacion")
        if "espiritualidad" not in classify(" ".join(fields[:2])):
            tags.discard("espiritualidad")
        if note.get("provenance") and not tags:
            tags.add("documentacion")
        if record["kind"] == "ficha de diálogo" and not tags:
            tags.add("aprendizaje")
        source_tags[sid] = sorted(tags)
    topics = {}
    for key, (label, _) in TOPICS.items():
        sources = [sid for sid, tags in source_tags.items() if key in tags]
        if sources:
            topics[key] = {"label": label, "sources": sources,
                           "clusters": sorted({membership[sid] for sid in sources})}
    return topics, source_tags
