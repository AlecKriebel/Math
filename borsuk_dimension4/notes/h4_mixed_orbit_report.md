# Exact mixed-orbit radial elimination for the golden H4 families

**Checkpoint:** 2026-08-01T17:35:27-07:00
**Discovery discipline:** exact first-principles computation only; no web or
literature search was used.

## Result

Let \(V\) be the 120-vector golden root orbit, scaled so that every vector has
squared norm \(16\).  Let \(W\) be the 600-vector orbit of scaled tetrahedron
centroids from the dual-orbit audit, with squared norm

\[
 N=112+48\sqrt5.
\]

The most symmetric mixed-orbit constructions do not give a Borsuk
counterexample:

1. For every \(r>0\), the diameter graph of the full radial union
   \(V\cup rW\) is two-colorable.
2. Choose either orientation of every one of the 60 antipodal lines in \(V\),
   and independently choose either orientation of every one of the 300 lines
   in \(W\).  For every one of these \(2^{360}\) choices and every \(r>0\),
   the diameter graph of the resulting 360-point radial union is
   five-colorable.
3. The two intermediate cases, with one full antipodal orbit and one oriented
   projective representative set, are also five-colorable for every \(r>0\).

Thus all four full/projective occupancy modes are eliminated for every radial
ratio.  This is a family-wide negative theorem for symmetry-preserving radial
unions.  It does **not** eliminate arbitrary vertex deletions from the mixed
720-point union, where non-extreme within- or cross-product levels may become
diameters.

The dependency-free exact checker is
`borsuk_dimension4/search/h4_mixed_orbit_search.py`.

## 1. Exact construction and the complete cross table

Write \(s=\sqrt5\).  The root coordinates are the exact 120 vectors already
audited in the single-orbit searches.  The 600 dual vectors are

\[
 w_Q=\sum_{v\in Q}v,
\]

