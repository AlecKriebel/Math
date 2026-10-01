# Source, prior-art, and interpretation audit

Checked2026-09-30. No outside individual was contacted. This bounded review
does not certify novelty or resolve an undefined source convention.

## Original question

Itai Benjamini, *Euclidean vs. Graph Metric*, Question5.7 (with Romain Tessera).
The recovered `erd100.pdf` version has the question on p.7; the `erdos.pdf`
version has it on p.6 with the same mathematical wording.

- [Original author URL](https://www.wisdom.weizmann.ac.il/~itai/erd100.pdf)
- [Archived original PDF](https://arquivo.pt/noFrame/replay/20201231041538id_/http://www.wisdom.weizmann.ac.il/~itai/erd100.pdf)
- [Author-hosted alternate version](https://www.wisdom.weizmann.ac.il/~itai/erdos.pdf)
- [Original talk slides with the same question](https://people.maths.ox.ac.uk/drutu/workshopGG/IBenjamini1.pdf)

The direct PDF download returned502, but the dated archive download succeeded.
Its full text was read around the question and the rendered p.7 was visually
checked. It says triangles have diameter **at most** r, permits ambient
isometries without an orientation restriction, includes both ambient planes,
and asks for periodicity without defining that word. We preserve those facts.

The 2026 paper [Euclidean vs Graph Metric: The Fixed-Source Problem](https://arxiv.org/abs/2606.13271)
addresses a different metric approximation question; it does not provide a
resolution of this triangulation question in the checked text.

## Prior layered family

Dirk Frettlöh and Alexey Garber,
[Symmetries of Monocoronal Tilings](https://arxiv.org/abs/1402.4658),
[published PDF](https://dmtcs.episciences.org/2142/pdf),
[author-hosted text](https://www.math.uni-bielefeld.de/~frettloe/papers/corona.pdf).

- Definition1.3 distinguishes the rank of the translation group
- Definition1.4 calls compact-fundamental-domain symmetry crystallographic
- Theorem2.2 proves planar monocoronal tilings have at least one translational
  period, allowing reflection in matching vertex coronae
- Section2.3/Figure8 describes alternating isosceles-triangle layers I and
  independently chosen chiral triangular layers T0,T1
- AppendixA.1.2/Figure17 explicitly includes non-crystallographic triangulations
- Theorem4.1 treats hyperbolic monocoronal tilings through Böröczky duals, not
  the full metric-ball hypothesis of Benjamini–Tessera

The layered construction is therefore prior work. The present note supplies
specific rational parameters and a separate radius-r shielding proof. No
worldwide priority assertion is made for that metric specialization.

## Hyperbolic leads and why they are not promoted

Kazushi Ahara, Shigeki Akiyama, Hiroko Hayashi, Kazushi Komatsu,
[Strongly nonperiodic hyperbolic tilings using single vertex configuration](https://repository.exst.jaxa.jp/dspace/bitstream/a-is/893128/1/AA1840186002.pdf),
Hiroshima Math.J.48(2018),133–140. Its Theorem1 supplies single-vertex-configuration
rhombus tilings. These are not the required triangle metric-ball examples.
Splitting a rhombus along a diagonal alone does not check the enlarged radius
balls, so no hyperbolic conclusion is inferred here.

Chaim Goodman-Strauss,
[Regular production systems and triangle tilings](https://doi.org/10.1016/j.tcs.2008.12.012)
(2009), supplies weakly aperiodic hyperbolic triangles and related tiling
constructions. The existence of such tilings does not by itself give identical
vertex-centered balls at their maximal triangle diameter. This was a discovery
lead, not a theorem used to settle the present hyperbolic clause.

## Searches and duplicate check

Queries included the exact problem ID, Benjamini+Tessera+triangulation,
Question5.7, periodicity+radius-r isometries, monocoronal metric balls, and
hyperbolic single-vertex configurations. No equivalent full-ball proof was
located in this bounded pass. That is not proof that none exists.

At repository base01358d66fc67d1c462bddf31c0d4ee5b120e6737, the queue row is
rank38, queued0/5, with empty result cells. Exact-ID/code searches found only
catalog and desk-review metadata. No attempt folder, matching issue/PR,
remote branch, related-target group, or matching second dataset statement was
found. The imported prior report is literature triage without a proof.

Pinned source revision:37e53eabe540fb458758e198be61634bd02ee008.
The code AMR-099-0062 occurs once. The full record and prior report are saved
in input_record.json.
