# Recovered author turn 5: local transitivity and the final construction gap

## Final route

Try to use the global assumption C(A) as a closure principle, instead of trying
to improve an arbitrary atomic presentation. The aim is to reach a graph or
structure coding the jump through finitely many admissible intermediate
interpretations, then collapse the chain using C(A).

Keep the types distinct. In the source, an arbitrary finite-signature structure
M can be weakly interpreted in an admissible A, and this is equivalent to
HF(M) <=_Sigma A. For an admissible B, B <=_Sigma A refers to B's **own**
Sigma predicates. Replacing it by HF(B) <=_Sigma A changes the problem.
The compact notation for J(A) must likewise be read with the source's chosen
admissible representative of its structural degree; the displayed predicate
expansion is not assumed to satisfy every expanded-language KPU scheme for free.

## 1. An exact closure reformulation

Write W(M,A) for atomic Delta interpretability of the structure M in the
admissible A. Use the two background representation facts explicitly stated
in the original OWR source:

    W(M,A) iff HF(M) <=_Sigma A;                            (R1)
    for every admissible B, B ==_Sigma HF(G_B)
    for some directed graph G_B.                          (R2)

These facts are credited inputs, not new representation theorems proved here.

**Proposition.** C(A) is equivalent to the following local transitivity rule:

    for every admissible B and every finite-signature structure M,
    W(B,A) and W(M,B) imply W(M,A).                        (LT)

**Proof.** Suppose C(A) holds. Its application to W(B,A) gives a strong
surjection from A onto B. Compose it with a weak interpretation of M in B.
Atomic pullbacks for the latter are Delta over B; the strong map pulls both
those predicates and their complements to Sigma over A. The composite is
therefore a weak interpretation of M in A, proving (LT).

Conversely, suppose (LT), and let B be admissible with W(B,A). Choose G_B by
(R2). The comparison HF(G_B) <=_Sigma B and (R1) imply W(G_B,B). Applying
(LT) gives W(G_B,A), hence HF(G_B) <=_Sigma A by (R1). Compose with
B <=_Sigma HF(G_B) from (R2), obtaining B <=_Sigma A. This is C(A). QED.

By induction, C(A) collapses any finite weak-interpretation chain starting in
A, provided each intermediate object used as the domain of the next weak
interpretation is admissible. The final object may be an arbitrary structure.
This is a consequence of (LT), not an existence theorem for a chain to the jump.

## 2. Attempt to build the required chain

The proposed first intermediate object was HF(A_as_structure). It is weakly
interpretable in A: by (R1), its ordinary finite coding carries no new
admissible information beyond the given structure's atomic presentation.
But its internal sets are finite. It does not contain a set of all its A-atoms
over which one could bound the universal witness search. This merely repeats
the finite-coding level and does not supply the jump at the next weak step.

Adjoining a formal element for all A-atoms would permit bounded witness tests,
but the resulting object is not automatically admissible. Bounded separation
would require further sets encoding the results of those tests. Neither
well-founded KPU closure nor a Delta(A) atomic presentation of that closure
was constructed. Calling that closure HYP(A) does not prove its weak
interpretability in A.

A compactness or Henkin argument gives no shortcut: it can introduce
ill-founded membership, while the intermediate B must be well-founded in the
source's sense. Treating an ill-founded structure as a *urelement structure*
and then taking its admissible cover changes the domain and again requires a
presentation theorem. The generalized HYP coding missing in turn 3 reappears
at precisely that point.

One cannot instead insert the jump predicate as an extra atomic relation: a
universal Sigma predicate supplies its positive instances, not the Delta
pullbacks of both signs required by W. Nor does the existence of a structural
jump fixed point in other models produce a fixed point for the prescribed A.

## 3. Final mathematical verdict

**NO FULL RESOLUTION.** The original converse remains unproved and unrefuted:

    If every admissible B weakly interpretable in A is strongly
    Sigma-reducible to A, must A absorb its structural jump?

The exact uncompleted construction in the final route is an admissible
intermediate B weakly interpretable in A, together with a further weak
interpretation of the chosen jump-coding structure in B. Such a construction
would permit (LT) to finish the argument. It is a sufficient route obligation,
not an asserted equivalent reformulation of the conjecture and not a theorem
supplied by compactness or the classical HYP example.

The complementary rich-admissible counterexample route also failed: the
small-target reductions do not verify C(A) for large targets, and no candidate
was shown both to satisfy C(A) and fail jump absorption.

## 4. Five-turn record and review gate

The recovered continuation now documents five substantive author turns:

1. Internal-cover lifting theorem, with the cover hypothesis exposed.
2. Bounded-truth criterion, presentation invariance and failed jump compression.
3. HYP relativization test; proof that exact covers need not exist even for any
   strongly reducing presentation, and the countable-target parameter barrier.
4. Internal-code/H_kappa route, including its large-target compatibility gap.
5. The local-transitivity reformulation and the failed admissible-chain
   construction recorded here.

The pre-interruption count is still unknown; it has not been reset or called
zero. Source retrieval, independent review, diagnostics, publication work and
private administrative work were not counted as additional author turns.
Only the first conditional lemma has received its separate PASS so far.
The later deductions require independent review before a partial-results PR.
No complete-conjecture or novelty claim is justified. No further proof-search
route is being taken after this five-turn continuation without new direction.
