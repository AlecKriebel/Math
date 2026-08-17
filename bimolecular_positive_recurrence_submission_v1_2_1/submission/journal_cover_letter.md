# Draft journal cover letter — not submitted

**Submission-day note (not part of the letter):** this draft predates the
planned bioRxiv posting. Before journal submission, replace the final
prior-online-status paragraph with the actual bioRxiv citation, DOI, and date,
then remove this note.

16 August 2026

Editors<br>
*Journal of Applied Probability* and *Advances in Applied Probability*

Dear Editors,

Please consider the manuscript **“Positive Recurrence for Single-Linkage
Bimolecular Weakly Reversible Stochastic Reaction Networks”** for publication
in the Applied Probability journals.

Weak reversibility gives an elementary but useful state-space closure: every
enabled population transition has a return path, so the set reachable from any
initial population is already a closed communicating class. On each such
class, the paper proves that every finite weakly reversible stochastic
mass-action network with one linkage class and molecularity at most two is
positive recurrent for every positive rate vector unless the class is an
absorbing singleton, in which case its stationary law is the point mass. Each
reachability class therefore has a unique stationary probability
distribution. The return-cycle construction also recovers nonexplosion for
this subclass; the manuscript identifies nonexplosion as previously known for
the broader bimolecular weakly reversible class.

The theorem removes the pure unary/pure-double complex condition in the
binary one-linkage result of Anderson, Cappelletti, and Kim (2020), and thus
contains their positive-recurrence conclusion as a special case. In their
published Section 6, a tier criterion, a finite reaction word, and a
sampled-chain Foster argument are combined to prove recurrence. In the
boundary case of Section 6.1, the extra assumption forces $S_v$ after D-tier
maximality excludes $2S_v$; the source propensity of $S_v$ supplies the
required comparison. The present construction avoids that boundary step.

The new proof retains the target of the most recently fired labelled reaction
channel and subtracts it from the population before applying a residual
log-factorial potential. This yields an exact target/source falling-factorial
increment. A scalar recursion propagates terminal negative drift along finite
target-following paths, while normalized-log compactification and a
bimolecular top-complex alternative provide the terminal source or a
stoichiometric obstruction to divergence. Random-time Foster, finite
trace-chain, and regenerative occupation arguments complete the recurrence
proof.

The manuscript distinguishes its target-shifted discrete potential from the
classical pseudo-Helmholtz/Horn--Jackson family. Its concise systems-biology
motivation is that stationary molecule-count laws support long-run state
frequencies and bounded-observable statistics in low-copy-number biochemical
CTMC models satisfying the stated structure. The paper gives no explicit
stationary formula, moment or tail guarantee, mixing rate, or claim that all
biological networks meet the hypotheses. It makes no claim for multiple
linkage classes or molecularity above two.

A publicly available deterministic verification package, linked from the
manuscript, supports the paper.
It checks exact identities, state-cycle lifting, finite reachability symmetry,
boundary cases, the rate-sensitive example, and finite calibration chains,
and it requires byte-identical canonical outputs. These checks are
falsification aids; no finite computation proves the universal theorem,
enumerates the analytic Foster set, or certifies a useful bound on it. The
package includes complete hashes, deterministic PDF and archive builders, and
a clean-checkout release replay.

Generative-AI systems were used substantively for mathematical exploration,
counterexample search, proof criticism, software work, literature support,
drafting, and editorial review. The manuscript contains a concise declaration,
and the complete statement linked from the manuscript identifies the known tools, models,
dates, access routes, and uses through 16 August 2026 in accordance with the
current Cambridge instructions. Rejected approaches are not part of the final
proof. I directed the research, determined the released claims, and assume
responsibility for the manuscript and verification materials. No AI system is
an author.

The work has not been published as a peer-reviewed article and is not under
consideration by another journal or publisher. Tagged repository versions
0.3, 1.0, 1.1, 1.2, and 1.2.1 are publicly accessible as unrefereed research
releases. As of this draft, no version has been deposited on a formal preprint
server. I received no specific funding for this work and declare no competing
interests. No empirical dataset is associated with the paper.

Thank you for your consideration.

Sincerely,

Alec Kriebel<br>
Independent researcher<br>
<me@aleckriebel.com><br>
ORCID: <https://orcid.org/0009-0001-9320-500X>
