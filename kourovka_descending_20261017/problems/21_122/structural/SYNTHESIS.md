# Structural family outcome for Kourovka21.122

**Outcome: unsolved.** The exact arbitrary-word, arbitrary-profinite-group implication

    |G_w|<continuum => G_w finite

has neither a proof nor a counterexample from this family. No statement about finiteness of w(w(G)), the closed verbal subgroup, or a restricted class is being promoted to the full set conclusion. Best guess completion toward the full discovery goal: **2%**.

## Strongest checked artifact

`CENTRAL_NONPOLYNOMIAL.md` constructs

    G=Heisenberg(Z3) semidirect_M Z3, M=[[10,3],[3,1]],

with G solvable of derived length exactly three. The derived word δ2 is central-valued, and its value set is exactly the central subgroup9Z3. However, δ2:G^4→Z3 is not a Passi-polynomial map of any finite degree. The all-degree proof uses the nonzero determinant

    det(B^d e1,C B^d e1)=(-9)^d(-3),

where C=M^-1 and B=C-I. A fresh independent reviewer accepted the exact proof hashac18f9ace801047954722adfd612ff4673ad01c00b13d2a59fd7571e88bd55ab and supplied a distinct affine-matrix verifier, an alternative scalar-recurrence proof, and the exact image simplification. See `central_countermodel_review/review_receipt.json`.

This falsifies only the **unconditional** extension of central-valued⇒polynomial from metabelian groups to arbitrary profinite groups. It does not refute a statement using the additional small-image hypothesis: that possibility remains unproved and is not contradicted by an example with continuum many values. The construction's priority has not been audited; no originality claim is made.

## Approach ledger

| Approach family | Mechanism/evidence | Status | Exact remaining gap |
|---|---|---|---|
|FC-centre and finite central quotient|Every small word-value is FC; prior iterated-verbal theorem; explicit compact normal FC-set in product S3|Partial constraints; generic FC shortcut disproved|Use actual word-map structure to prove finite [w(G),G], if true; compactness and FC-generation alone do not suffice|
|Verbal closedness/finite width|Closed abstract verbal subgroup iff finite width; small cardinal plus closedness gives finiteness; uniform finite quotient width would suffice|Exact conditional reduction|No arbitrary-word uniform width or abstract closedness theorem follows from the hypothesis|
|Marginality|Finite value set iff closed marginal subgroup is open; small image supplies one constant coset box|Exact target reformulation|Propagate one local coset identity to one global open marginal subgroup without equational Noetherianity or another new mechanism|
|Iterated verbal closure|Prior w(w(G)) finite; product D8 shows even central K with w(K)=1 may have continuum original values|Insufficient on its own|The actual small-image restriction must still force original set finiteness|
|Central-valued polynomial route|Reviewed Heisenberg-by-Z3 nonpolynomial δ2 countermodel|Unconditional shortcut **defeated**|A small-image-dependent central-word argument remains possible but unsupported; finite central reduction is also unproved generally|
|Central relation/cocycle transfer|Considered encoding central word values through central extension data|No checkable new bridge; **blocked**|No proof that countably many word values control all cocycle values or bound the associated relation-module width; arbitrary section data cannot simply inherit the word-image hypothesis|

`FC_WIDTH_AND_MARGINAL_ROUTES.md` supplies the proofs and carefully scoped countermodels for the first four rows. Their separate fresh audit is complete at100%, with no substantive objection, in `route_review/review_receipt.json`; none is a positive or negative solution of21.122.

## Countermodels distinguish the gaps precisely

The countable compact set of single-coordinate transpositions in product S3 is normal, consists of FC-elements with finite normal closures, and topologically generates a group with infinite derived subgroup. It is explicitly **not a word-value set**: every word-value set in that product is a product of identical finite factor images, hence is a singleton or has cardinality continuum.

For product D8 and either w=x² or w=[x,y], the word-value set is the central product C2^N and w(w(G))=1. Those values have cardinality continuum. They do not refute the target; they prevent dropping the small-image argument from an iterated-verbal reduction.

The Heisenberg-by-Z3 example likewise has exactly continuum many values, verified directly by δ2(a(r),t,b,t)=-9r for r∈Z3. No finite or countable word-image counterexample has been constructed here.

## Status and preservation

All work stays in this dedicated structural folder; no other original approach family's mathematics was used during discovery. No outside communication, git operation, paper, Zenodo upload, DOI, tracker update or human review occurred. Parent controls shared repository checkpoints and top-level problem status. This family has made substantial attempts through several distinct structural mechanisms and records their precise limitations rather than substituting an unsupported equivalent statement for a proof.
