# Independent whole-helper review 04

**Disposition: one remaining material conservative-alias guard gap. Do not use this report as unconditional approval of v4.** No live append, service mutation, Git mutation, outreach, or new publication was performed.

The complete reviewed helper is `reconcile_external_ledger_v4.py`, 15464 bytes, SHA-256 `99f3d6760535f158e219ed5d2a2ae594e3f254bfec7b5c87f403b4eacdba56d3`. The reviewed plan has SHA-256 `83df78463704c63ea3969a87325f18ab21c21893d6e1b8b49c5b16a6b4e3b2e1`. I read the entire helper and plan independently before reviewing any earlier ledger report. No earlier ledger report was needed or read for this conclusion.

The accepted scope is recording one existing Alper Ferudun publication, version 1.0, record 23350364 / concept 23350363. The plan accurately distinguishes complete separate Dickinson Question (2), maximal finite CP-plus rank equals p_n in every positive order including singular matrices and attainment, from the unresolved general pointwise gap in Question (1). It states the exact ordinary-rank corollary, prior Perron-lift credit, AI-assisted unrefereed status, and limits of finite regression checks. It does not transfer authorship to Alec Kriebel or assert chronological firstness. Mathematical and priority root acceptances are inputs to this operational review, not independently reproved here.

## Material finding: unresolved resolver references escape the alias gate

`ops_binding.py:445–448` sets the unresolved short-resolver flag only for `http://` or `https://` forms. The row/account paths do use that exact pinned function, but these four textual references are accepted without identity review:

- `//shortdoi.org/abc`
- `//doi.org/abc`
- `shortdoi.org/abc`
- `doi.org/abc`

The whole helper reaches a simulated append and writes a verified receipt when any one appears in any of the four cells of an otherwise unrelated ledger row, or in the metadata of an otherwise unrelated owned account record. In contrast, `https://shortdoi.org/abc` and `https://doi.org/abc` correctly stop before append. The account scanner serializes and inspects the full raw record, so this is not a raw-field projection problem; the underlying unresolved-alias recognizer omits reference forms.

The suffix `abc` is fabricated fixture text. I make no claim that it resolves, that the references are HTTP-equivalent, or that a current ledger duplicate exists. The issue is that an unresolved resolver lead of the same kind already treated as requiring root review silently bypasses the conservative gate when its scheme is omitted. It could conceal the relevant identity until resolved. The requirement under review includes robust unresolved alias leads; that guarantee is therefore incomplete. The suitable response is conservative review/blocking for these exact reference classes, not guessed canonical identity or unbounded substring matching against arbitrary foreign URLs.

`alias_boundary_probe.py` is a standalone reproducer atop the whole-helper harness. All 22 cases were run under normal, -O, and -OO Python. Each mode produced 20 unexpected simulated append-plus-verified-receipt outcomes and two correctly blocked full-URL controls. The three `ALIAS_BOUNDARY_MODE_*.json` files preserve exact case outcomes. No real resolver request was made.

## What the remaining guard matrix established

The separate 156-case matrix passed completely in each of normal, -O, and -OO Python: 468 expected outcomes. Cases execute the exact full helper bytes and all six actual dependency sources in fresh, private fixture trees. An audit hook rejects any accidental real socket resolution/connection, process launch, or system execution. The stubs permit only the reviewed read calls and an in-memory simulated append; no real boundary was attempted. Fixtures are deleted after each case, and all original source/data SHA pins matched before and after every mode.

Controls cover the following mechanisms:

- External acceptance SHA, ready flag, exact helper/plan hashes, full dependency inventory, individual dependency tampering, leaf symlink rejection, and review evidence tampering. The plan and all six sources were replaced on disk after their first read in one passing control; execution still used the parsed/compiled checked snapshots. Shadow modules and invalid cached bytecode did not enter the reached project import path.
- Complete three-page owned enumeration, stable exact totals, duplicate and malformed records, missing pages, loops and foreign pagination, known positive record 23408971, unrelated drafts, target drafts, raw id/parent/pids/concept/arbitrary fields, semantic leads, every known MD5 in prefixed/unprefixed/mixed-case forms, fully encoded aliases, and bounded deep encoding.
- All four ledger columns, version/concept identities, ambiguous full-URL aliases, later-cell ambiguity after an earlier match, duplicate exact rows, wrong attribution, four-column header/data schema, nontext/fifth cells, title/gid/spreadsheet binding, full range and ROWS orientation.
- PR head/base/body and final state/merged/draft changes; exact publication metadata, family, file inventory, three payload MD5/SHA/size checks, and strict live DOI destination outcomes. Freshness passes at exactly 0 and 180 seconds and blocks negative age and 180.001/181 seconds.
- Exclusive intent races and fsync ordering for file plus directory, immediate ledger changes, lost append response, absent-row unknown-outcome blocking, exact-row idempotent adoption, both spreadsheet IDs in the append receipt, ROWS orientation, exact four updated cells/one row/four columns, exact data/range/values, preservation of all preceding rows, no extra row, exact final-row range, and unique version/concept identity.

The harness checks durable intent before its simulated append. It also records that a malformed response or postappend mismatch can occur after a mutation: such cases retain intent and fail verification; they are not represented as rolled back. A lost response causes no automatic retry. A later invocation may adopt the unique exact existing row; absent row plus existing intent stops.

## Trust and concurrency limits

Root must execute the helper source snapshot it has itself SHA-checked, using the canonical `__file__` and the externally anchored acceptance SHA argument. This is specified in the review task and closes the entry-code load race; the helper then checks and executes exact dependency source snapshots. Interpreter, standard library, credentials, CLI binaries, provider authenticity, and root-adopted acceptance contents remain environment/trust assumptions. No helper can infer mathematical equivalence of every unlabelled account record from lexical or checksum leads.

The local exclusive intent coordinates invocations sharing that intent path. It does not lock Google Sheets, GitHub, or Zenodo globally. Immediate rereads and the 180-second gate reduce the window but cannot prevent another actor from changing a service after the final read or after final read-back. The append response/read-back checks detect the tested inconsistencies; they cannot undo a successful external append. The receipt must be read as checked observations at its time, not a cross-service transaction, future invariant, universal proof, or global priority certification.

The review's ordinary source/data inputs are hash-mapped in `SOURCE_PINS.json` and retained once in a private 6.7 MB snapshot. Public review artifacts are bound by the closed nonself manifest. Private snapshots and Python caches are explicitly excluded from the public artifact inventory.
