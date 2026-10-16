# Sealed source-first baseline: function theory family

This record was completed before reading TURN_1 through TURN_5, candidate code, computed outputs, status/results/finals/history, prior reviews, or any sibling/root mathematical findings.

## Exact research claim and assumptions

Hayman–Lingham Problem 2.55 (PDF printed p.43) asks whether, for three nonconstant entire one-variable functions f_i, every ambient entire F on C^3 whose restriction is bounded on V={f_1(z_1)+f_2(z_2)+f_3(z_3)=0} takes one constant value on all of V. No finite order, finite singular set, derivative nonvanishing, polynomial, growth, or smoothness assumption is imposed. The quantifier is all such triples; the conclusion concerns all of V, not merely each local branch or an individual fiber/component.

Success means a checkable proof with these exact quantifiers, or an explicit triple and ambient entire F with a global bound and at least two distinct restriction values. Partial positive families must state the additional assumptions; reductions alone do not settle the target. A claimed equivalence with the intrinsic bounded-holomorphic formulation must justify extension from the closed analytic set and treatment of singularities.

## Independently retrieved primary source facts

* Hayman and Lingham, Research Problems in Function Theory, 1809.07200v2, printed p.43: Problem 2.55 as above; the update reports a special case due to Demailly. The original catalog ID is 2302055 / AMR-022-2055. Its queued/open bookkeeping is not evidence of correctness or of current novelty.
* Demailly, Bull. Sci. Math. 103 (1979), 179–191, first three PDF pages inspected visually: bounded holomorphic functions on S={e^x+e^y=1} are constant, and polynomial-growth functions are polynomial restrictions. The introduction states the separated sum for n>=3 is irreducible (attributed to Rubel–Squires–Taylor), and the Liouville answer is positive when one f_i is rational. This irreducibility is quoted source knowledge, not independently re-proved here.
* Demailly, C. R. Acad. Sci. Paris 288 (8 Jan 1979), pp.39–40, both scanned pages inspected: Theorem 2 gives polynomial restriction for polynomial growth on S; Corollary 2 gives bounded-holomorphic constancy on {e^x+e^y=h(w)} for nonzero meromorphic h on C^n. Thus two exponential summands are already a known family, including arbitrary entire third summand. Its n-dimensional exponential hypersurface corollary is likewise known.
* Lin and Zaidenberg, Liouville and Caratheodory Coverings in Riemannian and Complex Geometry, alg-geom/9611020v2: a connected Zariski open subset of a compact complex space is ultra-Liouville by bounded plurisubharmonic extension and the maximum principle (section 1.3). Theorem 1.6 proves Liouville for a hypernilpotent group acting ultra-Liouville, hence for hypernilpotent coverings of an ultra-Liouville base. These conclusions require the stated base/action hypothesis; a merely Liouville base is insufficient. Section 1.9.2 identifies e^x+e^y=1 as the maximal abelian covering of C minus {0,1}, Liouville but not ultra-Liouville. Ordinary Liouville, ultra-Liouville and hyperbolicity must not be conflated.
* Rempe-Gillen and Sixsmith, Hyperbolic Entire Functions and the Eremenko-Lyubich Class: Class B or not Class B?, 1502.00492v2: section 2 defines S(f) as the singular values of the inverse. It is the smallest closed set outside which the full preimage mapping is a covering, and is the closure of critical and finite asymptotic values. The stated covering conclusions are away from S(f), not just away from critical values. Hyperbolicity is a distinct dynamical notion and imposes bounded singular values.

All five PDF bytes were independently downloaded from their routed primary URLs; all five SHA-256 digests match the frozen routing entries. Raw source PDFs, extracts and rendered scans are private and excluded from public delivery.

## Falsification boundaries registered in advance

1. All nonconstant entire triples, including infinite order and arbitrary critical/asymptotic value sets.
2. Points with multiple/vanishing derivatives, singular hypersurface loci, exceptional fibers, omission of values, and zero/nonzero right-hand sides for exponential equations.
3. Connectedness, irreducibility, and global gluing versus local or per-component constancy. A two-variable analogy is not evidence for three variables; removing a nonconstant summand changes the hypothesis.
4. Polynomial/proper maps versus transcendental maps with inverse singularities. Absence of critical values does not guarantee properness or a covering over the proposed base.
5. Any claim that entire curves force bounded functions constant must show a sufficient family of curves through/connecting generic points; finite sampled curves do not establish coverage. Entire curves may be absent on hyperbolic fibers.
6. Any differential-equation or tangent-field method must prove global completeness and remain valid at degeneracy; local flows alone do not invoke Liouville on C.
7. Quotient/descent arguments must justify the quotient, transitivity, boundedness of envelopes, extension across deleted analytic sets, and maximum principle hypotheses.
8. Computations may falsify exact formulas or support finite examples only. No degree cutoff or numerical survey certifies a universal conclusion.

## Independence and provenance

Frozen head: d9e4600d05b8272fe913a22ae7dcc0fbe0a26344. Original base: efd29c05204703acca9a0860812f54b94fae54b1. Review family: complex function theory, global entire maps, differential equations, growth/degeneracy counterexamples. No external contact or Git mutations. No candidate artifacts or other reviewer conclusions read during this baseline.
