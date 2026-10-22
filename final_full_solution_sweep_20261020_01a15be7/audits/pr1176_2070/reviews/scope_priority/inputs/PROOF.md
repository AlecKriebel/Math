# A parity obstruction to the variable-base part of Erdős problem 354

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the variable-base counterexample, with no external human peer review, journal acceptance, or formal proof-assistant certification claimed. The complete substantive mathematical proof and audit are retained. No mathematical correction was required. The fixed-base-2 irrational-ratio question remains unresolved by this work. The exact quartic family and positive-multiplier mechanism are prior work of Dubickas (2006); no novelty of the application is claimed. Executable programs, raw datasets, detailed execution receipts, full computational certificates, and copied source documents are omitted. This is not an executable reproduction package. Edition preparation performed byte-integrity and publication-structure checks, with no new mathematical test execution or scholarly-source retrieval or inspection.

## Status and exact scope

**Result: the universal variable-base assertion is false.** The base-2 assertion is not resolved here.

The formulation inspected in Graham (1971), printed page 36, question 12, and Erdős–Graham (1980), printed page 58, asks whether, for positive real numbers alpha and beta with irrational alpha/beta, the indexed sequence

    floor(alpha), floor(beta), floor(gamma alpha), floor(gamma beta), ...

is complete, first for gamma=2 and then with 1<gamma<2. Completeness means representation of every sufficiently large integer as a finite sum of distinct **positions**. Exponents start at zero. Coincident values in different positions are retained.

We give explicit positive alpha,beta and gamma in (1,2) with irrational alpha/beta for which every term is even. Thus every odd integer is omitted, regardless of the repetitions. This does not concern the base-2 rational-power-of-two-ratio exclusions.

The construction is an explicit quantitative application of the published mechanism in Artūras Dubickas, *On the limit points of the fractional parts of powers of Pisot numbers* (2006), Theorem 4 and its proof on printed page 156, and *Even and odd integral parts of powers of a real number* (2006), Theorem 1(iv) and its proof on printed page 334. The Glasgow paper also explicitly identifies the family X^(d-1)-X^(d-2)-...-X-1 for d>=5 on printed page 332, which includes the exact quartic here at d=5. The underlying mechanism and this base family are prior mathematics; no priority claim is made for their consequence for the variable-base question. A self-contained proof, including an explicit shift, follows.

## The explicit counterexample

Let

    P(X) = X^4 - X^3 - X^2 - X - 1,

