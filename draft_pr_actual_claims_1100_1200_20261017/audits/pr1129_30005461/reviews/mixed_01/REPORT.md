# Independent adversarial audit: credited mixed odd SOS exponents

**Verdict: PASS for the full credited mixed-exponent clause.** No actionable mathematical gap was found in the frozen credited proof. Both disclosed source-index errors are genuine, and the explicit corrections preserve the full claimed conclusion. This verdict was reached from fresh primary-source inspection, independent derivation, and independently authored exact checks; the inherited acceptance verdict and historical computation counts were not treated as evidence.

Audit date: 17 October 2026 UTC. Assignment: PR1129 / problem 30005461 / OWR-12697710-007. Assigned snapshot: `26fed29c1130e539ba018a37200f133870f0e036`. No Git references were inspected or changed.

## Exact scope and frozen inputs

Let SOS mean a finite sum of squares of real polynomials in a common ring `R[x_1,...,x_d]`. The entire clause tested is:

> For arbitrary real multivariate polynomials p,q and integers i,j >= 0, if p^(2i+1) and q^(2j+1) are SOS, then (p+q)^(2i+2j+1) is SOS.

The hypotheses do not require equal degrees, nonzero inputs, positive definiteness, or positive i,j. Success requires the exponent exactly as stated, without a denominator or additional multiplier. Credit belongs to Blekherman–Kozhasov–Reznick (BKR), with the truncated-binomial ingredient credited to Iosif Pinelis. This audit makes no novelty claim.

The three specified byte identities were checked afresh in both computation modes:

| Input | Bytes | SHA-256 |
|---|---:|---|
| CREDITED_MIXED_EXPONENT_PROOF.md | 7385 | be068e1471372383675640c282109ae82c2c74d3856a4e6bedf046dead97473c |
| PROOF.md | 10963 | 46af7394ebfee7b0de9861693f84ab684502da3be208c626411f24e2538c7d15 |
| MATHEMATICAL_AUDIT.md | 13253 | f9faede12ad50034f5620f4576c621dc275a6ddbbf29bb3e13096d778a094cce |

I read the complete credited proof, the complete supplied substantive audit, and the README/source-review/source-metadata scope. The principal proof was read for the target and notation interface. Its essential geometry is assigned to a separate reviewer and is not independently accepted by this report. The optional real-delta appendix is outside this report's mathematical verdict.

## Fresh primary-source findings

