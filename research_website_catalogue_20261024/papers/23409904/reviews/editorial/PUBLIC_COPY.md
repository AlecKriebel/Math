# Global Hessian realizations of statistical manifolds

Alec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X) · Version 1.0, 15 October 2026 · CC BY 4.0

A global positive-Hessian realization of smooth statistical manifolds with a proper embedding, explicit finite dimension and the prescribed ordered dual connections.

## Original abstract

Let M be a smooth, Hausdorff, second-countable n-manifold without boundary, with a positive Riemannian metric and two prescribed, mutually dual, torsion-free connections. For n≥1 we construct a proper smooth embedding into an open subset of ℝ^{binomial(2n+4,3)} carrying one smooth positive Hessian potential. Orthogonal projection of the ambient standard connection and its metric dual induces exactly the ordered pair of given connections. Finite polynomial features provide a smooth global scalar third-jet lifting; a variable tubular neighborhood and a pointwise Schur estimate provide ambient positivity without compactness or uniform bounds. For a general Riemannian dual pair, vanishing of both torsions is necessary and sufficient for such realization. This supplies a self-contained answer in the smooth statistical category to the historical dually flat realization question. Historical novelty and present openness are not asserted; important prior constructions and unresolved primary-source coverage are specified.

## The idea in plain English

A statistical manifold combines a Riemannian metric with two mutually dual ways of differentiating tangent vectors. This note constructs a higher-dimensional space with a single Hessian potential whose metric and projected connections reproduce all that prescribed data.

The construction works for smooth positive statistical manifolds of any fixed finite dimension, including noncompact, disconnected and incomplete ones. It gives a proper embedding and an explicit finite ambient dimension. The surrounding open domain depends on the data and may be nonconvex or incomplete.

Polynomial features lift the required metric and connection data into one finite-dimensional family. A variable normal-neighborhood correction then makes the ambient ordinary Hessian positive along the entire embedded manifold, without assuming uniform geometric bounds.

This is an explicit construction in the historical geometric setting. Substantial prior statistical-embedding, contrast-function and local Hessian constructions are credited. Material earlier final-source coverage remains unresolved, so no first-answer or current-open-status claim is made.

## The precise result

Let (M,g,∇,∇*) be smooth, with M a Hausdorff, second-countable manifold without boundary of one fixed finite dimension n≥1, g positive definite, and ∇,∇* a prescribed ordered mutually g-dual pair of torsion-free connections. There exist N=binomial(2n+4,3)>n, an open U⊂ℝᴺ, one smooth Ψ:U→ℝ with positive ordinary Hessian G=Hess Ψ, and a proper smooth embedding f:M→U such that f*G=g.

The standard ambient connection D and its G-dual D* are both flat and torsion-free on U. Their G-orthogonal tangential projections induce exactly ∇ and ∇*, in that order. Flatness refers to these affine connections; it does not assert vanishing Levi–Civita curvature of the Hessian metric.

For a general smooth positive Riemannian dual pair on the same class of manifolds, realization by orthogonal projection from a torsion-free dually flat statistical manifold is possible if and only if both prescribed torsions vanish. Necessity applies separately to each connection; sufficiency is the construction.

No compactness, connectedness or completeness is required. A second-countable zero-dimensional manifold is treated separately as a countable discrete set, properly embedded in ℝ with Ψ(z)=z²/2; the empty case is vacuous.

## Why the result holds

Duality and both torsion conditions identify the ordered connections with ∇=L−C♯/2 and ∇*=L+C♯/2, where L is Levi–Civita and C=∇g is totally symmetric. Proper Whitney embedding into ℝ^(2n+1), followed by all polynomial features of degree at most three, supplies the same finite space spanning scalar third jets at every point.

A smooth fiberwise right inverse lifts compatible scalar-jet data without a finite atlas or a uniform inverse bound. Differentiating the frozen-coefficient identities gives the exact metric and connection signs and a global covector field φ with φ·df=0. This vanishing compatibility form avoids a global primitive or period obstruction; global injectivity of φ is not needed.

A variable-radius Euclidean normal neighborhood of the closed embedded image supplies Ψ₀(z)=φ_r(z)(ν(z)). Its tangent Hessian block is the prescribed positive metric, while its mixed block B may be unbounded. Adding λ(r)|ν|² with λ=1+tr(A⁻¹)‖B‖²_HS preserves the first jet and gives a positive normal Schur complement at least (2+t)I, where t=tr(A⁻¹)‖B‖²_HS.

The positive-Hessian locus of this one smooth function is an open U containing the whole image. Its unchanged first jet recovers the metric and the ordered projected connections. The gradient of Ψ gives local affine coordinates for D*, proving dual flatness without a globally injective gradient map. Projecting the two ambient torsion identities proves the two necessity statements.

## Scope and limitations

The result is for smooth positive Riemannian data on Hausdorff second-countable boundaryless manifolds of fixed finite dimension. Boundary, indefinite-metric and lower-regularity extensions are not asserted.

Positive Hessian means positive definiteness of the ordinary second-derivative matrix, not positivity of the scalar value of Ψ. U is data dependent and may be nonconvex and incomplete. The dual affine coordinates are local; neither global injectivity of ∇Ψ nor a global embedding of φ is required or concluded.

The theorem supplies no fixed finite probability model and makes no claim that N is optimal. An unrestricted finite-simplex embedding theorem would already imply the historical existence answer through the Fisher Hessian potential; properness alone does not certify novelty.

