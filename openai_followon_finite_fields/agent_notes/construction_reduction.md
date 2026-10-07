# Prescribed-degree construction: independent reduction audit

Checkpoint: 2026-10-06 America/Los_Angeles. Mathematical completion of the **conditional construction reduction**: 95%; publication package: 0%. This percentage does not certify the upstream prime-factorization theorem. The construction mechanism has a proof below; the unconditional headline still depends on the independent audit of that theorem and its analytic inputs.

Authoring/review scope: this agent independently read the original problem, the local instruction file, the arithmetic/computation triage, and Shoup's author-hosted primary paper. No external individuals were contacted. The original upstream clone was not changed.

## Exact strongest claim

Assume an oracle `PF` that, on a dense polynomial of degree at most `t` over the promised prime field `F_p`, deterministically returns its complete irreducible factorization in bit time `T(t,B)`, where `B=ceil(log_2 p)` and `T` is polynomial in `t+B`. Then, given a monic irreducible `h` of degree `m>=1` over `F_p`, and a requested degree `d>=1`, there is a uniform deterministic algorithm that outputs a monic irreducible polynomial of degree `d` over `K=F_p[Z]/(h)`. Its bit time is polynomial in `m,d,B`, and hence in the supplied dense field representation and dense requested output size.

The primality of `p` and irreducibility of `h` are input promises, or must be verified separately. Irreducibility of `h` can be checked without factoring a large integer: compute `Z^(p^m)=Z mod h`, and for every prime `ell|m` check `gcd(h,Z^(p^(m/ell))-Z)=1`. Trial division of `m` costs polynomial in `m`; this is legitimate because `h` has dense length `Omega(mB)`. A primality certificate may instead accompany `p`, or a standard deterministic primality test may be used. No extension representation is inferred from its cardinality alone.

Degrees here are numeric degrees, not their binary encoding lengths. The output has `(d+1)m` prime-field coefficient slots, each encoded using `B` bits. In particular, the result does **not** assert polynomial time in `log d` while printing a dense degree-`d` polynomial.

This is a conditional consequence of an established reduction. It does not independently prove `PF`, does not provide an integer-factorization algorithm, and makes no practical-efficiency claim.

## Primary source and priority

Victor Shoup, *New algorithms for finding irreducible polynomials over finite fields*, Mathematics of Computation **54** (1990), 435–447, DOI `10.1090/S0025-5718-1990-0993933-0`; extended abstract appeared at FOCS 1988, pages 283–290. Primary author copy: <https://www.shoup.net/papers/detirred.pdf>.

Theorem 3.1 gives the deterministic polynomial-time reduction from prime-field construction to prime-field polynomial factoring. Theorem 4.1 and its proof already extend the construction implication to a supplied nonprime field representation. The construction implication should be attributed to Shoup, not advertised as new machinery. The author-hosted copy is dated January 31, 1989; public priority should use the FOCS publication evidence rather than treating this manuscript date as a verified first disclosure.

Downloaded primary PDF SHA-256: `00590fb8f0717338530b067626428781991edb840fb74c37cf846f07f50e0644`. Its embedded character encoding prevents normal text extraction. Pages 3–10 were rendered at 180 dpi and OCRed for reading. Mathematical expressions in the notes below are independently derived rather than trusting OCR formulas. The saved source PDF and rendered pages are research inputs, **not proposed publication attachments**: redistribution rights were not established.

## A simple lift from prime fields to an arbitrary explicit base

Set `N=md`. Construct a monic irreducible `H in F_p[X]` of degree `N` using the prime-field reduction below. Regard `H` as an element of `K[X]`, with its coefficients embedded as constants, and run the validated extension-field factoring reduction. Select the lexicographically first irreducible factor.

Proof of the degree assertion: a root of `H` has a Frobenius-`p` orbit of size `N`. Frobenius-`p^m` acts on that orbit by adding `m` modulo `N`, so every orbit has size `N/gcd(N,m)=d`, and there are exactly `m` orbits. These are precisely the irreducible factors over `K`. As finite fields are perfect, `H` is separable. Thus every returned factor has degree `d` and multiplicity one. No field isomorphism algorithm, root embedding, or primitive element is required.

For `d=1`, simply return `X` (and the degree-one extension is the original field). For `m=1`, one may directly use the prime-field construction, avoiding a redundant factorization.

## Prime-field construction, with every oracle use exposed

Factor the requested numeric degree `N` by trial division. For each prime-power divisor `D=r^e` of `N`, construct a degree-`D` field and an explicit element that generates it over `F_p`. Combine the resulting fields using coprime degrees. All factor selection uses a fixed lexicographic rule.

### Odd `r != p`: bounded-degree nonresidues, then trace

