# Public sources and verification metadata

The mathematical arguments in this package are authored analyses. Citations establish context and conventions, not an assertion of novelty or an exhaustive open-status review. See SOURCE_GATE.md for inspection history and qualifications.

1. Daniele Micciancio, *Ideal Lattices: cryptographic applications and open problems*, IPAM, October 13, 2006. Historical question: PDF p.37; coefficient model: p.23.
   - https://helper.ipam.ucla.edu/publications/SCWS1/SCWS1_6240.pdf
   - Workshop schedule: https://docs.ipam.ucla.edu/today/helper_schedule.php?pc=SCWS1
   - Retrieved PDF: 824541 bytes; SHA-256 878de5ec70efe17303b591df6154c833d14c35bf096470df454fc6e22ac4d4c2.
2. Phong Q. Nguyen and Damien Stehle, *LLL on the Average*, corrected ANTS VII 2006 version, section 2: two-parameter LLL conventions and distinct SVP/Hermite guarantees.
   - https://perso.ens-lyon.fr/damien.stehle/downloads/average-corrected.pdf
   - Correction notice: https://perso.ens-lyon.fr/damien.stehle/practLLL.html
3. Thomas Plantard, Willy Susilo and Zhenfei Zhang, *LLL for ideal lattices: re-evaluation of the security of Gentry–Halevi's FHE scheme*, accepted March 4, 2014. Theorem 2 addresses iLLL correctness, not an extremal approximation lower-bound family.
   - https://thomas-plantard.github.io/pdf/PlaSusZha14.pdf
   - https://doi.org/10.1007/s10623-014-9957-1
   - Retrieved PDF: 583160 bytes; SHA-256 6633f875d29c448de30b45955984c05d740fef4f13d88167bc6e5e4db29b14d4.
4. Chris Peikert and Alon Rosen, ECCC report 2006/147, section 1.4. Ideal-lattice worst-case hardness context is not a worst-case LLL-output construction.
   - https://eccc.weizmann.ac.il/report/2006/147/download
5. Paul Kirchner, Thomas Espitau and Pierre-Alain Fouque, *Algebraic and Euclidean Lattices: Optimal Lattice Reduction and Beyond*. Abstract/introduction inspected for related algorithmic context.
   - https://eprint.iacr.org/2019/1436.pdf
6. Johannes Buchmann and Richard Lindner, *Density of Ideal Lattices*, preliminary draft, Dagstuhl 2009. Fixed-order counting does not supply the coefficient-geometry density transfer needed here.
   - https://d-nb.info/1367234891/34

Source files are not redistributed. Hashes identify the inspected bytes, not independent proof of their contents. Bounded searches did not establish an exhaustive current literature status.
