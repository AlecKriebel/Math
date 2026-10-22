# Mathematical dependencies and exact source versions

## Original source and convention

Miklós Abért, Some questions, 2 November 2010, printed page 4, Question 24.
Actual source: https://www.renyi.hu/~abert/questions.pdf
PDF SHA256 576000d7a042147021311cb8fd944e414d8d49db73642fcaf06dd9c2d90aa4e1.
The actual seven-page source was read, including the introduction, section
contexts, Question22's explicit unimodularity clause and Question23's known-unimodular comment, Question
24's arbitrary vertex-transitive wording and its Cayley comment. Printed4
was visually inspected. There is no implicit global unimodularity restriction.
The source omits a normalization formula. The present theorem states and uses
b_F = Edeg_FUSF/2 - 1; it proves unequal expected degrees directly.
The author's warning that questions may since have been solved is retained as
a priority limit, not an invitation acted on. No outreach was prepared.

## Electrical and forest imports

Benjamini–Lyons–Peres–Schramm, Uniform spanning forests,
Ann. Probab. 29 (2001), 1–65, DOI 10.1214/aop/1008956321.
Actual read body: https://rdlyons.pages.iu.edu/pdf/usf.pdf ,
corrected author version 27 January 2009.
SHA256 17da5f8f44c41ae071c306743155bab0ae56863cb2652bb010ae006963333693.
Read finite electrical/Thomson discussion and Theorem4.1 with its proof;
complete opening Section5 free/wired induced-exhaustion definition and
exhaustion independence; Section7 free/wired distinction, Proposition7.1,
Theorem7.3 proof and transfer-current Theorem7.8. Not every theorem in the
long paper was independently audited. The note uses only:
- finite Thomson minimization of energy and Rayleigh monotonicity;
- finite Kirchhoff marginal P(edge in UST)=unit-conductance resistance;
- free exhaustion and its independence, giving the free limiting marginal.

No mass-transport, full infinite-network square-summable minimization,
forest connectedness theorem or joint-flow feasibility is required for the
negative comparison. Such an infinite-network energy minimization would
generally be WIRED resistance, not the quantity used here.

## Established graph and context

Pengfei Tang, Weights of uniform spanning forests on nonunimodular transitive
graphs, Electron. J. Probab.26(2021),1–62, DOI 10.1214/21-EJP709.
Actual read body: https://arxiv.org/pdf/1908.09889v2 , 3 December 2020.
SHA256 819b0faeb961c4b27d4f01213d518564bb16420f9b1fe4c0b6e23a63717bf109.
Read actual Section2.3 criterion/modular setup and complete Section5.2,
printed40–48, including Lemma5.4, Claim5.6, Propositions5.8–5.9 with proofs
and Remarks5.10–5.12. This is the same grandparent graph family; its
connectivity/branching results are credited but not needed as proof inputs.
The full automorphism-group recovery in our note is directly demonstrated.
Final journal PDF access returned an HTML challenge rather than a scholarly
body. Journal metadata/DOI were authenticated via the Crossref primary
publisher-deposited record; final PDF bytes are not claimed read.

Gábor Pete and Ádám Timár, The free uniform spanning forest is disconnected
in some virtually free groups, depending on the generator set,
Ann. Probab.50(2022),2218–2243, DOI 10.1214/22-AOP1581.
Actual read body: https://arxiv.org/pdf/2006.06387v2 , 24 January 2021.
SHA256 93c983afa07300ea25efc7d538f5da5786603896e6ddb7122052f6d7d4e6c6eb.
Read introduction, Theorems1.1–1.3 and explicit expected-degree versus
component-count distinction. The long disconnection/lightness construction
was not independently re-proved. Final journal PDF request returned an HTML
challenge; journal metadata/DOI were authenticated, not final-body identity.

Damien Gaboriau, Invariant percolation and harmonic Dirichlet functions,
Geom. Funct. Anal.15(2005),1004–1051, DOI 10.1007/s00039-005-0539-2.
Actual read body: https://arxiv.org/pdf/math/0405458v3 .
SHA256 a17243287c3eb2313e35f80f9fe88b6d4cfb8e9c136201beb47e4a9167172e55.
Read preceding mass-transport discussion and actual Section2.4 through
Proposition2.9/Definition2.10. It explicitly assumes a transitive unimodular
action. This is contextual support, not authority for dropping that hypothesis.

The two infinite conductance derivations, contraction bounds, complete
root-neighbor count, finite graph specification and finite-flow-to-free
upper-bound transfer are written explicitly in main.tex.
