# Independent adversarial review of the proposed covering-priority issue

**Result: the proposed covering issue survives independent falsification.**
The exact k404 theorem in PR255 follows from two earlier publicly available
results. This conclusion does not depend on extending the main theorem of a
paper with a different parity, and does not infer a theorem from numerical
experiments. The antipedal factor is explicitly proved for every centrally
paired elliptic-caustic orbit in the earlier paper. The prior k204 proof supplies
the needed pedal factor at precisely the target parity. A positive formula in
the earlier paper, or an elementary geometric argument, removes the generic
pedal theorem's possible exceptional denominator at either focus.

I read the complete immutable candidate proof, the complete original PR250
proof, and the complete original deposited `main.tex` before reaching this
conclusion. I did not read the other new priority reviewers' conclusions. I
independently fetched provider records and original source files, verified their
checksums, and checked thirteen identities with a fresh symbolic program.
No Git, PR, tracker, or publication mutation was performed.

## 1. Exact object and hypothesis map

Use `A = area(P)`, `p = area(Q_F)`, and `q = area(U_F)`, with signed shoelace
area and trajectory order. Here `Q_F` projects the fixed **original focus**
onto the consecutive original orbit side lines. `U_F` intersects the lines
through consecutive original vertices perpendicular to their focal rays.
The prior paper defines these same objects; its equations for the antipedal
sides are `(P_i-F)·(X-P_i)=0`. No outer-pedal or contact polygon is substituted.
Its outer tangent area is a separate quantity that is unnecessary for this
transfer.

Both earlier sources and the candidate use a fixed, strictly nested,
nondegenerate confocal elliptical caustic in a noncircular ellipse. Write
`alpha=a²`, `beta=b²`, `c²=alpha-beta`, and `0<lambda<beta`. Fix a primitive
least period `N=2m=2 mod4` and any allowed coprime winding `tau`, oriented with
`0<tau<N/2`. Then `tau` and `m` are odd. Stachel's canonical contact increment
is `delta=4K tau/N`, which lies strictly between zero and `2K`. The vertex
index shift by `m` is a Jacobi shift by `2K tau`, so

    P_(i+m)=-P_i.

This holds for every permitted star, as well as convex winding one. The prior
antipedal lemma requires central pairing, not `N=0 mod4`. It therefore applies
at the target parity without an additional conjecture. The main area-product
theorem in that paper does use `N=0 mod4`, but that restriction belongs to its
quarter-period permutation relating pedal and outer areas. That portion of
the argument is not imported here.

Changing focus from `c` to `-c` leaves the antipedal coefficient below unchanged.
The pedal coefficient from PR250 depends on `|F|²=c²`, so it is also unchanged.
Reversing trajectory order negates `A,p,q`, and hence preserves the quotient.
Repeating an already admissible orbit scales all three signed areas equally;
padding another primitive parity does not satisfy this theorem's hypotheses.

## 2. Checkable independent reconstruction of the antipedal factor

