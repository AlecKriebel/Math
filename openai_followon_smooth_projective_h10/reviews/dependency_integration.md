# Independent integration audit of the arithmetic dependencies

Checkpoint: 2026-10-07 05:50 UTC / 2026-10-06 22:50 PDT.
Reviewer: internal agent `/root/dependency_integration`, newly assigned after the first component audits. No external communication, upstream changes, Git changes, or publication actions. Initial assignment completion estimate:95%; the closing addendum below completes the assignment at100%. This is an estimate of audit coverage, not a probability that the theorem is true. The lead researcher remains responsible for overall mathematical and publication percentages.

## Finding

The current union of source-body reconstructions closes the six formerly named pointwise-2-converse interfaces in the **non-CM, full rational two-torsion branch actually required for Family004**. In particular, the agreement between the paired functional over the two height-one coefficient rings is a consequence of a unique derived inverse of a specified Selmer-cone map, rather than an unproved equality of arbitrary cochains. The same finite arithmetic diagrams provide the input to both the outer rank argument and the bounded group-ring clearing argument.

I independently reconstructed that agreement, checked the central-rank alternatives at the unknown base, checked the level-exponent/ramified-determinant premise of the trace identity, read the complete displayed nonvanishing calculation, and checked the Pan-at-5 substitution against Pan's exact primary theorem. I found no material unsupported step or counterexample in these needed interfaces. Earlier reports that said a given interface was outside their scope are not proof-failure findings; their exact open obligations can now be matched to later reconstructions or to the elementary calculation below.

This is an integration recommendation, **not a complete-package publication review**. The manuscript currently advertises a conditional audit note; changing it to an unconditional consequence requires global consistency edits and the user-required complete-package review cycles. Priority and attribution must still be reviewed independently. No claim of formal verification or conventional peer review is made. No mathematical permission to publish follows merely from this report.

## Exact reviewed material

The original user brief in the attachment was read completely, together with the theorem/dependency ledgers and all component notes available at the checkpoint, including the new `arithmetic_assembly.md`, `central_clearing_adversary.md`, and `nonvanishing_audit.md`. The earlier reports' superseded vK–Kret shortcut was treated as withdrawn. The clone HEAD was reconfirmed as `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

Direct source-body reads in this integration pass:

* Pointwise companion `ring-determinants.tex`: 1–184, 410–472, 630–933, 937–1269, 1340–1772.
* `ring-limits.tex`: 121–219, together with the complete independent reconstruction and the explicit evaluation/outer statements quoted in it.
* `coefficients.tex`: 60–244 and 595–1029, together with the complete weighted-theta audit and its primary geometry checks.
* `pointwise.tex`: 1–110, 320–555, and 742–1058, together with the full split-witness reconstruction in `arithmetic_assembly.md`.
* `graphs.tex`: 1–255, together with the network proof, independent program checks and two-symbol allocation reconstruction.
* `nonvanishing.tex`: all 425 lines; the independent analytic report was then read completely.
* Family004 `04-height.tex`: 710–1311; `02-reduction.tex`: 230–300, 590–643, 750–887 and its complete independent logic audit; `03-parity.tex`: 450–535 and its complete independent descent/matrix audit.
* `manuscript/height-repair.tex`: complete current source.

