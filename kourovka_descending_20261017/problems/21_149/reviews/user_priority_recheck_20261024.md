# Fresh audit of the user-linked Lean priority objection

UTC checkpoint: 2026-10-24T16:54:52.637161+00:00. Completion of this narrow source-scope audit: 100%. This is not a new mathematical discovery or a certification of the whole published theorem.

## Conclusion

The linked Lean file is a prior solution of the original formulation of Kourovka 21.149. It must be credited as such. It does not state or establish the corrected ambient-group formulation; its particular witness is explicitly conjugation-induced in a larger Dlab group.

## Independently checked evidence

1. Current raw source retrieved 24 October 2026 from https://raw.githubusercontent.com/pitmonticone/Kourovka/main/Kourovka/Problem_21_149.lean has SHA-256 `4a69f3e9d739fc1119d5fbf561fc4ca63c064bcdeece6766ff987eabcd8c5655`, matching the existing local source. Its physical lines 768–775 label the theorem as the original formulation. Its quantifiers are existential over a slope subgroup H, an order on `DlabGroup H`, and an automorphism of that same group outside `MulAut.innerSubgroup (DlabGroup H)`. The inner subgroup is defined at physical lines 65–66 as the range of conjugation by elements of that same group. There is no quantification over larger Dlab groups or embeddings.
2. The source physical lines 96–98 give the conjugator h0(x)=2x for x<=1/3 and h0(x)=(x+1)/2 otherwise. This increasing interval homeomorphism fixes 0 and 1 and has allowable slopes 2 and 1/2. It is in the full interval Dlab group, but is not identity near either endpoint, so is outside the compact-support source group. Its automorphism is therefore already conjugation-induced after the natural inclusion in that larger full group. Even if an ambient compact-support family were required, extending h0 by identity outside [0,1] inside a strictly larger interval produces a compactly supported locally right 2^Z-affine conjugator, with the source embedded by the same identity extension.
3. Appendix A of https://arxiv.org/html/2607.17477v2, browser-extracted lines 497–499, explicitly reports that the original non-inner question was solved affirmatively, accepted by a problem author, and then clarified to require nonconjugation in a possibly larger Dlab group. Its statement that the clarified problem was open is historical as of that July version, not a certificate of its present status.
4. The authoritative October 20 Notebook text, local `sources/21tkt_oct20_2026.txt` lines 9664–9666, asks about conjugation by elements of a possibly bigger Dlab group. It remains unstarred there; lack of a star alone is not proof of current openness.
5. The existing preprint `preprint/main.tex` explicitly credits the linked Lean and original solution, reproduces h0, and explains its larger-group implementation. Its own explicit theorem concerns every embedding into each of two defined ambient affine-germ groups, rather than only internal conjugation. This is a real difference in mathematical quantifiers.

## Limits and originality risks

I did not rebuild Lean. This audit reads the exact theorem and gives a direct ambient realization of its witness; it does not independently validate all formal dependencies or the full new preprint proof. The scope distinction defeats the claim that this particular Lean theorem is already a solution of the corrected all-ambient problem, but it does not by itself establish first priority for our stronger result. In particular the prior Gong–Yang–Zeng result acknowledged in the manuscript already treats an ambient nonconjugation setting; any novelty claim must specify the extension beyond that theorem and survive its separate priority audit. Do not describe the original problem as previously unsolved or the full submission as Lean verified.

No published artifact was modified and no publication action was taken in this audit. Existing project receipts show publication already occurred on October 17; user-facing explanations should disclose that timing accurately.
