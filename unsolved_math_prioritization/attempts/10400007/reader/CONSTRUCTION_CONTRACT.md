# Source-faithful acceptance contract: row 1786 / 10400007

**Edition note.** Historical source contract. For the current accepted theorem and qualifications, read [the reader](JONES_RESEARCH_READER.md) and [status and scope](STATUS_AND_SCOPE.md). The opening zero-pass status describes preparation of this contract, not the completed reader.

Prepared 14 October 2026 UTC. Source recovery and authored scope clarification only. **Zero mathematical passes; no proof, construction, computation, or resolution certificate.**

## 1. Exact target and nature of the question

J. Roberts's Problem 1.7 occurs on printed p385 / PDF13 of T. Ohtsuki (editor), [*Problems on invariants of knots and 3-manifolds*](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), GTM 4 (2002), pp377–572, DOI 10.2140/gtm.2002.4.377. The article itself was published 1 June 2004. In paraphrase, the source requests an intrinsic construction of the Jones polynomial through local-system homology.

This is a request for a mathematical construction with a topological interpretation. It is not a yes/no assertion about a pre-specified family of groups, or a problem whose complete model can be reconstructed from the truncated queue title alone.

The short question does not formally define intrinsic. Its adjacent remark contrasts the Alexander polynomial's complement interpretation with Bigelow's existing braid/plait model. Roberts's preceding discussion at printed p383 / PDF11 explains intrinsic in ambient-three-dimensional terms. These passages are the interpretive anchors. Any stricter categorical or functorial formulation adopted for an attempt must be labelled as an authored acceptance formulation, not a verbatim condition hidden in the original.

## 2. Domain and quantifiers

The contextual minimum is a general construction valid for ordinary knots K in oriented S^3, with no alternating, fibered, hyperbolic, torus, low-crossing or bounded-braid restriction. The surrounding Section 1.1 defines the Jones polynomial for oriented links, but the immediate Problem 1.7 remark repeatedly discusses a knot and its complement. Therefore:

- A proposed answer must state whether it covers all knots or all oriented links.
- A knot-only result must not silently be advertised as a link theorem.
- Do not demand an arbitrary-3-manifold extension as part of this row. The neighboring discussion explicitly distinguishes that situation.
- Any treatment of tame/smooth category, orientation, peripheral marking, complement versus compact exterior, or extra framing must be explicit. The short problem does not prescribe all of these choices; preserve the standard knot-theoretic ambient setting rather than infer a theorem about arbitrary topological wild embeddings.

The task is not satisfied by constructing a space or coefficient system separately after looking up a knot's already-known Jones polynomial. The proposed rule must genuinely explain the polynomial from the topology and its homological data. This is an anti-circularity acceptance requirement, not a new mathematical theorem.

## 3. Polynomial normalization

Use Section 1.1, printed p380 / PDF8:

- V_unknot(t) = 1.
- t^(-1) V_(L+)(t) − t V_(L−)(t) = (t^(1/2) − t^(-1/2)) V_(L0)(t).
- V_K belongs to Z[t,t^(-1)] for knots; the source's oriented-link polynomial belongs to Z[t^(1/2),t^(-1/2)].

A full construction must recover the entire polynomial with a stated equality in the proper coefficient ring, not merely one special value, a few finite-type coefficients, a formal asymptotic expansion without a proven reconstruction, or a different invariant. Colored Jones polynomials are not required, although a valid colored construction may include the target specialization. Explicitly reconcile reduced/unreduced, variable, writhe/framing and mirror conventions before asserting equality. In particular, the latest Anghel–Juhász Theorem 1.13 recovers V of the **mirror knot** under their stated normalization; extracted text can omit its overbar.

## 4. Intrinsic and local-system requirements

A source-faithful successful proposal must specify its topological input and output and explain why orientation-preserving diffeomorphisms of the ambient knot pair transport the construction naturally. The important extra work is to account for the topology before making an arbitrary projection or choosing a braid/plat presentation. If auxiliary choices are used to compute an already intrinsic object, show what the object is and why they compute it. Merely checking that a known presentation formula has the same value under moves does not, by itself, supply the extra interpretation requested by Roberts.

Specify the spaces, coefficient ring, local systems/monodromy, homology theory and degree(s), any relative/locally-finite support conditions, classes or pairings, and the operation producing the polynomial. Prove the claimed definitions and independence/naturality under the advertised scope. A homological label attached to a combinatorial sum is not a substitute for this data.

The source gives configuration spaces of n points in the knot complement as an example of a possible direct construction. It does **not** mandate that route, choose ordered versus unordered configurations, require a fixed n uniform over all knots, restrict to rank-one systems, require ordinary rather than relative/Borel–Moore homology, or insist on an Euler characteristic rather than a pairing. Do not impose these extra restrictions without stating that they define a narrower attempted subproblem. Do not transplant Bigelow's punctured-disc model unchanged and call its disc the knot complement.

This recovery does not assert that a completely choice-free literal chain complex is necessary, or that every use of a Heegaard diagram, braid or triangulation automatically disqualifies a result. The question is whether a genuine intrinsic three-dimensional local-system construction and its transport under changes have been supplied, beyond the already known scalar invariant.

## 5. Prior-work and acceptance gates

1. **Bigelow is baseline, not a new resolution.** Reference [55] is explicitly cited by the original remark. Its Theorem 2.8 gives the plat-closure Jones polynomial from a covering-space intersection pairing. The author's own introduction flags the special-form/move-check limitation. A reproduction of that theorem alone does not answer the additional request.
2. **Categorification alone is insufficient.** Khovanov homology is already discussed in the original source, pp388–389. Symplectic/Floer categorifications or a spectral sequence may be highly relevant, but they need a precise bridge to the intrinsic local-system construction sought here. Conversely, the problem does not require categorification as an extra output.
3. **Read intrinsic in context.** Anghel 2022's fixed homology classes and Anghel 2025's homological proof are described using intrinsic language, while their inspected models use punctured-disc braid actions. Anghel 2025 explicitly separates the knot-complement interpretation. A title, adjective, abstract or keyword match is not an exact-resolution certificate.
4. **Use current manuscript versions.** Anghel–Juhász arXiv:2601.08805v4, dated 7 September 2026, is titled *Quantum braid Floer homology*. It gives a braid invariant, not a knot invariant before specialization; §9.2 records Markov noninvariance. This fact does not invalidate the Jones specialization and does not prove that Roberts's problem is impossible. The January title and old formula must not silently replace v4.
5. **A positive answer needs a complete bridge.** State a source-faithful general construction, define all needed data, establish naturality and well-definedness, prove exact Jones agreement, and distinguish genuinely new content from earlier constructions. A claim of prior resolution needs an authenticated primary theorem matching these obligations.
6. **A negative statement needs a bounded target.** The original leaves broad freedom in what local-system construction is allowed. An obstruction for one rank, one configuration family or one coefficient system is only an obstruction to that specified approach, not a proof that no intrinsic construction exists.

## 6. Historical scope and current reading

This acceptance contract predates the mathematical construction. It establishes the question and its quantifiers, rather than certifying a solution. The current reader supplies a later accepted construction within the documented broad source-supported class, while continuing to disclaim historical recognition and novelty. Its ordinary degree-zero homology is on surface Teichmüller spaces. The knot-exterior state and label-1 filling are defined geometrically before the comparison proof; the result covers knots, without claiming a full link theorem.

This public edition paraphrases the original problem sentence and omits ancillary research-record and work-routing references. Its original and public byte identities are recorded separately. It includes no copied source documents or dataset contents.
