You are an adversarial independent mathematical/software reviewer.  Work
read-only.  Review only the clean-room primitive atlas at

`s_tc_jc_landmark_closure/independent/decorated_atlas/`

in the repository `/Users/alec/Documents/Math-stc-jc-final-repair`.

First read:

- `s_tc_jc_landmark_closure/docs/DEFINITIONS_LOCK.md`;
- `s_tc_jc_sharp_boundary/repair/reviews/ATLAS_GATE_REVIEW.md`;
- `s_tc_jc_sharp_boundary/repair/reviews/DEFINITIONS_GATE_REVIEW.md`.

Do not import, execute, or trust historical atlas generators, canonicalizers,
Fourier engines, tables, or separator selectors.  Inspect the new source files
and the `certificates_p7_trial` records.  You may run bounded independent
scratch calculations in `/tmp`, but do not modify the repository.

Actively try to falsify:

1. exhaustion of primitive cycle/theta ported blobs under the locked narrow
   standard `S_TC` convention;
2. duplicate-free graph canonicalization and every raw-to-canonical transport;
3. the admissible-rooting/LSA census and compatibility with one-step root
   suppression;
4. graph -> displayed switchings -> descendant masks -> exact JC polynomial
   compilation;
5. joint canonicalization of ordered source-target relations with complete
   port matching, including source/target edge and inheritance transports;
6. mutation sensitivity;
7. the *limited* claim that equality of the displayed-parameter signature is
   sufficient for complete JC tensor equality under an explicit edge and
   reticulation-choice permutation.

Check especially for missing primitive roles, a false local-to-global use of
`S_TC`, an invalid LSA test, relation IDs that collapse distinct source
embeddings, incorrect inheritance-weight transport, and any inference from
unequal signatures.  The implementation must not claim that this signature is
a complete observational separator.

Return a concise report with P0/P1/P2 findings, exact file/line references,
tests performed, and one verdict:

- `ACCEPT_PRIMITIVE_GATE`;
- `ACCEPT_AFTER_LISTED_CORRECTIONS`; or
- `REJECT_PRIMITIVE_GATE`.

Do not assess or endorse the full global identifiability theorem; this review
is only for the bounded primitive-atlas gate.
