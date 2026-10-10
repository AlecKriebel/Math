# Consolidated acceptance and exact scope

On 2026-10-07, two independently authored full mathematical reviews accepted the unchanged proof in `public/PROOF.md`. Neither acceptance requires a mathematical patch. Optional source-citation improvements remain separate from the frozen proof.

The author manifest SHA-256 is `7df56d745e4c57a30d0303388b1adda3e52d1c99190d2f96fe50b6d616b1cf3f`. The proof has 17,635 bytes and SHA-256 `a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2`.

Audit A manifest SHA-256: `22d1bab327e70db3d594c2580f592256bb342bd33c1081fa07beb1c197f0edff`.

Audit B manifest SHA-256: `8bbb5b62a4610881e7b1f78a52f7c208723529304dd0e8ab341a1be9f1283459`.

## Accepted theorem

Every smooth Hausdorff second-countable positive-definite statistical n-manifold without boundary, n>=1, with mutually dual torsion-free smooth affine connections admits a proper smooth global embedding into an open domain U in R^N with positive Hessian metric, where N=binomial(2n+4,3), inducing the metric and both specified connections in the correct order. The ambient dual connections are flat and torsion-free. The proof treats dimension zero separately. For general mutually dual pairs, torsion-freeness of both is necessary for realization in this torsion-free ambient class.

The construction combines a proper Euclidean embedding, a finite scalar 3-jet spanning family, a smooth global right inverse, an exactly conormal compatible pair, and a variable normal quadratic correction in a tubular neighborhood. Positivity uses pointwise bounds rather than compactness or a uniform spectral bound. Global potential compatibility is identically zero, avoiding an unproved vanishing-period assumption.

## Source interpretation and exclusions

FMU's 1998 item 1(a), printed p.125, is read with its cited Amari 1997 account of flatness, which includes vanishing torsion and curvature and only local affine coordinates. The original source does not impose ambient convexity, completeness, a fixed probability model, or globally injective gradient coordinates. The accepted result uses precisely this geometric scope. The two complete audits discuss the interpretation and primary sources in detail.

The noncompact theorem does not rely on a broad older abstract of Lê's finite-probability-model result. Lê's corrected later version explicitly requires compactness for those claims. Proper Whitney embedding, smooth bundle metrics on paracompact manifolds, and smooth tubular neighborhoods are declared external mathematical inputs.

No claim is made to historical novelty, journal acceptance, optimal dimension, convexity, completeness, globally injective dual coordinates, finite probability-simplex realization, indefinite/nonsmooth metrics, manifolds with boundary, or a torsion obstruction in the larger class allowing torsionful curvature-flat ambient connections.

## Evidence levels

The full proof and both mathematical reviews address the global existence argument. Author finite checks record 26 exact residuals plus numerical positivity samples; audit A records 63 controls in six groups; audit B records 72 exact residuals and additional negative controls. Those finite checks supplement mathematical review and do not establish the global theorem by computation. Integrity scripts establish byte identity and scope binding, not mathematical truth. This draft is AI-assisted and unrefereed.
