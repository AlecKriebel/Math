# Mirror-quintic orbifold leading terms: exact audit and bounded result

Date: 2026-10-21. Queue 1863 / problem ID 20000721.
Status: PARTIAL PROGRESS / EXISTING LOW-GENUS ANSWER VERIFIED. The original unqualified all-genus question is not closed. No novelty claim is made for HKQ coefficients, period formulas, or the support rule. No GitHub or queue changes are part of this work.

## Target and acceptance contract

The primary target is the leading orbifold terms of the genus-g B-model free energies for the quintic quotient in AIM problem 4.1, not classification of analytic singularities. The source-recovery gate already verified the original wording. Its unspecified coordinate and frame must be fixed before accepting numbers.

Write u=−z_AIM/5, Ψ=u^5, and x=1/(5^5 Ψ). Here x is the large-radius algebraic coordinate, not its exponentiated flat coordinate Q. Choose compatible fifth roots. The quotient is taken to be the standard effective Greene–Plesser diagonal group { (ζ_i)∈μ5^5 : ∏ζ_i=1 } / diagonal μ5, isomorphic to (Z/5)^3, with the smooth crepant mirror interpretation implicit in HKQ. No unrestricted equivalence between stack and resolution potentials is asserted. Let ω_k=u^k A_k(Ψ), k=1,…,4, with A_k(0)=1, and set s=ω_2/ω_1. We use HKQ §3.4's orbifold polarization, antiholomorphic limit, and rescaled periods ωhat_(k−1)=5^(3/2)ω_k. Genus zero has its quadratic integration terms fixed to zero; genus one has its additive constant fixed to zero. Only with this contract do the coefficients below have the stated meaning. On the LG side t=5u and τ=5s identify the normalized period ratios. This alone does not identify higher-genus potentials.

## Approach 1: audit of inherited/generated expansions

We inspected the primary HKQ §3.4 text, its period formula, Yukawa formula, holomorphic-limit prescription, and displayed four coefficients at each genus 0–5. The inherited first two coefficients in each genus match that source. The machine-readable transcription in exact_checks.json contains all 24 displayed coefficients, distinctly labelled as transcription. An independent derivation below reproduces eight of them, the four genus-zero and four genus-one coefficients. Genera 2–5 are NOT independently recomputed here.

The first two coefficients in this fixed normalization are:

- F0 = (5/6)s^3 + (5/1008)s^8 + O(s^13).
- F1 = −s^5/9 − (163/18144)s^10 + O(s^15).
- F2 = (155/18)s^2 − (5/864)s^7 + O(s^12).
- F3 = (488305/9072)s^4 − (3634345/979776)s^9 + O(s^14).
- F4 = (48550/567)s + (36705385/163296)s^6 + O(s^11).
- F5 = (1237460905/224532)s^3 + (108607458385/28740096)s^8 + O(s^13).

These are existing HKQ computations. The HKQ text calls the higher-genus orbifold quantities predictions. Modern GW/BCOV results materially strengthen the foundations, but this audit has not executed the full continuation/polarization dictionary needed to promote every entry to an independently proved geometric orbifold invariant. In particular, merely invoking the genus-two GW theorem is not a coefficient verification in this frame.

## Approach 2: exact Picard–Fuchs and frame transform

Put θ=Ψ d/dΨ. The local period equation is

    [Ψ θ^4 − ∏_(j=1)^4(θ−j/5)]ω = 0.

It follows from the usual large-radius equation θ_x^4−5x∏_(j=1)^4(5θ_x+j) by θ_x=−θ and x=(5^5 Ψ)^−1. For ω_k=Ψ^(k/5)∑_(n≥0)a_(k,n)Ψ^n with a_(k,0)=1, direct coefficient comparison gives

    a_(k,n) = a_(k,n−1) (n−1+k/5)^4 / ∏_(j=1)^4(n+(k−j)/5),  n≥1.

All denominators are nonzero. Thus each normalized solution is uniquely determined without fitting coefficients. Equivalently a_(k,n)=5^(5n)(k/5)_n^5/(k)_(5n), the HKQ expression. The recurrence ratio tends to 1, proving radius of convergence 1 in Ψ for these A_k. In particular these are genuine convergent germs, not just numerically suggested formal series.