Compute `s=ord_r(p)` by repeated multiplication modulo `r`, with at most `r-1` multiplications; there is no need to factor `r-1`. Let `k=v_r(p^s-1)`, calculated by forming the integer `p^s-1` and repeatedly dividing by the known prime `r`. Its bit length is at most `sB+1`; no factorization of that integer is needed.

1. Ask `PF` to factor `Phi_r(X)=1+X+...+X^(r-1)` and select a factor `f_1` of degree `s`.
2. For `j=2,...,k`, ask `PF` to factor `f_(j-1)(X^r)` and select a factor `f_j`.
3. Put `K_r=F_p[A]/(f_k)` and let `a` be the image of `A`.

Each root of `f_j` has exact order `r^j`. Since `r^j|p^s-1`, its Frobenius orbit size divides `s`; reduction modulo `r` shows that this orbit size is also a multiple of `s`. Therefore every chosen factor has degree exactly `s`. The substituted polynomial is separable: its nonzero roots are mapped by `X -> X^r`, whose derivative is nonzero since `r != p`, to roots of the separable `f_(j-1)`. The last element `a` has order `r^k`; if it were an `r`th power in `K_r`, an `r`th root would have order `r^(k+1)`, impossible in a group of order `p^s-1`. Thus `a` is an `r`th nonresidue.

The binomial irreducibility criterion says that `X^D-a` is irreducible over `K_r` when `a` is not an `r`th power; its extra `4|D` exception is absent for odd `r`. This is the classical binomial criterion used as Lemma 2.2 in Shoup's paper (attributed there to Lang, *Algebra*, 1984, p. 331, Theorem 9.1). Consequently

`L=K_r[B]/(B^D-a)`

is a field of dimension `sD` over `F_p`, with `b` the image of `B`. Because `a=b^D` generates `K_r`, the element `b` generates `L` over `F_p`.

Define

`gamma=sum_(i=0)^(s-1) b^(p^(D*i))`.

This is the trace from `L` to its unique degree-`D` subfield `E`, so `gamma in E`. We prove that `gamma` generates `E`. If it lay in a proper subfield, it would lie in `F_(p^(D/r))`, hence in `K_r(b^r)`. Over this last field, `b` has degree `r`. Write `p^(D*i)=r*u_i+v_i`, with `1<=v_i<=r-1`. Since `s|r-1` and `D=r^e`, one has `D=1 mod s`; therefore the `v_i` are the `s` distinct residues `p^i mod r`. The identity

`sum_i (b^r)^u_i * b^v_i - gamma = 0`

would be a nonzero polynomial of degree at most `r-1` satisfied by `b` over `K_r(b^r)`: its nonconstant exponents are distinct and their coefficients are nonzero. This contradicts the degree `r`. Hence `[F_p(gamma):F_p]=D`. Computing the first linear dependence among `1,gamma,...,gamma^D` produces the desired monic minimal polynomial over `F_p`.

### `r=2`, odd `p`: the necessary exception is explicit

If `p=1 mod 4`, use the same nonresidue construction with `s=1`, starting from `Phi_2=X+1` and taking factors of successive `f(X^2)` up to `k=v_2(p-1)`. The resulting `a in F_p` has order `2^k` and is nonsquare. Since `-1` is a square in `F_p`, every element of `-4(F_p)^4` is a square, so the binomial criterion's exceptional possibility is excluded. Return `X^(2^e)-a`.

If `p=3 mod 4`, `X^2+1` is irreducible over `F_p`. For `e=1`, return it. For `e>=2`, take `s=2`, `k=v_2(p^2-1)>=3`, `f_2=X^2+1`, and recursively factor `f_(j-1)(X^2)` for `j=3,...,k`. For every `2<=j<=k`, `ord_(2^j)(p)=2`, so the selected factors have degree two. Let `a` be a root of `f_k`; it is nonsquare in `F_(p^2)`, which contains a square root of `-1`. Thus `X^(2^(e-1))-a` is irreducible over that quadratic field. A root `b` satisfies `a=b^(2^(e-1))`; hence `F_p(b)` contains `F_p(a)=F_(p^2)` and has degree `2^e`. Its monic minimal polynomial is exactly

`f_k(X^(2^(e-1))) in F_p[X]`.

This variant uses the factor oracle instead of Shoup's explicit quadratic-extension square-root formula. It avoids the need to trust or transplant that formula and still uses only degree-four oracle inputs.

### `r=p`: an Artin–Schreier tower with a trace certificate

Start with `K_0=F_p`, `a_0=1`. For `i=1,...,e`, define

`K_i=K_(i-1)[Y_i]/(Y_i^p-Y_i-a_(i-1))`,

