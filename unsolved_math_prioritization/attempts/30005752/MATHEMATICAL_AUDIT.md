# Audit of the quantum greedy positivity proof

## Verdict and credit

**ACCEPT FOR SOURCE CREDIT, with the preprint qualification below.** Qiyue Tang's *A Note on Universal Positivity of Rank-Two Quantum Greedy Elements*, arXiv:2609.37452v1, gives a valid argument for the full divisibility case of Lee–Li–Rupel–Zelevinsky's Conjecture 1.10. This audit finds no unresolved mathematical gap in the argument or in its use of the specified dependencies. The conclusion covers all integer labels, every adjacent cluster, and coefficientwise Laurent positivity over an indeterminate quantum parameter.

The credited proof is Tang's. This is an independent audit of that proof, not a new proof claim. The inspected work is the September 26, 2026 arXiv v1 preprint. Its second page discloses generative-AI assistance. The checked arXiv record establishes neither journal acceptance nor refereeing of this manuscript. This audit is not a refereeing or publication claim, and makes no novelty determination beyond identifying this source as sufficient for the target.

The complete fifteen-page manuscript was read. Its mathematical pages 1–14 were also inspected as rendered pages. Every named imported result was checked against its specified source version at the statement and proof-interface level; unrelated portions of the long references are not represented as independently re-proved. The original conjecture, recurrence, support characterization, and reflection statements were inspected in the original source. The independent exact computations below are corroborating diagnostics and are not the universal proof.

Primary proof: https://arxiv.org/abs/2609.37452v1

Original conjecture: https://arxiv.org/abs/1405.2414v1

Audit date: October 10, 2026 UTC.

## Exact proposition audited

Let b,c be arbitrary positive integers with b dividing c or c dividing b. Let v be indeterminate, and impose

- X₂X₁ = v²X₁X₂;
- Xₘ₊₁Xₘ₋₁ = vᵇXₘᵇ+1 for odd m;
- Xₘ₊₁Xₘ₋₁ = vᶜXₘᶜ+1 for even m.

Write X^(r,s)=v^(rs)X₁^rX₂^s. The multiplication law is X^m X^n=v^(-det(m,n))X^(m+n). Every adjacent ordered pair uses the identical normalized-monomial convention.

For each (A,N) in Z², the original quantum greedy element is pointed at (A,N), with leading coefficient one and terms e(p,q)X^(-A+bp,-N+cq). Its defining recursion, outside (0,0), is

- H(p,q)=Σᵢ₌₁ᵖ (-1)^(i-1)e(p-i,q) [[N-cq]₊+i-1 choose i]_(vᵇ), when cAq≤bNp;
- V(p,q)=Σⱼ₌₁ᑫ (-1)^(j-1)e(p,q-j) [[A-bp]₊+j-1 choose j]_(vᶜ), when cAq≥bNp.

Both formulas are required when equality holds. Tang's definition is exactly this recurrence, including the positive parts, the parameters of the two Gaussian binomials, zero/negative labels, and the overlapping boundary. Original Theorem 1.7 supplies existence and uniqueness; replacing the overlapping relation by an unchecked one-sided version would not suffice.

The audited conclusion is e≥0 coefficientwise in Z[v,v⁻¹] after expansion in every ordered adjacent cluster, for every integer label. There is no restriction to real roots, cluster variables, finite type, affine type, primitive labels, or v=1. Original Theorem 1.9(d) then supplies indecomposability. Indecomposability is a consequence, not a substitute for positivity.

Nakanishi's 2024 workshop statement has the same symmetric divisibility condition, with the alternative exchange-matrix sign/order convention. Relabeling or reversing the initial seed does not change that condition. The 2022 scattering background is not used as if it already proved positivity of every greedy element.

## Check of the Schur division argument

The key scalar result is stronger than symmetry or ordinary monomial positivity. For a partition λ of M and an alphabet of k principal sl₂ weights, let S(x) be its Schur specialization and d=gcd(M,k). The quotient [d]ₓS(x)/[k]ₓ is an integral nonnegative Laurent polynomial.

