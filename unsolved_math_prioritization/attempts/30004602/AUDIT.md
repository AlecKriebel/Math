# Arrangement-Lefschetz proof audit and correction acceptance

This AI-assisted correction edition is unrefereed. Acceptance records an independent internal AI logical audit, not external human peer review, author-approved erratum, journal acceptance, or formal proof-assistant certification.

The complete symbolic proofs, analytical formulas, and all-degree examples are retained. This is not a computational reproduction package: executable code, raw datasets and computational certificate tables, copied source documents and images, and private coordination material are excluded. Historical finite checks are corroboration only. The universal conclusions rest on the written arguments and explicitly named standard dependencies. The historical computations cannot be reproduced from this edition alone.

The characteristic-zero arrangement theorem survives with an explicit proof correction. The published proof is rejected unchanged. No new theorem, target counterexample, novelty, priority, current-openness, or complete current-literature-audit claim is made.

This edition preserves two complete authored reviews in chronological order. Part I records the original rejection and its then-pending repair; that historical pending language is superseded by the acceptance in Part II. The corrected proof is PROOF.md. No new mathematical execution or scholarly-source inspection occurred during editorial preparation.

## Part I. Original defect audit, historical pre-acceptance report

# Audit of the published arrangement-Lefschetz resolution

## Decision

**Do not accept the published proof unchanged.** The claimed characteristic-zero theorem matches the target, and the passage from WLP to 3-WLP is valid. However, Corollary 3.7 in the published Marchesi-Palezzato-Torielli paper is false, even for an essential arrangement of four planes. The published proofs of Theorems 3.3, 4.7, and 4.10 route through that corollary. A fully written correction candidate, using the paper's valid vector-bundle bounds and a weaker saturation inequality, is supplied separately. It requires independent review before any acceptance or public assertion that this audit closes the target.

This is a prior-result/proof-correction audit. It is not a claim of a new theorem, a counterexample to the target, or a claim that the target is open. The later paper is a published claimed resolution. The counterexample below concerns a stronger intermediate assertion in its printed proof.

## Target and source identity

Let K be a characteristic-zero field, S=K[x,y,z] with the standard grading, and A a finite set of distinct central hyperplanes. Let Q be the product of their defining linear forms and J=(Q,Q_x,Q_y,Q_z). The target is 3-WLP of S/J: three successive linear forms each induce maximal-rank degree-one multiplication after the preceding forms are killed. It is not multiplication to the third power, and it does not mean an Artinian reduction of S/J alone.

For nonempty arrangements, Euler's identity removes Q from the generators because |A| is invertible. Repeated hyperplanes/multiarrangements are not included. The empty arrangement, with Q=1, has zero quotient. There is no assertion in positive characteristic or for nonstandard gradings.

Sources:

