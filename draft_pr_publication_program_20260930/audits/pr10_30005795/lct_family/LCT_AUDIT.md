# Independent adversarial audit of the PR10 LCT bound

Frozen input: `source_snapshot/BOUND.md`, PR head `925f9e9f46f2c7407fd142cedf36995a4519a378`. Audit completed 2026-10-01 UTC. Read BOUND.md before status or prior verdicts. This certificate concerns the threshold argument and its edge cases; it does not establish the separate Mori-dream-space or source-priority claims.

**Disposition: the mathematical bound and optimal-constant identity pass in the stated algebraic Fano setting, with one minor terminology repair at line 56.** No counterexample was found within the hypotheses. A finite-type normal complex algebraic klt surface, a finite family of actual effective Cartier divisors, nonnegative weights with defined finite integrals, and surface divisorial valuations suffice. Du Val surfaces satisfy the surface hypothesis. Properness of S is not needed for this abstract argument.

## 1. Exact claim and independent certificate

Let S be a normal finite-type complex algebraic surface with (S,0) klt. Thus K_S is Q-Cartier and every log discrepancy A_S(F) is positive. Let D_1,...,D_r be effective Cartier divisors, and let w and f_j be nonnegative functions whose products are integrable with finite integrals a_j. Assume the displayed equality N(u)|_S=sum_j f_j(u)D_j is equality of actual R-Cartier divisors (not merely numerical or linear equivalence). Define I(F) as in BOUND.md.

Discard zero D_j. The strongest verified conclusions are

    I(F)=sum_j a_j ord_F(D_j)=ord_F(B),  B=sum_j a_j D_j,
    I(F)<=K0 A_S(F),  K0=sum_j a_j/lct(S;D_j),
    Kopt=0 if B=0,
    Kopt=1/lct(S;B) if B!=0.

The last constant is attained by a divisor on a finite log resolution. The proof uses no identity that combines the individual thresholds into the threshold of their sum.

Choose a single log resolution pi:Y->S of the finite support of B and the singularities of S. Include all exceptional divisors and all strict transforms of components of B in a finite list E_i with SNC union. Write

    K_Y=pi* K_S+sum_i k_i E_i,
    pi* B=sum_i m_i E_i,
    A_i=A_S(E_i)=1+k_i>0.

For strict transforms, k_i=0 and A_i=1. Since B is a nonnegative real combination of effective Cartier divisors, each m_i>=0. If B!=0, some strict transform has m_i>0, so

    c=min_{i:m_i>0} A_i/m_i

is finite and strictly positive. The real coefficients a_j cause no problem: pi* is real-linear, and the support remains finite. The crepant boundary for (S,tB) on Y is

    Gamma_t=sum_i (t m_i-k_i)E_i.

At t=c, every coefficient is at most 1, including coefficients at m_i=0, where positivity of A_i gives -k_i<1. An SNC real subboundary on a smooth surface is sub-lc. This remains true when some coefficients are negative: blowing up a point on q<=2 boundary components produces exceptional coefficient sum_{ell=1}^q gamma_ell-1<=1. A point away from the boundary has coefficient -1. The total boundary remains SNC after any point blowup. Every prime divisor over a smooth surface appears after a finite sequence of point blowups, or is a divisor already on that surface, so this verifies all further valuations.

Consequently

    A_S(F)-c ord_F(B)>=0

for every prime divisor F over S. A divisor E_i attaining the minimum has equality, and violates log canonicity for every t>c. Therefore c=lct(S;B), the endpoint pair is log canonical, and

    sup_F ord_F(B)/A_S(F)=max_{i:m_i>0} m_i/A_i=1/c.

Applying the same endpoint argument separately to D_j gives ord_F(D_j)<=A_S(F)/c_j. Finite linearity of the integrals then gives K0. No exchange of infinitely many summands or unproved interchange of limiting valuations is used. Nonnegative a_j are essential to the displayed summation inequality. The separately stated signed-weight variant is valid as an upper bound because w ord_F(N|_S)<=max(w,0)ord_F(N|_S) pointwise.

## 2. Global and local domains

The valuation must be a prime divisor over S. A prime divisor over X need not even induce a divisorial valuation of the different function field C(S), so the unrepaired ambient quantifier cannot be retained.

