# Partial results on Eisenstein maps from Bianchi homology to K2

14 October 2026. Problem identifier 30005572.

## 1 What this reader establishes

The full construction problem remains **UNSOLVED**. This reader collects precisely scoped mathematical arguments, their complete proofs, supporting finite checks, and separate internal review reports. It does not claim novelty. The arguments were AI-authored and subjected to separate internal AI mathematical review. “Accepted” in the accompanying records means accepted at the stated scope by that internal review; it does not mean journal peer review, independent human expert validation, or formal proof-assistant verification.

The strongest established results form a partial construction. Canonically normalized geometric auxiliary cocycles retain five-primary information over \(R=\mathbf Z[1/6]\). At proper levels with injective unit reduction they descend to actual arithmetic maps on all components of the open Bianchi space, satisfying every good-prime Eisenstein identity, including good primes above five. Auxiliary removal, compactification, bad-prime compatibility, and theta-symbol formulas are proved in specified additional ranges. They are not simultaneously established at every level and on every character.

Three distinctions are essential throughout:

- An actual arithmetic map, or an actual value of such a map, is stronger evidence than a possible coefficient-module obstruction.
- A theta-symbol identity is not a comparison with the normalized, moved geometric cocycle unless that comparison is explicitly proved.
- A compactified map to a level-localized K2 group need not have values in the K2 of the integer ring.

The complete arguments are included in the [proof collection](PROOF_INDEX.md), rather than replaced by this overview. The index gives each proof's dependencies, restrictions, and review. Read the [source-sign qualification](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md) and [model-transport qualification](qualifications/L1_MODEL_TRANSPORT_SCOPE_CLARIFICATION.md) before using any comparison with the source construction. The [bibliography](REFERENCES.md) records public citations and what was and was not inspected. The [check instructions](CHECKS.md) explain how to replay the finite calculations and their limits.

This is a reader of a bounded partial investigation. Earlier proof annexes retain their historical statements of what remained open when written. Later results close only the particular gaps expressly described below. Their presence never removes an older proof's coefficient, level, character, regularity, or component hypothesis.

## 2 The mathematical construction target

Let \(F\) be an imaginary quadratic field, \(\mathcal O\) its maximal order, \(\mathfrak N\) a nonzero proper integral ideal, \(L=F(\mathfrak N)\) its ray class field, and \(\mathcal O_L\) its integer ring. Write \(Y_1(\mathfrak N)\) for the GL2 Bianchi space with all \(h_F\) ideal-class components and \(X_1(\mathfrak N)\) for its minimal compactification. The intended absolute map is

\[
\Pi_{\mathfrak N}:H_1(X_1(\mathfrak N),R)
       \longrightarrow K_2(\mathcal O_L)\otimes R.
\]

A relative extension should take values initially in \(K_2(L)\otimes R\), agree with the absolute map under the natural inclusions, and carry the admissible Cremona-type classes to genuine CM theta or elliptic-unit Steinberg classes. The theta prescription is part of the construction problem. A rational function with divisor consisting of one point is not available; the construction needs a normalized degree-zero theta system or an equivalent intrinsic definition. Unspecified theta values, arbitrary division in K2, or an arbitrary zero map cannot supply this requirement.

The source's coordinate restrictions are \(c,d\in\mathcal O\setminus\mathfrak N\) and \((c,d,\mathfrak N)=\mathcal O\). The exact cusp set, orientations, all-component representatives, descent, and compatibility with relations must still be defined as part of a completed construction. A presentation by classical symbols alone is not assumed to generate every non-Euclidean component. Small proper levels, where unit reduction is not injective, remain part of the full ambition. The unit ideal is a separate degenerate boundary convention: its proposed primitive point is the origin and the displayed nonzero-coordinate formula does not apply there.

The required good-prime relation is

\[
\Pi_{\mathfrak N}\circ(T_{\mathfrak q}-\operatorname N\mathfrak q-S_{\mathfrak q})=0,
\qquad \mathfrak q\nmid\mathfrak N.
\]

