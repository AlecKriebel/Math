# Independent tooling adversary contract

Scope: only PR 883 / PID 9900008 new verification tooling. This is neither mathematical approval nor either of the two required new final whole-package reviews. No new proof search, PDF work, external communication, git changes, releases, or work on other PRs.

Independence: authored before the candidate seal and before reading an engineer verdict. Original check_publication.py (6670 bytes) and author/verify.py (10266 bytes) were fully read, including entrypoints. Candidate execution is prohibited until the parent supplies its final manifest/code pins; every candidate line, including isolated bootstraps, must first be read.

External original anchor: SOURCE_MANIFEST.json SHA-256 53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab, frozen head af25d26e21945a1a132aace5e600485152777070, 26 files and 211771 bytes. The anchor is supplied independently of the candidate. Original replay is supplementary and finite; legacy code by itself is permissive about JSON and file metadata.

Success criteria: independently exercise the sealed standalone scripts and distinguish actual rejection from an assumed negative-control label. A nonzero process must carry the expected verifier rejection and no archival execution when authentication should fail. Positive baseline and normal/-O outputs must agree materially. Preserve command/stdout/stderr/returncode evidence with mode and exact assertions.

Attack families:
1. Startup and trust: authenticate installed code/inventory before original code executes; forged inventory/anchor, altered originals, unsafe startup and PYTHONPATH shadowing; explicit no hostile-code sandbox/no trust if all anchors replaced.
2. Strict serialization: duplicate keys, NaN/Infinity and exponent overflow; boolean/float where integer labels, counts or byte sizes are required; forbidden unknown keys and absent/nonempty required layout paths.
3. Closed filesystem: extra and missing regular files, unexpected empty directories, symlink/fifo/ancestor aliases, payload aliases and bounded reads. Private fixture copies only; original corpus hardlinks read-only, unlink before mutation, never chmod/truncate originals.
4. ZIP structure: preamble/trailer, comments, unsafe and duplicate members, divergent local/central metadata, overlaps, limits; equality with the exact 26-source archive and 24 preserved outer-root originals.
5. Binding semantics: cross-copy bindings/metadata equality, catalog-review canonical pair and optional source/corpus real bytes versus claimed records only.
6. Builder: output byte determinism between ordinary and -O invocation, collision abort without partial overwrite, fail closed on malformed layout/source.
7. Replay semantics: six direct and sixteen nested replays if that is the final explicit contract; requested versus effective flags, intercepted child request count and -I -S -B effectiveness; original 18 negative controls must be actual rejections.

Method: test materially distinct mutations in sequential small fixtures and remove this audit's transients. Record candidate pins, complete-code-read evidence, final positive/negative counts, gaps and decision. Public manifest includes only own authored safe tooling/report/log and compact textual outputs, never private PDFs/corpora.