`a_i=a_(i-1)*y_i^(p-1)`.

For any finite field of characteristic `p`, the map `z -> z^p-z` has kernel `F_p` and image exactly the kernel of the absolute trace to `F_p`. The trace map is nonzero: its defining polynomial has degree smaller than the field cardinality and is not the zero polynomial. Thus `Y^p-Y-c` has no root when `Tr(c)!=0`; by the Artin–Schreier dichotomy it is then irreducible of degree `p`.

The roots of `Y_i^p-Y_i-a_(i-1)` are `y_i+j` for `j in F_p`. Summing their `(p-1)`st powers gives `-1`, using the sums of powers over `F_p`. Therefore

`Tr_(K_i/K_(i-1))(a_i)=-a_(i-1)`,

and inductively `Tr_(K_i/F_p)(a_i)=(-1)^i !=0`. This supplies a certificate for every tower step. An element in a proper subfield of `K_i=F_(p^(p^i))` has absolute trace zero, because the relative degree of `K_i` over that subfield is divisible by `p`. Hence `a_i` generates `K_i`, and its minimal polynomial has degree `p^i`. Compute the final polynomial by linear dependence among its powers.

This tower is a variant of the Artin–Schreier construction in Shoup's proof, which credits Adleman–Lenstra. It requires no calls to `PF`. If `p|N`, then `p<=N`, so writing a degree-`p` polynomial is permitted by the dense degree bound. If `p>N`, this branch is never entered.

### Combining coprime degrees

Suppose irreducible polynomials `f,g` have coprime degrees `a,b`. In the tower

`F_p subset F_p[U]/f subset (F_p[U]/f)[V]/g`,

the second polynomial remains irreducible, since a degree-`b` Frobenius orbit splits over degree `a` into orbits of size `b/gcd(a,b)=b`. Let `u,v` denote the distinguished roots. The element `u+v` generates the degree-`ab` field: every maximal proper subfield has degree `ab/ell` for a prime `ell|ab`; it contains exactly one of the two component fields, so if it also contained `u+v`, subtraction would put both roots inside it, a contradiction. Compute the minimal polynomial of `u+v` by linear dependence. Combining prime-power degrees inductively yields degree `N`.

This coprime compositum argument is Shoup's Lemma 2.4, with ordinary exact linear algebra substituted for his product-of-conjugates implementation. It is established machinery.

## Pseudocode

```
ConstructPrime(p,N,PF):
    require p prime, N >= 1
    if N == 1: return X
    factor N by trial division
    for each prime-power D=r^e in N:
        if r == p:
            build trace-certified Artin-Schreier tower of degree D
            H_D = MinimalPolynomial(a_e)
        else if r == 2 and p % 4 == 3:
            if e == 1: H_D = X^2+1
            else:
                k = v_2(p^2-1); f = X^2+1
                for j in 3..k: f = FirstFactor(PF(f(X^2)))
                H_D = f(X^(D/2))
        else:
            s = multiplicative_order_by_iteration(p modulo r)
            k = valuation_by_division(p^s-1,r)
            f = FirstFactor(PF(1+X+...+X^(r-1)))
            for j in 2..k: f = FirstFactor(PF(f(X^r)))
            K_r = F_p[A]/f; a=A mod f
            if r == 2: H_D = X^D-a
            else:
                L = K_r[B]/(B^D-a)
                gamma = Trace_{L/F_(p^D)}(B)
                H_D = MinimalPolynomial(gamma)
    combine H_D by coprime-degree towers and MinimalPolynomial(u+v)
    return the final polynomial

ConstructOverBase(p,h,d,PF,ExtensionFactor):
    require h irreducible of degree m>=1, d>=1
    if d == 1: return X
    H = ConstructPrime(p,m*d,PF)
    factors = ExtensionFactor(H embedded into F_p[Z]/h,PF)
    assert every factor has degree d and multiplicity 1
    return lexicographically first factor
```

`MinimalPolynomial(c)` forms successive powers in a known finite-dimensional field algebra and solves over `F_p` for the first dependence. If the first dependence has degree `t`, its monic polynomial generates the kernel of the evaluation map `F_p[X] -> F_p(c)`, hence is the irreducible minimal polynomial. All matrices use the explicit recursively flattened power basis; no numerical linear algebra is involved.

## Concrete size and call ledger

Let `N=md`, `B=ceil(log_2 p)`, and `J` be the number of distinct prime divisors of `N`, so `J<=log_2 N` for `N>=2`.

