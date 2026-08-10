# Primary literature scope check

This is a proof-interface check, not a priority or novelty audit. It records
why the standard published recurrence criteria do not by themselves certify
the inherited T3-2 claim.

## Direct tier-Foster criterion

Anderson and Kim, *Some network conditions for positive recurrence of
stochastically modeled reaction networks* (SIAM J. Appl. Math. 78 (2018),
2692--2713; arXiv:1710.11263), prove a direct CTMC Foster theorem when every
tier sequence has a descending reaction whose source is in the global top
S-tier.

That hypothesis fails on the exact seam

\[
 L_0=\{2B,A+B\},\qquad L_1=\{C,A+C,B+C\}
\]

along \((A,B,C)=(n,n,1)\). The two sources in \(L_0\) have order \(n^2\)
and form the global top S-tier, but every \(L_0\) reaction stays in the same
D-tier. The descending sources in \(L_1\) have only order \(n\). Hence the
global top S-tier contains no descending source. The scoped corrected
factorial potential in `certified_exact_shielded_seam.md` is genuinely
additional: it balances the fast neutral linkage so that the lower-rate
negative linkage becomes visible to the generator.

Primary source:
<https://arxiv.org/abs/1710.11263>

## Single-linkage theorem

Anderson, Cappelletti, and Kim, *Stochastically modeled weakly reversible
reaction networks with a single linkage class* (J. Appl. Probab. 57 (2020),
792--810; arXiv:1904.08967), assume one linkage class and, in their binary
application, a pure multiple complex for every species. Those hypotheses do
not cover the two-linkage T3-2 interfaces.

Primary source:
<https://arxiv.org/abs/1904.08967>

## One-dimensional classification

Wiuf and Xu, *Classification and threshold dynamics of stochastic reaction
networks* (arXiv:2012.07954), prove
positive recurrence for weakly reversible mass-action networks with
one-dimensional stoichiometric subspace. This rigorously covers some reduced
shielded phases, but not the remaining two-dimensional coupled seams.

Primary source:
<https://arxiv.org/abs/2012.07954>

## Finite-phase Lamperti theory

Lo and Wade, *Non-homogeneous random walks on a half strip with generalized
Lamperti drifts* (Markov Processes Relat. Fields 23 (2017), 125--146;
arXiv:1512.04242), classify several recurrent, null, and transient regimes
for a level coordinate coupled to a finite internal phase. Their generalized
Lamperti criterion contains phase--level correlation terms; averaging only
the first level drift is not sufficient in the critical case.

This is directly relevant to the reflected-level repair in
`reflected_level_process_repair.md`: after a legitimate finite-phase
reduction, a vanishing leading debt drift still requires a second-moment and
phase-corrector audit. The theorem is not directly applicable to every T3-2
episode because promotion boundaries, state-dependent physical holding
times, and occasional macroscopic increments fall outside its basic
half-strip hypotheses. It supplies a warning and a possible terminal tool,
not a black-box proof of the one-active gate.

Primary source:
<https://arxiv.org/abs/1512.04242>

## Consequence for this project

The existing primary theorems validate several branches and motivate the
direct physical-time generator route, but none supplies the missing universal
shielded/available or signed-service seam. No claim of literature-wide
novelty has been assessed while the global theorem remains open.
