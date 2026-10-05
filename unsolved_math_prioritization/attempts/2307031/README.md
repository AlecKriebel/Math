# Function Theory 7.31: audited partial results

Target 2307031 / AMR-022-7031, rank 689. Broad-target disposition:
**unsolved, five of five approaches used**. No sixth proof-search approach
is added by this publication. The complete classification remains unresolved.

## Results and limits

For a_1>0 and 0<=a_n<=n, define b_n=sum_{k<=n}a_k and
c_n=sum_{k<=n}b_k. At zero a_n use c_n/a_n=+infinity and f(+infinity)=0.
The [frozen proofs](author/PROOFS.md) establish:

- A single infinite admissible sequence and a single positive entire,
  strictly completely monotone function f for which sum f(n^2) converges
  and sum f(c_n/a_n) diverges. This disproves that implication under the
  listed strong smoothness assumptions; it is not a full classification.
- A global count N_a(T)=O_{a_1}(sqrt(T) log T), uniform over sequences with
  fixed a_1, and matching-order examples along square T. The extremal
  sequence may depend on T; no pointwise bound on index locations is claimed.
- A discrete weighted sufficient criterion and its tail-integral form,
  covering f(t)=1/[sqrt(t)(log(e+t))^p] for p>2. Necessity, the range
  1<p<=2, and the condition sqrt(t)f(t) nonincreasing remain unsettled here.

Read the [controlling integral clarification](INTEGRAL_CLARIFICATION.md)
with Corollary 3: start the integral at A>=2 after monotonicity begins;
starting at 2 additionally requires measurability on [2,A].

The [full independent audit](independent_audit/AUDIT.md) passes the principal
results with that minor clarification. It is an independent AI audit, not
external human peer review or a machine-formal proof. The historical
"audit pending" and "no remote writes" phrases inside frozen files describe
their earlier state; this wrapper records the completed audit and correction.
No novelty, priority, current-openness, or full-resolution claim is made.

## Preserved evidence and replay

The nine authored files, their original ZIP, and all five independent audit
files are byte-preserved. BINDING.json binds both freezes and the controlling
clarification. PUBLICATION_MANIFEST.json inventories the exact package.
The [five approaches](author/APPROACH_LOG.md) and [target scope](author/TARGET_SCOPE.md)
record the mathematical history and remaining gaps. Public source metadata
is in the author and audit directories; no source PDF, copied scholarly text,
dataset contents, or private coordination material is included.

From any working directory, with Python 3.10+ and its standard library:

    python3 /path/to/2307031/verify_publication.py --replay --selftest

The strict wrapper rejects extra or missing files, links, empty directories,
duplicate or unsafe manifest paths, duplicate JSON keys, changed freezes,
and changed controlling correction or disposition. Replay uses a temporary
copy and forces unoptimized child Python processes even if the wrapper is
invoked with -O. It compares both verifiers' deterministic results exactly.
Finite checks corroborate but do not replace the written infinite proofs.

Primary source: W. K. Hayman and E. F. Lingham, *Research Problems in Function
Theory (New Edition)*, arXiv:1809.07200v2, Problem 7.31, printed p. 169
(PDF p. 170): https://arxiv.org/pdf/1809.07200v2 .