The final Lê 2006 article, final Lê 2007 chapter, separate Lauritzen Lancaster pair note and Abe article remain material unverified primary bodies in the bounded priority comparison. The complete Ay–Jost–Lê–Schwachhöfer chapter, including page 239, was not obtained. These are historical attribution limits, not deductive inputs of the explicit proof. No first solution, first priority, absence of earlier equivalent work or current worldwide openness is certified.

The universal claim rests on the written construction and standard differential topology. Exact finite controls and numerical examples corroborate identities. Numerical tolerances are diagnostic choices rather than proved roundoff bounds.

## Status and AI use

AI tools were used extensively in research, writing and checking. This is an unrefereed preprint without external human or journal peer review or formal proof-assistant certification; the author is responsible for its claims.

The manuscript and declared publication date are 15 October 2026, version 1.0. Zenodo created the record on 16 October 2026 UTC. These dates do not establish priority.

## Read the paper

Read the complete 6-page paper in the on-page PDF reader.

[Open the PDF](https://aleckriebel.com/research/global-hessian-realizations-statistical-manifolds/global-hessian-realizations-v1.0.pdf)

[Download the PDF](https://aleckriebel.com/research/global-hessian-realizations-statistical-manifolds/global-hessian-realizations-v1.0.pdf) (download)

[Download the Zenodo original PDF](https://zenodo.org/records/23409904/files/global-hessian-realizations-v1.0.pdf) (download)

On-page PDF reader: [Global Hessian realizations of statistical manifolds — complete paper PDF](https://aleckriebel.com/research/global-hessian-realizations-statistical-manifolds/global-hessian-realizations-v1.0.pdf)

## Supporting materials

[Complete source and verification materials (ZIP)](https://aleckriebel.com/research/global-hessian-realizations-statistical-manifolds/global-hessian-realizations-source-verification-v1.0.zip) (download)

[Zenodo original ZIP](https://zenodo.org/records/23409904/files/global-hessian-realizations-source-verification-v1.0.zip)

## Collaborate on this result

Substantive collaboration on independent verification, a meaningful mathematical extension, or development toward journal submission is welcome. Authorship and responsibilities would reflect actual research and writing contributions and mutual agreement.

## Cite this paper

Kriebel, Alec. (2026). Global Hessian realizations of statistical manifolds (Version 1.0, 15 October 2026). Zenodo. 10.5281/zenodo.23409904.

[10.5281/zenodo.23409904](https://doi.org/10.5281/zenodo.23409904)

```bibtex
@misc{kriebel2026_23409904,
  author = {Kriebel, Alec},
  title = {Global Hessian realizations of statistical manifolds},
  year = {2026},
  month = oct,
  doi = {10.5281/zenodo.23409904},
  url = {https://aleckriebel.com/research/global-hessian-realizations-statistical-manifolds/},
  version = {1.0},
  publisher = {Zenodo},
  note = {Unrefereed preprint; version 1.0, dated 15 October 2026. Zenodo record created 16 October 2026 UTC. Prepared with extensive AI assistance.}
}
```

## Background and prior work

[Amari, Information geometry; Furuhata, Matsuzoe and Urakawa, historical problem list](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en). The induced-dual-structure question and its smooth positive geometric interpretation; historical listing does not establish present openness.

[Lauritzen, Statistical manifolds](https://doi.org/10.1214/lnms/1215467061). Prior metric/cubic, dual-connection and orthogonally induced-connection framework. The distinct Lancaster note Conjugate connections in statistical theory is credited for pair embeddings; its original body was unavailable.

[Matumoto, Any statistical manifold has a contrast function](https://doi.org/10.32917/hmj/1206128255). Global contrast functions from compatible scalar third-order data are an important predecessor; contrast existence alone is different from the Hessian ambient embedding.

[Whitney, Differentiable manifolds](https://doi.org/10.2307/1968482). The classical proper smooth finite-dimensional embedding input, including the noncompact case.

[Gualtieri, smooth normal-neighborhood theorem](https://www.math.toronto.edu/mgualt/courses/17-1300/docs/17-1300-notes-11.pdf). The classical variable-radius tubular neighborhood supplies a global normal retraction without compactness or a constant radius.

[Marugame, The Bonnet theorem for statistical manifolds](https://arxiv.org/abs/2103.10102v1). The local pair/Hessian equivalence and positive transverse correction are direct antecedents. The inspected preprint and accepted manuscript are distinguished from the publisher version.

[Lê, Monotone invariants and embeddings of statistical manifolds](https://arxiv.org/abs/math/0506163v6). Finite jets, free maps and right inverses have earlier Nash–Gromov and statistical-embedding ancestry. Earlier texts contain broader finite-simplex claims; the inspected v6 finite-model theorems assume compactness. Final 2006 and 2007 bodies remain unresolved for priority comparison.

[Ay, Jost, Lê and Schwachhöfer, Information Geometry, Chapter 4](https://doi.org/10.1007/978-3-319-56478-4_4). The accessible actual Theorems 4.10 and 4.11 distinguish finite models for compact input from countable models for noncompact input. The complete chapter was unavailable.

[Loi and Matta, Robustness of statistical manifolds](https://arxiv.org/abs/2110.06145v1). Prior free-map and minimum-norm inverse construction for already-induced statistical data; that starting assumption does not itself realize arbitrary prescribed data.

[Osipov, Locally conformally Hessian and statistical manifolds](https://arxiv.org/abs/2209.02357v3). Genuine global Hessian realizations in the stated constant-statistical-curvature classes, credited in their actual scope.

[Abe, Affine immersions and conjugate connections](https://dl.ndl.go.jp/en/pid/11196378). Material historical reference, Tensor 55(3), 1994, 276–280; its original article body was unavailable in the bounded comparison.
