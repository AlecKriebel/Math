# Exact-byte hostile audit: anisotropic 336 quotient Foster theorem

**Audit date:** 2026-08-12 PDT  
**Audited theorem:** [frozen h112 theorem](proof_first_336_h112_quotient_foster_theorem.md)  
**Audited SHA-256:** concatenate
`9206aa2b07aa802e4d06a769b3b60d520` and
`b2dbd12752312497aa5b41156780d48`  
**Audited size:** 414 lines, 15,620 bytes  
**Verdict:** **STRICT PASS.**

The theorem bytes named above were treated as immutable.  This audit did not
edit them.  I replayed the algebra, the exhaustive support split, the marked
episode construction, and the random-time recurrence interface independently.
I found no counterexample, hidden orientation assumption, face exception, or
unproved stochastic inference.  The mathematical replay was first completed
on the earlier 411-line freeze (SHA-256 beginning `62f5995b` and ending
`397718`).  Section 8 records its full hash and certifies exactly that the
current target is a render-only derivative of those passed bytes.

## 1. Scope replay

After a coordinate permutation the audited family is exactly

\[
 \begin{aligned}
 h&=(1,1,2), & R&=\{0,A,B\},\\
 T&=\{C\}\cup Q, &
 Q&\subseteq\{2A,A+B,2B\},\qquad |Q|\ge2.
 \end{aligned}
\]

Both linkage graphs may have arbitrary strongly connected orientations and
arbitrary fixed positive labelled rates.  The proof uses only strong
connectivity, the displayed supports, and finiteness of the labelled edge
sets.  It never enumerates orientations, histories, rates, or population
boxes.  The homogeneous \(h=(1,1,1)\) cases are explicitly excluded and are
not silently claimed.

## 2. Marked factorial identities

At a marked state \((x,t)\), the previous target is enabled, so
\(x_i\ge t_i\) and

\[
 F(x,t)=\sum_i\log((x_i-t_i)!)
\]

is well defined and nonnegative.  If \(e:y\to u\) is the next reaction,
factorial cancellation gives exactly

\[
 F(x+u-y,u)-F(x,t)=\log\frac{(x)_t}{(x)_y}.
\]

Writing \(p_y=K_y(x)_y/\Lambda\), averaging this identity gives

\[
 D=\log p_t-\sum_y p_y\log p_y-log K_t+sum_y p_y\log K_y.
\]

There are finitely many sources and all \(K_y\) are fixed and positive.
Consequently \(D\le\log p_t+C\).  Moreover the positive part of an
individual reward is bounded by \(-\log p_y+C\); hence all fixed positive
source-weighted moments are uniformly bounded.  Thus (2.2)--(2.4) are exact,
including on coordinate faces.

## 3. Workload and global physical clock

For \(H=A+B+2C\), every top reaction is \(H\)-neutral.  The lower linkage
contributes only constant births, unary transfers, and direct unary deaths,
so

\[
 \mathcal LH=\beta-\delta_AA-\delta_BB.
\]

Strong connectivity of \(R\) forces \(K_A,K_B>0\) and at least one of
\(\delta_A,\delta_B\) to be positive.  Since \(C\) is a top source,
\(K_C>0\).  Therefore

\[
 \Lambda\ge K_AA+K_BB+K_CC+K_0
          \ge c(A+B+C+1)\ge c'(H+1).
\]

This verifies the global hazard lower bound on every face.  It is the exact
reason that all bounded-depth marked episodes have expected physical duration
\(O((H+1)^{-1})\).

## 4. Quotient sign audit

For

\[
 V=H+\epsilon\frac{F}{H+1}
\]

