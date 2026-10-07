# Independent extension-field factorization reduction

Checked by subagent `extension_reduction`; checkpoint 2026-10-06 21:25 America/Los_Angeles (2026-10-07T04:25:04Z). Mathematical resolution of this **conditional reduction**: 90%; unconditional project target: not certified here; publication package: 0%. No external communication, git operation, or upstream edit occurred.

## Scope and dependency

The exact claim proved below is a deterministic polynomial-time **Turing reduction** from complete dense factorization over an explicitly represented finite field to complete dense factorization over its prime subfield. It does not validate family 142 or any analytic companion. Therefore it does not by itself establish an unconditional polynomial-time factorization theorem.

Assume a deterministic algorithm `PrimeFactor(p, u)` that returns the monic irreducible factors, with multiplicities, of every nonzero `u in F_p[X]`, and whose bit cost on degree at most `d` inputs is at most a nondecreasing bound `P(d,L)`, where `L = ceil(log_2 p)`. Suppose `p` is prime and `h in F_p[T]` is monic irreducible of degree `m >= 1`. Set `K=F_p[T]/(h)`, using the power basis `1,t,...,t^(m-1)` and canonical residues `0,...,p-1`. Input `f in K[X]` has degree `n` and dense encoding. The output consists of its leading coefficient and distinct monic irreducible factors with positive multiplicities in binary. Nonzero constants have empty factor lists; zero is returned as a separate zero-polynomial case, because it has no finite factorization into irreducibles.

There is a uniform deterministic reduction with polynomial nonoracle bit overhead in `n,m,L`. The trace version makes at most `mn` prime-factor calls, each on a polynomial of degree at most `n`, with sum of call degrees at most `mn^2`. The direct prime-Frobenius version makes at most `n` calls, with sum of call degrees at most `n^2`. Neither reduction enumerates `F_p` or `K`; integer factorization, primitive elements, GRH, and random choices are unused. For `P` polynomial, both are polynomial in the dense field/input/output size. This is an algorithmic consequence of a prime-field oracle, rather than a new base factorization mechanism.

The dense field definition has `m+1` prime-field coefficients, and a field element has `m` prime-field coefficients. Thus the field/input size is `Theta((n+2)mL)` up to binary dimension and separator overhead. The compressed factor output has at most `n` factors and sum of degrees at most `n`; its coefficient portion has `O(nmL)` bits and its multiplicity portion has `O(n log(n+1))` bits. Prescribed output degrees are not binary-compressed in a construction problem, which is separate from this reduction.

## Verifying the field promise without integer factorization

The irreducibility of `h` may be promised or checked. Starting with `v=T mod h`, repeatedly replace `v` by `v^p mod h` for `d=1,...,m`; check `gcd(h,v-T)=1` for every `1 <= d <= floor(m/2)` and check `v=T` at `d=m`. These checks are necessary if `h` is irreducible. Conversely a reducible degree-`m` polynomial has an irreducible factor of degree at most `m/2`, so one of the gcd checks detects it. This remains true for repeated factors. The final equality is redundant for sufficiency but provides the familiar finite-field certificate condition. There are at most `m` modular exponentiations and `m/2` gcds, and exponents have `L` bits. No factorization of `m` is required. Degree one is accepted after the equality check. Primality of `p` is an input promise or separately verified by a deterministic primality algorithm; this note does not treat a composite modulus as a field.

## Squarefree input: structural identities

Let `f` be monic squarefree of degree `d >= 1`, with unknown distinct monic irreducible factors `f_1,...,f_s`, of degrees `d_1,...,d_s`; `s <= d` and `sum d_a=d`. The Chinese remainder map gives

`A=K[X]/(f) ~= product_(a=1)^s K[X]/(f_a) ~= product_(a=1)^s F_(q^(d_a))`, where `q=p^m`.

The `q`-power map is `K`-linear on `A`. Its fixed algebra

`B_q=ker(Frob_q-I) ~= K^s`

therefore has `K`-dimension exactly `s`. The `p`-power map is generally **not K-linear**; it is `F_p`-linear on the `dm`-dimensional prime-field space `A`, and

`B_p=ker(Frob_p-I) ~= F_p^s`

has `F_p`-dimension exactly `s`. In a field of characteristic `p`, the roots of `Z^p-Z` are exactly its prime subfield; in `F_(q^(d_a))`, the roots of `Z^q-Z` are exactly the embedded `K`. These observations prove both fixed-algebra identities. They do not require knowing the factors while running the algorithm.

