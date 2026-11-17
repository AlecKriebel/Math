# Lossless native snapshots

These files retain the complete structured native connector responses, including every CellData field and all eight sheets' metadata. `recursive-json-intern-v1` replaces repeated arrays/objects with `$ref` indices into `nodes`; array nodes contain `items`, object nodes ordered `entries`. Primitives are unchanged. Recursively expand references from `root`. Round-trip equality to the complete original structured response was checked before saving. Transport-only duplicate text is omitted.
