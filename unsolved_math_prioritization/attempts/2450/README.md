# Polynomial lemniscate inradius

Database problem 2450 / Erdős problem 1039. Accepted conventional proof of the uniform positive c/n bound and sharp 1/n order of the worst-case inradius. This is a credited reconstruction of the Price/Kitamura 2026 method; no novelty is claimed.

For monic degree-n polynomials with roots in the closed unit disk, let R_n be the infimum of the inradii of their strict lemniscates {|f| < 1}. The complete proof gives

(log 2)/n <= R_n <= pi/(2n).

Every such polynomial has a root-centered open disk of radius (log 2)/n in its strict lemniscate, and the maximum possible inradius is exactly 1. The exact limiting constant and existence of a limit of n R_n are not proved.

## Documents

- [Complete reconstruction](LEMNISCATE_INRADIUS.md)
- [Complete independent audit and standalone proof](AUDIT.md)
- [Acceptance and precise limitations](ACCEPTANCE.md)
- [Public sources, capture hashes, and inspection history](SOURCE_PINS.json)
- [Aggregate exact diagnostic results](CHECKS.json)
- [Exact preservation results](PRESERVATION.json)
- [Closed public file manifest](MANIFEST.json)

The candidate's historical awaiting-audit sentence is retained; the completed audit and acceptance supersede it. The candidate's stated Lean blob identity has an explicit single-terminal-LF normalization qualification in the audit, acceptance, and source metadata. Selected static source inspection is not Lean execution or compilation verification. The live EP1039 problem/forum pages returned HTTP 403 during inspection, and the linked Overleaf project was inaccessible.

The three 39,357-check diagnostic runs are finite corroboration only. Mathematical acceptance rests on the complete conventional proof. This packet includes only authored documents, public verification metadata, and aggregate checks. The manifest lists all permitted public files and hashes every payload file; its own bytes are pinned by an external preparation seal, avoiding a circular self-hash.
