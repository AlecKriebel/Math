# Independent final audit of the hard exact-carrier entropy theorem

**Audit date:** 2026-08-12 PDT.  
**Verdict:** **STRICT PASS in the stated local analytic scope.**

The frozen inputs are

```text
theorem             3c18d0ee481e5c351663e4923b97473e871030c86ff37ca674f00688d66a047f
finite certificate  43788cb4a458f6950d9316959393efc7270fbb2ef52bbb2f82bca0b6da848e66
certificate tests   aa963d45f67388902ba2f8ebe40a95288b8deab4b32e3505243a168a24eab1dc
prior hostile audit 3254ab07684637a98353f19fe20d15cb196c8dd9492930090a5b18136de7a42f
```

This is a proof audit, not an orientation search.  I did not enumerate
orientations or inspect a finite state box in order to infer a stochastic
conclusion.  The finite replay below verifies only the nineteen support
premises.  The verdict covers the raw stopped macroscopic exact-carrier
episode for an arbitrary fixed strong orientation, arbitrary fixed positive
rates, and arbitrary fixed common correction vector \(\ell\).  It makes no
pair-recurrence or global T3-2 claim, and the upstream claim flags remain
false.

## 1. Exact carrier and sourcewise perturbation

For the proper pair \(\{aU,V+I\}\), level \(i\) has

\[
 (U,V,I)=(u-ai,v+i,i),\qquad
 {\pi_i\over\pi_0}
 =\rho^i{(u)_{\underline{ai}}\over
              i!(v+1)^{\overline i}}.
\]

If a lower edge has source \(y=cU+bI\), multiplying its source
factorial by this carrier weight and putting \(i=b+j\) gives exactly

\[
 {\kappa_e\rho^b(u)_{\underline{c+ab}}
       \over(v+1)^{\overline b}}
 \sum_{j\ge0}{\rho^j
 (u-c-ab)_{\underline{aj}}
 \over j!(v+b+1)^{\overline j}}.
\]

The ratio of consecutive summands is
\(O(s^{pa-q+o(1)}/(j+1))\).  Since the nineteen rows have
\(q-pa\ge1\), the series is \(1+O(s^{-1+o(1)})\), including uniformly
over a logarithmic number of bounded macros.  The resulting source exponent
is

\[
                  \phi(y)=p(c+ab)-qb.
\]

For two lower insertions, order the marked firing times.  In the
future-ordered term, the downward carrier Green potential bounds the
remaining lower hazard using the largest lower \(U\)-degree actually present:

\[
                    O(s^{pc_*-q+o(1)}).
\]

The killed carrier is reversible, so the past-ordered term is identical
after interchanging the two marked levels.  Edge-size bias leaves
\(i=b+J\), with every fixed moment of \(J\) bounded by the corresponding
Poisson moment of mean \(O(s^{pa-q+o(1)})\).  Consequently the relative
first-kill error is

\[
 O(s^{-\gamma+o(1)}),\qquad
 \gamma=\min\{q-pa,q-pc_*\}\ge1.
\]

The same potential at the shifted post-firing invariants supplies the
endpoint-weighted second-firing estimate.  This check is sourcewise and does
not use a quadratic supremum over all possible complexes.  In particular,
the \((p,q)=(4,5)\) row has \(a=0,c_*=1\), so its perturbation is paid by
\(u/v=s^{-1+o(1)}\); the false quantity \(u^2/v\) never appears.

## 2. Entropy gradient

A clean macro \(y\to z\) ends at

\[
 u'=u-w_a(y)+w_a(z),\qquad v'=v+b_y-b_z,
 \qquad w_a(cU+bI)=c+ab.
\]

The bounded-jump factorial identity therefore gives

\[
 \Delta G_\ell
 =\{p[-w_a(y)+w_a(z)]+q[b_y-b_z]\}\log s+o(\log s)
 =\{\phi(z)-\phi(y)\}\log s+o(\log s).
\]

Thus the exponent selecting the next source is exactly the negative
factorial-entropy gradient of its clean macro.  Every singleton maximizing
source must leave its singleton, so all eighteen singleton cases have an
immediate decrement of at least \(\log s+o(\log s)\).

## 3. The old pathwise counterexample remains valid

The unique nonsingleton row is

\[
 (p,q,a)=(1,3,2),\quad L_+=\{2U,V+I\},\quad
 L_0=\{0,I,2I,U+I\},\quad Y_*=\{0,U+I\}.
\]

The earlier hostile audit correctly rejected a pathwise negative-shell
claim.  Take the strong lower cycle

\[
       0\longrightarrow U+I\longrightarrow I
       \longrightarrow2I\longrightarrow0,
\]

put \(u=s\), \(v=\lfloor s^3/e\rfloor\), and take \(\ell=0\).  Fixed
rates may be chosen so that the two maximal-source outcomes select the
equality birth \(0\to U+I\) with limiting probability \(9/10\) and the
strict exit \(U+I\to I\) with limiting probability \(1/10\).  After
\(m=\lceil2\log s\rceil\) equality births, followed by the strict exit,
the exact entropy increment is

\[
 \sum_{k=0}^{m-1}
 \log{(u+3k+1)(u+3k+2)(u+3k+3)\over v-k}
 -\log(u+3m)
 =(1+o(1))\log s>0.
\]

This is a clean path of positive probability before any admissible cap.
The independent audit certificate replays it at \(s=10^4\), where the exact
increment is approximately \(9.94896>0\).  Hence a pathwise negative sign
would still be false.  The frozen theorem does not assert one.

## 4. Why the killed-overshoot repair closes the gap

Let \(k\) count equality births and put

\[
 U_k=u+3k,\qquad V_k=v-k,\qquad H(k)=G_\ell(U_k,V_k,0).
\]

