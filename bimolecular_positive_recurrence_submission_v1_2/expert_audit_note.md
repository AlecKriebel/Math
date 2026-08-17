# Expert audit note

This note orients a subject-matter expert to the load-bearing claims in the
Version 1.2 submission candidate. It is not a substitute for reading the
proof. Suggested falsification checks are listed separately in
`supplement/reviewer_checklist.md`.

## 1. Lifted state-space return cycle

Let an enabled channel $y\to y'$ fire at $x=r+y$, where $r\geq0$, and
produce $x'=r+y'$. Weak reversibility gives a directed complex path

\[
  y'=z_0\to z_1\to\cdots\to z_m=y.
\]

For every path edge, the population $r+z_j$ contains its source $z_j$, so
the corresponding channel is enabled and takes $r+z_j$ to $r+z_{j+1}$.
The lifted path returns from $x'$ to $x$. Thus every enabled one-step
population transition has a return path. Reversing each step of any
accessibility path in this sense proves that accessibility is symmetric.
Every reachable set is consequently one communicating class and is closed.

The argument includes the zero complex, boundary populations, parity and
lattice restrictions, labelled parallel channels, and coincident population
displacements: the lift consists of actual enabled channels and keeps the
same nonnegative residual throughout. At an absorbing singleton there is no
enabled genuine transition, so the assertion is vacuous and its reachability
set is already closed. This lemma uses weak reversibility but not one linkage
class or bimolecularity.

## 2. Exact theorem

Fix any initial population $x_0$. Its reachable population set
$\Gamma(x_0)$ is the closed communicating class supplied by Section 1. For
every positive rate vector, if the finite weakly reversible reaction network
has one linkage class and every complex has molecularity at most two, then the
minimal CTMC on every nonabsorbing $\Gamma(x_0)$ is nonexplosive and positive
recurrent. If
$\Gamma(x_0)$ is an absorbing singleton, its stationary law is the point
mass. Every reachability class therefore has a unique stationary probability
distribution.

The formulation retains coordinate faces, siphons, parity constraints,
conservation relations, and other lattice restrictions rather than assuming
irreducibility on all of \(\mathbb N_0^d\). There is no separate class-entry
problem under weak reversibility: $x_0$ lies in its closed reachability class
at time zero.

## 3. Exact Anderson--Cappelletti--Kim comparison

Anderson, Cappelletti, and Kim (2020) proved the binary one-linkage
positive-recurrence conclusion under the additional condition

\[
  \{S_i,2S_i\}\cap\mathcal C\ne\varnothing
  \qquad\text{for every species }S_i.
\]

The present theorem removes that condition and therefore contains their
positive-recurrence conclusion as a special case. The comparison should be
audited against their Section 6, without relying on version-dependent journal
page numbers:

1. Theorem 6.1 reduces positive recurrence to tier inclusion (11).
2. Lemma 6.5 constructs the finite reaction word.
3. Lemma 6.3(ii) converts strict D-tier descent into a negative contribution
   tending to minus infinity.
4. Lemma 6.4 assembles those ingredients in the sampled-chain argument.
5. In Section 6.1, equations (19)--(20), the pure-species assumption first
   supplies either $S_v$ or $2S_v$.
6. D-tier maximality excludes $2S_v$, so $S_v$ is forced.
7. The source propensity of $S_v$ then supplies the required comparison.

The accurate summary is: the assumption forces $S_v$ to be a complex after
$2S_v$ is excluded by D-tier maximality; $S_v$ then supplies the
source-rate comparison. It is not $S_v$ or $2S_v$ that supplies the final
comparison, and the manuscript makes no unsupported broader characterization
of the prior assumption.

## 4. Relation to classical reaction-network entropy

For residual population $r=x-t$, Stirling's formula gives

\[
  \sum_i\log(r_i!)
  =\sum_i(r_i\log r_i-r_i)
   +O\!\left(\sum_i\log(r_i+1)\right).
\]

This is a discrete, target-shifted analogue of the classical
pseudo-Helmholtz/Horn--Jackson family

\[
  G_c(r)=\sum_i\bigl[r_i(\log(r_i/c_i)-1)+c_i\bigr].
\]

The entropy/log-factorial growth is classical. The contribution to audit is
the target shift: the potential is applied after subtracting the complex
actually produced by the preceding labelled reaction channel. The manuscript
does not identify its potential with the Horn--Jackson function.

## 5. Marked target and exact identity

