# Independent mathematical audit: universal transverse surgery

Problem 10300034 / AMR-102-0034, queue rank 1005. Inspection date: 2026-10-08 UTC.

## Verdict

**Accept the unchanged frozen author packet as five substantive, unsuccessful approach families, with the stated partial results. The original problem remains unsolved by this packet. No mathematical correction is required.**

This is a complete review of the arguments supplied in PROOF.md, not an endorsement based only on successful scripts. Every proposition, the corollary, the source-dependent scope statements, and the final quantifier claim were checked. The elementary mathematical statements are valid in the stated closed, connected, oriented setting and under their additional stated hypotheses. The review does not establish historical novelty, comprehensive literature status, or a formal proof.

The authenticated author archive has 24,236 bytes and SHA-256 533268c19efeb1e024777bfca36afbb20ee4e9ee09ab0fd01c7d3fc0bfed8564. Its 13 members agree byte-for-byte with the supplied frozen tree. PROOF.md has 18,562 bytes and SHA-256 c04d615722f2f2498eaeaff86f21cc7b0d5dd0cd8e1e96c324b16fb7413f57e3. All original author bytes were preserved.

## 1. Target and category

The target has the quantifier order: there exists one fixed output manifold M such that every admissible pair (N,F) admits some finite transverse link and some filling slopes giving M. A link, its component count, and its slopes can depend on both N and F. No continuation of F across the filling is stipulated. The separate common-exterior variation is not substituted for this target. The statement and adjacent context were checked at Question 9.1 of [C02].

The author's chosen closed, connected, oriented category is explicit. Smoothness and coorientation are imposed when used, rather than claimed to follow from the displayed problem statement. All obstruction examples lie in a legitimate smooth cooriented subclass. The audit does not use omitted category conventions to manufacture a negative solution.

The meridian-longitude notation presupposes solid-torus link neighborhoods. This is automatic in the oriented setting. Proposition 2's broad wording must be read within this declared setting, or, more generally, for links whose neighborhoods are solid tori; it is not a construction of Dehn slopes on one-sided knots in nonorientable manifolds. No extension of the conclusion to that unrelated situation is needed.

## 2. Approach I: transverse isotopy

### Proposition 1: accepted