Writing H=A_2/A_1 gives

    s=u H(u^5)=u[1+(13/360)u^5+(110069/9979200)u^10+…].

Since H(0)=1, the analytic inverse-function theorem supplies a local inverse u=s K(s^5). Uniqueness and equivariance prove the stated form; exact_checks.py computes it through s^21 and verifies composition. The source LG components obey I0(5u)=A_1(u^5), I1(5u)=5u A_2(u^5), hence τ/5=s, not merely to two orders but as the corresponding normalized convergent period ratios.

For g≥2, frame matters independently of coordinate: if the chosen period trivialization a is multiplied by a nonzero constant c, the normalized genus-g scalar formed as a^(2g−2) times the raw section is multiplied by c^(2g−2). More generally a nonvanishing invariant factor h(s^5) mixes coefficients within a residue class. Genus one uses its separate logarithmic formula and additive normalization; its anomalous transformation is not captured by substituting g=1 in that homogeneous weight. Neither a raw variable replacement nor this scalar adjustment performs the change of polarization. HKQ explicitly selects a new polarization and holomorphic limit; substituting s into the large-radius holomorphic scalar is not the procedure proved here.

## Approach 3: monodromy and exact selection rule

The period basis has monodromy ω_k→ζ^k ω_k under u→ζu, with ζ^5=1. Therefore s→ζs. For a regular scalar satisfying the HKQ monodromy covariance F_g(ζs)=ζ^(2g−2)F_g(s), coefficient comparison proves

    F_g(s) ∈ s^r C[[s^5]],   r the least nonnegative residue of 2g−2 mod 5.

This covariance is the genus-by-genus consequence of HKQ's simultaneous transformation of s and the squared string coupling λ²→ζ³λ². It is not a consequence of regularity alone. Under the stated normalization it rules out quadratic-or-lower additions to F0; an additive constant remains allowed at genus one and is explicitly set to zero.

There is a separate elementary FJRW proof. For a quintic 5-spin line bundle with n insertions of multiplicity 2, the coarse degree is (2g−2+n−2n)/5=(2g−2−n)/5. It must be an integer; hence correlators vanish unless n≡2g−2 mod 5. The claim is about the specified narrow primary insertions, not arbitrary states or descendants. No all-genus LG/CY identity is needed for this proof, and none follows from it.

If q=c s H(s^5), c≠0 and H(0)=1, formal/analytic inversion is equivariant, so residue-class support survives. Multiplication by an invariant nonvanishing frame factor also preserves it. A non-equivariant coordinate such as q=s+s² need not preserve support.

The selection rule does NOT prove nonvanishing at the least allowable exponent. Locally both 0 and c s^r (for any c), as well as s^(r+5m), satisfy regularity and the same covariance. For g≥2 with g≡1 mod5 a constant is allowed; genus 6 is the first such case. At genus one the chosen normalized series has no constant and may start at s^5. No positivity or universal nonvanishing assertion has been obtained.

## Approach 4: independent finite-genus checks

Let J=ds/du=H+5ΨH'. Transforming the HKQ Yukawa tensor with ωhat_0=5^(3/2)uA_1 gives exactly

    C_sss = 5 A_1(u^5)^−2 (1−u^5)^−1 J(u)^−3.

This follows directly from C_ΨΨΨ=5/[Ψ²(1−Ψ)], multiplying by ωhat_0^−2 and (dΨ/ds)^3. The factors 125 cancel; omitting the period rescaling would leave the wrong constant. Reversion into s and three integrations, with no quadratic terms, independently reproduce the four displayed HKQ genus-zero terms:

    (5/6)s³ + (5/1008)s⁸ + (5975/10378368)s¹³
    + (34521785/266765571072)s¹⁸.

The Guo–Ross genus-one formula, in its proved small-FJRW convention, becomes

    F1(5s(u)) = −(31/3)log A_1(u^5)
                −(1/12)log(1−u^5) −(1/2)log J(u).

