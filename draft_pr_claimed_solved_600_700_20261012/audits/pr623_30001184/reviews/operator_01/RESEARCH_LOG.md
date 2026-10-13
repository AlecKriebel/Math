# Independent operator and analytic review

## 2026-10-13 04:52:32 UTC - Start; completion estimate 15%

Bound to frozen PR head `947442c091ae617804c6a0d07b98ff2c50368798` and packet
`PROOF.md` SHA256 `f2a1b3b4233c2850d8dd79ba17b464d74343aa66e7d22d12104d17fc5470e8a3`.
Read the actual proof, without importing previous audits or checker results as
mathematical evidence. The source PDF text identifies the target as the first
problem in Michael Skeide's section, pp. 542-543, and explicitly separates
kernel descent from adjointable-operator extension. The advertised claim is a
counterexample to forward generation alone, not a theorem covering stronger
minimality or conditional extension after kernel invariance.

Workflow: independently derive the ambient action by conjugating translation;
construct the universal GNS module directly; check the adjointable algebra by
its central column projections; construct exact radical arithmetic for the
witness; verify original source pages visually and bind the downloaded PDF by
hash. Raw source text/PDF and intermediate images stay in ignored directories.

No remote, queue, PR, publication, or other-shard mutation is authorized in this
review. No outside individual is contacted. Review artifacts remain within
this dedicated review directory.

## 2026-10-13 04:54:02 UTC - Primary-source check; completion estimate 45%

Downloaded the actual primary EMS PDF and verified SHA256
`b3c4037dd84c3dccae4fd3b941a11fb3b9957865671ee940879be489e54c7aeb`.
Rendered and visually inspected all four relevant printed pages, including
the source's diagrams, rather than relying on search snippets or copied
packet source claims. General dilation is explicitly C* or von Neumann;
the expectation arrow typo on p. 542 is resolved by p. 498 and both diagrams.
Generation is an explicitly proposed sufficiency condition. Strong/corner
or faithful-expectation hypotheses are not part of this general category.

The all-real ambient action is directly conjugate to translation, providing
an independent proof of the cocycle action and point-norm continuity. The
algebra is the exact smallest forward-invariant subalgebra containing the
observed diagonals, and has a countable rational-time generating set.

## 2026-10-13 04:55:42 UTC - GNS and exact arithmetic; completion estimate 75%

Constructed the universal algebraic GNS quotient map onto `M2`; its inner
product isometry proves this is the actual module, with cyclicity obtained
from the off-diagonal matrix units in the evaluation image. Central right
column projections identify `B^a(E)` as `M2 direct-sum M2`. The full
representation kernel is exactly evaluation at zero. Fullness does not
imply representation faithfulness.

Fresh radical-field arithmetic passes 22 exact identities without importing
the packet's verifier. The positive square of the witness also starts in
the kernel and leaves it. The original publication verifier was rerun and
its byte-identical replay passed; this is integrity evidence only.

Independent strengthening: for every `s>0`, with `r=exp(-s)`, the analogous
witness has shifted coefficient
`d_s=(1-r^2)(sqrt(1+r^2)-r)/2>0`. Thus kernel invariance fails at every
positive time. The formula also checks the limits at zero and infinity.

## 2026-10-13 04:59:20 UTC - Mathematical review complete; completion estimate 100%

Saved the independent derivations in `FINDINGS.md`, scoped machine-readable
`VERDICT.json`, fresh code/results, the original integrity replay, and source
URL/hash metadata. The audit goal is complete: the scoped mathematical
counterexample passes, with no mathematical repair identified. The verified
claim refutes generation alone at the first GNS descent stage. It does not
decide conditional extension after kernel invariance, find stronger useful
minimality conditions, address the source's second problem, or determine
literature priority. Those are exact remaining gaps for any broader claim.

All work stayed within this review directory; raw third-party fulltexts and
rendered intermediates are ignored. No outside contact, remote mutation,
queue mutation, PR change, or publication was made by this reviewer.

## 2026-10-13 05:00:48 UTC - Adversarial wording repair; completion estimate 100%

The root reviewer challenged a supporting sentence that suggested the
direct witness might fail global positivity. Independently differentiated
`g` on `(0,infinity)`: `g'(x)=1/(2 sqrt(exp(2x)-1))` is positive and
decreasing, so forward increments there are bounded above by `g(s)`.
Negative `x` and endpoints obey the same bound by the definition of `g`.
Hence `a_s(x)=(cos^2(g(x+s)-g(x))-cos^2(g(s)))q>=0` everywhere.
Corrected the report to prove the stronger, globally positive witness
statement. The square witness and the frozen candidate's self-adjoint
witness argument were already valid; this repair removes an unnecessarily
weak and potentially misleading supporting-report sentence. Regenerated
the review manifest after the correction.
