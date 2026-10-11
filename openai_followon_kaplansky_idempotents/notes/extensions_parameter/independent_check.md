# Independent check of the q=32 parameter change

Checkpoint: 2026-10-06 22:46:56 America/Los_Angeles (2026-10-07
05:46:56 UTC). Assigned mathematical audit: complete, estimated 100%.
This estimate concerns this parameter audit only, not novelty, publication,
an explicit matching certificate, or the overall research goal.

## Independence and sources

This check read the pinned construction directly, without reading the
parent's summaries or extension notes. It changes no pinned source and
performs no git, publication, or external communication actions.

Files under
`sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/sections/`:

| File | SHA-256 |
| --- | --- |
| `random.tex` | `bb172b92ba622e262c2bf124e70c3cd55922200083c09db658615759b81323c4` |
| `patterns.tex` | `20c6cc1f3fb035150831e5091c98313f04e7a9d8aaa347507020b176394ed4ea` |
| `planar.tex` | `e3a1a4e23dd6871a9746ffde05d32297e695f3167b8efa0f0a4cad5da8c9ae6b` |
| `assembly.tex` | `3987e23ea7c5c8d217ca539d5a307d59f8eac5b8381a0afe411125e57f0bee4a` |

## Exact claim and outcome

Replacing q=128 by q=32, preserving the seven extra letters, Fano-complement
types, inverse-pairing rule, and random matching mechanism, preserves every
quantitative hypothesis of the pinned random, bounded-pattern, and
no-arrangements arguments. The deterministic algebraic and topological
conclusions can therefore be applied to the altered construction exactly as
in its assembly argument. Its rose has 532 generators. This establishes an
existential upper bound, conditional only on the pinned deterministic proofs;
it does not exhibit a matching outcome or provide a new independent proof of
those already-audited deterministic results.

The q=16 construction with these same types and weights cannot have the
pinned squared-word decay property. This is an exact growth obstruction for
its matrix, independent of the arbitrary choice of the seven paired ordinary
letters. It does not exclude a q=16 construction proved by a different
mechanism or with altered types.

## Balances, inverse pairs, parity, and turn counts

For q=32,

\[
v=32^2+32+1=1057,\quad |T|=1064,\quad
p=33/1057,\quad n=1057m,\quad m\equiv1\pmod4.
\]

There are seven extra--ordinary inverse pairs and
(1057-7)/2=525 ordinary--ordinary inverse pairs, giving 532 rose edges.
The possible degrees are 33, 37, and 40. Every ordinary line intersection
has size 33 or 1, hence odd. Intersections of empty/Fano-complement extra
parts have sizes 0, 2, or 4. The distinguished full extra part has size 7,
and its intersection with a Fano complement has size 4. Thus the only
even A--A total intersection is the distinguished self-intersection, of
size 40; every A--B intersection is odd. Changing the projective plane
order affects no parity rule.

The prescribed counts are

\[
a_m=(33m-1)/4,\qquad b_m=33(m-1)/4.
\]

They are integers along the specified sequence. Four Fano complements
contain each extra letter and two contain each extra pair. Therefore
ordinary and extra letters both occur exactly 33m=np times in A, and
33(m-1)=(n-v)p times in B. Feasibility of disjoint assignment within each
line class follows from

\[
7\lceil a_m/v\rceil+1,
\quad7\lceil b_m/v\rceil
\leq\frac{231}{4228}m+O(1),\qquad 231/4228<1.
\]

These bounds are eventually less than m-1. The same distribution argument
still gives ordinary/extra turn frequency np^2+O(1), with constants fixed
as m grows. Ordinary/ordinary frequency is m or m-1=np/33+O(1).
Extra/extra frequency in A is 2a_m+1=(np+1)/2 and in B is
2b_m=(n-v)p/2=np/2+O(1). Hence all three turn-count cases hold with exactly
the original turn-weight rule, now w=1/33, p, or 1/2.

## Exact contraction at q=32

Partition T into E (the seven extra letters), C (the seven ordinary letters
paired with extras), and O (the remaining v-7 ordinary letters). Set
a=(q+1)^{-2} and b=p^2. The squared-turn matrix M has an exact equitable
quotient, in this E,C,O order,

\[
Q=\begin{pmatrix}
7b&6a&(v-7)a\\
3/2&7b&(v-7)b\\
7b&7a&(v-8)a
\end{pmatrix}.
\]

For example, in an E row, the inverse is a C letter; only six of the seven
C successors are allowed. In a C row, the inverse is an E letter; only six
E successors are allowed, each contributing 1/4. In an O row, one of the
v-7 ordinary O successors is excluded. Thus the counts are exact and
independent of which ordinary letters were chosen for pairing with E.

The pinned positive vector is f=(1,4,1) on this partition. At q=32 its exact
ratios are

\[
\frac{(Qf)_E}{f_E}=\frac{57534613}{57937341},\qquad
\frac{(Qf)_C}{f_C}=\frac{116319}{182408},\qquad
\frac{(Qf)_O}{f_O}=\frac{57694220}{57937341}.
\]

Every ratio is less than one, and their maximum is

\[
\lambda=57694220/57937341
=1-243121/57937341<1.
\]

Equivalently, the two original looser bounds remain valid:

\[
32/33+7p^2+21/33^2=\lambda<1,
\qquad 3/2+(v+21)p^2=116319/45602<4.
\]