and workload increment \(d\in\{-1,0,1\}\), direct subtraction gives (3.1).
If \(F'=F+r\) is the endpoint factorial value, then a birth has the extra
term

\[
 -\epsilon\frac{F'}{(H+1)(H+2)}\le0,
\]

whereas a death has the extra term

\[
 \epsilon\frac{F'}{H(H+1)}=O\!\left(\frac{\log(H+2)}{H}\right)=o(1).
\]

The latter is absorbed pointwise into half of the favorable unit death for
all sufficiently large \(H\).  Constant-source births occur with probability
\(O(H^{-1})\).  On a bounded-depth path, replacing the successive
denominators by the initial \(H+1\) costs only
\(O(\log(H+2)/H^2)\).  Thus (3.2)--(4.6) contain no missing positive
\(\log H/H\) toll.

## 5. Rare-source Bellman replay

Along a fixed labelled path, retain all clocks and continue only when the
designated label fires.  At every competitor, stop at its actual population
and actual target; after designated arrival at the terminal complex, include
one final ordinary jump.  The recursion is therefore exactly

\[
 J_i=D_i+a_iJ_{i+1},\qquad a_i=\alpha_i p_{y_i},
\]

where the finite path menu supplies \(\alpha_i\ge\alpha_*>0\).  If the
terminal source probability is at most \(\delta\), the scalar recursion

\[
 B_0=\log\delta+C_0,\qquad
 B_{k+1}=C_0+\sup_{0<p\le1}
              \{\log p+\alpha_*pB_k\}
\]

is a valid upper bound.  Once \(B_k<0\), replacing \(\alpha_i\) by the
smaller \(\alpha_*\) increases the upper bound.  If \(B_k=-L\), the supremum
is \(-\log(\alpha_*L)-1\) for large \(L\); iteration through any fixed path
length still tends to \(-\infty\) as \(\delta\downarrow0\).  Taking the
maximum over the finite path menu proves the uniform function \(A(\delta)\).

For a lower-linkage mark, the terminal complex \(0\) has constant propensity,
so the global hazard bound makes \(p_0=O(H^{-1})\).  Hence every lower mark is
covered.  The terminal activation jump is part of the preceding marked
episode, and no conditioning on its having occurred is used.

The Bellman decrement enters \(V\) as \(-\epsilon A(\delta)/(H+1)\), while
the workload-birth charge and the physical duration are both \(O(H^{-1})\).
Choosing \(\delta\) after fixing \(\epsilon\) gives one uniform negative
physical-time inequality.  A uniform embedded-jump margin is neither claimed
nor required.

## 6. Exhaustive top-mark dichotomy

For a top mark \(t\), let \(z_c=x-t+c\) be the deterministic success endpoint
of a fixed path to \(c\in T\).  The two alternatives are literal and
exhaustive:

1. some \(p_c(z_c)\le\delta\), in which case the rare-source Bellman episode
   applies; or
2. every \(p_c(z_c)>\delta\).

In the second case, \(c=C\) yields both \(C(x)=\Theta(H)\) from below and
\(\Lambda(z_C)=O(H)\).  For each \(q\in Q\), the lower global hazard bound
and \(p_q(z_q)>\delta\) yield \((z_q)_q\ge cH\).

The repaired bounded-displacement comparison is essential and is correct:

\[
 \Lambda(w+b)\le C_b\{\Lambda(w)+H(w)+1\}.
\]

The additive \(H+1\) term covers a mixed or double source that a bounded shift
activates on a face.  Transport from \(z_C\) therefore gives
\((z_q)_q\le CH\), not the false shift-only factorial comparison.  Thus every
selected quadratic propensity is \(\Theta(H)\).

There are only three possible two-element cores of \(Q\):

\[
 \{2A,2B\},\qquad \{2A,A+B\},\qquad \{2B,A+B\}.
\]

In each case the two factorial bounds force, after the bounded endpoint
shift,

\[
 A=\Theta(\sqrt H),\qquad B=\Theta(\sqrt H).
\]

Extra top vertices do not weaken this conclusion.  Since strong connectivity
of \(R\) supplies a direct death of at least one of \(A,B\), the workload
drift is at most \(-c\sqrt H\), and bounded-displacement transport also gives
\(\Lambda(x)=\Theta(H)\).

For one ordinary all-clock jump, group the death denominator correction with
half of that death's favorable workload decrement.  Birth denominator
corrections are favorable, and the remaining averaged factorial reward is
\(\epsilon D/(H+1)\le C\epsilon/H\).  Hence

\[
 \mathbb E\Delta V
 \le -\frac{c}{\sqrt H}+\frac{C}{H},
 \qquad
 \mathbb E\tau\le\frac{C}{H}.
\]

This proves the same fixed-\(\eta\) episode inequality in the all-nonrare
case.  The argument remains valid at faces: either a face makes a tested top
source rare, or the all-nonrare inequalities themselves force both unary
coordinates into the displayed square-root regime.

## 7. Tiling, localization, and recurrence

The state-selected rules form a finite menu: a lower mark selects its fixed
path to zero; a top mark selects the first rare terminal path if one exists,
and otherwise takes the service jump.  Every rule contains at least one
actual physical jump.  Competitors stop at their actual endpoint and actual
target, which selects the next rule immediately.  Therefore the episode
times are strict stopping times and no zero-duration classifier cycle is
introduced.

The potential is nonnegative and proper because \(V\ge H\).  A finite
\(V\)-sublevel contains finitely many populations and finitely many marks.
Every episode has bounded jump count and bounded displacement, so its positive
endpoint increment is integrable uniformly on a localized start set.  The
stopped conditional sum therefore gives

\[
 \eta\,\mathbb E S_{n\wedge N_K\wedge\sigma_R}\le V(y).
\]

Letting the localization level and then the episode count tend to infinity
is valid by nonnegativity and Fatou/monotone convergence.  On non-hitting,
the endpoints contain infinitely many genuine jump times; nonexplosion forces
those times to diverge.  The displayed bound rules out non-hitting and gives
the stated finite mean endpoint-hitting bound.

Nonexplosion is also correctly verified: every population-increasing channel
has aggregate rate at most linear in population, while the quadratic top
channels preserve the positive workload \(H\) and cannot accumulate inside a
finite population sublevel.  A finite mean return cycle to the finite marked
set produces a finite invariant occupation measure.  Irreducibility
normalizes it, and projection over the finite target mark proves positive
recurrence of the physical class.

## 8. Exact derivative transfer and render checks

The current 414-line target was mechanically reversed through exactly three
source hunks:

1. the one-line display (1.1) was restored from its two-row `aligned` layout;
2. the one-line display (1.2) was restored from its two-row `aligned` layout;
3. the final recurrence and scope prose was restored from its shorter,
   logically equivalent wording.

The reconstructed file has exactly 411 lines and 15,622 bytes, and its
SHA-256 is exactly

~~~text
62f5995bdd2915745468652bcb8ae891ca744a9e94f607f6bf38fbb63a397718
~~~

Thus these are not merely the only visible changes: reversing precisely
these three hunks reproduces the earlier mathematical freeze byte for byte.
The first two hunks change only TeX layout.  In the third hunk, “finite mean
hitting from every marked state” is shortened to “finite mean hitting” in
the scope of Lemma 6.1, and “take one jump and apply the same bound to its
finitely many successors” is equivalently shortened to “one jump has
finitely many successors, each with the same bound.”  “Projecting away” the
finite mark is rephrased as “forgetting” it.  The final family description is
also only reordered.  No hypothesis, formula, stopping rule, estimate, or
conclusion changes.  The strict mathematical verdict therefore transfers to
the current target.

The audited hash, line count, and byte count were recomputed directly before
and after the proof replay.  A scan found no NUL bytes, carriage returns, or
other forbidden control characters.

The exact Markdown was converted with Pandoc's single-backslash TeX-math
reader mode and compiled with Tectonic.  The current target builds as a
seven-page letter-size PDF with zero Pandoc or Tectonic diagnostics.  All
seven pages were inspected.  The split opening displays, every equation tag,
the theorem block, and the compressed final scope paragraph are legible and
unbroken, and there is no orphan final page.

## 9. Final verdict

The frozen theorem proves classwise positive recurrence for all 24
anisotropic residual incidences, for every strongly connected orientation and
every positive labelled rate choice, including all boundary faces.  Its
single marked quotient potential, finite all-clock episode menu, and
physical-time Foster interface are complete.  **STRICT PASS.**
