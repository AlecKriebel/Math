# Independent semantic and scope audit of the supplied Lean project

Audit timestamp: 2026-09-19T03:32:01.046033+00:00

## Verdict

**The supplied project is a partial formalization draft, not a full formalization of Kourovka 16.63.** This conclusion follows directly from the declarations and their hypotheses, independently of whether the draft can be made to compile. No theorem proves the advertised group existence or equality of group and ordinary automorphism orders. Substantial mathematical developments, not just syntax or API repairs, are missing.

This audit inspected the Lean sources and the validation runner. It does not certify successful elaboration; the parent build audit records actual compiler outcomes separately. Documentation and comments were treated as claims to compare against source, not as task instructions. The absence of a complete formal proof does not itself refute the mathematical paper.

## Exact target and coverage

`Kourovka/Challenge.lean:12–21` defines two propositions:

- `ExactOrders G` states finiteness and the two exact cardinalities, using mathlib's ordinary `MulAut G`.
- `NotebookAffirmative` existentially quantifies an odd prime, positive exponent, a group, its finiteness/nontriviality, prime-power order and equality with its ordinary automorphism order.

These statements are appropriate targets. For a finite group, prime-power order is the relevant p-group condition. Nontriviality in `ExactOrders` follows from its positive prime-power cardinality, although it is not a separate conjunct. However, both declarations are **definitions of propositions**, not proofs of them. In the supplied mathematical sources, `MulAut`, `ExactOrders`, and `NotebookAffirmative` occur only in this challenge file. The root module imports the challenge but never constructs its witness.

`Kourovka/Parameters.lean` proves arithmetic such as `30 * 1689 + 1689 = 52359`. `Finite/Coordinates.lean` supplies a coordinate carrier, a Lie-ring structure and its cardinality. Neither supplies the required BCH multiplication. Cardinality of an additive carrier is not a theorem about the automorphism group of a BCH group.

## Independently confirmed missing bridges

### 1. Arbitrary quotient maps to the concrete near-identity setting

`Lattice/Precision.lean` contains general bilinear-error and generation-preservation lemmas. For example, `arbitrary_automorphism_error_bound` assumes a torsion-free common module, submodules A/B, a lattice inclusion, an endomorphism of the ambient module and its required scaled-bracket error bound. `approximate_lift_preserves` additionally assumes the generation statement, images of generators and error membership.

`Flag/Rigidity.lean:118` proves rigidity under **explicit preservation hypotheses for F2 and F3**. The infinitesimal theorem at line 201 has the analogous assumptions. These are useful and noncircular conditional statements. They do not by themselves establish those hypotheses for representatives of every automorphism or every derivation of the quotient at depth 1689.

`Lattice/NearIdentity.lean` assumes concrete compatible integral endomorphisms E/C and the identity `embed (E a) = 1009 • C (embed a)`. It obtains power divisibility and a geometric inverse from that assumption. It does not construct such representatives from arbitrary finite automorphisms. The precise loss of two powers in the ell coordinates is retained, which is preferable to an unjustified replacement of the near-identity ideal by `p End(A)`.

### 2. Full exponential/logarithm equivalence

`Analytic/TensorAction.lean:90` proves `fixed_iff_derivation_of_factor`. Its parameters include Q, D, an already invertible tensor endomorphism U, and the equality

```
(action Q).toLinearMap - LinearMap.id = U * differential D
```

The resulting equivalence is a valid post-factorization argument if elaborated. But the source does not define the required exp/log maps, prove their inverse identities and integrality in the actual lattices, or produce this factorization for those maps. It therefore does not provide a bijection between **all** finite Lie automorphisms and **all** derivation solutions. A geometric inverse for `1 + F` in `NearIdentity` is not an exponential/logarithm correspondence.

### 3. Acceptance of the actual Smith certificate and actual kernel count

