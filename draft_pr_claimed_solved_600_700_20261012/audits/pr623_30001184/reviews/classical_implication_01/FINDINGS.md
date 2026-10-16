# Independent implication audit: PR623

**Conclusion:** The proposed BFH implication is complete after one necessary
continuity repair. Its explicit bit-flip specialization and forward-generated
restriction yield exactly the general unital C*-dilation category in the target,
including B=C^2 and the packet's exponential two-state Markov semigroup. The
GNS representation kernel fails invariance. This is an unstated short corollary
of the prior clock construction, with no new central dilation mechanism.

The theorem's statement alone is not a ready-made kernel-failure theorem. BFH
Theorem 4.4 states existence of an autonomous unitary dilation with a dynamical
decoupling property. The corollary uses its constructive proof, notably the
finite bath, point evaluation and equation (11). Attribution must distinguish
that stated theorem from this deduction. No evidence here says the prior authors
explicitly answered the OWR question.

## Assumptions attacked and resolved

| Issue | Independent check | Result |
|---|---|---|
| Strong versus point-norm continuity | Strong continuity on L2 does not imply norm continuity of conjugation on C_b. The explicit unitary W has both endpoint limits; uniform continuity of W proves orbit continuity on generators and then on A. | Resolved for the explicit specialization. |
| Generated-algebra restriction | A=C*(alpha_r(i(B)):r>=0) is forward-invariant, unital and separable; theta is the restriction of an ambient automorphism group. | Matches the exact generation hypothesis. |
| Expectation rather than a scalar state | p is finite bath compression after evaluation, optionally followed by system diagonal extraction; p i=id and the B-bimodule identity hold. | i p is a conditional expectation. |
| Genuine all-time Markov compression | Phi_t=(id+Ad_X)/2+exp(-t)(id-Ad_X)/2. On C^2 it is P_t=J+exp(-t)K. | Exactly the packet's semigroup for every t>=0. |
| Finite GNS image | The GNS module is represented within M_(4,2) with its explicit B-valued inner product. | The fixed representation image is a finite-dimensional C*-algebra. |
| Representation kernel versus vector-null space | The proof never equates f(0)S=0 with pi(f)=0. The exact witness has f(0)=0 as a full M4 matrix; its shifted expectation is nonzero. | Correct representation-kernel failure. |
| Expectation factorization | pbar(c)=<S,cS> factors p through pi and inherits j(B)-bimodularity. | No hidden faithfulness assumption. |
| Finite semigroup differentiability | A short integral argument gives a bounded generator from finite-dimensional continuity. Differentiating multiplicativity gives a derivation. | Complete, without assuming differentiability in advance. |
| Derivation obstruction | Both diagonal corners of delta(j(q)) vanish; expectation preserves these corners. T'_0(q)=diag(-1/2,+1/2). | Contradiction. |
| Explicit time of failure | s=log(2), a=q theta_s(q) q-(3/4)q. Then a(0)=0 and p theta_s(a)=3(sqrt5-1)/16 * diag(3/4,1/4). | Exact nonzero witness. |
| Every positive time, same mechanism | With u=exp(-s), a_s=q theta_s(q) q-((1+u)/2)q has full evaluation zero and shifted expectation d_s diag((1+u)/2,(1-u)/2), d_s=(1-u^2)(sqrt(1+u^2)-u)/2>0. | For both M2 and C^2, every s>0 fails kernel invariance. |
| Global positivity not silently added | In the odd BFH extension, at s=log(2), a_s(-s/2)=-(1/4)q. | The witness is selfadjoint and has positive shifted expectation, but is not globally positive. Clipped-extension positive witnesses are a distinct additional property. |

## Artifacts and controls

- `DERIVATION.md` contains the full standalone derivation and an independent
  direct witness, with exact source page/equation locators.
- `exact_compression_check.py` uses dependency-free exact arithmetic in
  Q(sqrt2,sqrt3,sqrt5); all 14 controls passed. The controls verify unitary
  matrices, full matrix vanishing, shifted compression, the radical coefficient,
  the semigroup projection identities and the diagonal generator.
- `SOURCE_LEDGER.json` identifies the actual downloaded source as v2, despite
  its inherited filename `bfh_v3.pdf`, and records source and input hashes.

## Exact remaining gap and limits

No mathematical gap remains in this specific implication/category check. The
counterexample does not resolve extension after kernel invariance has been
separately imposed. It also does not establish a normal von Neumann or weak
corner-dilation counterexample. Arbitrary analytic channels and arbitrary BFH
Kraus completions need not supply the global uniform continuity used here; only
the exhibited completion is required.

This review is a falsification of independence from the cited clock mechanism,
not a comprehensive history or first-priority adjudication. It did not read
the priority reviewer's conclusions before reaching its independent conclusion,
alter native inputs, communicate externally, mutate queues or PRs, or publish.
Completion of the assigned implication audit: 100%.