If `c in B_p` has component values `a_1,...,a_s in F_p`, then its monic minimal polynomial in `A`, computed over either `K` or `F_p`, is

`mu_c(Z)=product_(a in {a_1,...,a_s})(Z-a)`.

Indeed a polynomial annihilates `c` iff it vanishes at every component value; this divisibility condition proves the formula. Consequently `mu_c` is squarefree, splits into linear factors over `F_p`, and has degree at most `s`. No factor-degree information or hidden field oracle enters this assertion.

## Mechanism A: q-fixed algebra and trace coordinates

1. Form the `d by d` matrix over `K` for `u -> u^q-u`, in the basis `1,X,...,X^(d-1)`. Compute its kernel basis `b_1,...,b_s` by deterministic Gaussian elimination with the first available pivot.
2. For every `i=1,...,s` and `j=0,...,m-1`, form in `A`

   `c_ij = sum_(k=0)^(m-1) (t^j b_i)^(p^k)`.

   Its component values are `Tr_(K/F_p)(t^j b_i(a))`, hence lie in `F_p`. The equality is asserted only because each component value of `b_i` belongs to `K`; this trace formula is not being applied as the field trace of arbitrary elements in the larger factors.
3. Construct the minimal polynomial of `c_ij` by the first linear dependence among `1,c_ij,...,c_ij^s` over `K`. Incremental elimination in the ambient `d`-dimensional space constructs the unique monic first relation. The structural formula above proves its coefficients belong to the canonical embedded `F_p`. Convert them by checking every nonconstant power-basis coordinate is zero. The algorithm need not assume this property without checking it.
4. Call `PrimeFactor(p, mu_cij)`. Check that all returned irreducible factors are distinct linear factors and their product equals `mu_cij`. Their roots give exactly the finite list of component values of `c_ij`.
5. For each current monic block `g` of `f`, refine it by gcds `gcd(g,c_ij-a)` for the returned roots `a`. Keep nonconstant gcds and omit unit gcds. No enumeration of all prime-field values occurs. Reduction of `c_ij` modulo `g` is optional: the gcd with a representative modulo `f` has the same result because `g | f`.

### Trace separation proof and the case p divides m

The trace map is nonzero. The polynomial `S(Y)=sum_(k=0)^(m-1)Y^(p^k)` has degree `p^(m-1)<p^m`, is nonzero, and cannot vanish on every element of `K`. This includes `m=1`, where `S(Y)=Y`. For `delta != 0`, multiplication by `delta` is a bijection of `K`; thus `y -> Tr(delta*y)` is nonzero. If it vanished on all power-basis elements `t^j`, linearity would make it vanish on all `K`. Therefore some `j` has `Tr(t^j delta)!=0`. This proves the trace pairing is nondegenerate without computing a dual basis.

For distinct component indices `a != b`, the two coordinate functionals on `B_q=K^s` are distinct. Thus some basis element `b_i` has `b_i(a)-b_i(b)!=0`. Nondegeneracy supplies `j` such that `c_ij(a)!=c_ij(b)`. After every trace coordinate has refined the blocks, no block contains two irreducible components. Each resulting block is therefore one `f_a`.

`Tr(1)=m mod p` may vanish. Using only `Tr(b_i)` would then be unsafe. All `m` trace coordinates are essential to the proof as stated; the algorithm does not discard them when `p | m`.

### Detailed counts for one squarefree degree-d input

Use ordinary dense arithmetic, with polynomial multiplication/reduction and polynomial gcd each bounded by `O(d^2)` field operations. A field operation includes inversion when required. Let `L=ceil(log_2 p)`.

| Operation | Dimensions / count | Conservative cost |
|---|---:|---:|
| q-Frobenius matrix | `d` columns, `d by d` over `K` | `O(d^3 mL)` K operations, computing each column by binary powering |
| q-fixed kernel | `d by d` over `K` | `O(d^3)` K operations |
| trace elements | `ms <= md` elements; `m-1` p-powers each | `O(m^2 s d^2 L)` K operations |
| first dependence | `d by (s+1)` over `K`, per element | `O(s d^2+d s^2+s^3)` K operations per element using incremental elimination |
| prime calls | `ms`, degree `<=s` each | `<= ms P(s,L)` bit cost |
| gcd refinement | at most `s` current blocks times at most `s` roots, per element | `<=m s^3` gcds; `O(m s^3 d^2)` K operations |
| root/product checks | degree `<=s`, per call | polynomial in `m,s,L`, subsumed in displayed bounds |

