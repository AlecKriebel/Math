# Fresh adversarial audit: problem 30001232

Date: 2026-10-04 UTC. Rank 614; catalogue code OWR-3471-006.

## Verdict

**PASS: the frozen candidate supplies a complete counterexample to the primary conjecture. No fatal mathematical error or missing construction step was found.** The argument works for every integer d >= 7. Its degree-seven member is a smooth connected complex projective surface with ample canonical bundle, hence minimal, and has an ample integral polarization L and an integral curve C' through x satisfying

- K_S^2 = 144;
- L^2 = 6;
- L.C' = 1;
- mult_x(C') = 6;
- epsilon(S,L;x) <= 1/6 < 1/(2 + 144^(1/4)).

This is a mathematical audit of a candidate, not peer review or a historical-priority certificate. The literature searches below do not establish novelty or that no earlier counterexample exists. Do not describe it as a first solution. No remote mutation, release, or outside communication was performed.

The only source-precision note is nonblocking: Bauer's degree choice d=m+1 is stated for sufficiently large d. It supports the mechanism, but does not by itself certify the small degree d=7. The frozen proof already gives a valid independent polynomial and parameter-space argument for that degree, so no repair is needed to the theorem.

## Frozen input and review boundary

The input manifest SHA-256 is

572b23e2c5f2ddcaec74c05172542d9bfef69d317d6a0151f052bf4e0fc5c62c

The reviewed PROOF.md SHA-256 is

efa3b1a7c809bc244799048bd0cf25e9ac56e09d4f90c133ef5095b0458fbcc3

All nine listed author files matched the frozen manifest before and after verification. Both original control programs were executed without editing them; their output bytes matched the saved result files exactly. Review covered the full main proof, five-route research log, source interpretation, statement quantifiers, and computational limitations.

No source PDFs, text extractions, or rendered source pages are included in this audit package. Public source links and byte fingerprints identify the checked evidence without redistributing it.

## 1. Source and exact target

### 1.1 Primary source gate

The publisher's report landing page and linked report were independently reached:

- [Oberwolfach Report 21/2009](https://ems.press/journals/owr/articles/3471)
- [Publisher PDF](https://ems.press/content/serial-article-files/46224?nt=1)
- [Report DOI](https://doi.org/10.4171/OWR/2009/21)

The rendered printed page 1124, PDF page 24, was visually inspected. In Szemberg's contribution, Conjecture 2 has the lower bound 1/(2+|K_S^2|^(1/4)); the additive 2 is outside the fourth root. The context concerns smooth projective surfaces. The conjecture expressly includes arbitrary Picard number and arbitrary points. Its polarization is an ample line bundle, not a very ample bundle. The next theorem separately concerns very general points. These distinctions all matter, and the candidate matches the former target.

The catalogue URL was independently retried and remained inaccessible through the web tool. The pinned catalogue record has instead (2+|K_S^2|)^(-1/4), a different and stronger bound. This transcription cannot govern the mathematical audit. The example also violates it, since 146<6^4, but the primary-source violation is the substantive conclusion.

The final question on preprint page 7 of [Szemberg, arXiv:0711.0584](https://arxiv.org/abs/0711.0584), and Question 6.1.6 on preprint page 17 of [A primer on Seshadri constants, v2](https://arxiv.org/abs/0810.0728v2), corroborate the primary formula. The live arXiv record identifies the latter as v2, revised July 2010. Neither these historical statements nor the catalogue's present open label prove current open status.

### 1.2 Bauer gate

[Thomas Bauer, Seshadri constants on algebraic surfaces](https://arxiv.org/abs/math/9903072), Proposition 3.3 and proof, preprint pages 11-14, was checked. Page 13 was separately rendered and visually inspected. The known construction uses a pencil of irreducible curves, distinct simple basepoints, its blowup, and a polarization r(aF+E_1), a>=2. The surface and line bundle requirements apply to the candidate's rational intermediate surface Y, with r=1 and a=2.

Part (b) permits d=m+1=k+1 on the plane for sufficiently large d. It imposes no d~m^2 obstruction. Nevertheless, this is an asymptotic sentence: the candidate must supply its own degree-seven existence proof, and it does. The final base change is not claimed as a theorem of this cited proposition.

### 1.3 Other historical-route sources

Theorem 7 of Szemberg's paper applies to Picard number one. Fuentes Garcia's [ruled-surface paper](https://arxiv.org/abs/math/0503253), Theorems 4.14 and 4.16 on preprint page 10, applies to geometrically ruled surfaces and gives the cases used in the log. Bauer's Theorem 3.1 applies to smooth projective surfaces with ample L and uses the actual canonical slope, not K^2 alone. None of these special-case results is silently substituted for the full conjecture.

## 2. Attack on the singular plane curve

Let f_d=Z(X^(d-1)-Y^(d-1))+X^d and p=[0:0:1].

### 2.1 Global integrality

As a polynomial in Z over C[X,Y], the two coefficients are coprime: any common factor of X^d and X^(d-1)-Y^(d-1) would divide X and Y. Over C(X,Y) the polynomial has degree one and is irreducible. Primitivity and Gauss's lemma therefore establish irreducibility in C[X,Y,Z]. This is a global statement; the presence of multiple local branches at p does not make the curve globally reducible.

An independent normalization check is available. Put A=s^(d-1)-t^(d-1). The map

[s:t] -> [sA:tA:-s^d]

has no common zero of its three homogeneous degree-d coordinates. Substitution annihilates f_d. Away from A=0, the ratio X:Y recovers s:t, so the map is generically one-to-one. Its d-1 distinct points with A=0 map to p. This agrees with the claimed rational integral curve and ordinary multiple point. This is a cross-check of an existing proof step, not a replacement construction.

### 2.2 Multiplicity and remaining singularities

In the Z=1 chart, the tangent cone is x^(d-1)-y^(d-1), square-free over C. Hence p has multiplicity d-1 and d-1 distinct tangents. The three partial derivatives exclude all other singularities: if f_Z=0 and X,Y are nonzero, f_Y=0 forces Z=0 and f_X then cannot vanish; if either X or Y vanishes, both vanish.

For d=7, a separate exact Groebner calculation gives the affine singular ideal (x^5,y^5). Its support is only the origin. The potential point at infinity is excluded by f_Z. The calculation verifies this specified polynomial; the preceding argument handles the whole family.

## 3. Attack on the all-integral pencil and Bertini step

### 3.1 The bad locus really is closed and sufficiently small

Write V_d=P(H^0(P^2,O(d))) with dimension N_d=d(d+3)/2. For every split d=a+(d-a), 1<=a<=d-1, the multiplication map from two projective spaces is proper, so its image is closed. The union R of these finitely many images includes every reducible or nonreduced degree-d polynomial. There is no unaccounted repeated-factor case.

For every split,

N_d-(N_a+N_(d-a)) = a(d-a) >= d-1.

Thus dim R <= N_d-(d-1). Since [f_d] is not in R, the join of this fixed point with R has dimension at most dim R+1 <= N_d-(d-2). It is a proper closed locus for d>=3. Choosing [g] outside it makes the line spanned by [f_d] and [g] disjoint from R. If a reducible member r lay on that line, then g would lie on the joining line from f_d to r, exactly the excluded situation.

This establishes every member's integrality, not merely the general member's integrality. It is essential for the later ampleness of 2F+E_1. The audit controls check all factor splits through degree 256, but the displayed dimension identity, not those finite tests, proves the general assertion.

### 3.2 Simultaneous generic requirements are compatible

The full degree-d linear system on P^2 is basepoint-free and separates tangent directions. In characteristic zero, Bertini gives a nonempty open set of smooth g. Its restriction to the smooth locus of C_0 gives the required transverse intersection condition. The extra open condition g(p) !=0 avoids the sole singular point. These are dense opens in an irreducible projective parameter space, and their intersection with the complement of the proper join is nonempty.

There is no need to exhibit a numerical g, and failure to test an explicit g is not a proof gap. The proof does not infer existence from a random sample. Bezout then gives d^2 distinct transverse basepoints, all away from p, since C_0 and g have no common component.

### 3.3 One blowup is enough at each basepoint

Locally at a basepoint, f_d and g are regular parameters u,v. The graph of the pencil is the usual blowup of the ideal (u,v). Its exceptional P^1 maps isomorphically to the parameter P^1, so it is a section rather than a fibre component. Every combination alpha*u+beta*v has a nonzero linear term for [alpha:beta] in P^1. Consequently no member gains a multiple basepoint, and no second blowup is needed.

After the d^2 blowups, the fibres are exactly the strict transforms of the integral reduced pencil members. They are integral, reduced, and connected. The blowup is an isomorphism near p, so the ordinary (d-1)-fold point survives on the chosen fibre C.

## 4. Attack on the polarization

F=f^*O(1) is nef; F^2=0, F.E_i=1, and E_i^2=-1. For A=2F+E_1, the stated values A^2=3, A.E_1=1, and A.F=1 are correct.

The proof covers every integral curve D:

- D=E_1 has intersection one.
- If D differs from E_1 and F.D>0, then E_1.D>=0 on the smooth surface, so A.D>0.
- If F.D=0, then D maps to a point of the base: a nonconstant morphism from a proper integral curve to P^1 has positive pullback degree. Because the entire fibre is integral and reduced, D must be that fibre, and A.D=1.

Nakai-Moishezon applies to the Cartier divisor A on the smooth projective surface Y. Positivity of the square and every curve intersection proves ampleness. The argument would fail with reducible fibres, but their exclusion has already been proved. No global-generation or very-ampleness assertion is made or required.

## 5. Attack on the branched fibre product

### 5.1 Existence and smoothness of the cover

There are infinitely many smooth fibre values: the smooth pencil member g already supplies one, and the nonsmooth locus has closed image under the proper map f; equivalently generic smoothness and properness give only finitely many exceptional values. Pick four distinct smooth values avoiding C's value. A double cover of P^1 branched simply there exists, for example by adjoining a square root of a square-free quartic in an affine coordinate. Its smooth projective model B has genus one by Riemann-Hurwitz and is connected.

The base change pi:S=Y x_(P^1) B -> Y is finite flat of degree two. Away from the four branch fibres it is etale, including above singular fibres. Etale maps to a smooth surface have smooth source. Along a branch fibre, f is smooth, and completed or analytic local coordinates give t=v^2 with an independent coordinate u. The source coordinates (v,u) are regular. Thus the fibre product itself is smooth everywhere; no normalization, resolution, or later contraction changes its invariants.

### 5.2 Connectedness, integrality, and projectivity

The projection S->B is proper with the same geometrically connected fibres as f. A proper surjection with connected fibres onto a connected base has connected total space: a disconnection would partition the base into disjoint closed images, because a fibre could not meet both pieces. Hence S is connected. Smooth irreducible components cannot meet, so a connected smooth surface is integral.

As an independent check, a local rational square class defining the cover has odd valuation at any branch fibre. It cannot be a square in C(Y), so the generic cover cannot split. There is no hidden disconnected double cover.

Finite over projective Y implies projective S. In particular the later intersection theory and ampleness criteria concern projective algebraic surfaces.

### 5.3 Canonical line bundle, not merely a numerical guess

The branch divisor is four disjoint smooth fibres, with line bundle O_Y(4F). The double cover is constructed from O_Y(2F); the ramification divisor has line bundle pi^*O_Y(2F). The local differential relation dt=2v*dv gives the Hurwitz contribution once along ramification. Thus

K_S = pi^*(K_Y+2F)

as line bundles. There are no extra singular-fibre discrepancies because pi is etale there. The choice of smooth branch values is indispensable and has been made.

## 6. Attack on canonical ampleness and minimality

Set N=K_Y+2F=(2d-3)H-sum E_i. A useful independent simplification is

N=(d-3)H+F.

Both H and F are nef. If D is exceptional, then N.D=1. Every nonexceptional integral curve has H.D=e>0, hence N.D >= (d-3)e>0 when d>=4. Moreover N^2=3(d-1)(d-3)>0. This gives exactly the positivity required by Nakai-Moishezon.

The author's Bezout argument gives the same result. The image of a nonexceptional curve is an integral plane curve of degree e. A smooth pencil member different from that image has no common component with it and has multiplicity one at each basepoint. Therefore sum r_i<=de, and

N.D=(2d-3)e-sum r_i >= (d-3)e>0.

The choice of a different smooth member is always possible; there are infinitely many smooth values. Thus neither proof overlooks a curve passing through an unusually large collection of basepoints.

Finite pullback preserves ampleness, so K_S is ample. In particular it is big, so S is of general type, and a smooth rational (-1)-curve is impossible: adjunction would give canonical intersection -1. Minimality is therefore proved on S itself, rather than asserted after a contraction that might destroy the polarization.

The original E_i lift to elliptic sections T_i isomorphic to B, with T_i^2=-2 and K_S.T_i=2. They are not rational (-1)-curves. This explicit check addresses the most immediate concern about whether the nonminimal intermediate surface can lead to a minimal final one.

## 7. Independent incidence-model check of the invariants

The blowup graph Y sits in P^2 x P^1 as the incidence hypersurface of the pencil. Its base change is a hypersurface in P^2 x B in the class d*h+2*b, where h is the plane hyperplane class and b is a numerical point class on the elliptic curve. This follows directly from the graph equation; the simple transverse basepoints ensure the graph is exactly Y.

In the ambient intersection ring h^3=b^2=0 and integral(h^2*b)=1. Adjunction gives

K_S=((d-3)h+2b)|_S.

For d>=4 this is also the restriction of an ample external tensor product on P^2 x B, independently confirming canonical ampleness. The degree-two line bundle on B is h_cover^*O_P1(1); it is ample even if it is not very ample.

The Chow-ring calculation gives

K_S^2=6(d-1)(d-3),
c_2(S)=6(d-1)^2,
chi(O_S)=(d-1)(d-2),
H_S^2=2,
H_S.Q=d,
Q^2=0,
K_S.Q=d(d-3),

where Q is the numerical class of one fibre of S->B. These identities agree with the cover calculation, Noether's formula, and the genus (d-1)(d-2)/2 of a smooth degree-d plane curve. At d=7 they give K^2=144, c_2=216, and chi=30, with no surface-geography contradiction.

This cross-check uses the same already-constructed surface. It is not a new sixth proof-search approach or an unsupported alternative existence claim.

## 8. Attack on the degree-one lift and Seshadri comparison

If t_0 is C's unbranched value, then h_cover^(-1)(t_0) consists of two distinct reduced C-points b_1,b_2. The fibre-product identity gives

pi^(-1)(C)=C x {b_1,b_2}=C' disjoint union C''.

Each component is therefore isomorphic to C; it is not a connected degree-two cover of C. Projection formula on an individual component gives L.C'=A.C=1. Etaleness, or the induced isomorphism of completed curve local rings, preserves the multiplicity d-1.

It is important to distinguish one lifted fibre from the total pullback of F. Numerically pi^*F=2Q. If T=pi^*E_1, then T^2=-2, T.Q=1, and L is numerically 4Q+T. Thus L^2=6 and L.Q=1, whereas L.pi^*F=2. The candidate uses the correct individual-curve degree. On the elliptic base, different point fibres need not be linearly equivalent; only numerical equivalence is used in this additional calculation.

The primary definition takes the infimum of L.D/mult_x(D) over integral curves through x. C' is one admissible curve on a smooth surface, so its quotient is a valid upper bound. There is no need to show C' computes the exact Seshadri constant. L=pi^*A is an ample integral line bundle, not a fractional numerical class.

For d>=7, comparison with the primary bound is equivalent to

(d-3)^4 > 6(d-1)(d-3),

since all quantities and d-3 are positive. Division gives (d-3)^3>6(d-1). It holds at d=7 and its successive difference is 3(d-3)^2+3(d-3)-5>0. For d=7 alone, 144<4^4 is sufficient. Degrees 4,5,6 fail this strict comparison in the specified four-branch construction, and the independent controls retain these negative cases.

This refutes the universal primary conjecture. It does not refute the positive lower-bound question on one fixed surface, nor the Picard-rank-one theorem, nor very-general-point bounds. As d grows, the constructed surface changes.

## 9. Review of the earlier four routes

These routes are not premises of the counterexample, but their scope and arithmetic were checked.

1. **Numerically trivial canonical class.** For q=L.C>=1 and m=mult_x C, the genus drop and adjunction imply m(m-1)<=C^2+2; Hodge gives C^2<=q^2/L^2<=q^2. The assumption q/m<1/2 forces m>=2q+1, contradicting the inequality. This proves the claimed 1/2 lower bound in this class, without solving the full problem.
2. **Geometrically ruled surfaces.** Fuentes Garcia's stated cases imply the log's lower bound >=1 for integral ample classes. Here a=A.f is a positive integer, and the relevant 2b-ae=A^2/a is a positive integer; for e>0, b-ae=A.X_0 is also a positive integer. The theorem's e=0 section exception is retained. This is a class-specific result.
3. **Picard rank one and canonical polarization.** The cited rank-one theorem is used in its stated scope. The canonical-polarization lower bound is also independently consistent with the same elementary genus/Hodge calculation: for q=K.C, K ample implies C^2<=q^2/K^2<=q^2; m>=2q+1 contradicts m(m-1)<=q^2+q+2. Replacing arbitrary L by K would be invalid, and the log does not do so.
4. **Canonical slope and formal lattice.** The sufficient inequality sigma<=t^2+3t-1 is the correct algebraic rearrangement of Bauer's slope bound, with t=|K^2|^(1/4). It is not established universally. The log's Gram matrix has leading minors 2,-1,4s for s=m(m-1)-2>0, hence signature (1,2); parity and the displayed adjunction equality are consistent. The log expressly does not promote this formal matrix to an existing surface.

## 10. Exact controls and what they do not prove

Run from this audit directory:

    python3 independent_checks.py

SymPy 1.14.0 was used. The saved independent_results.json records:

- Both author programs replayed exactly: 27 lattice rows and 97 formula rows; output SHA-256 values equal the recorded author-result hashes.
- 60,731 explicit audit assertions passed, including 13 frozen-byte checks and two output-replay checks.
- Every one of 32,640 factor-degree splits for d=2,...,256 was checked.
- The degree-seven singular scheme and homogeneous normalization substitutions were checked exactly.
- Nine symbolic incidence/adjunction identities were checked before specializing d.
- The strict threshold and geography identities were checked for d=4,...,1000, retaining the d=6 negative control.
- 11,712 Bezout extremal/interior test cases were checked, as controls of the encoded intersection expression.
- Single-fibre versus total-pullback degree, section adjunction, and earlier-route algebra were checked separately.

These are reproducibility and arithmetic controls. Their counts are not evidence of geometric existence, and increasing their range would not prove Bertini, connectedness, smoothness, or ampleness. Those steps were addressed mathematically in Sections 2-8. No finite-field sample is used as a proxy for a complex all-integral pencil.

## 11. Nonblocking clarifications and recommended presentation

No correction to the theorem, constants, or construction is required by this review. Two optional clarifications would make a future non-frozen version harder to misread:

1. In the Bauer provenance sentence, explicitly say that his d=m+1 statement is asymptotic and that Section 1 independently proves the degree-seven case. This avoids accidentally turning the citation into a finite-degree existence certificate.
2. Add N=(d-3)H+F in Section 4. It compresses and independently explains the all-curve positivity already proved by Bezout.

Keep the correct primary denominator, the arbitrary-point qualifier, and the no-novelty disclaimer. Keep the author freeze untouched; these comments belong in the separate audit or a separately versioned revision.

## 12. Literature and redistribution boundary

Independent bounded searches combined Seshadri/minimal surfaces/Szemberg/counterexample, fourth-root bounds, Miranda/base change, and double covers/small constants. They did not locate a primary source settling the exact conjecture or providing this exact construction. This is a weak negative search result, not proof of current open status, novelty, or priority. Unrelated Nagata-Biran-Szemberg conjectures and minimal-degree surface results were not conflated with the target. No need for a contemporary survey is inserted as a mathematical premise.

Checked source-byte fingerprints, with sources retained outside this distributable package:

- OWR report PDF: ee3b3e545a5d613abbb63e51a4d4c15224db017ae5d54887803b824ae076450b
- OWR printed-page-1124 image inspected: 758b15854d62f89851a1d71ab54552351a5e5d1e64d8643c5bba0dad6bf9180e
- Bauer 1999 PDF: bebc68957350bb221e3d8a7f8877bb5d9cdf84b70d47c4ec3d42f789e5b251eb
- Separately rendered Bauer preprint-page-13 image: 6f5a6ed301d3e3d4cb5b3e0fded2d5221192be786457cafd6fb08a01693365d3
- Szemberg 2008 PDF: 84e438e50721d258ddadc76b0af8329890bd6ecb1d65cb1e2d2cb35b67ff9cc6
- Primer PDF: eeffe58c075a785a4654ca8b3529a1bef8b8e2bcfa99b827ab4c0b1c140d8166
- Fuentes Garcia PDF: f3c575fef7b5154178ea0c8018bc4dd50389fedfdbf348d1e4ace1ac281b0361

The accompanying AUDIT_MANIFEST.json binds this report, the independent program, and its result, and separately identifies the unchanged author manifest. Only explicitly enumerated authored files are publication-safe. The sibling source repository is excluded in its entirety.