For this investigation the full absolute Eisenstein interpretation also includes the expected bad-prime inverse-correspondence relation \(\Pi_{\mathfrak N}\circ(U_{\mathfrak q}^{\vee}-1)=0\). This is an openly adopted strengthening of the question's unqualified “Eisenstein,” not a Bianchi identity literally printed in the original question. Likewise, a source-calibration condition anchors the proposed construction to the existing auxiliary family after extending coefficients to \(\mathbf Z[1/30]\): multiplication by \((\operatorname N\mathfrak c)^2-R_{\mathfrak N}(\mathfrak c)\) must recover that family in its established range. The squared quantity is the square of the absolute norm. In particular a rational scalar auxiliary \((t)\) has factor \(t^4\), not \(t^2\).

These choices expose the intended target without claiming that failure of one proposed normalization disproves every interpretation of the original question. The report of Sharifi and the later manuscript of Lecouturier, Sharifi, Shih, and Wang support this construction objective; the later introductions leave the relative CM symbol formulas for further work. The source results also have genuine coefficient, character, and level restrictions. See [S01–S03](REFERENCES.md).

## 3 Geometry retaining five-primary information

The first difficulty is not caused by finite Bianchi stabilizers. Their orders have only the prime factors two and three, so the group-to-coarse-space comparison is compatible with \(R\). A separate motivic difficulty occurs in the trace-fixed Gersten complex.

For a product of two fixed elliptic curves with maximal imaginary-quadratic CM, the unmodified full-CM trace-fixed complex can have a left kernel consisting of constant five-torsion when five ramifies in \(F\). Its constant kernel is exactly \(K_2(k)[5]\) in that case and is zero when five is unramified, in the precise coefficient and base-field setup of [P01](proofs/P01_CONSTANT_FIVE_TORSION_OBSTRUCTION.md). This does not contradict the source theorem over \(\mathbf Z[1/30]\), and it is not a counterexample to the requested map.

Quotienting constants before taking fixed parts repairs left exactness. Integral pointed elliptic-curve Chow projectors, together with trace-weight annihilators of augmentation one, give the [constant-quotient argument](proofs/P02_CONSTANT_QUOTIENT_REPAIR.md). The needed [degree-zero residue primitives](proofs/P07_RIGHT_END_LIFTING.md) then exist on every relevant CM product. Their construction uses actual torsion orbits and CM elliptic subgroups; diagonal orbits are not treated as Cartesian products.

The ordinary group-cohomology lifting obstruction also vanishes when five ramifies. The proof combines an augmentation-five trace lift with finite-orbit local evaluations and two coprime annihilators. It uses integral Bézout, not division by a degree divisible by five. That result alone supplies an ordinary lift, not its canonical trace normalization. See [P09](proofs/P09_ORDINARY_LIFT_AND_REMAINING_TRACE_OBSTRUCTION.md) and [P11](proofs/P11_FINITE_ORBIT_NORMALIZATION.md).

For auxiliaries \(\mathfrak c\) prime to five, the actual residue primitive is literally fixed by the scalar-five trace \(T_5\). If \(B\) kills constants and has augmentation five, the operator

\[
P=125B+T_5-625
\]

kills constants and has augmentation one. It yields the unique eventual-trace-fixed and literally \(T_5\)-fixed genuine geometric cocycle over \(R\), including the ramified-five case. The two earlier valuewise representative obstructions vanish on this particular family. The general constant five-torsion obstruction remains valid. The full normalization proof is [P14](proofs/P14_SCALAR_FIVE_NORMALIZATION.md).

Exact product norms are compatible with this normalization even when their degree is divisible by five. Good Hecke compatibility at five requires more than an assertion that individual pullbacks preserve \(T_5\)-fixedness. [P19](proofs/P19_FIVE_HECKE_BY_KERNEL_INCIDENCE.md) uses finite étale kernel correspondences, line incidence, and an explicit integral transfer coboundary. The non-Cartesian defect is retained and accounted for. The resulting geometric identity is regular at the level orbit in its stated coprimality range.

No normalized auxiliary meeting five has been supplied by these arguments. Indeed, for a nontrivial ideal dividing \((5)\), scalar-five pushforward kills its auxiliary torsion cycle. Such a cycle cannot be the boundary of a literally scalar-five-fixed primitive. Replacing eigenvalue one by zero does not remove the known constant five-torsion ambiguity. This rules out that shortcut, not every possible alternative auxiliary construction.

