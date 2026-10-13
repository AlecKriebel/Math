# A credited single-edge obstruction to the literal Hopf-tree identification

Problem 30004409 / OWR-17471-016, rank 1073. Authored status: already_solved, 0/5. Findings: prior-known literal counterexample/source correction. This proof-and-audit-only draft leaves the repository QUEUE unchanged.

The source uses the full smooth, unordered and unoriented R^3 quotient and includes the single-edge tree. Its RAAG is Z^2. The explicitly imported Boyd–Bregman smooth theorem gives Q8; the authored proofs show that Q8 cannot embed in GL2(R), so it cannot be any actual subgroup of Aut(Z^2). The Dahm image is C2 x C2 and the kernel is central C2. This is prior-known mathematics applied to the literal source claim, with no new discovery or new proof-search turn. Revised conjectures and general connected forests remain unresolved here.

## Mandatory wording clarification

Read the last paragraph of Section 4 of original/PROOF_APPLICATION.md as follows: the oriented-and-labelled component has fundamental group C2, the kernel associated with the connected fourfold cover of the full link space. This is not a claim that this cover has degree two. The full eight-sheet decoration cover has two connected components. SU(2) to SO(3) is a different, twofold covering. The original authored note remains byte-for-byte preserved, with this additive clarification accepted. No mathematical correction to the proposition or Dahm exact sequence is required.

## Reading and scope

- original/PROOF_APPLICATION.md: source-matched proposition and credited topology dependency
- audit/INDEPENDENT_ACCEPTANCE.md: independent mathematical acceptance and cover clarification
- ACCEPTANCE.md and SCOPE.json: current scoped acceptance and authored target status
- original/SOURCE_AUDIT.md and metadata: public source URLs, hashes and inspection limits
- verification/REPRODUCTION.json: newly executed complete stdout/stderr receipts; historical outputs are not reused

The smooth topological theorem is an explicit imported result, not a topology proof established by finite checking. Neither a general forest formula nor an intended revised conjecture is solved here. The separate S^3 warning is not a premise. Goldsmith's full paper was not successfully inspected; the historical source and independent audit records state their actual bounds. Publication preparation performs no new source download, PDF rehash, or corpus rehash.

## Preservation and publication boundary

original/ is the complete original authored packet with its original manifest. The independent acceptance, authored checker, source-retrieval metadata, and input pins are preserved. historical/AUDIT_MANIFEST.json is metadata for historical evidence and does not claim that the omitted historical INDEPENDENT_VALIDATION.json is delivered. Its original hash and byte count are recorded in PROVENANCE.json. Its old workspace-bearing tracebacks are replaced for delivery by newly run, complete public-path outputs. DELIVERY_MANIFEST.json is the exact current inventory. No copied source text, PDF, dataset, private coordination material, or repository queue content is included. All published paths belong to this authored target packet.

## Reproduction and external trust

Copy bootstrap.py outside this delivery and verify its SHA-256 against the independently recorded draft PR value before running it. Use Python 3 with -I -S -B, as UID 1000, with a read-only delivery. Repeat with -O and -OO. There is no integrity-bypass option. The sole positional input is the delivery root.

The fixed external bootstrap authenticates the full manifest, acceptance, code and receipts before executing the verifier. Full stdout/stderr are compared byte-for-byte with the same mode and label, with recursive exact JSON types. Actual directory-create and existing-file write-open attempts must be denied. Receipt stages explicitly avoid circular self-hash claims. Reproduction requires only this authored packet; no source PDFs, dataset, or repository tracker is required.