The first-dependence cost includes tracking linear-combination coefficients, so it does not rely on a free nullspace certificate. The relation search always reaches a dependence by index `s`; no powers up to `q` or `p` are generated. Combining the displayed bounds gives the safe, intentionally loose nonoracle count

`O(m^2 d^5 (L+1))` K operations.

In the chosen field model, a K addition, multiplication, or inversion can all conservatively be bounded by `O(m^2(L+1)^3)` bit operations using schoolbook polynomial arithmetic and extended Euclid; the coefficients always remain canonical residues modulo `p`. Thus one squarefree input has nonoracle overhead `O(m^4 d^5 (L+1)^4)` bits plus `ms P(s,L)`. This is a polynomial-bound assertion, not a claim of practical efficiency. More efficient Frobenius and multiplication methods improve it, but are unnecessary here.

## Mechanism B: direct p-fixed algebra

This is an independent reduction that avoids the trace pairing and has fewer prime-oracle calls.

1. Use the prime-field basis `t^j X^i`, `0<=i<d, 0<=j<m`, of `A`. Compute each column `(t^j X^i)^p-t^j X^i` modulo `f`, expand its `K` coefficients in the power basis, and compute the kernel of the resulting `dm by dm` matrix **over F_p**. Its basis `c_1,...,c_s` has size `s` by the structural identities above.
2. For each `c_i`, compute its first power dependence over `F_p`, call `PrimeFactor` on the resulting split squarefree `mu_ci`, and refine by gcds with its returned roots as in Mechanism A.

A basis of `F_p^s` separates all pairs of coordinates: if every basis vector had equal values at two coordinates, every vector in its span would have equal values there, contradicting the corresponding coordinate idempotent. Thus the final blocks are exactly the irreducible factors. This proof avoids trace nondegeneracy entirely.

The p-Frobenius matrix requires at most `dm` binary powers, each costing `O(d^2L)` K operations, or `O(md^3L)` K operations total. Its kernel uses `O((dm)^3)` F_p operations. Each first-dependence computation uses at most `s` quotient-algebra multiplications (`O(sd^2)` K operations) and incremental elimination on `dm` rows (`O(dm s^2+s^3)` F_p operations). There are `s` such computations. At most `s^3` gcds cost `O(s^3d^2)` K operations. Hence a safe split accounting is

`O(md^3L+d^5)` K operations and `O(m^3d^3+md^4)` F_p operations,

plus at most `s P(s,L)` bits for prime calls. With the same schoolbook bounds, its nonoracle bit cost is

`O((m^3d^3(L+1)+m^2d^5)(L+1)^3)`.

The latter is a tighter conservative bound for this direct variant. Either it or the trace variant is polynomial in the dense data. The direct variant must never be implemented as a `d by d` K-linear p-Frobenius matrix: p-Frobenius is semilinear over `K`, so that shortcut would be wrong except `m=1` or specially restricted coefficients.

## Multiplicities and inseparability

Normalize nonconstant nonzero input by its leading coefficient. For monic `f`, run:

```
Squarefree(f):
    C = gcd(f, derivative(f))
    W = f / C
    i = 1
    while W != 1:
        Y = gcd(W, C)
        Z = W / Y
        if Z != 1: emit (Z, i)
        W = Y
        C = C / Y
        i = i + 1
    if C != 1:
        verify derivative(C) == 0
        H = pth_root(C)
        for (Z,j) in Squarefree(H): emit (Z,p*j)
```

For `C=sum c_k X^k` with zero derivative, all nonzero exponent indices are divisible by `p`, and its unique pth root in `K[X]` is

`H=sum_j c_(pj)^(p^(m-1)) X^j`.

Indeed `a^(p^m)=a` in `K`, so `a -> a^(p^(m-1))` inverts p-Frobenius. For `m=1` this is exponent `1`, as it should be. Binary powering uses `O(mL)` K operations per coefficient, rather than `p^(m-1)` successive operations. If `p>deg C`, a nonconstant C with zero derivative cannot arise. Dividing exponent indices by the binary-encoded p does not enumerate p values.

To verify the squarefree algorithm, fix an irreducible factor `g` of input multiplicity `e`. The derivative gcd initially gives exponent `e-1` when `p` does not divide `e`, and exponent `e` when `p` divides `e`, because `g` is separable over a finite field. Thus `W` initially has exponent one precisely for `p` not dividing `e`. The loop removes that factor in `Z` at iteration `i=e`, while factors with p-divisible multiplicity remain in `C`. At termination every multiplicity remaining in `C` is divisible by `p`. Taking its unique pth root divides all those multiplicities by p; recursion and multiplying returned labels by p recover them. Each emitted `Z` is squarefree. Emitted products have pairwise disjoint irreducible supports, because the p-divisible and non-p-divisible multiplicity cases are disjoint at each recursive stage. Every original irreducible factor appears once with its correct multiplicity.