1. E. Palezzato and M. Torielli, the report on k-Lefschetz properties in *Logarithmic Vector Fields and Freeness of Divisors and Arrangements*, Oberwolfach Report 5/2021, printed pp. 233-235, PDF pp. 9-11. Theorem 10 states the generic-initial-ideal equivalence; Conjecture 11 is the exact target. Characteristic zero and standard grading are standing assumptions on printed p. 233. [Report PDF](https://ems.press/content/serial-article-files/46883).
2. E. Palezzato and M. Torielli, *k-Lefschetz properties, sectional matrices and hyperplane arrangements*, J. Algebra 590 (2022), 215-233, DOI [10.1016/j.jalgebra.2021.10.014](https://doi.org/10.1016/j.jalgebra.2021.10.014). The retained Hokkaido PDF is an accepted-manuscript copy with a repository cover sheet, not the publisher's typeset pages. Manuscript p. 8 is PDF p. 9, and manuscript p. 17 is PDF p. 18. Its Proposition 8.5 gives the sufficient implication, and Corollary 4.9 upgrades WLP to 3-WLP. [Repository copy](https://eprints.lib.hokudai.ac.jp/repo/huscap/all/91057/J.%20Algebra%20590_215-233.pdf).
3. S. Marchesi, E. Palezzato and M. Torielli, *Lefschetz properties and the Jacobian algebra of 3-dimensional hyperplane arrangements*, Port. Math. 83 (2026), 1-18, DOI [10.4171/PM/2155](https://doi.org/10.4171/PM/2155). The retained copy is the published typeset article. Theorem 4.7 is on p. 14; Theorem 4.10 is on p. 15. [Published PDF](https://ems.press/content/serial-article-files/52275).
4. A. Dimca and D. Popescu, *Hilbert series and Lefschetz properties of dimension one almost complete intersections*, Comm. Algebra 44 (2016), 4467-4482. For the cited dependency we retrieved and inspected author preprint [arXiv:1403.5921v2](https://arxiv.org/abs/1403.5921v2), especially pp. 12-13. We do not claim that this is a page-by-page inspection of the 2016 publisher version.

## Exact published bridge

The OWR report and the 2022 article use x1,x2,x3. The 2026 article uses x0,x1,x2. Under the order-preserving reindexing

(x1,x2,x3)_old = (x0,x1,x2)_new,

the condition is identical: if p0 is the least exponent with the middle-variable power in rgin(J), every minimal generator divisible by the last variable has degree at least p0.

In the 2026 paper, the printed implication chain is

Theorem 3.3 -> Corollary 3.8 -> Theorem 4.7,

where Theorem 3.3 itself uses Lemma 2.7 and Corollary 3.7. Theorem 4.10 is another application of Theorem 3.3, restricted in its statement to essential arrangements. The OWR Theorem 10 then supplies 3-WLP. The 2022 Proposition 8.5 plus Corollary 4.9 supplies the forward implication without needing the OWR equivalence as an unexplained black box.

The upgrade is substantial in its definition but automatic in three variables: after the first Lefschetz form the quotient has at most two variables; every standard-graded homogeneous quotient of K[u,v] has 2-WLP (indeed 2-SLP). The 2022 article proves this in Theorem 4.7 and immediately obtains Corollary 4.9. None of these statements assumes the original algebra is Artinian.

The elementary monomial reconstruction and the nonessential cases appear in PROOF.md. They show that there is no unresolved variable-indexing, 3-WLP, or nonessential gap in the bridge itself.

## Definitive failure of Corollary 3.7

On published p. 12, Corollary 3.7 concerns the map with source H^1(T(i)) and target H^1(T(i+1)). Its relevant exact phrase is: "is surjective for any i ≥ deg(F)." Here p=deg(F) is the stabilization degree of S/J^sat, not a Jacobian generator degree or the generic-initial threshold p0.

Take K=Q and

Q=xyz(x+y+z),  s=x+y+z,
J=(yzs+xyz, xzs+xyz, xys+xyz).

This is an essential central arrangement of four distinct planes. All three generators have degree 3, so (d0,d1,d2)=(3,3,3), D=9. The six projective singular points are

[0:0:1], [0:1:0], [1:0:0], [0:1:-1], [1:0:-1], [1:-1:0].

At each point exactly two lines meet transversely. Locally Q is a unit times the product of two regular parameters, and its Jacobian ideal is the maximal ideal of that reduced point. There are no other projective singularities. Consequently J^sat is the vanishing ideal of these six reduced points.

### The saturated ideal from first principles

Put q0=yzs, q1=xzs, q2=xys, q3=xyz. Then

J^sat=(q0,q1,q2,q3).

To verify generation without software, restrict any homogeneous polynomial f vanishing on the six points to x=0. Its restriction vanishes at the three distinct points y=0, z=0 and y+z=0, so is divisible by yz(y+z). Subtract an appropriate multiple of q0 and write the remainder xg. The other three points, in the independent coordinates y,z,s, are the three coordinate points, whose ideal is (yz,ys,zs). Thus xg lies in (q3,q2,q1). This works degree by degree and includes the absence of nonzero degree-2 forms.

Equivalently, the degree-2 evaluation map at the six points is an isomorphism: the three coordinate points determine the coefficients of x^2,y^2,z^2, while the other points then determine yz,xz,xy. The saturated Hilbert function is therefore

1, 3, 6, 6, 6, ... .

For the tail, choose ell=x+2y+3z, which is nonzero at every one of the six points; multiplying degree-2 interpolation forms by powers of ell preserves surjectivity of evaluation. Thus its Hilbert numerator is F=1+2t+3t^2 and p=deg(F)=2.

### The torsion module exactly

The four qj are linearly independent cubics, while J_3 is spanned by q0+q3,q1+q3,q2+q3. Hence N=J^sat/J is generated by the nonzero cubic class of q3. The identities

x q0 = y q1 = z q2 = s q3 = Q

imply that q3 is killed by 2x+y+z, x+2y+z and x+y+2z. Their coefficient matrix has determinant 4. Thus x,y,z all kill q3 and

N is isomorphic to K(-3).

This determines every degree, not merely a finite experimental prefix. In particular N_2=0 and dim N_3=1, so for every linear form the map

N_2 -> N_3

has rank zero and is not surjective. Its source is i=2=p. This contradicts Corollary 3.7 exactly within its hypotheses. Via N_i=H^1(T(i)), it is the same map used in the corollary.

The quotient S/J has Hilbert function 1,3,6,7,6,6,... . In particular its degree-2 to degree-3 map cannot be surjective either; the printed proof of Theorem 3.3 also asserts surjectivity there. Yet the quotient has WLP: multiplication by the above ell is injective before degree 3 and surjective from degree 3 onward. This is no counterexample to WLP or 3-WLP.

An independently authored exact rational matrix check agrees with every dimension and all multiplication ranks through source degree 7. No author-provided computational code was used. The infinite-degree assertions above have independent algebraic proofs and do not rest on that finite check.

## Why the cited dependency does not repair the printed statement

Dimca-Popescu's inspected preprint Theorem 4.1 gives torsion surjectivity starting at

floor((d0+d1+d2-3)/2),

which is 3 in the four-line example, not p=2. Its Corollary 4.2 separately discusses when that threshold also works for the entire quotient. It does not supply the stronger p-threshold asserted in the 2026 Corollary 3.7.

There are two further cautions in the printed argument:

- The first paragraph of the proof of Corollary 3.7 prints an inequality for the nonstable case which is incompatible with the preceding equality and strict instability. The useful unstable injectivity bound is nevertheless correctly available in Proposition 3.6 and does not need that inequality.
- On p. 9 the equality p=D-m-2 is stated with m the minimum degree of any syzygy. That equality is not valid for all the dimension-one almost complete intersections of Section 3.2. For example J=(x^2,y^2,xz^4) has (d0,d1,d2)=(2,2,5), D=9, minimum syzygy degree m=4, and J^sat=(x,y^2), so p=1, whereas D-m-2=3. A Koszul relation can be the first syzygy. The weaker inequality p<=D-m-2 is valid and sufficient; the correction candidate proves it directly, bypassing this issue entirely.

## Proof components reviewed

The full text of the published 2026 article was read. The actual resolution depends on its pp. 3-6 and 8-15; the dimension-at-least-two theorem, plus-one-generated theorem and SLP examples are outside the target and are not certified by this audit. The printed proof of Proposition 3.6 was reconstructed, including the shifts in Serre duality. The usable bounds survive; its sharpness statements for a split bundle are immaterial, because H^1 then vanishes.

For the 2022 article, the relevant sections on definitions, generic initial ideals, k-WLP, two-variable quotients, and the arrangement implication were read. Its full sectional-matrix development is not needed and is not certified. The OWR equivalence has been reconstructed in the correction rather than accepted only from its label.

The correction expressly retains standard named black boxes: Serre duality and line-bundle cohomology on projective space; the generic-line restriction theorem for semistable rank-two bundles in characteristic zero (Grauert-Mulich); existence/strong stability of generic initial ideals and reverse-lex generic-hyperplane-section Hilbert-function preservation. Their full original proofs were not independently reproved or fully source-audited here. The exact uses are listed in the candidate.

## Final disposition

Published theorem located; target matches. Published proof as printed fails this audit. A correction candidate covering essential/nonessential arrangements, arbitrary characteristic-zero fields, and 3-WLP is attached for independent checking. No acceptance is recorded here, and no repository or external publication action was performed.

## Part II. Independent logical acceptance of the correction

# Independent acceptance review of the corrected arrangement-Lefschetz proof

## Decision and exact scope

**ACCEPT the corrected proof for the characteristic-zero arrangement target. REJECT the published proof unchanged. No further mathematical repair of the supplied correction is required.**

The accepted target is this: for a characteristic-zero field K, the standard-graded quotient K[x,y,z]/J(Q) of a finite central arrangement of distinct hyperplanes has 3-WLP. Here J(Q) includes Q and its three partial derivatives, and 3-WLP means successive degree-one maximal-rank multiplication after each preceding linear form is killed. Neither Artinianness of the original quotient nor a statement about a third power is substituted for that target.

This review accepts an authored correction of a published claimed result. It does not assert novelty, that the original proof is valid, or that a counterexample to the target has been found. The claims for higher-dimensional arrangements and strong Lefschetz properties in the later paper are outside this decision.

The incoming 37-member manifest, SHA-256 d812c2f0b39d1b0afdc4902e8904e764b5d86a134fca3188a4762f648099da1a, and all its listed member hashes and byte counts were independently verified. The two authored input reports were read in full. No program from the input packet or from a source author was executed. The finite rational computations accompanying this review were written afresh and do not establish the universal theorem; the proof below does.

## 1. Source statements and the specific defect

The published article is Marchesi, Palezzato and Torielli, *Lefschetz properties and the Jacobian algebra of 3-dimensional hyperplane arrangements*, Port. Math. 83 (2026), 1-18, DOI [10.4171/PM/2155](https://doi.org/10.4171/PM/2155). Its [published PDF](https://ems.press/content/serial-article-files/52275), pages 8-12, defines p as the stabilization degree of the saturated quotient and uses source degree i in the torsion multiplication map. Corollary 3.7 claims surjectivity when i>=p. Pages 12-15 use it in the route to the arrangement conclusion. The source-versus-target grading is unambiguous in the rendered source.

The [Dimca-Popescu author preprint](https://arxiv.org/abs/1403.5921v2), Theorem 4.1 and Corollary 4.2, uses the central source threshold floor((D-3)/2), where D is the sum of the three generator degrees. That is not an assertion of torsion surjectivity from source p. No inspection of the 2016 typeset version is claimed.

The [Oberwolfach report](https://ems.press/content/serial-article-files/46883), the Palezzato-Torielli contribution on printed pages 233-235, supplies the characteristic-zero, standard-grading convention and the exact 3-WLP target. The [2022 accepted manuscript](https://eprints.lib.hokudai.ac.jp/repo/huscap/all/91057/J.%20Algebra%20590_215-233.pdf) supplies the generic-section bridge and two-variable result. Its repository cover adds one to manuscript page numbers. The mathematical bridge is reconstructed below, rather than accepted merely from theorem numbering.

### Independent four-line reconstruction

Take K=Q, s=x+y+z and Q=xyzs. The normals to x,y,z span K^3, so the arrangement is essential. All four factors are distinct and central. Euler's identity gives

J=(Q_x,Q_y,Q_z)=(yzs+xyz,xzs+xyz,xys+xyz).

Thus each generator has degree 3 and D=9. The three cubics are independent, and the ideal has height two. The projective singularities are precisely the six pairwise intersections

[0:0:1], [0:1:0], [1:0:0], [0:1:-1], [1:0:-1], [1:-1:0].

There is no triple intersection in P^2. Locally at each point, Q is a unit times the product of two parameters. The localized Jacobian ideal equals the point's maximal ideal: its two local derivatives have independent linear terms, so Nakayama's lemma applies. Away from these six nodes the projective Jacobian ideal is the unit ideal. Its saturation is therefore the reduced six-point ideal.

Put q0=yzs, q1=xzs, q2=xys and q3=xyz. That six-point ideal is (q0,q1,q2,q3). Here is a degree-independent verification. Restrict a homogeneous form h vanishing at the six points to x=0. The restriction vanishes at the three distinct points on that line and so is divisible by yz(y+z); subtract a multiple of q0. The remainder is xg. At the other three points x is nonzero. In the independent coordinates y,z,s those points are the coordinate points, whose homogeneous ideal is (yz,ys,zs). Hence xg belongs to (q3,q2,q1). In degrees below 3 the same argument says h=0; constant-degree cases are immediate.

The degree-two evaluation matrix in the six monomials is nonsingular (the independently reconstructed determinant is 1 with the stated ordering). Indeed, evaluations at the coordinate points determine the square coefficients, and the other three evaluations determine the mixed coefficients. Consequently the saturated Hilbert function is 1,3,6,6,...: to see the full tail, multiply interpolation quadrics by powers of ell=x+2y+3z, which takes the nonzero values 3,2,1,-1,-2,-1 at the six points. Thus F=1+2t+3t^2 and p=2.

The four q's are independent cubics, while J_3 has basis q0+q3,q1+q3,q2+q3. The module N=J^sat/J is therefore generated by a nonzero cubic class q3. The polynomial identities

xq0=yq1=zq2=sq3

show that (x+s)q3, (y+s)q3 and (z+s)q3 vanish modulo J. The coefficient matrix of these three linear forms has diagonal 2 and off-diagonal 1, with determinant 4. Therefore x,y,z annihilate the class and N=K(-3), in all degrees.

In particular source N_2=0 and target N_3=K. For every linear form, N_2 -> N_3 is nonsurjective. This source degree is i=p=2, exactly within the printed corollary. All its standing hypotheses are satisfied. For M=S/J the Hilbert function is 1,3,6,7,6,6,..., so source degree 2 also contradicts the stronger surjectivity assertion in the printed proof of Theorem 3.3.

There is no failure of WLP here. The same ell gives injections through source degree 2, surjections from source degree 3, and isomorphisms from source degree 4. These statements follow in every degree from N=K(-3) and the saturated quotient, not from a truncated rank table. The separate exact-rational reconstruction through source degree 8 agrees. It also gives minimal total syzygy degree m=5, so the corrected semistable threshold is c=3, as it should be.

### The blanket equality also needs replacement

For I=(x^2,y^2,xz^4), D=9 and I^sat=(x,y^2). To check saturation, the localization at z gives (x,y^2), whose projective support is the single point [0:0:1]; algebraically every degree-five monomial times x belongs to I, so x belongs to I^sat. The reverse containment follows because (x,y^2) is saturated. Its quotient has Hilbert function 1,2,2,..., hence p=1.

The relation (y^2,-x^2,0) has total degree 4. No smaller relation exists: the third coefficient would have negative degree and the two relatively prime quadrics have no relation below total degree 4. Thus m=4 and D-m-2=3, not 1. This is within the height-two, three-generator setting of Section 3.2. The weaker inequality used by the correction is essential to the stated generality.

## 2. Reconstruction of the corrected cohomological proof

All geometric arguments in this section are initially over an algebraically closed characteristic-zero field. Let I=(f0,f1,f2) have height two, with positive generator degrees d0,d1,d2 and D their sum. Let Z be its nonempty finite projective scheme, A=S/I^sat, M=S/I, and N=I^sat/I.

### 2.1 The syzygy bundle and saturation degree

Sheafification gives

0 -> T -> E=O(-d0) direct_sum O(-d1) direct_sum O(-d2) -> I_Z -> 0.

T is locally free of rank two. At a point of Z the local ring is regular of dimension two. The finite-colength ideal has projective dimension at most one, so the kernel of a free presentation is projective, hence free locally; off Z the claim is immediate. Since I_Z agrees with O outside finitely many points, det(T)=O(-D). For a rank-two bundle the exterior-product pairing gives T^*=T(D).

Let m be the least twist with H^0(T(m)) nonzero. Line-bundle H^1 vanishing on P^2 and the equality H^0(I_Z(i))=(I^sat)_i give multiplication-compatible identifications

H^1(T(i))=(I^sat/I)_i=N_i.

Saturation eliminates the irrelevant associated prime of A. Since A has dimension one, a linear form avoiding the finite projective support is A-regular. Its multiplication is injective in every degree. The Hilbert function is thus nondecreasing and eventually equals length(Z). Let p>=0 be its first stabilization degree.

**Key inequality:** p<=D-m-2.

To prove it without the disputed equality, set t=p-1. If p>0, H^1(I_Z(t)) has positive dimension length(Z)-dim A_t. If p=0, t=-1, and the same nonvanishing follows from H^0(O(-1))=0 and length(Z)>0. The long cohomology sequence injects this group into H^2(T(t)), because H^1(E(t))=0. Serre duality then gives a nonzero section of

T^*(-t-3)=T(D-p-2).

Minimality of m proves the inequality. This proof handles p=0 explicitly, contains no regularity off-by-one, and does not distinguish Koszul from non-Koszul syzygies. Equivalently, p is reg(A), but no regularity formula is needed here.

### 2.2 Duality on multiplication

For mu_i: H^1(T(i)) -> H^1(T(i+1)), its dual is multiplication in the opposite pair of Serre-dual twists:

H^1(T(D-i-4)) -> H^1(T(D-i-3)).

Thus mu_i is surjective exactly when mu_(D-i-4) is injective. The -4 comes from twisting the target by -(i+1) and then by the canonical bundle O(-3). It is not D-i-3 for the source. Naturality of Serre duality makes the form the same ell; this does not require independently chosen lines for the two maps.

### 2.3 Split and strictly unstable cases

If T splits, H^1(T(i)) vanishes for every i. Hence N=0 and M=A, and a general ell is injective in every degree. This includes split semistable and split unstable bundles; no sharpness claim is made.

Suppose T is nonsplit and unstable. Then m<D/2. For completeness, a saturated rank-one destabilizing subsheaf of a vector bundle on the smooth surface is a line bundle: its quotient is torsion-free and the depth lemma makes the subsheaf reflexive. Every line bundle on P^2 is O(a). A destabilizing O(a) yields a section with m<=-a<D/2. Conversely, such a minimal section destabilizes.

A minimal section has no divisorial zero locus, since removing a divisor of positive degree lowers its twist. Consequently

0 -> O(-m) -> T -> I_Y(m-D) -> 0

for a finite scheme Y. Y is nonempty; otherwise the extension splits since H^1(O(D-2m))=0. Choose one general line L avoiding Y and Z. On L the extension splits, again by line-bundle cohomology, and

T|L=O_L(-m) direct_sum O_L(m-D).

For t<=D-m, H^0(I_Y(t+m-D))=0, including t=D-m because Y is nonempty. Thus all sections of T(t) come from O(t-m) in this range. In

0 -> T(i) --ell--> T(i+1) -> T|L(i+1) -> 0,

the second line summand has no sections when i<=D-m-2. Sections of the first summand lift by restriction of plane polynomials. The connecting homomorphism to H^1(T(i)) is zero, giving injectivity of mu_i for i<=D-m-2. Duality gives surjectivity for i>=m-2, since

D-i-4<=D-m-2 if and only if i>=m-2.

Set c=max(p,m-2). The key inequality bounds p by D-m-2. Strict instability gives m-2<=D-m-2 (indeed strictly). Hence c<=D-m-2. For every i<c multiplication on N is injective; for every i>=c it is surjective and multiplication on A is bijective because c>=p. This is the required overlap, with no central-threshold assumption on p.

### 2.4 Semistable cases, including equality

Semistability implies m>=ceil(D/2), by applying the slope inequality to the line subsheaf from a section. The general-line Grauert-Mulich splitting is balanced. There are two cases.

- D=2r: T|L=O_L(-r)^2. H^0(T|L(i+1))=0 for i<=r-2, giving injectivity there. Duality gives surjectivity for i>=r-2. Take c=r-2=floor((D-3)/2). The key inequality gives p<=r-2=c.
- D=2r+1: T|L=O_L(-r) direct_sum O_L(-r-1). The same H^0 vanishing gives injectivity for i<=r-2. Duality gives surjectivity for i>=r-1. Take c=r-1=floor((D-3)/2). Now p<=r-2<c.

Thus in either parity multiplication on N is injective for i<c and surjective for i>=c; multiplication on A is bijective for i>=c. Equality m=D/2 belongs to the even semistable case and is fully covered. The inequalities and p>=0 ensure c>=0 whenever this case occurs. In even degree both directions hold at c, which merely says the map there is an isomorphism. In odd degree there is no missing integer between r-2 and r-1.

The reconstructed ranges also encompass the weaker Dimca-Popescu central ranges: in the unstable case D-2m>=1 places its injective and surjective bounds on either side of that center. However the stronger unstable overlap above is what accommodates p larger than the center. The repair does not need Dimca-Popescu as an additional theorem.

### 2.5 Transfer to M

Apply ell to 0 -> N -> M -> A -> 0 in consecutive degrees. Since the map on A is injective, the Snake lemma identifies ker(mu_N) with ker(mu_M) and gives

0 -> coker(mu_N) -> coker(mu_M) -> coker(mu_A) -> 0.

Below c the first kernel vanishes. At and above c both outer cokernels vanish. Hence every degree-one multiplication map on M has maximal rank. The split case was already covered. The corrected height-two, three-generator theorem follows.

No unsupported universal assertion of surjectivity at i=p has reentered the proof.

## 3. Arrangement hypotheses and degenerate cases

For an essential arrangement with d planes, Euler's formula gives J=(Q_x,Q_y,Q_z), with common positive degree d-1. A common irreducible divisor of all partials would, by Euler, divide the squarefree product Q. At the generic smooth point of that factor's plane, a normal derivative is nonzero, a contradiction. Thus J has height at least two. Every pairwise intersection line lies in its affine zero set, so its height is exactly two.

The partials are linearly independent. If a constant-direction derivation delta annihilates Q, reduction modulo each distinct factor alpha shows that the constant delta(alpha) is zero. Essentiality says that the intersection of the kernels of these linear forms is {0}, so delta=0. Thus the application meets the claimed three-generator hypotheses without zero derivatives or redundant generators. The projective scheme is nonempty because there are pairwise intersections.

For rank two, make a linear coordinate change over K so Q lies in K[x,y]. Then S/J=(K[x,y]/(Q_x,Q_y))[z]. Multiplication by z is injective in all degrees. Killing z leaves a two-variable homogeneous quotient, which has 2-WLP by the next section. This already gives 3-WLP. No height-two syzygy argument or empty minimum is forced onto a degenerate case.

A rank-one arrangement of distinct central hyperplanes has one member, so a partial derivative is a nonzero constant and J=S. For the empty arrangement Q=1 also gives J=S. The zero quotient satisfies maximal rank trivially. Multiarrangements and positive characteristic are not covered.

## 4. Two-variable, 3-WLP, and generic-initial bridge

### 4.1 Two variables

Let B be strongly stable in K[u,v], u>v. A nonzero monomial kernel for multiplication by v from degree k to k+1 supplies a minimal generator t dividing v times the source monomial. Since t does not divide the source, it involves v; its degree a is at most k+1. Strong stability implies u^a in B, hence u^(k+1) in B. The cokernel in degree k+1 is spanned by that sole pure-u monomial and is zero. Thus the map cannot have both nonzero kernel and cokernel and always has maximal rank. Killing v leaves a quotient of K[u], whose multiplication by u plainly has maximal rank. The zero ideal and unit ideal cases also satisfy this argument or are immediate.

For an arbitrary homogeneous ideal, use its characteristic-zero reverse-lex generic initial ideal. Generic-section Hilbert functions agree with those for killing the last coordinate variables. For any graded quotient R,

rank(ell:R_(d-1)->R_d)=dim R_d-dim(R/ell R)_d.

Therefore these equalities give the needed equality of generic multiplication ranks, degree by degree and successively. This proves the two-variable 2-WLP statement, without assuming the quotient is Artinian or using the stronger 2-SLP claim as a black box.

### 4.2 WLP to 3-WLP

A Lefschetz linear form for a homogeneous quotient of K[x,y,z] leaves a homogeneous quotient of a polynomial ring on at most two variables. Apply the previous argument to choose the next two forms and lift them. Conversely, 3-WLP includes WLP in its definition. Thus the exact target, and not only a first-step property, follows.

### 4.3 Monomial condition and equality boundary

Let B=rgin(J) be a proper height-two ideal in K[x,y,z], with x>y>z, and put p0=min{p:y^p in B}. This minimum exists: a strongly stable height-two monomial ideal cannot be contained in (x), and any monomial in it not divisible by x yields a pure y-power by strong stability.

If every minimal generator involving z has degree at least p0, multiplication by z into target degree d<p0 is injective. Otherwise a kernel monomial would supply such a generator of degree at most d. Into d>=p0 the map is surjective: strong stability of y^p0 puts all degree-d monomials in x,y into B.

Conversely, a minimal z-divisible generator t of degree g<p0 produces a nonzero kernel class t/z in source degree g-1 and a nonzero cokernel class y^g in target degree g. This contradicts WLP after the generic-section rank transfer. Equality g=p0 is allowed; the cokernel then vanishes. The variable reindexing (x1,x2,x3) to (x0,x1,x2) preserves the middle-power and last-variable roles exactly.

This independently proves the required equivalence with 3-WLP. It is consistent with the 2022 manuscript's four-line Example 7.5, which gives a last-variable generator of degree equal to the middle-power threshold. That corroboration is not used to prove the counterexample or the repair.

## 5. Arbitrary characteristic-zero fields and finite openness

Every characteristic-zero field K is infinite. For the first multiplication form, work after algebraic closure as above. N has finite length; choose q such that N_i=0 for i>q. On the open set of forms avoiding Z, the maps on A are isomorphisms from p onward. Thus the maps on M are automatically isomorphisms from source max(p,q+1) onward. Only finitely many other maximal-rank conditions remain. Each is given by nonvanishing of suitable minors of matrices over K. Their intersection with the support-avoidance open set is a nonempty K-defined Zariski open, so it has a K-point. No uncountable-field hypothesis is needed.

For essential arrangements the resulting quotient by the first form is Artinian, making the remaining checks manifestly finite. More generally the two-variable argument uses the single nonempty coordinate-change open defining a gin and its generic sections; it is not a countable intersection of unrelated degree-wise opens. Hence the successive choices can also be made over K. Rank-two coordinate changes are ordinary K-linear algebra. The optional regularity-truncation result in the candidate is unnecessary for this descent, so this review does not depend on certifying its full SLP version.

## 6. Dependency and acceptance boundary

The accepted proof retains the following conventional mathematical inputs, with precisely these uses:

1. Cohomology of line bundles on P^1 and P^2, Serre duality with canonical bundle O(-3), and its compatibility with multiplication. These give the saturation inequality, splitting calculations, and duality shift.
2. Standard local commutative algebra on a smooth surface: depth, Auslander-Buchsbaum/projective resolutions, and reflexive rank-one sheaves; together with Pic(P^2)=Z, they justify the vector bundle and destabilizing line subbundle constructions.
3. The characteristic-zero Grauert-Mulich general-line theorem for rank-two semistable bundles on P^2, only to conclude balanced splitting. The later paper cites Okonek-Schneider-Spindler, *Vector bundles on complex projective spaces*, II, Corollary 2. Its foundational proof is not independently reproduced or fully source-audited here.
4. Existence and strong stability of characteristic-zero generic initial ideals and reverse-lex preservation of Hilbert functions of generic linear sections. The 2022 paper's Theorem 3.6 invokes Conca, *Reduction numbers and initial ideals*, Proc. AMS 131 (2003), Lemma 1.2. Their exact rank consequences and the needed monomial assertions are proved above; the foundational original papers are not fully re-audited.
5. Basic sheafification/saturation and finite-generation facts, and existence of K-points in nonempty K-defined affine open sets over an infinite field.

These are explicitly bounded named dependencies, not gaps hidden by computations. Neither the false Corollary 3.7 nor the blanket equality p=D-m-2 is a dependency. The Dimca-Popescu result is used only to check the erroneous citation's scope. No claim is made to verify the whole 2022 or 2026 article, all their cited literature, strong Lefschetz assertions, or original-source code.

**Final acceptance:** the incoming correction's universal proof, all boundary cases needed for the exact arrangement target, and its 3-WLP/generic-initial bridge are valid with these standard inputs. The published argument must be credited with this explicit correction, rather than described as accepted unchanged. There is no remaining mathematical blocker in the supplied candidate.
