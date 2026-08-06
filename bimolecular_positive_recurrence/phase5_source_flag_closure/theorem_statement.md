# Unrestricted single-linkage positive-recurrence theorem

## Theorem

Let \(G=(\mathcal S,\mathcal C,\mathcal R)\) be a finite stochastic
mass-action reaction network such that:

1. every complex has molecularity at most two;
2. the reaction graph has one linkage class and is strongly connected;
3. every nontrivial reaction has a positive rate constant.

Then every closed communicating class of the associated nonexplosive
continuous-time Markov chain is positive recurrent.

No assumption is made that a species occurs as a unary complex \(S_i\) or as
a pure binary complex \(2S_i\).  The theorem includes coordinate-face,
parity, lattice-restricted, siphon, conservative, and boundary classes.

## Stronger Foster statement used in the proof

For an infinite closed class, augment the embedded jump chain by the target
complex \(t\) of the most recent reaction.  For \(x\ge t\), put

\[
V(x,t)=\sum_i\log((x_i-t_i)!).
\]

There are:

- a finite set \(K\) of augmented states;
- one finite target-following episode for every ordered pair of complexes;
- a deterministic state-dependent choice among those episodes;

such that every selected episode has at most \(|\mathcal C|\) jumps and,
outside \(K\),

\[
\mathbb E_{(x,t)}[V(Z_\tau)-V(x,t)]\le -1.
\]

The current target is always enabled, so if \(\kappa_*\) is the smallest
nontrivial reaction rate, the physical duration of an episode is
stochastically dominated by a sum of \(|\mathcal C|\) independent
\(\operatorname{Exp}(\kappa_*)\) variables.

This finite-family random-time Foster certificate gives finite expected
hitting time of \(K\), and a finite trace-chain argument gives finite
expected return time to one state.
