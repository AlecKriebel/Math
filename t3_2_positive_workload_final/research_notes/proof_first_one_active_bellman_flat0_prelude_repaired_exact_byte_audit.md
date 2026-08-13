# Exact-byte hostile audit of the repaired one-active Bellman/Flat0 prelude

**Independent proof-first audit, 2026-08-12 PDT.**  This audit freezes the
exact target

```text
research_notes/proof_first_one_active_bellman_flat0_prelude_repaired.md
SHA-256 f8ad11189d41fc5f1d09d0cf306c90d77a9b2b4b18cd00fe3dc06918d762c19b
295 lines, 12097 bytes
```

The verdict is **STRICT PASS** at these exact bytes.  The pass is scoped to
the one-active Bellman/degree-zero-flat seam stated in Theorem 6.1.  It is not
a recurrence theorem for support pairs outside that seam and is not a global
potential-switching theorem.

## 1. Hostile questions replayed

The audit attacked the following load-bearing points.

1. Is the marked factorial identity valid at the actual physical endpoint,
   with the actual target as the next mark?
2. Does a Bellman mark admit a one-active proof, rather than silently invoking
   a theorem whose formal statement is limited to two-active charts?
3. Does the Flat0 prelude retain every physical clock and avoid conditioning
   on a future activation?
4. Is the finite phase kernel genuinely transient when a closed no-access
   class is reachable?
5. Are structural exit, top access, degree-zero Bellman launch, and closed
   no-access absorption disjoint events?
6. Is the launch reaction counted exactly once at the Bellman handoff?
7. Are reaction count, physical time, and positive endpoint reward uniformly
   controlled?
8. Is the final probability split exhaustive even when top access has no
   uniform lower bound over unrelated phases?

All eight checks pass.

## 2. Marked identity and one-active Bellman path

For a physical jump $y\to z$, the endpoint/mark convention gives exactly

\[
 F(x-y+z,z)-F(x,t)=\log{(x)_t\over(x)_y}.
\]

Aggregating by the next source yields the displayed entropy identity and the
uniform positive-moment estimate.  There is no missing target-dependent
correction.

Section 2 then proves the required one-active corollary directly.  From every
actual Bellman target, strong connectivity supplies a simple same-linkage
path to $c$.  At its success endpoint $x-t+c\ge c$, coordinatewise
dominance in the bounded coordinates enables $q$, and $q_X=1,c_X=0$
gives

\[
 p_c(x-t+c)\le {K_c(x-t+c)_c\over K_q(x-t+c)_q}=O(X^{-1}).
\]

The all-clock recursion

\[
 J_m=D_m,\qquad J_i=D_i+a_iJ_{i+1}
\]

includes every competing reaction in $D_i$.  The first rare prefix source
has $D_i\to-\infty$; earlier designated probabilities are bounded below on
the fixed source-ratio cell, and a later positive tail is multiplied by a
vanishing designated probability.  Thus the stopped reward is coercively
negative unless a finite success prefix records a physical structural exit
with positive probability.  This proof uses one diverging coordinate and
does not rely on the two-active wording of the frozen parent theorem.

## 3. Finite Flat0 phase and absorption

Before top access, every in-chart continuing reaction has source of
$X$-degree zero.  On the fixed padded inactive box its rate is independent
of the escaping value of $X$.  Exit is assigned first priority, and the four
absorbing sections are literally disjoint:

\[
 E_{\rm out},\qquad A,\qquad B,\qquad C.
\]

Every closed no-access communicating class is put into $C$ before the
remaining kernel $Q$ is formed.  Hence that remaining finite substochastic
kernel is transient, $\rho(Q)<1$, without assuming that $C$ is
unreachable.  The carried flat target is enabled and has a positive outgoing
label, so total hazard is uniformly bounded below.  Geometric absorption
therefore gives all fixed moments of reaction count and physical duration.

Flat-prefix reward telescopes between two states in a finite inactive phase;
it does not accumulate once per attempted transition.  A degree-zero launch
or an exit-causing jump also has bounded positive reward.  At top access, the
ordinary next all-clock jump has expected charge at most
$-\log X+O(1)$.  At a degree-zero launch, the included launch is the last
prelude jump; its actual target starts the Bellman path and is not counted a
second time.

For each fixed starting phase the absorption probabilities are independent
of $X$ and satisfy

\[
 a_e+b_e+c_e=1.
\]

The target makes the complete split explicit:

* $c_e>0$: the closed irreducible physical class is finite;
* $c_e=0,a_e>0$: the finite mixture is coercively negative, unless a
  Bellman continuation has positive structural-exit probability;
* $c_e=a_e=0$: $b_e=1$, so the rule records an exit.

No uniform activation probability is inferred or needed.

## 4. Fixed-class and Foster interfaces

Inside $C$, no Bellman source and no structural exit is enabled; only the
degree-zero flat linkage acts and $X$ is constant.  For the entrance value
of $X$, the represented physical populations form a finite closed subset.
Reachability inside a closed irreducible population class forces that whole
class to equal the finite subset.

All nonclosed alternatives use the single proper marked potential

\[
 W(x,t)=1+\sum_i\log((x_i-t_i)!).
\]

Uniform positive endpoint moments and duration moments justify adding a
small physical-time toll.  The result is exactly the random-time Foster
alternative stated in Theorem 6.1.  Every endpoint is physical and every
jump is counted once.

## 5. Render replay

The exact bytes were rendered independently with Pandoc's single-backslash
TeX-math reader, both to MathJax HTML and through Tectonic to PDF.  Tectonic
produced zero stderr bytes; the PDF has six
letter-sized pages and was visually checked.  No clipping, overfull display,
missing equation, or hash overflow was found.

## 6. Frozen verdict

**STRICT PASS** for SHA-256

\begingroup\scriptsize\ttfamily
f8ad11189d41fc5f1d09d0cf306c90d77a9b2b4b18cd00fe3dc06918d762c19b
\par\endgroup

The exact repair supplied by this target is the unconditioned finite Flat0
prelude plus the explicit one-active Bellman corollary; neither interface is
left to an informal activation argument.
