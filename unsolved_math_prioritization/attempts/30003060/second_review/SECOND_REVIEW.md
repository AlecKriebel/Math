# Independent review of the higher Koszul characteristic obstruction

Problem 30003060 / OWR-14218-004, supplied rank 865. Review dated 6 October 2026 UTC.

## Decision

Accept the mathematical counterexample to the literal unrestricted-field equivalence. The free associative algebra k<x,y> is Koszul in every characteristic, but its higher Koszul homology in degree one is nonzero in every positive characteristic. The characteristic-zero vanishing-to-Koszulness question is not resolved by this argument.

The source record does not justify treating an exclusively characteristic-zero historical intention as established fact. The proposed wording patch removes that implication and adds contemporaneous evidence. It does not alter the mathematics. The original archive remains unchanged. This is an independent AI-assisted review, not human peer review or formal proof-assistant certification. No publication or priority claim is made.

## Inputs and independence

The reviewed author archive is HIGHER_KOSZUL_30003060_AUTHOR_SAFE_FREEZE.zip, 17,517 bytes, SHA-256 571f5c0834dc0996cd8a2c75915e24b77b45295f1866af6bc7d71695b8789714. Its external manifest has SHA-256 1b54474d1e6b45c176a3ed7cb699c8837a179c9f908ed90df937c2c5c5c1404b; the original external bootstrap has SHA-256 b89fd41e4187f4ff30ea5ba358b94099ef633f18c7591a7f44c569add3ebed63. All three pins and all 11 member size/hash bindings were independently checked before any archive script was run. Extracted originals were kept separate from derivatives.

The mathematical and source-scope conclusions below were established independently before receiving another reviewer's conclusions. The later execution-hardening work is separately scoped and is not accepted by implication in this report. The complete dataset was not rehashed in this second review; source-scope acceptance is based on the original scholarly contribution and the detailed primary paper, independently retrieved and inspected. No conclusion here depends on treating the author's source-inspection record as independent evidence.

## Original question and historical scope

