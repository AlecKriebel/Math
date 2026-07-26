# Research log — `D4-DN-3` full descent

## 2026-07-26T04:19:22Z — contact atlas banked

- A corrected all-lower \(E_7/E_6\) reconstruction retained all 18
  lower variables.
- The exact contact projection is two conjugate affine planes with four
  specialization-safe charts of ranks \(7,7,6,5\).
- A separate hostile reconstruction certified the contact radical and
  atlas.  No family exclusion was claimed.

## 2026-07-26T05:07:00Z — transverse obstruction found

- On the plus-plane chart \(k\ne0\), two \(E_5\) coefficients independent
  of all eleven free lower variables were found:
  \[
  3(\sqrt2-2)k(s+c_+k)^2,\qquad
  3(\sqrt2-2)k(s-4k/3)^2.
  \]
- Their zero loci are incompatible.  Galois conjugation gives the same
  conclusion on the minus plane.
- The result was held provisional pending a clean-room derivation and a
  direct PARI replay.

## 2026-07-26T05:16:31Z — legacy boundary proof audited

- A hostile audit matched an older arbitrary-binary descent exactly to the
  punctured intersection and origin of the new atlas.
- The mathematics passed: \(E_4\) forces \(S=0\), \(E_5\) then forces
  \(D=0\), and the remaining system forces \(\det L=0\); the origin has
  two \(E_4\) squares and a Moh exit.
- The old SymPy certificate was not promoted because it substituted
  \(S=0\) without asserting the forcing coefficients and had no
  methodologically independent lower implementation.

## 2026-07-26T05:34:00Z — complete independent exclusion

- A blind clean-room SymPy reconstruction independently derived both
  transverse obstructions, descended the punctured intersection through
  an additional pivot split, and rebuilt the origin before division.
- A direct PARI/GP implementation independently reconstructed the
  transverse coefficients and the entire punctured-intersection/origin
  chain.  Its boundary wrapper includes two required-failure mutations.
- The top-level aggregate combines the primary and hostile contact-atlas
  verifiers with all four clean-room lower charts, both direct PARI
  implementations, optimized-Python rejection, and a third mutation.
- Terminal marker:
  `D4_DN3_FULL_FAMILY_EXCLUSION_STRICT_PASS`.
- Promoted to a certified family-level exclusion.  Fine progress is now
  \(5/26\); the parent row and global quartic denominator do not change.
