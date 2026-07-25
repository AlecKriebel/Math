# Hostile audit: level-five deepest transposition

**Verdict: PASS after one factual wording correction.**

**Completed:** 2026-07-25T11:34:30Z.

The \(p=23,s=3\) certificate is correct.  A structurally independent
regular-representation calculation reproduces every requested norm and
guard, the prime-square derivative, the rational vanishing sheet, the
local transposition, and the \(S_3^{81}\) kernel argument.  I found no
extraneous quotient branch, nonunit denominator, simultaneous vanishing
sheet, arithmetic/geometric monodromy conflation, or group-theoretic gap.

The audit caught one factual wording error in the initial draft of
`../RESULT.md`: it called the announced map “degree-three.”  Its total
polynomial degree is seven and its generic degree is three.  The candidate
was corrected to “degree-seven Keller map of generic degree three” before
this verdict.  No arithmetic or theorem statement changed.

## 1. Independent tower construction

Let \((a,b,c)\) be a target point and put
\[
C_{a,b,c}(T)=2aT^3-bT^2+2T-c.                          \tag{1}
\]
For a source point \((x,y,z)\), write \(u=1+xy\) and
\[
t=\frac{x}{u}.
\]
Direct substitution in the announced map gives
\[
C_{F(x,y,z)}(t)=0.                                     \tag{2}
\]
Conversely, if \(t\) is a root of (1), then
\[
\begin{aligned}
y&=-\frac{bt^2+3c-6t}{2t^2},\\
x&=\frac{t}{1-ty},\\
z&=\frac{2x-3x^2y-c}{x^3}.                             \tag{3}
\end{aligned}
\]
The three divided-by elements at each inverse step are therefore
\[
2t^2,\qquad1-ty,\qquad x^3.                            \tag{4}
\]

The audit does not import `finite_field_norm_depth4.py` or any W4
arithmetic.  At each level it represents every algebra element by its
regular multiplication matrix.  If the current algebra has rank \(n\),
the next root is the \(3n\times3n\) block companion matrix
\[
T=
\begin{pmatrix}
0&0&-c_0\\
I&0&-c_1\\
0&I&-c_2
\end{pmatrix},
\]
where \(T^3+c_2T^2+c_1T+c_0=0\) is the monic form of (1).  Base elements
embed as three equal diagonal blocks.  Matrix arithmetic and inversion
then evaluate (3) directly.

This produces ranks
\[
1,\ 3,\ 9,\ 27,\ 81
\]
without coefficient-vector quotient reduction.  At every level the
certificate checks:

- the block companion relation;
- all three forward equations \(F(X_i)=X_{i-1}\);
- recovery \(t_i=x_i/(1+x_i y_i)\); and
- invertibility of every element used in (3).

Thus the tower consists of genuine successive inverse points rather than an
eliminant component introduced by denominator clearing.

## 2. Exact modular replay

At \(p=23,s=3\), the independent rank-81 calculation gives
\[
\boxed{(10,22,10,4,0)}
\]
for the target discriminant and four inverse-level discriminant norms.
The first four entries are units, so all four quotients used to construct
the rank-81 algebra are étale at the specialization.

The five leading-coefficient norms are
\[
\boxed{(2,14,19,11,1)},
\]
including the leading coefficient of the final, potentially ramified
cubic.  The twelve reconstruction-guard norms, grouped by inverse step,
are
\[
\boxed{(18,14,5;\ 2,8,21;\ 13,13,7;\ 8,17,12)}.
\]
Every value is nonzero modulo \(23\).

