# 6800007: totally real immersions into the complex flag manifold

**Complete classification candidate; independent adversarial review pending.**

The proposed classification uses ordinary integral cohomology and an explicit cokernel of cup-product maps. It includes a precise existence condition and retains nonorientable torsion. The proof covers a fixed smooth 3-manifold without boundary, including the noncompact case, with homotopies through totally real immersions and no properness condition. It does not classify embeddings or quotient by source diffeomorphisms.

- [Complete candidate and scope](CANDIDATE.md)
- [Original-source and prior-art audit](SOURCES.md)
- [Exact algebra checker](verify.py) and [receipt](verification.json)
- [Pinned original record](source_record.json), [source hashes](source_manifest.json), [readiness](readiness.json)
- [Research log](RESEARCH_LOG.md), [attempt count](turns.jsonl), [status](status.json)

The h-principle, the three-sphere case, and general homogeneous-space obstruction theory are prior work. No novelty or verified-solution claim is made. The finite checks validate algebra only; independent review must validate the topology and all stated quantifiers.

Run `python3 verify.py`; requires SymPy (tested with 1.14.0). One substantive attempt used out of five.
