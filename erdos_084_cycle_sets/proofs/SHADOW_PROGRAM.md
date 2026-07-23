# The global shadow program

This note records the shortest currently visible route from the protected
construction to a solution. The proposed inequalities are conjectural unless
explicitly labeled otherwise.

## 1. The direct harmonic target

Recall

\[
S_m=\sum_{P\subseteq[2m]}q_m(P),
\qquad
E_m=\sum_{P\subseteq[2m]}\bigl(e_0(P)+e_1(P)\bigr).
\]

The proved recurrence

\[
S_{m+1}\ge8S_m+2E_m
\]

becomes, for \(T_m=S_m/8^m\),

\[
T_{m+1}\ge T_m+\frac{E_m}{4\cdot8^m}.
\]

Thus the direct theorem-strength target is

\[
E_m\gg\frac{8^m}{m}.
\tag{H}
\]

Exact enumeration through \(m=10\) strongly supports (H):

| \(m\) | \(S_m\) | \(E_m\) | \(mE_m/8^m\) | \(mE_m/S_m\) |
|---:|---:|---:|---:|---:|
| 5 | 93,198 | 30,527 | 4.658051 | 1.637750 |
| 6 | 854,156 | 234,374 | 5.364395 | 1.646355 |
| 7 | 7,674,138 | 1,698,857 | 5.670547 | 1.549620 |
| 8 | 67,615,730 | 12,335,479 | 5.882015 | 1.459480 |
| 9 | 586,193,940 | 89,453,245 | 5.998308 | 1.373401 |
| 10 | 5,021,202,766 | 626,972,078 | 5.839132 | 1.248649 |

The values near \(6\) are evidence for harmonic scale, not evidence for an
exact limiting constant.

## 2. A stronger aggregate inequality

The following simple inequality holds in every exact case \(2\le m\le10\):

\[
mE_m\ge S_m.
\tag{A}
\]

If (A) holds for all sufficiently large \(m\), then

\[
T_{m+1}
\ge
T_m\left(1+\frac1{4m}\right).
\]

Since \(T_1=10/8\), multiplication gives

\[
T_m\gg m^{1/4},
\]

and the protected construction solves the lower-bound half of Erdős Problem
84. More generally, \(mE_m\ge cS_m\) for any fixed \(c>0\) would suffice.

Pointwise inequalities are false: there are many \(P\) for which

\[
m\bigl(e_0(P)+e_1(P)\bigr)<q_m(P),
\]

and some \(P\) have \(e_0(P)+e_1(P)=0\). Any proof of (A) must move mass
between different parameters \(P\).

## 3. Ordered Toeplitz-row formulation

The generators have the equivalent form

\[
G_{m,P}(b)
=
\{b,-b\}
\cup
\{c\in[-m,b-1]:b-c\in P\}.
\tag{T1}
\]

Indeed, \(c=b-p\) for some positive \(p\in P\) exactly when \(c<b\) and
\(b-c\in P\). Thus the generator masks are augmented rows of a lower
triangular Boolean Toeplitz matrix: the entry below the diagonal depends
only on the difference \(b-c\), while \(\{b,-b\}\) supplies two marked
entries.

Likewise,

\[
V(P)
=
\{c\in[-m,m]:m+1-c\in P\},
\tag{T2}
\]

so \(V(P)\) is precisely the unmarked Toeplitz row at the hypothetical next
vertex \(b=m+1\). The quantities \(e_0,e_1\) measure the increment of the
Boolean OR-closure after adjoining this row without or with the bottom marker
\(-m\). This is the natural language for both orbit cuts and
deletion--contraction.

## 4. Rank-paired refinement

Define Boolean-rank totals

\[
S_{m,k}
=
\sum_{\substack{P\subseteq[2m]\\|P|=k}}q_m(P),
\qquad
E_{m,k}
=
\sum_{\substack{P\subseteq[2m]\\|P|=k}}
\bigl(e_0(P)+e_1(P)\bigr).
\]

The following stronger rank-symmetric statement was initially supported by
exhaustive enumeration for \(m=5,6,7\):

