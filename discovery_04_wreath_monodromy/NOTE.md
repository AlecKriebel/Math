# Full wreath-product monodromy for the square of an explicit Keller map

**Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI)**

Research draft, 21 July 2026. Not peer reviewed.

> Alec Kriebel is a complete amateur exploring the limits of AI-assisted
> mathematics and cannot independently verify the claims in this note. The
> argument and exact certificates are being released to make expert checking
> and rapid correction possible. No claim of guaranteed worldwide priority is
> made.

## Abstract

Let `F : C^3 -> C^3` be the newly announced noninjective polynomial map with
constant Jacobian determinant `-2` and generic geometric monodromy `S_3`. We
determine the geometric monodromy of its canonical self-composition. It is the
full imprimitive wreath product

```text
Mon(F o F) = S_3 wr S_3
```

in degree nine, of order `1296`. The proof is geometric. On the target line
`(1,2,s)`, an exact degree-nine eliminant has a one-edge Newton polygon at
infinity, giving a 9-cycle; its discriminant has a squarefree factor of
multiplicity one, giving a single within-block transposition; and the outer
cubic has a simple branch giving a transposition of the three blocks. An
elementary group lemma forces the full wreath product. Postcomposing `F o F`
by `diag(1/4,1,1)` gives a noninjective polynomial self-map of `C^3` with
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

**Theorem.** The map `G` has generic degree nine and

```text
Mon(G) = S_3 wr S_3 <= S_9,
|Mon(G)| = 6^3 * 6 = 1296.
```

The action has three blocks of size three, indexed by the intermediate points
in a generic fiber of the outer copy of `F`.

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

The remaining problem is to prove equality.

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

Its nine roots generically parametrize the nine points in the slice fiber.

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

In particular, the slice eliminant is irreducible over `C(s)`.

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
Section 2 gave the opposite upper bound. The theorem follows.

## 8. Full-cycle inertia for every iterate

The 9-cycle above is the second case of a uniform local calculation. Put
`u=1/s` and start from

```text
X_0 = (1,2,s).
```

Choose a compatible inverse tower `F(X_k)=X_(k-1)`. Write the leading growth
of its coordinates as

```text
x_k ~ const * s^(-a_k),
y_k ~ const * s^( a_k),
z_k ~ const * s^( c_k),
```

with `a_0=0` and `c_0=1`. If `t_(k+1)` is the next inverse-resolvent
parameter, its cubic is

```text
2 x_k t^3 - y_k t^2 + 2t - z_k = 0.
```

Provided `c_k>5a_k`, the lower Newton edge balances the first and last terms,
so

```text
t_(k+1) ~ const * s^((a_k+c_k)/3).
```

The reconstruction formulas then give

```text
a_(k+1) = (c_k-2a_k)/3,
c_(k+1) = 2(c_k-a_k).
```

The hypothesis persists. Indeed, for `rho_k=a_k/c_k`, the interval
`0 <= rho_k <= 1/6` is invariant because

```text
rho_(k+1) = (1-2rho_k)/(6(1-rho_k)),
```

whose image on that interval is `[2/15,1/6]` after the first step. In
particular `c_k>5a_k`, so no omitted term lies on the lower edge and no leading
coefficient cancels.

Now put

```text
A_k = 3^k a_k,   C_k = 3^k c_k.
```

These are integers satisfying

```text
A_0=0, C_0=1,
A_(k+1)=C_k-2A_k,
C_(k+1)=6(C_k-A_k).
```

The exponent of `t_m` is

```text
E_m / 3^m,  where E_m=A_(m-1)+C_(m-1).
```

For `m>=2`, `C_(m-1)` is divisible by three and `A_(m-1)` is congruent to one
modulo three. Hence `E_m` is never divisible by three. The first exponents are

```text
1/3, 7/9, 34/27, 178/81, ... .
```

At stage `m`, the local inverse field therefore has ramification index at
least `3^m`; the global degree is at most `3^m`, so it is exactly `3^m` and is
totally ramified. Over `C((u))` the extension is tame, and local inertia acts
as one `3^m`-cycle on the sheets. This proves the all-iterate statement.

As an independent check, nested PARI resultants for `m=3` produce a
degree-27 eliminant. After removing common vertical content, its lower Newton
edge is `(0,0)-(27,34)`, agreeing with the recurrence.

## 9. Independent arithmetic cross-check

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
specialization, the proof in Sections 4-7 determines geometric monodromy.

## 10. Verification

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
```

The symbolic verifier checks the Jacobian and collisions, the inverse
resolvent identities, the exact resultant, all 48 coefficients of `P`, the
Newton data, the full discriminant factorization, squarefreeness, and every
coprimality assertion. The dependency-free verifier implements polynomial
arithmetic and Rabin irreducibility tests from scratch. The optional
level-three script builds the tower equations in SymPy and delegates the two
nested resultants to PARI, providing a cross-system check of the `(27,34)`
Newton edge.

## 11. Priority and limitations

The closest public monodromy paper explicitly states only
`Mon(F_0 o F_0) <= S_3 wr S_3` and calls its exact group a natural next
computation. The detailed, timestamped audit is in `PRIORITY_AUDIT.md`.

A separate four-variable construction already claims a different imprimitive
degree-eight group of order `192`; accordingly, this note does **not** claim to
be the first imprimitive or first non-symmetric Keller monodromy. It claims the
exact self-composition result and the specific realization
`(9,S_3 wr S_3)`.

The natural stronger question is whether every iterate `F^m` has the full
iterated wreath product. Full-cycle inertia is proved above, but the required
new single transposition at every level is not; the full arboreal statement
remains open.

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