| Operation | Dimension, degree, or count | Coefficient/integer size |
|---|---|---|
| Trial factorization of `N` | at most `N` trial divisors; polynomial numeric-degree cost | `O(log N)` bits |
| Order `s=ord_r(p)` | `s<=r-1<=N`; at most `r-1` modular multiplications | `O(log r)` bits |
| Compute valuation | `k<=sB`; at most `sB` divisions by known `r` | `p^s-1` has `O(sB)` bits |
| `PF(Phi_r)` | degree `r-1<=N`; one per relevant `r` | at most `(N+1)B` dense bits |
| `PF(f(X^r))` | degree `sr<=N^2`; `k-1` calls for odd/general branch | at most `(N^2+1)B` dense bits |
| Exceptional 2-power branch | degree 4; at most `2B` calls | `O(B)` coefficient bits |
| Total prime-field construction calls | at most `J(1+NB)+2B` (safe bound) | calls all to `F_p` |
| Odd-prime tower `L` | dimension `sD<=N^2` over `F_p` | every flattened entry `B` bits |
| Artin–Schreier towers | dimensions `p^i<=N` | every flattened entry `B` bits |
| Coprime composita | dimensions `ab<=N` | every flattened entry `B` bits |
| Minimal-polynomial systems | at most `M x (M+1)`, `M<=N^2`; Gaussian elimination `O(M^3)` prime operations | entries always reduced mod `p` |
| Trace computation | at most `s` powers by exponent `p^D`, bit length `DB+1`; `O(sDB)` tower multiplications by repeated squaring | stored exponents `O(NB)` bits |
| Arbitrary-base lift | one extension factorization of degree `N=md` over supplied degree-`m` field | dense lifted input length `O(NmB)` |

With schoolbook polynomial arithmetic, multiplying in a recursively flattened tower of total dimension `M` uses `O(M^2)` prime-field operations per tower level with harmless polynomial overhead; the number of levels is `O(log N)`. Reduction coefficients are part of the same bounded representations. Prime-field inversion uses the extended Euclidean algorithm on integers of `B` bits; multiplication/addition use standard exact integer arithmetic. Therefore the construction overhead is bounded by some fixed polynomial in `N+B`, independently of `PF`. A deliberately loose bound `O((N+1)^10(B+1)^4)` bit operations suffices for the above explicit implementation; optimizing that exponent is unnecessary here. The oracle contribution is bounded by

`[J(1+NB)+2B] * T(N^2,B)`.

The lift's extra oracle contribution should use the separately audited extension-factorization bound at degree `N`, including its trace-coordinate calls. The cost is polynomial in `m,d,B` even though the intermediate lifted polynomial has more coefficients than the final output.

## Boundary and failure conditions

- `N=1`, `d=1`, and `m=1` have explicit branches; no empty prime-factor list is used as an invalid field construction.
- Characteristic two uses the Artin–Schreier branch for 2-powers; it never invokes an odd-characteristic square-root argument.
- The 2-power binomial exception is essential. For example over `F_3`, `X^4+1=(X^2+X+2)(X^2+2X+2)`, even though `-1` is nonsquare. A blanket nonsquare-to-arbitrary-2-power binomial rule would be false.
- The source theorem's integer factorization of the numeric output degree is legitimate, because that degree contributes linearly to the dense output. It must not be described as an efficient factorization oracle for arbitrary binary integers.
- Distinct-factor and separability guarantees in the nonresidue stage use `r != p`. They are not valid if that condition is dropped.
- The construction's linear dependence steps operate over exact prime fields. Floating-point eigenvalues, numerical traces, or approximate zero tests would not supply proof certificates.
- Any material unverified gap in `PF` prevents the unconditional construction claim. The established algebraic reduction remains valid as a partial result, but is not a full resolution of the original project.

## Optional roots: no extra analytic assumption needed after core factorization

If complete deterministic finite-field factoring is actually established, then factoring the dense polynomial `X^r-a` and extracting its linear factors returns all `r`th roots that lie in the input field, including the characteristic-dividing case after multiplicity handling. Its time bound is polynomial in numeric `r,m,B`. For each fixed `r`, this is polynomial in `m,B`; for variable binary-encoded `r`, it is not a bound polynomial in `log r`. This is a direct factoring consequence and should not be marketed as a new nonresidue mechanism. The BIMS weak-GRH route is unnecessary for this optional fixed-`r` consequence, and was not used in this construction audit.

## Remaining gap and status

Construction route: **verified conditional reduction**. Remaining gap: actual unconditional validation of `PF` and extension factorization, plus executable clean-package verification if the upstream dependencies pass. Novelty status: inherited Shoup machinery and an immediate consequence of a new prime-field factoring theorem; no independent novelty claim is warranted for the algebraic construction itself. Upstream analytic validity and publication eligibility are outside this agent's reviewed scope and must be decided by the lead researcher after the independent audits.