`Certificates/DerivationMatrix.lean` defines K from the actual bracket and connects its complete kernel to the derivation condition. This avoids counting only a selected family of derivations.

`Certificates/Elementary.lean:150–161` proves that a **generic** elementary circuit gives a kernel equivalence/cardinality equality **if** its checker returns true. Its operations validate invertibility, including rejecting a nonunit modulo 9 and rejecting a same-coordinate shear. However, there is no concrete circuit instance for the 14415-by-961 matrix with a Lean proof of acceptance of the supplied 931-pivot computation.

`Certificates/DiagonalKernel.lean:50` counts kernels of a **given diagonal system**, with valuation data supplied as a parameter. It does not prove that the actual K is equivalent to that diagonal system. `InnerScalarExtension.characteristic_zero_rank_upper` provides an upper-rank bound via independent inner derivations, but a rank bound alone cannot recover the p-adic invariant valuations or the desired finite kernel cardinality. No declaration instantiates these pieces to obtain the actual `1009^(30*i+1689)` count.

### 4. BCH group and recovery of all group automorphisms

`Finite/Nilpotency.lean` targets the relevant nilpotency bound for the explicit finite Lie ring. `BCH/Dynkin.lean` and `BCH/CoefficientSoundness.lean` develop Lie-word reconstruction and conditional coefficient soundness. The latter requires homogeneity, vanishing collected coefficients and an injectivity condition for multiplication by the degree.

These sources do not construct a finite BCH product or establish its associativity, identity and inverse laws. No concrete `Group` instance for the advertised BCH object is present. No theorem proves both directions of the correspondence between ordinary `MulAut` and the full Lie-ring automorphism set. Even proving that each Lie automorphism induces a group automorphism would only give one direction and would be insufficient for the desired equality.

`Finite/LieAutomorphisms.lean` is appropriately broader than a chosen automorphism subgroup: it relates the ordinary integer-linear Lie equivalence type, residue-ring-linear Lie equivalences, and all invertible bracket-preserving matrices. But its final theorem merely equates cardinalities of two descriptions of that same set; it supplies neither a numerical count nor a group/Lie correspondence.

## Trust and loophole review

No direct admission, custom axiom declaration, `native_decide`, `unsafe`, foreign proof implementation, or kernel-check bypass was found by the source search in the project mathematical modules. Increasing recursion/heartbeat limits does not itself add an axiom. This is a source observation, not a substitute for actual transitive `#print axioms` output after elaboration.

The visible conditional hypotheses are explicit rather than concealed as axioms. The main problem is missing instantiations and missing theorems, not a discovered attempt to make a false final theorem pass by changing `Aut` to a smaller set.

The runner `scripts/check.py` also explicitly distinguishes this status: default mode fails with `INCOMPLETE_FINAL_GROUP_THEOREM_ABSENT`; milestone mode can at most return `DRAFT_SOURCE_VALIDATION_PASSED_NOT_FINAL_GROUP_THEOREM`. Its hard-coded incomplete status should not be edited into a success flag merely because a library build succeeds. Printed types, dependency queries and selected module builds do not establish semantic completeness.

## Publication acceptance criteria

A complete-formalization claim requires all of the following in addition to clean builds:

1. An unconditional theorem producing the actual group and proving `ExactOrders`, followed by `NotebookAffirmative` (or equivalently explicit ordinary `MulAut` statements).
2. The four mathematical bridges above instantiated at the actual lattice, quotient, matrix and depth, with no result-sized hypotheses.
3. Actual elaborated statement inspection confirming the exact carrier, group law, Lie structure and ordinary automorphism type.
4. Transitive axiom reports permitting only the stated foundational Lean axioms and containing no admissions/custom problem axioms; reproducible full-target build and recheck records.

Until those criteria are met, publish a download, if desired, as **partial Lean development with an audit and an exact remaining-obligations list**. A successful repair of existing draft modules is meaningful progress, but must not be described as a kernel-verified full solution.