Here the left side uses τ=5s, and dτ/dt=ds/du because t=5u. Exact rational logarithmic expansion and reversion yield

    −s⁵/9 − (163/18144)s¹⁰ − (85031/46702656)s¹⁵
    − (6909032915/20274183401472)s²⁰,

agreeing with all four displayed HKQ genus-one coefficients. This is an independent finite-order check against a rigorous genus-one formula, not an extrapolation from two known terms. At u=0 the factors A_1 and J equal 1, so their reciprocals and logarithms with log(1)=0 are analytic on a sufficiently small disk. Thus the normalized genus-zero and genus-one formulas in this calculation define actual analytic germs; no assertion about convergence of the full sum over genera is implied.

Reproducibility: run `python exact_checks.py` with SymPy. Every arithmetic operation is exact rational/symbolic. The script checks 16 recurrence coefficient equations, inverse composition through (s^5)^4, the eight low-genus coefficient matches, all 24 displayed residue checks, and the ambiguity-index count for genera 2–53. The extra genus-zero s^23 coefficient in the JSON is an output of this same local Yukawa formula, not a claimed new theorem or new invariant.

## Approach 5: all-genus obstruction and current status

There are two distinct obstacles, not a single missing-gap slogan.

1. Local regularity and covariance leave infinitely many possible scalar germs, as the explicit family above demonstrates. They do not determine even the leading coefficient. This is a precise nonuniqueness statement for those local constraints ONLY, not a proof of global BCOV ambiguity after all enumerative inputs are imposed.
2. In the finite-generation/BCOV reconstruction framework, lower-genus information and anomaly equations leave holomorphic initial data. Liu–Ruan describe remaining indices ceil((3g−3)/5)+1 through g−1 after the stated BCOV boundary constraints, numbering floor((2g−2)/5). This elementary index count is verified by the script; the source's global reconstruction assertions are not re-proved here. It is positive already at genus 4 and grows with genus. Castelnuovo vanishing and additional inputs determine many of these and support the source's reconstruction range through genus 53. That is not an arbitrary-genus orbifold-leading-term formula. Nor does this parameter count prove that every remaining parameter changes the leading orbifold coefficient; that would require an explicit evaluation of the relevant coefficient functional.

### Explicit homogeneous-ambiguity witness (conditional HKQ reconstruction model)

The following sharpens parameter counting and identifies a direction which really changes the leading coefficient. It is an algebraic statement inside HKQ's stated polynomial ansatz, not a claim that the changed potential satisfies all geometric constraints or Castelnuovo vanishings.

Fix g≥2 and all lower-genus inputs. This is a single-genus homogeneous difference, not a simultaneous all-genus solution of the coupled equations. Put X=1/(1−Ψ), m=ceil(3(g−1)/5), and r=5m−3(g−1)∈{0,1,2,3,4}. HKQ write P_g=P̂_g+f_g(X), with f_g a polynomial of degree at most 3g−3. The homogeneous HAE allow adding a polynomial δP(X). Consider only these three further constraints: unchanged large-radius constant map, unchanged conifold principal part, and orbifold regularity.

- The constant-map constraint is δP(0)=0, as HKQ §3.3 explicitly states that only a0 changes that limit.
- In a conifold frame with holomorphic nonzero period, the scalar difference is a local analytic unit times (1−Ψ)^(g−1)δP(X). If deg δP=d, its leading order at Ψ=1 is g−1−d. Thus preserving the whole conifold principal part is equivalent to deg δP≤g−1. Passing to the conifold flat coordinate, whose derivative is nonzero, preserves regularity.
- At the orbifold the difference is a local analytic unit times u^(−3(g−1))δP(1/(1−u^5)). Since X−1=u^5/(1−u^5), regularity is equivalent to (X−1)^m dividing δP.

Therefore the homogeneous solution space for precisely these constraints is

    δP(X)=X(X−1)^m R(X),   deg R≤g−m−2,

interpreted as the zero space when the bound is negative. Its dimension is g−m−1=floor((2g−2)/5). This derives the count directly in HKQ coordinates rather than identifying differently normalized finite-generation variables without proof.

