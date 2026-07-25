# Full wreath-product monodromy through the third iterate of an explicit Keller map

**Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI)**

Public research draft, first posted 21 July 2026 at 18:44:48 UTC.
Strengthened site edition: 22 July 2026, 02:24:28 UTC. Not peer reviewed.

> Alec Kriebel is a complete amateur exploring the limits of AI-assisted
> mathematics and cannot independently verify the claims in this note. The
> argument and exact certificates are being released to make expert checking
> and rapid correction possible. No claim of guaranteed worldwide priority is
> made.

**Revision note.** The site edition first expanded two points identified in
external AI review: Section 3.1 proves that the degree-nine resultant has no
extraneous generic branch and identifies the complete function-field tower;
Section 8 is a local-field/Puiseux induction with every Newton and
reconstruction valuation written explicitly. The present revision adds an
exact degree-27 certificate and proves the full third-level wreath product.

## Abstract

Let `F : C^3 -> C^3` be the newly announced noninjective polynomial map with
constant Jacobian determinant `-2` and generic geometric monodromy `S_3`. We
determine the geometric monodromy of its second and third iterates. They are
the full iterated imprimitive wreath products

```text
Mon(F^2) = S_3 wr S_3,
Mon(F^3) = S_3 wr S_3 wr S_3.
```

Their degrees are `9` and `27`, and their group orders are `1296` and
`13,060,694,016`. The proof is geometric. On the target line `(1,2,s)`, exact
primitive eliminants have one-edge Newton polygons at infinity, giving a
9-cycle and a 27-cycle. Each discriminant has a squarefree divisor occurring
with multiplicity one, hence supplies a single deepest-block transposition;
at level three, exact leading-coefficient and reconstruction-denominator
guards are included. Elementary group lemmas force the full wreath products.
Postcomposing `F o F` by
`diag(1/4,1,1)` gives a noninjective polynomial self-map of `C^3` with
Jacobian determinant one and monodromy `S_3 wr S_3`. More generally, every
iterate `F^m` has a full `3^m`-cycle in its geometric inertia at infinity.
Exact SymPy, independent dependency-free finite-field, GAP, and PARI/GP checks
accompany the proof.

## 1. The map and statement

Put `u = 1+xy` and define `F=(F_1,F_2,F_3)` by

```text
F_1 = u^3 z + y^2 u (4+3xy),
F_2 = y + 3x u^2 z + 3xy^2(4+3xy),
F_3 = 2x - 3x^2y - x^3z.
```

Exact expansion gives `det JF = -2`. The three points

```text
(0,0,-1/4), (1,-3/2,13/2), (-1,3/2,13/2)
```

all map to `(-1/4,0,0)`.

Let `G=F o F`. We use `Mon(G)` for the Galois group of the normal closure of
the induced function-field extension, in its natural action on the generic
fiber.

Define `W_1=S_3` and

```text
W_(m+1) = S_3^(3^m) semidirect W_m
```

in the natural action on the depth-`m+1` ternary tree.

**Theorem.** The second and third iterates have generic degrees nine and 27,
respectively, and

```text
Mon(F^2) = W_2 = S_3 wr S_3 <= S_9,
Mon(F^3) = W_3 = S_3 wr S_3 wr S_3 <= S_27.
```

Here `|W_2|=6^4=1296` and
`|W_3|=6^(1+3+9)=13,060,694,016`. The depth-three action has nine bottom
blocks of size three, indexed by the points in a generic fiber of `F^2`.

**All-iterate full-cycle statement.** For every `m >= 1`, the geometric
monodromy of `F^m` contains a cycle of length `3^m`. This does not assert that
the entire group is the full `m`-fold iterated wreath product.

**Corollary.** If

```text
G_hat = (G_1/4, G_2, G_3),
```

then `det JG_hat = 1`, `Mon(G_hat)=S_3 wr S_3`, and `G_hat` is noninjective.
Indeed, all three displayed collision points map under `G_hat` to
`(0,0,-1/2)`.

## 2. The cubic inverse resolvent

For a target `(a,b,c)`, introduce

```text
C_(a,b,c)(t) = 2a t^3 - b t^2 + 2t - c.
```

For a simple root `t`, the generic preimage is reconstructed by

```text
y = -(b t^2 + 3c - 6t)/(2t^2),
x = t/(1-ty),
z = (2x - 3x^2y - c)/x^3.
```