Direct primary web reads in this pass: [Pan, author version1901.07166v2](https://arxiv.org/pdf/1901.07166v2), Conjecture1.0.1 and Theorem1.0.4, printed pp.2 and5; [published Cai–Shu–Tian](https://msp.org/ant/2014/8-10/ant-v8-n10-p05-p.pdf), surrounding Heegner conditions and Theorem1.1, pp.2524–2525. The other established inputs are used through the exact primary-source/assumption checks recorded in the component reports. This pass did not reprove the entire Kato Euler-system theorem, Nekovář's book, or all foundational adelic theta theory.

Source SHA256 identities:

| Source section | SHA256 |
|---|---|
| pointwise companion / ring-determinants.tex | `b0edb60ba616f8043f6a12f0c2206ffc236c10e9ccb5423fede9d60158a59995` |
| pointwise companion / pointwise.tex | `66717dc63cf7821281f988386a24a99f65113cfa1fa97419f8ebd752a78056d3` |
| pointwise companion / coefficients.tex | `6e2266b43cdada2d63df5c0d5bba8b42e6dd24ea6cc9b230e3d52e9dbc5f213d` |
| pointwise companion / nonvanishing.tex | `b5c0209d2202cc798c3fc7896432c0c534f51284447df7bd6b84f59243c69963` |
| Family004 / 04-height.tex | `f50c9e92a61f8ad5da7ba8c2000545c7847dfa500d12da8bb53ae93ac9f443d9` |
| Family004 / 02-reduction.tex | `ceee1c9e957d4069184e8984824e06a4a523eb30be3b9d7ac40f108e2b1221bc` |
| Family004 / 03-parity.tex | `d986fd78ba814d6783165ab3fcc9da89c2b983d43d1e737a4bf798d1d753ac58` |

The final audit-evidence hashes are recorded after the pending module report in the closing addendum; earlier snapshots should not silently be substituted.

## 1. The two paired-functional representatives agree for a precise reason

Let `C` be the relaxed Selmer complex and `C_perp` its orthogonal complex. Both are the specified cone of the same global/local cochain maps. Their difference at active primes and the auxiliary prime r is the corresponding full local cochain complex; all other local conditions are the same self-orthogonal conditions. Thus the natural map

    j : C_perp → C

has cone equal to a sum of these full local complexes, up to the fixed cohomological shift. After extending to the fraction field they are acyclic, so j is a quasi-isomorphism. Its inverse in the derived category is unique. If two local contracting homotopies are used, they represent homotopic inverses, and induce the same map on cohomology.

The paired functional is therefore exactly

    lambda = H¹(D j⁻¹)([P]) ∈ H²(C)*,

where D is the retained conjugate-Weil global duality morphism. This defines one generic functional. The representatives obtained over `O = completed Lambda_(2)` and over `Lambda_(t)` are its two integral models. It is unnecessary, and generally false, to demand an evaluation-at-t=0 map from all of O or one cochain integral at every localization.

At the characteristic-zero central localization, -2 contracts an active ramified-quadratic inertia direction, and the nonzero auxiliary Frobenius determinant contracts the r terms. At O the odd scalar Frobenius exponent and moving inertia give unit-pivot contractions. The maps j and D are the same retained maps in both cases. This proves the exact agreement requested in the initial dependency note.

The finite diagram itself is checkable. In the common cone model

    C_delta^n = G^n ⊕ U_delta^n ⊕ L^(n-1),
    d(g,u,l) = (dg,du,res(g)-i(u)-dl),

the face maps are identity on g,l and the inclusion on u. Every square commutes. The derivative local model has degree1 planes F,S with zero pure cup products at precision `ell² ≡ 1 mod 2^(a+1)`; both mixed coefficients are units. Therefore the pure-plane isotropy homotopies and their restrictions to the strict face are literally zero. The unchanged old Kummer homotopies are retained once. Finite contraction transports the whole diagram, including its degree2 identities and boundary witnesses, instead of selecting independent cohomology models. This supplies the simultaneous input to the global duality theorem; the theorem is not being asked to manufacture it.

## 2. Unknown-base ranks and the two limit arguments are compatible

At nonzero addresses a known simple zero gives rank1, finite Sha and nonzero central Heegner point. At the zero address only **Selmer corank1 over K** is assumed. Rational central Kummer cohomology consequently has dimension1 in degrees1,2. Generic dimension is at most1 by specialization. If generic dimension is0 the coordinate is defined to be0; if it is1, generic and central dimensions match and the derived-specialization lemma applies. Thus vanishing of the base derivative makes the central point class zero in either case, without silently assuming Mordell–Weil rank1 or finite Sha at the unknown base.

For the outer bound, minimal sizes depend on E, the bounded number of ramified companion primes, and the fixed number of derivative slots. Uniform torsion lengths are not inferred from matrix size. The actual all-sequence evaluations, integral degree2 matrices, exact-kernel restriction and finite Chebotarev extensions allow rank reduction before the terminal nonzero minor is used. Approximate outer cycles retain crossed-cocycle identities because their integral degree2 errors tend to0. A surviving primitive inner kernel vector forces outer dimension≥1 throughout. The exact integral switch retains each determinant valuation, including divisible classes. This is the additional mechanism absent in the counterexample `[2^i]`.

For the binary family K is fixed, and the finite quotient of its base discrete Selmer group is finite even when its divisible part is nonzero. Hence its fixed torsion length may enter the central clearing constants. No uniform bound as K varies is imported into this step. The universal cycle and functional are made over the group ring before evaluating its finitely many characters. The old complex is a subcomplex in the actual localization cone; the singular new-prime blocks can be eliminated simultaneously. Their residual t-order is≤4, and sign evaluations differ from augmentation by twice a power-series matrix. The Schur expansion bounds the negative pole by `4M`, independent of the number of blocks. This verifies the central size/pole premise needed by the independently stress-tested clearing and transfer lemmas.

## 3. The trace module's level premise is checkable

For an odd new p, if f has half-integral level4L, then `V_p f(z)=f(pz)` has level4Lp. For gamma=(a b;c d) in Gamma_0(4Lp), conjugation by diag(p,1) gives `(a,pb;c/p,d)` in Gamma_0(4L). The theta multiplier differs by `(p/d)`. Thus the character changes by `(p/·)`, and the level exponent at p is at most1. The extraction identity `U_p = U_(p²)V_p` holds coefficientwise, and U_(p²) preserves that raised level. Every newly raised character has ramified quadratic determinant at p, so a non-old weight2 constituent has conductor exactly1.

Consequently its local parameter is principal series with one unramified and one ramified quadratic line. A Steinberg parameter would have unramified determinant at conductor1; a supercuspidal parameter has conductor≥2. With Frobenius eigenvalues lambda,mu and inertia diag(1,-1), the two trace differences are `-2z mu` and `-2z`; multiplication by the U_p eigenvalue lambda proves the source identity. Old constituents have trivial inertia and both differences vanish regardless of their old multiplicity spaces.

The character ratios in the unary subtraction are quadratic, even when the common character takes higher 2-power roots of unity. Thus their differences are0 or twice a unit. Fresh-prime traces kill each unary correction coefficientwise. This proves determinant reduction on the reduced trace orbit without assuming that all eigenbasis lattices split integrally. The deeper all-split witness uses the same corrected lattice and the extra /4 division, not a new unexplained modular lift.

## 4. No circular odd normalization or common-address assumption

The dependence order is:

    even coefficients and cyclotomic lower bound
    → even partitionable upper estimate at known nonvanishing twists
    → bounded-factor nonvanishing companions
    → ring lower bound plus height ratio
    → odd lower bound
    → odd minimum/stabilized symbol
    → final simultaneous graph cubes.

The rough-companion proof applies the even estimate only where analytic nonvanishing has already given finite Sha by the forward theorem. It never assumes the corank-one converse being proved. The varying companion has bounded prime count; later a separate companion k is fixed before b.

In the full-two-torsion final branch, duplicate compatible common labels to make each packet have rational total0. The even oriented total belongs to `(1+c)V`, because it annihilates every conjugation-invariant quadratic character. Reserved orientation flips give the required change while preserving rational labels. Separate contractions to the even and odd minimum witnesses establish **two nonzero terminal polynomials**; they do not assert a shared unit evaluation. The two-symbol address theorem uses a coefficient of their product in the ordinary polynomial ring, before Boolean reduction, to supply that shared evaluation. The finite network and b are fixed first; only then is one actual finite stage selected from finitely many ultrafilter-large requirements. There is no countable intersection or one stage working for all b.

## 5. Analytic uniformity and the height ratio

I read the entire displayed moment calculation independently before reading `nonvanishing_audit.md`. The off-diagonal Dirichlet series has good factor `1+lambda(p)xi(p)p^-s`; division by the GL2 Euler factor leaves a correction converging for Re s>1/2. The bad factors cost a polynomial in J|nu| with an absolute exponent. On shifting the dyadic Mellin sum to Re s=-1/4, its factor is T^-1/4; the ranges `|nu|≤J X^(2rho)` and `T≥X^(1-rho)/J` give `J^B X^(3/4+O(rho))`. The square-divisor tail and `J≤bd²` then permit fixed absolute eta,B. The curve and progression enter constants and thresholds only. The independent analytic report supplies an explicit noncircular choice and a primary Richert lower-sieve replacement when the quoted FI book passage was not directly accessible.

The lower sieve therefore yields an absolute prime-count bound, while the required size may depend on the varying absorbed curve. This is precisely the quantifier needed by the odd lower-bound proof. Ordinary nonvanishing without that bound would be insufficient.

The published CST formula uses the unaveraged character sum and denominator `u² c sqrt|D|`; in both needed applications all level primes split, `(N,D)=1`, and u=1. The ring conductor is exactly|h|; the genus conductor is1. Taking the ratio introduces `sqrt|hk|`, hence exactly the normalized central value `L_*(hk)`. It introduces neither a class-number divisor nor a product over the conductor primes. The degree2 rational projection maps bound lattice indices independently of the number of active h primes. These conditions agree across the ring and coefficient constructions.

## 6. Pan-at-5 substitution and its exact effect on H10

Pan's primary Conjecture1.0.1 requires a continuous irreducible odd representation, finite ramification and potential semistability. His Theorem1.0.4 adds distinct Hodge–Tate weights, with the residual exception only at3. The source's prime-independent sign descent produces `R_ell=r_ell⊕r_ell` for ell=5,2 and a controlled field L'. Faltings gives absolute irreducibility; the Betti involution gives oddness; semistable reduction over a finite local extension gives potential semistability at5; the exponents are0,1; and the ramification set is finite. The quaternion algebra may ramify at5, since it is split over the finite coefficient extension, not required to split over Q5.

Good special-fiber quasi-endomorphism traces identify r2 with the same algebraic conjugate of the newform obtained from r5. For its level, use coefficient5 at every residue prime except5, and coefficient2 there. Thus Carayol is always used with coefficient prime different from residue prime. The bounded-degree field L controls all small-prime ramification cuts; the larger field L' of degree≤CM is used only for the global Hom/isogeny comparison. The modular Jacobian source height is already bounded before applying the isogeny theorem. This avoids circular use of the unknown fiber height.

The target Family004 curves are `E_l: y²=x(x-l)(x+3l)`, with full rational two-torsion and j=35152/9. The latter is not an algebraic integer, so they are non-CM. Each E_l is fixed before an internal cube is constructed; l need not itself be an odd fundamental discriminant. All internal varying h have odd conductor away from the fixed bad support, as the cyclotomic audit requires. Constants are allowed to depend on each E_l; no uniform constant over all l is used in the pointwise rational-point transition.

The elementary descent gives `r+dim Sha[2]=1`, and hence full Selmer corank≤1. The pointwise converse supplies finite Sha; the perfect alternating Cassels–Tate pairing on the full finite 2-primary group makes dim Sha[2] even. Thus r=1, Sha[2]=0, and the selected Selmer class is rational. This closes exactly the divisible-Sha alternative that previously blocked pole parity. It does not replace Selmer corank by rank or by the finite Selmer dimension.

The logical audit then uses only these audited inputs, a fixed rank1 elliptic group, the five-point height bound and the ordinary prime-pattern witnesses. Fixed constants can be hardcoded in the existential contradiction algorithm. Compactness is used for a proof, not as a computation; the final search dovetails integer zeros against finite rational tests. The same polynomial error controls all ring-element height radicals, and the transferred quadratic elliptic height bound forces all root indices ordinary. No stronger many-one or fixed-variable claim is needed.

## Reproduced finite checks

On this pass, Python3 independently executed all three saved programs successfully:

* `agent_notes/parity_matrix_check.py`: 1,960 reciprocity-consistent cases, exhausted q0–J toggles, seed4003.
* `verification/check_two_converse_programs.py`: 62 restrictions, three programs each, b=1,…,5.
* `reproducibility/arithmetic_checks.py`: exact quadratic-field point identity and26 selected finite-field primes; all checks passed, including the recorded nontrivial gcd examples.

These finite checks support the named calculations; they are not substitutes for the source proofs or asymptotic analytic argument.

## Promotion boundary

Once the final coefficient-module addendum is saved and matched to the level argument above, this integration pass has no named material mathematical gap left in the restricted dependency route. The established geometric consequence remains Poonen's finite disjunctive oracle transfer, with regular=smooth over Q and explicit filtering of non-geometrically-integral connected components. The computable-height obstruction follows by finite primitive-coordinate enumeration. The inherited arithmetic breakthrough, established geometric transfer, and immediate consequence must be distinguished in every eventual title, abstract and metadata.

The current ledgers' unverified labels are historically accurate for earlier checkpoints but should be explicitly updated, not silently used as contrary mathematical evidence or removed from the research history. Complete-package review, accurate disclosure, priority resolution, exact clean build, and publication/tracker verification remain separate required work. This report performed none of those final operations.

## Closing addendum: exact integrated version and verdict

2026-10-07 05:55 UTC. I read the complete final `coefficient_trace_audit.md` and `VERIFIED_CORRECTIONS.md`. The former matches the independent level/conductor calculation above and supplies the precise extra determinant correction after division: the unraised unary coefficient at p is even, so its correction vanishes modulo2 without assuming an arbitrary oldform satisfies the ramified U_p identity. Its primary James–Ono/Purkait level statements agree with the direct metaplectic conjugation calculation. The finite Frobenius matching retains K and every support quadratic character, ensuring pp′ lies on the total filter even when p alone does not. This closes the last explicitly pending integration item.

The universal inverse-Euler correction in `VERIFIED_CORRECTIONS.md` was checked algebraically. The identities

    P_q(Z)-Z²P_q(Z⁻¹)=(1-q)(1-Z²),
    A_c⁺-gamma_c A_c⁻=c(c+1)(1-gamma_c)

are exact, and each right side is divisible by2. Thus the correction is integral before evaluation and has the claimed unused/active character values. Its central convention units are1; no increasing per-prime 2-loss is introduced. Both correction routes are needed evidence for this accepted dependency path and must be included or explicitly linked in any unconditional publication candidate.

| Initial pivotal obligation | Actual closing evidence |
|---|---|
| Uniform non-CM cyclotomic integral coordinate and central PT length | `two_converse_cyclotomic.md`, including primary Kato hypotheses, real-place supplement and universal convention correction |
| Integral derivative class and one fixed multiplier | `two_converse_limits.md`, finite descent and local coordinates; explicit local cone/cup faces in `arithmetic_assembly.md` |
| All-sequence and approximate outer-cycle evaluation | `two_converse_limits.md` plus the integral degree2 source identities; no unrelated later ultrafilter |
| Outer rank reduction and the same paired functional | source `rd:outer-bound`, the unique-derived-inverse reconstruction above, and `arithmetic_assembly.md` |
| Weighted theta/whole-prime trace support and deeper all-split witness | `two_converse_coefficients.md`, `coefficient_trace_audit.md`, actual level/conductor calculation above, and final split-witness source reconstruction |
| Fixed-base family clearing, analytic lower bound, common stage | `central_specialization.md`, `central_clearing_adversary.md`, `nonvanishing_audit.md`, `arithmetic_assembly.md`, and the noncircular dependency/quantifier checks above |

**Final mathematical integration verdict:** the restricted non-CM full-rational-two-torsion pointwise-converse route needed by Family004, the Pan5-repaired five-point height route, the exact Family004 finite-test/compactness implication, and Poonen's promised-input geometric transfer fit together. No exact material unsupported inference remains in these checked dependencies. This is a positive reconstruction of their joint hypotheses, rather than acceptance inferred from the absence of formalization or from favorable isolated verdicts. It supports preparing an unconditional geometric **consequence of the repaired/audited arithmetic input**, with the two technical substitutions exposed. It does not establish priority, constitute a complete-package review, verify a deposit, or authorize claiming formal or human peer review.

Evidence SHA256 at this closing checkpoint (paths relative to the project):

| Evidence | SHA256 |
|---|---|
| `agent_notes/arithmetic_assembly.md` | `c2cada499702bb227a5359f350570270e46101cb16f23716f7f3eb21835b0e5e` |
| `agent_notes/central_clearing_adversary.md` | `fbd8ed888911d6df637592b92a71106ac5e8e3c80d60b07e69befb6cc8d72228` |
| `agent_notes/central_specialization.md` | `aa1836377e95b62c69ccb65107da85383c6c18d68840ea0324166d98c1ddae23` |
| `agent_notes/coefficient_trace_audit.md` | `765c6a8ea358d2403d2bf73523c0e7dd06a178f571df915dad835fd9f31a6842` |
| `agent_notes/geometric_transfer.md` | `5a5a9f07267ff5327d3fdb324b759f389e9ed43767f5ec5135f1aca8fd776152` |
| `agent_notes/height_descent.md` | `d3492838578e709933ccba236acffe35f0d13409f179580a4248fc3c525b146d` |
| `agent_notes/nonvanishing_audit.md` | `08c6ee663ed3a31b3ac4bc84e0a3756716c1630aa22e6ba4854ea28efacb84b7` |
| `agent_notes/priority.md` | `e31777622a170e8c5e92f9505cc7cb078bbc46640f59f92d044e0828066804e7` |
| `agent_notes/two_converse_adversary.md` | `bcdc992120318e988c4303e0aff9467f4982df55aabe8efb89d95ab95c36254d` |
| `agent_notes/two_converse_coefficients.md` | `74747f1a743dd247e4b1a1725719ccd95e9e9077ab4ded7300569812146b24f4` |
| `agent_notes/two_converse_cyclotomic.md` | `55e6379763011ea77aecc3b3ea489f7eb410e7876e98f492d179b0c01ae55b3b` |
| `agent_notes/two_converse_dependency.md` | `9f2ba0b0fe022abd8853555f2e4a5b4316c06257587c1a96ddff3e7c35c277ae` |
| `agent_notes/two_converse_limits.md` | `47b95820bd2da24aecc29de61ab1bf210a4de5027fa816f22dc15e32645f7199` |
| `agent_notes/upstream_arithmetic.md` | `a5f89503c88ab3c0dbab0ae76dc161729e6dbb8b7e162a7012113c2cc01b62be` |
| `agent_notes/upstream_logic.md` | `f1dbd4a27cddfa6209944cb94c13d9aea2ae75439d6c1f09dd213ce4bfc524ac` |
| `manuscript/height-repair.tex` | `6eaffd0eb970d8573181bc53b888711d11dc50301414f5d9ca153533a59b319d` |
| `VERIFIED_CORRECTIONS.md` | `8fb237ec02e893fd12fde4c3f454d292e4dde7d9e8ec979e301f860399a5e239` |

Assignment completion:100%. Overall discovery and publication progress remain for the lead researcher to report. No additional source changes or external actions were performed.

## Correction addendum: the normalized Euler determinant and the same universal class

2026-10-07 06:11 UTC. This addendum preserves the preceding checkpoint as history and corrects a substantive error in its closing Euler paragraph. I accepted the unnormalized polynomial `1-a_q Z+q Z²` at the unchanged Frobenius variable. That polynomial is not the determinant of the actual local block in `cyclotomic.tex:478–482`. The coefficient module there is `W_q=V_h(-1)`, and the required polynomial is

    P_q(Z)=1-(a_q/q)Z+(1/q)Z²,
    D_q=P_q(chi_h(Fr_q) gamma_q).

The correct identity is

    P_q(Z)-Z² P_q(Z⁻¹)=((q-1)/q)(1-Z²).

The previous displayed identity with `(1-q)` belongs to the unnormalized polynomial and does not validate the required application. The original detailed audit `two_converse_cyclotomic.md` already used the normalized polynomial and the correct identity. The complete-package reviewer exposed the mismatch in the promoted summary and manuscript. I directly reread the pinned primary source, its actual localization triangle, fixed-form coefficient map, smoothing operation, rational comparison and determinant/Fourier intersection, rather than inferring that the two normalizations have the same divisors.

### Why the error cannot be dismissed by checking the central valuation

Write `P_cov(Z)=1-a_q Z+qZ²`. Exactly,

    P_cov(Z)=q Z² P_q(Z⁻¹),
    P_cov(Z)/(Z²P_cov(Z⁻¹))=r_q⁻¹,
    r_q=P_q(Z)/(Z²P_q(Z⁻¹)).

Thus using the wrong polynomial reverses the correction ratio. Applied to the same inverse-convention class, the wrong multiplier would supply `(Z²P_q(Z⁻¹))²/P_q(Z)`, rather than the required `P_q(Z)`. The known rational divisibility does not pay the denominator in that expression. Its being an `O[G]` unit and having central value1 do not repair this height-one problem.

A concrete example lies in the actual full-two-torsion curve family. For `E_1: y²=x(x-1)(x+3)` at the good prime5, direct enumeration gives8 points and `a_5=-2`. Choose the real cyclotomic generator5, so `Z=1+t` at the unused trivial character. Then

    P_5(1+t)=(t²+4t+8)/5,
    P_cov(1+t)=5t²+12t+8.

Both central values have2-adic valuation3. Their monic distinguished polynomials are `t²+4t+8` and `t²+(12/5)t+8/5`. They are different irreducible polynomials over Q2: their discriminants are `-16` and `-16/25`, respectively, and -1 is not a square in Q2. Both have roots of t-valuation3/2. Consequently they give distinct height-one primes of `A=Z2[[t]][1/2]`. This explicitly shows why central agreement is insufficient. The finite point enumeration and polynomial expansions were independently reproduced during this addendum.

### Universal integrality before evaluation

Let `R=Lambda[G]`, `O=completed Lambda_(2)`, `G` an elementary two-group, and `Z_q=theta_q gamma_q` with `theta_q²=1`. Here `gamma_q` means the cyclotomic scalar of the **actual** local block `1-gamma_q Fr_(W_q)`; it is not independently renamed or inverted in that block. Let `g_q` be the universal inertia bit. Define

    r_q=P_q(Z_q)/(Z_q²P_q(Z_q⁻¹)),
    w_q=(r_q-1)/2,
    U_q=1+w_q(1+g_q),
    V_Q=product_(q in Q) gamma_q².

For the restricted full-rational-two-torsion branch, `a_q` is even. Modulo the maximal ideal `(2,I_G)` of `O[G]`, both denominator polynomials reduce to `1+gamma_q²`, a nonzero element of `F2((t))`: the cyclotomic Frobenius exponent of an odd prime is nonzero. They are therefore `O[G]` units. The normalized identity shows `r_q-1` belongs to `2O[G]`, so `w_q` is integral in the whole group ring. Moreover `U_q` reduces to1 modulo `(2,I_G)`, since `1+g_q` reduces to0. Hence `U_q` is an `O[G]` unit **before any character evaluation**. The apparent `/2` is cancelled in `r_q-1`; there is no per-prime or character-idempotent denominator. `V_Q` is already a group-like unit of `Lambda`.

At an unused character, `g_q=1`, so `U_q=r_q`; at an active character, `g_q=-1`, so `U_q=1`. For an unused character `theta_q=±1` and `Z_q²=gamma_q²`. Thus the exact class multiplier acts on the actual inverse Euler factor as

    gamma_q² U_q P_q(theta_q gamma_q⁻¹)
      =Z_q² r_q P_q(Z_q⁻¹)=P_q(Z_q)=D_q.

At an active character the raw Euler factor is1 and the multiplier leaves only `gamma_q²`, an `A` unit. These equalities apply at the generic Iwasawa coordinate, not only at t=0. No involution of the entire coefficient module or change to the local complex is used: multiplication is a scalar operation on the same universal cohomology class obtained by the integral coefficient map in `cyclotomic.tex:350–361`.

### Smoothing is corrected on that same smoothed class

The stated CRT makes the tame actions of `c,d` trivial and fixes `v2(c-1)=v2(d-1)=e`, independent of the varying support. Put

    A_c⁺=c²-c gamma_c,       A_c⁻=c²-c gamma_c⁻¹,
    B_c=gamma_c A_c⁻,       R_c=A_c⁺/B_c.

Both `A_c⁺` and `B_c` are `O` units. The exact identity

    A_c⁺-B_c=c(c+1)(1-gamma_c)

gives `R_c-1 in 2O`; its rational central value is1. The same holds for d. If `z_raw⁻` is the actual inverse-convention **smoothed** fixed-form class, define the corrected class by first multiplying it universally by

    gamma_c gamma_d R_c R_d V_Q product_q U_q

and then dividing by `A_c⁺A_d⁺`. Algebraically this is exactly

    z_new=V_Q (product_q U_q) z_raw⁻/(A_c⁻A_d⁻).

Therefore the comparison is with the same unsmoothed inverse-convention fixed-form class; no unmatched smoothing divisor is left at an `A` height-one prime. All the operations used for the integral bound are `O[G]` units. The two smoothing central valuations are the fixed values e,e. Central evaluation here means evaluation of the rational expressions, which are regular at t=0, and later of the recovered `A` determinant coordinate. There is no claimed evaluation homomorphism from O.

### Height-one regularity and the uniform bound concern the same determinant

The rational comparison in `cyclotomic.tex:500–542`, expressed in the inverse convention, gives the actual unsmoothed constituent as

    z_x⁻=c_x epsilon_x E_x^fix
          (product_(q unused) P_q(theta_(q,x) gamma_q⁻¹)) z_BK,x.

The scalar `c_x in Q2×` is an `A` unit; `epsilon_x` is group-like. Using the preceding exact scalar operations gives

    z_new,x=c_x epsilon_x E_x^fix
        (product_(q active) gamma_q²)
        (product_(q unused) P_q(theta_(q,x) gamma_q)) z_BK,x.

Each possible `A` pole of `r_q` at an unused inverse Euler factor cancels **against that factor in this very class**. At active characters `U_q=1` has no such denominator. The extra active product is an `A` unit. Fixed bad-support discrepancies, and Kato's local prime2 correction, are handled by the same finite-set fixed multiplier `F_E` already constructed in the primary source; the new normalization introduces no varying bad-prime factor. In particular the corrected constituents are regular in `A` cohomology after these fixed corrections. It would be incorrect to assert that the ratios `r_q` themselves are regular over A merely because they are `O[G]` units.

For every height-one prime p of A, the localization triangle has `H1(Q_q)=0` and `length H2(Q_q)_p=v_p(D_q)`. It identifies the old and full global `H1`; enlarging the degree2 module costs at most the sum of those lengths. Multiplication by the actual normalized product `product_(q unused)D_q` adds exactly that sum to the index of the **same** rank-one class. Together with Kato's audited rational divisibility and `F_E`, this gives the primary inequality `cy:divisibility` at every p. For the determinant coordinate defined by `a wedge lift(2F_E z_new)=u e`, it implies `u_x in A`. This is the coordinate of the universal class just constructed, not a separately prescribed family of central values.

On the other side, that same construction gives `2^C_int u in O[G]` with the original uniform exponent: all new multipliers and smoothing divisions are `O[G]` units. Fourier inversion can be used solely to establish `u in A[G]`, because `1/|G|` belongs to A. It is **not** used to estimate the denominator. Each group-basis coefficient of `2^C_int u` then lies in `A intersection O=Lambda`. This recovers `2^C_int u in Lambda[G]` without adding b to `C_int`. The primary Fourier-intersection lemma, lines102–113, explicitly proves this distinction. Only after this recovery is the ordinary central evaluation used. At an unused character `r_q(0)=1`; at an active character `gamma_q²(0)=1`; the smoothing ratios also have central value1. Thus the original central reciprocity and bounded central error apply to the repaired determinant coordinate.

**Rechecked verdict:** the wrong normalization was a real application/presentation error and invalidated that particular paragraph of my earlier closing verification. With the actual normalized polynomial, the universal translation, U correction and smoothing correction act on the same fixed-form Iwasawa class and pay exactly the local `A` height-one divisors required by the proof. I find no material unsupported step remaining in this corrected convention interface. The earlier restricted mathematical integration verdict survives with this explicit correction; it does not certify a complete-package review, priority, formalization, human review, deposit or publication.

Exact versions read for this addendum:

| Evidence | SHA256 |
|---|---|
| Pinned primary `build/sections/cyclotomic.tex`, reread lines65–113 and350–627 | `29d8764bf7ed79913a4def3d56e49b125bb96d334a5a4514b5390f34d6294605` |
| `agent_notes/two_converse_cyclotomic.md`, including the original normalized repair | `55e6379763011ea77aecc3b3ea489f7eb410e7876e98f492d179b0c01ae55b3b` |
| Corrected `VERIFIED_CORRECTIONS.md` read at06:11 UTC | `f349e1e5dede87089851c31eca0b275a4e52c29fad19cfe44c2d8e4f234b9438` |
| Corrected `manuscript/main.tex` read at06:11 UTC | `bd5d25a00785a5de65051facecc98e9440f86858eff2c76282cbc9c8cb9f4b50` |
| This report before this addendum, preserving the erroneous closing paragraph as history | `6c4118468e40d4417667fe88bd945fcad108b34982636e74d6f16c2adec50f63` |

Assigned normalization re-audit completion:100%. Only this report was edited. No upstream, Git, publication or external communication action was performed.
