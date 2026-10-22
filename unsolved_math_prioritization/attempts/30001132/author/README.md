# Smooth Schubert cycles and admissible Gelfand–Zetlin faces

Problem 30001132 / OWR-3384-004, queue rank 665.

## Result

The proposed universal statement is false under the original definition of admissibility. This is an existing published negative result, not a new resolution: Valentina Kiritchenko's final article, *Gelfand–Zetlin Polytopes and Flag Varieties*, IMRN 2010(13), 2512–2531, states on p. 2522 that a smooth Schubert cycle for SL4 has no admissible-face representative. The older preprint and 2009 Oberwolfach report contain the conjecture instead.

This packet supplies an authored reconstruction identifying the example as the dimension-three class indexed by 2413 in the conventions of `PROOF.md`. A 24-row exact certificate excludes every Borel subgroup containing the fixed diagonal torus. A direct projective-bundle description proves smoothness without relying on a pattern-avoidance convention. The proof addresses the specific orbit-to-face correspondence; it does not exclude representations by unions or sums of faces, or other polytope-ring identities.

## Reading and reproduction

- `PROOF.md`: conventions, smoothness, complete finite obstruction proof.
- `certificate.json`: one violated face equation for each of the 24 Borel choices.
- `verify_faces.py`: exact diagram-based enumeration for n=2,3,4.
- `check_certificate.py`: a separate exact-rational tangent-cone checker, importing no code from the generator.
- `APPROACH_LOG.md`: research accounting and stopping decision.
- `SOURCE_VERIFICATION.json`: bibliographic information, public URLs, hashes, inspection history, and version discrepancy.
- `LIMITATIONS.md`: precise scope, audit status, and non-novelty.
- `TEST_RESULTS.json`: reproduced checks.
- `MANIFEST.json`: safe packet inventory and hashes.

Run with Python 3.10+ standard library only:

```
python3 verify_faces.py --output enumeration.json
python3 check_certificate.py certificate.json
```

Expected nonrepresentable permutations for n=4 are 2413, 3412, 4231. Only 2413 is smooth; all classes are represented for n=2 and n=3. The main negative proof needs only the 24 vertex obstructions, not completeness of the positive-class enumeration.

## Sources

- [Published article DOI](https://doi.org/10.1093/imrn/rnp223), [institution-hosted published PDF](https://publications.hse.ru/pubs/share/folder/omll7zg0oc/66625291.pdf), p. 2522.
- [Author-hosted revised manuscript](https://users.mccme.ru/valya/flag.pdf), p. 9.
- [Original report](https://ems.press/journals/owr/articles/3384), pp. 24–25.
- [Earlier arXiv version](https://arxiv.org/abs/0906.4866), Conjecture 3.2.

No source PDFs, source text, dataset contents, or private correspondence are included in this packet. No remote change was made during this investigation. Independent review is required before publication.