Lifting f to T gives Mf<=lambda f. Since 1<=f<=4, exactly the pinned proof
yields

\[
\sum_{W\in T^h}P(W)^2
\leq4256\lambda^{h-1}.
\]

Taking delta=-log(lambda)/4>0 yields its eventual exp(-2 delta h) bound.
Numerically delta is approximately 0.001051275949897804, but no numerical
approximation is needed for the proof.

## Girth conditioning and expansion

All alphabets, positive weights, and degree bounds remain constants
independent of m. Set d_*=40 and choose any c0>0 satisfying

\[
c_0\log(2\cdot1064/p)<1,\qquad 2c_0\log40<1.
\]

Such a choice exists. The bad-edge expectation, distant switch counts,
nonempty high-girth conditioned space, and prescription bound transfer
unchanged, with vp=33 and
r_n=33+O(40^{2L+2})=o(n). The case of loops or two parallel edges is handled
by the same distinct-slot and distinct-prescription argument.

The explicit numeric changes in small-set expansion are essential. A
nonexpanding set S of k vertices inside Z of size 2k forces at least

\[
r=\lceil33k/2\rceil,\qquad16.5k\leq r\leq17k
\]

distinct prescriptions. Choose rho<1/4 and 17 rho<p/4. With the same
count of possible prescriptions and conditioning bound, the union bound is

\[
\left(\frac{en}{2k}\right)^{2k}(C_2 k)^r
\left(\frac2{np}\right)^r
\leq\bigl(C_3(k/n)^{14.5}\bigr)^k.
\]

For example C2 may be chosen at least 8e|T|/33. Constants absorb rounding
because r/k lies in [16.5,17]. Shrink rho so C3 rho^{14.5}<1/2. For
k<=sqrt(n), this is bounded by (C3 n^{-7.25})^k; for sqrt(n)<k<=rho n it
is bounded by 2^{-k}. Both summed ranges tend to zero. Thus expansion
and the diameter proof survive. Retaining the pinned exponents 62.5 and
31.25, or its 65 rho threshold, would be an incorrect transcription;
the appropriate replacements are 14.5, 7.25, and 17 rho.

## No-arrangements dependency audit

The only explicit degree constants outside random.tex occur in the short
closures proof in planar.tex. Its minimum degree 129 becomes 33; after
deleting up to two edges, its 127 becomes 31. The proof needs only a
remaining degree at least three, so its count 3*2^{k-1}>n and its displayed
closure bound D0>=d+8/(c0 log 2)+8 remain valid.

The bounded-pattern proof in patterns.tex uses only: a fixed finite alphabet
with a fixed-point-free inverse involution; a positive minimum among reduced
turn weights; the turn counts; high girth; prescription bounds for O(L)
edges; and the established delta>0. Every input is preserved. It then
chooses its new epsilon from the new delta and a0. The planar extraction
depends on epsilon and the diameter/closure constants, so U, eta, K0, C,
and I must be rechosen in the stated order, all before m tends to infinity.
It assumes no further numeric lower bound on q or on the alphabet size.
The geometric pairing and separator statements are alphabet independent.
The resulting probability bounds still tend to zero, however large these
fixed constants become. Assembly then uses only the no-arrangements result,
girth L>=3, and intersection parities.

## Exact obstruction at q=16

Here v=273, |T|=280, a=1/289, b=289/74529. The exact quotient is

\[
Q_{16}=\begin{pmatrix}
289/10647&6/289&266/289\\
3/2&289/10647&10982/10647\\
289/10647&7/289&265/289
\end{pmatrix}.
\]

Use the different positive vector g=(1,13/5,1). Direct rational arithmetic
gives

\[
\frac{(Q_{16}g)_E}{g_E}=\frac{15408581}{15384915}>1,
\qquad
\frac{(Q_{16}g)_C}{g_C}=\frac{39577}{39546}>1,
\qquad
\frac{(Q_{16}g)_O}{g_O}=\frac{15493757}{15384915}>1.
\]

Their positive differences from one are respectively
23666/15384915, 31/39546, and 108842/15384915. The middle ratio is the
minimum; let lambda16=39577/39546>1. Lift g to the full matrix M using the
same partition. Because M is nonnegative,

\[
M^{h-1}g\geq\lambda_{16}^{h-1}g.
\]

Also 1>=(5/13)g, and 1^T g=7+7(13/5)+266=1456/5. Therefore for every
h>=1,

\[
\sum_{W\in T^h}P(W)^2
=1^T M^{h-1}1
\geq (5/13)\lambda_{16}^{h-1}1^T g
=112\lambda_{16}^{h-1}.
\]

This lower bound grows exponentially, proving that the pinned squared-word
decay conclusion is impossible for q=16 with these weights. An independent
exact spectral cross-check is

\[
\det(I-Q_{16})=-3687500605/556930846017<0.
\]

The explicit positive-vector certificate is stronger than noting that the
original f test fails: it rules out every attempted positive contraction
vector for this M and proves failure of the word-mass conclusion itself.

## Remaining gap and limitations

No mathematical gap was found in the q=32 parameter substitution or in the
q=16 squared-weight obstruction. The result remains existential because
the pinned large-m proof chooses a matching rather than specifying one.
This audit establishes neither novelty nor priority of a 532-generator
bound, does not independently re-prove the entire topological criterion,
and does not justify minimality among alternative constructions or other
proof mechanisms.
