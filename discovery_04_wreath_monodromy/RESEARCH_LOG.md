# Discovery 04 research log

Status: public research draft; not peer reviewed.

Author: Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.

## Acceptance bar

Discovery 04 must be qualitatively new rather than a smaller presentation of a
known consequence. It must have an exact proof or finite certificate, at least
two genuinely independent verification paths, and a source-specific priority
audit. No worldwide novelty guarantee is possible, especially while the public
record is changing hourly.

## Landscape audit, 21 July 2026

The following tempting targets were rejected before construction work:

- explicit Dixmier counterexample: already public in rank three;
- complete nonproperness locus, fiber stratification, and image of the announced
  map: already public in the Harrison and Naskrecki repositories;
- explicit Gaussian Moments counterexample: Christopher D. Long already gives
  a three-variable example on arXiv:2607.18186;
- smaller homogeneous or symmetric reductions: active dimension/sparsity race,
  explicitly outside the acceptance bar;
- the smooth-connected Nollet-Xavier condition: the announced map's
  nonproperness hypersurface is singular, so the hypothesis does not apply.

The surviving candidate is a new monodromy type. Existing audited examples in
dimension three have full symmetric monodromy `S_n`. Compositions have been
mentioned as a way to obtain fiber degrees `3^m`, but no source located in the
initial web, arXiv, MathOverflow, or public-GitHub sweep computes their exact
generic monodromy.

The closest public source is MikhailSzh and Claude, *The Antiderivative
Resolvent of the Weighted-Lift Family of Keller Maps*, repository commit
`9193c66385ce390f61a4e25d3f5255435bfa056a` inspected on 21 July 2026. It says
both that compositions give imprimitive groups with the exact groups
unresolved (Section 6) and, specifically, that determining the exact group of
`F_0 o F_0` is a natural next computation (Section 8). This is direct evidence
that the target was open in the nearest public work; it is not a universal
priority guarantee.

## Candidate construction

Let `F` be the announced three-dimensional map. Study the canonical
self-composition

```text
G = F o F.
```

The geometric degree is `9`, and the monodromy is a priori a subgroup of the
imprimitive wreath product `S_3 wr S_3` in its degree-nine action.

The inverse of `F` is controlled by the covering cubic

```text
C_(a,b,c)(t) = 2*a*t^3 - b*t^2 + 2*t - c.
```

For a simple root `t`, the corresponding preimage is

```text
y = -(b*t^2 + 3*c - 6*t)/(2*t^2)
x = t/(1-t*y)
z = (2*x - 3*x^2*y - c)/x^3.
```

If `(x,y,z)` is an outer preimage, the inner resolvent is simply

```text
2*x*r^3 - y*r^2 + 2*r - z.
```

Eliminating `t` on the target line `(a,b,c) = (1,2,s)` produces a degree-nine
polynomial `P(r,s)` with 48 terms.

## Geometric proof mechanism

The slice already has full wreath-product monodromy:

1. At `s = infinity`, after writing `u = 1/s`, the lower Newton polygon of
   `u^8 P(r,u^-1)` is the single edge from `(0,0)` to `(9,7)`. Its coprime
   slope denominator gives a tame inertia 9-cycle.
2. The exact discriminant factorization is

   ```text
   disc_r(P) = 2^38 (27s^2-28s+12)^8 A_12(s) B_22(s)^2,
   ```

   where `A_12` is squarefree and coprime to the other factors and to the
   leading coefficient `128s`. Inertia at any root of `A_12` is therefore a
   single transposition. It must lie within one three-sheet block.
3. The outer cubic has discriminant
   `-4(27s^2-28s+12)`. Inertia at either of its two simple discriminant roots
   projects to a transposition of the three blocks.
4. In a subgroup of `S_3 wr S_3`, a 9-cycle, a single transposition, and an
   element projecting to a block transposition force the full wreath product:
   the cube of the 9-cycle is a 3-cycle in every block; conjugating the single
   transposition by that cube generates one full block `S_3`; the 9-cycle
   moves it to all three blocks; and the block 3-cycle plus block
   transposition generate the top `S_3`.

Thus the slice monodromy, and hence the generic geometric monodromy of `F^2`,
is `S_3 wr S_3`, of order `6^3*6 = 1296`. This is now a proof, subject to
line-by-line external review of the Newton-polygon and discriminant-to-inertia
steps; it no longer depends on arithmetic specialization.

## All-iterate strengthening

The local calculation extends partially to every iterate. If an inverse tower
over `(1,2,s)` has coordinate growth exponents

```text
x_k ~ s^(-a_k), y_k ~ s^(a_k), z_k ~ s^(c_k),
```

then exact dominant-balance induction gives

```text
a_(k+1)=(c_k-2a_k)/3, c_(k+1)=2(c_k-a_k).
```

Writing `A_k=3^k a_k` and `C_k=3^k c_k`, the next inverse parameter has
exponent `(A_k+C_k)/3^(k+1)`, whose numerator is always `1 mod 3`. Therefore
the local ramification index of `F^m` at this infinity branch is `3^m`, so its
geometric monodromy contains a full `3^m`-cycle for every `m>=1`.

An independent nested-resultant calculation for `m=3` gives degree `27` and a
single lower Newton edge `(0,0)-(27,34)`, matching the recurrence. This does
not prove full iterated-wreath monodromy: a new single transposition at every
level is still missing.

## Level-three upgrade, 22 July 2026

