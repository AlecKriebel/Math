# Independent acceptance: final-pass exceptional-five smoothing

14 October 2026 UTC. Row 1777 / 30005572. Independent review within the final shared PASS 5/5; this review adds no mathematical pass. The full construction remains **UNSOLVED**. No novelty claim is made.

## Verdict and frozen inputs

**ACCEPT the restricted results** in the following frozen proofs:

- `pass5_exceptional_smoothing/RAMIFIED_FIVE_TAME_RAY_REMOVAL.md`, SHA-256 `58723b67e6e23fe0f1ff0fff466f40eb3d713285931cc0c4b6b1e2176e890219`.
- `pass5_exceptional_smoothing/EXACT_FIVE_SMOOTHING_OBSTRUCTION.md`, SHA-256 `9be734e6e41a6f10e2a915068248d3584a69798853b5627711f6d35dac191a2f`.

The first proves genuine exceptional-block vanishing, and hence genuine auxiliary removal, when five ramifies in F, 5 does not divide h_F, and every level prime q away from five has Norm(q) not congruent to 1 modulo five. The level is proper and unit-injective. Arbitrary depth at the prime above five is allowed; the full ray group need not have order prime to five.

The second computes the exact exceptional smoothing quotient and gives a sharp five-power annihilator and an exact two-stage test for the actual remaining obstruction. It does **not** evaluate a nonzero obstruction on an actual surviving family. These are different kinds of conclusions and must remain distinguished.

## 1. The arithmetic vanishing is about the actual target

The exceptional character is precisely the quadratic character of F(sqrt(5))/F, the square of the mod-five cyclotomic character restricted to G_F. When five ramifies this quadratic extension is unramified and lies in every ray field. This is the accepted PASS4 convention; the published p>=7 automatic-exclusion slogan is not substituted for it.

Let S contain the unique five-adic place and every level prime, as well as the infinite places. Passing to all ray moduli supported on S identifies the abelian pro-five Galois group with the pro-five part of the inverse limit of ray class groups. The ray-class exact sequence retains the ordinary class group and the image of global units. Under the stated hypothesis the class group has no five-part. Global units have order two, so their pro-five image is trivial. At q away from five, principal units are pro-ell and residue units have order Norm(q)-1, prime to five. Thus these places supply no pro-five unit contribution.

The remaining local factor is the principal-unit group at the ramified quadratic completion F_v/Q_5. It has no fifth roots of unity: adjoining a primitive fifth root to Q_5 has degree four, which cannot fit inside a quadratic field. The local unit structure therefore gives a torsion-free Z_5-module of rank two. In fact the convergent logarithm identifies its first principal-unit group with the additive maximal ideal, because its least positive five-adic valuation is 1/2>1/4. There is no unaccounted finite five-torsion or p-adic global-unit quotient. Consequently the actual G_{F,S} has dim H^1(G_{F,S},F_5)=2.

The global Euler characteristic is applied to the full restricted-ramification Galois group, with trivial coefficients F_5. Its value over an imaginary quadratic field is 1/5, so dim H^0-dim H^1+dim H^2=-1. Since H^0 has dimension one, H^2(G_{F,S},F_5)=0. The computation is not a claim about compactly supported cohomology, and it is not made with an uncancelled Tate twist.

## 2. The wild finite-cover step does not average a five-group

This is the essential enlargement beyond the initial prime-to-five ray-degree statement. Write Q=P x Q', with P its five-Sylow subgroup, and L_0=L^P. All extensions considered become finite etale after removing S. Their restricted-ramification Galois groups form an actual open normal subgroup pair H=G_{L,S_L} inside G=G_{L_0,S_{L_0}}, with quotient P. This identification uses stability of being unramified outside S under Galois closure.

The group G has five-cohomological dimension at most two. Hence H^2(G,-) is right exact on discrete finite five-primary modules. The presentation

A_0^m -> A_0 -> F_5 -> 0, with A_0=F_5[P],

