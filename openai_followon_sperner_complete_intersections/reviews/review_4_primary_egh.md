# Fresh primary audit of the necessary family-200 EGH dependency

Audit completed: 2026-10-07 UTC. Reviewer: fresh independent audit child `primary_egh` of complete-package review 4. Assigned primary-dependency audit completion: 100%. This percentage describes the completed review scope, not an independent new discovery or the state of the entire publication project.

## Scope and verdict

**Verdict: no substantive mathematical issue found in the necessary primary EGH argument.** I reconstructed the deductions from the pinned primary TeX sources, rather than treating their theorem statements as certificates. The audited construction gives the full-complex-Artinian EGH Hilbert-function statement, and the finitely generated coefficient-field argument gives the required full-Artinian statement over every characteristic-zero field. The full lex-plus-powers Betti theorem is unnecessary for this conclusion and was not audited in full here.

The exact necessary result is: if $F$ is any field of characteristic zero, $n\ge1$, $2\le a_1\le\cdots\le a_n$, and a homogeneous ideal $I\subset F[x_1,\ldots,x_n]$ contains a homogeneous regular sequence $f_1,\ldots,f_n$ of degrees $a_i$, there is one monomial ideal $J$ containing each $x_i^{a_i}$ with

\[
\dim_F(F[x]/J)_d=\dim_F(F[x]/I)_d\quad\text{for every }d\ge0.
\]

This audit makes no assertion about a stronger Lefschetz property, positive characteristic, nongraded complete intersections, the all-ideal Sperner reduction, novelty, publication metadata, or a machine formalization. Those are separate review scopes. Within this scope, the exact remaining primary-proof gap is **none identified**. The proof uses named standard results in coherent cohomology, determinant of cohomology, Riemann--Roch, complex topology, and integral topological $K$-theory; the critical cited topology and $K$-theory interfaces were checked directly as described below.

## Independence and audited input

I read `/Users/alec/Documents/Math/AGENTS.md` and `PROJECT_BRIEF.txt`. Before reconstructing the necessary deductions I did not read the project root README, theorem-status file, research log, any existing complete-package review, response record, `review*.json`, packaged scoped audit, or dependency ledger. I did not consult those records later either. No primary source was edited, no modifying Git operation or publication action was performed, and no external person was contacted. An attempted narrow topology-reference subagent could not be spawned because the available agent slots were already occupied; I completed that reference check myself.

The upstream checkout reports exactly commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The relevant source directory was clean on inspection. All eleven copied EGH primary files (`paper.tex`, bibliography, and sections 01--09) matched the read-only upstream files byte for byte.

Use the following absolute directory as the base for the line references in this report:

`/Users/alec/Desktop/math/preprints/Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026/build/`

Audited primary ranges:

| File | Ranges read and proof roles checked |
| --- | --- |
| `paper.tex` | 1--84: source assembly and exact stated scope |
| `sections/01-introduction.tex` | 1--299, especially 33--110 and 285--299: construction, EGH scope, field embeddings and conventions |
| `sections/02-reduction.tex` | 1--163: full ordered basis and one monomial ideal |
| `sections/03-low-relations.tex` | 1--440: low-degree induction data, simple-factor lemma, initial division algebra, bounded-curve exclusion and finite-extension preservation |
| `sections/04-parameters.tex` | 1--342: joins, parameter integrality, singular codimension, integral homology and connectivity |
| `sections/05-curves.tex` | 1--439: connected étale cover, genuine linearization, matrix pencils, free degree-one Picard action and character maps |
| `sections/06-descent.tex` | 1--422: semilinear algebra descent, coherent extension, determinant correction, mixed Picard pairing and torsor Euler characteristic |
| `sections/07-index.tex` | 1--476: equivariant maps, integral $K$-pushforward, section comparison, congruences and genuine division |
| `sections/08-assembly.tex` | 1--382: finite Veronese extension, invariant sum, coefficient nonvanishing, binary substitutions, descent and completed induction |
| `sections/09-consequences.tex` | 1--47: coefficient-field descent; only the full-length case is needed |
| `bibliography.tex` | Relevant entries for Hamm--Lê, Hatcher, Schnürer--Soergel, Stacks, determinant of cohomology and Riemann--Roch |

