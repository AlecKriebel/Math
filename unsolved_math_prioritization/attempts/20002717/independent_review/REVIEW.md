# Independent source-scope review: rank 424 / problem 20002717

Date: 2026-10-03 UTC. Reviewed frozen `SOURCE_GATE.md` SHA-256 `86a0249b8dd9f425225feb0f0508232a5b8ba219ec02bc69ddd3fcbd0ce7001d`.

## Decision

**PASS — CREDITED SOURCE RESOLUTION AT THE EXPLICIT EXISTENTIAL NATURAL-CLASS SCOPE.** Recommend `already_solved` only with this scope qualification and the supplied prior-work credit. No novel result, no author research turn: **0/5**. No remote modification or PR was made.

The packet collectively supplies (i) natural sufficient conditions, (ii) a mathematically substantial natural class with an exact lattice/nonlattice criterion, and (iii) a natural class with an entirely algebraic/word-metric proof. Thus it answers each explicit request in the source. Gobet's proof alone does **not** supply item (iii); the credited imported product proof does.

This is an audit judgment about coverage of an open-ended workshop prompt. It is not a claim that the cited authors explicitly declared McCammond's Problem 4.3 completely solved, nor that the general interval-lattice research program is finished. The imported report's `partial_result` label is preserved as historical provenance; its stronger proposed next problems are not silently promoted to requirements of the original source.

## 1. Source boundary and the representation remark

The primary workshop PDF identifies McCammond's Problem 4.3 on printed page 9, followed by its remark on page 10. Its hypotheses are a group and a finite conjugacy-closed generating set. It asks for sufficient natural conditions and an explanatory natural class. The remark contrasts a reflection-representation proof with a possible group-structural explanation in a class of quasi-Garside structures. [Primary source, pp. 9–10](https://aimath.org/WWN/braidgroups/braidgroups.pdf).

There are three distinct propositions that must not be conflated:

1. An interval admits a criterion expressed through the marked group's algebraic data.
2. Such a criterion has a proof avoiding linear/reflection representations.
3. The interval's lattice property is independent of the generating set on an unmarked abstract group.

The source context supports questions (1) and (2), existentially over a natural class. It does not require (3), a universal classification of marked groups, or a representation-free proof for all Coxeter noncrossing intervals. A source-specific proof obligation for the entire Coxeter family would need to be added explicitly before treating it as unfinished work.

The source's generating set is not explicitly required to be inverse-closed. The audited families deliberately have inverse-closed sets. This restriction is legitimate when furnishing sufficient conditions or an existential class. It would be insufficient for a purported classification of every source-allowed generating set, which is not claimed.

## 2. Which evidence answers which request?

### Natural sufficient conditions, all endpoints

The imported theorem covers

G = F × C(n1) × ... × C(nd),

where F is any finite group and each cyclic factor is finite or infinite. Its generating set is all nonidentity elements of F, embedded in that factor, together with the positive and negative generator in each cyclic coordinate. There are finitely many factors. This is a finite, symmetric, generating, conjugacy-closed set. Conjugation preserves the entire nonidentity F-part and fixes the cyclic-coordinate elements.

The proof is algebraic and genuinely all-endpoint: a word must spend at least the factor distance in letters assigned to each factor, and concatenating shortest factor words attains their sum. Equality in the sum of factor triangle inequalities is equivalent to equality in every coordinate. The same argument for two elements proves the order isomorphism, not merely a bijection of interval vertices.

Each finite-factor interval is a singleton or a two-element chain. A cyclic interval is a shortest-arc chain, except that an even antipode has two chains joined at bottom and top. Internal elements on different arms have bottom as meet and top as join. Products preserve these operations coordinatewise. Identity endpoints and order-two cyclic factors are correctly covered. Translation reduces arbitrary Cayley intervals to principal intervals.

No reflection representation enters this argument. The chosen product decomposition and marking remain part of the algebraic data. This is an explicit natural, nontrivial class answering even the proof-sensitive interpretation of the remark. It is credited to the imported report, not to this audit. No novelty claim survives the gate.

### An explanatory class containing both outcomes