Over \(\mathbb Z/23^2\mathbb Z\), the independently reconstructed norms are
\[
\boxed{N_4(3)=460,\quad N_4(26)=299,\quad N_4(49)=138}
\pmod {529}.                                            \tag{5}
\]
All reduce to zero modulo \(23\).  Their first differences give
\[
\frac{299-460}{23}=16\pmod {23},\qquad
\frac{138-460}{23}=9=2\cdot16\pmod {23}.                \tag{6}
\]
Hence
\[
\boxed{N_4'(3)=16\ne0\pmod {23}}.                       \tag{7}
\]
As a supplemental Hensel check, the first lifted root is
\[
3+16\cdot23=371\pmod {529},
\]
and a separate exact evaluation gives \(N_4(371)=0\pmod {529}\).

The strict independent replay takes \(6.37\) seconds wall time and peaks
at \(19{,}824{,}640\) bytes (about \(18.9\) MiB) on the stated machine.

## 3. Rational sheet path

Scalar root enumeration over \(\mathbb F_{23}\), independent of all
rank-81 determinants, finds exactly one rational path whose fourth inverse
point has vanishing discriminant:
\[
\boxed{(t_1,t_2,t_3,t_4)=(10,22,13,1)}.                 \tag{8}
\]
The corresponding points are
\[
\begin{aligned}
X_1&=(2,18,22),\\
X_2&=(11,1,6),\\
X_3&=(10,9,13),\\
X_4&=(22,2,21).
\end{aligned}                                          \tag{9}
\]
The actual reconstruction denominators along this path are
\[
\begin{aligned}
&(16,5,8),\quad(2,2,20),\\
&(16,22,11),\quad(2,22,22),
\end{aligned}
\]
so no scalar reconstruction pole is hidden.

Implicit differentiation of the four simple inverse roots gives
\[
(t_1',t_2',t_3',t_4')=(7,22,4,19)
\]
and
\[
\boxed{\frac{d}{ds}\Delta(X_4)=18\ne0\pmod {23}}.       \tag{10}
\]
The final cubic at \(X_4\) has residue roots
\[
1,\ 22,
\]
with derivative values \(15,0\), respectively.  Thus \(1\) is simple and
\(22\) is double.  There is no triple-root ambiguity.

## 4. Localization and norm valuation

Work initially over \(\mathbb Z_{(23)}[s]\).  Localize successively at the
displayed leading and reconstruction norms.  For a finite free algebra,
an element with unit norm is itself a unit, so every division in (3) is
legal in this localization.  The four monic quotients therefore form a
finite free algebra \(E\) of rank \(81\).

Localizing further at the four lower discriminant norms makes \(E\) finite
étale.  The element
\[
d=\Delta(X_4)\in E
\]
is regular, and its norm is a rational function
\[
N_4(s)=\operatorname{Norm}_{E/R}(d)=A(s)/B(s)
\]
whose denominator is a \(23\)-adic unit at \(s=3\).  Reduction,
specialization, inversion, and norm commute because every localized
element remains a unit.  Equations (5)--(7) therefore imply
\[
A(3)=0,\qquad A'(3)=16B(3)\ne0\pmod {23}.              \tag{11}
\]

Hensel's lemma gives a unique \(\sigma\in\mathbb Z_{23}\) with
\(\sigma\equiv3\pmod {23}\) and \(A(\sigma)=0\).  Let \(P\) be the
characteristic-zero irreducible factor of \(A\) containing \(\sigma\).
It occurs with multiplicity one.  Every lower discriminant, leading
coefficient, and reconstruction guard remains a \(23\)-adic unit at
\(\sigma\), so \(P\) divides none of them.

At the generic point of \(P\), étaleness and regularity give
\[
\operatorname{ord}_{P}\operatorname{Norm}(d)
=\sum_{\mathfrak q\mid P}
 f(\mathfrak q/P)\operatorname{ord}_{\mathfrak q}(d)=1. \tag{12}
\]
Every nonzero summand is a product of positive integers.  The only
possibility is one prime with
\[
f(\mathfrak q/P)=1,\qquad
\operatorname{ord}_{\mathfrak q}(d)=1.                 \tag{13}
\]
All other primes have \(d\) a unit.  This rules out two simultaneous
branching sheets and explains the rational residue path in (8).

The audit separately enumerates the positive-integer decompositions of
(12); (13) is the unique one.

## 5. From the norm zero to one transposition

The discriminant of (1) is
\[
\operatorname{disc}_T C_{a,b,c}=-4\Delta(a,b,c).        \tag{14}
\]
At the unique prime (13), its leading coefficient \(2a\) is a unit and
its discriminant has valuation one.  The residue calculation in Section 3
shows one simple and one double root.  Since the residue characteristic is
\(23\ne2,3\), the ramification is tame.  Local inertia swaps exactly the
two branches meeting at the double root and fixes the third.

All first four inverse levels are étale there.  Therefore, on the
\(3^5=243\) leaves, this inertia element is one transposition supported
inside a single bottom three-leaf block and fixes the other \(241\) leaves.
The divisor is characteristic zero and survives base change to
\(\mathbb C\), so this is geometric—not merely arithmetic—monodromy.

## 6. W5 group step

Geometric monodromy at level five lies in
\[
W_5=S_3^{81}\rtimes W_4
\]
and projects onto the already proved \(W_4\).  The all-level inertia theorem
supplies a \(243\)-cycle \(\alpha\).

Label the bottom blocks as
\[
B_j=\{j,j+81,j+162\},\qquad0\le j<81.
\]
Then \(\alpha\) cycles the \(81\) blocks and \(\alpha^{81}\) is a
three-cycle on each \(B_j\).  If \(\tau\) is the new transposition in
\(B_0\), then
\[
\langle\tau,\alpha^{81}\tau\alpha^{-81}\rangle
=S_3(B_0).
\]
Conjugating this factor by \(\alpha^j\), \(0\le j<81\), gives \(81\)
copies of \(S_3\) with pairwise disjoint supports.  They generate the full
kernel \(S_3^{81}\).  A subgroup containing this kernel and surjecting to
\(W_4\) is all of \(W_5\).

The independent permutation certificate explicitly constructs each local
six-element group, checks all \(81\) disjoint supports, and checks that they
cover all \(243\) leaves.  Thus
\[
\boxed{\operatorname{Mon}_{\mathbb C}(F^{\circ5})=W_5}.
\]

## 7. Verification and fault guards

Run:

```sh
./verify_strict_and_faults.sh
```

The strict run uses only the Python standard library.  Twelve mutations
independently corrupt:

- the inverse cubic sign;
- the reconstruction sign;
- the discriminant sign;
- each of the three modular profiles;
- one prime-square norm and its derivative;
- the rational path and its dual derivative;
- the norm-valuation uniqueness; and
- the group-kernel stride.

Every mutation exits nonzero through its intended guard.  The wrapper avoids
recomputing the unrelated heavy \(81\times81\) prime-square towers for
lightweight sheet and group mutations; its complete wall time is
\(30.78\) seconds.

This audit was AI-assisted and is not peer reviewed.  Exact checks are
evidence about the encoded algebra, not peer review.