The earlier [original deposited source](https://zenodo.org/records/23079799)
contains an opposite-edge lemma that gives

    q = R A,
    R = [alpha beta (3beta-alpha)+lambda(alpha-beta)²]
        /[2alpha beta(beta-lambda)].

The argument has no division by a total area and allows `R=0`.
I checked its algebra from the actual focal endpoint coordinates, rather
than merely reading the lemma statement.

To see why the grouped area formula applies to crossed polygons, translate
the focus to the origin. A side with normal `u=P-F` has equation
`u·Z=|u|²` and may be parameterized as `Z=u+s Ju`, where `J` is positive
quarter rotation. At its next intersection with the side having normal `v`,
the coordinate is `( |v|²-u·v )/det(u,v)`. Collecting the preceding and
following intersection contributions on every side gives the edge summand

    E(u,v) = [|u|² |v|²-(|u|²+|v|²)(u·v)/2]/det(u,v).

This derivation uses the signed cyclic determinant and finite consecutive
intersections only. It does not require a simple antipedal boundary.

For an edge with boundary endpoint parameters `t-epsilon,t+epsilon`, put
`U=alpha sin²t+beta cos²t`, `z=c cos t`, `C=cos epsilon`, `S=sin epsilon`.
Strict caustic tangency gives `S²=lambda U/(alpha beta)`, and the chosen lift
has `S,C>0`. Direct endpoint coordinates give

    det(P,Q)=2ab S C,
    det(P-F,Q-F)=2b S(aC-z),
    (aC-z)(aC+z)=U(beta-lambda)/beta > 0.

Both focal determinants are nonzero. The grouped numerator reduces to
`2 S² H(c)`, where

    H(c)=(2beta-U)(a-zC)²+U(U-beta)S².

The opposite edge replaces `c` by `-c`. Combining the two edge terms and
dividing by the original edge determinant yields

    [E(P-F,Q-F)+E(-P-F,-Q-F)]/det(P,Q)
       =2-(alpha beta-(alpha+beta)lambda)U
             /[alpha beta(beta-lambda)].

The elementary boundary identity

    det(P_i,P_(i+1)) cos(2t_i)
       =ab[sin(2theta_(i+1))-sin(2theta_i)]/2

telescopes over the closed ordered trajectory. Opposite edges have the same
determinant and the same `U`. Consequently their weighted `U` sum is
`(alpha+beta)A/2`, while their unweighted determinant sum is `A`.
Summation proves the displayed `q=R A` for **any even centrally paired
trajectory**, including a coprime star. No quarter-period argument or area
product theorem occurs in this proof.

`fresh_transfer_checks.py` reconstructs the original endpoint determinants,
focal-distance identities, grouped antipedal numerator, common-denominator
combination, caustic simplification, and weighted telescope as exact polynomial
identities. All their remainders are zero. The check does not sample phases
as a replacement for closure or central pairing.

## 3. The earlier pedal result has the needed parity and all-star scope

The complete [PR250 original proof at its immutable commit](https://github.com/AlecKriebel/Math/blob/ea34ca1dd8e2693b58f615aa2a4b45bc548cacc3/unsolved_math_prioritization/attempts/5100013/PROOF.md)
proves for every fixed real `M`

    area(Q_M)=(c0+c2|M|²) A,

with `c0>0` and real phase-independent `c2`, for primitive `N=2 mod4`, including
every permitted coprime star. This is an identity even when the left side is
zero. The natural-domain qualification concerns dividing by that pedal area,
not the preceding identity.

I checked that proof's analytic mechanism for this transfer. Central pairing
first cancels the linear-in-`M` area terms; the quadratic terms telescope to
a radial coefficient. The general-even meromorphic pedal trace has at most
simple poles: each pedal vector is even and has at most a double pole at a
zero of `dn`, while the difference of its regular neighbors is odd. Singular
vertices are separated by `m>=3` indices here, and hence are not adjacent.
The radial identity supplies the imaginary anti-period after complexification.
Primitive arithmetic gives real period `h=2K/m`. On the quotient torus the
trace and `sum_j dn(u+j delta+K)` have the same two possible simple poles,
and the latter has nonzero residues from the two equal central terms.
Residue matching leaves a holomorphic constant which the anti-period forces
to zero. Finally `K+v=((m+tau)/2)h` is an integer multiple of `h` exactly at
the required odd-`m` parity. This aligns the pedal trace with the original
area trace. There is no assumption of phase invariance in proving that trace
identity, and no convexity premise.

Specialize the earlier identity to either fixed focus:

    p = d_F A,      d_F = c0+c2(alpha-beta).

Thus both foci have the same phase-independent coefficient. It remains to
check `d_F != 0`; overlooking that condition would invalidate the quotient
transfer for arbitrary `M`.

## 4. Two independent ways to remove the denominator issue

First, the same original Zenodo source already proves, in its focal-pedal
lemma, for every centrally paired orbit,

    p = sqrt(lambda) alpha(beta-lambda)/beta
          * sum_i sqrt(W_i-lambda)/W_i,
    W_i=beta cos²theta_i+alpha sin²theta_i.

All factors are strictly positive: `W_i>=beta>lambda>0`. This applies to the
target parity and all stars, because the lemma uses the velocity telescope
and opposite vertices; its proof does not use the later quarter-period
permutation. I independently checked its frame-bracket simplification,
opposite-vertex local sum, velocity telescope numerator, and final coefficient
as exact identities. It supplies `p>0` directly from prior explicit formulas.
Since `A>0` for the selected caustic-left orientation, `d_F=p/A>0`.

Second, a short geometric argument would suffice even without that positive
formula. Either focus is strictly inside the caustic. Write its foot on a
caustic tangent as `Q_F-F=rho n_hat` with outward unit normal `n_hat`; the
support distance `rho` is strictly positive. In the canonical real contact
parameter, the outward normal angle increases strictly and advances by `pi`
over `2K`. As `0<delta<2K`, each consecutive normal angle increment lies in
`(0,pi)`. Therefore each consecutive determinant of `Q_F-F` is positive.
The signed shoelace sum is positive after translation back to `F`, even for
a star. This is an elementary domain check, not a new unsupported all-period
invariance theorem.

The same caustic-left geometry gives `det(P_i-F,P_(i+1)-F)>0`; hence all original
focal-antipedal intersections are finite. It also gives `A>0` with origin in
the caustic. No simplicity or unsigned-area interpretation is used.

## 5. Exact covering corollary and boundary tests

Combining the earlier results now gives the entire candidate conclusion:

    area(U_F)/area(Q_F)
      = R/[c0+c2(alpha-beta)],
    c0+c2(alpha-beta)>0.

The right side depends on the fixed billiard family and not its phase or the
choice of focus. A zero antipedal coefficient gives the defined quotient zero;
there is no division by the antipedal numerator. A negative numerator is
also retained as a signed value. Generic star zero circles for arbitrary
pedal centers cannot contain either focus, by the preceding strict positivity.
Limits `lambda=0`, `lambda=beta`, circular billiards, hyperbolic caustics,
and parity manufactured by repeated lists remain outside the target and
outside the imported statements. No unresolved extension is needed inside
the stated target domain.

This is an **actual covering corollary of prior explicit proven results**,
not merely a similar method, a product theorem divided by an unknown factor,
or an unproved extension of a theorem at the wrong parity. The candidate's
direct meromorphic antipedal derivation can still be a separately useful
proof, but cannot support framing this target as newly unresolved until that
derivation.

## 6. Independently verified source and chronology pins

`SOURCE_CHRONOLOGY_PINS.json` and the raw native/provider receipts preserve
the independently fetched responses. The record is submitted and has state
`done`. Both archive and PDF were fetched afresh and match the provider MD5
checksums and the earlier saved source bytes. All 43 source-archive member
SHA256 entries were verified, including the original deposited `main.tex`.

| Artifact or event | Pin or provider time |
| --- | --- |
| Zenodo record DOI | `10.5281/zenodo.23079799` |
| Zenodo record created | `2026-10-01T10:00:33.366348+00:00` |
| Zenodo record updated | `2026-10-01T10:00:56.046398+00:00` |
| Original source ZIP SHA256 | `6680bf0a3fd4cade6fabaf2061f88941c9d57776fe65f28bfb9e69acb8b39876` |
| Original deposited main.tex SHA256 | `7bdaae97eacd19214d46c175bc7d9d119d02af7a3593877ec49ef182fbeb8247` |
| Original PDF SHA256 | `34ff068237a7ebbd6ffa063f89717aae946bc4d27df6db23d4468b5bb52d3582` |
| PR250 original head | `ea34ca1dd8e2693b58f615aa2a4b45bc548cacc3` |
| PR250 native created and updated | both `2026-10-01T10:56:06Z` |
| PR250 Git author and committer dates | both `2026-10-01T10:55:54Z` |
| PR250 original proof SHA256 | `ac486431077ab33493c78dc83ce3940648a7121e72015da8563e4dc6fea7d124` |
| PR250 original proof native blob SHA1 | `db3f2a1dae892d978384e7448a4dbfe1d6331e7e` |
| Candidate original proof SHA256 | `b8edd78d03dac33a7be77837649eef7a8558900b3499774725174836fa54d462` |
| Candidate self-recorded source gate | `2026-10-01 11:12–11:15 UTC` |
| Candidate self-recorded substantive derivation | `2026-10-01 11:15–11:25 UTC` |
| PR255 original head | `a624d16a87c5ee67a3ab23621b891e5991794071` |
| PR255 Git author and committer dates | both `2026-10-01T11:46:46Z` |
| PR255 native created | `2026-10-01T11:49:58Z` |

Provider creation/update times and content-addressed source pins establish
the bounded public-source ordering used here. The Git author/committer dates
are self-assigned metadata, and the research-log intervals are author reports;
neither independently proves private discovery order. No worldwide-firstness
conclusion is made. In particular, a provider-created time should not be
described as the exact mathematical discovery time or as the exact upload
instant of an individual archive member. The earlier record's later update
is still before PR250 and the candidate's documented derivation.

## 7. Recommendation under the current goal

**Priority gate fails for a preprint framed as a novel resolution of an open
k404 problem. Mathematical validity is not rejected.** The strongest checked
classification is that the exact target was already a covering consequence
of these earlier public results, by the bounded chronology above.

The parent should record this finding and its exact transfer in the audit
of the currently eligible `claimed_solved` PR. If it corrects the source
classification to `already_solved`, the user's current goal explicitly skips
that status: no new result preprint, Zenodo deposit, tracker row, or merge
under this goal. There is no mathematical reason to reject the valid proof
as false. I leave all repository/PR disposition actions to the parent.

This audit's scientific task is complete, with no remaining transfer gap.
It does not replace the parent's full mathematical acceptance or establish
absolute historical priority of either source.
