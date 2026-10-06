# Initial independent source comparison

Pinned before reading any candidate or review. Source: complete Volker Kaibel contribution, *Open Problem: Arborescences and NP-hardness*, Oberwolfach Report 50/2018, printed pages 3014-3015, PDF pages 46-47. The PDF page images and independent text extraction were both inspected. Date: 2026-10-06T04:07:43.351516+00:00.

## Exact literal Problem 2

Input is a directed graph D=(V,A), a supplied root r in V, and one cost vector c^v in R^A for every v in V\{r}. The feasible object is an arborescence T contained in A for which the r-v path P^v contained in T exists for every v in V\{r}. This forces T to span V, even though the adjective spanning is not repeated in this problem. The path direction is away from r toward v; an in-arborescence directed toward r does not satisfy literal r-v directed paths. The supplied root is fixed for the instance and is not another optimization choice. Each v has its own full arc vector; c^v(P^v) means the sum of the coordinates c^v_a over a in the unique r-v path. The objective is sum over nonroot destinations of these path costs. The root contributes no cost vector or nonempty root path. A graph without a rooted spanning arborescence can be infeasible; feasibility is not assured by the literal source.

The source permits arbitrary real entries, not only rational, integral, nonnegative, or bounded costs. A classical finite-input NP-completeness statement needs an explicitly encoded rational or integer decision subclass and threshold. NP-hardness on such a subclass proves hardness of the optimization task on any input model supporting that subclass. It does not put an unencoded arbitrary-real task into NP. Restrictions such as DAGs, small integer coordinates, few cost-bearing destinations, or guaranteed feasibility can strengthen a hardness theorem if proved, but are not source requirements.

## Adjacent Problem 1 is a separate formulation

Problem 1 starts with an undirected graph G=(V,E), uses the two directed versions of every edge, supplies one c^r for every possible root r, and selects one undirected spanning tree T minimizing the sum over all roots of c^r(T^r). These are costs on full rooted directed tree arc sets, not costs on one supplied-root path per destination. A solution to literal Problem 2 does not automatically solve Problem 1. Their placement under one contribution is not an equivalence proof.

## What the source certifies

Both questions use the parenthesized wording `(Why)` and ask whether the following problem is NP-hard. This is a request for a hardness explanation, not a theorem proving hardness and not evidence that every subsequent explanation is new. The stated motivation says Problem 1 is equivalent to integer optimization over Martin's extended formulation of the spanning tree polytope; Problem 2 is equivalent to integer optimization over Wong's extended formulation. The word integer is material. A polynomial description of a continuous relaxation does not itself imply polynomial-time integer optimization. The motivation supplies context and an asserted equivalence, but no explicit formulation, reduction, proof of exact coefficient correspondence, or history of prior solutions. It certifies neither historical novelty nor the absence of a pre-existing NP-hardness result, and cannot make a proof about ordinary minimum-cost arborescence solve this path-vector objective.

## Success and falsification criteria for this audit

Accept the mathematical/source gate only if the frozen candidate proves a finite-encoded decision hardness result for this literal supplied-root, spanning out-arborescence, destination-dependent path objective, with every advertised additional restriction actually satisfied. Independently check membership in NP, polynomial reduction size, numerical bounds relevant to any strong-hardness label, exact equality/gap, both directions, and boundary cases. Test tempting polynomial reinterpretations against the literal per-destination objective. Historical priority remains separate from proof validity. This is verification only: zero new proof-search turns.
