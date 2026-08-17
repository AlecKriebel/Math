# Authoritative status

Status: **PROVED — FINAL OUTCOME A**

Release revision: **v1.1.3 Englander-crosswalk and portal-package hardened**.
The v1.1.2 proof and public-replay release remains mathematically unchanged.
v1.1.3 locks the exact Englander-v4/Omega comparison, prints complete Omega
rank-minor provenance, adds the quartet-distance comparison, and places a
small verifier-entrypoint ZIP in every submission-support set.  The bioRxiv
map uploads it as supplementary code; the journal maps route it to the
external repository in accordance with their current policies.  The full
graph/certificate archive remains an external hash-bound release asset and
counts as published evidence only after the separate public-download verifier
returns `PUBLIC_RELEASE_VERIFIED`.

Manuscript: **Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary for
Level-2 Jukes–Cantor Networks**

The active release proves the exact one-sided classification

```text
N preceq_JC N'
  iff
their labelled reduced bridge trees agree and corresponding nontrivial blobs
are labelled-isomorphic or differ by ordinary triangle redirection T.
```

The scope is the open four-state Jukes–Cantor model on binary, LSA-valid,
already-simple, reticulation-preserving semi-directed strongly tree-child
level-2 networks. Consequently there are no proper one-sided generic
containments, symmetric full-dimensional regular overlap is characterized by
the same relation, and a generic exact distribution determines one standard
semi-directed topology modulo `T`.

The boundary is sharp even without triangles. The bounded Omega audit proves
that, for every `n >= 4`, the larger weakly-but-not-strongly tree-child class
contains a triangle-free nonisomorphic, non-`T` pair with a common
full-dimensional regular JC germ of dimension `2n+1`. The separately frozen
Theta family supplies a second triangle-containing mechanism of dimension
`2n`.

The proof uses the full incidence-scaling bridge quotient. It does **not**
claim recovery of physical bridge multipliers, equality of complete
stochastic images under `T`, pointwise classification of the exceptional
locus, K2P/K3P results, or a theorem for arbitrary hidden rooted refinements.

The active manuscript, dependency graph, theorem-to-certificate crosswalk,
release metadata, exact component verifiers, and, once generated from the
immutable source commit, clean-clone transcripts are the only authoritative
release surfaces. Superseded claims are retained only under `history/` and
are not inputs to any active verifier.

The release uses a non-self-referential two-layer seal. The core metadata in
this directory is included in the persistent archive.
`ARCHIVE_SOURCE_COMMIT.txt` records its immutable source commit, and the
external `release_artifacts/RELEASE_ENVELOPE.json`, once sealed, binds that
commit, the three clean transcripts, and the final archive hash.
