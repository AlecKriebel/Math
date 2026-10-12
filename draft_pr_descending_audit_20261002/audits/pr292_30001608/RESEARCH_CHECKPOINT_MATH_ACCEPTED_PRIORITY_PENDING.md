# PR292: mathematical review complete; priority review pending

Research checkpoint, 5 October 2026. This is an interim audit record, not a
preprint or a declaration of novelty. PR292 remains open and draft. The
descending campaign processes only problems whose original submitted
`QUEUE.md` status is exactly `claimed_solved`; PR8 is excluded.

## Exact verified conclusion

For every fixed real arrival rate \(\lambda>0\), the continuous-time Markov
chain on \(\mathbb Z_{\ge0}^4\), with state \((a,b,x,y)\) and
\(D=x+y+1\), is nonexplosive, irreducible, and positive recurrent. Its six
rates are arrivals into each of \(a,b\) at \(\lambda/2\), transfers
\(a\to x\) at \(a(x+1)/D\) and \(b\to y\) at \(b(y+1)/D\), and
departures from \(x,y\) at \(x(y+1)/D\) and \(y(x+1)/D\). A decrement
from a zero coordinate has zero rate. Consequently it has a unique invariant
probability distribution.

The model has one permanent seed, invisible empty peers committed to their
first chunk, and immediate departure on completion. Including empty peers in
the sampling denominator, replacing the request-dependent seed contribution
by a bounded seed upload clock, or changing the selection protocol changes
the chain. No conclusion is asserted for such variants, zero load, more than
two chunks, or bounds uniform over arrival rates.

The accepted proof constructs a coercive Lyapunov function from a weighted
population count, a rounded imbalance term, and two bounded finite
birth-and-death Poisson corrections activated by queue-to-visible-population
cutoffs. Exact signed product increments control the interfaces. A finite
three-region decomposition proves generator drift at most \(-1\) outside a
finite set for every fixed positive real load. A stopped Dynkin argument
and a finite-set regeneration argument establish finite expected return
time; stationary moments or a fast-mixing approximation are not assumed.
The complete derivation is in the original `TURN_4.md` and the independently
written `ROOT_MATHEMATICAL_ADJUDICATION.md`.

## Evidence and limits

Original head: `1198534928f4c2bf8bf758c9ceb16edaa3a496e8`; original status:
`claimed_solved`, author budget `4/5`. The original snapshot is immutable.
Both independent full mathematical review families found no remaining gap
in the all-state proof. Original and independently written exact arithmetic
controls were reproduced. Finite controls supplement the analytic argument;
they do not establish recurrence over an infinite state space. A separate
audit of all forty original progress files is completing its consistency
and reproduction checks.

The source is Norros (joint with Reittu), “On the stability of population
processes,” OWR48/2010, printed2782–2783, DOI10.4171/owr/2010/48, together
with Ilkka Norros, Hannu Reittu and **Timo Eirola**, “On the stability of
two-chunk file-sharing systems,” Queueing Systems67(2011),183–206,
DOI10.1007/s11134-011-9209-2. The inspected January2011 author proof, publicly
deposited as HAL00781341, has the exact generator in Figure2 and the stability
conjecture in §3.2. The publisher-final body has not yet been inspected.
The October2009 arXiv version0910.5577v1 has the opposite conjecture; it is
not substituted for the later stability statement.

The known large-system ODE instability is credited to
Norros–Reittu–Eirola. Their scaling changes the arrival rate to
\(N\lambda\) and divides states by \(N\) at fixed time. It is distinct
from fixed-arrival, time-accelerated fluid scaling. The present audit does
not claim the first stable stochastic network with an unstable deterministic
model: earlier general examples and their scaling distinctions are under
review. The priority question concerns the exact DFC conjecture and its load
quantifier, as well as any previously established narrower resolution.

Two independent priority investigations are reviewing chronological source
versions and citation descendants, and equivalent models/general proof
mechanisms. Earlier stable peer-to-peer protocols require explicit generator
comparison. No current-openness or novelty clearance has been granted.
No preprint, DOI, tracker row, merge, closure, or completion-count increment
has been authorized by this mathematical acceptance.

One frozen acceptance receipt mistakenly wrote “Esros” in a source-edition
qualification. `ROOT_AUTHOR_METADATA_ERRATUM01.json` records the correction
to **Eirola** while preserving the historical receipt. All current credit
uses the correct name; the error does not alter the mathematical conclusion.

AI tools were used extensively for derivation, reproduction and adversarial
review. These are independent AI-assisted checks, not journal refereeing or
formal human peer review. The research remains unrefereed.

At this checkpoint: mathematical review100%; source/model correspondence100%
within the stated edition limits; priority clearance0%; publication
workflow30%. Campaign counters remain29 completed dispositions,9 preprints,
9 native merges, and0 pending tracker rows. PR293 remains an uncompleted,
open draft with mathematics accepted and later-priority evidence unresolved.