The divisibility proof is sound. A root ζ of [k]ₓ/[d]ₓ has ζ² of order h dividing k but not d, hence not M. Rotation of the principal alphabet by ζ⁻² preserves it. Symmetry and homogeneity force S(ζ)=ζ^(-2M)S(ζ), so S(ζ)=0. The divisor has simple roots and, after a monomial shift, is monic integral. Thus its division leaves an integral Laurent polynomial.

Nonnegativity needs the sl₂ structure: its weight multiplicities are symmetric and nondecreasing toward degree zero in steps of two. In the expansion of the quotient at zero, every coefficient in nonpositive degree is a finite sum of differences of multiplicities, with the first index closer to zero than the second. The differences are nonnegative. Symmetry handles positive degree. This checks both integrality and the sign, rather than inferring the sign merely from divisibility.

For a ray multiple n(p,q), write g=gcd(p,k) and dₙ=gcd(np,k). The identity dₙ=g gcd(n,k/g) implies dₙ divides ng. Consequently multiplication by [ng]ₓ/[dₙ]ₓ preserves positivity after the Schur division. This is the precise reason the quantum shift can be reduced to the full-lattice step; positivity at the larger split-color step alone would not be enough.

The graded dilogarithm convention was checked directly from its logarithm. An even grading contributes a positive binomial power to the centered quotient. An odd grading contributes a positive geometric-series power. In particular, the odd factor before taking the quotient is Ψₜ(-tʲZ)⁻¹, not Ψₜ(tʲZ)⁻¹. The sign and inversion both matter. The audit independently reproduces the logarithmic sign (-1)^((h-1)(j+1)). Degreewise finiteness follows from positive source degree and finite-dimensional BPS spaces.

## Check of the source-color construction

### Framed moduli and the ordered-eigenvalue family

For total source dimension P and sink dimension Q, the stability inequality is Q times the total source subdimension minus P times the sink subdimension ≤0. The small framing perturbation has weight QA-PB+ε(η-A/P), with 0<ε<1. Since the first two terms are integers, vanishing forces either the zero or full dimension vector. Thus semistability equals stability in the framed problem. Equivalently, the underlying object is semistable and no proper equal-slope subobject contains all the framing vectors.

The effective change-of-basis group acts freely on the stable locus. The original framed star is acyclic, so the GIT quotient is smooth and projective. Its dimension is fP+bPQ-Q²-Σaᵢ². These claims agree with the sign convention and GIT results in Hoskins §2.2 after changing the sign of the stability parameter.

After merging sources and adding an endomorphism L, the invariant functions are generated by the characteristic coefficients of L. Sink and frame scaling eliminate any invariant involving the outgoing maps or framing vectors. The stable loop-quiver moduli is consequently proper over the characteristic-polynomial space. Adjoining an L-invariant complete flag is a proper operation. Factoring through the finite ordered-root cover proves properness of the ordered-eigenvalue map.

Smoothness is also justified: in a flag basis the parameter space is an open subset of upper-triangular matrices, arrow matrices, and framing vectors. Projection to the diagonal is smooth; the free effective quotient preserves that property. The relative dimension is fP+bPQ-Q²-P. Thus its cohomology local systems on C^P are constant. Over distinct ordered eigenvalues the family is the thin-source star, and reordering eigenvalues permutes its labeled sources. Extending the action across collisions is justified by constancy and connectedness, not assumed on a potentially nontrivial braid local system.

### Springer signs at collisions

The imported Springer facts are the block action and the statement that the sign summand on the nilpotent cone is supported only at the zero endomorphism, in cohomological degree d(d-1). Feng–Yun–Zhang §3 contains the precise statements and the supporting flag argument. The Betti form used here is the same ordinary Grothendieck–Springer construction over C; no finite-field Frobenius assertion is required.