where \(Q\) runs over the 600 four-cliques in the root relation
\(\langle v,v'\rangle=4+4s\).  These are four times the actual centroids.

Set

\[
 C=28+12s.
\]

Exact arithmetic gives \(N=4C\).  Moreover,

\[
 \langle v,w_Q\rangle=C \quad\Longleftrightarrow\quad v\in Q.
\]

Thus the positive extreme cross relation is exactly the root--tetrahedron
incidence graph.  Every dual vector is incident with four roots and every
root with twenty tetrahedra.

The complete \(120\times600\) cross-product table is:

| product | pair count | degree at a root | degree at a dual point |
|---:|---:|---:|---:|
| \(-28-12s\) | 2,400 | 20 | 4 |
| \(-20-12s\) | 2,400 | 20 | 4 |
| \(-24-8s\) | 3,600 | 30 | 6 |
| \(-16-8s\) | 7,200 | 60 | 12 |
| \(-12-4s\) | 7,200 | 60 | 12 |
| \(-4-4s\) | 7,200 | 60 | 12 |
| \(-8\) | 2,400 | 20 | 4 |
| \(0\) | 7,200 | 60 | 12 |
| \(8\) | 2,400 | 20 | 4 |
| \(4+4s\) | 7,200 | 60 | 12 |
| \(12+4s\) | 7,200 | 60 | 12 |
| \(16+8s\) | 7,200 | 60 | 12 |
| \(24+8s\) | 3,600 | 30 | 6 |
| \(20+12s\) | 2,400 | 20 | 4 |
| \(28+12s\) | 2,400 | 20 | 4 |

The checker reconstructs every entry and verifies regularity on both sides.
Antipodality explains the symmetry of the table.

## 2. Why every projective orientation has the same extrema

Choose a deterministic representative of each antipodal line.  On a
maximum-absolute-product relation, label an edge by the sign of the dot
product of its two representatives.  Changing representatives switches all
edge signs incident with the changed vertex.  The product of signs around a
cycle is therefore switching-invariant.

The three relevant maximum absolute products are

\[
 L_A=4+4s,\qquad L_B=104+48s,\qquad C=28+12s.
\]

The exact checker contains the following negative cycles.  Indices refer to
the lexicographically ordered canonical root lines, canonical dual lines, and
their concatenation, respectively.

| signed graph | cycle | sign word | product |
|---|---|---:|---:|
| root lines | \(0,2,12,13,3,0\) | `--+-+` | \(-1\) |
| dual lines | \(0,3,7,56,97,57,131,49,137,129,55,133,53,99,59,0\) | `-+-+++++++++++-` | \(-1\) |
| root--dual | \(0,70,5,62,11,82,10,63,4,71,0\) | `---++++--+` | \(-1\) |

Every switching leaves each cycle product negative, so every switching has
at least one negative edge in each of the three maximum-absolute relations.
No product has larger absolute value.  Hence **every** independent choice of
the 360 orientations has the same minima

\[
 u=-4-4s,\qquad t=-104-48s,\qquad c=-28-12s.
\]

This switching-cycle argument is stronger than a sample over hemispheres: it
simultaneously handles all \(2^{360}\) orientation choices, including choices
not induced by a linear functional.

## 3. Complete radial envelope

For a root relation \(u\), a dual relation \(t\), and a cross relation \(c\),
the squared distances at radial ratio \(r\) are

\[
 A_u=32-2u,
 \qquad B_t=2r^2(N-t),
 \qquad X_c=16+Nr^2-2cr.
\]

Consequently every possible radial tie, including the non-extreme levels
that can arise after deletions, is parametrized exactly by

\[
\begin{array}{rcl}
 A_u=B_t&\Longleftrightarrow&(N-t)r^2+u-16=0,\\
 A_u=X_c&\Longleftrightarrow&Nr^2-2cr+2u-16=0,\\
 B_t=X_c&\Longleftrightarrow&(N-2t)r^2+2cr-16=0.
\end{array}
\]

Together with the seven root products, thirty dual products, and fifteen
cross products, these three equations are a symmetry-reduced complete list
of all candidate radial ratios.  Each is quadratic over
\(\mathbb Q(\sqrt5)\), hence has a rational norm polynomial of degree at most
four.  The checker exposes these formulas as `tie_equations`.

For the full/projective radial families, the switching cycles reduce the
upper envelope to the following five curves:

\[
\begin{array}{c|c}
\text{occupancy}&\text{within-orbit maximum}\\ \hline
A\text{ full}&A_F=64\\
A\text{ projective}&A_P=40+8s\\
B\text{ full}&B_F=(448+192s)r^2\\
B\text{ projective}&B_P=(432+192s)r^2
\end{array}
\]

and, in every mode,

\[
 X=16+(112+48s)r^2+(56+24s)r.
\]

Put \(g=7+3s\) and \(h=20+9s\).  The eight pair crossings are listed below.
The rational intervals are certified by exact sign evaluation.  The last
column gives the primitive rational norm polynomial \(P(r)\); its intended
positive root is the unique root in the displayed interval.

| crossing | exact equation over \(\mathbb Q(s)\) | isolating interval | \(P(r)\) |
|---|---|---:|---|
| \(A_P=X\) | \(2gr^2+gr-(3+s)=0\) | \((253/1000,254/1000)\) | \(4r^4+4r^3-5r^2-3r+1\) |
| \(B_P=X\) | \(2hr^2-gr-2=0\) | \((264/1000,265/1000)\) | \(5r^4+5r^3+39r^2-7r-1\) |
| \(A_F=X\) | \(2gr^2+gr-6=0\) | \((280/1000,281/1000)\) | \(4r^4+4r^3-41r^2-21r+9\) |
| \(B_F=X\) | \(6gr^2-gr-2=0\) | \((260/1000,261/1000)\) | \(36r^4-12r^3-41r^2+7r+1\) |
| \(A_F=B_F\) | \(gr^2-1=0\) | \((270/1000,271/1000)\) | \(4r^4-14r^2+1\) |
| \(A_F=B_P\) | \((27+12s)r^2-4=0\) | \((272/1000,273/1000)\) | \(9r^4-216r^2+16\) |
| \(A_P=B_F\) | \((56+24s)r^2-(5+s)=0\) | \((256/1000,257/1000)\) | \(64r^4-80r^2+5\) |
| \(A_P=B_P\) | \((54+24s)r^2-(5+s)=0\) | \((259/1000,260/1000)\) | \(9r^4-75r^2+5\) |

The certified ordering gives the entire upper envelope:

| root mode | dual mode | crossing order | diameter classes |
|---|---|---|---|
| full | full | \(XB_F<AB_{FF}<AX_F\) | \(A/B\); cross hidden |
| full | projective | \(XB_P<AB_{FP}<AX_F\) | \(A/B\); cross hidden |
| projective | full | \(AX_P<AB_{PF}<XB_F\) | \(A/X/B\) |
| projective | projective | \(AX_P<AB_{PP}<XB_P\) | \(A/X/B\) |

For example, in the projective/projective case the first genuine transition
is \(A_P=X\), the cross relation is uniquely maximal until \(B_P=X\), and
the direct \(A_P=B_P\) crossing is strictly below it.  The quartic norm
polynomials are supplementary fingerprints; the quadratic equations over
\(\mathbb Q(s)\) plus isolating intervals specify the roots exactly.

## 4. Five-colorability at every regime and tie

Only a few graph facts are needed.

1. The projective root extreme relation
   \(|\langle a,a'\rangle|=4+4s\) has the explicit five-line-coloring
   already used in the root audit.  It has five classes of size twelve.
2. The full 600-vertex oriented dual relation
   \(\langle b,b'\rangle=-104-48s\) has an explicit three-coloring with
   class sizes \(258,231,111\).  Every oriented projective representative set
   inherits it.
3. A cross-only diameter graph is bipartite.
4. At an \(A_P=X\) transition, first five-color the root relation.  Every
   dual vertex has at most four extreme cross neighbors, so it can be assigned
   a missing color.  There are no dual--dual diameter edges at this radius.
5. At the projective \(B_P=X\) transition, use the three dual colors and give
   every root a fourth color.  At the full \(B_F=X\) transition, two-color the
   antipodal matching in \(W\) and give every root a third color.
6. At a direct \(A=B\) transition the cross curve is strictly lower.  The
   graph is a disjoint union of the corresponding within-orbit graphs:
   matchings in a full orbit, the five-colored root relation in a projective
   root orbit, or the three-colored dual relation in a projective dual orbit.

This proves the claimed uniform five-color bound without enumerating the
\(2^{360}\) switchings.

For an additional replay check, the script constructs explicit colorings of
the two transition graphs for the canonical representatives.  Their SHA-256
fingerprints are

```text
A--cross: d5c6af46a62c1ca46b4179ced4e68227d0cea8cae6feec99807937becf2a96a1
B--cross: d00d9ba2d5044df1100e9194e64c3ea4b00a349a45589963f6d4e2e5e7ad108b
```

The full dual three-color string has fingerprint

```text
4db72692637cb646a136b858fcc0f060b7a9b8417edca85a9343ad466cf5cba4
```

Every certificate is checked edge by edge after rebuilding the exact
coordinates.

## 5. Reproduction

From `/Users/alec/Documents/Math-borsuk4`, run

```text
python3 borsuk_dimension4/search/h4_mixed_orbit_search.py --verify
```

The audit uses only the Python standard library and the two exact orbit
constructors already in the repository.  It takes about three seconds on the
project machine.  Its final line is

```text
all_full_and_all_projective_oriented_radial_unions_five_colorable=true
```

No floating-point comparisons are used in the proof.  The displayed decimal
scale information is represented internally by exact rational intervals and
exact signs in \(\mathbb Z[\sqrt5]\).
