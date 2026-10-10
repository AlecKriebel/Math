# Independent mathematical and source audit: problem 30001405

Date: 7 October 2026. Unrefereed independent audit. No novelty or priority claim.

## Verdict and exact scope

**ACCEPT the counterexample to the literal set-approximant formulation, and ACCEPT all three bridge lemmas under their stated smallness and saturation conventions. No mathematical correction to the frozen manuscript is required.**

The accepted conclusion is that the written hypotheses permit a definable two-class equivalence relation on a semialgebraic 2-sphere for which the second definable homotopy group is nonzero and the second ordinary homotopy group of the logic quotient is zero. The quotient map is discontinuous. The counterexample therefore does not address the strengthened continuous-projection or open-approximant formulations. Those variants remain unresolved **by this packet**. This is not an assertion that every relevant later theorem has been excluded.

The reviewed author manifest has SHA-256:

`10a8affedf81c5d559356b842c6d7216f88c1fb143d66dce667f62804b4d013b`

All eight entries in that manifest match their files. The public author directory contains precisely those eight files plus its manifest. The manuscript and primary sources were inspected directly; no previous independent audit was consulted. The author files were not edited. This review is source-free: scholarly PDFs, extracted source text, dataset records, and private coordination material are excluded.

## 1. Does the original problem actually admit this example?

The complete relevant OWR contribution was read, including its concluding reference on printed page 29, and its body on printed pages 27-28 was inspected in newly rendered PDF images. Its opening compactness and connectedness convention concerns definable **groups**. The subsequent general setting expressly allows a definable set X and a bounded type-definable equivalence relation E. The higher-homotopy conjecture strengthens the two displayed conditions by replacing simple connectedness with contractibility. No additional continuity or open-approximant condition appears in the contribution. Neither the definition of a type-definable set nor the logic topology supplies one implicitly. [OWR10]

The local corpus record agrees with that weak formulation. A discrete two-point space is locally contractible in every usual neighborhood-basis sense. Even importing second countability, local compactness, or Hausdorffness from the related preprint would not exclude this quotient. No convention in the inspected contribution requires the general quotient to be connected or every approximant to be a neighborhood. The sphere itself is definably connected and definably compact, so those properties of X would not eliminate the example either.

A countable decreasing family uses weak inclusion unless strictness is specified. Constant sequences satisfy this convention. More substantially, Bridge Lemma 1 proves that any countable decreasing definable presentation of a definable fiber stabilizes in the saturated setting. Requiring strict decrease indefinitely would exclude every definable fiber, rather than provide the ordinary meaning of the source's assumption.

**Source verdict:** the counterexample addresses the literal general assertion as written. The common mathematical intention, clarified by later open-approximant statements, is a separate scope and is preserved as such.

## 2. Ambient structure, definability, and boundedness

Take a sufficiently saturated elementary extension M of the pure ordered real field. This is an o-minimal expansion-of-a-field example, not a change of category. Finitely many parameters are permitted in each definable map; every countable type used in the argument is smaller than the saturation cardinal. Choosing that cardinal larger than the cardinality of the real field is adequate for the comparisons cited here.

Let X be x^2+y^2+z^2=1, with north and south poles N and S. The Boolean formula saying that two points either both equal N or both differ from N defines an equivalence relation. The two nonempty classes are A={N} and B=X minus {N}. Thus E is definable, hence type-definable, and its index is 2, which is bounded.

There is no need to assume topological closedness of E. Type-definability is a model-theoretic intersection condition, not topological closedness. Likewise, the order topology on M need not have the ordinary connectedness properties of the real line. The proof correctly uses **definable** connectedness where relevant and uses classical connectedness only for the ordinary real sphere downstairs.

## 3. Contractibility, with all denominator conditions

For r=u^2+v^2, the inverse stereographic chart is

Q(u,v) = (2u/(1+r), 2v/(1+r), (r-1)/(1+r)).