and let gamma be its unique positive root. Define

    c = 1 / ((gamma-1) P'(gamma)),
    alpha = 2 c gamma^20,
    beta = gamma alpha.

Then gamma lies in (1.92,1.93), c>0, alpha>0, beta>0, and alpha/beta=1/gamma is irrational. For every integer n>=0,

    floor(alpha gamma^n) = 2 k_(20+n),
    floor(beta  gamma^n) = 2 k_(21+n),

where the integer sequence k is defined by

    k_0=k_1=k_2=k_3=0,
    k_(m+4) = k_(m+3)+k_(m+2)+k_(m+1)+k_m+1  (m>=0).

Consequently the entire indexed multiset is contained in 2Z, and it is not complete. The relation beta=gamma alpha is allowed by the original hypothesis: gamma is irrational, so alpha/beta is irrational. At base 2 the analogous shift would have rational ratio and would be inadmissible; that exclusion does not carry over to an irrational base.

## 1. Root locations, simplicity, and irrationality

Descartes' rule of signs gives at most one positive root of P, counting multiplicity. Exact substitutions give

    P(48/25) = -37009/390625 < 0,
    P(193/100) = 3092301/100000000 > 0.

Hence the positive root gamma is simple and

    48/25 < gamma < 193/100.

Write Q(t)=P(-t)=t^4+t^3-t^2+t-1. For t>=0,

    Q'(t)=4t^3+3(t-1/3)^2+2/3 > 0.

Moreover

    Q(77/100) = -1483659/100000000 < 0,
    Q(39/50) = 101891/6250000 > 0.

Thus P has precisely one negative real root, -u, with 77/100<u<39/50. It is simple. The two remaining roots are a distinct nonreal conjugate pair z, conjugate(z). Put z=x+iy with y>0. Vieta's identities give

    x = (1-gamma+u)/2,           |z|^2 = 1/(gamma u).

Therefore

    -2/25 < x < -7/100,
    5000/7527 < |z|^2 < 2500/3696 < 25/36,
    y^2 = |z|^2-x^2 > 5000/7527-4/625 > 16/25.

In particular |z|<5/6 and y>4/5; also u<39/50<5/6. All roots other than gamma have modulus less than 5/6.

The rational root theorem shows that gamma is irrational: a rational root of the monic integer polynomial P would be an integer, whereas 1<gamma<2. Since P is monic with these four distinct roots,

    P'(gamma)=(gamma+u)|gamma-z|^2>0.

This proves the stated positivity of c, alpha, and beta, and the irrationality of alpha/beta.

## 2. Exact trace identity with an integer recurrence

For each root r of P set

    c_r = 1 / ((r-1) P'(r)),
    S_m = sum_(P(r)=0) c_r r^m  (m>=0).

For m=0,1,2,3, polynomial interpolation, or partial fractions, gives the identity

    X^m/P(X) = sum_(P(r)=0) r^m / (P'(r)(X-r)).

For clarity, multiplying by P(X) proves it: both sides are polynomials of degree at most 3 and take the same value at each of four distinct roots. Substituting X=1 and using P(1)=-3 shows

    S_0=S_1=S_2=S_3=1/3.

Each root satisfies r^4=r^3+r^2+r+1. Consequently

    S_(m+4)=S_(m+3)+S_(m+2)+S_(m+1)+S_m.

It follows by induction that

    S_m=k_m+1/3,

with exactly the nonnegative integer sequence k displayed above. No assertion that S_m itself is an integer is being made: its constant residue 1/3 is essential.

## 3. Uniform all-future error bound

The coefficient at the positive root is c_gamma=c. All three other coefficients have absolute value less than 1.

For r=-u, the product formula for the derivative gives

    |(r-1)P'(r)|
      = (1+u)(gamma+u)|r-z|^2
      > 1 * 2 * (4/5)^2 = 32/25 > 1.

For r=z (and identically for its conjugate),

    |(z-1)P'(z)|
      = |z-1| |z-gamma| |z+u| |z-conjugate(z)|
      > 1 * 1 * (4/5) * (8/5) = 32/25 > 1.

Here x<0 gives the first two strict lower bounds, and the imaginary parts give the last two. Thus, if

    E_m = c_(-u)(-u)^m + c_z z^m + c_conjugate(z) conjugate(z)^m,

then E_m is real and

    |E_m| < 3(5/6)^m.

For all m>=20,

    3(5/6)^m <= 3(5/6)^20 < 1/6.

The last inequality is the exact integer comparison 18*5^20<6^20. Combining this with the trace identity yields

    c gamma^m = k_m + 1/3 - E_m,
    1/6 < c gamma^m-k_m < 1/2.

Hence

    2 k_m + 1/3 < 2 c gamma^m < 2 k_m + 1,

so floor(2 c gamma^m)=2 k_m for **every** m>=20. Taking m=20+n and m=21+n proves both asserted floor formulas from exponent zero onward. There is no unchecked finite prefix and no exchange of an asymptotic assertion with an all-n assertion.

## 4. Independent-checkable examples

The following decimal values are orientation only, not used in the proof:

    gamma approximately 1.92756197548292530426,
    c     approximately 0.08525335178624324299,
    alpha approximately 85488.65181866524872,
    beta  approximately 164784.67458095836188.

The first six **pairs of indexed terms** are

    (85488, 164784),
    (164784, 317632),
    (317632, 612256),
    (612256, 1180162),
    (1180162, 2274836),
    (2274836, 4384888).

For example, 164784 at beta's exponent zero and 164784 at alpha's exponent one are different usable positions. Both are even. An arbitrary finite sum of the indexed terms is still even, so all positive odd integers, however large, are omitted.

The original candidate's verifier, omitted from this edition, used only Python's standard library and exact rational/integer arithmetic. It isolated gamma by rational bisection, enclosed 2 gamma^m/((gamma-1)P'(gamma)) by rational interval bounds, and checked 128 consecutive floor values against the recurrence. It also checked every rational inequality displayed in the all-future proof. These are historical finite-check claims, not executable reproduction from this edition; the all-future conclusion rests on Sections 1–3, not on numerical sampling.

## 5. Residual question and attribution limits

- The original assertion with gamma=2 and alpha/beta irrational is **unresolved by this work**.
- A single allowed gamma refutes the universal extension to all gamma in (1,2); it does not classify the good or bad bases in that interval.
- The reported prior individual-pair result (10 sqrt(2),10 sqrt(3)) for base 2 is not used, re-certified, or presented as new.
- No copied source document, source text, private coordination record, or dataset is needed to state or check this proof.
- Dubickas's positive-parameter fractional-part construction is explicitly credited. The source search here does not establish that the application to Erdős problem 354 has never appeared elsewhere.

## References

1. R. L. Graham, *On sums of integers taken from a fixed sequence*, Proceedings of the Washington State University Conference on Number Theory (1971), 22–40, question 12 on printed page 36 (PDF page 15). https://mathweb.ucsd.edu/~ronspubs/71_08_integer_sums.pdf
2. P. Erdős and R. L. Graham, *Old and New Problems and Results in Combinatorial Number Theory*, Monographie 28, L'Enseignement Mathématique (1980), printed page 58. https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf
3. A. Dubickas, *On the limit points of the fractional parts of powers of Pisot numbers*, Archivum Mathematicum 42 (2006), 151–158, Theorem 4 and its proof, printed pages 154 and 156. https://dml.cz/handle/10338.dmlcz/107991
4. A. Dubickas, *Even and odd integral parts of powers of a real number*, Glasgow Mathematical Journal 48 (2006), 331–336, Theorem 1(iv), proof on printed page 334. https://doi.org/10.1017/S0017089506003090
