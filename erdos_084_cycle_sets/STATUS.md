# Status

Last updated: 2026-07-24 11:33 PDT.

## Published frontier

- The best published general lower bound remains the Faudree construction of
  order \(2^{n/2}\).
- The target \(f(n)/2^{n/2}\to\infty\) remains open.
- Nenadov proved the upper bound
  \(f(n)\le 2^{n-\Omega(\sqrt n/\log^{3/2}n)}\).

## Rigorously reconstructed internally

1. Fan graphs realize shifted positive difference supports.
2. The protected signature family \(\mathcal F_k(P)\) gives
   \[
   h(2M)\ge 2^{M-3k-1}S_k\qquad(M>3k+1).
   \]
3. The eight-way lift gives \(S_{m+1}\ge8S_m\).
4. The union-shadow refinement gives
   \(S_{m+1}\ge8S_m+2E_m\).
5. The previously recorded values are
   \[
   S_k=10,102,1020,9906,93198,854156,7674138
   \quad(1\le k\le7).
   \]
   These values, the corresponding \(E_m\), and the trace totals through
   \(m=7\) have been reproduced by the repository reference verifier.
6. An independent C++ verifier extends the exact full-family counts to
   \[
   \begin{aligned}
   S_8&=67{,}615{,}730,&E_8&=12{,}335{,}479,\\
   S_9&=586{,}193{,}940,&E_9&=89{,}453{,}245,\\
   S_{10}&=5{,}021{,}202{,}766,&E_{10}&=626{,}972{,}078.
   \end{aligned}
   \]

## Strongest active route

Put \(T_m=S_m/8^m\). The sharper recurrence implies

\[
T_{m+1}\ge T_m+\frac{E_m}{4\cdot8^m}.
\]

It therefore suffices to prove

\[
\sum_m\frac{E_m}{8^m}=\infty.
\]

A concrete intermediate target is

\[
\sum_{\substack{P\subseteq[2m]\\1\in P}}R_m(P)
\gg\frac{8^m}{m}.
\]

The shortest active target is the global shadow inequality

\[
mE_m\ge S_m.
\]

It holds exactly for \(2\le m\le10\). Together with the proved recurrence it
would give

\[
T_{m+1}\ge T_m\left(1+\frac1{4m}\right),
\]

hence \(T_m\gg m^{1/4}\) and a solution. A stronger complementary-rank
inequality holds through \(m=8\) but is false at \(m=9,10\); global surplus
must move across multiple ranks.

A second conditional route separates nearly alternating cyclic parameter
words. Their total \(S_m\)-mass is exponentially negligible. A conjectural
aperiodic orbit-boundary inequality with congestion \(O(m^2)\) would give
\(E_m\gg8^m/m\) and finish the proof, but new targeted data put this
inequality under serious empirical threat.

The independent orbit verifier exhaustively checks every orbit through
\(m=10\). The proposed constant \(c=1/2\) survives \(5\leq m\leq9\) but
fails at \(m=10\). The minimum normalized constants at \(m=8,9,10\) are
respectively
\[
0.585695352914,\qquad0.519819418576,\qquad0.428738331457.
\]
The weaker theorem-strength assertion with some fixed \(c>0\) remains open;
finite data do not establish that the minima stay bounded away from zero.
An unconditional additive defect bound is proved in the orbit note, but it
does not scale with the orbit's \(q_m\)-mass and is too weak for the
recurrence. Explicit four-run words through \(m=14\) have \(m\Lambda\)
between \(3.8\) and \(4.7\), strongly suggesting
\(\Lambda\asymp1/m\). The orbit route should not be treated as viable until
this candidate counterexample family is resolved.

An earlier mechanism used averaged collision energy for a restricted witness
family. A global second-moment estimate

\[
Q_m=O(mW_m)
\]

would prove this trace estimate. Exact computation now rules out that route.
The sharper guess \(Q_m\le mW_m\), which held through \(m=7\), is false at
\(m=8\):

\[
W_8=3{,}145{,}728,\qquad
Q_8=26{,}055{,}940>8W_8.
\]

