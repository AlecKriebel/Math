# General-theorem implication audit for PR200 / k115

Audit date: 2026-10-16 UTC. The initial challenge was frozen before the submitted proof was read. No other audit's conclusions were used. This is a bounded implication audit, not a certification of novelty, firstness, historical completeness, or author independence.

## Finding

The analytic product step has a complete short specialization of classical theta addition. It does **not** require a new elliptic norm theorem. The specialization, with every substitution, is given below and includes the exceptional primitive four-period case automatically.

In the inspected older geometric sources, I did **not** establish an already-published theorem that carries the entire target dictionary: successive tangents to the original ellipse, their intersections Q, and ordinary distances from Q to the original foci. The close angle, pedal, inverse, and polar results concern other functionals. Replacing the missing dictionary with an unproved equivalence would merely transfer the central task.

The strongest verified conclusion is therefore two-part: a classical analytic specialization is available; an earlier geometry-level proof or equivalent previously proved invariant was not established in this source set. This does not justify either an absolute novelty claim or an assertion that the whole target was already proved in 2003/2020.

## Target and geometric dictionary

Fix `E: x²/a²+y²/b²=1`, `a>b>0`, and a proper confocal elliptic caustic with semiaxes `alpha,beta`, where `a²-alpha²=b²-beta²=lambda>0`, `alpha²-beta²=c²=a²-b²`. The claim concerns a primitive billiard of least period `N=4n` and all coprime windings. For consecutive vertices P_i, Q_i is the intersection of their tangents to E. The focus is `F=(c,0)` or `(-c,0)` of E.

Stachel's canonical parametrization, [arXiv v2 Theorem 2, equation (4.10), PDF p.11](https://arxiv.org/pdf/2105.03624v2), gives, in modulus notation `k=c/alpha`,

```
P(u)=(-a sn u, b cn u),
a=alpha dn(v)/cn(v),  b=beta/cn(v),
delta=2v=4K tau/N,  gcd(tau,N)=1,  0<tau<N/2.
```

Solving the two actual tangent equations at `u-v,u+v` gives

```
Q(u)=(-A sn u, B cn u),
A=a dn(v)/cn(v)=a²/alpha,
B=b/cn(v)=b²/beta.
```

Consequently `diag(alpha/a,beta/b) Q(u)=P(u)`. This is an exact affine correspondence, with a fixed phase shift in the actual Q list. It is not an isometry. In particular,

```
A²-B² = c² [1-lambda²/(alpha² beta²)].                 (D1)
```

Thus the Q locus does not have the original foci for any proper pair. Its major axis can even be vertical for the larger allowed star winding. At `lambda=alpha beta`, the locus is a circle (the primitive four-period case). Theorems about a confocal billiard inscribed in the Q locus cannot be imported with the original foci. The affine correspondence also changes the Euclidean distance functional.

## Complete classical theta specialization

Let `q=exp(-pi K'/K)` and `Theta(u)=theta_4(pi u/(2K),q)`. The standard theta addition formulas and theta definitions of sn give

```
1-k² sn²u sn²w
 = Theta(u+w) Theta(u-w) Theta(0)² / [Theta(u)² Theta(w)²].   (T1)
```