Substitution reduces each coordinate of `F(x,y,z)-(a,b,c)` to zero modulo
`C_(a,b,c)(t)`. Thus the three roots of the cubic parametrize the generic
fiber. This is the reciprocal form of the more familiar resolvent obtained
from `T=y+1/x`: here `t=x/(1+xy)=1/T`.

For `G=F o F`, the generic fiber is partitioned by the three roots of the
outer cubic. Over each outer root, a second cubic parametrizes three inner
preimages. Therefore

```text
Mon(G) <= S_3 wr S_3.
```

Iterating once more gives the natural depth-three ternary-tree block system,
so `Mon(F^3) <= W_3`. Its action on the nine bottom blocks is the monodromy of
the intermediate `F^2` cover. The remaining problems are to prove equality at
levels two and three.

## 3. A degree-nine one-parameter slice

Restrict the target to `(a,b,c)=(1,2,s)`. Let `t` satisfy

```text
2t^3 - 2t^2 + 2t - s = 0
```

and reconstruct the corresponding intermediate point `(x(t),y(t),z(t))` by
the formulas above. An inner resolvent root `r` then satisfies

```text
2x(t) r^3 - y(t) r^2 + 2r - z(t) = 0.
```

Eliminating `t`, and removing the vertical content `256s^7`, gives the
following primitive polynomial:

```text
P(r,s) =
  128 r^9 s - 256 r^8
  + 2592 r^7 s^2 - 3072 r^7 s + 1408 r^7
  - 7452 r^6 s^3 + 1248 r^6 s^2 - 1584 r^6 s - 576 r^6
  - 17496 r^5 s^4 + 82944 r^5 s^3 - 87936 r^5 s^2
      + 42240 r^5 s - 5760 r^5
  + 52488 r^4 s^4 - 142884 r^4 s^3 + 135144 r^4 s^2
      - 60144 r^4 s + 8928 r^4
  + 104976 r^3 s^5 + 97200 r^3 s^4 - 97056 r^3 s^3
      - 41472 r^3 s^2 + 93824 r^3 s - 26880 r^3
  + 236196 r^2 s^6 - 380538 r^2 s^5 - 147744 r^2 s^4
      + 772080 r^2 s^3 - 754944 r^2 s^2 + 333792 r^2 s
      - 62208 r^2
  + 236196 r s^6 - 734832 r s^5 + 1916784 r s^4
      - 2658432 r s^3 + 2128320 r s^2 - 919296 r s + 186624 r
  + 531441 s^8 - 2204496 s^7 + 5436882 s^6 - 11805534 s^5
      + 17996446 s^4 - 17402304 s^3 + 10364976 s^2
      - 3544992 s + 557280.
```

### 3.1 Why the eliminant is the actual fiber polynomial

This point is slightly more delicate than the resultant calculation alone.
Put `K=C(s)` and

```text
C_0(t)=2t^3-2t^2+2t-s.
```

The polynomial `C_0` is irreducible over `K`: equivalently,
`s=2t^3-2t^2+2t` defines a degree-three map of rational function fields.
Thus the intermediate slice field is `K_1=K(t)`. On `C_0=0`, the
reconstruction formulas simplify to

```text
x(t) = 2t^2/(3s+2t^2-4t),
y(t) = -(3s+2t^2-6t)/(2t^2).
```

The exact resultants

```text
Res_t(C_0,t)=s,
Res_t(C_0,3s+2t^2-4t)=4s(27s^2-28s+12)
```

show that every reconstruction denominator is nonzero over the generic point
of the `s`-line.

Let `N(t,r,s)` be the numerator obtained after substituting the reconstructed
intermediate point into the inner cubic, and let `R` be the remainder of `N`
modulo `C_0`; then `deg_t R=2`. The exact checker verifies

```text
Res_t(C_0,R)=4s^7 P(r,s).
```

More importantly, the subresultant degrees of `C_0,R` with respect to `t`
are

```text
3, 2, 1, 0.
```

Write the degree-one subresultant as

```text
L(t,r,s)=lambda(r,s)t+mu(r,s).
```

Here `lambda` has `r`-degree six, 52 nonzero terms, and

```text
gcd(P,lambda)=1 in C(s)[r].
```

Consequently, at the generic point of every component of `P=0`, the common
root is recovered by `t=-mu/lambda`. It satisfies both `C_0=0` and the inner
cubic, and none of the reconstruction denominators vanishes generically.
Conversely, every genuine pair `(t,r)` annihilates the resultant. Thus the
primitive resultant has no extraneous generic branch: its function field is
the function field of the two-step inverse incidence curve.

## 4. A 9-cycle at infinity

