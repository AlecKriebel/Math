# Exact controls

Run `python check_turn1.py` from this folder. Its output matches
turn1_receipt.json and contains 5,705 exact assertions. Python and installed
SymPy 1.14.0 are used; there is no downloaded executable or simulation.

The checker implements the primitive right-kernel and symplectic-projection
reduction on generated admissible forms, with nontrivial unimodular changes
of basis. It checks each integral complement, the exact symmetric enlargement
shape, and determinant identities at enough distinct integer points to
certify the bounded-degree polynomial identity, plus a generic symbolic
block calculation. It includes empty, unit, prime and composite cores.

The computations do not claim integral congruence of every pair in a class
or realize surfaces. Those steps have the stated mathematical proofs and
credited primary inputs. The composite case remains unresolved. Source PDFs,
OCR images and text are reading copies and excluded from public checkpoints.