uses right multiplication by g_j-1 on the left regular P-module. These are G-linear maps. Factoring through the augmentation ideal and applying two short-exact-sequence cohomology sequences verifies right exactness at precisely the two places needed. Shapiro identifies H^2(G,A_0) with H^2(H,F_5). The induced right regular maps are the deck actions, possibly inverted; inversion leaves the coinvariant quotient unchanged. Thus the cokernel is exactly

H^2(H,F_5)_P = H^2(G,F_5),

with the identification induced by corestriction. This construction is natural for the remaining Q' action. It does not assert that P-invariants are exact and does not divide by |P|. It also does not replace the full Galois group by its maximal pro-five quotient in a cohomological-dimension argument.

The coefficient mu_5 tensor mu_5 is trivial over L_0, since L_0 contains F(sqrt(5)); its descent character over F is chi. Taking its chi-part is therefore taking the trivial part of the untwisted cohomology. Only Q', whose order is prime to five, is averaged. This proves that the P-coinvariants of the entire upstairs mod-five chi-module vanish. The augmentation ideal of F_5[P] is nilpotent, so Nakayama makes that entire module zero. There is no appeal to coinvariants preserving a subgroup injection.

## 3. Comparison and the localization boundary

The odd-prime comparison identifies K_2(O_L[1/S_L]) tensor Z_5 with H^2_et(O_L[1/S_L],Z_5(2)). The coefficient exact sequence injects the quotient of this cohomology by five into H^2_et(mu_5 tensor mu_5). No extra H^3 vanishing is needed for that injection. Projection to chi is exact because it is the Q'-idempotent projection, even when P is nontrivial. The previous section gives a zero quotient by five; finiteness of S-integer K_2 then gives zero for the entire completed chi-group.

