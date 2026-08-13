# Independent hostile audit of the mixed-111 fast Schur theorem

**Audit time:** 2026-08-12 00:47 PDT.  
**Frozen target:** `proof_first_mixed111_fast_schur_resolvent.md`.  
**Target SHA-256:**

```text
50696e88cc6c195f106331f27cab4af8566a693f983947d486ad1cf9c903692e
```

## Verdict

**STRICT PASS in the stated mixed generalized one-active scope.**

The proof establishes the stopped local theorem for the 111 mixed support
templates at entrances

\[
                         (U,V,I)=(u,n,0),\qquad u=n^{o(1)},
\]

with a historically reachable positive incoming reflected \(V\)-mark.  The
proof is uniform over every fixed strong orientation and every fixed positive
rate vector.  I found no orientation, population, residue class, endpoint, or
time-accounting counterexample to any of the scoped claims.

This verdict does **not** cover the six separated supports, the seventeen
exact base-open supports, the twelve no-history supports, the extra physical
two-active templates, pair composition, recurrence, or T3-2.  It also does not
reinstate the false two-sided terminal entropy equalities in the older note.
The frozen target correctly proves only the upper inequality needed by the
common fourth-power Foster estimate.

## 1. Scope replay

Let

\[
 {\cal B}=\{0,U,2U\},\qquad {\cal C}=\{I,2I,U+I\},\qquad q=V+I.
\]

I replayed the canonical 146-support table using only the following support
predicates, with no orientation enumeration:

* exact base-open: the proper support is \(\{aU,q\}\);
* mixed: after deleting \(q\), at least one linkage meets both
  \({\cal B}\) and \({\cal C}\);
* no-history: all proper ordinary complexes lie in \({\cal C}\), and the
  lower linkage lies in \({\cal B}\);
* separated: the proper ordinary complexes lie in \({\cal B}\), and the
  lower linkage lies in \({\cal C}\).

Giving exact base-open priority, the counts are

\[
   17\text{ exact base-open},\quad111\text{ mixed},\quad
   12\text{ no-history},\quad6\text{ separated}.
\]

The sorted support-and-label payload has SHA-256

```text
095650d07fbda263683cf6d1bdf341729cce090bb88a70538e080290d53b6568
```

Thus the two abstract hypotheses in Section 1 of the target—mixedness and
exclusion of an exact proper pair \(\{aU,q\}\)—select exactly the intended
111 supports.  This finite replay is scope bookkeeping only; no probability
estimate below is inferred from it.

## 2. Exact Schur outcomes

At a no-fast base, a source \(y=c_yU\) can have only the following clean
outcomes.

