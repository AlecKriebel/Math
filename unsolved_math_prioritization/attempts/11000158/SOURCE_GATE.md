# Source, prior-work, and eligibility gate

Checked 2026-10-03. Target 11000158 / AMR-109-0158 was rank 422, queued,
0/5 when read live. No mathematical discovery turn has been opened.

## Original question and inherited conventions

[B] Joan S. Birman, Chapter 10, *3-manifolds, Heegaard distance and mapping
class groups*, in Benson Farb (ed.), *Problems on Mapping Class Groups and
Related Topics*, Problem 2.1, printed p.149 / PDF p.156.
https://math.uchicago.edu/~farb/papers/mcgbook.pdf

The original page was checked visually and through text extraction. The target
requires a precise double-coset formulation for compression bodies, its relation
to their handles, and the knot-space case. The surrounding text on pp.142,
145–146 fixes the compact, connected, orientable setting, oriented gluing,
and fixed-splitting equivalence. The default genus is at least two. It
constructs a knot exterior using a torus product and tunnel 1-handles.
The p.145 convention caps spherical negative boundary; the proof packet
explicitly retains puncture data if literal sphere boundary is also allowed.

## Primary-source comparison

[J] Ian Biringer, Jesse Johnson, Yair Minsky, *Extending pseudo-Anosov maps
to compression bodies*, arXiv:1011.0021v1 (2010), §4, Lemma 4.2,
printed/PDF pp.15–16. Published in *Journal of Topology* 6 (2013),
DOI https://doi.org/10.1112/jtopol/jtt021.
https://arxiv.org/pdf/1011.0021

The checked version characterizes marked compression bodies by their
fundamental-group marking kernels. Equal kernels give a homeomorphism
extending the boundary identification. This directly supplies the converse
needed for the normal-closure stabilizer description, rather than merely
an obstruction to extension. Its proof was read, and the statement on p.15
was visually checked. The compression bodies in that section cap sphere
boundary and have a nonspherical positive boundary. We apply precisely
that result and handle low genus and punctures separately.

[F] Francis Bonahon, *Cobordism of automorphisms of surfaces*,
Ann. Sci. École Norm. Sup. (4) 16 (1983), 237–270,
Appendix B, Proposition B.1 and Corollary B.2, pp.267–268.
https://numdam.org/item/10.24033/asens.1448.pdf

Its minimal complete disk systems are related by slides and isotopies.
This explains why a selected finite handle system must not be frozen
setwise. The group in the answer preserves the complete extension data;
it is independent of which handle system describes that marked body.
The definitions and proof in Appendix B were checked.

[O] Ulrich Oertel, *Mapping class groups of compression bodies and
3-manifolds*, arXiv:math/0607444v2 (2007), Definitions 1.1–1.3 and
Theorems 1.4(b), 1.5, pp.1–3; proof of Theorem 1.5, pp.11–12.
https://arxiv.org/pdf/math/0607444

This source distinguishes the image of unrestricted extension from the
image of extensions fixing the inner boundary. It supplies the restriction
homomorphism and its short exact sequence. Its at-most-one-spherical-inner-
component hypothesis is not silently extended to multiple spheres: the
packet uses the theorem for conventional nonspherical inner boundaries
and treats removed interior balls separately. No generator theorem about
4-dimensional compression bodies is misapplied to this 3-dimensional target.

[S] Martin Scharlemann, *Heegaard splittings of compact 3-manifolds*,
arXiv:math/0007144v1 (2000), §§2.2–2.3, pp.3–5, and §§3.1, 7.
https://arxiv.org/pdf/math/0007144

The construction for a chosen boundary partition and its dual handle
description are standard background. This record does not claim an
algorithm for stabilization or identify distinct fixed-genus splittings.

[A] Ahmed Barbar, *Automorphism-weighted ensembles from TQFT gravity*,
arXiv:2511.04311v1 (6 November 2025), §3.2, equation (3.37).
https://arxiv.org/html/2511.04311v1#S3.SS2

This is an explicit preexisting use of a compression-body group on one side
of the mapping-class-group double quotient and a handlebody group on the
other. It uses the boundary-relative compression-body group and cites [O].
It is corroboration of prior use, not the proof dependency for the gluing
classification. Its formal infinite sums and limiting weights are not
assumed or reproduced.

## Imported data and earlier report

The UnsolvedMath problem page could not be retrieved with the web tool.
The repository's pinned fallback was used:

https://huggingface.co/datasets/ulamai/UnsolvedMath/tree/37e53eabe540fb458758e198be61634bd02ee008

Before selection, the complete `problems.json` and `research_results.json`
bytes matched the sizes and SHA256 values in the repository manifest.
The selected statement agrees with [B]. The report is indexed by the alias
AMR-109-0158. It contains only OPEN-TRIAGE, says it read a truncated
statement, and asks for the full statement. It incorrectly attributes the
chapter to Morandi/Humphries; the primary author is Birman. It supplies no
proof and is not a previous attempt by Alec Kriebel.

The existing individual desk review proposes an extension subgroup but
does not settle markings or scope. Its source hashes are recorded in
`readiness.json`; it is also not a substantive proof attempt.

## Duplicate and prior-attempt checks

Read the root AGENTS.md, queue AGENTS.md, repository README, queue README,
live target row, state.json, and related-target-groups file. The target has
no state entry and its canonical attempt directory returned 404 before
this packet. Exact-ID/default-branch code and commit searches, all-state
PR searches for the ID, alias, Heegaard, Birman, compression body, and
double coset found no matching campaign. All 439 available branch names
were enumerated to an empty terminal page; no target or semantic match
appeared. Related 11000xxx branches refer to different numeric problems.
No exact-target prior user attempt was found in the available conversation
retrieval. This is a bounded accessible-history check, not proof that no
unrecorded attempt ever existed.

The related-target-groups file has no entry for this ID. Catalog keyword
matches include 30001048 (geodesicity of tunnels), 2714 (a Kirby
concordance/fibration problem), and 20002959 (manifold realizability);
their mathematical targets differ from this gluing-equivalence formulation.
They are not solved or reprioritized by this packet.

## Disposition

The full descriptive target follows from the checked primary results and
the standard gluing-orbit argument. Recommend **already_solved 0/5**, as a
credited literature consequence. Independent review must check every
scope item in `PROOF.md` before acceptance. Historical priority for the
first written answer specifically naming Birman's Problem 2.1 is not
established. No claim of novel resolution is supported or intended.