\[
m\bigl(E_{m,k}+E_{m,2m-k}\bigr)
\ge
S_{m,k}+S_{m,2m-k}
\qquad(0\le k\le m).
\tag{R}
\]

It fails in the empty/full rank pair for \(m=2,3,4\), and more decisively at
the central rank beginning with \(m=9\). The minimum paired ratios are

\[
1.020686,\quad0.911097,\quad0.784321
\qquad(m=8,9,10).
\]

Thus (R) is false.

The rank data still suggest a broader weighted mass-transport proof:
low-density \(P\) have large shadow surplus, while high-density \(P\) have
small shadow. However, neither individual complement pairs nor complementary
rank pairs support the required inequality uniformly. Any proof of (A) must
allow surplus to move across several ranks.

## 5. A separate Boolean down-set conjecture

For \(P\ni1\), let

\[
R_m(P)=|\{C\in\mathcal F_m(P):-m\notin C\}|
\]

and

\[
g_m(P)=e_0(P)+e_1(P)-R_m(P).
\]

Exhaustive enumeration through \(m=10\) supports the stronger down-set
inequality

\[
\sum_{\substack{P\subseteq P_0\\1\in P}}g_m(P)\ge0
\qquad
\text{for every }P_0\subseteq[2m]\text{ with }1\in P_0.
\tag{D}
\]

Taking \(P_0=[2m]\) would transfer aggregate trace mass into \(E_m\).
The same statement with \(e_0\) alone is false; the \(\alpha=1\) shadow is
essential. A plausible proof would delete the largest offending element of
\(P\), charging a collision lost under union with \(V(P)\) to a new
\(V_1\)-shadow at a proper subparameter. No injective charging rule has yet
been proved.

There is stronger exact evidence. Writing

\[
H_m(P_0)
=
\sum_{\substack{P\subseteq P_0\\1\in P}}g_m(P),
\]

exhaustive computation through \(m=10\) finds that \(H_m\) is coordinatewise
nondecreasing:

\[
H_m(P_0)-H_m(P_0\setminus\{p\})
=
\sum_{\substack{P\subseteq P_0\\1,p\in P}}g_m(P)
\ge0
\quad(p\in P_0\setminus\{1\}).
\tag{D+}
\]

The two newest exact cases are

\[
\begin{array}{c|r|r|r|r}
m&\sum_{P\ni1}R_m(P)&\sum_{P\ni1}e_0(P)&
\sum_{P\ni1}e_1(P)&H_m([2m])\\ \hline
9&11{,}921{,}862&16{,}710{,}755&10{,}765{,}434&15{,}554{,}327\\
10&83{,}431{,}916&109{,}868{,}703&73{,}048{,}687&99{,}485{,}474
\end{array}
\]

For both \(m=9,10\), the unique zero of \(H_m\) is \(P_0=\{1\}\). The
minimum nontrivial first differences in (D+) are \(143\) and \(352\),
respectively. These are finite verifications, not a proof.

Mixed second differences can be negative, so this is not full absolute
monotonicity. The required base case is already elementary:
\(H_m(\{1\})=g_m(\{1\})\geq0\). Indeed, for \(P=\{1\}\), every trace
signature avoids both \(-m\) and \(m\), while \(V(P)=\{m\}\); hence
\(C\mapsto C\cup\{m\}\) injects the trace signatures into new
\(e_0\)-outputs. Therefore a deletion--contraction proof of (D+) for
Toeplitz OR-closures would establish (D).

### Exact safe/unsafe decomposition

For \(P\ni1\), put \(x=-m\), \(y=m\), \(U=V(P)\), and regard all sets below
as subsets of \([-m,m]\setminus\{x\}\). Define

\[
\mathcal A_P=\{C\in\mathcal F_m(P):x\notin C\},
\qquad
\mathcal H_P=\{C\setminus\{x\}:C\in\mathcal F_m(P),\ x\in C\}.
\]