For a regular parametrization of an oriented circle, positive transversality means alpha(gamma') is strictly positive at every parameter. Its integral is strictly positive by continuity and compactness. A transverse connected circle has a nonzero continuous evaluation, so its sign cannot change. Reversing orientation changes the integral's sign.

Closedness of alpha, not merely its nonvanishing, is what makes the period invariant under homology and hence isotopy. Therefore a zero-period knot cannot become transverse by isotopy, even if its orientation is reversed. A null-homologous knot is covered, including a knot in a small ball. There is no converse claim that every positive-period class or knot is transverse.

For Sigma_g times S1, dt is a globally defined closed form even though t itself is circle-valued. Vertical circles meet every fiber, proving the tautness required for the example. Knots in a fiber have period zero. Thus the asserted unrestricted transverse-isotopy lemma fails within the intended category.

This does not obstruct alternative surgery diagrams related by changes other than isotopy. In particular it does not show that a given N lacks a transverse link with a prescribed filling output. The use of ordinary surgery duality supplies no missing transversality theorem. The limited Lickorish credit is appropriate; see Section 7.

## 3. Approach II: group and homology

### Proposition 2: accepted, with the epimorphism in the stated direction

Let H be the fundamental group of the exterior. Let U be the normal closure of its peripheral meridians and V the normal closure of all meridians and longitudes. The original manifold has group H/U. The further quotient by the component classes is H/V, because each longitude becomes its component's core class after the original filling. Basepoint choices only conjugate these elements.

For any primitive filling slope, its image in H is a product of powers of the meridian and longitude. Those two peripheral elements commute, since they come from a torus, even when the peripheral homomorphism is not injective. The normal closure S of the filling slopes is contained in V. The quotient map is consequently H/S onto H/V, giving pi1(M) onto pi1(N)/normal(L). The converse direction is not justified and is generally false.

Van Kampen supplies the filling quotient without requiring an incompressible boundary torus or a nontrivial meridian. Abelianization gives the integral epimorphism. Tensoring with the rationals is right exact, and quotienting the rational first homology by the span of the component classes removes exactly d dimensions. Thus b1(M) is at least b1(N)-d, and d is at most the number r of components. Possible torsion, a zero component class, redundant classes, and an empty link cause no exception. The empty-link case reduces to equality.

The argument is valid for rational Dehn slopes represented by primitive integral pairs, not just integer surgery coefficients. Changing longitude by a meridian multiple does not affect its image in the original group or the common quotient. Reversing a slope changes neither its normal closure nor the filling.

### Corollary 2A: accepted

The rational first homology of Sigma_g times S1 has dimension 2g+1. Since every fixed closed M has a finite first Betti number, the bound r >= 2g+1-b1(M) tends to infinity with g. This disproves a strengthening that imposes a common finite component bound. It does not contradict the original allowance of an arbitrary finite number for each input. A nonpositive lower bound at small genus imposes no restriction and is not interpreted as a negative component count.

### Proposition 3: accepted

A section s maps to (gamma(s),s). The circle projection is the identity, so the section is embedded and positively transverse regardless of self-intersections of gamma in the surface. To separate finitely many sections, regard their surface-coordinate loops as a map from S1 to the finite product of copies of Sigma_g. Each pairwise coincidence diagonal has codimension two. A simultaneous arbitrarily small generic perturbation of this one-dimensional map avoids every such diagonal. It preserves each free homotopy class and the identity circle projection. Thus the representatives can indeed be disjoint while retaining degree one.

This argument does not require all loops to share a fixed basepoint after perturbation. Based component elements are conjugates of the indicated free homotopy classes, which is sufficient for a normal closure. Killing t and the elements a_i t and b_i t kills all the surface generators. Their surface relation and the centrality relations create no obstacle: the quotient has every generator trivial.

In integral homology the columns are t and each surface generator plus t. Subtracting the first column from the others produces the usual basis. This proves an integral basis, stronger than rational independence, for every g >= 1. The case g=1 uses the same argument; the unused g=0 case would also admit the single t section.

Neither a trivial common quotient nor an integral basis proves that some slopes yield S3 or a universal M. The packet expressly does not make that sufficiency claim. The algebraic method supplies a necessary condition whose obstruction can disappear.

## 4. Approach III: original fiber class

### Proposition 4 and the punctured-bundle description: accepted

Orient each transverse component so f restricted to it is locally orientation preserving. A local diffeomorphism of compact circles is a finite covering; its degree d_i is a strictly positive integer, and need not equal one. On the exterior the integral fiber class evaluates to zero on every meridian and to d_i on its longitude. These facts are invariant under a longitude-framing change.

For a connected space, integral H1-cohomology is Hom(pi1,Z). A homomorphism on the exterior extends across the attached solid tori if and only if it kills the filling relations. Consequently the necessary and sufficient condition is q_i d_i=0 over the integers for every component. Since each d_i is positive, q_i must vanish. Primitivity then forces p_i=+1 or -1. These are exactly the unoriented meridional slopes, and these fillings recover the original manifold and class.

No extra divisibility condition arises: once a primitive slope is killed, the map on the peripheral group factors through the infinite cyclic group of that solid torus. Integral coefficients matter here; reducing the evaluations modulo an integer would invalidate the reasoning. Likewise a degree-zero component would defeat the meridional-only conclusion, but the transverse hypothesis excludes it.

Small disk neighborhoods of the moving finite point set in each fiber can be transported around the base circle. Allowing the disks to be permuted handles degrees greater than one. Removing their union gives a punctured-surface bundle with total puncture count sum d_i. This construction is compatible with disjoint tubular neighborhoods.

The conclusion concerns precisely the restriction of the original class. A nonmeridional filling may have another fibration, another foliation, or neither. Merely showing that this restricted class fails to extend is not an obstruction authorized by the original question.

## 5. Approach IV: contact approximation

### Proposition 5 and the strict transfer criterion: accepted

Writing c=cos(2*pi*t) and s=sin(2*pi*t), differentiation gives d beta = -2*pi*epsilon*s dt wedge dx + 2*pi*epsilon*c dt wedge dy. The exterior product has coefficient -2*pi*epsilon squared times (c squared+s squared) relative to dx wedge dy wedge dt. Its sign is negative for every positive epsilon; flipping the sine term flips the sign. Thus both contact-sign versions of the example are available.

The coefficient of dt stays one, so beta is nonzero. Its other coefficients tend uniformly to zero, giving uniform convergence of the cooriented kernels to ker(dt). On the fixed x-circle at y=t=0 the evaluation is epsilon, whereas dt evaluates to zero. The period obstruction proves the stronger claim that no isotopic representative is foliation-transverse. The fiber foliation on this torus has torus leaves; it is not the foliation-by-planes exception in Bowden's displayed theorem.

For a fixed metric and a unit tangent v, the dual norm bounds the evaluation error by the norm of alpha-beta. A lower contact evaluation margin strictly exceeding that norm implies positive evaluation by alpha. In the example, using the natural flat metric, both the margin on the knot and the error norm are epsilon. The equality case correctly gives zero, not strict positivity. At epsilon=0 the form is not contact, and the proposition does not include it.

This refutes a universal transfer of contact-transverse knot types from an arbitrarily close contact structure. It does not rule out a carefully chosen surgery link with a controlled margin. No contact surgery theorem or assertion about its framings is imported into the proof. Approximation alone cannot supply the missing uniform margin for arbitrary contact-transverse links.

## 6. Approach V: circulation and geometric realization

### Proposition 6: accepted

If each edge lies on a directed cycle, sum one integral cycle vector for each edge. The result is balanced and strictly positive on every edge. Repetitions, parallel edges, and self-loops cause no issue.

Conversely, for a directed edge u to v without a return path, the vertices reachable from v form a set with no outgoing edge and with that edge entering from outside. Summing the conservation laws cancels all internal contributions. It leaves strictly positive incoming flow and zero outgoing flow, which is impossible. Self-loops already have a return of length zero. Empty edge sets satisfy both conditions vacuously; the corresponding circulation and realization can be empty.

The proposition does not confuse this edge-cycle criterion with strong connectivity. For example, two disconnected directed cycles admit a positive circulation but are not recurrent in the stronger all-vertices-to-all-vertices sense used in Calegari's local-orientation definition. Nor do positive incoming and outgoing degrees at each vertex suffice; a one-way bridge between two looped vertices is a counterexample.

### Proposition 7: accepted under its stated geometric hypotheses

At each vertex, conservation allows a bijection between incoming and outgoing edge copies. A finite set of edge copies with these pairings decomposes into closed directed walks. The local foliation-chart assumption ensures cut incoming ends lie below, and outgoing ends above, the vertex leaf. Each paired connection can therefore be interpolated with strictly increasing transverse coordinate. This would not follow from an abstract graph orientation alone.

Away from vertices, parallel copies can be chosen inside arbitrarily small edge neighborhoods, staying positively transverse. At joins, the cone of positive tangent vectors is open and locally convex; monotone smoothing can preserve positivity. The resulting finite collection consists of smooth transverse immersed circles. Its compactness gives a positive tangent margin after choosing a metric and positive defining form near the curves.

A sufficiently small C1 general-position perturbation separates the circles and removes their double points: the off-diagonal pair-parameter domains have dimension two, while the diagonal in the product of two 3-manifolds has codimension three. Near the parameter diagonal, immersion already supplies local embedding. This is the standard dimension-three embedding argument for finitely many one-dimensional compact domains. Performing the perturbation in the prescribed edge tubes and vertex charts keeps the directed traversal multiplicities and positivity. No original knot type is promised or needed.

These arguments produce a transverse link near an already realized transverse graph. They contain no slope, framing, attaching-map, or cancellation computation. The claimed missing step, control of a fixed filling output, is real. Calegari's positive-cohomology condition cannot be obtained by replacing it with recurrence; the source distinctions are retained.

## 7. Primary-source applicability and inspection limits

Three local primary PDFs were rehashed. Their complete text was freshly extracted for targeted reinspection, and each new extraction matched the retained extraction byte-for-byte. The supplied renderings of the target statement and the two cited theorem pages were also visually checked. No source document, extraction, or screenshot is included in this audit package.

- **[C02] Danny Calegari, Problems in foliations and laminations of 3-manifolds**, arXiv:math/0209081v1. Definition 1.1 uses one closed transversal meeting all leaves. Question 9.1 on printed page 21 asks for a common surgery output, and the adjacent remark proposes a triangulation/Heegaard direction. The separate common-exterior question is clearly marked. The author's target interpretation is faithful. https://arxiv.org/abs/math/0209081v1
- **[C00] Danny Calegari, Foliations Transverse to Triangulations of 3-Manifolds**, arXiv:math/9803109v1, published in Comm. Anal. Geom. 8 (2000), 133-158. Reinspected printed pages 2-4 and 8-9. The smooth, oriented, cooriented convention applies. A local orientation includes nonempty connected incoming/outgoing link subgraphs, tetrahedral ordering, and recurrence. Lemma 4.2 supplies such a triangulation for a taut foliation, with essential directed loops. Theorem 2.2 uses a positive orientation, including a common cohomology functional positive on directed loops and the appropriate vertex-link condition. It cannot be applied using only Proposition 6's circulation criterion. The packet cites it only for the correctly distinguished stronger hypothesis. https://arxiv.org/abs/math/9803109v1
- **[B16] Jonathan Bowden, Approximating C0-foliations by contact structures**, arXiv:1509.07709v2, Geom. Funct. Anal. 26 (2016), 1255-1296. Reinspected the introduction, Theorem 1.2, and the immediate discussion. The smooth-leaf/continuous-tangent convention, coorientable scope, and sphere and plane exceptions are preserved. The following discussion explains that the plane exception can be removed in further work; the packet narrowly identifies the displayed theorem and does not claim the exception is an impossibility theorem. The explicit example depends on its own calculation, not on this literature theorem. https://arxiv.org/abs/1509.07709v2
- **[L62] W. B. R. Lickorish, A Representation of Orientable Combinatorial 3-Manifolds**, Ann. of Math. 76 (1962), 531-540. The indexed primary opening-page facsimile confirms the closed, connected, orientable surgery theorem. The facsimile PDF request did not produce a readable full paper; JSTOR supplied no body. Thus the opening theorem scope was independently confirmed, but neither a complete-paper inspection nor a local PDF hash is asserted. This does not block the elementary partial results. https://www.jstor.org/stable/1970373

The primary facsimile locator for [L62] is https://sites.iiserpune.ac.in/~tejas/Teaching/Spring2017/Notes/A%20representation%20of%20orientable%20combinatorial%203-manifolds_Lickorish.pdf .

Bounded current searches for the exact universal-transverse-surgery phrase and Calegari Question 9.1 did not locate a verified resolution. This is a search outcome, not certification that no resolution exists. The accepted disposition means that this packet has not solved the problem.

## 8. Independent controls and replay

The independent exact checker uses integer/rational arithmetic and separately implemented constructions:

- 384 abelian presentation cases test the quotient rank bound and a reversed-inequality countercontrol.
- 1,856 commuting peripheral-pair/slope cases in S3 and the order-eight dihedral group test normal-closure containment. A C6 example distinguishes the correct epimorphism direction. These are algebraic models, without claims that every model is a link exterior.
- 40 integral section-basis/inverse and normal-generator word cases, and 23,520 primitive slope/positive-degree cases, including framing and sign changes. Zero degree and nonprimitive slopes are explicit hypothesis controls.
- Two symbolic exterior-algebra calculations verify both contact signs. There are 171 exact rational circle samples, 16 strict-margin tests, and the zero-epsilon/equality countercontrols.
- 875 graphs, including loops, parallel edges, empty graphs, disconnected cycles, and one-way cuts. All 350 positive cases have exact weighted cycle decompositions; 525 negative cases have reachability-cut certificates. Strong connectivity and local degree countercontrols distinguish the hypotheses.

The author's authenticated bootstrap and diagnostics pass normally and under -O and -OO. The author's adversarial harness reports, in each mode, three accepted and 31 rejected controls. The independent artifact harness adds, in each mode, three positive environments and 27 rejected cases, including nine direct semantic-payload mutations. Seven direct malformed-JSON parser tests reach the parser independently of raw-hash rejection. Read-only relocated copies preserve their full byte inventories. Hostile import-path variables do not affect isolated interpreter results.

The direct semantic/parser controls are important: a corrupt manifest failing its fixed hash does not by itself establish that every deeper parser branch was exercised. The audit distinguishes these layers. The trusted bootstrap is externally pinned before execution; a substituted bootstrap is rejected by the auditor's outer authenticator without executing it. The results assume a trusted interpreter and operating system and stable files during a run; no defense against concurrent filesystem races is claimed.

Both complete external corpus inputs were replayed in all three modes. Their byte counts and hashes, target record, research record, pair binding, and statement binding agree with the author metadata. Only metadata was emitted. This verifies the identity binding; it does not independently certify the author's entire duplicate-history search.

The independent replay driver itself was run normally, under -O, and under -OO, producing identical reports. Optimization therefore does not remove its checks. Finite controls are evidence about calculations and artifact handling, not substitutes for the general arguments in Sections 2-6.

## 9. Acceptance boundary

Accepted: the period obstruction; common group quotient and Betti lower bound; absence of a bounded-component universal strengthening; disjoint positive normal-generating sections; the exact extension slopes for the original fiber class; the contact-to-foliation transfer countercontrol; and the conditional circulation-to-link construction.

Not established: a universal target; an obstruction excluding every possible target; a successful selection of surgery coefficients; extension of the original foliation; a theorem that abstract directed graphs can always be realized in the required way; historical novelty; or worldwide current openness.

The five families are mathematically distinct. The section construction is the countercontrol within the group/homology family, rather than an extra counted approach. Source research, numerical checks, review, and packaging are not counted as approaches. The approved classification is **unsolved, 5/5 approach families**. No correction patch or replacement author manifest is needed or supplied, because the original accepted proof bytes have not changed.