I also checked, without using them as a substitute for the companion proof, the exact interface in `/Users/alec/Desktop/math/preprints/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026/build/sections/01-forms.tex:1--48` and its coefficient-field passage in `sections/08-characteristic-zero.tex:1--85`. The first expressly imports the same companion construction. I did not rely on its Betti-transfer sections.

## Reconstructed mechanisms and falsification attempts

### 1. The ordered-basis implication really concerns the full polynomial algebra

In section 02:38--98, let $k$ be the current center and write $N=\Delta[x]$, regarded as a right module over the commutative algebra $A$. As a $k[x]$-submodule of the finite free module $N$, $A$ is finite; $N$ is also finite over $A$. The central variables give depth $n$ at the homogeneous maximal ideal and the support dimension is at most $n$, so the localized module is Cohen--Macaulay of dimension $n$. The triangular identities, read in increasing row order, imply that every common zero of the $t_i$ has all $f_i$, then all $x_j$, zero. Finiteness makes $A/(t)$ zero-dimensional. The $N$-quotient retains its nonzero degree-zero part, so it has support dimension zero at that maximal ideal. The Cohen--Macaulay module system-of-parameters theorem therefore makes the $t_i$ regular on $N$.

The homogeneous localization argument is valid: an element outside the graded maximal ideal has nonzero degree-zero scalar, which cannot annihilate the lowest nonzero degree of a homogeneous kernel. Multiplication of Hilbert series by $(1-t)^n$ then leaves precisely $\dim_k\Delta$ in degree zero. Consequently all positive degrees are spanned by right multiplication by the $t_i$. They commute as whole forms, so induction spans by ordered $t^\alpha$; the cardinality in degree $d$ equals the left $\Delta$-dimension of $N_d$. This gives independence and the full basis, without bounding the exponents.

