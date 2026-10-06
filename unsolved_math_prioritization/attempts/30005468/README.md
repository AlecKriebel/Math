# Published fixed moment separator

This branch records the literal fixed-polynomial result for
30005468 / OWR-12697710-015. The current paper and finite verification supplement
are [available at DOI 10.5281/zenodo.23196750](https://doi.org/10.5281/zenodo.23196750), with the
[published files](https://zenodo.org/records/23196750). The exact publication and tracker
readbacks are in PUBLICATION_RECEIPT.json; the tracker range is 'Math Puzzles'!A34:D34.

The original author budget remains 1/5. Integration, reproduction, literature
comparison and preprint review did not consume a new author proof-search turn.
The note was prepared and checked extensively with AI tools. It is unrefereed;
no independent human peer review or formal proof-assistant certification is
claimed. Two fresh whole-package AI adversarial reviews and ROOT acceptances
are recorded under audit/. Their scope is the exact final package, not a
worldwide priority or current-openness certification.

The exhibited polynomial is fixed: p=1+f, where f is Scheiderer's classical
rational ternary quartic that is a sum of real squares but not rational squares.
On K={1-x^2-y^2-z^2>=0}, p has minimum one. The rational degree-four moment vector
has all 35 entries, m_0=1, m_(4,0,0)=-1 and all other entries zero. It has no
nonnegative representing measure, even on R^3, and L_m(p)=0. For the displayed
ball generator g, p belongs to 1+Q_R(g) but not to 1+Q_Q(g), at every finite
multiplier degree. Rational certificates mean rational polynomial square
factors, equivalently rational positive-semidefinite Gram data.

This is an affirmative instance of the phenomenon asked about in the printed
fixed-polynomial OWR question, with that explicit rational-square convention.
It does not establish a PSD-input case: M_2(m) has diagonal entry -1 at x^2.
The same m has a rationally certified separator q=1+x^4. The polynomial p itself
is rationally certifiable in Q_Q(g), and every rational rescaling c*p with c>1
is rationally certifiable in 1+Q_Q(g), by Powers' strictly positive ball theorem.
For c<1 even the real normalized membership is impossible at the origin.
The rational-coefficient real-SOS multiplier list (f,0) already exists, so that
weaker requirement is not obstructed. No all-separator, strict-margin, minimum
relaxation degree, general descent or world-first claim is made.

Read PROOF.md for the proof, SOURCE_SCOPE.md for the interpretation, and preprint/paper.tex for the concise research note. Extract the published verification archive and run its verify_package.py without changing its files. The original 2,059 finite controls support exact identities; they do not prove the all-degree theorem by finite search.

The quartic, norm/Galois construction and real identity are Scheiderer (2016),
Theorem 2.1 and Example 2.8. The local leading-term mechanism is classical:
Scheiderer (2000), Lemma 1.1 and the proof of Proposition 6.1; Benoist (2022),
Remark 2.7; and the ball-module argument in Nie's May 26, 2011 author version,
Example 5.3. Earlier irrational semidefinite infeasibility certificates include
Naldi--Sinn (2021), Example 3.8. The note's contribution is the explicit
fixed-separator application and normalization clarification, with these
established ingredients credited. It introduces none of those ingredients.

All eighteen originally submitted bodies are preserved byte-for-byte in audit/original_submission/. HISTORICAL_ERRATUM.md identifies their historical status. No downloaded third-party source PDFs are redistributed.
