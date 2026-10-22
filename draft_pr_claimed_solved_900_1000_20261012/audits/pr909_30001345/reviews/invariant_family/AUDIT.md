# Independent audit: local resolution and singularity invariants

## Decision and exact scope

**PASS with a mandatory scope qualification already present in the frozen proof.** The local invariant and delta calculations are correct. The displayed family gives a delta-constant degeneration from an ordinary ninefold point to twelve ordinary triple points with

\[
\overline M_0=7<12=\sum_p\overline M_{t,p},\qquad
\delta_0=36=\sum_p\delta_{t,p}.
\]

This is a counterexample for the **summed, rough invariant on unrestricted reduced multibranch deformations**. It does not refute a marked-section assertion, a unibranched assertion, or the published parametric Conjecture 3.8. That conjecture concerns the rough invariant; calling Conjecture 3.8 itself a fine-M conjecture would be inaccurate. No defect requiring a mathematical repair was found in the audited invariant calculation. No priority or present-day openness conclusion was investigated.

The original target's broad wording is supported by its source, subject to the distinction between a literal formulation and an unstated authorial intention. If promotion of “claimed solved” is intended to mean resolution of the published parametric conjecture or its intended unibranched core, this package cannot support that promotion. For the literal broad question, the counterexample is sufficient.

## Inputs, independence and limits

This review is restricted to PR909 / problem30001345, original head `d186dea31791cd3e8acf6829e0b65d01849623b8`. The frozen proof's independently recomputed SHA256 is `561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b`, matching preflight. The bound original package-manifest hash supplied by preflight is `a8376fa67c497c4b31522364ac87163cdd6f5ec42961893981c44f0d95f0ee02`.

I read the exact target, charter and frozen proof first, reconstructed the resolution and delta arguments, then read the complete primary-source contribution and complete published article. I did not consult the old audits or acceptance files. I subsequently inspected the original checker for its stated limits; `verify_invariants.py` does not import or execute it. The independent checker verifies exact tangent positions, resolution arithmetic and finite boundary controls; it is supplementary to the proofs below. This is the invariant-family review, not a claim that every implementation or publication gate has been independently discharged.

No original/candidate files, Git state, PR state, releases or remote data were changed. All writes are confined to this review directory. Raw PDFs, full extracts and rendered pages remain in ignored directories. There was no contact with any outside individual and no work on another target.

## 1. Actual embedded resolution and canonical sign

Let an ordinary r-fold point have r smooth branches with distinct tangent lines, with r>=3. Blowing up the origin once separates the branches: its exceptional curve E is a smooth rational curve with E^2=-1; the strict transforms meet E transversely at r distinct points. Consequently the reduced total transform D=C'+E is a normal-crossings divisor. Before this blowup, r>=3 branches through one surface point are not a normal-crossings divisor. Thus this one blowup is the minimal embedded resolution, not merely a resolution of the strict-transform curve.

The canonical divisor supported on the exceptional locus is **K=+E**. There are two independent checks:

1. In coordinates y=u, x=uv, the pulled-back nonvanishing base 2-form has one zero along u=0. Its exceptional divisor is +E.
2. Write K=aE. Adjunction gives (K+E)E=-2, hence -(a+1)=-2 and a=1.

The support convention removes canonical ambiguity. On a general embedded resolution the negative-definite exceptional intersection matrix makes the adjunction equations unique among exceptional rational divisors. Adding the divisor of a meromorphic function can introduce strict-transform components and is not an allowed change of the supported local canonical representative. In the present one-curve calculation uniqueness is immediate.

The required intersection is therefore