Write `u=1/s` and consider `u^8 P(r,u^-1)`. For the coefficients of
`r^0,...,r^9`, their `u`-adic valuations are

```text
0, 2, 2, 3, 4, 4, 5, 6, 8, 7.
```

Every intermediate point lies strictly above the line from `(0,0)` to
`(9,7)`. Thus the lower Newton polygon is one edge of slope `7/9`.

For completeness, set `u=v^9` and `r=v^-7 w`. The initial equation becomes

```text
128 w^9 + 531441 = 0.
```

Its nine roots are simple, so each lifts uniquely to a Puiseux branch. The
local deck transformation `v -> zeta_9 v` multiplies the leading term of `w`
by `zeta_9^-7`. Since `gcd(7,9)=1`, it permutes all nine branches in one orbit.
Hence the geometric monodromy of the slice contains a 9-cycle `alpha`.

In particular, `P` is irreducible over `C((1/s))`, hence over `C(s)`.
Combining this with the subresultant calculation in Section 3.1 gives the
explicit field tower

```text
C(s)  subset  C(s)(t)  subset  C(s)(t,r)=C(s)(r),
          degree 3                 total degree 9.
```

The inner step therefore has degree three, `P` is the genuine degree-nine
fiber polynomial, and the nine Puiseux branches are precisely the nine sheets
of the pullback of `F o F` to the line. This proves both generic degree and the
absence of hidden vertical or denominator components used below.

## 5. A single transposition

Exact discriminant factorization gives

```text
disc_r(P) = 2^38 q(s)^8 A(s) B(s)^2,
q(s) = 27s^2 - 28s + 12,
```

where

```text
A(s) =
  1129718145924 s^12 - 6474958632657 s^11
  + 21955119111630 s^10 - 60661410535386 s^9
  + 123515279853390 s^8 - 191093865073182 s^7
  + 235490291194248 s^6 - 188631015819696 s^5
  + 54561577345568 s^4 + 41882989175328 s^3
  - 44714997684096 s^2 + 15094447332352 s
  - 1434819245056.
```

The exact checker verifies that `A` is squarefree and coprime to `q`, `B`, and
the leading coefficient `128s`. At every root of `A`, the discriminant
therefore has valuation one while the degree remains nine. Exactly one pair of
roots coalesces simply, so local geometric inertia is a single transposition
`beta`.

Because the nine sheets have a three-by-three block system, a permutation that
moves only two sheets cannot act nontrivially on the set of blocks. Thus
`beta` is supported inside one block.

The degree-22 polynomial `B`, included for full reproducibility, is

```text
B(s) =
  1423119505038213888 s^22 - 155058052818404824443 s^21
  + 1413754646027656083066 s^20 - 8145658955220494785812 s^19
  + 33677018812011807334224 s^18 - 108385682498649366622416 s^17
  + 280859820926917245978240 s^16 - 598631883156564470992728 s^15
  + 1062288637590844067815584 s^14 - 1579910926841521168581900 s^13
  + 1974730823883289142626824 s^12 - 2073348574060015592229024 s^11
  + 1822485349587628391880960 s^10 - 1333523184375693801555072 s^9
  + 806144943610022071172864 s^8 - 398941760796329492797440 s^7
  + 159756878618286560778240 s^6 - 50952869532774134959104 s^5
  + 12636860641575849510912 s^4 - 2344566242453066735616 s^3
  + 304677812001210531840 s^2 - 24551525690267664384 s
  + 926711257485017088.
```

## 6. A transposition of the blocks

The outer cubic on the same line has discriminant

```text
disc_t(2t^3-2t^2+2t-s) = -4(27s^2-28s+12) = -4q(s).
```

The quadratic `q` is squarefree and coprime to `A` and `B`. A small loop about
either root of `q` therefore has outer monodromy a transposition. The inertia
of the total nine-sheet cover contains an element `gamma` whose image on the
three blocks is that transposition.

## 7. The group lemma

**Lemma.** Let `H` be a subgroup of `S_3 wr S_3` in its natural action on
three blocks of size three. Suppose that `H` contains:

1. a 9-cycle `alpha`;
2. a single transposition `beta`; and
3. an element `gamma` inducing a transposition on the three blocks.

Then `H=S_3 wr S_3`.

**Proof.** The 9-cycle induces a 3-cycle on the blocks. Its cube acts as a
3-cycle inside each block. The single transposition is supported in one block;
conjugating it by `alpha^3` gives a distinct transposition in the same block.
Those two transpositions generate the full `S_3` supported on that block.
Conjugating by powers of `alpha` gives the full `S_3` independently on all
three blocks, so the base subgroup `S_3^3` lies in `H`.