The complete Solotar contribution, including its references and adjacent contribution boundaries, was read on printed pp. 479-481 of the [2016 Oberwolfach report](https://ems.press/journals/owr/articles/14218). Its question equates Koszulness with positive-degree higher Koszul homology vanishing and gives no field-characteristic restriction. The report's opening context supplies no shared restriction for all talks. Nearby speakers' assumptions cannot be imported.

In the published [Berger-Lambre-Solotar paper](https://doi.org/10.1017/S0017089517000167), Theorem 6.4 explicitly assumes characteristic zero. The displayed Conjecture 6.5 does not repeat that hypothesis and includes the additional degree-zero condition. Immediately preceding it, the authors consider removing the characteristic restriction as well as asking for a converse. The same distinction occurs on p. 24 of [arXiv v1](https://arxiv.org/abs/1512.00183v1), dated 1 December 2015, before the workshop.

Thus the unrestricted reading has direct textual support. The characteristic-zero converse is a natural research motivation, but exclusive historical intent is uncertain. Neither declaring the entire research question solved nor dismissing the counterexample as automatically outside the printed scope is justified.

## Definitions and signs

Use coefficients in A itself. Set A=T_k(V), where V has basis x,y, and relation space R=0. Since each W_q for q>=2 contains a factor R, all those spaces vanish. The coefficient-A Koszul chain complex is

0 -> A tensor V --b--> A -> 0,

where b(a tensor v)=av-va. This agrees with BLS Section 2.2, formula (7), with homological degree one. Consequently HK_1(A)=ker b, HK_0(A)=A/im b, and HK_q(A)=0 for q>=2.

BLS Section 5.2 defines the higher differential by cap product with the fundamental degree-one cocycle in every characteristic. On an ordinary cycle, its degree-one specialization is delta([sum a_i tensor v_i])=[sum a_i v_i]. The left-cap expression using v_i a_i gives the same class, because their difference is a commutator. There is no missing minus sign or Euler-weight factor. Both b and delta lower homological degree by one and raise coefficient weight by one, preserving total weight.

These conventions are not ordinary Koszul homology alone and do not use trivial-module coefficients. In particular, positive ordinary HK_1 is entirely compatible with A being Koszul.

## Independent verification of Koszulness

A direct bimodule proof verifies the precise BLS convention without needing an unstated equivalence of definitions. The augmented bimodule complex is

0 -> A tensor V tensor A --d--> A tensor A --mu--> A -> 0,

with d(a tensor v tensor c)=av tensor c-a tensor vc and mu(a tensor c)=ac.

Fix a word w of length n. In A tensor A, the basis vectors whose concatenation is w correspond to the n+1 possible cuts of w. Call them e_0,...,e_n. In A tensor V tensor A, the corresponding n basis vectors mark one distinguished letter; call them f_0,...,f_(n-1). Then d(f_i)=e_(i+1)-e_i, and mu sends every e_i to w. The n consecutive differences are linearly independent over any field and span exactly the coefficient-sum-zero subspace. The assertion also holds for n=0, with no f_i. Summing these exact blocks over all words proves exactness in every degree and over every field. Hence A is Koszul under BLS Definition 2.1. The author's shorter linear left-resolution argument is also valid.

## Characteristic two witness

In characteristic two, z=x tensor y+y tensor x is nonzero because its terms are different basis vectors. Its ordinary differential is (xy-yx)+(yx-xy)=0 even over the integers. Its higher image is [xy+yx]=2[xy]=0 in A/im b. The quotient is by the commutator vector subspace, not by an ideal; [xy]=[yx] holds already because b(x tensor y)=xy-yx.

No ordinary boundary can kill z because the degree-two chain space is zero. No higher boundary can kill its nonzero ordinary homology class because HK_2(A)=0. Therefore HK^hi_1(F_2<x,y>) is nonzero. The class has homological degree one, coefficient weight one, and total weight two. The relevant total-weight-two higher H_1 space is exactly one-dimensional.

## Every positive characteristic and the full orbit formula

Let char(k)=p>0. The p rotations of w=x^(p-1)y are distinct, since the unique y occupies different positions. Write each rotation w_i=a_i v_i with v_i its last letter, and let z_p=sum a_i tensor v_i. Concatenation identifies these distinct terms with distinct words, so z_p is nonzero even though there are p summands. Its differential telescopes as sum(w_i-rho(w_i))=0, where rho moves the last letter to the front. In A/im b all rotations have the same class, so delta([z_p])=p[w]=0. The absence of degree-two chains and homology again excludes both kinds of boundary. Its coefficient weight is p-1 and total weight is p. This proves the claim for every field of positive characteristic, including odd characteristic; it is not an inference from finitely many primes.

For completeness, at total weight n>=1 identify A_(n-1) tensor V and A_n with the word space E_n. Then b=1-rho. On a cyclic orbit O of size d, ker b consists of constant-coefficient sums of the d basis words and is one-dimensional in every characteristic. The quotient E_O/im b is one-dimensional too: differences identify all basis words, and a linear functional assigning 1 to every basis word proves that their common class is nonzero. This functional does not require division by d.

Delta is induced by the identity from ker b to coker b and maps the orbit sum to d times that common class. Thus each orbit contributes one dimension to both higher H_1 and higher H_0 exactly when p divides d, and contributes zero otherwise. In characteristic zero no positive-weight orbit contributes. Weight zero supplies the usual copy of k in higher H_0, and higher H_q vanishes for q>=2. Orbit cardinality d, rather than the possibly larger word length n, is the correct scalar; periodic words do not invalidate the calculation.

The extra higher-H_0 condition displayed in BLS Conjecture 6.5 does not rescue the unrestricted equivalence. The same free algebra violates it in positive characteristic. It satisfies the expected acyclicity in characteristic zero, so this construction says nothing against the characteristic-zero conjecture.

## Computational checks and their limits

The original author bootstrap reproduced RESULTS.json byte-for-byte. Separately, the verified extracted author checker was run directly with python -I -S -B and again reproduced that result. Code inspection found only standard-library exact arithmetic and explicit diagnostic checks in the mathematical checker. The original bootstrap's execution-isolation limitations are left to the separately scoped hardening audit; a successful replay is not a claim that the bootstrap is secure against every startup configuration.

The included independent_check.py does not import or call author code. It uses a different matrix invariant: because delta is the inclusion ker B -> coker B, its kernel is ker B intersect im B, of dimension rank(B)-rank(B^2). It compares this exact rank computation over Q and F_2,F_3,F_5,F_7,F_11 against a least-period count in 120 cases: one generator through weight 9, two through weight 7, and three through weight 4. It checks 13 primitive witnesses through prime 101, plus characteristic-zero and one-generator negative controls. All pass. These finite controls are not the proof of the universal claims.

The review bootstrap requires isolated, no-site, no-bytecode, nonoptimized Python in the parent and explicitly applies the same flags to the independent checker. It pins the external manifest and validates the full ZIP, exact inventory, paths, regular-file types, sizes, and member hashes before parsing or executing payload code. Its role is replay integrity, not a mathematical proof assistant.

## Patch and acceptance scope

SOURCE_SCOPE.patch changes only four authored files: README.md, PROOF.md, SOURCE_AUDIT.md, and SOURCE_METADATA.json. It qualifies historical intention and records the pre-workshop source. Full corrected files and exact before/after bindings are supplied. It makes no mathematical change and no execution-code change. Applying this patch to the pinned original succeeds exactly. The original archive is not replaced.

Recommended disposition: accept a characteristic-scope counterexample to the literal unrestricted formulation; keep the characteristic-zero equivalence and especially its converse unresolved in this investigation. A concise public description is: “The unrestricted-field statement fails: k<x,y> has nonzero degree-one higher Koszul homology in every positive characteristic. This leaves the characteristic-zero converse unresolved.”

No independent exhaustive current-literature search, novelty certification, or claim that the converse is universally open as of today is made. The deliverable contains authored analysis, code, hashes, public URLs, and correction files only. Retrieved PDFs, their extracted text and images, dataset contents, and private coordination are excluded.