Because 1+r is strictly positive in every ordered field, this map is everywhere defined on M^2. The norm identity and 1-Q_z=2/(1+r) show that its image lies in B. Conversely, a point of X with z=1 has x=y=0, so every point of B has z different from 1. Therefore P(x,y,z)=(x/(1-z),y/(1-z)) is defined on precisely the needed domain. The inverse identities follow from x^2+y^2=1-z^2. Rational functions with nonzero denominators are continuous in the finite-dimensional order topology. Hence the charts are definable homeomorphisms.

An independent direct formula makes the contraction domain especially transparent. Put w=1-z, a=1-t, and D=w^2+a^2(x^2+y^2). On B, w is nonzero and D is strictly positive. Then

H(x,y,z,t) = (2axw/D, 2ayw/D, (a^2(x^2+y^2)-w^2)/D).

The numerator norm is D^2, while 1-H_z=2w^2/D is strictly positive. Thus H stays on the punctured sphere throughout. At t=0 it is the identity, at t=1 it is S, and it fixes S. This is exactly the author's conjugated linear contraction. The singleton A has its constant contraction. Consequently A_j=A and B_j=B give the required countable decreasing contractible definable presentations.

The independent script checks these rational identities, including the domain-sensitive north-pole exclusion identity. The inequalities ensuring denominator positivity are mathematical ordered-field arguments, not conclusions of symbolic cancellation.

## 4. Logic topology and the obstruction in degree 2

All four subsets of Y=X/E have definable inverse images: the empty set, A, B, and X. They are therefore logic-closed; their complements are also logic-closed. Y is exactly the discrete two-point space. It is compact, Hausdorff, second countable, locally contractible, and a finite polyhedron.

Fix the basepoint N upstairs and its class downstairs. For every positive n, any continuous based map from the ordinary real n-sphere into a discrete space is constant, because the domain is connected. Hence pi_n(Y,[N])=0 for n>0. Disconnectedness of Y causes no ambiguity: based homotopy groups are taken in the specified singleton component.

Upstairs, the based identity of the definable 2-sphere is an admissible representative of pi_2^def(X,N). This is the sphere definition of definable homotopy used in the comparison literature. If its class vanished, it would admit a definable continuous based nullhomotopy. Forgetting the basepoint condition would already give a forbidden ordinary contraction after transfer, so no delicate based-to-free homotopy implication is needed.

### First-order transfer is legitimate

Choose the single ordered-field graph formula defining that hypothetical homotopy, with a finite parameter tuple c. Its totality, uniqueness, target membership, and endpoint requirements are first-order conditions. Continuity is also first-order for this fixed formula. For each domain point p and epsilon>0, require a delta>0 such that all domain points p' with squared distance less than delta^2 have images whose squared distance is less than epsilon^2. The graph formula expresses the images. This is a finite formula over the ordered-field language, even if the graph formula itself has quantifiers.

Existentially quantify c. This does **not** transfer arbitrary original parameter values to the real field and does **not** quantify over functions. It asserts that this one fixed graph formula has some parameters making it a nullhomotopy. Completeness of real closed fields transfers that sentence to the real field, where it produces an actual continuous nullhomotopy of the real 2-sphere's identity. Pointwise epsilon-delta continuity is equivalent to the relevant relative product topology in both fields.

### The integral homology contradiction

Use integer coefficients. The boundary of a tetrahedron has four oriented triangular faces, six edges, and no 3-simplex. With faces ordered 012,013,023,123, its degree-2 kernel consists exactly of

(-d,d,-d,d), with d an integer.

The independent calculation solves the kernel equations, rather than relying only on a rational rank. The displayed vector is primitive, and its last coordinate is 1; hence rational proportionality to it forces an integral parameter for any integral chain. Since C_3 is zero, H_2 is an infinite cyclic group. The tetrahedral boundary realizes a real 2-sphere. The standard simplicial-to-singular identification and homotopy invariance imply that the identity and a constant map cannot be homotopic: their induced maps on H_2 are the identity and zero. Hatcher's Theorems 2.27 and 2.10, respectively, provide these foundational facts. [H02]

