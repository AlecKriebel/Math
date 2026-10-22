# Square selection and contraction rotations for surface obstructions

Status: unsolved. Problem 3327 / OPG-172. Second newly documented substantive investigation, 12 October 2026; lifetime investigation count unknown. No history reset or fresh investigation budget is asserted.

The target is a finite ordinary simple graph G and h≥1 such that G does not embed in N_(h+1), while every proper minor embeds in N_h. Both deletion and contraction are required. Write E for Euler genus and ν for minimum positive nonorientable genus.

## New partial results

- For connected quartic, triangle-free, K_(2,3)-free graphs with two or three squares through each edge, E≤2 is equivalent to an exact square cover of the three-square edges by eligible omitted squares.
- Reversing a consecutive rotation block and its edge signatures raises Euler genus by at most one. The contraction of an h=2 target consequently has strictly alternating endpoint classes in every Euler-genus-at-most-two embedding.
- Every h=2 target edge belongs to at least two 5-cycles; an edge in exactly two squares belongs to at least four. This excludes bipartite h=2 targets and bipartite ordinary Euler hoppers with E=4.
- The co-Heawood graph has E=ν=4. For e=(0,10), its deletion has E=2 and ν=3, and its contraction has E≥3. It fails both the direct target route and the ordinary hopper route. Its equality E=ν also excludes the orientably simple Euler-critical route.

These conclusions do not exclude all higher-genus targets or bipartite orientably simple Euler-critical graphs of Euler genus four. No target graph, universal nonexistence theorem, novelty claim, or claim about the complete current literature is supplied.

## Complete evidence

1. [Full structural proof](STRUCTURAL_REPORT.md).
2. [Full co-Heawood proof](COHEAWOOD_GENUS_REPORT.md), [compact square-orbit certificate](COHEAWOOD_SQUARE_ORBIT_CERTIFICATE.json), [N4 rotation](COHEAWOOD_N4_CERTIFICATE.json), and [deletion torus rotation](COHEAWOOD_DELETE_0_10_TORUS_CERTIFICATE.json).
3. [Independent mathematical audit](INDEPENDENT_AUDIT.md), [exact acceptance record](ACCEPTANCE.json), and [independent checking guide](CERTIFICATE_GUIDE.md).
4. [Integration and acceptance boundary](INTEGRATION_AND_ACCEPTANCE.md), [source identities](SOURCE_IDENTITIES.json), and [public byte manifest](PUBLIC_MANIFEST.json).
5. [Unchanged first edition](../3327_surface_obstruction_reductions_20261012/README.md) and its [complete independent acceptance](../3327_surface_obstruction_reductions_20261012/INDEPENDENT_EDITION_ACCEPTANCE.md).

The first edition's twelve companions are preserved byte for byte. Its earlier co-Heawood E≥3 statement describes that edition's evidence; this edition supplies the additional exact E=ν=4 proof. The mathematical audit is computational and mathematical review, not human peer review. Public files contain authored prose, small exact mathematical objects, and public source metadata.