For precise checked sources, use [DLMF 20.7.9](https://dlmf.nist.gov/20.7.E9), its squared-theta identities [20.7.1–20.7.5](https://dlmf.nist.gov/20.7), and [22.2.2–22.2.4](https://dlmf.nist.gov/22.2). The displayed form (T1) is an algebraic rearrangement of those formulas, not a k115 statement quoted from DLMF. DLMF's addition-formula notes point to Lawden (1989), section 1.4, and Whittaker–Watson (1927), pp.487–488; these books were not independently read here.

Suppose translation by delta on the real circle modulo 2K has finite order m. If `w` belongs to that translation orbit, the factors `Theta(u+j delta+w)` and `Theta(u+j delta-w)` separately permute the same list as `Theta(u+j delta)`. Because Theta has real period 2K,

```
prod_(j=0)^(m-1) [1-k² sn²(u+j delta) sn²w]
 = [Theta(0)/Theta(w)]^(2m).                             (T2)
```

For real arguments there are no Theta zeros; the [standard theta product, DLMF 20.5.4](https://dlmf.nist.gov/20.5.E4), shows positivity. Thus no pole limiting argument is concealed in this real-variable cancellation. Formula (T2) is a general product consequence of (T1), derived in this audit. It was not located as a separately named older k115 theorem.

The target-specific bridge is the following coefficient identity. Put `r=cn(delta)/dn(delta)`, `M=B²+c²>0`, and `s=sn u`. From the displayed A,B above and Jacobi double-angle identities,

```
|Q(u)-F|² = M(1+k s)(1+k r s).                          (T3)
```

Here is an exact coefficient check rather than a numerical assumption. Put `t=sn²v`, `q_v=1-t`, `U=1-2k²t+k²t²`, and `V=1-2t+k²t²`. Direct substitution gives `M=alpha² U/q_v²`, `A²-B²=alpha² k² V/q_v²`, and the double-angle identities give `r=V/U`. Finally `U+V=2q_v(1-k²t)`. Thus `M k(1+r)=2Ac` and `M k²r=A²-B²`, which match every coefficient of `B²+c²+2Ac s+(A²-B²)s²` and prove (T3). Pairing the two foci gives

```
H(u)=|Q(u)-F|² |Q(u)+F|²
    = C_v dn²u [dn²(delta)-k² cn²(delta) sn²u],
C_v = M²/dn²(delta)>0.                                 (T4)
```

For `N=4n`, set `m=N/2=2n`. The winding tau is odd, delta has order m modulo 2K, and `n delta=K (mod 2K)`. Set `w=K-delta`, which therefore lies in the same finite orbit. The quarter-period identity `sn(K-delta)=cn(delta)/dn(delta)` turns the last bracket in (T4) into

```
dn²(delta) [1-k² sn²u sn²w].                            (T5)
```

Also `dn(u+K)=k'/dn(u)` gives `prod_j dn²(u+j delta)=(k')^m`. Formula (T2) now yields the explicit positive constant

```
prod_(j=0)^(m-1) H(u+j delta)
 = [C_v k' dn²(delta) (Theta(0)/Theta(K-delta))²]^m.     (T6)
```

The actual N points satisfy `Q(u+(j+m)delta)=-Q(u+j delta)`. Thus the square of the one-focus ordinary product is exactly the left side of (T6); positivity fixes its square root, and the same antipodal pairing gives equality of the two focal products. No assumption about the Q locus's foci occurs. At `N=4`, `delta=K`, so `w=0`; all formulas remain valid. Coprime star windings merely permute the finite orbit.

This is a full analytic implication, not an analogy. Its historical limit is equally explicit: (T3)–(T4) are the geometric/focal bridge supplied by the present problem, rederived here after reading the submitted proof. The old theta identities by themselves do not assert that bridge. They show that the proof method and final cancellation are classical; they do not establish an earlier occurrence of the entire geometric theorem.

## Literal older geometric theorems and implication gaps

| Primary source and exact location | What was tested | Status and exact missing bridge |
|---|---|---|
| [Akopyan–Schwartz–Tabachnikov, arXiv 2001.02934v2](https://arxiv.org/pdf/2001.02934v2), Theorems 1–3, PDF pp.2–3; Theorem 6 p.7; section 6 pp.7–10 | Outer angle cosine product, odd-period area ratio, circle/concentric-ellipse angle products, and their grid generalizations | These are actual theorems, but none states the original-focus Q-distance product. To use one requires an explicit expression for that product in terms of those invariants and fixed pair parameters. No such published expression was established. The outer-angle theorem covers the right polygon but a different metric quantity. |
| [Bialy–Tabachnikov, arXiv 2001.08469v2](https://arxiv.org/pdf/2001.08469v2), Theorem 2.2 p.3; Theorem 3.3 pp.5–6; Theorem 4.1 pp.6–7; Lemma 4.2 and Theorem 4.3 pp.7–11; [published PDF](https://par.nsf.gov/servlets/purl/10408490), pp.1349–1353 | General billiard support-function sums; outer cosine product; pedal sums; focal-to-side integral; a 4-divisible center-pedal radius product | The correct center-pedal radius product accounts for the basic dn norm. It does not supply the second factor in (T4). Q is neither that pedal point nor a confocal billiard vertex with the required foci. The literal focal point-product statement has a point/line mismatch discussed below; its proof concerns distances to sidelines. |
| [Reznik–Garcia–Koiller, arXiv 2004.12497v11](https://arxiv.org/pdf/2004.12497v11), Table 2 PDF p.5; [published Table 2 p.345](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf) | Whether the source itself attributes an existing proof of k115 | Both inspected rows specify the outer-vertex focal product and `N=0 mod4`, with `?` in the proof column. This records the listed conjecture/status in those versions; it does not show current openness or exclude an unnoticed corollary. |
| [Roitman–Garcia–Reznik, arXiv 2103.11260v3](https://arxiv.org/pdf/2103.11260v3), Theorems 1–2 PDF pp.4–6, Corollary 1 p.7, Appendix A pp.8–11 | Focus polarity, limiting points, bicentric pedal and inverse polygons | The source proves a bicentric angle sum and limiting-point pedal perimeters, with the focus-inverse billiard perimeter as corollary. The target becomes a product of inverse support distances of the bicentric CONTACT polygon. It is not that pedal perimeter. The full mapping is given below. |
| [Garcia–Reznik, arXiv 2012.03020](https://arxiv.org/pdf/2012.03020), propositions PDF pp.4–8 and Appendix A p.13 | Focus-inverse spoke sums, areas, circular loci | Principally three-period statements, sums, areas and loci. Neither inverting original billiard vertices nor its proved spoke-sum invariant identifies the target product of inverse OUTER vertices. |
| [Khare–Lakshminarayan–Sukhatme, math-ph/0207019v2](https://arxiv.org/pdf/math-ph/0207019v2), section 2.1 PDF pp.5–8, equation (26), p.22 after (115), and pp.34–35 | General cyclic elliptic identities and known complete dn product | The even-grid dn product is explicitly old. Their master identity handles cyclic sums through aggregate principal parts. Applying it to H'/H still requires the target zero/pole locations; using it as a black box without that computation transfers the central cancellation. The theta route (T1)–(T6) supplies the missing analytic computation explicitly. |
| [Schwartz, *The Pentagram Integrals for Poncelet Families*](https://www.math.brown.edu/~res/Papers/poncelet_monodromy.pdf), Theorem 1.2 PDF p.4, section 2 pp.6–9 | General Poncelet monodromy invariants | The theorem applies to monodromy invariants defined from projective corner cross-ratios. No identification of the dimensional original-focus product with one of those quantities was established. Generic complex-torus compactness is a method, not that identification. |
| [Stachel, *On the Diagonals of Billiards*](https://www.geometrie.tuwien.ac.at/stachel/SaoPaulo_Diagonals.pdf), Theorems 1–3 PDF pp.3–5 and Theorem 5 p.8 | General axial scalings, diagonal envelopes and pole/polar correspondence | These explain related projective geometry. They do not assert a Euclidean original-focus product. A nonsimilarity scaling cannot silently carry that functional. |

These geometric routes are blocked **as currently proposed implications**, pending a materially new metric identity or a newly found source. They are not claims of impossibility.

## Exact focus-polar bridge, and why the bicentric theorem stops short

Take F=(c,0) as origin and use unit Euclidean polarity. For a confocal ellipse with semiaxes `A0,B0`, its polar conic is

```
B0²(X²+Y²)-2cX-1=0,
```

a circle of center `(c/B0²,0)` and radius `A0/B0²`. Thus the original pair becomes a nested circle pair, and F is a limiting point as in the cited bicentric paper. Let Z_i be the pole of the tangent to E at P_i. The Z_i lie on the polar circle of E and are its contact points with the bicentric polygon obtained by polarizing the original billiard sides. The polar of Q_i is the line `Z_i Z_(i+1)`.

Consequently `|Q_i-F|` is the reciprocal of the perpendicular distance from F to this contact sideline. This fully specifies the transformed target. The known bicentric pedal-perimeter theorem instead sums side lengths of perpendicular feet from F to the bicentric polygon's sidelines; those feet are the inversions of the original P_i. It supplies neither the product just described nor the inversions of Q_i. A purported inference from that perimeter alone remains unsupported.

## Literal BT point/line issue: exact falsification of an unsafe bridge

In both inspected BT versions, Theorem 4.3 first defines R_i as the foot from the **center** to the billiard sideline, then part (a)/(1) prints a focal point-to-R_i product equal to `beta^N`; its proof invokes the focal-to-sideline Lemma 4.2. The literal point formulation fails on an exact billiard rectangle:

```
caustic alpha=2, beta=1, c²=3;
outer a²=6, b²=3;
orbit vertices (±2,±1), in rectangle order;
center feet R_i=(±2,0),(0,±1).
```

The rectangle satisfies both tangency and reflection. Its point-distance product to `(sqrt(3),0)` is `(4-3)(1+3)=4`, whereas `beta^4=1`. The product of perpendicular focus-to-sideline distances is indeed 1. The target Q vertices are `(±3,0),(0,±3)` and their focal product is `(9-3)(9+3)=72`.

This is a local notation/formulation caution, not a challenge to the intended focal-to-line integral. In particular it forbids using the literal printed point product as an unexplained bridge to Q. No external contact about this issue was prepared or made.

## Verification and scope of this audit

The accompanying `check_bridges.py` independently solves the actual pairs of tangent equations; it does not import submitted verification code. At 80 decimal digits it checks (D1), (T1), (T4) and (T6), phase constancy, and equality of the two focus products on 51 primitive cases: `N=4,8,12,16,20,24`, every coprime winding in the admitted half interval, and `k=.35,.8,.97`. Three even-but-not-4-divisible controls (`N=6,10,14`) show phase variation. All checks passed. These are diagnostics supplementing the displayed derivation, not proofs of a universal or historical claim.

The final replay used mpmath 1.3.0 from the parent's existing pinned standard-software directory `../math_algebra_family_01/runtime_packages`, under Python 3.14 with `-E -S -B -P`. No authored file from that sibling family was read. The initial system/bundled interpreters lacked mpmath. A small privately installed mpmath 1.4.1 was used for a preliminary run, then removed; the retained receipt is the pinned 1.3.0 replay.

Other priority families' findings, including a contemporary exact-proof lead reported by the parent, were not used to prove any conclusion above. This audit does not adjudicate that lead's timestamps or independence. No Git/ref/PR/publication operations or external outreach occurred. All retained audit artifacts are within this dedicated folder.

Exact remaining historical gap: identify an older full source that already proves (T3)–(T4), directly proves the Q/original-focus product, or supplies a previously proved invariant with a complete metric equivalence. A broad theorem title, classical cancellation principle, or matching conjecture label does not fill that gap.
