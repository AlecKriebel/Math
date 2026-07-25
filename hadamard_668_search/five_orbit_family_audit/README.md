# Five-orbit anti-tensor family audit

## Result

A new structured placement family has been tested exactly on all five
certified shell-two profile orbits.  Write

```text
x = j mod 3,       z = j mod 6,
h_j = +1 for 0 <= j < 6 and -1 for 6 <= j < 12.
```

For channel `X` in `{A,B}`, the family is

```text
u_X(j,s)
  = P_X(x,s) + h_j F_X(z) G_X(s)                       (1)
```

over `F_3`, where:

- `P_X` is an arbitrary polynomial of total degree at most two;
- `F_X` is an arbitrary table `F_X:Z/6 -> F_3`;
- `G_X:F_3 -> F_3` is nonzero and nonconstant, considered up to a
  nonzero scalar.

The last convention loses nothing: a scalar multiplying `G_X` can be
absorbed into `F_X`.  There are 13 points in `P^2(F_3)`, one is the
constant-function line, and therefore there are exactly 12 new row
directions.  The channels choose directions independently, giving

```text
12^2 = 144 charts per profile.
```

For each fixed pair `(G_A,G_B)`, (1) is a 24-parameter linear feature
family.  The certified first placement digit is substituted exactly,
leaving affine spaces of dimension 4 through 9.  Every point in their
union is deduplicated and evaluated in all twenty exact second-placement-
digit quadratics.

The result is a complete exclusion of this family at digit two:

| profile | consistent charts | affine incidences | distinct digit-one points | genuinely new points | best digit-two rows | digit-two points |
|---|---:|---:|---:|---:|---:|---:|
| `h2-222222-0` | 144 | 93,636 | 93,053 | 93,049 | 17/20 | 0 |
| `h2-422220-0` | 144 | 214,326 | 95,499 | 94,770 | 16/20 | 0 |
| `h2-422220-1` | 144 | 259,524 | 131,949 | 131,220 | 17/20 | 0 |
| `h2-422220-2` | 144 | 225,990 | 111,537 | 110,808 | 18/20 | 0 |
| `h2-422220-3` | 127 | 86,265 | 85,071 | 85,065 | 18/20 | 0 |
| **total** | **703 / 720** | **879,741** | **517,109** | **514,912** |  | **0** |

Seventeen charts on the last profile are inconsistent already at digit
one.  Every other chart is completely enumerated through digit two.  There
are no timeout or solver-status inferences.

## Why this is a new family

The opposite component in (1) is a rank-one tensor in the six-class and
row-residue coordinates:

```text
H_X(z,s)=F_X(z)G_X(s).
```

This multiplicative class-by-row coupling is not the previously tested
additive opposite twist `F(z)+G(s)`, a helical pullback `H(j +/- s,s)`,
an affine- or quadratic-in-class control law, a half-turn/global fiber
permutation, or an `F_27` invariant submodule.  The half-turn, global
fiber, and class-control theorems also belong to a different (`h=0`)
profile sector.

The verifier makes the novelty quantitative.  It independently rebuilds
the seven earlier all-five linear-feature families and all 56 minimal
`F_27` submodules.  Only 2,197 of the 517,109 points lie in their combined
union.  Thus

```text
514,912
```

first-digit placements are new relative to every previously certified
all-five structured family.  Every one of those new points is also outside
all five proper fixed-common-multiplier supergroups from the July 2026
multiplier classification.  Their digit-two failure therefore adds
coverage not supplied by that literature result.

## Exact finish line and remaining-search estimate

Within (1), the remaining search through digit two is exactly zero: all
144 charts on each of the five profiles have been decided.

This does **not** materially shrink the unrestricted first-digit spaces.
Each profile has `3^36=150,094,635,296,999,121` first-digit placements.
Across five profiles, the points outside this one family still number

```text
5*3^36 - 517,109
  = 750,473,176,484,478,496.
```

That count is an honest warning against interpreting half a million exact
tests as convergence toward a Legendre pair.

The immediately larger rank-at-most-two anti-tensor extension is also not
a sensible flat census.  Fixing one two-dimensional row subspace per
channel gives `13^2=169` charts.  Before chart overlaps and exceptional
ranks, the generic first-digit dimension is about 18, corresponding to
roughly

```text
5 * 169 * 3^18 = 327,370,313,205
```

chart incidences—about 372,000 times this audit.  The next useful attack
would have to exploit the two missing equations at the `18/20` points to
solve for a second tensor component algebraically; enumerating rank-two
charts would be a regression to brute force.

## Claim boundary

- **Profile level:** the five inputs are the previously certified exact
  profile-zero representatives.
- **Digit level:** every member of (1) passing placement digit one has
  been tested at placement digit two.
- **Placement level:** no member passes digit two.  No primitive-nine
  placement is constructed, and placements outside (1) are not excluded.
- **`LP(333)` level:** no Legendre pair is constructed or excluded.
- **`H(668)` level:** no Hadamard matrix of order 668 is constructed or
  excluded.

## Reproduction

Run from `hadamard_668_search`:

```sh
python3 five_orbit_family_audit/verify_anti_tensor_family.py
```

NumPy is used automatically when available; there is a standard-library
fallback.  The accelerated reference run took 28.3 seconds and peaked at
182 MB resident memory on the 16 GB M1 Pro host.

The verifier reconstructs the charts, prior-family comparisons, multiplier
fixed sets, and all second-digit residuals.  It also performs detached
exact-Eisenstein replays.  Its semantic certificate hash is

```text
39de8bf9d6e60ee078e7710daa81d3546e519589a769bbd2c5579693c6203bef
```

and the compact pinned certificate is
`anti_tensor_family_certificate.json`.

The artifact SHA-256 hashes are:

```text
verifier source:
406a4d59120e445a3b3c4069282d12d223d8ca3225319f5a36c386b457f29e45

compact certificate file:
806efa26dd8d28c79223c969f41bcd085e2fc4865fb8647160d7dc6c58b405e9
```