The bundle U tensored with the dual framing line descends through the effective quotient, so Tang's map to the endomorphism quotient stack and its flag Cartesian square are valid. Proper base change therefore pulls back the Springer action. The comparison of this action with permutation of ordered eigenvalues is valid: the finite pushforward of each constant local system, shifted by P, is the intermediate extension from the distinct-eigenvalue locus, so its endomorphisms are determined there.

For collision blocks aᵢ, the sign projection removes all nonscalar nilpotent parts. What remains is exactly the colored framed moduli. The top flag cohomology local system is trivial because each GL(aᵢ) is connected. The shift is 2gₐ=Σaᵢ(aᵢ-1), precisely the difference between the thin and colored relative dimensions. A global S_P sign twist therefore turns the block-sign multiplicities into Young-subgroup invariant multiplicities with the required centered degrees. Zero-sized colors cause no exception.

### Stabilization to stacks

For a proper equal-slope source subspace, A<P. The space of source/sink subspace choices has dimension at most floor(P²/4)+floor(Q²/4). Requiring f framing vectors to lie in that proper source subspace imposes at least f conditions. The bad-framing codimension therefore tends to infinity uniformly, including at eigenvalue collisions. Equivariant cohomology with supports yields the stated stable range.

Appending a zero framing vector preserves the stable condition and gives compatible pullbacks. Their compatibility with the permutation action holds over the distinct-eigenvalue locus and hence for the constant local systems everywhere. Proper base change preserves the sign-summand comparison. In the limit the centering uses the stack dimensions, not the growing framed dimensions. This distinction is correctly maintained. The resulting representation is bounded below and finite in each degree, which is sufficient for the subsequent formal characters.

## Check of the BPS extraction

The star is acyclic with zero potential. The imported BPS space is the centered intersection cohomology of the projective coarse semistable moduli when stable objects exist, and zero otherwise. Nonempty stable loci are dense since the representation space is irreducible. This is exactly the version in Davison–Mandel §6.2 and Proposition 6.14.

All dimension vectors of a fixed projected slope (p,q) have vanishing antisymmetric Euler pairing: it depends only on the total source and sink dimensions. Therefore the slope-genericity hypotheses in Davison–Meinhardt Theorems A and C hold even for noncoprime multiples and even when distinct color dimension vectors have the same slope.

The equivariance assertion in Tang's Lemma 4.1 is justified by the actual constructions of the cited canonical PBW map. Relabeling sources preserves semisimplification, intersection complexes, the ambient perverse filtration, the primitive/full-support inclusion, the common scalar subgroup, and the short-exact-sequence correspondence. It also preserves the Euler form and all shifts. The canonical inclusions of Corollaries 4.11 and 5.9 and the Hall product therefore commute with these relabelings. At zero potential, Example 2.11 gives the identity monodromic vanishing-cycle functor. Verdier duality recovers the centered ordinary stack cohomology used in the manuscript. Source dimensions zero simply remove their spaces and arrows.

The additional PBW exchange sign is essential. On disjoint thin-source blocks it is

τ(d₁,d₂)=χ(d₁,d₂)+χ(d₁,d₁)χ(d₂,d₂) mod 2.

With block totals (Pᵢ,Qᵢ)=(nᵢp,nᵢq), direct reduction gives τ=P₁P₂ mod 2. Tensoring with the sign representation of the total label set supplies exactly (-1)^(P₁P₂) on block exchange. Hence the additional Euler-form sign cancels, leaving ordinary cohomological Koszul symmetry. It would be incorrect to discard this sign before taking Young invariants.

The thin-source dimension-one condition forces PBW factors to be supported on disjoint subsets partitioning the label set. Positive slope excludes nonzero source-free factors. Evaluation of this symmetric sequence on an even k-dimensional color space turns induction into tensor product, and its weight-a piece is the Young-subgroup invariant space. The preceding stack comparison identifies its graded character with the colored stack character.

