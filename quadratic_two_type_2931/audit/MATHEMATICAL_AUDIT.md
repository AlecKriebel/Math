# Independent mathematical audit: KP-4.55 (ID 2931)

Audit date: 2026-10-06. Outcome: **accepted as a stalled partial after precision corrections**, five approaches used. No full solution, counterexample, new classification result, or novelty claim is accepted.

## Exact question and invariant

The source asks for ordinary homotopy equivalence of closed, connected, orientable topological 4-manifolds with finite fundamental group and isomorphic quadratic 2-types. Smoothness, stabilization, a fixed marking, and simple homotopy equivalence are not additional requirements. The adjacent definition includes the group, its second-homotopy module, the first Postnikov invariant, and the equivariant form. The printed labels KPR24/KNR22 in Remark (1) are interchanged; the preceding paragraph and actual papers identify the intended references. The cached primary PDF was independently re-extracted and page 234 was freshly rendered and visually checked. [K3](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf)

Concretely, a quadratic-2-type isomorphism has a group isomorphism alpha and an alpha-semilinear module isomorphism beta, with beta(gx)=alpha(g)beta(x), carrying the k-invariant to the other k-invariant and carrying the equivariant form by the induced group-ring isomorphism. The first three data determine the homotopy 2-stage; the form is additional. An orientation-reversing equivalence changes the sign of the form. One must not silently restrict the target to orientation-preserving equivalence.

## Necessary proposition: independent proof check

Choose identifications u:P2(M) -> B and v:P2(N) -> B, with f=u p_M and g=v p_N. If h:M -> N is a homotopy equivalence, define a=v P2(h) u^{-1} in the homotopy category. Postnikov naturality gives a f homotopic to g h. Applying the same construction to a homotopy inverse of h proves a is a self-equivalence. This addresses both the existence and invertibility of the induced map, rather than assuming an arbitrary invariant isomorphism extends to h.

Because each manifold is closed, connected and oriented, H4 is infinite cyclic and h_*[M]=epsilon[N] for epsilon=+1 or -1. Naturality in integral homology gives a_*f_*[M]=epsilon g_*[N]. The contrapositive is valid. The relevant coarse action is the group of homotopy classes of all self-equivalences of B, together with the central sign action, on H4(B;Z). Altering u or v merely changes representatives in these orbits; altering orientations changes signs. Thus the obstruction is independent of markings and orientation choices.

No prescribed identification is required to be realized. Failure for one identification is insufficient. Using every self-equivalence, even ones not preserving a fixed form, gives a valid necessary obstruction. The proof contains no converse. Its finite-group assumption is harmless and not used in this elementary argument. The cited fundamental-triple classification is a substantially stronger external input and is not being reproved. Its exact pointer is the Introduction and Section 2.1, Theorem 2.1. [HKPR](https://arxiv.org/html/2508.07504v1)

## Polarization, torsion and realization

For a realized fixed quadratic 2-type with finite group, HH Theorem 3.1 supplies the torsor; Remark 3.2 requires the action of Aut(B,w,lambda) to forget polarization. In the orientable setting w is trivial. This torsor action must not be confused with the signed action used for the necessary obstruction. The derivative explicitly records nonemptiness/realizability of the initial Poincare type. [HH, Section 3](https://arxiv.org/html/1712.04572v3)

The elementary example S=T with either the indiscrete or equality relation correctly proves that a nontrivial torsor alone does not determine quotient cardinality. It makes no claim about the actual topological action. Separately, a Poincare homotopy type need not contain a manifold. Consequently, nonzero Gamma coinvariant torsion for (Z/2)^3 proves neither ordinary orbit separation nor two manifold realizations. The packet accurately stops at both gaps. No computed orbit, Gamma calculation, or manifold construction has been independently supplied.

## Nearby-source exclusions

- KPR and KNR give positive cases with exact Sylow hypotheses, summarized in SOURCE_AUDIT.json. Their conclusions cannot be expanded to every finite group.
- HN Theorem 6.16 concerns doubles of minimal finite 2-complexes with a fixed finite group. Isometric quadratic 2-types imply equal quadratic bias. Hence examples distinguished by this bias have different quadratic 2-types. The converse is not claimed. [HN](https://arxiv.org/html/2412.15089v3)
- HU Corollary D combined with KNV Theorem C separates ordinary from simple equivalence; ordinary equivalence already holds. KNV's smooth construction uses pi*pi, infinite for a nontrivial finite pi. Both exclusions are sound. No surgery calculation was re-proved. [HU](https://arxiv.org/abs/2602.05003v1), [KNV](https://arxiv.org/abs/2405.06637v2)
- Kupers-Powell starts with h-cobordism/torsion-realization data, with extra conditions. Since both inclusions of an h-cobordism are homotopy equivalences, that premise already implies ordinary equivalence of the ends. It does not produce an equivalence from a bare quadratic 2-type isomorphism. [KP](https://arxiv.org/html/2604.27635v2)
- Pavlov's infinite-group classification requires p to be an odd prime and the additional compatible form. This hypothesis is now explicit. It does not resolve the finite orientable target. [P](https://arxiv.org/html/2608.03245v1)

## Corrections and acceptance boundary

CORRECTIONS.patch changes only precision and audit-status wording: HKPR location, explicit nonempty realized torsor setting, the exact 4-periodic/Sylow condition, Pavlov's odd-prime and compatible-form hypotheses, and corresponding completed-audit notices. The main proposition and its proof are unchanged. The patch was actually applied to a clean extraction and every resulting byte matched the corrected packet.

Acceptance covers the proof of the necessary condition, the logical gap analysis, and accurately bounded literature triage. It does not certify the full proofs of cited theorems, a new classification, a solution of the original problem, or exhaustive literature coverage. The independent exact-byte acceptance is supplied separately from integrity-check results.
