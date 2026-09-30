# Source, scope, and prior-work audit

Checked 30 September 2026. This is a targeted audit, not an exhaustive priority
search. Source PDFs remain outside the research package; hashes identify the
exact files consulted.

## Original task

The complete **Bruß contribution, pp.203–205** in
[OWR 4/2005](https://ems.press/journals/owr/articles/785), DOI
10.4171/OWR/2005/04, was read. The report PDF was obtained from the publisher;
printed pp.204–205 were also visually checked. The surrounding unrelated workshop
contributions are not premises of the argument. Page 204 explicitly gives the
asymptotic interpretation, independent sender information, the fixed assignment
of sender qubits to the two receivers, and LOCC between receivers. Page 205 asks
the W-state class-membership question. It does not require a single-copy
zero-error alphabet or an exact optimal capacity.

The full pinned record, ID 30000177 / OWR-785-003, is in source_record.json.
It comes from dataset revision 37e53eabe540fb458758e198be61634bd02ee008.
No imported research report was found under either the exact problem code or
numeric ID in the pinned research_results.json. The dated upstream literature
assessment is context rather than a certificate of current openness.

## Primary dependencies and nearby literature

1. **Bruß et al., Dense coding with multipartite quantum states**, full
   [quant-ph/0507146v1](https://arxiv.org/abs/quant-ph/0507146v1), July 2005.
   Sections 2–4 distinguish Holevo information from asymptotically achievable
   coding. Sections 6–7 define the two-receiver model, the no-communication
   comparison and the LOCC-DC shell, and give the LOCC upper bound.
   The stored PDF has a later typesetting timestamp in its page header; its
   arXiv version banner and record identify the 2005 preprint. The theorem
   application here does not assume its LOCC upper bound is attainable.
2. **Winter, The capacity of the quantum multiple-access channel**, full
   [quant-ph/9807019v3](https://arxiv.org/abs/quant-ph/9807019v3), 1 February 2001;
   IEEE Transactions on Information Theory 47 (2001), 3059–3065,
   [DOI 10.1109/18.959287](https://doi.org/10.1109/18.959287).
   Section II defines independent messages, separate codebooks, finite cq
   outputs and average error. Theorem 9, pp.4–5, proves the direct coding
   theorem for the product-input region; its proof was checked through the
   successive gentle-decoding construction. This is the established
   achievability input, not a new theorem proved by this package.
3. **Pradhan–Agrawal–Pati**, [arXiv:0705.1917v1](https://arxiv.org/abs/0705.1917v1),
   Section 4.2 and especially 4.2.3, printed p.36. The full PDF was retrieved;
   the relevant multi-receiver discussion was read. Its Bell measurements for
   a four-state W alphabet already give a two-bit single-copy protocol. This
   is direct prior work for the receiver measurement pattern. The current
   argument keeps a quantum output at the second receiver and applies block
   coding; it does not claim novelty for Bell processing. Statements about
   selected orthogonal alphabets in that paper are not used as upper bounds
   on all asymptotic protocols.
4. **Das–Prabhu–Sen(De)–Sen**, [arXiv:1412.6247v1](https://arxiv.org/abs/1412.6247v1),
   December 2014; Phys. Rev. A 92, 052330 (2015). The full PDF was retrieved;
   the model, Section II bounds and the generalized-GHZ comparison were
   checked. The paper explicitly notes that attainability of the general
   LOCC Holevo-like bound has not been established. It supplies no verified
   obstruction to the smaller achievable W-state rate used here.
5. **Muhuri–Gupta–Ghosh–Sen(De)**,
   [arXiv:2211.13057v2](https://arxiv.org/abs/2211.13057v2), March 2024;
   Phys. Rev. A 109, 032616. The full PDF was retrieved; the two-sender,
   two-receiver formulation, equation (7), Section IV two-receiver discussion
   and Figure 3 were checked. These are explicitly upper-bound calculations
   in the noisy setting. A plotted upper bound above two is not an
   achievability certificate; it is not used as one here.
6. **Hayashi–Wang**, PRX Quantum 3, 030346 (2022):
   [author's publication page](https://kunwang.info/publication/2022-hayashi-dense/).
   Abstract and protocol summary checked. Its sender–helper setting with
   symmetry restrictions differs from the two independently encoding senders
   in the original question. No theorem from it is needed or transplanted.
7. **Roy et al.**, [arXiv:1707.02449](https://arxiv.org/abs/1707.02449), and
   **Yeo–Chua**, [PRL 96, 060502](https://doi.org/10.1103/PhysRevLett.96.060502):
   primary abstracts/scope checked. Their single-receiver deterministic or
   different-resource tasks do not replace the present target.

The original 2004 publication,
[Bruß et al., PRL 93, 210501](https://arxiv.org/abs/quant-ph/0407037v3), is also
identified in the OWR references and explicitly raises the W question. The
2005 full exposition above is the source used for its detailed definitions.

Targeted searches included “four-qubit W LOCC dense coding capacity”,
“W state two receivers dense coding”, “W state dense coding multiple access”,
and recent 2025–2026 variants. No verified source establishing the same
independent-message asymptotic construction was identified. This does **not**
establish novelty or claim that the problem remained open immediately before
this work.

## Prior-attempt and duplicate gate

The live repository queue showed rank 96, queued, 0/5. Exact-ID and “dense
coding” all-state PR searches returned no earlier attempt. The proposed branch
was absent, the attempt path had no all-branch history, and the related-target
index had no matching entry. Repository-wide text search found the desk-review
metadata and an unrelated four-qubit Yang–Baxter project, not an attempted
resolution of this communication problem. The campaign skip rule therefore did
not apply. No queue generator or shared status file was edited.
