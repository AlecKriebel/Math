# Kourovka 21.122: research outcome

UTC checkpoint: 2026-10-24T23:36:00.374197+00:00. **Outcome: unsolved. Discovery estimate: 5%.**
Three independent original research families attempted the full question. None
produced a complete proof or an ordinary-word counterexample. This is an account
of checked deductions and precise failed routes, without an originality claim.

## Exact unresolved target

For every ordinary finite-arity group word w and every profinite group G,
prove that the set G_w is finite whenever its cardinality is below continuum,
or construct an explicit counterexample. The question imposes no generation,
rank, solubility, metrizability or pro-p assumption. A conclusion about the
closed verbal subgroup, an iterated verbal subgroup or a restricted class
cannot replace this set-cardinality conclusion.

The latest official 21st Notebook, October20 revision, p197, attributes the
problem to P.Shumyatsky. The primary and independent source audits found no
complete prior resolution in their bounded coverage. Their access limits and
precise known positive classes remain in priority/. In particular, all-word
results for metabelian, virtually nilpotent, dense-equationally-Noetherian and
FC-generated groups are credited prior work, not new solutions here.

## Supporting deductions and constructions

1. **Exact reduction of the full question.** Any hypothetical infinite small
   word image descends to a countably infinite word image in a metrizable
   profinite quotient. Selected values survive countably many separating
   finite quotients; compact metric perfect-set theory supplies countability
   without CH. For a surjective finite-group inverse sequence the word image
   is exactly the inverse limit of the finite word images, by compact tuple
   lifting. Uniform boundedness of those finite images is equivalent to
   finiteness of the limit image. Two independent reviewers checked these
   proofs. The original source contract's overbroad cardinal warning is
   explicitly corrected in priority/SOURCE_SCOPE_ADDENDUM.md.

2. **Topology alone cannot close the reduction.** The first-nonzero-coordinate
   map on the product of countably many C2 groups is continuous, densely
   locally constant, conjugacy equivariant and compatible with integer
   powers. Its countably infinite compact image is a convergent sequence.
   It is not a word map: it fails additivity and coordinate-swap naturality.
   This defeats a generic compactness or thin-tree fusion proof, rather than
   the original group-word assertion.

3. **Abelian extraction is false.** A class-two profinite group constructed
   from V=product Z/p^2 and a bilinear central cocycle has p-power image pV
   of cardinality continuum, for every odd prime p. Commuting inputs have
   proportional reductions modulo p, so every abstract abelian subgroup has
   at most p power values. Thus infinite word variation need not occur on
   an abelian source subgroup. A fresh nonauthor reviewer checked the
   infinite construction and separate finite models; the even-prime boundary
   correctly fails the displayed simplified power formula.

4. **Centrality does not give unconditional polynomiality.** The pro-3 group
   Heisenberg(Z3) semidirect Z3, with action matrix [[10,3],[3,1]], has a
   central-valued derived word delta2 whose image is exactly 9Z3. Its Passi
   differences have no finite degree bound, by an all-degree determinant
   argument, independently checked with affine matrices and a second
   recurrence proof. It has continuum many values. It refutes only an
   unconditional extension of the metabelian polynomial argument; a theorem
   crucially using the small-image hypothesis remains possible and unproved.

5. **Structural reductions retain their missing hypotheses.** Finite values
   are equivalent to an open full marginal subgroup. Closedness of the
   abstract verbal subgroup is equivalent to one finite word-width bound;
   under the small-image hypothesis either would imply finiteness. A common
   finite width in all finite quotients is essential. A compact countable
   normal FC-set in product S3 generates a group with infinite derived
   subgroup; that set is not a word-value set. Product D8 has central square
   and commutator images of continuum size despite trivial iterated verbal
   subgroup. Both examples prevent dropping the actual small-image step.
   These deductions and countermodels passed a separate fresh audit.

6. **Construction restrictions.** Word images in full fiber products of finite
   groups over one fixed finite common quotient have the dichotomy: finitely
   many quotient-input fibers are Cartesian products of finite sets. The
   empty index case is treated separately, and activity means more than one
   possible value, not a deterministic nonidentity output. Shumyatsky's
   prior finite-iterated-verbal theorem forces every hypothetical nontrivial
   counterexample to satisfy an explicit nontrivial group law. A direct
   rigid-stabilizer argument also excludes profinite weakly branch groups.
   Central extensions leave an exact central word-cocycle realization gap;
   arbitrary continuous central maps cannot be substituted. Fresh primary and secondary constructive-family reviews passed; the
   exact accepted scope is recorded in FINAL_PARTIAL_ACCEPTANCE.json.

## Exact gaps and reopening conditions

The topological route needs a fixed-word algebraic mechanism excluding a
countable thin inverse tree of values. Merely restating that property transfers
the central difficulty. The structural route needs a justified uniform width,
a global open marginal subgroup, or a central reduction and an argument that
uses the small-image hypothesis. A local constant coset box is insufficient.
The construction route needs compatible genuine group-word cocycles with a
countably infinite compact joint image; independent coordinates restore
continuum. Neither such a construction nor a theorem excluding it was found.

All three families have terminal mechanism ledgers. Reopen a blocked route
only for a materially new mechanism or evidence. This record does not prove
that the problem is intractable or globally open forever; it records the
substantial unsuccessful attempts in this effort.

## Verification and publication boundary

The root read the supporting proofs and their fresh adversarial reviews.
All five supporting packages passed fresh nonauthor review, with secondary
reviews of the quotient and law/branch arguments. Ninety-two current reviewed-file
hash checks and twelve root computation reproductions pass; frozen author and
reviewer files are unchanged. FINAL_PARTIAL_ACCEPTANCE.json records the exact
proof and receipt hashes.
Finite computations test explicit constructions and boundary cases; infinite
claims depend on the displayed proofs. No check covers the universal open
step, and no novelty audit for these partial constructions has been completed.

No complete result, solved_verified status, preprint, release, Zenodo upload,
DOI, tracker row or independent human review is claimed for21.122. Publication
remains closed. The next descending candidate is21.121(b); part(a) has a prior
recorded negative solution and is excluded from original discovery.
