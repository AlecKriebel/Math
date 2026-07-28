# Problem normalization

Let \(D=d^n\) and identify
\[
(\mathbb C^d)^{\otimes n}_A\otimes
(\mathbb C^d)^{\otimes n}_B
\cong \mathbb C^D_A\otimes\mathbb C^D_B.
\]
A vector \(\psi\) is represented by its \(D\times D\) coefficient matrix
\(C\), with
\[
|\psi_C\rangle=\sum_{x,y}C_{xy}|x\rangle_A|y\rangle_B,\qquad
\|\psi_C\|^2=\|C\|_F^2,\qquad
\operatorname{SR}(\psi_C)=\operatorname{rank}C.
\]

For \(S\subseteq[n]\), write \(P_S=\bigotimes_{i\in S}P_d^{(i)}\), with
identity on the complementary pairs.  The central exact task is to express
\(\langle\psi_C|P_S|\psi_C\rangle\) as a squared Frobenius norm of a partial
contraction of \(C\), and then control the alternating weighted sum
\[
\sum_{S\subseteq[n]}(\alpha d)^{|S|}
\langle\psi_C|P_S|\psi_C\rangle
\]
under the sole constraint \(\operatorname{rank}C\leq2\).