Only after this full-group vanishing does the proof use the equivariant injection from K_2(O'(N)). The injection follows from localization and K_2 of a finite field being zero. Tensoring with Z_5 is flat. In particular, the proof does not assume that reducing an arbitrary subgroup inclusion modulo five remains injective.

The exact O'(N) convention is preserved: it is O_L[1/N] at a prime-power ideal level and O_L otherwise. The proof is permitted to enlarge both rings further by removing S, because it proves zero in the larger group and then returns to the subgroup. It does not claim to improve the nonexceptional prime-power target to the integer ring.

Actual auxiliary values on the exceptional block are zero because their coefficient module is zero. Thus the zero unaugmented block is forced and unique. This is a valid source-calibrated conclusion, not an arbitrary zero map chosen to imitate Hecke eigenvalues. All other five-blocks still use the accepted unit-smoothing construction.

## 4. Exact smoothing quotient at arbitrary depth

Write (5)=p^2, n=v_p(N), and a=max(1,ceil(n/2)). The local calculation is correct. For a uniformizer pi with pi^2=5u, O_{F_p}=Z_5[pi] and trace(a+b pi)=2a. The even and odd maximal-ideal powers have trace ideals 5^ceil(n/2) Z_5. Logarithm, exponential, and trace/norm compatibility give

Norm(1+p^n)=1+5^ceil(n/2) Z_5 for n>=1.

Squaring is invertible on these principal-unit groups. At n=0 the squared residue norm is one modulo five, and a first-order principal unit realizes exact valuation one. CRT therefore produces a proper integral principal ray auxiliary c_0 with smoothing factor exactly 5^a times a five-adic unit.

The calculation uses (Norm c)^2 throughout. For a rational scalar t, this is t^4, not t^2. It is distinct from the scalar-theta coefficient ideal in PASS3.

The squared five-adic cyclotomic character modulo 5^a factors through the ray group, while a principal ray auxiliary shows failure modulo 5^(a+1). Dividing its Teichmuller part chi leaves rho_a on P. The evaluation map Z_5[P] -> Z/5^a annihilates J. Conversely, Chebotarev supplies auxiliary ideals whose ray classes are (g_j,1), for generators of P. Their smoothing relations make every g_j scalar in the quotient; c_0 kills 5^a. The two opposite surjections therefore identify the quotient exactly with Z/5^a. This proves the complete quotient, not merely its residual support.

In particular the common annihilator at depths zero, one, or two is M[5]^P. At greater depth the nontrivial rho_a action and the larger exponent must be retained. Replacing the ideal by the ordinary maximal ideal at every depth would be incorrect.

## 5. The actual obstruction test and the unconstructed auxiliary

For the actual auxiliary cohomology classes, exchange and c_0 construct v with s_c v=5^a a_c. This proves that 5^a annihilates their existence obstruction. If an unaugmented class exists then v lies in 5^a M. If it does lie there, a chosen root leaves a residual family in M[5^a]; its class modulo residual smoothing families is independent of the choice. Vanishing of that second class is both necessary and sufficient. The ambiguity is exactly M[J]. These conclusions follow by direct module algebra and do not divide by a nonunit in a finite K_2 group.

The tests have not been evaluated on an actual family outside the new vanishing theorem. The formal finite-module counterexamples in the checker are expressly not arithmetic data.

The analysis of a five-divisible auxiliary is also valid at its limited scope. For d dividing (5), its degree-zero torsion cycle is nonzero but its scalar-five pushforward is zero. Thus it cannot be the boundary of a literally scalar-five-fixed primitive. Changing the desired eigenvalue to zero leaves the known constant five-torsion ambiguity. This invalidates that shortcut to the accepted normalization; it does not prove that every alternative construction is impossible.

## 6. Examples, source inspection, and reproducibility

The final examples are correct. In Q(sqrt(-5)), three splits and |Cl_(3)|=4. Thirteen is inert, giving Norm((13))=169 and ray degree168, with the prime-power localized target. Eleven is inert, giving norm121 and degree120; it violates the tame-norm hypothesis. An earlier draft's inertness assertion for seven was corrected before freezing: seven splits. The final proof does not contain that error.

The author checker was read and independently replayed under Python -O and -OO, with identical output. It verifies nine local depth minima, the three final ray examples, and 125 compatible formal families (five soluble, 100 first-stage failures, 20 second-stage failures). These are finite support checks, not a computation of general arithmetic K_2 or of a surviving actual obstruction.

Primary academic sources inspected for the imported statements:

- Milne, *Arithmetic Duality Theorems*, second edition, I Theorem4.10(c), printed p.57, and I Theorem5.1, printed p.67: https://www.jmilne.org/math/Books/ADTnot.pdf . They supply full-group higher-cohomology vanishing and the global Euler formula under the stated S hypotheses.
- Milne, *Class Field Theory*, V Section1, especially Theorem1.7: https://www.jmilne.org/math/CourseNotes/CFT.pdf . The ray-class sequence is applied by inverse limit; the rank-two conclusion above is checked from its actual local factors.
- Banaszak–Popescu, *On the Stickelberger splitting map in the K-theory of number fields*, arXiv:1008.1000v1, Theorem1.3, Section6 (pp.17–18), and equation(37), p.22: https://arxiv.org/pdf/1008.1000 . These explicitly state the odd-prime K_2 comparison, its S-integer extension, and the H^2 identification used here. No conjectural higher-K comparison from that paper is used.
- Tate's original bibliographic record is https://doi.org/10.1007/BF01390012 . The publisher's full original PDF was not accessible during this review; the exact S-integer theorem was checked through the foregoing author research paper. A previously retained local file labeled as Tate is actually Bass and was not used as evidence for Theorem5.4.
- The retained LSSW author manuscript was inspected at Sections4.3 and5.2: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . Its p>=7 theorem and existing source conventions are used only at their accepted scope.

No source PDF or copied source text is part of this acceptance report. The proof does not settle five-divisible class numbers, tame level norms congruent to one modulo five, missing small-level descent, full compactification, unrestricted bad-U, prime-power absolute integrality, or the prescribed relative calibration. The original full construction remains UNSOLVED.
