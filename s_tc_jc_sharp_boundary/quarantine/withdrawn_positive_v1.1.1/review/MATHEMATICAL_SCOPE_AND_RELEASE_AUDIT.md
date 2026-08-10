# Mathematical scope and release audit

## Verdict: PASS after reconstruction-scope correction

A release-oriented audit checked the manuscript independently of its prose-development workflow. The headline theorem concerns the open four-state Jukes--Cantor model on all binary standard semi-directed `S_TC` level-2 networks, modulo ordinary triangle redirection. The formerly explicit one-triangle-per-blob restriction is no longer an assumption: a separate theorem proves it automatically for the larger class `W_TC`. The statistical result distinguishes a common full-dimensional regular germ from equality of complete stochastic images.

The reconstruction theorem has been narrowed to the exact consequence of the
classification. It returns one canonical structural topology modulo labelled
isomorphism and `T`, and may enumerate the structural `T`-equivalence class.
It does not assert that one fixed input distribution belongs to every
redirected model. Input-specific triangle-orientation membership is left as a
separate semialgebraic problem.

The audit rechecked the dependency chain:

1. structural reduction of every level-2 blob to a cycle or theta core;
2. reduction of any two-triangle theta to path lengths `(1,2,2)` and exclusion
   of all tree-child rootings, with independent Python and C++ census;
3. primitive cycle and four-theta generator enumeration;
4. bounded-support and ordered-word reconstruction;
5. complete five-, six-, and seven-outgoing-port local universes;
6. source/target orientation for every directed containment relation;
7. exact residual seven-port trinet separators;
8. pointwise cut preservation, including two active endpoints;
9. root reduction, including insertion on a retained reticulation edge;
10. reciprocal bridge gauge and local-product projection;
11. semialgebraic full-dimension and proper-exceptional-set arguments; and
12. the exact `W_TC \ S_TC` Theta sharpness family.

The hash-locked base statistical theorem remains an input and is composed with
the automatic triangle theorem through a machine-readable strengthening
certificate. No quarantined historical gate or richer-model artifact is a
theorem dependency. The release verifier is fail-closed: any failed universe
count, graph code, polynomial identity, strict sign, Jacobian minor, structural
census, or dependency hash aborts before reporting success.
