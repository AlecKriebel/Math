# Independent acceptance: initialized critical-gap bootstrap

Accepted input: `pass5_coupling/CRITICAL_GAP_BOOTSTRAP.md`, SHA256
`4bdaf8be8eafc74fc9bb4c590bef15cb0feb30797c73d429bc8d2933bdc9a923`.
This accepts the conditional reduction, its age indexing and initialization,
not the unproved family of geometric hypotheses A_k or C_k. The full target
remains unresolved.

## 1. State indexing and tail counts

Immediately before actual move n, relative target j means absolute target
n+j-1. A known pair whose relative time is at least j in a lead-H history
must have been announced at r>=n+j-1-H, and known announcements have r<=n-1.
This interval has exactly H-j+1 integer round indices. Distinct pairs need
distinct witnesses, giving the asserted tail bound. No relative target
larger than H can remain. Negative or zero early round indices only
strengthen the bound because no such announcements occurred.

The before-move state is the same physical boundary as the preceding
post-announcement state; there is no extra Devil announcement before the
Angel's next move. The unrestricted W_(k+1) recursion therefore has exactly
one safe Angel move followed by every possible Devil announcement and W_k
of the shifted successor.

For H=k+14, the tail at the newly inspected layer j=k+1 is at most
H-(k+1)+1=14. Thus the numeric age statement is exact. Not imposing the
spatial cone in the stated admissibility class only strengthens its
hypothesis; unreachable pairs can be deleted without changing W_k.

## 2. Sufficient geometric premises

C_k assumes the implication on all finite pending states of total size at
most k+14. Since H-admissibility implies this total bound when H=k+14,
C_k implies A_k. The converse need not hold, and neither all-depth family
is established by the two accepted small-depth cases.

For k=1, an immediately viable state with no safe two-move continuation
needs at least sixteen current/next pairs by the accepted local neighborhood
lemma. This verifies the stated C_1 base. The cited accepted W_2 implies W_3
result for at most sixteen pending pairs supplies C_2. No propagation from
these cases to higher k is asserted or inferred.

## 3. Nonvacuous initialization and robust continuation

Assume the entire family A_k for k>=2. Suppose an infinite strategy for
maximum lead H-1 is already established, and let k=H-14. Starting from empty,
only announcements made at r>=1 and targeting t<=k can affect a k-move
horizon, and their effective leads satisfy t-r<=k-1<=H-1. Thus the prior
bounded-lead strategy, run on a history that replaces irrelevant pairs by
null announcements, wins that finite unrestricted horizon. An adaptive
Devil can retain all discarded real information internally in the virtual
simulation, as in the accepted all-finite-leads reduction. Therefore this
projection does not weaken the adversary. It proves W_k(empty).

At every actual lead-H state, chronology gives H-admissibility. If W_k
holds, A_k gives unrestricted W_(k+1), which supplies an immediately safe
move whose successor is in W_k after every announcement. The actual Devil's
lead-H actions are a subset of those universally quantified actions.
Chronology remains valid in the successor. This is an infinite invariant
argument including every death check and adaptive update.

Starting from the accepted lead-fifteen win, induction establishes each
lead H>=16 under the stated hypotheses. The accepted finite-horizon
compactness reduction then yields a single infinite unrestricted strategy.
No uniformity or compatibility across H-dependent strategies is required.

## 4. What is and is not proved

The initialization induction is a genuine sufficient mechanism and avoids
the vacuous-large-depth loophole. The unresolved mathematical content is
A_k for all k>=3, or another all-H robust invariant with a proved empty base.
The accepted two cases, the fact that finite arenas eventually stabilize,
and an asymptotic lower bound on some critical preload sizes do not by
themselves supply that content.

This audit does not certify any separate mass-obstruction file mentioned
in the input. It accepts the exact conditional reduction only.
