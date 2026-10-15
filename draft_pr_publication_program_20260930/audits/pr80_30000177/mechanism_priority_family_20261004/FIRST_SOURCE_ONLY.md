# FIRST_SOURCE_ONLY — immutable model freeze

Frozen before candidate, author SOURCES, prior reviews, sibling verdicts, or ROOT conclusions were read.

The target is the symmetric four-qubit W state in the LOCC dense-codeable class (Oberwolfach Report 4/2005, contribution “Distributed quantum dense coding”, printed pp.203–205, final question p.205). Context: Bruß, D’Ariano, Lewenstein, Macchiavello, Sen(De), Sen, PRL 93, 210501, published 19 November 2004; author PDF and quant-ph/0407037v3 dated 8 December 2004. The expanded text quant-ph/0507146v1 is dated 15 July 2005. Its PDF typesetting timestamp 7 November 2018 is not the submission date.

The exact operational allocation for four qubits is two distant senders A1,A2 and two distant receivers B1,B2. Each sender applies a local unitary selected by her own classical message, with product distribution p(i1)p(i2); A1 sends her physical qubit noiselessly to B1, A2 hers to B2. Only the receivers may communicate classically during decoding across A1B1:A2B2. Joint quantum operations within either receiver lab, including collective decoding of arbitrarily many copies, respect that LOCC partition. There is no sender-to-receiver free classical side channel, no prior joint sender lab, no quantum transfer between receivers.

The target capacity is asymptotic, optimized over unitary encoding and receiver LOCC accessible information. The nonentangled dimensional benchmark is log2 dA1+log2 dA2=2 bits per shared W4 copy/two transmitted qubits. Dense-codeability requires a strict sum rate >2, not equality. A protocol with exact optimal capacity is unnecessary to decide class membership; a sound achievable strict lower bound is sufficient.

The original 2004 texts explicitly leave W4 LOCC-DC unknown. They establish W4 not LO-DC, and a nontrivial LOCC upper bound, not an achievability theorem for that bound. The expanded text repeats the original sender/receiver restriction and states that it considers only unitary encoding. Its Sec.6–7 uses genuine accessible information and the additive upper bound; therefore a mere entropy/Holevo value, or a one-copy postselected success without weighted asymptotic error accounting, is insufficient.

Source reading: retained complete PDF files for all four originals; extracted full files and inspected all four pages of both 2004 versions, all fourteen pages of expanded 2005 text, and complete OWR contribution pp.203–205. Visually inspected OWR pp.204–205, 2004v3 p.3, PRL p.4, 2005 p.7 to check typography/equations/partition. The unrelated OWR contributions were not adjudicated.

No submitted-protocol mathematical validity verdict or priority conclusion has been reached at this freeze.