The ordinary integrality theorem for the colored quiver supplies a second character expression using colored BPS spaces. Comparing the two expressions in increasing total source degree is legitimate: every nonlinear contribution uses strictly smaller positive source degrees. The scalar factor has character t/(1-t²), which can be cancelled in Q((t)) by multiplying by t⁻¹-t. Thus the primitive characters agree. The finite-dimensional sign-twisted thin BPS representation supplies the asserted Schur-positive color polynomial. This verifies the universal geometric step; it is not inferred from the finite Schur tests.

## Check of Hall factorization and full-lattice positivity

Assume c=kb. Put u=(-b,0), w=(0,c), and t=v⁻ᶜ. The Hall pairing for source-to-sink maps is B(Uᵢ,W)=b. The conventions in Davison–Mandel use right modules; taking the opposite quiver gives exactly this representation category and pairing.

Harder–Narasimhan factorization at source weight one and sink weight zero orders factors by decreasing source slope, equivalently increasing q/p. At reversed stability every mixed object has its sink subobject destabilizing, leaving only the two pure factors. Combining those factorizations gives the stated ordered mixed product. The order is consistent with the quantum-torus product.

Passing to the opposite torus and taking inverse together is a group homomorphism. It preserves the order of the factorization and sends pure Hall factors to the stated quantum dilogarithms. The graded mixed factors agree with the plethystic conventions in Davison–Mandel equations (26), (28), and (30), including the odd-degree sign discussed above.

The color projection sends each source monomial to v^(b(k-1-2i))X^u and the sink to X^w. It preserves multiplication because t⁻ᵇ=vᵇᶜ=v^(-det(u,w)). Every degree fiber is finite. The finite geometric sum in the logarithm merges the source factors into Ψ_(v⁻ᵇ)(X^u); the sink becomes Ψ_(v⁻ᶜ)(X^w). Uniqueness of ordered factorization identifies the projected mixed factors with the desired wall factors.

The BPS parity χ(d,d)+1 reduces to 1+n(p+q-bpq) modulo two, independent of the color composition. Reversing colors changes the projection's alphabet to the principal alphabet without changing the BPS character. The Schur argument therefore produces a positive shifted quotient at step b gcd(p,k).

For D=(-bp,cq) with gcd(p,q)=1, the actual pairing subgroup on Z² is gcd(bp,cq)Z=b gcd(p,k)Z. Thus this is precisely the smallest required step on the original lattice. An arbitrary positive pairing is a nonnegative integer multiple of it; telescoping yields positive oriented conjugation. A negative pairing uses the inverse action and an argument shift of the same positive quotient. Zero pairing gives the identity. Normalizing a monomial product adds a power of v and cannot change coefficient signs. The proof never substitutes the split-color lattice for the required full lattice.

## Check of the theta lift and three-chart identification

The general quantum scattering construction applies with L=L₀=Z², skew form det, parameter v⁻¹, and the pointed second-quadrant degree cone. For multiples of u and w, the lattice indices are exactly hb and hc, matching the logarithmic generator denominators. Hence both incoming walls really lie in the required Lie algebra; no fractional lattice extension is silently assumed.

Existence and uniqueness of the consistent completion are furnished by Davison–Mandel Theorem 2.13. All added degrees lie in the monoid generated by u,w, since Lie operations add degrees. No new pure-axis corrections arise. The loop product matches the previously checked ordered Hall factorization, so the outgoing wall factors are the same factors already proved positive.

The broken-line crossing rule in the cited source uses the sign of det(D,m), exactly the sign in the wall-action proposition. Incoming actions are finite positive binomial products because their pairings are divisible by b or c. Outgoing actions are positive by the full-lattice result. For a fixed increment pu+qw, there are finitely many walls and at most p+q nontrivial bends in the relevant truncation. Backward tracing at a generic endpoint determines at most one line for each fixed sequence. Consequently each coefficient is a finite positive Laurent polynomial for every initial exponent, including h=0.