## 4 Signs and model transport

Two conventions must never be silently conflated. With the displayed standard tame symbol,

\[
\tau_{\mathrm{std}}\{a,b\}=(-1)^{v(a)v(b)}
        \overline{a^{v(b)}/b^{v(a)}},
\]

separated variables have differential

\[
d_{2,\mathrm{std}}\{u(x),v(y)\}
 =u(x)\mathbin\boxtimes\operatorname{div}(v)
  -\operatorname{div}(u)\mathbin\boxtimes v(y).
\]

Sharifi–Venkatesh use the reciprocal tame symbol, and the LSSW complex refers to that convention. The chain isomorphism is \(J_2=-\mathrm{Id}\), \(J_1=J_0=\mathrm{Id}\). It fixes the zero-cycle and its degree-one primitive and negates the corresponding degree-two cocycle. Consequently the calibrated standard-sign swap is a positive raw pair, while the same-primitive source-sign swap is its negative. Homogeneous vanishing, Hecke, norm, and integrality statements transport unchanged. A claimed exact edge value or source calibration must carry the sign. The final Cremona-edge orientation has not been determined by these homogeneous results. See [L2](qualifications/L2_GERSTEN_SIGN_TRANSPORT_ADDENDUM.md).

Literal transport of the axis primitive is proved for product-coordinate elliptic-model isomorphisms with the shear transported, or when the target primitive is deliberately defined by transport. An arbitrary mixed linear isomorphism does not preserve a separately chosen axis primitive. For independently chosen primitives, the difference has a normalized K2 lift and yields a cohomological coboundary. Specializing that comparison requires the lift to be regular at the marked orbit. This is the indispensable [L1 qualification](qualifications/L1_MODEL_TRANSPORT_SCOPE_CLARIFICATION.md), including in nonprincipal component comparisons.

These qualifications are mathematical corrections. They are not editorial deletions and must accompany the preserved earlier proofs.

## 5 Actual arithmetic maps and auxiliary removal

At a proper level with injective unit reduction, and for auxiliaries prime to \(5\mathfrak N\), [P20](proofs/P20_ARITHMETIC_DESCENT_AND_AUXILIARY_REMOVAL.md) descends the normalized family to actual arithmetic cocycles on all \(h_F^2\) source CM products. Its coefficient target is

