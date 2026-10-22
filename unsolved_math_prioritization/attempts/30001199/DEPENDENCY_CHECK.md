# Provisional check of a published proof dependency

**30001199 source audit, not a counterexample to the source's main circular rule.** The 2010 paper's Theorem4 claims the exact positive result for the linear model. Before using it as a literature-resolution certificate, the displayed Lemma1 and its proof require clarification. The original journal PDF has been read through indexed primary text; direct binary retrieval returns403 and screenshot rendering is unavailable, so a possible transcription issue is not excluded. Do not publish an unqualified error allegation from this provisional check.

Reference: F. Kerber and A. van der Schaft, *Compositional analysis for linear systems*, Systems & Control Letters59 (2010),645–653, DOI10.1016/j.sysconle.2010.08.002. Lemma1 at p.648, equation(22), and AppendixA at p.651. Primary indexed PDF: https://pure.rug.nl/ws/portalfiles/portal/2629447/2010SystContLettKerber.pdf .

## Reading under test

For a full simulation relation R of P1||Q2 by Q1||Q2, the displayed construction adds vectors (a,b',c,−b) whenever (a,b,c,b') belongs to R and each component lies in the kernel of both of its output maps. The claim is that R plus this new subspace remains a full simulation relation. AppendixA appears to infer that a derivative vector from R also satisfies those componentwise output-kernel restrictions. Instantaneous output kernels need not be invariant.

## Exact test

Use scalar P1=Q1 with A=B=G=L=C=H=0. Use P2=Q2 with

A = [[0,1],[0,0]], B=G=L=0, C=H=[1,0].

All spaces are finite-dimensional real vector spaces; unused inputs may be chosen scalar with zero matrices. Both circular premises are identity simulations, and the conclusion is an identity simulation too. Thus this test **does not refute Theorem4 or the OWR conjecture**.

Write a vector in the first premise's simulation product as (a,b1,b2,c,d1,d2). The diagonal full simulation relation is

R = {(a,b1,b2,a,b1,b2)}.

The kernel restrictions in the displayed construction force b1=d1=0 and permit arbitrary b2=d2. Its added subspace therefore contains

v = (0,0,1,0,0,−1).

Both outputs agree at v, since they are initially zero. The product-system drift maps v to

A_aug v = (0,1,0,0,−1,0).

The two Q2 outputs of this derivative vector are 1 and −1. Every vector of R plus the displayed added subspace has matching first Q2 coordinates b1=d1, so A_aug v is outside the enlarged relation. Since L=0, no target disturbance can compensate for this failure of invariance. Equivalently, the resulting deterministic Q2 outputs from these initial states are t and −t, unequal for every t>0.

The exact checker confirms the diagonal relation is full/invariant/output-preserving, v lies in the added subspace, the enlarged relation is initially output-preserving, and its derivative leaves the relation.

## Consequence for the current audit

Under the indexed formula, the displayed enlargement lemma fails even in a deterministic identity-comparison case. This is a narrow proof-dependency issue. A version using a suitably invariant unobservable subspace would be a different construction requiring proof; it is not silently inserted here. The main circular theorem might have a valid proof independent of this formula. The next action is independent verification of the primary formula and dependency, not promotion to either a main-theorem counterexample or an established literature solution.