For a fixed point P, the local threshold is computed from the same resolution using only E_i with P in pi(E_i) and m_i>0. The images are closed, and the finitely many images not containing P can be removed from S, giving an open neighborhood of P. The endpoint argument on this neighborhood applies to each F with P in c_S(F): any open set containing P contains the generic point of the irreducible center c_S(F). The center may be a curve; it need not equal P. The frozen text's local restriction is correct.

If P is outside Supp(D_j), a neighborhood of P misses D_j. For all admitted centers ord_F(D_j)=0; set 1/c_{j,P}=0 because c_{j,P}=infinity. This case is handled separately: there is no log pair with boundary infinity*D_j to evaluate. If P is in Supp(D_j), a component containing P imposes a finite bound, and the finite-resolution minimum is positive. Thus infinite local thresholds create no missing term or undefined product in the actual estimate.

Explicit falsification of an unrestricted local version: on S=A^2, let D=m(x=0), m>=1, and P=(1,0). Then lct_P(S;D)=infinity, but for F=(x=0) one has A_S(F)=1 and ord_F(D)=m. The local constant 0 fails for this F because its center does not contain P. BOUND.md:46 already forbids that misuse.

## 3. Cartier restriction and zero divisors

If X is smooth and E_j is a prime divisor on X, then E_j is Cartier. If S is normal integral and E_j!=S, S is not contained in E_j. A local equation for E_j restricts to a nonzero element of the local domain O_{S,P}; it is therefore a nonzerodivisor. The restricted section defines an effective Cartier divisor on S, possibly the zero divisor if E_j is disjoint from S. Smoothness or factoriality of S is unnecessary. The restriction may be nonreduced or reducible, and its multiplicities must be retained.

If E_j=S, its defining section restricts to zero and does not define the required effective Cartier divisor. The hypothesis E_j!=S is essential. The claim that S is absent from the negative part is assigned to the separate finiteness family; the LCT argument establishes the consequence once that claim holds.

Zero D_j have zero valuation order for every F. Discarding them before using a finite threshold is valid. If all a_j for nonzero D_j vanish, B=0, I(F)=0, and the least nonnegative K is 0. Choosing 1+K0 when a strictly positive K is requested is valid. Empty families, tau=0, and weights vanishing almost everywhere fall under this same case.

## 4. Exact examples with independently checkable resolution data

### Transverse curves: K0 can exceed Kopt by a factor two

On A^2 take D1=(x=0), D2=(y=0), tau=1, w=1, f1(u)=u, f2(u)=1-u. Both global thresholds equal 1 and a1=a2=1/2. The boundary B=(D1+D2)/2 is already SNC. Its threshold is 2, attained by each component, so K0=1 and Kopt=1/2. The origin blowup has A=2, ord(B)=1 and gives the same ratio 1/2. This explicitly checks the finite integral identity as well as a strict K0>Kopt.

### Tangent smooth curves: Kopt also sees interactions between components

On A^2 take D1=(y=0), D2=(y-x^2=0), and a1=a2=1. Each D_j is smooth and has threshold 1, so K0=2. Blow up the origin, giving E1 with A_S(E1)=2 and ord_{E1}(D1+D2)=2. In the chart y=xv, the strict transforms are v=0 and v-x=0, while E1 is x=0. These are three distinct lines through Q=(0,0). Blow up Q, giving E2 with A_S(E2)=3 and order 4. Their strict transforms then meet E2 at three distinct points, giving SNC support. The full finite data are

| Divisor | A_S | ord(D1+D2) | A_S/ord |
|---|---:|---:|---:|
| D1 or D2 strict transform | 1 | 1 | 1 |
| E1 strict transform | 2 | 2 | 1 |
| E2 | 3 | 4 | 3/4 |

Thus lct(S;D1+D2)=3/4 and Kopt=4/3. At t=3/4, the corresponding log discrepancies are 1/4, 1/4, 1/2, 0, respectively. This example rules out replacing the threshold of B by an unsupported maximum of the individual contributions.

### Du Val surface and a nonreduced Cartier divisor

