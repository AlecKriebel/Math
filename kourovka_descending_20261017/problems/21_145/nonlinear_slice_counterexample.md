# A nonlinear quasi-isometric embedding defeating affine slice rigidity

Checkpoint 2026-10-17T20:57:28.100003+00:00. This is a restricted deduction for the research record, not an answer to either original question and not a novelty claim.

Use the standard generators x0,x1 and their word norm |.|. Let L,R be the affine copies of F on the left/right halves. The known block homomorphism j:F x Z->F is j(g,n)=L(g)R(x0^n). It is a quasi-isometric embedding, by the standard tree-pair metric estimates or the classical product-embedding theorem (Burillo; Guba–Sapir; Cleary–Taback).

Define psi(g)=j(g,|g|). The graph map g->(g,|g|) has exact bounds

    d_F(g,h) <= d_F(g,h)+abs(|g|-|h|) <= 2 d_F(g,h).

Therefore psi is a quasi-isometric embedding F->F. Let chi1(f)=log2 f-prime(1-minus), the terminal slope character. It is1-Lipschitz for the standard word metric, and chi1(psi(g))=|g| because the left copy is identity near1 and chi1(R(x0))=1.

For any homomorphism alpha:F->F, any s in F, and any nonidentity w in F-prime, chi1(s alpha(w^n))=chi1(s) for all n: the composite chi1 alpha is a character and kills the commutator subgroup. On the other hand, |w^n| tends to infinity, since F is torsion free and finite word balls are finite. Consequently

    d_F(psi(w^n),s alpha(w^n)) >= abs(|w^n|-chi1(s)) -> infinity.

Thus psi is not bounded distance from ANY left-translated endomorphism. The same argument excludes right-translated endomorphisms and their conjugates. It is not coarsely onto: its image lies in H=Stab(1/2), whose distance from x0^-n is exactly n, as proved separately.

This directly disproves the tempting assertion that every quasi-isometric embedding F->F must lie a bounded distance from an affine homomorphism. Restrictions of a hypothetical F x Y->F quasi-isometry to horizontal slices are only quasi-isometric embeddings. Hence the independently checked affine-slice obstruction cannot be promoted to a full answer by that assertion. Truly nonlinear slice behavior is an explicit surviving mechanism, even though the constructed psi itself is not a full product quasi-isometry.

The fresh partial-result adversary independently checked this argument from its statement before this note was written. Its full review records the exact assumptions and scope.