I directly checked [Stacks Proposition 10.103.4, Tag 00N6](https://stacks.math.columbia.edu/tag/00N6): its Cohen--Macaulay **module** statement applies to the dimension drop used here. The algebra itself need not be assumed Cohen--Macaulay.

Section 02:116--154 then extends $I$ to the two-sided ideal $\Delta I$. Using **least** exponents in reverse coordinate order is deliberate and correct. Right multiplication by $t_j$ translates exponents and leaves left coefficients untouched. Elimination over a division algebra gives exactly one pivot exponent per left dimension in each degree. The triangular relation has pivot $a_i e_i$, because every remaining term has a positive coordinate of higher index. All degrees therefore define a single upward-closed exponent set, with the desired pure powers and the whole Hilbert function. This step does not need coefficients within a form to commute.

### 2. Low relations avoid transferring the difficulty to a simple-factor assumption

Section 03:73--92 proves base-point-freeness of the actual stage ideal piece using only generators of degree at most $b$, previously retained rows, finiteness and regularity. In 127--212 the annihilator condition produces genuine differential equations for every linear or quadratic generator of $Q$. A repeated nonlinear factor has its projective gradient in the characteristic set. Restricting a nonconstant gradient to a transverse plane curve bounds the image degree by $\deg(p)(\deg(p)-1)\le b(b-1)$, contradicting the no-small-curve property. A constant gradient forces the irreducible factor to be linear. If all factors are repeated linear factors, logarithmic differentiation puts the ambient gradient of the product in the same characteristic set. Restriction to a line again produces a forbidden low-degree curve unless the polynomial is a pure power. That pure power contradicts the base-point-free annihilator condition. Thus the factor hypothesis used in section 04 is deduced, not assumed.

The initial data in 291--395 are concrete. The skew Laurent domain becomes a finite-dimensional division algebra after central localization. Even row length makes its center precisely the square-parameter field. Different rows commute and yield jointly independent generic quadrics. For a hypothetical bounded-degree curve, its Chow coefficients contribute a uniformly bounded transcendence degree. The greedy block count retains at least $m-d_*$ jointly generic full quadric coefficient blocks over a field of definition of its image. Their reduced pairwise disjoint divisors give independent squareclasses by valuations. The cover degree is at least $2^{m-d_*}>D$, incompatible with the curve's ambient degree. This remains valid over algebraically closed extensions: generic divisor conditions are imposed over the curve's field of definition and persist after extension. The $n=1$ case instead has a finite projective set and auxiliary forms ensure $\dim U\ge3$.

The finite homogeneous enlargement in 404--426 cannot introduce a bounded-degree curve: the projective map is finite, everywhere defined, and preserves the hyperplane bundle. Curve degrees upstairs equal map degree times image degree. This is precisely the induction invariant later used in section 08.

### 3. The parameter topology allows nonisolated singularities

Section 04:34--72 proves the join statement using an explicit two-open-set cover of $f+g=1$. The half-plane roots exist globally on those two sets and on their intersection. Their contractions preserve the half-plane inequalities. A simple factor gives a meridian generating the cyclic-cover monodromy, hence a connected nonzero level. The join homology range is integral, including possible torsion, and gives vanishing through $2M-2$.

The Jacobian incidence bound in 122--153 is enough to show every component has the expected dimension and is generically smooth; complete-intersection Cohen--Macaulayness then gives reducedness. It does not assume integrality before proving it. For $s\ge1$, the complement incidence space has contractible affine fibers over the complement, and a smooth submersion to $\mathcal O_{\mathbf P(W)}(1)^\times$. The proper-support Leray calculation uses fiberwise compact-support cohomology rather than asserting that this submersion is a fiber bundle. I checked the potential nonproper-family failure explicitly: the cited [Schnürer--Soergel Theorems 5.9 and 5.10](https://ems.press/content/serial-article-files/43914) do supply derived composition and the stalk base-change statement for these locally compact Hausdorff spaces. Their Corollary 2.11 supplies the relevant locally proper/separated hypotheses. Complex orientation trivializes the top compact-support direct-image sheaf by a local submersion chart; no lower-row local constancy is required.

Set $d=N_*-s$, $c=M-2s+1$, $\kappa=M+2h$. The two essential inequalities are

\[
2s+\kappa-1\le2M-2,\qquad \kappa\le2c-2.
\]

Both follow from $M\ge2h+4s+10$. The first transfers complement homology to the closed cone; the second permits removing its singular subset and origin without changing compact-support cohomology in the needed range. Duality gives $H_0(Y^o)=\mathbf Z$ and vanishing through $\kappa$. Connectedness of the smooth locus then proves one irreducible component, not conversely.

I checked [Hamm--Lê, Theorem 1.1.3(ii), printed p. 126](https://www.numdam.org/article/BSMF_1985__113__123_0.pdf) directly. Its smooth-open hypothesis and general-hyperplane cell statement match section 04:287--314. At each successive section the deleted subset is intersected as well. The final general surface avoids it because its codimension is greater than $h\ge2$. A smooth complete-intersection surface has trivial fundamental group by the smooth flag and projective Lefschetz argument given in the text. The unit-circle-bundle exact sequence then makes the cone's fundamental group abelian; its already proved $H_1=0$ makes it trivial. Hurewicz now legitimately upgrades the integral homology range to connectivity. The special $s=0$ sphere case is handled separately in 117--119.

### 4. Picard descent does not mistake a matrix algebra for a division algebra

Section 05:101--210 constructs a connected Kummer cover for arbitrary, including composite, $b$: the detecting valuations are one, so the subgroup is genuinely free over $\mathbf Z/b$. The auxiliary cyclic cover is disjoint from it because all its nontrivial subextensions ramify at the additional branch point. Local index $b$ at the common branch points cancels upon normalization, making the resulting $G$-cover étale. The degree-$b$ linearization descends through the diagonal scalar subgroup exactly; this is a genuine group-law linearization, not merely projective transport. The genus and degree formulas give $\deg(A L^{g_T-1})=g(C)-1$, including $b=2$, where the genus is one.

Generic noneffectivity and Riemann--Roch make $\pi_*(A L^{g_T})$ a trivial rank-$e$ bundle. Its multiplication matrices preserve the curve identities. Coefficientwise commutativity is not claimed within one link. The two Picard roles are distinguished correctly: cyclic-subgroup descent forbids a stabilizer on (\operatorname{Pic}^1), while lifted integral periods and the Abel-map lattice isomorphism produce maps for every prescribed character.

Section 06:81--98 descends only to a central simple algebra initially. The actual proof of division is deferred to the module-rank argument. I directly checked [Stacks Tag 0CDR](https://stacks.math.columbia.edu/tag/0CDR): semilinear finite-Galois descent supplies the vector-space descent; multiplication and the unit descend as compatible maps, so the algebra assertion follows.

For an arbitrary module of reduced rank $r$, Morita tensoring leaves rank $e_0r$ with right $\Delta_0$-action and scalar weight one in each degree-zero universal line. The coherent lattice extension is the finite sum of corrected translates inside rational sections, so it preserves that generic module and its composition law. The determinant line in 202--267 has weights

\[
(-\chi(AV)+\chi(A),-\chi(AV)+\chi(V))=(-1,0),
\]

which cancels precisely the first scalar ambiguity and leaves none from the auxiliary degree-one universal lines. The group law follows from functorial composition; it is not obtained merely by cancellation at isolated points. Derived restriction at the fixed origin of $R$ is legitimate through its finite Koszul resolution. It does not require flatness of the chosen lattice over $R$.

In 289--344 the first Chern class of the correction is $-q_*(av)$. Normalization and degrees remove pure-factor terms; the remaining mixed integral lattice matrix is unimodular. To saturate the degree-one Picard factors one must also saturate the degree-zero factors, so every positive-degree Chern-character term of the residual class vanishes upon integration. The determinant is a unit, hence the fiber Euler characteristic is exactly $\pm r$, not $r$ times an uncontrolled integer.

The proof of the torsor Euler formula in 353--385 covers singular $X$: the rank-zero difference of finite pushforward lowers the support filtration, is nilpotent, and its pullback vanishes. The projection formula gives $(a+d)d=0$. Rationally invert $a+d$; integer Euler characteristic kills the remaining torsion. Thus the finite free quotient really multiplies the Euler characteristic by $|H|=e_1$. I checked [Stacks Tag 07S7](https://stacks.math.columbia.edu/tag/07S7): the free constant finite group action on the projective scheme gives a scheme quotient and a torsor. The invariant tensor product of translates of an ample line gives projectivity. Cohomology downstairs remains a module over the **old division algebra**, so its dimensions are divisible by $e_0^2$. This yields $p(l)\in e_0e_1\mathbf Z$, before any complex splitting of $\Delta_0$.

### 5. The integral $K$-theory and arithmetic steps recover genuine division

Section 07:54--85 constructs an equivariant map by actual obstruction extension over a base of dimension $M+2h$, and an ordinary homotopy uses one higher cell dimension with the same available vanishing. The scalar-equivariant lift controls the tautological line bundle. The Picard character maps supply the equivariant torus map even for a nonfaithful image of $H$ in the torus.

The pushforward proof in 142--204 is integral: the complex Thom class is chosen in the Koszul convention with zero-section restriction $\lambda_{-1}(\nu^\vee)$, giving Todd correction $\operatorname{td}(\nu)^{-1}$. An ambient projective embedding reduces the pushforward to an integral linear combination of the projective-space $K$-basis. I directly checked [Hatcher, Vector Bundles & K-Theory, Proposition 2.24 and Theorem 2.25](https://pi.math.cornell.edu/~hatcher/VBKT/VB.pdf): these supply the torsion-free truncated polynomial basis and the product formula used here. The text specifies its dual/Koszul orientation explicitly; the positive-exponential Thom convention elsewhere in Hatcher should not silently replace it. Injectivity of the Chern character on this torsion-free finite basis gives the claimed uniqueness. Rational Riemann--Roch alone would not suffice, but that is not what the proof uses.

The equivariant pullback descends to $V=Z/H$. Its integral pushforward consequently has all coefficients divisible by $e_1$. The constant coefficient is $\pm r$ by the already checked fiber pairing. The ordinary homotopy compares it to the smooth algebraic section $D_0$; the tautological-bundle identity permits comparing the two lifted maps on $D_0$, with obstruction range safely below available connectivity. The Koszul resolution of the section applies even though $X$ itself may be singular, since the zero set is transverse in its smooth locus and the complex is locally exact elsewhere. It expresses the section index as integer finite differences of the original (p$l$), preserving $e_0e_1$-divisibility.

Finally 402--475 does not divide by a degree that might be noninvertible modulo a prime. It uses the integral series identity, multiplies by the denominator, substitutes $t=1-u$, and cancels only the monomial $u^s$, coefficientwise. The result is

\[
A_b(u)^s Q_*(u)=0\pmod{(e_0,u^{h+1})},\qquad
A_b(u)=\frac{1-(1-u)^b}{u}.
\]

For $p^v\mid e_0$, with $a=v_p(b)$, $A_b(u)^s\bmod p$ has exact order $\nu=s(p^a-1)$. The elementary truncation lemma repeatedly forces initial coefficients of $Q_i$ to be divisible by $p$, divides those coefficients, and loses exactly $\nu$ degrees each time. Its bound $h\ge v\nu$ leaves the constant coefficient through the final step. Therefore $p^v\mid Q_*(0)$. This includes $p\nmid b$ $(\nu=0)$, $s=0$, composite $e_0$, and composite $b$. It proves $e_0e_1\mid r$ for **every** module, and therefore excludes a nonzero proper right ideal. Genuine division follows without specialization or an unproved index-multiplication assertion.

As an additional falsification check, I exhaustively enumerated coefficient pairs modulo $p^v$ at three small minimal truncation bounds. No violating constant coefficient occurred: $(p,v,\nu,h)=(2,2,1,2)$, 1,024 pairs; ($3,2,1,2$), 118,098 pairs; ($2,2,2,4$), 131,072 pairs. Lowering $h$ by one produces explicit counterexamples in all three cases (for example $A=Q=2+u\bmod4$ at $h=1$). These computations are illustrations of the sensitivity of the bound, not a substitute for the coefficientwise proof above.

### 6. The induction and arbitrary-field scope close

Section 08:48--70 proves the finite Veronese extension by explicit pair exchanges and monic equations, retaining only linear and quadratic generators. In 191--216 the coefficient of $f_i$ is genuinely nonzero: either it can be chosen arbitrarily after absorption into the old subspace, or a pure-power expression of $f_i$ produces an actual cone point where that coefficient is nonzero. Geometric integrality then makes it nonzero at the generic point.

The binary substitutions in 235--256 use coefficientwise commutation only between distinct tensor factors and the old algebra. The commuting inputs centralize the new factor, so substitution is an algebra homomorphism and preserves the needed within-link polynomial commutations. The recursive character weights in 131--175 and 281--322 are consistent with inverse point action and transport of coordinate functions. The last output has trivial weight. Full degree-one and degree-two relation spaces descend under finite-Galois descent, so the entire relation ideal and evaluation descend, rather than just the final identity. Finite extension preserves the curve exclusion, and every earlier high-degree row remains a consequence of the retained low-degree relations. The final application of section 02 is thus justified.

For the required full-length arbitrary-field statement, section 09:28--39 needs only finitely many coefficients of $I$ and the $f_i$. Their field $F_0/\mathbf Q$ is finitely generated and embeds in $\mathbf C$. Regularity descends to $F_0[x]$ by faithful flatness, then persists over $\mathbf C$. Copying the monomial exponents back to $F_0$ and $F$ preserves every graded dimension. No embedding of the whole field $F$ in $\mathbf C$ is required. The partial-length Artinian reduction cited in 14--26 is not needed when $c=n$. Degree-one elimination belongs to the downstream note, not to this degree-at-least-two dependency.

## Source fingerprints

SHA-256 of the audited EGH primary files:

```text
7e505ce01aa6901be4de3c21b0732c94e1d8b694f71567fac782233e67d4b1d3  paper.tex
840e99d516c388a3a759fb9a780cb263e8dcf0138a5dbd3ba2c187841fc99acf  sections/01-introduction.tex
1efb1a5bb86d9dc1d35e8ef7ba5bfdda97a373258686936cfcfcf7457cecef76  sections/02-reduction.tex
ceae87ed9f77268c351e03a110c436d3b541707efc335ac91b24b856e138c233  sections/03-low-relations.tex
83814bb0e7601c095c8bbd728d4f51c8789c972e1e41e26f8c25c17f50b213ad  sections/04-parameters.tex
5cfe4627325738e6b311be9521afe2d8ab5fc3f2b9557bdecf162baad70a8774  sections/05-curves.tex
0f63e6a6cc362f49f582c1794291d97f1d2e1599b05ed4bb181655c0032e91dd  sections/06-descent.tex
576a43912d169f04c08a28ce1edbc83db872bf1fb6c2ac83ee6b9821051d66b6  sections/07-index.tex
1ca684ecd670058f2f0ef0d36de2ff607f4e75af14ee873d96ece21dac60fdf3  sections/08-assembly.tex
3ed6d5e1f4e06d200a1697bfb7ab2ba753a4727f449b9c64de48fc1ba048ef8a  sections/09-consequences.tex
```

The assigned proof audit is complete. No primary-source repair is requested by this review. Its strongest checked conclusion is the all-degree Artinian EGH statement over arbitrary characteristic-zero fields with degrees at least two; the larger publication candidate must still be judged on its separate reductions and package conditions.