On blocks, `alpha` supplies a 3-cycle and `gamma` a transposition, so the image
of `H` is the top `S_3`. A subgroup containing the full base and surjecting to
the top is the whole semidirect product. QED.

Applying the lemma to the three inertia elements above shows that the slice
monodromy is `S_3 wr S_3`. Slice monodromy embeds into generic monodromy, while
Section 2 gave the opposite upper bound. This proves the level-two assertion
of the theorem.

## 8. Full-cycle inertia for every iterate

We replace a growth heuristic by a local-field induction. Put `u=1/s`, let
`K=C((u))` with valuation `nu(u)=1`, and work in a fixed Puiseux closure of
`K`. Start from `X_0=(1,2,u^-1)` and choose a compatible inverse tower
`F(X_(k+1))=X_k`. We prove inductively that, for nonzero leading units,

```text
nu(x_k)= a_k,     nu(y_k)=-a_k,     nu(z_k)=-c_k,
```

where `a_0=0`, `c_0=1`, and that the local branch field at level `k` has
ramification degree `3^k` over `K`.

Assume the statement at level `k`. The next inverse parameter satisfies

```text
2 x_k t^3 - y_k t^2 + 2t - z_k = 0.
```

The valuations of its coefficients, in increasing powers of `t`, are

```text
(-c_k, 0, -a_k, a_k).
```

If `c_k>5a_k`, the two middle points lie strictly above the segment joining
`(0,-c_k)` to `(3,a_k)`. The Newton polygon theorem therefore gives, for
each of the three roots,

```text
nu(t_(k+1)) = -(a_k+c_k)/3.
```

The endpoint residual polynomial is a binomial cubic with nonzero endpoint
coefficients and is separable in characteristic zero.

It remains to justify the valuations after reconstruction, including every
possible cancellation. In

```text
y_(k+1) = -(y_k t^2 + 3z_k - 6t)/(2t^2),
```

the term `3z_k` is uniquely smallest because

```text
-c_k < -a_k+2nu(t),    -c_k < nu(t).
```

Hence

```text
nu(y_(k+1))=(2a_k-c_k)/3=-a_(k+1).
```

Next `nu(t y_(k+1))=(a_k-2c_k)/3<0`, so `t y_(k+1)` uniquely dominates `1`
in the denominator of

```text
x_(k+1)=t/(1-t y_(k+1)),
```

and `nu(x_(k+1))=a_(k+1)`. Finally, `-z_k` uniquely dominates the numerator
of

```text
z_(k+1)=(2x_(k+1)-3x_(k+1)^2 y_(k+1)-z_k)/x_(k+1)^3,
```

so `nu(z_(k+1))=-c_(k+1)`, where

```text
a_(k+1) = (c_k-2a_k)/3,
c_(k+1) = 2(c_k-a_k).
```

Thus all leading coefficients stay nonzero. For `rho_k=a_k/c_k`, the
interval `0<=rho_k<=1/6` is invariant under

```text
rho_(k+1)=(1-2rho_k)/(6(1-rho_k));
```

its image is contained in `[2/15,1/6]` after the first step. In particular,
`c_k>5a_k` at every level, completing the valuation induction.

For the ramification induction, set

```text
A_k=3^k a_k,       C_k=3^k c_k.
```

These are integers satisfying

```text
A_0=0, C_0=1,
A_(k+1)=C_k-2A_k,
C_(k+1)=6(C_k-A_k).
```

At the `m`th inverse step,

```text
nu(t_m)=-E_m/3^m,       E_m=A_(m-1)+C_(m-1).
```

For `m>=2`, `C_(m-1)` is divisible by three and
`A_(m-1)=1 mod 3`; the case `m=1` has `E_1=1`. Hence `3` never divides
`E_m`. The level-`m-1` branch field has value group
`(1/3^(m-1)) Z`, while `nu(t_m)` has exact denominator `3^m`. Adjoining
`t_m` therefore has ramification degree at least three. Its defining
polynomial is cubic, so the relative field degree and ramification degree are
both exactly three. Since the reconstruction is rational and
`t_m=x_m/(1+x_m y_m)`, no field is lost in passing between `t_m` and `X_m`.