The degree-27 calculation was extended from a Newton-edge cross-check to an
exact monodromy certificate. After removing `q`-content of `s`-degree 196,
the primitive eliminant has bidegrees `(27,48)`. Its discriminant has
`s`-degree 1612. The squarefree radical has degree 752, and the product `E`
of factors occurring with multiplicity exactly one has degree 76. Exact gcd
checks show that `E` is squarefree and avoids the degree-27 leading
coefficient and both levels of rational-reconstruction denominators.

Thus a root of `E` gives a literal transposition inside one of the nine
bottom blocks. The one-edge Newton polygon supplies a 27-cycle. Its ninth
power is a 3-cycle on every bottom block; conjugating the transposition first
by this power and then around the nine blocks generates the full kernel
`S_3^9`. The quotient on bottom blocks is the already-proved `W_2`, so

```text
Mon(F^3) = W_3 = S_3 wr S_3 wr S_3,
|W_3| = 6^13 = 13,060,694,016.
```

At this stage `W_4` was still open: a new deepest-level simple branch divisor
was required there. The next entry records the separate computation that
found it.

## Separate level-four certificate, 22 July 2026

A bounded-memory quotient-tower evaluator scanned the target line modulo
`p=1009`. At `s=801`, the lower discriminant norms are the units
`497,650,840`, while the deepest norm vanishes. Every cubic-leading and
rational-reconstruction guard is also a unit. Evaluation modulo `1009^2`
gives deepest-norm derivative `917`, so the zero is simple.

An independent audit tightened the localization and norm-valuation argument
and added a direct dual-number check on the unique vanishing inverse sheet:
the root path is `(803,282,899)`, the deepest point is `(727,885,561)`, and
`d Delta/ds=527` modulo 1009. Thus exactly one deepest cubic acquires a simple
double root, giving a single leaf transposition. With the all-level 81-cycle
and the proved `W_3` quotient, its conjugates generate `S_3^27`, hence

```text
Mon(F^4) = W_4 = S_3 wr S_3 wr S_3 wr S_3.
```

The full scan used about 15 MB, the strengthened verifier about 24 MB, and an
independent exact-determinant cross-check under 50 MB. The proof is published
separately in `w4_search/RESULT.md`; it is not folded into the level-three
paper.

## Separate level-five certificate, 25 July 2026

A depth-agnostic rank-\(81\) quotient-tower evaluator found a smaller
good-reduction certificate at \(p=23,s=3\).  The five discriminant norms are

```text
(10,22,10,4,0),
```

all leading and reconstruction guards are units, and the deepest norm has
derivative \(16\) modulo \(23\).  The unique rational vanishing path is
`(10,22,13,1)` and its direct sheet discriminant derivative is `18`.

A hostile implementation imported none of the quotient-vector arithmetic.
It rebuilt the ranks \(1,3,9,27,81\) with block regular-representation
matrices, checked every forward reconstruction and resolvent recovery, and
replayed the localization, norm-valuation, tame-inertia, and group steps.
Twelve fail-closed mutations passed.  The resulting single bottom
transposition, all-level \(243\)-cycle, and proved \(W_4\) quotient generate
the kernel \(S_3^{81}\), hence

```text
Mon_C(F^5) = W_5.
```

The proof is in `w5_search/RESULT.md`.  This is another finite-level theorem;
the all-iterate wreath equality remains open.

## Initial exact evidence

For each target below, the degree-nine polynomial is irreducible over `Q` and
PARI/GP 2.17.4 independently identifies its arithmetic Galois group as
transitive group `9T31`, of order `1296`, named
`[S(3)^3]S(3)=S(3)wrS(3)`:

```text
(1,2,3), (2,3,5), (1,1,2), (2,-1,3), (3,2,1).
```

At `s=-3`, the three good-prime factorizations have irreducible degree patterns

```text
p=13: (9)
p=61: (2,1,1,1,1,1,1,1)
p=19: (2,2,2,2,1).
```

A dependency-free verifier checks the displayed modular factorizations and
Rabin irreducibility certificates. GAP independently confirms that no proper
subgroup of the wreath product contains all three cycle types. These
arithmetic checks corroborate, but are not used by, the geometric proof.

## Candidate theorem and corollary

The geometric monodromy of `F^2` is the full imprimitive group
`S_3 wr S_3` of order `1296`. Consequently the normalized map

```text
(G_1/4, G_2, G_3)
```

is a unit-Jacobian polynomial self-map of `C^3` realizing the
non-symmetric pair `(9, S_3 wr S_3)`. It remains noninjective: the announced
three collision points all map under `F^2` to `(0,0,-1/2)`.

The repository-wide audit also found Juan M. G. H.'s separate four-variable
degree-eight construction claiming an imprimitive group of order `192`.
Accordingly, Discovery 04 must not be described as the first non-symmetric or
first imprimitive Keller monodromy; its novelty claim is the exact canonical
self-composition group and the all-iterate full-cycle inertia statement.

## Post-release hardening

The first repository release was committed at 21 July 2026, 18:44:48 UTC.
Before publication on the notebook site, external AI review identified two
places where a specialist would reasonably demand more detail. The revision
therefore adds:

- exact denominator resultants and a linear-subresultant certificate recovering
  `t` from `(r,s)`, which identifies the function-field tower and rules out an
  extraneous generic resultant branch;
- a local-field induction over `C((1/s))`, with the four coefficient
  valuations and every strict dominance inequality in the reconstruction
  formulas made explicit.

The checkers were expanded to cover both additions. A later revision enlarged
the theorem statement to the full third-level wreath product, backed by the
separate exact certificate described above.
