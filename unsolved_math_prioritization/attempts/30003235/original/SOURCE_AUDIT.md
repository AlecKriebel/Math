# Source and status audit

Checked 2026-10-07. This is a bounded primary-source review, not an exhaustive current-status or priority certificate. Source files are excluded from this public packet; hashes and sizes identify locally inspected public PDFs.

## Original target

Hanna Husakova's contribution “Davenport's problem: an overview” in *Arbeitsgemeinschaft: Diophantine Approximation, Fractal Geometry and Dynamics*, Oberwolfach Reports 13 (2016), 2749--2792, p.2780, asks whether the positive epsilon in the affine-line coefficient condition can be removed. The official report page dates publication to 21 December 2017. This endpoint question is distinct from Davenport's earlier full-rank Jacobian theorem; the supplied catalogue's assessment mixes those topics.

Public report: https://ems.press/journals/owr/articles/15169
DOI: https://doi.org/10.4171/OWR/2016/48
PDF: https://ems.press/content/serial-article-files/46650

The p.2780 overview prints an unrestricted pair a,b and does not explicitly exclude a=0. It also contains a nearby malformed phrase around a,b. We checked the rendered page. The theorem it summarizes is An--Beresnevich--Velani's Theorem 1.2, which expressly requires a!=0 and the positive-weight condition (1.1). Those are the intended theorem's hypotheses used in this investigation. The wider curated statement is false in the horizontal case; PROOF.md provides a complete explicit construction. At i=0 or j=0, 1/sigma is undefined, so the displayed endpoint condition cannot simply be read literally. Under the usual zero-weight convention the bad set reduces to a one-coordinate condition; this is a separate elementary scope, not the endpoint exponent problem.

## Exact credited line theorem

Jinpeng An, Victor Beresnevich, Sanju Velani, *Badly approximable points on planar curves and winning*, Advances in Mathematics 324 (2018), 148--202, Theorem 1.2, pp.152--153, and Remarks 3--5. The same theorem is in the 2014 arXiv preprint. The final published page 152 was rendered and visually inspected, and text from pp.152--153 was checked. The exact theorem gives winning for any fixed inhomogeneous shift, under positive excess exponent; it already allows zero excess for nonzero rational slopes. Remark 4 gives necessity of the endpoint coefficient lower bound; Remark 5 states the correct horizontal exponent 1/j.

Paper: https://doi.org/10.1016/j.aim.2017.11.009
ArXiv: https://arxiv.org/abs/1409.0064
Published PDF: https://eprints.whiterose.ac.uk/id/eprint/124399/1/1_s2.0_S0001870817303286_main.pdf

The dual characterization, coordinate-fiber theorem, and winning-intersection properties used here are credited standard inputs. The coordinate-fiber winning theorem is attributed by ABV to Jinpeng An, *Badziahin--Pollington--Velani's theorem and Schmidt's game*, Bull. London Math. Soc. 45 (2013), 721--733. We verified its statement through ABV and the OWR report, not by claiming a new full reading of An's original proof.

## Later results checked

Victor Beresnevich, Erez Nesharim, Lei Yang, *Winning property of badly approximable points on curves*, arXiv:2005.02128v3, 23 December 2020, Theorem 1.1 (later Duke Math. J. 171 (2022)). The primary PDF and its introduction were checked. Its analytic map must be nondegenerate: 1 and its component functions must be linearly independent over R. The map x->(x,ax+b) fails that hypothesis identically. Thus this later absolute-winning theorem does not settle the affine-line endpoint.

https://arxiv.org/abs/2005.02128

Shreyasi Datta, Liyang Shao, *Winning of inhomogeneous bad for curves*, published online 21 October 2024, Mathematische Annalen 391 (2025), 4037--4061. The publisher's accessible introduction and main theorem were inspected, not its entire proof. Its curve hypothesis is again nondegenerate analytic. Its more general inhomogeneous winning conclusion is not an endpoint theorem for affine lines.

https://doi.org/10.1007/s00208-024-03012-6

Targeted searches also considered phrases combining affine lines, weighted bad approximation, critical/zero epsilon, nonempty intersections, and recent winning results. No full resolution of the exact intended irrational-slope endpoint was located. Search silence is not evidence of global openness or novelty of any partial in this packet.

## Retrieval and inspection record

SOURCE_IDENTITIES.json contains the exact byte counts, SHA-256 digests and retrieval times of four complete public PDFs. All were successfully downloaded before mathematical drafting. The two ABV versions were compared at the theorem statements; the final edition, not the preprint alone, supports the hypothesis correction. OWR p.2780 and ABV final p.152 were inspected as rendered images after web screenshot delivery failed. Local rendering succeeded. Full PDF retrieval does not mean every proof page was studied.