Inductively, the chosen level-`m` local branch has degree and ramification
index `3^m` over `C((u))`. The global slice cover has degree at most `3^m`,
so this one branch exhausts it and is totally ramified. Newton-Puiseux theory
in characteristic zero makes tame inertia cyclic and transitive on its
`3^m` conjugates; its generator is a single `3^m`-cycle. This proves the
all-iterate statement.

As an independent check, nested PARI resultants for `m=3` produce a
degree-27 eliminant. After removing common vertical content, its lower Newton
edge is `(0,0)-(27,34)`, agreeing with the recurrence.

## 9. Full wreath monodromy at level three

We now retain more information from that exact level-three eliminant. On the
same target line, put

```text
C_0(t) = 2t^3 - 2t^2 + 2t - s,
X_1 = reconstruct((1,2,s),t),
C_1(t,r) = numerator(C_(X_1)(r)),
X_2 = reconstruct(X_1,r),
C_2(t,r,q) = numerator(C_(X_2)(q)).
```

Here `reconstruct` denotes the three rational formulas in Section 2. Form the
nested resultant

```text
R(q,s) = Res_t(C_0, Res_r(C_1,C_2))
```

and divide by its content in `q`, obtaining the primitive polynomial `Q(q,s)`.
The exact computation gives

```text
deg_q R = 27,    deg_s R = 244,
deg_s content_q(R) = 196,
deg_q Q = 27,    deg_s Q = 48.
```

With `u=1/s`, the lower Newton polygon of the normalized polynomial is the
single edge

```text
(0,0) -- (27,34).
```

Because `gcd(27,34)=1`, every irreducible factor over `C((u))` would have
degree divisible by 27. Thus `Q` is irreducible over `C((u))`, hence over
`C(s)`, and local inertia contains a 27-cycle `alpha`.

The rational reconstruction denominators do not create a hidden component.
Indeed, if `D_1` and `D_2` are the denominators cleared in the definitions of
`C_1` and `C_2`, the exact checker forms

```text
L(s) = Res_t(C_0,D_1),
U(s) = Res_t(C_0,Res_r(C_1,D_2)).
```

Both are nonzero. Choose a generic inverse tower and its deepest resolvent
parameter `q`; reconstruction is defined there and elimination gives
`Q(q,s)=0`. Since `Q` is irreducible of degree 27, it is the minimal polynomial
of this genuine `q`. The corresponding inverse-tower field therefore has
degree at least 27, while the three cubic steps give degree at most `3^3`.
Equality holds, `q` generates the tower field, and `Q` is precisely the
generic fiber polynomial of the pulled-back third iterate.

It remains to obtain a deepest-block transposition. Let

```text
D = disc_q(Q),
G = gcd(D,dD/ds),
R_sf = D/G,
M = gcd(R_sf,G),
E = R_sf/M.
```

Thus `E` is the product of exactly those irreducible discriminant factors
which occur with multiplicity one. Exact PARI arithmetic gives

```text
deg_s D = 1612,       deg_s R_sf = 752,
deg_s M = 676,        deg_s E = 76.
```

Moreover, `E` is squarefree and coprime to `M`, to the degree-27 leading
coefficient of `Q` (which has `s`-degree 14), and to both `L` and `U`. At any
root of `E`, therefore, the degree remains 27, every reconstructed point is
genuine, and the discriminant has valuation exactly one. Local geometric
inertia is a single transposition `tau`. Since monodromy preserves the nine
bottom blocks of size three, a permutation moving only two leaves must be
supported inside one bottom block.

We finish with the depth-three group argument. The image of `Mon(F^3)` on the
nine bottom blocks is `Mon(F^2)=W_2`. The 27-cycle `alpha` induces a 9-cycle
on those blocks, and `alpha^9` acts as a 3-cycle in each bottom block. Hence
`tau` and its conjugate by `alpha^9` generate the full `S_3` on one bottom
block. Conjugating by powers of `alpha` gives independent `S_3` factors on
all nine bottom blocks, so the full kernel `S_3^9` lies in `Mon(F^3)`. A
subgroup containing this kernel and surjecting onto `W_2` is all of

```text
W_3 = S_3^9 semidirect W_2.
```

Consequently

```text
Mon(F^3) = W_3,
|W_3| = 6^(9+3+1) = 13,060,694,016.
```

This paper proves level three only. A separate bounded-memory computation,
published in `w4_search/RESULT.md`, subsequently produced and independently
audited the required deepest-block transposition at level four and proves
`Mon(F^4)=W_4`. Its localization and norm-to-inertia argument are intentionally
kept outside this level-three paper.

## 10. Independent arithmetic cross-check

