# Formulation and literature audit: KP-2.8 / 2756

Assessment date: 2026-10-06. Result: **stalled partial**. No claim of a new theorem solving the full problem.

## Primary formulation

The actual K3 author PDF, page 90, was retrieved and visually inspected. Its problem concerns two distinct trivial n-tangle isotopy classes with the same 2n boundary points. Reflection of the second tangle into the lower half-space produces an unknot with the first. The desired subgroup is the intersection of their stabilizers in the ordinary planar braid group B_(2n). The questions ask for a description and for finite generation and finite presentation across all such pairs, with no upper bridge-number restriction.

The reflection bar is visibly present in the PDF. Its absence in the inherited machine-readable statement is a transcription loss. The source attribution is J. Meier and N. Salter. The source is the K3 book itself, not an AIM workshop summary.

The exact live problem URL failed web retrieval, and a direct HTTP request returned 403. The live page was therefore not inspected. Identity instead rests on the complete exact-ID record, its independently matched statement and record/report hashes, and the primary K3 page. No live-site status is inferred.

## Group-convention correction

HIKK's Theorem 2.1 uses a spherical-braid quotient. Its group is not literally the planar subgroup in K3; the hyperelliptic group in the branched double cover is another related group.

The authored proof establishes the full-preimage relation and computes the missing planar kernel as F_(2n-1) times Z. This makes the low-bridge finiteness transfer rigorous. It also rules out the mistaken inference that a finite spherical quotient makes the planar intersection finite.

## Verified literature and scope

- Brendle-Hatcher, *Configuration spaces of rings and wickets*, Proposition 3.6, gives a finite presentation for each individual planar wicket group. It does not make arbitrary two-stabilizer intersections finitely generated. [arXiv:0805.4354](https://arxiv.org/abs/0805.4354), [publication DOI](https://doi.org/10.4171/CMH/280).
- HIKK Examples 2.8-2.9 give the low-bridge spherical results used in the proof. Their Question 2.10 asks about general finite generation, including the unknot. [Primary manuscript](https://arxiv.org/abs/2004.03098), [publication DOI](https://doi.org/10.1093/imrn/rnab001).
- Iguchi-Koda's *Distance and the Goeritz groups of bridge decompositions*, Theorem 0.1, gives the threshold 5 for spherical n-bridge decompositions in S3 with n >= 3, and threshold 6 in the stated broader setting. The precise theorem is in the 2021 distance paper, not the 2020 *Twisted book decompositions* citation used for this assertion in K3. Its hypotheses do not provide a general answer to the present unknot problem. [Primary manuscript](https://arxiv.org/abs/2105.00631), [publication DOI](https://doi.org/10.2140/pjm.2021.315.347).
- Koda-Tanaka's *The Goeritz groups of (1,1)-decompositions*, version 2 dated 2025-01-27, classifies genus-one, one-bridge decompositions. That is a different surface/bridge-number problem and does not settle arbitrary (0,n) unknot decompositions. Its main theorem and introduction were inspected. [Primary text](https://arxiv.org/html/2403.15809v2).
- Koda-Takao's 2024 *Diagrammatic criteria for strong irreducibility of Heegaard splittings and finiteness of Goeritz groups* supplies conditional Heegaard-diagram criteria, not a universal finite-generation theorem for these unknot bridge groups. Its statement and scope were checked. [Primary text](https://arxiv.org/html/2402.06849v2).

The K3 source is [*K3: A New Problem List in Low-Dimensional Topology*, Problem 2.8](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf). The capping and Birman facts used for the transfer were checked in [Farb-Margalit, version 5.0](https://pagine.dm.unipi.it/~a019210/Farb%20Magalit_Primer%20on%20Teichmuller%20theory.pdf).

## Bounded duplicate/history check

AlecKriebel/Math was searched for the exact numeric ID, KP-2.8 / title, wicket, and tangle-stabilizer terms across pull requests, commits, branches, and default-branch file search, using bounded result limits. No matching substantive work was returned. The current queue row was separately read and was queued at 0/5. These are limited retrieval results, not proof of novelty or absence of prior work elsewhere.

The complete inherited exact-ID record and exact report were reviewed before mathematical work. The only inherited work was dated literature triage; the report was empty. Dataset size/hash and exact statement/pair comparisons all matched. Dataset contents are excluded from this package.

## Outcome and stopping condition

The proof verifies the transfer theorem, the low-bridge consequences n = 2,3, and the obstruction to an invalid general subgroup-intersection argument. It does not solve the universal finite-generation or finite-presentation questions for n >= 4. The remaining quotient problem and missing complex-action hypotheses are specified in `PROOF.md`.

Three approaches were used. The simultaneous-complex route has no proved finite quotient/connectivity/stabilizer package, so work stops at a rigorous partial report. No claim that the general problem remains open is based solely on empty searches; the narrower claim is that no full solution was verified in this bounded review.
