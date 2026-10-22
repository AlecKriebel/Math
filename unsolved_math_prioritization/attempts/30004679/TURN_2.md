# Turn 2: absorb effectively indexed adaptive calls, but not arbitrary feedback

Substantive author turn **2/5**. Let A=wFindHS_{Pi^0_1}. This turn tests whether the countable-fusion theorem can remove the residual adaptive compact-choice call. It proves an absorption theorem for an explicitly restricted form of adaptive access, and gives a concrete reason that arbitrary continuous instance formation need not have this form. Neither original reduction is resolved.

## 1. An indexed-call model with all promises exposed

Let p name an input of a multivalued problem F. Suppose, uniformly from p, we can enumerate a sequence (P_i(p))_{i∈N} of open-set names such that

                     every P_i(p) belongs to dom(A).               (4)

Suppose a computable oracle protocol produces an F-solution using p and answers to requests of the form “return some member of A(P_i(p))”. The requested index i may be computed adaptively from p and all previous answers. Each request for a natural-number index must finish after finite computation on those answers. The protocol may make unboundedly many requests while producing its output stream, provided that for **every** sequence of allowed answers it is a total realizer on the F-domain: each output symbol is eventually produced. No computable uniform bound on the number of calls is assumed.

The promise (4) covers the entire supplied menu, including indices not reached on a particular run. One cannot add invalid speculative instances merely because a intended execution would avoid them.

## Theorem

Every F admitting such an indexed-call protocol satisfies F<=_W A. Conversely A itself admits such a protocol, so the indexed-call model has exactly the ordinary Weihrauch degree of A.

## Proof

Apply the computable preprocessing of turn 1 to the whole sequence (P_i(p)), obtaining

                        Q_p=⋃_i s_i^{-1}(P_i(p)).                  (5)

By (4) and the fusion proof, Q_p is a valid A-instance. For any h∈A(Q_p), the tail h_i=s_i(h) lies in A(P_i(p)) for every i, uniformly and without further oracle calls.

Simulate the original protocol with input p. Whenever it requests index i, answer with h_i. This is a legal sequence of answers; repeated requests may reuse the same answer, which the correctness-for-all-answers hypothesis permits. The totality and output correctness of the protocol therefore guarantee an F-solution. Both the forward map p↦Q_p and the backward simulation using (p,h) are computable, proving an ordinary Weihrauch reduction. The backward map is allowed to use p, so no unjustified strong reduction is asserted. The converse uses the menu P_i=P and one request. □

This applies, for example, to finite or countable decision networks whose node instances are uniformly named in advance and all valid. Their later branching may depend on finite information extracted from earlier infinite answers. They add no power to A even if their paths are unbounded or infinite. It does **not** say that every computable map from an earlier real answer to a later open-set name factors through a natural-number index in a fixed computable menu.

## 2. Continuous instance formation can have uncountable range

For x∈2^N define the open, indeed relatively clopen, subset of [N]^N

 P_x={f: there exists n with x(n)=1, f(0)=2n and f(1)=2n+1}.          (6)

The map x↦P_x is computable in the standard representation: enumerate the cylinder with first two terms (2n,2n+1) whenever the bit x(n) is 1. Its complement is also uniformly open, using the first two terms and, when necessary, that same bit.

Every P_x is a valid A-instance. For any infinite h, take a subsequence beginning with h(0),h(2). Their difference is at least 2, so that subsequence is outside P_x. Thus h cannot land homogeneously in P_x. The computable all-even sequence avoids every P_x, so this particular family is uniformly easy.

Nevertheless x↦P_x is injective: if x(n) differs from y(n), a sequence beginning with (2n,2n+1) belongs to exactly one of P_x,P_y. Hence its range is uncountable. No single countable menu of exact open sets can contain every value, let alone have a computable index selector. Finite use for each output symbol of an open-set **name** does not imply finite use to choose the entire named instance.

This example is only a refutation of a proposed countable-range shortcut. It is not a counterexample to either original Weihrauch reduction, and it does not prove that this easy family needs adaptive calls: its common computable solution shows the opposite.

## 3. What still fails in the proposed path reduction

The credited factorization C_{N^N} equivalent_W C_{2^N} star A produces a compact-choice input after receiving an infinite A-answer. The bounded subtree can vary with that entire answer. The absorption theorem would help only if one supplied, uniformly from the original input, an all-valid indexed menu together with a computable selector or some other justified replacement protocol. The factorization itself does not provide that additional structure.

Thus independent calls and effectively indexed feedback can be flattened, but arbitrary infinite-answer-dependent instance names remain outside the theorem. Calling a computable real-to-real transformation “continuous” does not close that gap. The original remains unresolved after two substantive author turns. The general simulation lemma is a consequence of parallelization, not a claimed new theorem in the Weihrauch literature.