The recursion depth is at most `floor(log_p n)`, at most `floor(log_2 n)`. The sum of input degrees across recursive calls is at most `n+n/p+n/p^2+... <=2n`. Loop counts and gcd counts are `O(n)`, and all degrees are at most `n`. Thus `O(n^3+nmL)` K operations safely cover squarefree decomposition, coefficient pth roots and exact divisions; normalization adds only polynomial overhead. The multiplicities never exceed `n`, so their encodings have `O(log(n+1))` bits. This proof includes characteristic two, wholly inseparable polynomials, mixed multiplicities and extension degree one.

Now apply either squarefree factoring reduction separately to all emitted `Z_l`, of degrees `d_l`. Their disjoint supports give `sum d_l <= n`. Therefore `sum d_l^k <= n^k` for integer `k>=1`. The overall trace reduction keeps the bound `O(m^4 n^5(L+1)^4)+mn P(n,L)`, rather than paying n extra copies of the worst bound, and at most `mn` calls with sum of call degrees `<=m sum d_l^2<=mn^2`. The direct variant similarly has at most `n` calls, total call degree `<=n^2`, and the direct displayed overhead with `d` replaced by `n`, plus the squarefree cost. Degree-one factors, `m=1`, and `p=2` require no special algorithmic exception beyond the constant/zero input conventions.

## Pseudocode for the complete direct variant

```
FactorOverExplicitField(p,h,f):
    require p prime and h monic irreducible, deg h=m>=1
    if f==0: return ZERO
    scalar = leading_coefficient(f)
    if deg f==0: return (scalar, [])
    answer=[]
    for (u,e) in Squarefree(f/scalar):
        d=deg u
        M = columns of Frob_p-I on basis t^j X^i of K[X]/u
        basis = deterministic_kernel_over_Fp(M)
        blocks=[u]
        for c in basis:
            mu = first_power_relation_over_Fp(c, ambient_dimension=d*m)
            roots = roots_from_checked_linear_factorization(PrimeFactor(p,mu))
            refined=[]
            for g in blocks:
                for a in roots:
                    v=gcd(g,c-a)
                    if deg v>0: refined.append(v)
            verify product(refined)==u
            blocks=refined
        verify product(blocks)==u
        for g in blocks: answer.append((g,e))
    verify scalar*product(g^e for (g,e) in answer)==f
    return (scalar,answer)
```

The pseudocode's product check after refinement is against the squarefree `u`; internally each former block can also be checked. Each gcd is monic. Distinct roots partition component supports, so the displayed loop includes no repeated nonconstant gcd. The final reconstruction check is necessary for implementation validation but does not prove irreducibility on its own; the separating-basis proof supplies that part.

## Adversarial checks completed and limits

* **Semilinearity:** p-Frobenius is used only in an F_p matrix; q-Frobenius is used in a K matrix.
* **p divides m:** the full trace pairing separates even when `Tr(1)=0`; a concrete F_4 fixture should test this.
* **Minimal-polynomial field:** K-linear relations in the trace version have F_p coefficients because the exact minimal polynomial is the product over distinct F_p component values, not because an arbitrary annihilating relation was chosen.
* **Exponent lengths:** q has `O(mL)` bits; a p-power has `L` bits; inverse coefficient Frobenius has `O(mL)` bits. No iteration up to p or q occurs.
* **Gcd splitting:** all roots actually occurring among the components are returned, so the nonconstant gcds partition every current block; the result is not a one-root search that could miss a component.
* **Dimension:** the q-fixed algebra has K-dimension s, the p-fixed algebra has F_p-dimension s, and the ambient spaces have dimensions d and dm respectively.
* **Derivative-zero inputs:** they pass to the pth-root recursion before any Berlekamp argument requiring a reduced algebra.
* **Zero and constants:** zero is a separate output status; nonzero constants return their scalar and no factors.
* **No prime factorization oracle for integers:** even field-definition irreducibility can be checked by all degrees up to m/2. The reduction oracle factors polynomials only.

These deductions establish the conditional transfer, not the central prime-field hypothesis. The family-142 audit and any family-003/029 analytic gap remain outside this note. No novelty or priority claim is certified here. A reference computation with a small-prime exhaustive oracle can validate implementation mechanics, but cannot substantiate the polynomial-time prime-field oracle or remove this conditional status.