Moreover,

\[
\frac{Q_9}{W_9}=15.5802,\qquad
\frac{Q_{10}}{W_{10}}=30.3878,
\]

so even \(Q_m=O(mW_m)\) is empirically implausible. The direct distinct-output
statistic is much healthier:

\[
\frac{mD_m}{8^m}
=0.7430,\ 0.7136,\ 0.6796
\quad(m=8,9,10).
\]

The direct support-size version remains of structural interest, but larger
diagnostics now indicate decay and it is secondary to the global shadow
inequality.

The trace estimate is not yet known to imply the required shadow gain. A
stronger Boolean down-set bridge

\[
\sum_{\substack{P\subseteq P_0\\1\in P}}
\bigl(e_0(P)+e_1(P)-R_m(P)\bigr)\ge0
\]

for every \(P_0\ni1\) is exactly verified through \(m=10\), but unproved.
At \(m=10\), the minimum remains \(H_m(\{1\})=0\), and the minimum
nontrivial first difference is \(352\).

A bounded Hall-matching experiment at \(m=6,7\) has now sharpened this route.
The two positive boundary families in the safe/unsafe identity are proved to
be identical setwise for every \(m\): with
\(\mathcal B_P=(\mathcal H_P\vee V(P))\setminus\mathcal H_P\),

\[
g_m(P)=2|\mathcal B_P|
 -\bigl(|\mathcal A_P|-|\mathcal A_P\vee V(P)|\bigr).
\]

This follows by adjoining the universal bottom generator \(\{-m,m\}\) and
is a genuine all-\(m\) simplification.  Exact raw one-deletion capacity
matchings exist at \(m=6,7\), but a normalized one-deletion rule has Hall
deficiencies \(7,158\); two deletions repair those finite capacity graphs.

At the object level, a graph permitting one row add, remove, or exchange
fails by \(20,268\) units at \(m=6,7\).  The sole enlargement to
row-selection Hamming radius two has exact full matchings in both cases and
repairs the failed matchings with alternating depth at most two and three.
The \(m=7\) repairs nevertheless use 32 coarse templates, so no canonical
all-\(m\) rule or uniform-depth lemma has been obtained.  The bounded
experiment is complete; no \(m>7\) or larger locality was tested.

## Theorem-strength unresolved gaps

- Prove a nonsummable lower bound for \(E_m/8^m\).
- Prove \(mE_m\ge S_m\), or any fixed positive-constant weakening.
- Resolve the four-run candidate counterexample before using the
  aperiodic orbit-boundary lemma (O).
- Prove the displayed trace estimate via \(D_m\gg8^m/m\), or a replacement.
- Prove the Boolean down-set trace-to-excess lemma.
- Prove the representation-aware Hamming-two Hall conjecture, or replace its
  finite matching by a canonical congestion-two boundary charge.
- Or prove a fixed-block amplification
  \(S_{m+L}\ge8^LS_m+c8^{m+L}\) for fixed \(L,c>0\).
- Audit the exact relationship with the 2026 Dunås thesis.

## Failed or insufficient claims

- Pointwise lower bounds for every \(P\) are false because periodic \(P\) can
  have large witness fibers.
- The sharp global guess \(Q_m\le mW_m\) fails at \(m=8\).
- The broader estimate \(Q_m=O(mW_m)\) is contradicted by rapidly worsening
  exact data through \(m=10\), though finite data alone is not a disproof.
- The pointwise bridge \(e_0(P)\ge R_m(P)\) is false.
- The complementary-rank inequality (R) fails at \(m=9\).
- The concrete orbit constant \(c=1/2\) fails at \(m=10\); only the
  existence of some fixed positive constant remains conjectural.
- The proposed pointwise “skew \(V(P)\)” bridge fails at
  \(m=10,\ P=[10]\), where \(e_0+e_1-R_m=-2\).
- The finite values \(S_1,\ldots,S_7\) are evidence only; they do not prove
  divergence.
- The recurrence \(S_{m+1}\ge8S_m\) alone only proves that \(T_m\) is
  nondecreasing.