Up to the already paid \(O(s^{-1+o(1)})\) sourcewise perturbation, the
clean birth, death, and strict-exit rates have the form

\[
 b_k=B,qquad
 d_k=D{(U_k)_{\underline3}\over V_k+1},\qquad
 r_k=R_0+R_1{(U_k)_{\underline3}\over V_k+1}.
\]

Strong connectivity supplies all three structural inequalities needed by
the killed chain:

\[
 B+R_0>0,qquad D+R_1>0,qquad R_0+R_1>0.             \tag{4.1}
\]

The first two say that each equality source has an outgoing edge; the third
says that the proper subset \(Y_*\) has a strict directed cut.  These
conditions cover arbitrary missing equality directions as well as the case
where both are present.

When both directions occur, adjacent detailed balance is

\[
 {d_{k+1}\over b_k}
 =C_*\exp\{H(k+1)-H(k)\}[1+O(s^{-1+o(1)})].          \tag{4.2}
\]

Inside a fixed kinetic tube the two source scales are comparable.  Equation
(4.1) then makes the probability of selecting a strict cut uniformly
positive.  Above the tube, the \(U+I\) source dominates.  If \(R_1>0\),
killing is comparable to that dominant rate; if \(R_1=0\), (4.1) forces
\(D>0\), and the dominant death decreases \(H\).  Below the tube the
symmetric statement holds: either the \(0\)-sourced cut kills comparably or
the dominant birth decreases \(H\).  An uphill move of entropy height
\(h\) has, by (4.2), relative weight \(O(e^{-h})\).

Applying the embedded killed kernel to
\(\exp\{\theta[H-H(0)]_+\}\), \(0<\theta<1\), therefore gives a strict
Foster inequality.  Optional stopping, its move-marked version, and
layer-cake integration yield

\[
 \Pr\{\tau=C_M\log s\}\le s^{-M},\qquad
 \Pr\{\max_{j\le\tau}(H(k_j)-H(0))\ge h\}
   \le Ce^{-\theta h}+s^{-M},
\]

and every fixed moment of the positive pre-exit overshoot is bounded.
The old counterexample is now handled exactly as it should be: its long
positive path has exponentially small weight, rather than an impossible
pathwise sign.

On a strict exit the integer \(\phi\)-gap pays
\(-\log s+o(\log s)\).  The alternative entropy-threshold branch has
already paid \(-2\log s\), and the cap has arbitrarily small
endpoint-weighted mass.  Hence

\[
 \mathbb E\Delta G_\ell\le-(1-o(1))\log s,qquad
 \mathbb E|\Delta G_\ell|^r=O(\log^r s).
\]

This is an expectation-and-overshoot statement, not the refuted pathwise
statement.

## 5. Defects, boundaries, duration, and fourth power

At each of the \(O(\log s)\) occupied shell states, a nonmaximal source or
second lower firing has endpoint-weighted mass \(s^{-1+o(1)}\).  The
move-marked killed Green estimate sums these contributions without losing
their power.  A carrier level \(K\log s\) has a product tail with successive
ratio at most \(s^{-1+o(1)}/i\); even after the polynomial number of proper
openings it is superpolynomially small.  The move cap is paid the same way
by choosing \(M\) above the requested endpoint moment.

For physical time, the level-zero waiting time for a macro has fixed
\(s^{o(1)}\) moments because \(\max\phi\ge0\).  Proper openings have rate
at most \(s^{pa+o(1)}\), while a completed excursion has fixed
\(r\)-th duration moment \(O(s^{-qr+o(1)})\): its downward clock is at
least \(cVi\), and its upward/downward ratio is
\(O(s^{pa-q+o(1)}/i)\).  The compound-Poisson moment recursion and then the
time-marked logarithmic shell Green bound give

\[
                         \mathbb E\sigma^r=s^{o(1)}.
\]

The included boundary-causing reactions and the shifted cleanup estimates
give all fixed endpoint moments.  Finally, with
\(g=G_\ell(X_0)=s^{q+o(1)}\log s\), the exact identity

\[
 (g+H)^4-g^4=4g^3H+6g^2H^2+4gH^3+H^4
\]

shows that \(4g^3\mathbb EH\le-cg^3\log s\) dominates all higher
terms.  The duration term is negligible on this scale.  This proves the
stated local common-fourth-power inequality.

## 6. Finite scope replay and durable check

The independent replay starts from all 188 normalized physical hard
templates and selects exactly the nineteen proper supports
\(\{aU,V+I\}\).  It verifies

* the lower-complex universe;
* \(\min(q-pa)=1\);
* \(\min(q-pc_*)=1\);
* every maximizer set is a proper subset;
* \(\min\max\phi=0\); and
* the unique nonsingleton maximizer displayed in Section 3.

The frozen row digest is

```text
e931d5277596c5084d89bf63b3963a6fe0ecb202be6549075b47f89c30b0a33b
```

The independent audit artifacts are

```text
audit source  eafaa7e0254e01d6478d385a7e143e63ec6d8185fcb9389961189d83a2ff05fd
audit tests   f2cd19f4d0a16d1685b0665d7e7d01c2e554f29c57c4b3112919a1241d533440
audit payload 3f7a353473cceeec378bceb7136319e0d2dfca7174e864229aa9c05262565ad7
```

The original four certificate tests and six independent-audit tests pass.
The audit source verifies that all upstream analytic, pair, and global claim
flags remain false.  Its own verdict is local and analytic only.

There are two harmless copyediting slips in the frozen theorem: Section 1
says “four” before listing five structural facts, and the scoped theorem
says “three support identities.”  The proof and replay use the five listed
facts, together with the separately displayed carrier gap \(q-pa\ge1\).
These wording slips do not affect the strict analytic verdict.
