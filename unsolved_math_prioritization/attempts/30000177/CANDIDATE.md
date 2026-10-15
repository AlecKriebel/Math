# Four-qubit W: an asymptotic LOCC dense-coding protocol

**Full candidate answer to OWR-785-003: yes, in the source's asymptotic
unitary-encoding model.** Separate adversarial review is pending. The argument
uses the established classical–quantum multiple-access coding theorem; priority
of this application is unestablished. No optimal-capacity, one-copy zero-error,
or experimental-implementation claim is made.

## 1. Source and exact communication task

Dagmar Bruß's contribution, pp.203–205 of
[Oberwolfach Report 4/2005](https://ems.press/journals/owr/articles/785), asks:

> Is the so-called W-state of four qubits in the LOCC dense codeable class?

The preceding page explicitly uses the asymptotic capacity. For the four-party
case, there are two independent classical-message senders, A₁ and A₂, and two
receivers, B₁ and B₂. Initially each holds one qubit of

\[
 |W_4\rangle=\tfrac12(|1000\rangle+|0100\rangle
                         +|0010\rangle+|0001\rangle).
\]

Each sender encodes by unitaries on her own qubits, sends A₁ to B₁ or A₂ to B₂,
and sends no classical message to a receiver. Afterward the receivers may use
local quantum operations, including operations on blocks of their own qubits,
and classical communication between themselves. They may not exchange quantum
systems or perform a joint quantum operation across their spatial partition.
Rates are per copy of W₄, hence per pair of transmitted qubits. The unassisted
benchmark is two classical bits.

The detailed model and the LOCC-DC versus LO-DC distinction are given in
[Bruß et al., Sections 6–7, equations (16)–(26)](https://arxiv.org/abs/quant-ph/0507146).
We retain that model. In particular, an asymptotic vanishing-error block code is
allowed; a single-use perfectly distinguishable alphabet is not required.

**Claim.** With this sender/receiver assignment,

\[
 C_{\mathrm{LOCC}}(W_4)\ \ge\ \frac32+h_2(1/4)>2,
 \qquad h_2(p)=-p\log_2p-(1-p)\log_2(1-p).
 \tag{1}
\]

The non-strict inequality means a supremum of achievable rates. More concretely,
independent message rates \((9/8,9/8)\), totaling \(9/4\) bits per copy, are
achievable with vanishing average decoding error. The state is not LO-DC under
the source's no-communication criterion, as checked in Section 6.

## 2. Allowed encoding and receiver preprocessing

Use the real Pauli representatives

\[
 \mathcal P=\{I,X,Z,XZ\}.
\]

A₁ and A₂ each use their own four-letter alphabet. For a block of n copies, their
respective codewords specify tensor products of these one-qubit unitaries.
Their codebooks are fixed beforehand, their messages are independent, and neither
encoder receives measurement outcomes or feedback.

After the prescribed transmissions, put
\(L=A_1B_1\) at B₁ and \(R=A_2B_2\) at B₂. This is only a reordering of tensor
factors. Permutation symmetry of W₄ gives

\[
 |W_4\rangle_{LR}=
 \frac{|\psi^+\rangle_L|00\rangle_R
             +|00\rangle_L|\psi^+\rangle_R}{\sqrt2},
 \quad |\psi^+\rangle=\frac{|01\rangle+|10\rangle}{\sqrt2}.
 \tag{2}
\]

B₁ measures each L pair in the orthonormal Bell basis
\(\mathcal B=(\phi^+,\phi^-,\psi^+,\psi^-)\), where
\(\phi^\pm=(|00\rangle\pm|11\rangle)/\sqrt2\) and
\(\psi^\pm=(|01\rangle\pm|10\rangle)/\sqrt2\). B₁ sends the outcomes Jⁿ
classically to B₂. Each Bell measurement is local to B₁, because A₁ has already
been transmitted to that receiver.

For input letters x,y, let

\[
 |v_{xyj}\rangle=
 (\langle j|_L\otimes I_R)
 [(U_x\otimes I)_{L}\otimes(U_y\otimes I)_{R}]|W_4\rangle.
\]

The normalized output available at B₂ is the classical–quantum state

\[
 \omega_{xy}^{JR}
   =\sum_{j\in\mathcal B}|j\rangle\langle j|^J
                         \otimes|v_{xyj}\rangle\langle v_{xyj}|^R.
 \tag{3}
\]

The vectors are unnormalized; their squared norms already contain the outcome
probabilities. For n uses the induced channel is precisely
\(\bigotimes_{t=1}^n\omega_{x_ty_t}\). This follows because the resource consists
of independent copies and the preprocessing is the same local measurement on
each copy. Thus (3) is a finite, memoryless cq multiple-access channel with two
separate classical inputs and a single *available output system at B₂*.
It does not posit a global decoder on the original two receivers' quantum data.

## 3. Exact channel spectra

For x=y=I, the four unnormalized conditional states on R are

\[
 \sigma_{\phi^+}=\sigma_{\phi^-}
     =\tfrac14|\psi^+\rangle\langle\psi^+|,
 \quad \sigma_{\psi^+}=\tfrac12|00\rangle\langle00|,
 \quad \sigma_{\psi^-}=0.
 \tag{4}
\]

A Pauli on the first qubit of L permutes its Bell basis, up to phases.
Consequently x only permutes the four blocks in (4). A Pauli y conjugates every
R block by \(U_y\otimes I\). In particular every \(\omega_{xy}\) has nonzero
spectrum \((1/2,1/4,1/4)\), so

\[
 S(\omega_{xy})=3/2. \tag{5}
\]

Take x and y independently and uniformly from \(\mathcal P\). Define

\[
 \omega_x=\tfrac14\sum_y\omega_{xy},\qquad
 \omega_y=\tfrac14\sum_x\omega_{xy},\qquad
 \bar\omega=\tfrac1{16}\sum_{x,y}\omega_{xy}.
\]

These subscripts denote which input remains fixed, not a quantum subsystem.
The qubit Pauli twirl is

\[
 \tfrac14\sum_{U\in\mathcal P}(U\otimes I)\tau(U^\dagger\otimes I)
 =\tfrac{I_2}{2}\otimes\operatorname{tr}_{A_2}\tau.
 \tag{6}
\]

For fixed x, averaging y turns the weight-1/2 product block into
\(I_2\otimes|0\rangle\langle0|/4\), with two eigenvalues 1/4. Each weight-1/4
Bell block becomes \(I_4/16\). The fourth block is zero. Thus the nonzero
spectrum of \(\omega_x\) is two copies of 1/4 and eight copies of 1/16, giving

\[
 S(\omega_x)=3. \tag{7}
\]

For fixed y, each outcome label sees each of the four preimages in (4) once
as x varies. Its R block is

\[
 \tfrac18(U_y\otimes I)
 (|00\rangle\langle00|+|\psi^+\rangle\langle\psi^+|)
 (U_y^\dagger\otimes I).
 \tag{8}
\]

The two displayed vectors are orthogonal. Each of the four blocks has two
eigenvalues 1/8, whence

\[
 S(\omega_y)=3. \tag{9}
\]

Finally, averaging (8) over y yields the same block for every j:

\[
 \bar\omega_j=\tfrac1{16}I_2\otimes|0\rangle\langle0|
                  +\tfrac1{32}I_4
       =\operatorname{diag}(3,1,3,1)/32.
 \tag{10}
\]

Its trace is 1/4. Across all four labels, the spectrum of \(\bar\omega\) is eight
copies of 3/32 and eight copies of 1/32. Therefore

\[
 S(\bar\omega)=5-\tfrac34\log_2 3
              =3+h_2(1/4). \tag{11}
\]

This also checks normalization of all the averaged channel states.

## 4. Independent messages and achievable rates

We use the direct coding theorem for a memoryless cq multiple-access channel,
[Winter, Theorem 9, pp.4–5](https://arxiv.org/abs/quant-ph/9807019v3).
For a product input distribution, independent message rates satisfying

\[
 r_1\le I(X:JR\mid Y),\qquad
 r_2\le I(Y:JR\mid X),\qquad
 r_1+r_2\le I(XY:JR)
 \tag{12}
\]

are achievable in the usual limiting sense by separate classical codebooks and
a POVM on the output block. This established theorem, rather than the mere
Holevo upper bound, supplies achievability. Its hypotheses apply to (3): both
alphabets and the output space are finite, the input distribution is a product,
and the channel tensorizes. No joint encoder or common-message assumption is
inserted.

For the cq state with uniform X,Y, (5), (7), (9), and (11) give

\[
 \begin{aligned}
 I(X:JR\mid Y)&=3-3/2=3/2,\\
 I(Y:JR\mid X)&=3-3/2=3/2,\\
 I(XY:JR)&=3+h_2(1/4)-3/2=3/2+h_2(1/4).
 \end{aligned} \tag{13}
\]

The point \((9/8,9/8)\) is strictly inside (12): each coordinate is below 3/2,
and

\[
 h_2(1/4)=2-\tfrac34\log_2 3>\tfrac34,
 \tag{14}
\]

because \(3^3=27<32=2^5\). Thus the sum 9/4 is strictly below the sum constraint.
Applying the theorem at a slightly larger interior rate pair and trimming the
message sets if desired yields codes with rates tending to 9/8 each and error
tending to zero. Taking rate pairs approaching the sum boundary proves (1).
The approximate sum bound is 2.311278124 bits per copy; the strict advantage
already follows from the exact integer inequality in (14).

## 5. Why the coding-theorem decoder is LOCC here

Winter's POVM acts on \((JR)^{\otimes n}\), all of which is available at B₂ after
receiving Jⁿ. No quantum part of L remains necessary. Moreover all channel states
are diagonal in Jⁿ. Any decoding POVM can be replaced by its pinching in the
classical Jⁿ basis without changing a single decoding probability. It is therefore
implemented as: read Jⁿ and apply the corresponding local POVM to Rⁿ at B₂.

This allows arbitrary collective quantum processing at **one receiver only**,
which is local with respect to B₁:B₂. The decoding stage uses only the forward
classical outcomes from B₁ to B₂. If both receivers must explicitly output the
entire message pair, B₂ can send its decoded classical pair back to B₁. That
optional final classical transmission does not change the rate or error and is
allowed LOCC. Neither operation informs an encoder, supplies extra entanglement,
transmits quantum information between receivers, or changes who receives either
sender's qubits. All measurement branches are retained; no postselection or
success-probability renormalization occurs.

## 6. Class membership and limits of the result

The original one-qubit marginals have spectrum \((3/4,1/4)\), hence entropy
\(h_2(1/4)\). The two-qubit marginals A₁B₁ and A₂B₂ each equal

\[
 \tfrac12|00\rangle\langle00|+
 \tfrac12|\psi^+\rangle\langle\psi^+|,
\]

with entropy one. The source's no-communication expression is consequently

\[
 C_{\mathrm{LO}}=2[1+h_2(1/4)-1]=2h_2(1/4)<2.
\]

If an optional classical-only fallback is included, the corresponding
comparison becomes max{2, 2h₂(1/4)} = 2, with no strict LO dense-coding advantage.
Together with (1), this places W₄ in the source's LOCC-DC shell.

The published LOCC upper bound, from equation (21) of Bruß et al., specializes to
\(1+2h_2(1/4)\), approximately 2.622556249. Thus this proof does not identify the
optimal capacity. Nor does it prove a one-copy accessible-information advantage.
For a useful control, if both receivers Bell-measure each copy under the full
uniform Pauli encoding, the resulting classical output is uniform on 16 outcomes
and has four equiprobable outcomes conditional on either input pair. That
particular measurement has mutual information exactly \(4-2=2\) bits. The block
quantum decoder at B₂ is essential to the achievability argument presented here.
This control is not an upper bound on other single-copy measurements.

## 7. Attribution and reproducibility

Pauli dense coding, Bell-basis processing, cq entropy identities, and Winter's
coding theorem are established tools. In particular,
[Pradhan–Agrawal–Pati, Section 4.2.3](https://arxiv.org/abs/0705.1917) already
uses Bell measurements for a four-state, two-bit W-state protocol. That
single-copy construction is prior work; it does not state the independent-message
asymptotic lower bound proved above. No claim of priority for the present
application is made. The limited current-literature audit is in [SOURCES.md](SOURCES.md).

The standard-library [checker](verify_channel.py) constructs all 16 input pairs
and all 64 unnormalized conditional blocks directly from the four-qubit vector.
It checks their spectra by exact rational power sums, verifies all averages and
marginals, and evaluates the entropy expressions symbolically in
\(\mathbb Q+\mathbb Q\log_2 3\). It also checks the both-Bell negative control.
It does not numerically simulate an asymptotic code or replace the coding theorem.
Run `python3 verify_channel.py` and compare with [verification.json](verification.json).