\[
K(K+D)=E(C'+2E)=r-2.
\]

Equivalently, the principal total transform satisfies C'+rE numerically zero, so K+D is numerically (2-r)E. These are local intersection computations with compact exceptional curves; no compactification-dependent canonical divisor was substituted.

For the actual central polynomial, all spatial x-coefficients of the nine linear factors are nonzero. In the blowup y=u, x=uv their strict transforms intersect E at v=-b/a. The independent exact Q(omega) calculation finds nine distinct values. Thus the calculation above applies to the actual central equation, rather than to an assumed topological model.

### Node and resolution conventions

An ordinary node is already a normal-crossings divisor. With the identity minimal resolution there are no exceptional curves, and the invariant is zero. A convention requiring the two strict-transform branches to be disjoint instead uses one blowup; then E(C'+2E)=2-2=0 again. Consequently the two common node conventions agree here. A smooth point has value zero by the empty-resolution convention; the formula r-2 must not be extended to r=1.

Further blowups of crossings of the reduced boundary preserve the computed rough intersection: K_new=pi*K+F, D_new=pi*D-F, so K_new+D_new=pi*(K+D). Arbitrary extra blowups are not harmless. Blowing up a smooth boundary point instead gives K_new+D_new=pi*(K+D)+F and lowers the rough value by one. This is why the minimal embedded-resolution qualification is material. Neither contracting E and allowing the original r-fold crossing nor inserting extra smooth-point blowups is the prescribed resolution.

Using K=-E would produce -r, and using the unreduced total transform in place of D would produce -1. These competing conventions do not reproduce the claimed calculation and were explicitly rejected in the supplementary checks.

## 2. Negative part and fine invariant

The Zariski negative part is zero for these ordinary points. Indeed,

\[
(K+D)E=r-2\ge0.
\]

The exceptional locus consists only of E, so K+D is relatively nef; taking H=K+D and N=0 satisfies the decomposition. At the node's identity resolution there is no exceptional negative part either. Thus every point used in the example has N^2=0. The rough value and either printed fine correction agree point by point in this example. No hidden negative-square term can reverse 7<12.

This observation also means that the same broad multibranch construction gives the same values for the published fine invariant. It still supplies no counterexample to a conjecture imposing a unibranched central fiber. The frozen proof's decision to state only the rough theorem is legitimate and conservative.

## 3. Delta from local algebra, with no equinormalization shortcut

For relatively prime reduced equations f and g in the two-variable convergent local ring, the injection into the two component rings and their difference map give

\[
0\longrightarrow\mathcal O/(fg)\longrightarrow
\mathcal O/(f)\oplus\mathcal O/(g)\longrightarrow
\mathcal O/(f,g)\longrightarrow0.
\]

The normalization of the reduced union is the direct sum of the component normalizations. Taking lengths of the relevant normalization quotients yields

\[
\delta(fg)=\delta(f)+\delta(g)+I(f,g).
\]

Every component of an ordinary r-fold point is smooth, with delta zero. Every pair has intersection multiplicity one. Induction therefore gives delta_r=binomial(r,2). This argument establishes the numerical delta statement directly; it does not assume delta constancy from a putative simultaneous normalization.

The central value is binomial(9,2)=36. Each nearby triple has delta 3, so twelve triples give 36. At each fixed nonzero parameter all twelve points are retained in the fixed representative; summing delta is exactly the usual deformation-of-one-germ convention in that representative. No singularities elsewhere or boundary intersections are being discarded.

As a separate consistency check, the central Milnor number is 64 and the sum of nearby Milnor numbers is 48. The difference 16 equals the first Betti number of the connected nearby union of nine disks glued at twelve triple points: each triple identifies three points, decreasing Euler characteristic by two; hence chi=9-24=-15 and b1=16. This does not contradict zero geometric genus: normalization has nine disk components. It also explains why the source's specialized cuspidal-and-node Betti-number formula must not be applied here.

## 4. Independent all-n incidence and invariant argument

Fix n>=2 and a primitive n-th root zeta. Write the three groups of lines as

\[
A_i:X=\zeta^iY,\quad B_j:Y=\zeta^jZ,\quad C_k:Z=\zeta^kX.
\]

Within each group its n distinct lines meet at the corresponding coordinate vertex. No line from the other groups passes through that vertex. Between groups, A_i and B_j meet at

\[
P_{ij}=[\zeta^{i+j}:\zeta^j:1],
\]

which lies on exactly C_{-i-j}, exactly A_i and exactly B_j. The P_ij are distinct and all coordinates are nonzero. Conversely every intergroup intersection is obtained this way. These statements enumerate all pair intersections; the pair count is

\[
3\binom n2+3n^2=\binom{3n}2.
\]

The n lines at a coordinate vertex have distinct tangents, and the three distinct lines at each P_ij have distinct tangents. Thus the singularity list consists of three ordinary n-fold points and n^2 ordinary triples. For n=2 the coordinate vertices are nodes; for n=3 all twelve points are triples.

The proposed infinity L=X+2Y+4Z misses the coordinate vertices. At every P_ij its value has modulus at least 4-2-1=1 in the displayed representative. Hence it misses every pair intersection. In the chart L=1 no pair of arrangement lines is parallel. Scaling that affine arrangement by t makes the central fiber an ordinary 3n-fold point and preserves the enumerated incidence list for every t!=0.

One can use the explicit universal equation

\[
F_n=(x^n-y^n)\bigl(4^ny^n-(t-x-2y)^n\bigr)
\bigl((t-x-2y)^n-4^nx^n\bigr).
\]

Its x-leading coefficient is (-4)^n-1, which is nonzero. Dividing by this constant makes it monic, proving flatness over the parameter by freeness over C[y,t]. It is the product of 3n distinct linear planes whose fiber directions are distinct; all fibers are reduced. The disjoint union of these planes is finite over the hypersurface and is its normalization; each fiber is the disjoint union of the corresponding lines. This checks that using an arrangement does not hide a normalization-topology change.

The coordinate-vertex chart norms are at most 1, and the other chart norms at most sqrt(2). All moving intersections therefore have norm at most sqrt(2)|t|. The line forms have spatial coefficients (1,-q), (q,4+2q), and (-(1+4q),-2), respectively, with |q|=1. Their distances to the origin are at most 0, |t|/sqrt(5), and |t|/sqrt(13). Thus the same unit ball and |t|<1/4 retain every intersection strictly inside radius 1/2 and meet every component transversely at the boundary, for every n>=2. The invariant summation takes place in a valid local representative.

Now apply the previously derived local formulas:

\[
\begin{aligned}
\delta_0&=\binom{3n}2,
&\sum\delta_t&=3\binom n2+3n^2=\binom{3n}2,\\
\overline M_0&=3n-2,
&\sum\overline M_t&=3(n-2)+n^2.
\end{aligned}
\]

The rough excess is n^2-4. It is zero at n=2 and positive for every n>=3. At n=3 this is precisely 12-7=5 and delta 36. At n=1 the coordinate vertices are smooth and contribute zero, not -1; the displayed excess formula no longer applies. The remaining arrangement is one triple point before and after scaling, with no strict excess. The public finite checks n=2..100 supplement these universal arguments.

## 5. Branch shifts and marked sections

The alternative multibranch normalization that adds r-1 at each local singularity changes these numbers. For an ordinary r-fold point it gives 2r-3. Thus the ninefold central point has value 15, while twelve triples total 36, yielding excess 21. More generally the shifted excess for the Fermat family is 3n^2-6 for n>=2. The convention cannot be silently interchanged: already n=2 changes from equality for the displayed rough invariant to strict failure for the shifted one.

The displayed family has a distinguished section (x,y)=(0,0), with a nearby triple point. Along that section the comparison is 1<=7, so no failure occurs. Every nearby local singular value is at most 1. Thus an interpretation asking only for the invariant at one chosen nearby point is not refuted by this construction. The violated assertion sums the local invariants over all split singularities in the fixed ball.

The normalized central fiber has nine disks. A nearby normalized fiber has nine disks as well, so the deformation is rational in the relevant geometric-genus sense. It is not unibranched and hence not parametric in the published terminology. Neither rationality nor delta constancy repairs that missing hypothesis.

## 6. Primary-source binding

**OWR source.** I read all of Borodzik's contribution on printed pp. 2446–2448, including its references, and inspected the page images. Definition 1 displays the barred rough invariant K(K+D); Questions 2–3 use that barred symbol. The opening germ and questions do not impose a branch restriction. Page 2447 first states a one-branch signature proposition, then separately sets up several nearby singularities and their summed invariants, and introduces a cuspidal/node assumption for the ensuing estimate. These are restrictions on the method and theorem, rather than an earlier definition of Questions 2–3. The paragraph motivating the question mentions parametric forms, so intent cannot be inferred from omission alone; the positive evidence for the broad reading is the general germ setup, barred definition, and later explicitly added restrictions. [Official OWR PDF](https://ems.press/content/serial-article-files/46242?nt=1), DOI 10.4171/OWR/2009/43.

**Published source.** I read the complete 2014 article, visually checking printed pp. 575–577. Definition 3.3 expressly allows multibranched germs and fixes the exceptional-supported canonical divisor. Remark 3.4 records the branch-count shift. Definition 3.5 uses rough-M minus N^2, whereas OWR's printed fine definition uses plus N^2; N=0 makes this discrepancy immaterial here. Definition 2.1 defines parametric deformations by rationality and a unibranched central fiber. Conjecture 3.8 explicitly has that hypothesis and sums rough invariants. The proof therefore cannot resolve that conjecture. The broad deformation definition itself has flatness, transversality and locality conditions, with which the arrangement is compatible. [Published Osaka PDF](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/ojm51_03_573.pdf), DOI 10.18910/50809.

The source binding supports the frozen proof's narrow claim about the literal unrestricted OWR question. It does not establish which narrower problem the original author intended, nor that a contemporary unibranched conjecture is resolved. These distinctions must remain visible in any downstream summary.

## 7. Required and optional findings

- **Required mathematical repairs:** none found within this review's invariant, incidence, and convention checks.
- **Required scope condition for promotion:** retain “summed rough invariant, unrestricted reduced multibranch delta-constant deformations.” Do not summarize this as a solution of published Conjecture 3.8. The frozen proof already satisfies this condition.
- **Optional clarification:** explain N=0 explicitly, since then fine corrections cannot alter this particular example despite the printed source sign discrepancy.
- **Optional boundary clarification:** n=2 gives equality for the selected invariant; n=1 is outside the formula. The stated n>=3 extension is correct.
- **Optional naming precision:** Conjecture 3.8 is a rough-M parametric conjecture, while the fine invariant is separately defined.

The strongest verified result is the explicit broad counterexample and its all-n extension n>=3. The exact remaining gap toward a unibranched or parametric result is the absent central-unibranched hypothesis; no alteration or argument in the package supplies it. There is no unresolved numerical or local-resolution gap in the claimed broad theorem. Novelty and priority remain outside this audit.