Gobet's finite-Coxeter involution family supplies a substantive iff criterion: the interval below an involution u is a lattice exactly when the involutive parabolic subgroups of P(u) are intersection-closed. Proposition 3.10 identifies the two posets. Corollary 4.3 gives allowed irreducible factors A1, I2(2k) (k ≥ 2), Bn (n ≥ 3), D4, H3. D4 and D6 central-longest intervals give positive and negative controls. The finite restriction keeps T finite. The broader corollary also handles arbitrary Coxeter groups via finite involutive parabolic closure, but this broader ambient scope is unnecessary here. The proof uses Carter's lemma and moved/fixed spaces: it is not representation-free. [Gobet, §§2–4](https://arxiv.org/html/2507.11340v1).

This criterion concerns a Coxeter system, its reflections, and parabolic structure. It does not concern the abstract group with that structure forgotten. This restriction is explicit rather than a hidden change of hypotheses.

### Marking dependence and a proved obstruction

For the same group Z² and same endpoint (3,0), the axial generating set yields the four-vertex chain. Adding the four diagonal directions yields the eight king moves, still finite, symmetric and conjugacy-closed. The latter word length is max(|p|,|q|): each move changes either coordinate by at most one, and diagonal moves followed by axial moves attain that bound.

The interval condition is

max(|p|,|q|) + max(|3-p|,|q|) = 3.

It forces 0 ≤ p ≤ 3 and |q| ≤ min(p,3-p). Thus the four ranks contain 1, 3, 3, 1 vertices. The atoms (1,0), (1,1) have exactly two minimal upper bounds (2,0), (2,1). The latter pair has exactly the former two maximal lower bounds. Equal-rank distinct bounds cannot be comparable; consequently the join and meet fail. This is a proof, independently replayed by computation.

Therefore even abelianness, torsion-freeness, and conjugacy closure together do not ensure the lattice property. In particular, a generating-set-independent conclusion for arbitrary T is false. This negative result clarifies the meaning of “group structure”; it does not invalidate an algebraic explanation for a specified natural marking.

## 3. Literature scope checks

- **BHNR final theorem:** Theorem 2.12 is about quasi-Coxeter endpoints in finite Coxeter groups. For the stated simply-laced types and F4 it selects Coxeter elements; H3 is positive; H4 also admits proper quasi-Coxeter endpoints of order 30. The H4 exception is present in the final publication. Do not replace this with an old “Coxeter or H3” summary. This is not a theorem about every endpoint of W. Theorem 2.16 separately supplies the balanced-lattice Garside construction. [Final BHNR paper](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/tlm3.12057).
- **Chavli–Gobet:** Theorem 1.1 restates the involution classification; its main purpose is identifying the resulting interval groups. Theorem 2.4 explicitly records the general finite balanced-lattice mechanism. It corroborates the framework and is not needed to create a new solution. [July 2026 preprint](https://arxiv.org/abs/2607.21510).
- **Gobet September 2026:** This paper studies intervals below Coxeter elements, introduces absolute moved spaces in the geometric representation, proves injectivity, supplies a rank-three lattice proof, and gives new infinite rank-four nonlattice families. Its introduction retains unresolved cases beyond finite, affine, universal, and rank-three settings. Its infinite reflection sets do not automatically satisfy the original finite-T requirement. These limitations constrain broad completion claims, but do not defeat an existential natural-class answer. [September 29, 2026 preprint](https://arxiv.org/abs/2609.37867).

There is no contradiction between the positive D4 involution interval and BHNR's negative proper quasi-Coxeter cases: the hypotheses impose different endpoint classes. Neither citation was used to infer that every finite-Coxeter interval is a lattice.

The Gobet theorem text was checked in the primary arXiv reading copy. Journal metadata was independently confirmed on the [author's publication list](https://gobet.perso.math.cnrs.fr/); the publisher page fetch failed. No claim is made that its final publisher text was independently inspected.

## 4. Exact replay and independently written controls

All seven files listed in the frozen packet manifest match their SHA-256 values. The packet verifier ran unchanged and its parsed output exactly equals the frozen `VERIFICATION.json`: 24,328 assertions, 462 positive S3 × Cn intervals (2 ≤ n ≤ 12), and the complete king obstruction.

The separately written checker uses a different finite nonabelian factor and separately constructs geodesic orders:

- All 192 endpoints of Q8 × C4 × C6 with the prescribed product marking give lattices, including products of antipodal factors.
- All four C2 × C2 endpoints cover order-two degeneracy.
- All 61 axial Z² endpoints of length at most five give lattices.
- The same-group, same-endpoint axial/king comparison confirms marking dependence and the exact imported join/meet obstruction.
- Signed-permutation Cayley BFS controls give |D4| = 192, |T| = 12, with a 44-vertex central-longest lattice; |D6| = 23,040, |T| = 30, with a 752-vertex central-longest nonlattice. The output records an actual missing-join pair.

The independent checker tests existence of actual least/greatest bounds, not just the number of bounds of minimum/maximum rank. It runs 271 explicit assertions. These are controls of credited claims, not general proofs or author turns. The signed-permutation controls are not offered as a representation-free proof of Gobet's classification.

## 5. Remaining target and disposition precision

**No additional mathematical obligation remains under the source's explicit existential natural-class request.** Close as credited source resolution, retain 0/5, and do not begin a speculative research turn merely to satisfy the imported report's suggested extensions.

If an owner deliberately chooses a stronger representation-free Coxeter task, a precise separate target would be:

> For a finite Coxeter system (W,S), its full reflection set T, and u² = 1, prove directly from Coxeter/group and parabolic-subgroup data that [1,u]T is a lattice iff the involutive parabolic subgroups of P(u) are closed under intersection, without invoking a linear reflection representation, fixed/moved spaces, or geometric Carter-lemma arguments.

The reviewed packet does not discharge that strengthened proof target. It is not an unfulfilled explicit requirement of Problem 4.3, and this review does not assert that it is new or open in all literature. It would require a fresh targeted prior-work gate before research. A classification of all markings of Z² or of arbitrary marked groups is even stronger and should not be substituted.

## 6. Audit limitations and credit

The primary AIM source was independently read through page-aware text; no visual screenshot verification is claimed. Five local primary-paper PDFs match the packet's recorded hashes. The imported report was inspected in full, including its elementary proofs and historical partial-result label. The complete corpus download hashes and exhaustive live-branch claims were not independently re-executed in this scope review; they remain the original packet's documented provenance checks.

All published results remain credited to their authors. The product theorem and exact king example remain credited to the imported UnsolvedMath third-party AI report, with low/undetermined novelty and no attribution to the user's author turns. No source file, original packet record, repository status, branch, commit, PR, release, DOI, or external message was changed.