The full current published [BKR article](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares/7C4BAF1C7EBA17DE741C36DB40691412) and its 25-page typeset PDF were retrieved, as were [arXiv v1](https://arxiv.org/abs/2407.21779v1), the original [OWR report](https://ems.press/content/serial-article-files/47007), and the actual [Pinelis MathOverflow discussion](https://mathoverflow.net/questions/444079/are-truncated-even-degree-binomial-polynomials-psd). Bodies, extracted text, and rendered page images remain under ignored `sources/private/`. Metadata and precise inspection boundaries are in SOURCE_INSPECTION.md and FETCH_LEDGER.json.

BKR is a published article in Forum of Mathematics, Sigma 14 (2026), e65, DOI `10.1017/fms.2026.10221`, with the publisher displaying online publication on 27 April 2026. Published Theorem 5.3 is the mixed odd-exponent result in the notation defined by equation (1.6); arXiv v1 labels it Theorem 44. Its printed proof uses the full two complementary binomial ranges needed below. Published Theorem 5.2 states the even-truncation positivity lemma correctly. Its complete proof was read; no further difficult imported result is hidden in this elementary route.

The MathOverflow question and sole answer were inspected in full. The answer is by Iosif Pinelis, dated 3 April 2023, and gives the derivative/Pascal critical-point induction. This independently confirms the ingredient attribution that the supplied package had historically verified through BKR only. This is a fresh audit fact, not a correction to the package's accurately limited historical inspection statement.

On original OWR printed p.780, I visually checked the arbitrary-polynomial mixed-exponent conjecture and the exact affine threshold family. The distinct positive-definite perturbation elsewhere on that page was not substituted for it.

### Both display corrections are necessary and already present

1. **Archived positivity index:** arXiv v1 Theorem 43, printed p.20, states positivity using `f_{n,r}` under `n>2r`, whereas its base case and intended result use `f_{n,2r}`. The archived proof on p.21 also drops the factor 2 in critical-point expressions. The false literal claim fails at `n=3,r=1,t=-1`: `1+3t=-2`. Current published Theorem 5.2 and its critical-point proof consistently use the even index. The general identities written with a generic index r are themselves valid; they do not require correction.
2. **Homogenization limit:** arXiv v1 p.21 and current published PDF p.22, as well as current publisher HTML, display an upper summation limit r in the form denoted `F_{n,2r}`. The correct limit is `2r`. At `n=3,r=1`, the literal displayed polynomial `v^2+3uv` has value -2 at (-1,1); its actual homogenized counterpart is `v^2+3uv+3u^2`, with value 1 there. This was checked in the rendered page images, not inferred only from text extraction.

The frozen CREDITED_MIXED_EXPONENT_PROOF.md Section 3.3 explicitly discloses precisely these errors. Its Sections 3.1–3.2 use corrected indices throughout. Thus there is no silent weakening, false lemma left in use, or theorem newly claimed because of a typographical repair. The optional remark about another preprint's Theorem 2.2 was not independently rechecked: neither this verdict nor the credited proof's mathematical sufficiency depends on that comparison.

## Universal mathematical reconstruction

Put `a=2i+1`, `b=2j+1`, and `N=a+b-1`. They are positive odd integers. Define, for `0<=m<N`,

    f_{N,m}(t) = sum_{k=0}^m binom(N,k)t^k,
    B_{N,m}(u,v) = sum_{k=0}^m binom(N,k)u^k v^(m-k).

### Positivity: check of the supplied proof

For positive even m, the base `N=m+1` gives

    f_{m+1,m}(t) = (1+t)^(m+1)-t^(m+1) > 0

because an odd power is strictly increasing. For `N>=m+2`, coefficient identities give

    f'_{N,m}=N f_{N-1,m-1},
    f_{N,m}=f_{N-1,m}+t f_{N-1,m-1}.

The degree m is even and its leading coefficient is positive, so the function has a global minimum. At a minimizer t_0 the derivative vanishes, making the second summand vanish. Induction applies because `N-1>m`; it gives `f_{N,m}(t_0)=f_{N-1,m}(t_0)>0`. For m=0 the polynomial is 1. The induction has a genuine base and decreases N while holding m fixed. It does not assume the desired mixed-exponent conclusion.

The condition `N>m` matters for strict positivity: at `N=m=2`, `f_{2,2}(-1)=0`. Evenness also matters: `f_{5,3}(-2)=-49`. Neither excluded case occurs in the mixed split, since `N-(a-1)=b>=1` and `N-(b-1)=a>=1`.

### Independent universal positivity and SOS mechanism

An independent identity, useful for falsifying a possible defect in the critical-point route, is

    f_{N,m}(t)
      = (N-m) binom(N,m) integral_0^1 (t+s)^m(1-s)^(N-m-1) ds.

It holds for every integer `0<=m<N`. Indeed, for `0<=k<=m` the coefficient of t^k on the right is

    [N!/(m!(N-m-1)!)] [m!/(k!(m-k)!)]
      * integral_0^1 s^(m-k)(1-s)^(N-m-1) ds
    = N!/[k!(N-k)!] = binom(N,k).

The integral evaluation is the integer beta integral, obtainable by repeated integration by parts. For even m the integrand is nonnegative and is positive on an interval: if m>0 its only possible zero inside (0,1) is a single point; for m=0 it is positive throughout. Hence the integral is strictly positive for every real t, including arbitrarily negative t.

Homogenizing gives the polynomial identity

    B_{N,2r}(u,v)
      = C integral_0^1 [(u+s v)^r]^2 (1-s)^(N-2r-1) ds,
    C=(N-2r)binom(N,2r)>0.

This already includes v=0 and has no denominator. More explicitly, with monomial vector `z_l=u^(r-l)v^l`, `0<=l<=r`, its Gram matrix is

    Q_{ij}=C binom(r,i)binom(r,j)
           * integral_0^1 s^(i+j)(1-s)^(N-2r-1) ds.

For every nonzero vector w, `w^T Q w` is the integral of the square of the nonzero polynomial `sum_i w_i binom(r,i)s^i` against a strictly positive weight on (0,1). It is strictly positive. Therefore Q is positive definite and admits an ordinary real Cholesky/LDL decomposition. Consequently B is a finite SOS of degree-r binary forms. This is a universal proof, rather than a claim inferred from finitely many positive pivots. It supplies an independent route to exactly the polynomial SOS factors required by the source proof.

The supplied alternative two-square factorization is also valid: a strictly positive real polynomial of degree 2r has no real roots and factors into conjugate pairs with multiplicity. Choosing one member from every pair, with positive leading-coefficient square root, gives a complex polynomial h of degree r with `f=h*conjugate(h)`. Real and imaginary parts give two real polynomial squares. Multiplying each root by `v^r` after substituting t=u/v is polynomial because its degree is at most r. Equality at v=0 follows as a polynomial identity, not from pointwise division by v after substitution.

### Exact binomial partition and the SOS conclusion

The decisive identity is

    (u+v)^N = v^b B_{N,a-1}(u,v) + u^a B_{N,b-1}(v,u).

The first block has u-exponents `0,...,a-1`. The second block has u-exponents `N,...,N-(b-1)=a`. Its coefficient at u^(N-k)v^k is `binom(N,k)=binom(N,N-k)`. Thus the two ranges partition all `0,...,N` exactly once. All their coefficients are positive integers. The reversed arguments in the second binary factor are essential.

Both binary factors are SOS by the preceding universal proof. Write `p^a=sum_l A_l^2`, `q^b=sum_h C_h^2`, and choose binary roots G_1,G_2 for the first factor and H_1,H_2 for the second. Substituting u=p,v=q yields

    (p+q)^N
      = sum_h sum_{t=1}^2 [C_h G_t(p,q)]^2
        + sum_l sum_{t=1}^2 [A_l H_t(q,p)]^2.

All factors are polynomials in the original variables. Products of SOS are justified by distributing the finite square sums. The equation proves the exact requested exponent. It uses no rational functions, divisibility inference, density of an input image, degree equality, or strict positivity of p and q.

## Homogenization and vulnerable boundary cases

The separate homogenization argument in Section 4 of the frozen credited proof is sound. Choose a positive even integer D at least the degrees of both nonzero inputs, and define

    P(x,z)=sum_alpha p_alpha x^alpha z^(D-|alpha|),
    Q(x,z)=sum_alpha q_alpha x^alpha z^(D-|alpha|).

These are forms of common degree D, including the zero form as an element of that graded space. Odd SOS powers imply p,q>=0 pointwise. Since D is even, P,Q>=0 for z!=0, and their continuous polynomial values remain nonnegative at z=0.

For any nonzero square root A_l in `p^a=sum A_l^2`, its degree is at most aD/2. Otherwise the maximal-degree homogeneous parts of the A_l would have a sum of squares identically zero. Evaluating at real points forces each of those top parts to vanish, contradicting maximality. Hence

    P^a = sum_l [sum_alpha (A_l)_alpha x^alpha z^(aD/2-|alpha|)]^2.

Every exponent of z is a nonnegative integer. The same argument applies to Q^b. The published homogeneous theorem therefore applies to the common degree D without an extra multiplier. The output roots in the two blocks have degrees

    bD/2 + D(a-1)/2 = ND/2,
    aD/2 + D(b-1)/2 = ND/2.

Dehomogenization z=1 yields the original conclusion. Choosing D odd would fail the sign and integral-half-degree requirements, but the actual proof expressly chooses D even.

- **Unequal degrees and any finite variable count:** substitution in the binary identity requires no degree condition. For the alternative source interface, common even-degree padding supplies precisely the missing common degree.
- **i=0 or j=0:** a=1 or b=1 makes the relevant binary factor `B_{N,0}=1`; no derivative at index -1 is used. If both are zero, N=1 and the conclusion is ordinary closure of SOS under addition.
- **p=0 or q=0:** the split remains a polynomial identity. For example, p=0 leaves `q^N=q^b*(q^((a-1)/2))^2`. Both zero give zero. No cancellation by p or q occurs.
- **Constants:** nonnegative constants meet the required hypotheses and work either directly or by even-degree padding. A negative constant cannot satisfy an odd SOS hypothesis.
- **Zeros and negative input values:** zeros are allowed throughout. A negative value of p or q is forbidden by its odd SOS hypothesis, not by an extra unstated assumption. The universal binary identity and its SOS factors were established for signed u,v anyway.
- **Infinity in the binary homogenization:** at v=0, the correct B is `binom(N,m)u^m`; for m even this is nonnegative, with no omitted leading term or division problem. The independent integral representation verifies this directly.

## Threshold notation interface and limited source-priority observation

Published BKR Theorem 6.3 concerns `M_c=x^4y^2+x^2y^4+z^6-cx^2y^2z^2`, with `V_{2k+1}=(-infinity,c_k]` and `0<=c_k<3`, for k>=0. This is the same sequence as the affine problem: setting z=1 gives f_c, and homogenizing f_c^(2k+1) to its exact degree `6(2k+1)` recovers M_c^(2k+1). Square roots in an affine SOS have degree at most `3(2k+1)`, so the reverse implication introduces no z multiplier. Parameters c>3 are excluded by the negative value at (1,1,1), or at (1,1) affinely. Thus the package's threshold notation is correctly aligned with the source.

The source's monotonicity follows by multiplication by M_c^2; the interval endpoint includes equality because the relevant finite-degree SOS cone is closed. The first-clause theorem with the other summand SOS establishes downward closure. These interfaces do not import the principal proof's geometric mechanism.

In the **inspected BKR current full-body Section 6**, the limit-3 question is still posed as a question. Original OWR p.780 also asks for that limit. Pinelis's discussion supplies the binomial ingredient, not a statement resolving the exact Motzkin limit. I did not find an explicit prior answer to the full two-clause target in these inspected primary bodies. This is a narrow source observation, not an exhaustive novelty/priority audit and not a denial of results elsewhere.

## Exact falsification artifacts and results

The independently authored standard-library program `verify_mixed.py` uses rational arithmetic, coefficient dictionaries, and explicit `RuntimeError` guards. It does not import or reuse historical verification code. Normal Python and Python -O each passed **181,634 explicit checks**, and their JSON results are byte-identical. `verify_runs.py` additionally invokes a deliberately failing guard in each mode; both exit nonzero with the expected explicit error. RUN_VALIDATION.json records the runtime and result digest.

Useful tested families include:

- All 1,296 odd pairs a,b in {1,3,...,71}, checking the complete coefficient-exact partition and parity/range conditions.
- Derivative/Pascal coefficients, base polynomials, and the independently derived beta-integral coefficients.
- Positive rational moment-matrix pivots, exact LDL reconstruction, and exact weighted-SOS reconstruction for 32 binary examples, including r=0 and r=7.
- Ten explicit multivariate SOS constructions using degrees 2 and 4, unequal odd exponents, zero polynomials, positive constants, and a=1 or b=1. The checker verifies 187 final weighted polynomial squares and their homogenizations to D=4 and D=6.
- Rational signed samples and v=0 in the binary factors, together with the exact affine/homogeneous threshold family transcription.

All 11 adverse controls are detected: the two literal source errors; strict positivity when N=m; an odd truncation; an omitted split endpoint; unswapped binary arguments; erasing B_{N,0}; odd-degree padding; incorrectly inferring nonnegativity from an even SOS power; a half-integral root degree; and an above-endpoint negative odd Motzkin power.

EXACT_BINFORM_CERTIFICATES.json preserves, for example, the coefficient-checkable identity

    B_{9,4}(u,v)
      = 126 (u^2 + uv/3 + v^2/21)^2
        + 10 (uv + v^2/4)^2 + (5/56)v^4.

The weights are strictly positive, so they may be absorbed into real square-root coefficients. No claim of rational square roots is needed. The finite checks support the transcription and constructions; the universal statements are justified by the proofs above.

## Remaining gap, disposition, and boundaries

**Strongest verified result:** the entire arbitrary-real-polynomial mixed-exponent implication, with the exact exponent, all listed boundaries, and correct existing attribution. The alternate homogenization route to published Theorem 5.3 is also valid. The published Theorem 6.3 notation matches the principal proof's affine thresholds.

**Exact remaining mathematical gap in this clause:** none identified. No repair is required. This is independent AI-assisted mathematical review, not human peer review or formal proof-assistant certification. It does not accept the separately assigned principal geometry by proxy, establish explicit exponents for that geometry, or give exhaustive literature clearance.

All writes were confined to this assigned review folder. No other worker, original input, tracker, Git reference/index/remote, PR, publication, or release was changed. No external individual was contacted. Third-party full bodies, text, images, and raw source material remain ignored and private. AUTHOR_ARTIFACT_RECEIPT.json fingerprints authored audit artifacts excluding itself and the ignored private/intermediate trees.
