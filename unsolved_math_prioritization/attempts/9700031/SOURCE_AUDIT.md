# 9700031 / AMR-096-0031: source and prior-attempt gate

Checked 2026-10-02 before substantive author turn 1. This source gate consumes zero proof turns. The direct UnsolvedMath page was inaccessible; the complete pinned problem record and prior report were read from dataset revision 37e53eabe540fb458758e198be61634bd02ee008.

## Exact source and corrections

The imported target is Open Problem 31, Section 8.3, printed pp. 48–49 of Aldous's [2012 manuscript](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf). The [published 2014 paper](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf), EJP 19, paper 15, DOI 10.1214/EJP.v19-2920, renumbers the topic Open Problem 5, Section 8.3, p. 37. Both complete PDFs were downloaded, and both question pages rendered and inspected. Published definitions in Sections 2.2–2.3 and 6.3 were read, including the continuum/measurability discussion and the planted-point consequence (6.4).

For a source-destination pair (x,y), the source measure is dx dy |y-x|^(-beta). Its traffic measure weights the length of the prescribed route R(x,y), rather than choosing a new shortest path or a Steiner subnetwork. The target asks for local finiteness on E(infinity,1), and hence a sigma-finite measure on the union over positive r, for 2<beta<4. The 2012 wording permits additional regularity hypotheses; the published problem also records the distributional push-forward scaling factor c^(beta-5). Additional quantitative assumptions must be explicit and cannot be called consequences of the ordinary axioms without proof.

Contrary to the imported report, E(infinity,r) is not a speed-threshold network. It is the union of route portions at Euclidean distance at least r from both endpoints, obtained through an increasing independent Poisson sample. The basic major-road statistic is expected length intensity p(r)=p(1)/r. The original setup is formulated through finite-dimensional distributions, so a proof of continuum traffic must address joint measurability and the relation of arbitrary endpoint routes to the Poisson-defined major-road sets. The publication year is 2014, not 2011.

## Current primary literature

- Kahn, *Improper Poisson line process as SIRSN in any dimension*, Annals of Probability 44(4) (2016), 2694–2725, DOI 10.1214/15-AOP1032; downloaded arXiv:1503.03976v3. Its construction and major-road finite-intensity result concern the Poisson-roads model. Theorem 5.1's proof supplies Euclidean route-length moments of order below gamma-1. The stronger moments discussed in Remark 5.1 are conjectural, not available input.
- Blanc, *Fractal properties of Aldous–Kendall random metric*, downloaded arXiv:2207.03349v3 (30 January 2023). The main results concern Hausdorff dimension and metric-ball volume properties. Its metric parameter gamma is unrelated to the source-destination exponent beta in this target.
- Blanc–Curien–Kahn, *Geodesics in planar Poisson road random metric*, PLMS 131 (2025), e70070, DOI 10.1112/plms.70070; downloaded arXiv:2407.07887v1 and checked the published full-page primary text. Its main results establish non-pausing geodesics, the geodesic frame, stars/hubs and confluence for that concrete model. They do not state the general traffic-intensity theorem requested here.
- Aldous's maintained SIRSN problem page still links the general problems and distinguishes subsequent Poisson-line constructions. Exact-phrase searches for SIRSN traffic intensity/density and local finiteness found no general resolution. This is a bounded literature check, not a novelty certificate.

The binary hierarchy's bounded-stretch estimate, Proposition 3.1 and its continuum extension in Section 3.7 of Aldous (2014), is known source material. It may provide a concrete application of a theorem with extra stretch assumptions, but it cannot stand in for a theorem about every SIRSN.

## Prior-attempt and related-target check

Live all-state PR searches, both exact attempt-path histories, branch/matching-ref searches, and commit-message searches found no attempt for 9700031 or AMR-096-0031. A read-only local all-reference audit covered 374 refs and found no target path history or matching target/traffic-SIRSN commit messages; its receipt is retained separately. Current related_target_groups.json contains no duplicate entry for this target.

There is a distinct related draft PR #41 for 9700035, on dot/math-9700035 at 292b95ca601f166e6d246e609cf7ed5ca5653e25. Its full proof and source audit were read. It concerns expected spanning-network length and proves a conditional exterior estimate under an extra fourth-tail assumption. It does not settle traffic local finiteness. Its known source definitions, large-excursion caution and model moment citations are useful shared context, not a second independent discovery.

Source PDFs, extracts, renders and raw imported records are local reading material and are excluded from a public mathematical packet. Current status: eligible for a first substantive attempt, 0/5 before that attempt.
