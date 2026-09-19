# Statement contract

## The intended final mathematical statement

The specific group must be the paper's BCH group on a carrier proved equivalent
to

```lean
Fin 31 → ZMod (1009 ^ 1689)
```

The coordinate operations define an **additive Lie ring**, not the final group
multiplication. The final multiplication must be the validated BCH product for
the actual weighted Lie bracket. Declaring the ordinary additive group on these
coordinates to be the answer is forbidden by this contract and not done in the
source.

The final assertions are, with the same explicitly defined `G` and its proved
BCH `Group` structure:

```lean
Nat.card G = 1009 ^ 52359
Nat.card (MulAut G) = 1009 ^ 52359
```

`MulAut` must be mathlib's ordinary full multiplicative automorphism type. The
second assertion cannot concern only selected exponentials, a Sylow subgroup,
inner maps, central maps, or an isomorphic custom type without a proved
surjective equivalence to **all** `MulAut G`.

`Kourovka.Challenge.ExactOrders` states this target for a supplied `Group G`.
It does not supply that group or assume that the target is true.
`Kourovka.Challenge.NotebookAffirmative` separately states the standard-definition
existence claim with an odd prime, a positive exponent, finiteness and
nontriviality. Neither proposition has a closed proof in this package.

## Present concrete definitions

`Ambient.V R` is `Fin 31 → R`. `RawCoefficients` fixes the integral raw,
unnormalized transvectants in the original order

```
h,e,f,U0..U6,V0..V4,W0..W6,T0..T2,R0..R4,Z0.
```

`TableCertificate`, `Ambient.IntData`, the finite-check shards, and
`Ambient.Lie` contain proof attempts connecting the formula, the original
export, and the bilinear Lie bracket on arbitrary vectors.

`Lattice.P` gives the adapted basis change starting with
`x=h`, `y=e+f+U1+V0+R2`, `t=U0`, followed by the published remaining basis order.
`weight` is `(0,0,1,2,...,2)` and `degree` is `2+weight`.
`Lattice.embed` is the actual integer map
`P ∘ diag(1009^(2+weight))`, not an unspecified embedding. The 199-term scaled
bracket `Lattice.LB` is connected to the ambient bracket by `embed_bracket` and
has a Lie-ring proof draft. This does not assert that the intermediate lattice
A is closed under the original bracket.

`Finite.LAt i` is the actual ell-coordinate carrier
`Fin 31 → ZMod (1009^i)` with the reduced `LB` bracket.
`Finite.lieRingAt` and `lieAlgebraAt` are explicit structure values.
`Finite.Padic.quotientEquiv` (see its source namespace) connects the p-adic
coordinate module modulo the actual reduction kernel with these coordinates;
the kernel theorem identifies multiplication by `1009^i`.
The surrounding source has not yet assembled the whole rational common-space
lifting argument used for all automorphisms.

`Finite.FullAutomorphisms.RingAut i` uses ordinary `LieEquiv Int` and is intended
to mean **all** additive bracket-preserving bijections. Its explicit equivalence
to scalar-linear maps and invertible bracket-preserving entries does not count
that set. The passage between this Lie-ring type and ordinary **group** `MulAut`
is still missing.

## Identity with the paper and exact data

The three original coefficient/pivot files remain byte-identical to the
previously recorded publication-tag files. External Python reconstruction also
compares the newly written Lean data literals with those exact originals.
Those external checks and hashes are evidence of provenance, **not** a Lean
proof of semantic agreement. The attempted formal connections are the actual
raw/table, embedding, reduction, and matrix-definition theorems, which still
need successful elaboration and review.

The actual DOI archive has not been acquired. See `reference/provenance.json`
for the publication tag, the historical paper copies, and the identity limits.
The latest source-only instruction is preserved separately.

## Acceptance condition

Before calling this complete, construct the actual BCH `G`, discharge every
mathematical dependency, and prove the two assertions with ordinary `MulAut`.
Then inspect their exact elaborated binders and instances, obtain actual
transitive axiom reports, and freshly recheck the full import closure. A
successful current-source build alone is not this acceptance condition.