1. A base target \(z=c_zU\) gives
   \(u'=u-c_y+c_z\).
2. A cofactor target \(z=c_zU+b_zI\) leaves \(R=0\), \(b_z\ge1\), so the
   next \(q\)-firing is the first strict downcrossing.  Its retained endpoint
   is exactly (2.5) of the target.
3. A target \(q\) first leaves \((R,I)=(1,1)\).  The first \(q\)-firing
   either returns to the no-fast face, or leaves \((R,I)=(0,b_t)\) with
   \(b_t\ge1\), in which case the second \(q\)-firing is strict service.

All \(q\)-edges share the factor \(VI\), so their conditional target law is
state-independent.  These three alternatives prove that a clean opening has
at most two fast windows, and they give

\[
 |U_D-u|\le4,\qquad0\le I_D\le3,
\]

at the actual service endpoint.

The only clean macro that restores the complete physical population is

\[
                         aU\longrightarrow q\longrightarrow aU.
\]

Deleting this outcome and summing its geometric repetitions gives exactly
the normalized kernels \(Q\) and \(S\), rather than a cemetery
approximation.  No other same-\(U\) clean continuation is possible: there is
only one base complex of each \(U\)-degree, and an ordinary cofactor outcome
is killed at strict service.

## 3. Uniform diagonal inverse

Fix a possible return pair \(\{aU,q\}\).  If either return edge is absent,
its diagonal probability is zero.  If both are present, the proper support
has a vertex outside this pair.  Strong connectivity forces an edge from the
pair to its complement.  Its source is either \(aU\), in which case it has
the same falling-factorial source as the opening, or \(q\), in which case it
has a fixed positive conditional probability among the \(q\)-targets.

Consequently every traversal of the return pair has an orientation- and
rate-dependent but \(u,n\)-independent chance \(\delta>0\) to leave it.
The number of erased clean returns has a geometric tail.  This is exactly the
place where the excluded exact base-open supports would fail; no such support
is present in the 111 block.

## 4. Sourcewise two-window defect estimate

During a clean fast window before service,

\[
 V\ge n,\qquad1\le I\le2,\qquad U\le u+4.
\]

Hence the fast hazard is at least \(cnI\), while all nonfast hazards together
are at most \(C(1+U+I)^2\).  At each of the at most two windows,

\[
 {\mathbb P}(\hbox{nonfast first}\mid\hbox{actual open state})
       \le {C(1+u)^2\over n}.
\]

The first nonfast firing is included, and one binary firing changes each
coordinate by a fixed amount.  Therefore its degree-\(p\) endpoint-weighted
mass is at most

\[
                      {C_p(1+u)^{p+2}\over n}.
\]

The same estimate survives the exact-return inverse because every clean
return restores the same physical population and the return count has the
fixed geometric tail established above.  This verifies (3.3)--(3.7)
sourcewise at the actual shifted state; it does not use a supremum over the
cutoff box.

## 5. Maximal-source killing and accessibility

Let \(d\) be the maximum base degree present in either linkage.  Every
nonself clean macro sourced at \(dU\) is either service or a strict decrement
of \(U\).  Indeed, a base continuation can only target a smaller base degree;
the only equal-degree target is the deleted exact return.  Every positive
continuation is sourced at degree at most \(d-1\).  The strong-cut argument
above ensures that the effective degree-\(d\) nonself mass is nonzero.  Thus

\[
 \Lambda(u)\asymp(1+u)^d,
 \qquad {\mathbb P}_u(U_1>u)=O((1+u)^{-1}),
\]

and a fixed fraction of the leading mass strictly decreases or is killed.

Accessibility on compact populations is also valid.  From any enabled base
complex in a mixed linkage, follow a directed path to the first ordinary
cofactor complex.  The residual \(U\)-population is nonnegative and preserved
along the path.  If the path visits \(q\), choose its next edge with its fixed
positive conditional probability.  The first ordinary cofactor state at
\(R=0\) is followed by strict service.

If that mixed base is not initially enabled, an enabled base-only linkage can
reach its maximal base degree.  The only residual degree pattern not handled
immediately is \(m=1,e=2\); its base support contains \(0,U\), and repeating a
positive path from \(0\) to \(U\) raises the population to two.  If no base
source is enabled, the physical point is absorbing.  Inside a closed
irreducible physical class it therefore forms a singleton class, whose
reachable reflected lift starts with zero mark.  Such a point cannot be a
relevant positive-debt base.  Clean no-service continuations preserve the
incoming positive mark, so they cannot enter one.

This proves both compact killed transience and the marked static-state
exclusion without declaring an arbitrary physical face to be serviceable.

## 6. Killed Green bounds

For

\[
 F_\theta(u)=\exp\{\theta u\log(u+e)\},\qquad0<\theta<1/2,
\]

a positive jump of size at most two multiplies \(F_\theta\) by at most
\(Cu^{2\theta}\), but all positive jumps together have probability
\(O(u^{-1})\).  The leading decrement-or-kill mass has fixed positive size.
It follows that \(QF_\theta\le\rho F_\theta\) outside a compact set for some
\(\rho<1\).  Compact killed transience supplies a bounded Green corrector.
Using a smaller exponent \(\theta'<\theta\) then gives

\[
                   (I-Q)^{-1}F_{\theta'}\le C F_\theta.
\]

Optional stopping of the corrected nonnegative supermartingale gives the
maximal tail

\[
 {\mathbb P}_u(\max U\ge k)
   \le C F_\theta(u)\exp\{-c k\log(k+e)\}.
\]

For polynomial weights, a leading decrement loses order \(u^m\) from
\((1+u)^{m+1}\), whereas the aggregate positive-jump contribution is only
\(O(u^{m-1})\).  Therefore

\[
 (I-Q)(1+u)^{m+1}\ge c_m(1+u)^m
\]

outside a compact set.  If \(b_m\) is the compactly supported deficit, the
explicit correction \(\chi_m=(I-Q)^{-1}b_m\) makes the inequality global.
Applying \((I-Q)^{-1}\) proves the polynomial occupation bound.  The usual
binomial recursion for the killed step count then proves every fixed count
moment.  These reconstructions validate (4.6)--(4.8), including the two
steps compressed in the target's prose.

## 7. Paid terminals and actual endpoint

The actual clean continuation kernel is entrywise below \(Q\): in the
geometric exact-return sum, imposing no insertion can only remove mass.
Summing the sourcewise defect estimate with the polynomial Green bound gives

\[
 {\mathbb E}[(1+U_E+I_E+|R_E|)^p;E_n]
       \le {C_p(1+u)^{C_p}\over n}.
\]

Before the first defect, \(I\) and \(R\) are absolutely bounded.  The
included defect changes them only by a fixed amount.  Hence a cutoff hit for
large \(n\) requires \(U\) to reach within a fixed distance of \(L_n\).
The exponential maximal tail pays both the path-labelled base endpoint
\(P_n\) and the other included boundary \(B_n\) faster than every power of
\(n\).  This remains true for a defect-caused boundary, because its prestate
is within a fixed \(U\)-distance of the cutoff.  Since
\(u=n^{o(1)}\), the factor \(F_\theta(u)\) is negligible relative to the
\(L_n\log L_n\) exponent.

The ideal trace is killed almost surely.  The only removed mass is defect or
boundary mass, so

\[
                         {\mathbb P}(D_n)=1-n^{-1+o(1)}.
\]

The endpoint in this statement is the actual state in (2.5) or (2.7), not a
cemetery point.

## 8. One-sided entropy and fourth power

For the spectator entropy

\[
 B_\ell(u)=\log(u!)+\ell_Uu,
\]

augmenting by \(C_0\log(u+e)\) with \(C_0>6\) pays every bounded spectator
gain at a leading-order service outcome.  A leading continuation strictly
decreases \(U\), and positive lower-degree continuations contribute only
\(O((\log u)/u)\).  Thus the augmented entropy has strict killed drift
outside a compact set.  The Green potential of the compact positive part is
a bounded nonnegative corrector.  Because the actual clean kernels are
subkernels and every function in the inequality is nonnegative, removing
defect and boundary mass preserves the upper inequality.

It follows at the actual service endpoint that

\[
 {\mathbb E}[B_\ell(U_D)-B_\ell(u);D_n]
       \le C\log(u+e)+C+{C(1+u)^C\over n}.
\]

Combining this with the exact active decrement \(-\log n\), the bounded
cofactor endpoint, and the paid exceptional labels gives only—and exactly—the
needed sign

\[
                         {\mathbb E}\Delta G_\ell
                              \le-\log n+o(\log n).
\]

The target explicitly exhibits a reachable mixed support where the
spectator entropy loses order \(u\log u\); hence no matching lower bound is
available.  The proof does not use one.

All fixed moments of \(\Delta G_\ell\) are \(n^{o(1)}\).  The physical
duration is also retained: no-fast holding moments are bounded, clean-return
counts have a fixed geometric tail, open holding times have rate at least
\(cn\), and the killed macro-count recursion gives

\[
                         {\mathbb E}\sigma_n^p
                              \le C_p(1+u)^{C_p}=n^{o(1)}.
\]

Finally, expanding \(W_\ell=G_\ell^4\) around the deterministic initial
value \(G_\ell(X_0)=\Theta(n\log n)\), the first term is strictly negative
of order \(G_\ell(X_0)^3\log n\), while the other three terms and the duration
reward are lower order.  Therefore (7.3) follows with the same population
potential used by adjacent charts.  The Schur, Green, and entropy correctors
are proof devices and do not alter the handoff state.

## Final audit statement

All requested replay points pass: exact Schur outcomes, strong-cut diagonal
inverse, support scope, marked compact accessibility, sourcewise shifted
two-window control, killed exponential and polynomial Green bounds, included
boundary endpoints, one-sided actual-terminal entropy, physical duration, and
the common fourth-power drift.  No repair to the frozen target is required.
