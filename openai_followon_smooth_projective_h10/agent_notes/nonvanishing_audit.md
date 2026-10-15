# Independent analytic audit

Checkpoint: 2026-10-07 05:46 UTC. Scoped audit completion: 100% of the displayed moment calculation and height comparison reconstructed; this does not assign a completion percentage to the whole H10(Q) proof. No source or Git mutation, no external communication, no retained downloaded PDF copies.

## Exact scope and verdict

Read and reconstructed all 425 lines of `build/sections/nonvanishing.tex`, and `pointwise.tex` 427–470, using the pinned upstream directory named in `two_converse_coefficients.md`. The hashes recorded there remain the source identity. The claims being tested were the absolute exponents in the fixed-progression moment, an absolute almost-prime bound with arbitrary fixed unit classes and excluded primes, and the height ratio with fixed genus partner h_* and separately varying companion k'(h).

No mathematical counterexample or unsupported central analytic claim remains in this scope. The reconstruction below supplies the calculations that mere theorem names would not supply. The precise source limitation is that Friedlander–Iwaniec's book Theorem 11.13 was not directly extracted; the necessary lower bound was checked instead against Richert's primary lectures, Theorems 11.12–11.13 and conditions (9.16), (11.3), (11.62), and against the displayed dimension-one sieve formulation in a primary research paper. This replacement proves the needed sieve conclusion with an absolute level exponent. It is a bibliographic substitution, not an extra mathematical hypothesis. Standard modularity, Ramanujan bounds, quadratic large sieve, functional equations, and Gross–Zagier are used in their established forms; they are not newly reproved here.

## 1. Approximate functional equation and square-divisor tail

Put Q_t=√N_A t/(2π), and Λ_t(s)=Q_t^s Γ(s+1/2)L(s,f⊗χ_{σt}). For j=0 in sign +1 and j=1 in sign −1, apply the functional equation to the integral of e^{z²}Λ_t(1/2+z)/z^{j+1}. The negative-line integral is the negative of the positive-line integral in precisely these two sign/parity combinations. Its residue, divided by Q_t^{1/2}, is L(1/2) for j=0 and L'(1/2) for j=1: Γ'(1)+log Q_t multiplies L(1/2), which is zero in the latter case. Thus the factor 2 and kernel Γ(1+z)/z^{j+1} in lines 85–98 are correct.

Heath–Brown's Theorem 1 bounds the quadratic character polynomial when both Jacobi variables are odd squarefree. His Corollary 1 permits all primitive real characters of bounded conductor and squarefree coefficient indices, including their even part. These hypotheses match χ_{σt}; no sieve assertion for arbitrary unsquarefree coefficient indices is silently being used.

For an ordinary polynomial with coefficients λ(n)/√n write n=u r², u squarefree. For fixed r the character contribution is χ_t(u)1_{(t,r)=1}. Apply the squarefree-index inequality only to the nonnegative sum of squared absolute values restricted to (t,r)=1, then enlarge the character set. Since |λ(u r²)|≤d(u r²), its coefficient squared norm is at most (ZU)^ε/r² after absorbing divisor and logarithmic factors. Minkowski gives

    ||Σ_{n≤U} λ(n)χ_t(n)/√n||_2
      ≪ (ZU)^ε Σ_{r≤√U} √(Z+U/r²)/r
      ≪ (ZU)^{2ε}(√Z+√U).

The main AFE at s=1/2+δ has n^{-δ}; partial summation cannot worsen this bound. The dual polynomial has n^δ, length U≪_f T(1+|τ|)^C for t∼T, and multiplier T^{-2δ}; hence its extra factor is ≤T^{-δ}(1+|τ|)^{Cδ}. Mellin separation of smooth t-weights and the gamma decay then yield the displayed second moment with T^{1+ρ}. All polynomial exponents in τ can be chosen independent of the level; √N_A is inside the curve-dependent constant. This is not a claim that those constants are uniform in A.

