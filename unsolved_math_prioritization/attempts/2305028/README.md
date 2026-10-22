# Function Theory Problem 5.28: known negative answer

Catalogue ID: **2305028** / **AMR-022-5028**.

The proposed asymptotic equality of the interior and boundary moduli of
continuity is false. Rubel, Shields and Taylor proved this in 1975,
Proposition 4.3 of *Mergelyan sets and the modulus of continuity of analytic
functions*. Hayman's Update 5.28 explicitly records the negative answer.
This packet verifies a known resolution; it makes no new-resolution claim.

- [Full self-contained verification](PROOF.md)
- [Source and scope gate](SOURCE_GATE.md)
- [Research log](RESEARCH_LOG.md)
- [Exact arithmetic verifier](verify.py)
- [Recorded verification output](verification.json)

Run `python3 verify.py` in this directory. Python's standard library suffices.
The script verifies arithmetic, not the entire analytic proof.

The construction gives one nonconstant disk-algebra function F with
limsup Ω_F(t)/B_F(t) ≥ 1668/1667 > 1, using chord distance on the circle.
The explicit lower bound is a convenient verification constant and is not
claimed as sharp or new.

This is an AI-assisted, unrefereed research note. Qualified mathematical
review remains important.