It follows that pi_2^def(X,N) is nonzero, whereas pi_2(Y,[N]) is zero. No coefficient system is being placed on the homotopy groups; integer coefficients occur solely in this homology obstruction. Computing the full upstairs group as Z is unnecessary for the refutation. The author's optional attribution of that computation to the closed bounded parameter-free semialgebraic comparison is consistent with the cited corollary.

## 5. The failure of continuity is genuine

The north-pole class is an open singleton in Y, but A is not relatively open in X. For s>0 the curve

c(s) = (2s/(1+s^2), 0, (1-s^2)/(1+s^2))

lies in B, begins at N when s=0, and has squared distance 4s^2/(1+s^2) from N. Given any positive neighborhood radius, a sufficiently small positive s belongs to that neighborhood. This is an ordered-field argument and does not presuppose sequential completeness or the Archimedean property. Thus q is discontinuous and B is not closed.

For clarity, the ordinary final topology of q has exactly the open sets empty, {B}, and Y. It is not the logic topology. There is no unsupported assumption that the usual quotient-map universal property applies to the logic quotient.

The exceptional fiber A cannot have an alternative countable decreasing presentation by definable relatively open sets: Bridge Lemma 1 would force one approximant to equal A. Similarly, B cannot have such a presentation by closed definable sets. Therefore the example is genuinely excluded by the relevant repairs, rather than merely using an inconvenient choice of approximants. Triangulability does not exclude it; Y already has that property.

## 6. Audit of the three bridge lemmas

### Lemma 1: stabilization

Accepted. If every D_j minus C were nonempty, the formulas expressing membership in each D_j together with nonmembership in definable C would form a small finitely satisfiable type. A finite subset is witnessed using the largest index present because the sets decrease. Saturation realizes the whole type, contradicting the definition of C. Thus some D_j=C, and weak decrease gives equality for every later index. Definability of C, smallness, and saturation are essential and correctly stated.

### Lemma 2: finite definable quotients

Accepted. Each class is definable with a chosen representative as a parameter, and any union of finitely many classes is definable. The logic topology is discrete. Continuity to a finite discrete space is equivalent to every class being open; if all classes are open, finite complements show that each is closed too. A definably connected X cannot be partitioned into two nonempty definable clopen pieces. Thus continuity forces the single-class case. No claim of ordinary connectedness of non-Archimedean X is needed.

The consequences for open approximants and for closed classes follow. They apply to finite definable partitions and do not purport to settle infinite quotients.

### Lemma 3: countable local bases

Accepted. For definable D, the saturation argument commuting an existential quantifier with a small downward-directed conjunction proves that the E-saturation of D is type-definable. Hence q(D) is logic-closed. Finite-conjunction closure of the formulas for E ensures finite satisfiability. The added point parameter causes no smallness problem.

Fix y and its decreasing presentation D_j. The sets U_j=Y minus q(X minus D_j) are open and contain y, because the whole fiber lies in each D_j. Their inverse images are contained in D_j. For any open V containing y, T=q^(-1)(Y minus V) is type-definable and disjoint from the fiber. If every D_j met T, their combined small type would be finitely satisfiable and realized by saturation, a contradiction. Thus some D_j lies in q^(-1)(V), implying U_j is contained in V. This is a valid countable neighborhood base.

The lemma proves first countability, not a countable global base or a triangulation. The review makes no claim that such stronger properties are impossible under additional hypotheses; only that they are not established by this argument.

## 7. Source versions and attribution

Four independently downloaded PDFs match the author's recorded bytes and SHA-256 values exactly: OWR10, BM09v2, AB17v1, and AB18. Their page counts and identifying version information were checked. The source metadata file records fresh retrieval details and the precise inspection scope.

The 2009 preprint's Assumption 4.1 lacks openness. The published 2011 Assumption 4.1(3) includes open approximants; its Theorem 4.4 includes continuity. This was independently checked in search-indexed primary-document text, with publisher publication/revision metadata checked separately. The full 2011 PDF remains unavailable through the tested links: the publisher returns 403 and the indexed document endpoint returns 404. No BM11 PDF hash or pixel inspection is claimed. This limitation does not affect the explicit counterexample. [BM09, BM11]

