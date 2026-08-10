# Finite-shell linkage activation and correction

## 1. Purpose

The one-linkage top-complex alternative sometimes identifies an available
terminal in a linkage different from the most recently fired linkage.  The
proof does not treat a stale formal ledger mark as physically enabled.
Instead it uses the following shellwise activation construction.

Fix a terminal chart, a rational workload shell band, a finite box for all
bounded coordinates, and the finite target-mark/lattice phase.  Pad the shell
band by the maximum displacement of a simple complex path.  The resulting
physical ledger state set is finite.

Let \(L\) be a linkage for which the certified one-linkage alternative gives
complexes \(s,c\in L\), with \(h(s)>h(c)\), such that the higher source \(s\)
is enabled over the lifted terminal \(c\).

## 2. Honest activation policy

The policy is fixed before future randomness is observed.

1. Wait until an actual channel of `L` fires, or until the process exits the
   padded shell/chart.
2. Its actual target `t` is enabled.  Select the fixed simple path in `L`
   from `t` to `c` and run exactly the certified target-following episode.
3. Continue only while the exact designated channel fires.  Stop immediately
   on every deviation, including a reaction in the other linkage.  If `c` is
   reached, take the prescribed final ordinary jump.

The episode has uniformly bounded jump length.  Every designated transition
is physical, and target following preserves one nonnegative residual vector.

## 3. Finite-mean activation

Before the first `L` reaction, kill on shell/chart exit or entry into a class
on which only the other linkage is active.  The padded shell and phase are
finite.  A closed nonabsorbing waiting class contains no `L` channel; its
physical dynamics is therefore the certified one-linkage reduction.  In all
other components the first `L` reaction or a declared exit has finite mean
physical time.  Appending the bounded target-following episode preserves
finite mean duration.

This argument allows arbitrarily fast neutral reactions and does not treat a
stale formal target as enabled.

## 4. Waiting-reward correction

Let \(\sigma\) be the first activation or structural exit, and let \(F\) be
the marked residual-factorial potential.  On the finite killed shell define

\[
 H_N(z)=\mathbb E_z[F(Z_\sigma)-F(z)],
\]

with \(H_N=0\) on the activation/exit section.  This is the unique finite
Dirichlet solution for the waiting reward.  Therefore the shell correction
\(\psi_N=H_N\) makes the expected corrected reward before the terminal
episode equal to zero.  Appending the certified terminal episode gives
expected corrected reward at most \(-1\) outside a sufficiently large chart
threshold.

The correction is bounded on each shell.  The inherited shell-adapted Foster
construction chooses shell offsets recursively so that these bounded
corrections and all seam overshoots are dominated.  No population-independent
duration bound or retrospective policy choice is used.