At `s=-3`, the primitive specialization is

```text
-384r^9 - 256r^8 + 33952r^7 + 216612r^6 - 4580568r^5
+9515052r^4 - 15697056r^3 + 223986114r^2
+599887620r + 17172300267.
```

Dependency-free modular arithmetic verifies squarefree factorizations with
irreducible-degree patterns

```text
mod 13: (9)
mod 61: (2,1,1,1,1,1,1,1)
mod 19: (2,2,2,2,1).
```

These are Frobenius cycle types `(9)`, `(2,1^7)`, and `(2^4,1)`. The same
elementary lemma forces the arithmetic Galois group to be the full wreath
product. GAP independently enumerates every subgroup of the wreath product and
finds no proper survivor. PARI/GP 2.17.4 also identifies five unrelated
rational fibers as transitive group `9T31`, named
`[S(3)^3]S(3)=S(3)wrS(3)`.

This arithmetic calculation is corroboration only; unlike a bare arithmetic
specialization, the proofs in Sections 4-7 and 9 determine geometric
monodromy.

## 11. Verification

From the repository root:

```console
python3 -m pip install -r discovery_04_wreath_monodromy/requirements.txt
python3 discovery_04_wreath_monodromy/verify_symbolic.py
python3 discovery_04_wreath_monodromy/verify_modular.py
python3 discovery_04_wreath_monodromy/verify_iterate_inertia.py
```

If PARI/GP and GAP are installed:

```console
gp -q discovery_04_wreath_monodromy/verify_pari.gp
gap -q discovery_04_wreath_monodromy/verify_group.g
python3 discovery_04_wreath_monodromy/verify_level3_newton.py
python3 discovery_04_wreath_monodromy/verify_level3_wreath.py
```

The symbolic verifier checks the Jacobian and collisions, the inverse
resolvent identities, denominator resultants, the exact resultant, the linear
subresultant and function-field recovery, all 48 coefficients of `P`, the
Newton data, the full discriminant factorization, squarefreeness, and every
coprimality assertion. The dependency-free verifier implements polynomial
arithmetic and Rabin irreducibility tests from scratch. The level-three Newton
script builds the tower equations in SymPy and delegates the two nested
resultants to PARI, providing a cross-system check of the `(27,34)` Newton
edge. The full level-three script additionally strips the vertical content,
certifies the simple discriminant divisor, leading and denominator guards,
and the depth-three group lemma. The dependency-free iterate checker verifies
every strict Newton-edge and reconstruction-dominance inequality for 30
levels.

## 12. Priority and limitations

The closest public monodromy paper explicitly states only
`Mon(F_0 o F_0) <= S_3 wr S_3` and calls its exact group a natural next
computation. The detailed, timestamped audit is in `PRIORITY_AUDIT.md`.

A separate four-variable construction already claims a different imprimitive
degree-eight group of order `192`; accordingly, this note does **not** claim to
be the first imprimitive or first non-symmetric Keller monodromy. It claims the
exact second- and third-iterate results and the specific realizations
`(9,W_2)` and `(27,W_3)`.

The natural stronger question is whether every iterate `F^m` has the full
iterated wreath product. Full-cycle inertia is proved above, but this paper
does not produce the required new single transposition at every level. The
separate certificates in `w4_search/RESULT.md` and `w5_search/RESULT.md`
settle `W_4` and `W_5`, respectively; the full arboreal statement remains
open.

## References and public comparison points

1. [MathOverflow 513387: cubic model and `S_3` monodromy of the announced map](https://mathoverflow.net/questions/513387/).
2. [MikhailSzh and Claude, weighted-lift monodromy note, audited commit](https://github.com/MikhailSzh/weighted-lift-galois/blob/9193c66385ce390f61a4e25d3f5255435bfa056a/note-weighted-lift.md).
3. [Juan M. G. H., quartic-resultant Keller map, audited commit](https://github.com/juanmgh3/quartic-resultant-keller-map/tree/640322133fa4bbe172e0ac95f3c485f2c86d8cea).
4. [König, Neftin, and Rosenberg, polynomial compositions with large monodromy groups](https://arxiv.org/abs/2401.17872).

## Assistance and responsibility statement

OpenAI's ChatGPT 5.6 Sol performed the exploratory algebra, source search,
proof drafting, and verification-code development under Alec Kriebel's
direction. Alec Kriebel is the named human author and has requested unusually
prominent disclosure that he is not qualified to validate the mathematics
independently. Readers should treat this as an AI-assisted research artifact
until specialists have checked it.
