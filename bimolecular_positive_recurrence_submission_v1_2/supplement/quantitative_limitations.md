# Quantitative limitations of the recurrence proof

The theorem is qualitative. For every fixed positive rate vector it proves
that the exceptional set $K$ used in the random-time Foster construction is
finite, but it does not give a practically useful rate-dependent estimate of
the location or diameter of $K$. No finite atlas, random stress test, or
simulation certifies this finiteness; it follows only from the analytic
compactness and top-complex argument.

## Exact rate-degeneration example

Consider the weakly reversible one-linkage bimolecular cycle

\[
 0\xrightarrow{\kappa_0}A
 \xrightarrow{\kappa_1}A+B
 \xrightarrow{\kappa_2}0,
 \qquad \kappa_0,\kappa_1,\kappa_2>0.
\]

At population $x=(m,0)$, $m\ge2$, carry target $A$. The residual is
$r=(m-1,0)$. Follow the unique simple path
$A\to A+B\to0$, and after reaching terminal complex $0$, take the final
ordinary jump required by the episode definition.

At the first phase, the expected one-jump reward and continuation probability
are

\[
 d_A=\frac{\kappa_0}{\kappa_0+\kappa_1m}\log m,
 \qquad
 \alpha_m=\frac{\kappa_1m}{\kappa_0+\kappa_1m}.
\]

At population $(m,1)$ with carried target $A+B$, they are

\[
 d_{A+B}=\frac{\kappa_0}
 {\kappa_0+(\kappa_1+\kappa_2)m}\log m,
 \qquad
 \beta_m=\frac{\kappa_2m}
 {\kappa_0+(\kappa_1+\kappa_2)m}.
\]

After the designated reaction $A+B\to0$, the population is $(m-1,0)$
and the carried target is $0$. The final ordinary jump has expected reward

\[
 d_0=-\frac{\kappa_1(m-1)}
 {\kappa_0+\kappa_1(m-1)}\log(m-1).
\]

Therefore the exact finite recursion is

\[
 D_0(m,A)=d_A+\alpha_m\bigl(d_{A+B}+\beta_m d_0\bigr).
\]

For fixed positive rates,

\[
 D_0(m,A)
 =-\frac{\kappa_2}{\kappa_1+\kappa_2}\log m
 +O\!\left(\frac{\log m}{m}\right),
 \qquad m\to\infty.
\]

In particular, the weaker requested form with an $O(1)$ remainder is valid.
The negative coefficient is nonzero for each fixed positive rate vector, but
its magnitude can be made arbitrarily small: with
$\kappa_1=1$ and $\kappa_2=1/N$, it is exactly $1/(N+1)$.

The terminal ordinary jump must not be omitted. Without it, the two
designated target-following jumps have zero immediate reward and the
remaining deviation terms are small and positive; the restoring
$-\log(m-1)$ term appears precisely at the terminal one-jump phase.

## No rate-independent bound on this proof's exceptional set

For this directed cycle, the simple path between each ordered pair of
distinct complexes is unique, so the path-library choice is unambiguous. At
the marked state $z_m=((m,0),A)$, the other two terminal episodes have

\[
 D_A(m,A)=d_A>0,
 \qquad
 D_{A+B}(m,A)=d_A+\alpha_m d_{A+B}>0.
\]

For fixed $m$, as $\kappa_2\downarrow0$, one has
$d_{A+B}\to d_A$ and $\beta_m d_0\to0$, and hence

\[
 D_0(m,A)\longrightarrow d_A(1+\alpha_m)>0.
\]

Thus, for every arbitrarily large $m$, there is a positive choice of
$\kappa_2$ for which all three terminal drifts exceed $-1$, so
$z_m\in K$. The cycle has one closed communicating class: from any state
one can reduce to $(0,0)$ by the displayed reactions, and from $(0,0)$
one can build any population. The marked state $z_m$ is reachable after a
$0\to A$ jump from $(m-1,0)$.

Moreover $z_1=((1,0),A)$ has residual zero and globally minimizes $V$, so
$z_1\in K$ for every rate vector. For the rate vector chosen above,
$K$ therefore contains both $z_1$ and $z_m$, whose population
$\ell^1$-distance is $m-1$. Consequently no bound depending only on the
number of species and complexes can control the location or diameter of this
proof's $K$ uniformly over all positive rate vectors.

This conclusion does not say that $K$ is infinite for a fixed rate vector;
the theorem proves the opposite. It says that the finite set can move
arbitrarily far out as rates degenerate.

## Claims not supplied by the theorem or verifier

The proof and computational package do not provide:

- a usable upper bound on the location, diameter, or cardinality of $K$;
- quantitative tail bounds for the stationary distribution;
- an explicit stationary formula or product form;
- a spectral gap, convergence rate, or mixing-time estimate;
- exponential ergodicity;
- a uniform bound on transient excursions.

Weak reversibility does imply, by the lifted state-cycle lemma, that the
reachability set of every initial population is already a closed communicating
class. This combinatorial closure fact supplies no additional quantitative
return-time, tail, or mixing estimate.

Effective rate-dependent recurrence, tail, excursion, and mixing bounds
remain open. The deterministic finite atlases and fixed-seed tests are
falsification tools and regression checks only. They do not prove recurrence,
do not enumerate $K$, and do not replace the analytic compactness proof.