The classical-limit map specializes the incoming actions to the standard rank-two diagram with the primitive-normal convention. The exact label transfer in Cheung et al. Theorem 4.3, Remark 4.5, and Theorem 5.1 is T(h₁,h₂)=(h₁+b min(h₂,0),h₂). Taking h=(-A+b[N]₊,-N) gives T(h)=(-A,-N) for every integer A,N. Thus the specialized theta series is the classical greedy element with the intended denominator label.

A positive finite Laurent coefficient vanishes at v=1 if and only if it was zero. Because the specialization has finite support, the quantum theta series has precisely that support and is itself finite. This reasoning is applied only after coefficientwise positivity and degreewise finiteness have been proved; numerical positivity at v=1 alone would not justify it.

The two adjacent chart maps were checked directly from the exchange relations. The determinant-one lattice maps have columns ((b,-1),(1,0)) and ((0,1),(-1,0)); conjugation by the incoming walls then sends the generators to (X₀,X₁) and (X₂,X₃), respectively. Crossing a short path down from the positive horizontal axis gives the inverse source-wall action; crossing left from the positive vertical axis gives the inverse sink-wall action. The transport theorem supplies positive endpoint expansions in each finite truncation. The endpoints may vary with the degree bound, but each truncation concerns the same fixed inverse series, so this does not introduce a compatibility gap.

The inverse series lie in translates of the corresponding pointed monoids. Their classical specializations are the finite adjacent Laurent expansions of the classical greedy element. The same support argument proves finiteness in both adjacent tori. Therefore the theta lift lies in all three required tori.

Finally, its pointed leading coefficient specializes to one and is positive, hence is a single power vˢ. Dividing by that monomial makes it pointed with leading coefficient one. The exact classical support is contained in the original six-case greedy region, including the strict boundary exclusions in the positive imaginary case. Adjacent Laurentness gives the row divisor with parameter vᵇ and the column divisor with parameter vᶜ. Original Proposition 3.7 therefore identifies the lift with vˢ times the quantum greedy element.

The first divisor displayed in equation (2.1) of arXiv:1405.2414v1 has a parameter typo. Tang explicitly corrects it to vᵇ. This correction agrees with the original recurrence, with the proof of original Proposition 3.7, and with the direct identity expanding v^(mr)X₀^mX₁^r in normalized initial monomials. It is not an additional unresolved assumption. Our adverse test rejects use of vᶜ in that horizontal divisor when b≠c.

## Both divisibility directions and every cluster

Interchanging (b,c,A,N,p,q) with (c,b,N,A,q,p) exchanges the two recursion branches. Induction in p+q gives the coefficient symmetry, with the equality branch and nonpositive labels included. This supplies c dividing b from the c=kb argument.

The original greedy reflection formulas act on every integer label and invert v. The reflections generate translations by two and act transitively on unordered adjacent pairs. Restoring the ascending order of a transported cluster introduces exactly the compensating quantum monomial factor. Neither this factor nor inversion of v changes coefficient nonnegativity. Thus positivity in the initial cluster for all labels gives positivity in every ordered adjacent cluster. Original Theorem 1.9(d) then gives the stated indecomposability conclusion.

## Independent exact diagnostics and adverse controls

The accepted audit used two independent Python programs for the finite diagnostics summarized here; programs and raw computational-output files are excluded from this publication edition. The recurrence program uses integer dictionaries for Laurent polynomials and exact polynomial division, with no floating-point arithmetic. The wall program uses exact rational functions in an indeterminate v and constructs the ordered torus factorization independently of the BPS proof.

The recurrence suite checks 3,718 parameter/label instances: all 22 divisible ordered pairs with 1≤b,c≤6, and every label in [-3,9]². It checks both recursion branches at 3,050 equality-boundary sites; positivity and bar invariance of the computed coefficients; the six-case support conditions; transposition symmetry; and exact row/column divisions and both adjacent-chart coefficient expansions. It inspects 475,912 nonzero initial Laurent terms and 29,306,600 nonzero adjacent Laurent terms across these instances. The finite rectangles include an additional margin beyond the original support bounds. No claim about uncomputed coefficients is obtained from this enumeration.

