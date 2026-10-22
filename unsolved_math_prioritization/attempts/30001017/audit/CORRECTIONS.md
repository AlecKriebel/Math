# Additive audit clarifications

These clarifications accompany, and do not alter, the frozen author packet.

## 1. Proof of the numerical birational-support lemma

In PROOF.md Lemma 6.1, the abstract statement does not assume that ell has a globally generated positive multiple. The hyperplane proof therefore uses an unstated hypothesis if applied to arbitrary bases. The numerical conclusion nonetheless follows directly from proper pushforward, without positivity.

Write q=p composed with f and let

    Delta_N = ((D')^N - (f^*D)^N) cap [X'].

This is a cycle of dimension n=G-N represented on Z, because every term of the binomial expansion contains E. For each n-dimensional component V of a representative, the image q(V) has dimension at most s<n. By the definition of proper pushforward of cycles, q_*[V]=0. Therefore q_*Delta_N=0. The projection formula then gives

    degree ((q^*ell)^n cap Delta_N)
      = degree (ell^n cap q_*Delta_N) = 0.

The remaining pullback term has the required degree on X because f_*[X']=[X]. This proves the stated equality of degrees for rational Cartier ell, D, and D'. Degrees can be taken on the proper image of X if necessary. The analogous argument applies in the stipulated rational stack intersection theory.

For the actual Satake/Hodge application, a positive multiple of ell is globally generated, so the author's hyperplane argument also applies. The correction removes the unnecessary mismatch between the general lemma's wording and its proof; it does not strengthen the genus-five result.

## 2. Additional OWR rank-one normalization warning

Add to SOURCE_ISSUES.md's OWR cautions: the displayed rank-one recurrence on printed p.2188 omits a factor 1/2 when the Hodge degrees and boundary are interpreted with the stack conventions used in the packet. The degree-two Kummer cover requires

    a_g^(g) = (1/2)(-2)^(g-1)(g-1)! H_(g-1).

For genus three this is 1/720, in agreement with the report's own p.2187 table; the displayed recurrence without 1/2 would give 1/360. The author packet already uses the correct formula, so its computations are unchanged. This observation concerns the inspected OWR report and is not a claim about another version of EGH.