Every member of \(\mathcal A_P\) omits \(y\), while \(y\in U\) and
\(x\notin U\). For a family \(\mathcal X\), write
\(\mathcal X\vee U=\{X\cup U:X\in\mathcal X\}\). Partitioning shadow outputs
according to whether they contain \(x\) gives the exact identities

\[
\begin{aligned}
e_0(P)
&=
|\mathcal A_P\vee U|
+|(\mathcal H_P\vee U)\setminus\mathcal H_P|,\\
e_1(P)
&=
|((\mathcal A_P\vee U)\cup(\mathcal H_P\vee U))
  \setminus\mathcal H_P|.
\end{aligned}
\]

Since \(R_m(P)=|\mathcal A_P|\), it follows that

\[
\begin{aligned}
g_m(P)
={}&|\mathcal A_P\vee U|-|\mathcal A_P|\\
&+|(\mathcal H_P\vee U)\setminus\mathcal H_P|\\
&+|((\mathcal A_P\vee U)\cup(\mathcal H_P\vee U))
  \setminus\mathcal H_P|.
\tag{DC}
\end{aligned}
\]

Thus the only negative contribution is the collision deficit
\(|\mathcal A_P|-|\mathcal A_P\vee U|\); the other two terms are boundary
expansions of the unsafe-row closure. For the smallest obstruction
\(m=3,\ P=\{1,2,6\}\), that deficit is one and both boundary terms vanish.

Toggling \(p\) has a one-diagonal effect. If
\[
p\in P\cap\bigl(\{2,\ldots,2m-1\}\setminus\{m\}\bigr),\quad
Q=P\setminus\{p\},\quad b=p-m,\quad v=m+1-p=1-b,
\]
then \(V(P)=V(Q)\cup\{v\}\); row \(b\) migrates from the safe closure to the
unsafe closure because its new diagonal entry is \(-m\); and each other
generator row \(b'\) gains at most the single entry \(b'-p\). This reduces
the generic coordinate of (D+) to charging safe OR-collisions caused by one
Toeplitz diagonal to the unsafe boundary created by the migrated row and the
other diagonal cells.

There are two exceptional coordinates. At \(p=m\), the putative row is
\(b=0\), which is not a generator. At \(p=2m\), row \(b=m\) is already
unsafe and the new entry \(-m\) duplicates its marker. These cases have no
row migration and must be handled separately in any deletion--contraction
proof.

The representative-preserving injection suggested by this description is
false already at \(m=3\): keeping the same generator representative after
deleting \(p\) does not separate all collision fibers. Any successful charge
must change representatives, use a rank-preserving swap, or be a
non-injective cardinality argument.

Another natural pointwise strengthening is also false. One might hope that
\(g_m(P)\geq0\) whenever \(V(P)\) contains no reflected pair
\(\{v,-v\}\). Exact computation gives the counterexample

\[
m=10,\qquad P=\{1,\ldots,10\},\qquad
(q_m,e_0,e_1,R_m)=(1800,41,9,52),
\]

so \(g_m(P)=-2\), even though \(V(P)=\{1,\ldots,10\}\) has no reflected
pair. The same interval family has \(g_m(P)=-5,-8\) at \(m=11,12\).
Exposed marker coordinates alone therefore do not supply the missing
injection.

The smallest pointwise obstruction is a useful unit test. For
\(m=3\) and \(P=\{1,2,6\}\),

\[
(e_0(P),e_1(P),R_m(P))=(3,0,4).
\]

The deficit is absorbed by the positive values at the proper subparameters
\(\{1,2\}\) and \(\{1,6\}\). Any proposed deletion charge should reproduce
this transfer without relying on a false pointwise inequality.

## 6. Priority

1. Prove (A) by compression or a weighted cross-rank injection.
2. Prove (D) by an acyclic deletion charge.
3. Analyze the explicit four-run family in
   `APERIODIC_ORBIT_PROGRAM.md`; current data suggest it may refute the
   fixed-constant orbit lemma.
4. Treat the trace/restricted-witness program as a secondary source of
   canonical objects, not as the sole route: its unweighted second moment is
   demonstrably too large.