The Schur suite checks 737 admissible partitions of sizes 1 through 12 with k from 1 through 6. A separate check verifies the PBW sign reduction on 12,005 integer instances. The wall suite independently reconstructs the quantum commutator and its ordered factors through total degree four for eight divisible pairs and the nondivisible pair (2,3). All expected exact identities and positivity tests pass.

The adverse controls show that the tests do distinguish the relevant errors:

- For (b,c,A,N,p,q)=(2,3,3,4,2,1), the original recursion gives v²-1+v⁻², while its v=1 value is +1.
- In the (2,3) mixed ray (1,1), the first minimal-full-lattice shifted-quotient coefficient is v-v⁻¹+v⁻³, again with a negative coefficient.
- Symmetric monomial positivity without Schur positivity fails: (x⁴+1+x⁻⁴)/[3]ₓ=x²-1+x⁻².
- Omitting the gcd factor in the Schur division fails Laurent integrality already for k=2 and λ=(2).
- The wrong odd-dilogarithm sign gives -v² in the simple scalar control.
- The incorrect horizontal parameter from the original displayed typo fails exact polynomial divisibility.

These controls corroborate the audit's normalization and prevent numerical specialization, a wrong divisor, a lost grading sign, or unsupported lattice enlargement from being mistaken for a proof. The universal conclusion rests on the checked geometric, representation-theoretic, and scattering arguments above.

## Dependency inventory

All references are primary sources. The associated source ledger records exact versions, public URLs, PDF byte counts and hashes, and the portions inspected.

1. Lee, Li, Rupel, and Zelevinsky, *The existence of greedy bases in rank 2 quantum cluster algebras*, arXiv:1405.2414v1. Definitions 1.6 and 3.1; Theorems 1.7, 1.9, and 5.8; Lemma 2.2; Propositions 3.7 and 5.1; the closing proof of Theorem 1.9. The original recurrence, uniqueness, support, mutation action, specialization, and conditional indecomposability all match the uses here.
2. Cheung, Gross, Muller, Musiker, Rupel, Stella, and Williams, *The greedy basis equals the theta basis*, arXiv:1508.01404v2. Theorem 4.3, Remark 4.5, Theorem 5.1, and the initial rank-two diagram. These supply the exact classical label transfer and equality for every integer label.
3. Davison and Mandel, *Strong positivity for quantum theta bases of quantum cluster algebras*, arXiv:1910.12915v3. Sections 2.2–2.3; Theorem 2.13; Proposition 3.1 and Theorem 3.2; equations (26), (28), and (30); §6.1; Theorems 6.3 and 6.6; Lemma 6.13 and Proposition 6.14. Its general scattering/transport results apply here; its skew-symmetric cluster positivity theorem is not incorrectly invoked to settle the skew-symmetrizable target directly.
4. Davison and Meinhardt, *Cohomological Donaldson–Thomas theory of a quiver with potential and quantum enveloping algebras*, arXiv:1601.02479v5. Theorems A and C; equation (1) and the symmetry sign (15); Example 2.11; Corollaries 4.11 and 5.9; §6.3. These provide the canonical equivariant-compatible primitive inclusion and PBW map, with their actual symmetry rather than an unsigned substitute.
5. Hoskins, *Parallels between moduli of quiver representations and vector bundles over curves*, arXiv:1809.05738v2, §2.2. The GIT stability sign, freeness, smoothness, projectivity over the affine quotient, and dimension formula match the framed constructions.
6. Feng, Yun, and Zhang, *Higher Siegel–Weil formula for unitary groups: the non-singular terms*, arXiv:2103.11514v4, §3, especially Corollaries 3.4 and 3.7 and the proof of Proposition 3.8. The flag/block action and sign-support identity match the use in the colored-source comparison.

No other new mathematical hypothesis is needed to reach the target. The audit does not rely on manuscript titles, abstracts, finite computations, or a claimed publication status as substitutes for the proof.
