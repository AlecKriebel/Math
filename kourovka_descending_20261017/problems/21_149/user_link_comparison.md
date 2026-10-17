# User-linked formalization: scope comparison

Checked current raw source on 2026-10-17T20:30:06.032311+00:00.

User source: https://github.com/pitmonticone/Kourovka/blob/main/Kourovka/Problem_21_149.lean

The declarations at lines 768–775 explicitly package the original non-inner formulation. The output quantifies over H and an order on the SOURCE DlabGroup H, then asserts an order automorphism not belonging to the source group inner subgroup. It contains no quantifier over larger Dlab target groups or embeddings. The documentation likewise identifies the original formulation. No Lean build was run by this scope audit, and no claim of independently rechecking the formal proof is made.

The displayed conjugator has two affine pieces (slopes 2 and 1/2, breakpoint 1/3). It fixes the two interval endpoints and belongs to the full interval Dlab group, though it is not identity near them and hence is outside the compact source. Thus it implements the prior automorphism in a larger standard Dlab group, which explains exactly why the formalized original claim does not resolve the current corrected Notebook claim.

This source is prior art, already cited indirectly through its authors' paper arXiv:2607.17477, and is now preserved locally with retrieval hash. The current two-tail result concerns the corrected arbitrary-ambient quantifiers. Its proof is not claimed Lean-formalized.

## 2026-10-17T20:35:26.779672+00:00 — User requested pre-upload explanation

Confirmed explicitly that the Lean theorem IS prior work solving the original wording, which is fully credited. Its own finite conjugator is h(x)=2x for x<=1/3 and h(x)=(x+1)/2 for x>=1/3. This map fixes0 and1, has positive slopes2 and1/2, and is locally right2^Z-affine at0, so it is an element of the full interval Dlab group. It is not identity near0 or1, hence not in the compact source. This is a direct witness that its automorphism becomes inner in a permitted larger group. Our proposed originality concerns only the corrected all-ambient claim. No Zenodo staging/upload has started; final sequential package reviews remain pending.