The accepted 2018 postprint identifies its final revision as 10 April 2018. Its Assumption 12.1 and Theorem 12.2 require both a triangulable quotient and decreasing contractible **open** approximants. Section 8 uses triangulable to mean a compact finite-polyhedron space. Proposition 3.4 supplies continuity from the open-approximant hypothesis. The comparison is pointed and yields positive-degree homotopy-group isomorphisms, also over open quotient subsets. Its Corollary 12.3 applies to the closed bounded parameter-free sphere. The corresponding 2017 version is distinct and is not used as a substitute for the accepted postprint. [AB17, AB18]

Nothing in this review proves that local contractibility plus the remaining strengthened hypotheses implies the required triangulability, or provides a replacement comparison construction. Merely adding continuity while allowing nonopen approximants is another distinct version. None of these variants is marked solved here.

## 8. Computation and integrity limits

- The frozen author's script completed successfully: all 20 checks passed, and both the parsed JSON and its exact stdout hash agree with the frozen results.
- The independent script completed successfully: all 30 checks passed. These include separately written direct-contraction identities, kernel equations over the integer-chain setting, finite equivalence-relation/topology combinatorics, and 75 supplemental exact rational witnesses.
- Both scripts use exact symbolic or rational arithmetic, not floating-point evidence.
- Neither script proves saturation, completeness of real closed fields, general continuity, or the foundational homology theorems. No formal proof checker or large exhaustive search was run.
- Local public dataset byte counts, SHA-256 values, the unique problem match, and absence of the exact two research-result keys were independently verified. Those are local checks, not certification of a fresh remote dataset download or of absent differently keyed research.
- The author's one-turn ledger is internally consistent with a single counterexample approach and subsequent bridge analysis. A mathematical/source audit cannot independently reconstruct all historical work merely from that ledger.
- Public files contain authored mathematics, public bibliographic/integrity metadata, and reproducible checks. Source documents and dataset contents are excluded. Hashes bind bytes and do not establish mathematical truth by themselves.

**Final acceptance:** literal formulation disproved in degree 2; bridge lemmas valid; no blocking proof defect; strengthened intended comparison not resolved by this work; no novelty claim.

## References

[OWR10] Alessandro Berarducci, joint work with Marcello Mamino, contribution in *Model Theory: Around Valued Fields and Dependent Theories*, Oberwolfach Report 01/2010, body pp. 27-28; final reference p. 29. https://doi.org/10.4171/owr/2010/01 . Official report: https://ems.press/content/serial-article-files/46259?nt=1 .

[BM09] Alessandro Berarducci and Marcello Mamino, *On the homotopy type of definable groups in an o-minimal structure*, arXiv:0905.1069v2, 30 November 2009. https://arxiv.org/abs/0905.1069v2 .

[BM11] Same title and authors, *Journal of the London Mathematical Society* 83(3) (2011), 563-586. https://doi.org/10.1112/jlms/jdq080 . Indexed primary document: https://citeseerx.ist.psu.edu/document?doi=5c5cf00ea6a3ab873d9b64164fd117e9a7e204bb&repid=rep1&type=pdf .

[AB17] Alessandro Achille and Alessandro Berarducci, *A Vietoris-Smale mapping theorem for the homotopy of hyperdefinable sets*, arXiv:1706.02094v1, 7 June 2017. https://arxiv.org/abs/1706.02094 .

[AB18] Same title and authors, *Selecta Mathematica* 24 (2018), 3445-3473. https://doi.org/10.1007/s00029-018-0413-3 . Accepted postprint: https://arpi.unipi.it/retrieve/e0d6c92a-cebc-fcf8-e053-d805fe0aa794/selecta-2nd-revision.pdf .

[H02] Allen Hatcher, *Algebraic Topology*, Chapter 2, Theorems 2.10 and 2.27. Author's chapter PDF: https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf .
