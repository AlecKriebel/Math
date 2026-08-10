# Expert audit note

This note orients a subject-matter expert to the load-bearing claims in the
Version 1.0 publication candidate. It is not a substitute for reading the
proof. Suggested falsification checks are listed separately in
`supplement/reviewer_checklist.md`.

## 1. Exact theorem

For every positive rate vector, every finite stochastic mass-action network
that is weakly reversible, has one linkage class, and has molecularity at most
two at every complex has a nonexplosive minimal CTMC on each closed
communicating class. Every nonabsorbing such class is positive recurrent;
each absorbing singleton has its point-mass stationary law. Every closed
class has a unique stationary probability distribution.

The statement is class-wise. It retains coordinate faces, siphons, parity
constraints, conservation relations, and other lattice restrictions rather
than assuming irreducibility on all of \(\mathbb N_0^d\).

## 2. Exact 2020 hypothesis removed

Anderson, Cappelletti, and Kim (2020) proved the binary one-linkage result
under the additional requirement

\[
  \{S_i,2S_i\}\cap\mathcal C\ne\varnothing
  \qquad\text{for every species }S_i.
\]

Thus every species had to occur in a pure unary or pure-double complex. The
present theorem removes that condition, so the 2020 theorem is a special case.
The manuscript gives a source-specific comparison with their tier/path
construction; the comparison should be checked against the cited locations
in the original paper rather than inferred from its abstract.

## 3. Relation to classical chemical-reaction-network entropy

For residual population \(r=x-t\), Stirling's formula gives

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

The entropy/log-factorial growth is classical. The point to audit is the new
target shift: the potential is applied after subtracting the complex actually
produced by the preceding reaction channel. The manuscript does not identify
its potential with the Horn--Jackson function and does not attribute the
marked-target construction to the classical sources.

## 4. Marked target and exact identity

The embedded chain records the target \(t\) of the actual labelled reaction
channel that most recently fired. If the post-jump population is \(x\), then
\(r=x-t\ge0\). For a next channel \(s\to u\),

\[
  V(x-s+u,u)-V(x,t)
  =\log\frac{(x)_t}{(x)_s}.
\]

Following the carried target, \(s=t\), therefore has exactly zero potential
increment. The exact channel label matters when different reactions have the
same population displacement.

## 5. Finite-path scalar propagation

A target-following episode selects a directed path from the carried target to
a terminal complex and continues only while the designated channels fire. A
deviation terminates the episode. Its continuation probability is exactly a
rate-constant factor times the enabled-source probability. The scalar envelope

\[
  F_q(M)=\sup_{0<p\le1}\{\log p+C_0+qpM\}
\]

is nondecreasing in \(M\). This monotonicity makes the backward induction
explicit: a terminal upper bound tending to \(-\infty\) propagates through
every finite target-following path, even when intermediate propensities have
separated scales.

## 6. Normalized-log top-complex alternative

Every divergent residual sequence is compactified by normalized logarithms.
Species may diverge on slower tiers while having limiting weight zero; they
remain in the divergent-coordinate set. Molecularity at most two yields the
critical dichotomy: either a useful terminal complex has vanishing source
probability, or a signed linear stoichiometric invariant prevents the proposed
divergence inside the fixed communicating class. The equivalence between top
complexes and unit normalized source weight also removes a formerly redundant
branch: if every complex has unit weight, every complex is top.

## 7. Qualitative and rate-dependent limitation

The proof establishes that its exceptional set \(K\) is finite and nonempty,
but does not give a useful general estimate of its location or diameter. For
the cycle

\[
  0\xrightarrow{\kappa_0}A
  \xrightarrow{\kappa_1}A+B
  \xrightarrow{\kappa_2}0,
\]

the exact episode recursion at \(x=(m,0)\) with carried target \(A\) has
leading drift

\[
  -\frac{\kappa_2}{\kappa_1+\kappa_2}\log m
  +O\!\left(\frac{\log m}{m}\right).
\]

The negative coefficient can approach zero through positive rate ratios.
Consequently, no rate-independent bound on \(K\) can be inferred solely from
the numbers of species and complexes. Effective rate-dependent recurrence,
tail, and mixing bounds remain open.

## 8. Exact class-wise scope

The proved conclusion begins on an already-closed communicating class. It
does not establish finite expected entrance from every arbitrary nonclosed
initial state into the union of closed irreducible components. Absorbing
singletons are handled separately by their point-mass stationary law; positive
return-time arguments concern nonabsorbing classes.

## 9. Multiple-linkage obstruction

The target-following mechanism needs a directed path from the carried target
to a terminal complex selected by the compactification argument. With several
linkage classes, a target in one class need not have any directed path to a
useful terminal in another class. The present proof therefore does not make
the multiple-linkage extension routine, and the manuscript does not claim the
full weakly reversible stochastic positive-recurrence conjecture.

## 10. Reproducibility route

From the release directory:

```bash
cd code
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
./reproduce.sh
```

The script runs exact identity, boundary, scalar-envelope, top-complex,
rate-degeneration, finite-calibration-chain, and absorbing-singleton tests; it
also requires two byte-identical canonical reports. The finite tests are
falsification tools, not a proof of the theorem or of the size of \(K\).

Release hashes and the clean-clone environment are recorded under
`validation/`. The targeted mathematical replay is in
`supplement/publication_v1_targeted_proof_audit.md`, and durable file hashes
are in `supplement/MANIFEST.sha256`.

## Claims deliberately not made

No claim is made for multiple linkage classes, molecularity above two, finite
expected class entry from every initial state, product-form stationary
distributions, explicit stationary formulas, quantitative tails or transient
excursions, mixing rates, exponential ergodicity, or bounded sample paths.