For every g≥4, choose R=1. Using the exact HKQ orbifold frame yields

    δF_g(s(u))=5^(2g−2) u^r A_1(u^5)^(2g−2) (1−u^5)^(g−m−2).

All factors after u^r have constant term 1. Since s=u+O(u^6), the coefficient of s^r changes by exactly 5^(2g−2), which is nonzero. Multiplying δP by any scalar changes it arbitrarily. Thus HAE plus these three boundary constraints, even with a fully proved conifold gap, do not determine the leading orbifold coefficient at any g≥4. The missing information may come from enumerative inputs or stronger global constraints; this witness is not evidence that the genuine geometric potential is ambiguous. It also does not contradict already known finite-genus computations, which use additional inputs.

For a general R the leading change is 5^(2g−2)R(1), so the leading-coefficient functional has rank one on this residual space. The witness is exact for all g≥4, not a numerical extrapolation. At g=2,3 the space is zero; no conclusion about normalization or actual coefficient values follows from that observation alone.

The September 2026 preprint Chang–Guo–You–Zhang, arXiv:2609.13921, claims an all-genus conifold-gap proof. Its Definitions 1.1–1.2 formulate a differential-ring map into formal Laurent series, and Theorems 1–2 give the transfer criterion and quintic application. The inherited claim “the conifold gap remains unproved” is obsolete as a literature summary. We report the new claim without claiming independent validation of its proof or peer-reviewed acceptance. Its theorem is about the conifold, not the orbifold, and is not an all-genus LG/CY theorem. Accepting its claimed result removes that particular hypothesis from compatible reconstruction arguments; it does not by itself calculate the remaining arbitrary-genus initial data or supply a normalized leading-orbifold formula.

For arbitrary genus, this audit has not shown that all additional geometric inputs uniquely reconstruct an arbitrary-genus coefficient, provided an effective closed all-genus formula for it, or proved full quantized GW/FJRW correspondence. The explicit witness above does show failure of uniqueness under the specified incomplete boundary package; it does not settle what all additional geometric inputs imply. These are not silently replaced by the support rule, formal conifold gap, or analytic low-genus calculation.

## Disposition

Accepted bounded results: exact normalized period recurrence and local coordinate transform; exact genus-zero and genus-one agreement through four coefficients each; conditional HKQ monodromy support and separate FJRW selection proof; an explicit fixed-genus homogeneous-ambiguity direction changing the leading coefficient for g≥4 under the specified incomplete BCOV boundary package; documented limits of local and global boundary information; corrected October 2026 status. The existing HKQ leading terms answer the chosen normalization for genera 0–5 as literature computations, with the proof-status qualifications above.

Not accepted: a novel solution to the unqualified all-genus AIM problem, arbitrary-genus nonzero leading coefficients, a proof of all-genus LG/CY, convergence of the genus sum, or an analytic-singularity classification inferred from formal expansions.

## Primary references

- AIM problem 4.1: http://aimpl.org/gromwitnumthry/4/
- Huang–Klemm–Quackenbush, §3.4: https://arxiv.org/abs/hep-th/0612125
- Chiodo–Ruan, genus-zero LG/CY: https://arxiv.org/abs/0812.4660
- Guo–Ross, genus-one LG mirror theorem: https://arxiv.org/abs/1611.08876
- Guo–Ross, genus-one global mirror theorem: https://arxiv.org/abs/1703.06955
- Guo–Janda–Ruan, genus-two GW formula: https://arxiv.org/abs/1709.07392
- Guo–Janda–Ruan, finite generation and orbifold regularity, Cor. 1.5 and Remark 1.6: https://arxiv.org/abs/1812.11908
- Liu–Ruan, Castelnuovo bound and reconstruction discussion: https://arxiv.org/abs/2210.13411
- Chang–Guo–You–Zhang, new conifold-gap claim: https://arxiv.org/abs/2609.13921

Source identity, retrieval metadata, and public PDF hashes are recorded in the separate source-recovery manifest. This deliverable contains authored analysis and public citations, not copies of third-party documents.