The embedded chain records the target $t$ of the actual labelled channel
that most recently fired. If the post-jump population is $x$, then
$r=x-t\geq0$. For a next channel $s\to u$,

\[
  V(x-s+u,u)-V(x,t)
  =\log\frac{(x)_t}{(x)_s}.
\]

Following the carried target, $s=t$, therefore has exactly zero potential
increment. The channel label matters when distinct reactions have the same
population displacement.

## 6. Finite-path scalar propagation and top-complex alternative

A target-following episode selects a directed path from the carried target to
a terminal complex and stops at the first deviation. The continuation
probability is exactly a rate-constant factor times the enabled-source
probability. The scalar envelope

\[
  F_q(M)=\sup_{0<p\leq1}\{\log p+C_0+qpM\}
\]

is nondecreasing in $M$, so a terminal upper bound tending to minus infinity
propagates backward along every finite path even when intermediate
propensities have separated scales.

Every divergent residual sequence is then compactified by normalized
logarithms. Species diverging on a slower tier remain in the divergent set
even if their limiting normalized weight is zero. Molecularity at most two
yields the critical alternative: either a useful terminal complex has
vanishing source probability, or a signed linear stoichiometric invariant
precludes the proposed divergence inside the class.

## 7. Qualitative and rate-dependent limitation

For the cycle

\[
  0\xrightarrow{\kappa_0}A
  \xrightarrow{\kappa_1}A+B
  \xrightarrow{\kappa_2}0,
\]

the exact episode recursion at population $(m,0)$ with carried target $A$
is

\[
  D_0(m,A)=a_m+p_m(b_m+q_mc_m).
\]

For fixed positive rates,

\[
  D_0(m,A)
  =-\frac{\kappa_2}{\kappa_1+\kappa_2}\log m
   +O\!\left(\frac{\log m}{m}\right).
\]

For fixed $m$, as \(\kappa_2\downarrow0\), one has $b_m\to a_m$ and
$q_mc_m\to0$, hence

\[
  D_0(m,A)\longrightarrow a_m(1+p_m)>0.
\]

The negative logarithmic coefficient can approach zero through positive rate
ratios. Thus no bound on the location or diameter of the proof's finite Foster
set $K$ can depend only on the numbers of species and complexes uniformly
over all positive rate vectors. No stronger quantitative claim is made.

## 8. Markov-chain and physical-time closure

The endpoint-chain proof identifies

\[
  W_n=V(Y_{n\wedge\sigma_K})+(n\wedge\sigma_K)
\]

as a nonnegative supermartingale and obtains finite mean hitting of $K$. A
finite trace-chain argument then produces finite positive return to one marked
state, expands trace excursions into ordinary embedded jumps, and projects to
a population return. A uniform positive lower bound on total population rate
converts finite jump-count return into finite physical return. Recurrent
visits to one population state contribute an almost surely divergent subseries
of independent positive exponential holding times, recovering nonexplosion.
The regenerative occupation formula yields the stationary probability law.

The propositions and their proofs remain in the manuscript. Additional
interface details are retained in the standalone
`manuscript/supplementary_note.pdf`.

## 9. Exact scope

The positive-recurrence theorem does not cover multiple linkage classes or
molecularity above two. The one-linkage condition is used to connect every
carried target to the terminal selected by the compactification; with several
linkage classes, that directed path need not exist. Bimolecularity is used in
the exhaustive top-complex alternative. The broader closure lemma does not
remove either hypothesis from the recurrence theorem.

No claim is made of a product form or other explicit stationary formula,
moment finiteness without integrability, quantitative tails, mixing rates,
exponential ergodicity, bounded sample paths, or useful general bounds on
$K$.

## 10. Reproducibility route

From the release directory:

```bash
cd code
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
./reproduce.sh
```

The suite includes exact identity and boundary tests, state-cycle lifting and
finite reachability-symmetry calibrations, scalar-envelope monotonicity, the
corrected rate limit and logarithmic coefficient, absorbing-singleton
handling, and finite-chain stationary return-cycle normalization. It requires
two byte-identical canonical reports. These checks are falsification tools;
no finite atlas or random test proves recurrence, enumerates $K$, or
certifies a useful bound on it.

Release identifiers and the replay procedure are recorded under `validation/`;
durable file hashes are in `supplement/MANIFEST.sha256`. The current audit is
`audit/publication_v1_2_submission_audit.md`; the focused Version 1.1
mathematical and primary-source replays remain, with their historical dates,
in `supplement/v1_1_mathematical_audit.md` and
`supplement/publication_v1_1_literature_audit.md`.