Take S=(xy=z^2) in A^3, an A1 Du Val surface, and D=(x=0). On the prime line L=(x=z=0), y is generically invertible and x=z^2/y, so D=2L. Blow up the vertex. The exceptional conic E has A_S(E)=1 by adjunction (ambient discrepancy 2 minus hypersurface multiplicity 2 equals 0). In the chart x=yX, z=yZ, the strict surface is X=Z^2; hence x=yZ^2. Thus pi*D=E+2L', and E and L' meet transversally. The two finite ratios are 1/1 and 1/2, so lct(S;D)=1/2. For B=aD, a>0, Kopt=2a. Ignoring the multiplicity or ignoring strict transforms would give a wrong threshold; the frozen statement does neither.

### klt is a necessary assumption

Take the normal cubic cone S=(x^3+y^3+z^3=0) in A^3. Blowing up the vertex resolves it with smooth elliptic exceptional curve E. Adjunction gives ordinary discrepancy 2-3=-1, so A_S(E)=0; the resolution boundary E is SNC and (S,0) is lc but not klt. The Cartier section D=(x=0) has ord_E(D)=1. No finite K satisfies ord_E(D)<=K A_S(E). This falsifies the tempting weakening from klt to merely lc and supports restoration of the source's Du Val hypothesis.

The exact rational values in the first three examples were independently checked with Fraction arithmetic: thresholds `(2,3/4,1/2)`, reciprocals `(1/2,4/3,2)`, and all endpoint differences nonnegative. The geometric resolution derivations above, rather than those arithmetic checks alone, certify the examples.

## 5. Actionable repair and boundaries

**Minor terminology defect — BOUND.md:56.** The phrase “all discrepancies of the klt surface are positive” is false if discrepancy has its customary meaning a(E;S)=A_S(E)-1. A Du Val crepant exceptional divisor already has ordinary discrepancy 0; more general klt surfaces may have negative ordinary discrepancies. Replace it with:

> The required endpoint log canonicity, as well as c_j>0, follows on a log resolution of (S,D_j), including the strict transforms: the relevant log discrepancies A_S(E) are positive, and c_j is the minimum of the finitely many ratios A_S(E)/ord_E(D_j) with positive denominator.

This exact repair strengthens the explanation without changing the theorem, constant, or proof mechanism. The quoted replacement is proposed text, not a modification of the frozen candidate.

**Optional scope precision — BOUND.md:31.** The Fano context already makes S an algebraic surface of finite type. If the abstract paragraph is meant to stand alone, write “normal finite-type complex algebraic klt surface.” Arbitrary noncompact analytic surfaces can have analytic Cartier divisors with unbounded multiplicities and global threshold zero. The independent endpoint subaudit records an explicit entire-function construction. This is not a defect in the algebraic source setting.

**Boundaries of this pass:** the proof presupposes a finite actual divisor decomposition and finite integrals; it does not itself prove these for the threefold. The weight must be nonnegative for the equality-based optimal-constant construction. The signed-weight upper bound uses its own positive-part coefficients. There is no universal constant independent of input data, no asserted rationality of the threshold for real B, and no K-stability conclusion. Homogeneity is consistent: lct(S;tB)=lct(S;B)/t and Kopt(tB)=tKopt(B) for t>0.

## Primary-source cross-checks

- [Cheltsov–Fujita–Kishimoto–Okada, published Appendix B, Lemma 27](https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/kstable-divisors-in-mathbb-p1times-mathbb-p1times-mathbb-p2-of-degree-112/999FB6032A21485AD71CF230CC802E6C): the first inequality uses local thresholds and P in C_S(F). Only that domain and short threshold proof were used here; bibliographic precedence is assessed separately.
- [Fujino, Introduction to the log minimal model program, Sections 1.6.1–1.6.2](https://www.math.kyoto-u.ac.jp/~fujino/MMP21.pdf): ordinary discrepancy convention and klt/lc definitions for real pairs.
- [Kollár, Families of varieties of general type, Chapter 11](https://web.math.princeton.edu/~kollar/FromMyHomePage/modbook-final.pdf): real pairs, ordinary discrepancy, and log discrepancy as 1+a. No external contact or outreach was prepared or performed.
- Independent endpoint challenge: `endpoint_subaudit/ENDPOINT_AUDIT.md` records a separate reconstruction and the analytic boundary counterexample, completed before seeing this family's verdict.
