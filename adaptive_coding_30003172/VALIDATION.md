# Validation scope and procedure

The mathematical acceptance is the documented independent review in INDEPENDENT_AUDIT.md. No computational experiment or automated mathematical proof check is claimed.

Byte integrity was tested using Python in ordinary and optimized (-O) modes. Isolated package copies were then modified, with each mutation tested in both modes: appended content; same-length replacement; deleted file; unexpected extra file; a file replaced by a symlink; invalid manifest schema; duplicate manifest entry; and unsafe manifest path. Both unmodified runs must pass and every modified run must return failure. Tests run on temporary copies, never on the frozen deliverable.

All JSON files are parsed and package Markdown is checked for private source-directory names and workspace paths. A packaging review confirms that no copied PDF, extracted third-party text, dataset contents, or private coordination artifacts are present. Original authored-input hashes are recorded in PROVENANCE.json; file hashes in MANIFEST.json identify the sanitized output.

These checks only establish internal byte consistency and intended packaging behavior. They do not certify proof validity, novelty, completeness of the literature search, authenticity of external sources, or authenticity against replacement of both package and manifest. Retain the separately reported manifest SHA-256 to anchor this frozen version.