\[
K_2(\mathcal O'(\mathfrak N))\otimes R,
\qquad
\mathcal O'(\mathfrak N)=
\begin{cases}
\mathcal O_L[1/\mathfrak N],&\mathfrak N\text{ supported at one prime},\\
\mathcal O_L,&\text{otherwise}.
\end{cases}
\]

Here the notation for localization means inverting the primes over the level. Exact marked-model transport proves image membership; varying definition moduli and transfer give unique arithmetic descent, including the five-primary part. Eventual scalar norms and literal scalar-five invariance kill the relevant good-model vertical constant-unit residues. Integral auxiliary exchange is retained.

Restricting to the strict level stabilizer makes the coefficient action trivial. The resulting actual open homology map on every Bianchi component satisfies

\[
f_{\mathfrak c,\mathfrak N}\circ
 (T_{\mathfrak q}-\operatorname N\mathfrak q-S_{\mathfrak q})=0,
\qquad S_{\mathfrak q}=R_{\mathfrak N}(\mathfrak q),
\]

for every good prime, including primes above five. [P22](proofs/P22_OPEN_HOMOLOGY_GOOD_HECKE.md) proves precisely this open-map statement by passing through field-valued cohomology and the injective localized-integer target inclusion. It does not claim a stronger integral Gamma0 cohomology identity at five.

On nonexceptional full-ray character blocks, a unit smoothing factor removes the auxiliary. The full ray group is used, including its class-group p-part. The squared cyclotomic exception cannot simply be dropped. When five ramifies, the exceptional quadratic extension \(F(\sqrt5)/F\) is unramified and is contained in every ray field; the familiar p-at-least-seven automatic-exclusion formulation does not carry over unchanged. A nonzero ambient exceptional module, such as the example with \(F=\mathbf Q(\sqrt{-5})\) and level \((11)\), is not a computed nonzero auxiliary obstruction.

### Actual removal in a restricted ramified-five range

[The final arithmetic vanishing theorem](proofs/P32_RAMIFIED_FIVE_TAME_RAY_REMOVAL.md) proves that the exceptional five-primary coefficient module itself is zero if:

1. five ramifies in \(F\);
2. \(5\nmid h_F\);
3. the proper level has injective unit reduction; and
4. every level prime away from five has norm not congruent to one modulo five.

There is no bound on the depth at the prime above five. The full ray degree may contain an arbitrarily large power of five. The proof uses a global mod-five cohomology calculation, top-degree corestriction, and Nakayama. It does not average a five-group or cancel its degree. The forced zero exceptional block is therefore genuine removal for the actual family; the other blocks remain the genuine unit-divided auxiliary classes.

With the separately established p-at-least-seven removal hypothesis that no \(p\ge7\) has both \((p)\mid\mathfrak N^2\) and \(p\mid h_F\), the proof gives the full unaugmented R-class in that restricted range. It still does not supply unrestricted bad-U, the relative formula, or the integer-ring target at prime-power level.

### Exact obstruction outside that range

When \((5)=\mathfrak p^2\), put \(n=v_{\mathfrak p}(\mathfrak N)\), \(a=\max(1,\lceil n/2\rceil)\), and let \(P\) be the five-Sylow ray subgroup. On the exceptional character block the [exact smoothing calculation](proofs/P31_EXACT_FIVE_SMOOTHING_OBSTRUCTION.md) identifies

\[
\mathbf Z_5[P]/J\simeq\mathbf Z/5^a,
\]

with the action of \(P\) given by the residual squared cyclotomic character after its Teichmüller part is removed. At depths zero, one, or two, \(J=(5,I_P)\). At larger depth the higher exponent and possibly nontrivial action must be retained.

For the actual compatible auxiliary family the existence obstruction is annihilated by \(5^a\). An exact two-stage test first asks for divisibility of a specified actual multiple in the cohomology module and then for a residual compatible-family class to vanish in its five-power torsion. Neither test is automatically discharged by exchange. Outside the vanishing theorem above, no surviving actual nonzero obstruction has been computed. This compatible-family existence obstruction is distinct from the residue-module quotient in Section 8.

## 6 Bad primes and the true inverse correspondence

The strongest bad-prime theorem is the [three-part nonprincipal package](proofs/P25_NONPRINCIPAL_DUAL_BAD_U.md), with its [principal recovery](proofs/P26_CONVENTION_AND_PRINCIPAL_RECOVERY.md), [central transport detail](proofs/P27_GEOMETRIC_CENTRAL_TRANSPORT_DETAIL.md), and [formal review](reviews/A16_NONPRINCIPAL_BAD_U_ACCEPTANCE.md).

Let \(\mathfrak N=\mathfrak M\mathfrak q^n\), with \(\mathfrak M\) proper and prime to \(\mathfrak q\), and suppose the high level is admissible. For \(p\ge7\), every prime ideal \(\mathfrak q\), principal or not, satisfies the actual norm-zero identity

\[
\operatorname{Cor}_{F(\mathfrak N)/F(\mathfrak M)}
 f_{\mathfrak c,\mathfrak N}(U_{\mathfrak q}^{\vee}-1)=0.
\]

The lower level need not have injective unit reduction. The exact ray square has a unit multiplicity \(u_{\mathfrak M}\mid6\); retaining that multiplicity repairs the previously false Cartesian simplification. The theorem then gives actual \(U_{\mathfrak q}^{\vee}=1\) on characters inflated from the lower ray field when

\[
p\nmid Q^{n-1}(Q-1)/u_{\mathfrak M},\qquad Q=\operatorname N\mathfrak q.
\]

The operator is the true inverse of the first-coordinate local double coset, without a degree normalization. The integral opposite coset differs by a central ideal-class factor; its eigenvalue must not be silently set to one. The proof keeps semilinear CM transport, marked-point changes, the weighted diamond action, and the central adelic coset. The formal acceptance covers the corrected three-file package, not its initial incomplete main draft.

On a noninflated character, norm may already be zero. At wild depth, its degree may not be a p-adic unit. Neither case permits cancellation. The pure prime-power case would have \(\mathfrak M=\mathcal O\), where the required nonzero lower marked point is absent. The theorem also has no five-primary extension. These remain genuine boundaries.

## 7 Compactification by actual cusp reflection identities

For a cusp line in a projective component lattice \(\Lambda\), split \(\Lambda=I\oplus J\) and write the strict level marking as a primitive row \((u,v)\) modulo \(\mathfrak N\). Put

\[
n_{\mathfrak q}=v_{\mathfrak q}(\mathfrak N),\quad
 e_{\mathfrak q}=v_{\mathfrak q}((2)),\quad
 r_{\mathfrak q}=v_{\mathfrak q}(\operatorname{image}(\lambda|_I)).
\]

The last valuation is truncated to \([0,n_{\mathfrak q}]\). [The cusp proof](proofs/P33_CUSP_REFLECTION_AND_COMPACTIFICATION.md) constructs an actual global reflection in the strict cusp stabilizer if either

\[
r_{\mathfrak q}\ge n_{\mathfrak q}-e_{\mathfrak q}\text{ for all }\mathfrak q,
\quad\text{or}\quad
r_{\mathfrak q}\le e_{\mathfrak q}\text{ for all }\mathfrak q.
\]

The projective Hom-module reduction map supplies the global off-diagonal entry; a locally written matrix is not mistaken for a global one. The reflection conjugates each unipotent cusp loop to its inverse. Every existing R-valued homomorphism therefore vanishes on those loops because two is invertible. This is an actual evaluation statement.

If at most one prime has \(n_{\mathfrak q}>e_{\mathfrak q}\), and at that prime \(n_{\mathfrak q}\le2e_{\mathfrak q}+1\), every cusp has zero first R-homology. The map

\[
H_1(Y_1(\mathfrak N),R)\longrightarrow H_1(X_1(\mathfrak N),R)
\]

is then an isomorphism. Every already constructed open map compactifies uniquely with the same target and its established Hecke relations. Examples include all prime ideal levels, powers above two through depth three when two is unramified or depth five when two ramifies, and the other precisely stated ideal configurations in the proof. For ordinary unit group \(\{\pm1\}\), the displayed all-cusp criterion is also necessary for ambient boundary H1 to vanish. The exceptional unit fields have the exact finite unit-pair criterion supplied in the proof.

A broader characterwise result holds when \(n_{\mathfrak q}\le2e_{\mathfrak q}+1\) at every level prime. Let \(W_{\mathfrak N}\) be the subgroup of the ray group generated by CRT local sign classes. It is an elementary abelian two-group. Global Gamma0 reflections imply that the \(W_{\mathfrak N}\)-trivial projection of any already existing arithmetic cocycle vanishes on all cusp loops. This includes arbitrary squarefree odd support, the entire wild p-part, and p equal to five. It does not construct a missing cocycle on an unresolved smoothing block.

The [explicit Gaussian test](proofs/P34_EXPLICIT_REMAINING_FIVE_CUSP.md) takes F = Q(i) and N = (2+i)^2. Here the genuine unaugmented open map already exists, the prime-power arithmetic residue module vanishes over R, and its values lie in K2 of the integer ring. Two displayed middle-cusp loops nevertheless have still unevaluated values in the five-primary Galois-invariant subgroup. They are not identified with descent through the degree-five ray extension. This isolates an actual cusp calculation separately from auxiliary removal and arithmetic integrality.

Failure of these criteria establishes at most that this reflection argument or ambient boundary vanishing does not apply. It does not establish that the actual K2 map has a nonzero cusp restriction. Compactification also leaves a prime-power target localized; topological boundary vanishing cannot remove arithmetic tame residues.

## 8 Prime-power arithmetic integrality remains an actual calculation

At \(\mathfrak N=\mathfrak q^n\), the arithmetic residue module is inflated from the Hilbert class field \(H\). Let \(C=\operatorname{Gal}(H/F)\), let \(\kappa\) be the class of \(\mathfrak q\), put \(f=\operatorname{ord}(\kappa)\), and \(Q=\operatorname N\mathfrak q\). [P12](proofs/P12_ABSOLUTE_INTEGRALITY_AND_RESIDUES.md) identifies

\[
M=\operatorname{Ind}_{\langle\kappa\rangle}^{C}
 \mathbf F_{Q^f}^{\times}\otimes R.
\]

Its exponent is the prime-to-six part of \(Q^f-1\). The exact character support gives unique integer-ring lifts off that support. On its surviving support, actual residues must still be evaluated.

For every component's strict group, every finite q-adic congruence quotient has order supported only at the residue characteristic, two, and three. Those primes do not divide \(|M|\). The [final residue proof](proofs/P29_CONGRUENCE_KERNEL_AND_SMOOTHING_RESIDUES.md) consequently proves that any homomorphism to \(M\) has its entire image on every arbitrarily deep congruence subgroup. It is zero if and only if it has finite q-adic dependence. Equivalently, restriction to the q-adic congruence kernel gives an exact isomorphism of the relevant continuous Hom groups. The missing theorem is the vanishing of the actual normalized arithmetic residue on that kernel. No such residue has been proved zero or nonzero in the surviving cases.

The same proof computes the common annihilator \(M[J]\) and the smoothing quotient \(M/JM\) on the entire Hilbert-class residue module without discarding a class-group five-part. They are both zero unless five ramifies in \(F\) and \(Q\equiv1\pmod5\). In that case each is exactly one \(\mathbf F_5\)-line with the unramified character of \(F(\sqrt5)/F\). This is a coefficient-module result. It is not the compatible-family existence obstruction from Section 5 and is not evidence that any actual residue attains the line.

Good-model vertical integrality is insufficient by itself. The elementary symbol \(\{u,x\}\), for a unit \(u\) in a DVR, has trivial generic vertical residue but its value at \(x=\pi\) has tame residue \(\bar u\). The section meets the deleted horizontal divisor in the special fiber. The same issue prevents a generic-regularity argument or an unsupported rigidity application from finishing the prime-power calculation. The full moved-cocycle expression, not its two possibly singular summands separately, must be controlled.

## 9 Genuine theta symbols and the remaining calibration

The [relative-symbol analysis](proofs/P03_RELATIVE_SYMBOL_DERIVATION.md) proves that the generic auxiliary-theta triangle can have a nonconstant tame residue. This is not a torsion-specialized counterexample. It also proves that correct pair smoothing has three Steinberg terms. Merely multiplying two smoothed units omits mixed terms.

Abstract absolute-to-relative extension is possible, but prescribed cusp-edge values extend exactly when their endpoint-balanced combinations agree with the absolute map. The unweighted edge-boundary lattice is saturated even for a disconnected edge graph. That criterion identifies a missing compatibility rather than supplying it.

The [repaired theta proof](proofs/P18_INTEGRAL_THETA_NORMALIZATION_AND_RELATIONS.md) constructs canonical scalar-powered \(U_n\) values by cancellation in a torsion-free universal unit group before specialization. An earlier attempt to cancel a level factor in specialized units was rejected. The unsupported general CM divided-power construction was withdrawn. For the unpowered CM system, the proved norm-coefficient criterion is that no rational \(p\ge5\) satisfies \((p)\mid\mathfrak N^2\); it is not a theorem at all levels.

The [final symbol theorem](proofs/P28_CYCLIC_POWERED_TRIANGLES_AND_CALIBRATION_OBSTRUCTION.md) proves exact scalar-powered triangles for every cyclic order. Its explicit free-exterior identity gives an equality of the form \(n^2\Psi_{U_n}=n^2W\), where \(W\) is a sum of Steinberg wedges. It cancels \(n^2\) in the torsion-free universal exterior square over \(\mathbf Q(Y_1(n))\), then specializes genuine units and passes to K2. No level prime is inverted in K2. The theorem is cyclic and powered. Substituting \(U_n=n\theta\) does not permit cancellation of \(n^2\) in the specialized K2 group.

The exact unshifted swap is calibrated, subject to the sign in Section 4. At the same-curve/principal-component cyclic-four level, genuine even theta entries descend to the ray field, which equals the Hilbert class field. Their K2 symbols are differences of an endpoint potential. This gives a map on the full relative homology of that restricted component with zero absolute restriction. The [ray-field proof](proofs/P24_CYCLIC_FOUR_RAY_FIELD_DESCENT.md) and [swap proof](proofs/P23_EXACT_SWAP_AND_CYCLIC_FOUR.md) do not identify that zero absolute restriction with the geometric absolute map.

The discriminant-minus-23 local example retains the \(\mathbf F_8\) constants. In the standard tame convention the raw pair has residue \(\bar j\) upstairs in the marked extension and \(\bar j^4\) in the unramified good-model base; allowed normalization by \(1/576\) gives \(\bar j^2\). It detects a nonzero relative edge of order seven. Raw factor 576 and correct three-term factor 624 differ on individual edges, although both telescope to zero on the represented balanced graph. This is not an evaluated residue of the actual moved arithmetic cocycle.

There are two precise method limitations. First, coordinate projection is injective on the full SL2(\(\mathcal O\))-invariant finite torsion cycles on a CM square. Such a nonzero invariant cycle cannot be assembled from external products of degree-zero divisors with zero marginals. This rules out the stated one-direction endpoint-primitive shortcut; it does not rule out more general moving chains. Second, at cyclic order seven the formal evenness/cross-ratio quotient contains a class of exact order seven. It is a formal relation obstruction, not a demonstrated nonzero CM K2 class. The absence of retained level-primary roots of unity in a favorable genuine ray field gives unit-root uniqueness only after theta descent, not K2 divisibility or the missing unpowered relation.

The original attempt comprised five shared mathematical passes, all now closed by the final restricted acceptances. Preparing this reader adds no mathematical claim or further pass.

The main unresolved comparison is between the source-sign normalized moved/sheared arithmetic cocycle and correctly three-term-smoothed unpowered theta sums on all balanced absolute chains, with all components and orientations included.

## 10 What a complete solution still requires

No conjunction of the restricted theorems above supplies the following full statement. The unmet obligations remain:

1. Arithmetic construction and compatible descent at every small proper level without unit-injectivity restrictions.
2. Removal of every surviving exceptional auxiliary block, including the remaining five-primary cases and other excluded full-ray characters, or a proof of an equivalent genuine construction.
3. Actual integer-ring values at prime-power levels, by evaluating or annihilating the normalized cocycle's surviving tame residues.
4. Compactification on the remaining cusp restrictions of the actual map, beyond the proved reflection and previously established character ranges.
5. Unrestricted bad-prime inverse-U identities, including pure prime-power levels, noninflated characters, wild norm kernels, and the five-primary part.
6. A genuine globally compatible unpowered relative theta prescription, with descent, all component and face relations, correct source sign and edge orientation, and agreement with the absolute geometric map on every balanced chain.

No actual counterexample to the full construction has been established. The trace-kernel, formal relation, finite-support, ambient residue, and smoothing-ideal obstructions each have the narrower meanings stated in their proofs.

## 11 How to check and use this edition

The [proof index](PROOF_INDEX.md) is the dependency guide. Every included theorem points to a complete authored argument and an exact internal review pin. The proof annexes have not been mathematically rewritten to fit the narrative. Two proof files have only the three declared neutral attribution deletions; two reading-list or scope-document pointers to excluded coordination documents have been replaced by pointers to this public reader. The [sanitization inventory](SANITIZATION_INVENTORY.json) records those changes by location, byte count, and hashes, without republishing the removed attribution text. The [preservation inventory](PRESERVATION_INVENTORY.json) distinguishes original proof hashes from derivative hashes and identifies the unchanged originals.

The accompanying Python checks test finite algebra, local matrix conventions, module dimensions, and explicit examples. They do not compute general number-field K2, the missing arithmetic cocycle values, or unrestricted Bianchi homology. [CHECKS.md](CHECKS.md) gives an isolated replay command and dependency instructions. Assertion-based checks must be run without optimization; designated explicit-runtime checks can also be replayed with optimization. Recorded output matching is a reproducibility check, not an independent theorem certificate.

Finally, [CORRECTIONS.md](CORRECTIONS.md) explains the mathematical repair history. Source text, PDFs, datasets, private coordination records, and mixed original manifests are absent. Public scholarly titles, URLs, source-byte hashes, and inspection limits are retained so that a reader can distinguish an inspected input from an unavailable one.