For nonsquarefree n=t v² in the fixed reduced progression, t is still prime to 2N_A, σt is fundamental, and χ_{σn}(u)=χ_{σt}(u)1_{(u,v)=1}. The Mellin integrand is therefore exactly the primitive twist L-function with the Euler factors at p|v removed. At Re z=δ_M>0 these removed factors are bounded by C^{ω(v)}≪_ε v^ε. A omitted square divisor d>Y divides v; its multiplicity is at most d(v), with no missing large-square contribution. On n∼X, (Q_A t v²)^{δ_M}≪_f X^{δ_M}. Cauchy applied to the second moment gives

    Σ_{t≤2X/v²}* |L(1/2+δ_M+iτ)|
       ≪ (X/v²)^{1+ρ'}(1+|τ|)^C.

Choose δ_M, ρ', ε small relative to ρ. Summation over v>Y is bounded by X^{1+ρ}Σv^{-2}≪X^{1+ρ}/Y. The imposed b|n condition can be discarded after absolute values. Thus the tail is uniform in b, stronger than needed. The z^{-2} derivative kernel costs a constant depending on δ_M, not an X-power.

## 2. Poisson identity and positive main term

For J=[d²,b], only (J,H)=1 survives. Writing n=Jm fixes m≡c_J=aJ^{-1} mod H. The CRT representatives x=c_J q q̄+H y H̄ give

    Σ_{x mod Hq, x≡c_J(H)} (x/q)e(νx/Hq)
      =e(νc_J q̄/H)(H/q)G_ν(q).

Multiplication by (σJ/q), the scale X/J, and the u=u_1q split produce exactly lines 187–205, including the factor (σJH/q). If q and J share a prime the Jacobi symbol is zero. No coprimality factor was omitted.

G_0(q) vanishes unless q is square; for q=p^{2r} it equals φ(p^{2r}). Hence the stated H_p(z) is the actual local factor. For x=p^{-1-2z} and D_p(x)=(1−α_p²x)(1−α_p^{-2}x),

    H_p(z) = [D_p(x)/p+(1−1/p)(1+x)]/D_p(x),
    C_p(z) := H_p(z)(1−x)D_p(x)
             =1+O(x/p+x²),

with an absolute implied constant. On Re z≥−1/16 this correction product converges absolutely, since |x|≤p^{-7/8}. Write F_J using the correction product over p∤HJ and the inverse symmetric-square Euler polynomials at p|J. This expression never divides by H_p(z), so possible zeros of that factor create no pole. Each omitted inverse degree-three polynomial is bounded by 8, giving a bound J³ sufficient for this contour shift.

Gelbart–Jacquet Theorem 9.3 explicitly excludes a nontrivial quadratic self-twist. Its Remark 9.9 covers that case by a Hecke L-function times the nontrivial quadratic L-function. For a weight-two CM form, the first Hecke character has nonzero infinity type and the second quadratic character is nontrivial. The untwisted symmetric-square L-function here is consequently entire also in the CM case; the remark's warning that some *twists* have poles does not supply a pole at our untwisted argument. Functional-equation strip bounds apply in both cases. The contour passes only z=0, producing an error O(J³X^{15/16}) after harmless fixed factors.

At z=0, E_p=Σ_{r≥0}λ(p^{2r})p^{-r}=(1+1/p)/|1−α_p²/p|²>0 and H_p=1/p+(1−1/p)E_p>1/p. The fixed H-supported Euler factors are positive, as is L(1,sym²f) by the positive Rankin–Selberg residue. The square-divisor sum is locally H_p−p^{-2} if p∤b, and p^{-1}−p^{-2} if p|b. Thus

    β_p=(p−1)/(p²H_p−1)=1/(1+pE_p),

and 0<β_p<1, β_p=1/p+O(p^{-2}) with absolute error, by |λ(p)|≤2. This also verifies that no old main factor depends on b. The double pole for j=1 has leading residue cX log X with c>0. Residue differentiation costs log d, absorbed by d^ε in the convergent d^{-2+ε} tail.

## 3. Nonzero frequencies and absolute exponents

For odd q, ε_q^{-1}G_ν(q) is multiplicative: the CRT cross symbols cancel ε_{q_1q_2}/(ε_{q_1}ε_{q_2}). Direct lift summation at p^r gives exactly the four cases in lines 285–293, including the even-r Ramanujan sum −p^{r−1} when r=v_p(ν)+1. Consequently the p∤2HJν local factor in D(s) is 1+λ(p)ξ(p)p^{-s}. Multiplication by the inverse GL₂ Euler polynomial leaves

    1+(1−λ(p)²)ξ(p)²p^{-2s}+λ(p)ξ(p)³p^{-3s},

which has an absolutely convergent product on Re s>1/2. At bad primes p|Jν, the local polynomial on Re s≥3/4 is at most Σ(r+1)p^{-r/4}; the inverse degree-two factor is bounded independently of the valuation of ν. Their product is <64 per prime, so ≤(2J|ν|)^6 suffices. Fixed H primes affect only the constant. The primitive character conductor is ≤4HJ|ν|. The degree-two functional equation and absolute convergence to the right of 1 give a conductor-polynomial bound with an absolute exponent. Taking the deliberately coarse exponent C=8 in (J|ν|)^C is sufficient. These twists are cuspidal even when f has CM, and their L-functions are entire.

The Mellin sum is indeed Σγ(q)q^{-1}w_T(q/T), not a different power of q; on shifting 1+s from Re 2 to Re 3/4 its factor is T^{-1/4}. On a fixed dyadic y interval, derivatives in y are linear combinations of z∂z and R∂R. The displayed weight estimate thus supplies the required Mellin seminorms uniformly in u_1,T,J,ν, apart from log X, and the latter is absorbed in X^ρ.

The truncation's large derivative orders need not increase the polynomial exponent in J. A useful check eliminating a potential circular choice is

    Σ_{ν≠0}(1+|ν|X/(HJq))^{-K}≪HJq/X.

Using |G_ν(q)|≤q, the full absolute majorant is then ≪X^{3/2+ε}, with the J factor canceled. Each discarded region has either u_1q/X>X^ρ or |ν|X/(HJq)>c_H X^ρ. Splitting the decay exponent in half makes its error ≪X^{3/2+ε−Kρ}; K may be chosen arbitrarily large without a growing J-power. Thus the same fixed polynomial exponent is valid when ρ is decreased at the final truncation choice.

After the shift, ν≤C_H JX^{2ρ} and T≥c_H X^{1−ρ}/J. The contribution is at most

    (X/J) J^C(JX^{2ρ})^{C+1}(X^{1−ρ}/J)^{-1/4}
        ≪J^{2C+1/4}X^{3/4+(2C+9/4)ρ},

up to logarithms. The H-supported u_1 sum converges at exponent 1/2. If the displayed lower bound for T is below 1, replacing it by 1 only improves this upper bound. One can use B_3=18 and bound the X exponent by 3/4+21ρ; no exponent depends on the curve, H, or b.

As a conservative explicit choice, take B_4=18, κ=1/16, δ=1/4096, ρ=1/32768 and Y=X^δ. Then the contour error exponent is at most 15/16+37δ<1, while the square-tail exponent is 1+ρ−δ<1. Thus B=18 and η=1/16384 are sufficient coarse constants. The purpose of these unoptimized numbers is to demonstrate a noncircular absolute choice, not to optimize A_0.

## 4. Lower sieve and bounded-factor witnesses

The weights a_n in the positive-sign case are nonnegative by Waldspurger in the exact primitive, prime-to-2N family; the same applicability is explicitly stated in Radziwiłł–Soundararajan, §1. With mass M=cX, g(p)=β_p for p∤H and zero otherwise, the lemma gives A_b=M g(b)+r_b for every squarefree sieve divisor, |r_b|≪b^B X^{1−η}.

For a direct check against the accessible primary lower-sieve theorem, use Richert's notation ω(p)=pβ_p. Condition Ω_1 holds because sup_p β_p<1 (the finitely many small primes are harmless). Condition Ω_2(1,L) follows from

    Σ_{w≤p<z} β_p log p = log(z/w)+O_{f,H}(1),

using β_p=1/p+O(p^{-2}); omitted H primes contribute a fixed finite constant. Richert's remainder condition has the extra weight 3^{ω(b)}. Since 3^{ω(b)}≪_ε b^ε, choose an absolute θ<η/(2(B+2)) and α=θ in his asymptotic theorem (rescaling X to M only changes constants). Then even the weighted remainder through X^θ is a power smaller than X, hence satisfies (11.62) with any prescribed fixed logarithmic saving for sufficiently large X. A nonnegative real weighted sequence is covered by the same sieve inequalities, by rational approximation or direct linearity; integrality of a_n is unnecessary.

Choose s=3 and z=X^{θ/3}. The primary formula (11.74) gives f(3)=2e^γ log2/3>0, while W(z)∼constant/log z. The lower bound is therefore positive in every sufficiently large dyadic interval. Since n<2X and every p|n is ≥z,

    ω(n)≤log(2X)/log z<6/θ

eventually. An integer A_0>6/θ is absolute. Fixed support primes are already excluded and z tends to infinity, so any additional fixed bound on all prime factors is satisfied. Arbitrary nonempty unit squareclasses are encoded by a reduced class mod a sufficiently enlarged fixed H; that affects the threshold and constants, not θ or A_0. In the derivative case the nonzero cX log X first moment alone supplies a witness. No positivity of derivatives is needed.

## 5. Gross–Zagier height ratio and projections

Cai–Shu–Tian Theorem 1.1, published pp. 2524–2525, requires a primitive ring-class character of conductor c coprime to N, level primes noninert (split when their level exponent is ≥2), and an extra character condition only at primes dividing (N,D). Its elliptic-curve formula is the **unaveraged** character sum and has denominator u² c√|D|, with factor 2^{-μ(N,D)} and the fixed modular degree. This matches the definitions in coefficients.tex 167–185 and ring-limits.tex 22–35.

For K=Q(√k), every p|h splits, (h,k)=1, and the norm-restriction of χ_h retains its ramified quadratic character on the units at either split place. Its exact ring conductor is |h|. For the genus field Q(√(hh_*)), h and h_* are coprime fundamental discriminants, and the character associated to adjoining √h_* is unramified, hence c=1. Both fields are split at every level prime; therefore (N,D)=1, μ=0, the character condition there is empty, and c is prime to N. The prescribed exclusions ensure u=1.

Artin induction of these two quadratic characters gives respectively χ_h⊕χ_{hk} and χ_h⊕χ_{h_*}; the Rankin L-functions are the stated products. If their factors have orders one and zero, the derivative is exactly L'(E^h,1) times the other central value. Solving the same fixed-parametrization CST formula for the heights gives the two factors |h|√|k| and √|hh_*| in lines 451–453. Their ratio is

    √|hk| L(E^{hk},1) / [√|h_*| L(E^{h_*},1)],

or L_*(hk)/L_*(h_*) when the same fixed imaginary-period convention is used. The genus partner is h_* throughout; it is not the new companion k'(h).

The twist identification preserves the canonical height. In E^h(K) the anti-invariant component has rank zero because E^{hk}(Q) has analytic rank zero; the free rank-one lattice is therefore the invariant rational twist line up to an index killed by 2. For the biquadratic genus sum, the other χ_{h_*} component also has rank zero. The maps 1±τ have composite multiplication by 2 on their relevant eigenspaces, so the lattice losses are bounded powers of 2, independently of ω(h). All torsion is on a fixed curve over fields of degree at most four and can be killed by a fixed integer. Comparing squared rank-one indices cancels the common regulator and yields precisely

    2j_h(k)−2j(P_h)=v_2(L_*(hk))+O(1).

This error is uniform for fixed k, and for the bounded-factor varying companions in the manuscript. No class-number divisor or ∏_{p|h}(p−1) appears: introducing one would incorrectly average the sums. This check does not rely on BSD or on the odd coefficient normalization.

## Primary source record

- Heath–Brown, author-deposited primary PDF: https://ora.ox.ac.uk/objects/uuid:b188b365-d8d1-4267-8548-49f01e6cb6a7/files/m6af40476f1b860392271a2d8ecae593b ; Theorem 1 and Corollary 1 extracted in memory, 263834 bytes.
- Gelbart–Jacquet: https://www.numdam.org/article/ASENS_1978_4_11_4_471_0.pdf ; Theorem 9.3 and Remark 9.9 read directly, pp. 534 and 541.
- Radziwiłł–Soundararajan: https://arxiv.org/pdf/1403.7067 ; §1 primitive family/positivity, Proposition 2 and §10 read. Its original modulus is fixed by E; the enlargement here was checked directly by CRT, rather than attributed to that proposition.
- Iwaniec: https://www.numdam.org/article/JTNB_1990__2_2_365_0.pdf ; §§2,4,6–8 read. Its initial root sign and specific quadratic progression are narrower than the manuscript's claim; the manuscript's derivative extension was reconstructed directly above.
- Richert: https://mathweb.tifr.res.in/Documents/Publications/Lectures/tifr55.pdf ; primary lectures pp. 109,134,145–149 and conditions/theorems specified above extracted in memory, 1300854 bytes. This is an independent sufficient replacement for the directly inaccessible FI book passage.
- Hoffstein–Luo: https://intlpress.com/api/bgcloud-front/resource/pdf/volume/1806607231397294082-1806607231397294082-ecf504fa497d5ea43300de9a771c613a.pdf ; theorem and §2 read directly, 148034 bytes. Its stated local conditions are χ_d(p)=1, not arbitrary prescribed classes; the broader statement here uses the reconstruction above.
- Cai–Shu–Tian: https://msp.org/ant/2014/8-10/ant-v8-n10-p05-p.pdf ; published Theorem 1.1 and surrounding definitions read directly.

The remaining task assigned after this audit is the separate `pw:split-mod8` local representation/module interface. Its initial reconstruction is affirmative, but its full level and coefficient check is recorded separately rather than silently incorporated into this analytic verdict. The H10(Q) dependency is still subject to the whole-proof audit led by the parent researcher.
