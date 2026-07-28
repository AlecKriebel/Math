// Discovery-only alternating minimization for rank-at-most-two coefficient
// matrices C = U V^T.  No conclusion from this file is used as proof.
//
// Build:
//   c++ -O3 -std=c++17 agent_witness_altmin.cpp -o agent_witness_altmin
// Run:
//   ./agent_witness_altmin <d> <n> <alpha> <restarts> <alternations> <seed>

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <vector>

using Vec = std::vector<double>;

static double g_alpha = -0.5;

static int ipow(int a, int n) {
  int r = 1;
  while (n--) r *= a;
  return r;
}

static double dot(const Vec& x, const Vec& y) {
  double s = 0.0;
  for (size_t i = 0; i < x.size(); ++i) s += x[i] * y[i];
  return s;
}

// Apply the tensor product of the local maps
//       L_alpha(A) = A + alpha Tr(A) I
// to a D by D coefficient matrix, represented row-major.
static Vec apply_L(const Vec& input, int d, int n) {
  const int D = ipow(d, n);
  Vec cur = input, next(D * D);
  int stride = 1;
  // The least significant base-d digit is processed first.
  for (int site = 0; site < n; ++site, stride *= d) {
    for (int a = 0; a < D; ++a) {
      const int da = (a / stride) % d;
      for (int b = 0; b < D; ++b) {
        const int db = (b / stride) % d;
        double z = cur[a * D + b];
        if (da == db) {
          double tr_fiber = 0.0;
          for (int x = 0; x < d; ++x) {
            const int aa = a + (x - da) * stride;
            const int bb = b + (x - db) * stride;
            tr_fiber += cur[aa * D + bb];
          }
          z += g_alpha * tr_fiber;
        }
        next[a * D + b] = z;
      }
    }
    cur.swap(next);
  }
  return cur;
}

static Vec make_C(const Vec& U, const Vec& V, int D) {
  Vec C(D * D, 0.0);
  for (int a = 0; a < D; ++a)
    for (int b = 0; b < D; ++b)
      for (int r = 0; r < 2; ++r)
        C[a * D + b] += U[a * 2 + r] * V[b * 2 + r];
  return C;
}

static double quotient(const Vec& U, const Vec& V, int d, int n) {
  const int D = ipow(d, n);
  Vec C = make_C(U, V, D);
  Vec LC = apply_L(C, d, n);
  return dot(C, LC) / dot(C, C);
}

// Orthonormalize the two columns of A.  R is returned row-major so A_old=Q R.
static bool thin_qr(const Vec& A, int D, Vec& Q, double R[4]) {
  Q.assign(D * 2, 0.0);
  double r00 = 0.0;
  for (int i = 0; i < D; ++i) r00 += A[i * 2] * A[i * 2];
  r00 = std::sqrt(r00);
  if (r00 < 1e-13) return false;
  for (int i = 0; i < D; ++i) Q[i * 2] = A[i * 2] / r00;
  double r01 = 0.0;
  for (int i = 0; i < D; ++i) r01 += Q[i * 2] * A[i * 2 + 1];
  double r11 = 0.0;
  for (int i = 0; i < D; ++i) {
    const double z = A[i * 2 + 1] - r01 * Q[i * 2];
    Q[i * 2 + 1] = z;
    r11 += z * z;
  }
  r11 = std::sqrt(r11);
  if (r11 < 1e-13) return false;
  for (int i = 0; i < D; ++i) Q[i * 2 + 1] /= r11;
  R[0] = r00; R[1] = r01; R[2] = 0.0; R[3] = r11;
  return true;
}

// Replace U,V by Q,V R^T while preserving U V^T and making U orthonormal.
static bool orthonormalize_left(Vec& U, Vec& V, int D) {
  Vec Q;
  double R[4];
  if (!thin_qr(U, D, Q, R)) return false;
  Vec W(D * 2);
  for (int i = 0; i < D; ++i) {
    W[i * 2]     = V[i * 2] * R[0] + V[i * 2 + 1] * R[1];
    W[i * 2 + 1] = V[i * 2 + 1] * R[3];
  }
  U.swap(Q);
  V.swap(W);
  return true;
}

// Replace U,V by U R^T,Q while preserving U V^T and making V orthonormal.
static bool orthonormalize_right(Vec& U, Vec& V, int D) {
  Vec Q;
  double R[4];
  if (!thin_qr(V, D, Q, R)) return false;
  Vec W(D * 2);
  for (int i = 0; i < D; ++i) {
    W[i * 2]     = U[i * 2] * R[0] + U[i * 2 + 1] * R[1];
    W[i * 2 + 1] = U[i * 2 + 1] * R[3];
  }
  U.swap(W);
  V.swap(Q);
  return true;
}

// Jacobi diagonalization. Returns a normalized eigenvector for the least
// eigenvalue of real symmetric H.
static Vec least_eigenvector(Vec H, int m, double& eval) {
  Vec E(m * m, 0.0);
  for (int i = 0; i < m; ++i) E[i * m + i] = 1.0;
  for (int sweep = 0; sweep < 80; ++sweep) {
    double off = 0.0;
    for (int p = 0; p < m; ++p)
      for (int q = p + 1; q < m; ++q)
        off = std::max(off, std::abs(H[p * m + q]));
    if (off < 1e-12) break;
    for (int p = 0; p < m; ++p) {
      for (int q = p + 1; q < m; ++q) {
        const double hpq = H[p * m + q];
        if (std::abs(hpq) < 1e-14) continue;
        const double tau = (H[q * m + q] - H[p * m + p]) / (2.0 * hpq);
        const double t = (tau >= 0.0 ? 1.0 : -1.0) /
                         (std::abs(tau) + std::sqrt(1.0 + tau * tau));
        const double c = 1.0 / std::sqrt(1.0 + t * t);
        const double s = t * c;
        const double app = H[p * m + p], aqq = H[q * m + q];
        H[p * m + p] = app - t * hpq;
        H[q * m + q] = aqq + t * hpq;
        H[p * m + q] = H[q * m + p] = 0.0;
        for (int k = 0; k < m; ++k) if (k != p && k != q) {
          const double hkp = H[k * m + p], hkq = H[k * m + q];
          H[k * m + p] = H[p * m + k] = c * hkp - s * hkq;
          H[k * m + q] = H[q * m + k] = s * hkp + c * hkq;
        }
        for (int k = 0; k < m; ++k) {
          const double ekp = E[k * m + p], ekq = E[k * m + q];
          E[k * m + p] = c * ekp - s * ekq;
          E[k * m + q] = s * ekp + c * ekq;
        }
      }
    }
  }
  int imin = 0;
  for (int i = 1; i < m; ++i)
    if (H[i * m + i] < H[imin * m + imin]) imin = i;
  eval = H[imin * m + imin];
  Vec x(m);
  for (int i = 0; i < m; ++i) x[i] = E[i * m + imin];
  return x;
}

// With U orthonormal, construct the compression of L to C=U V^T and
// globally minimize over V.
static double optimize_right(const Vec& U, Vec& V, int d, int n) {
  const int D = ipow(d, n), m = 2 * D;
  Vec H(m * m, 0.0), basis(D * D, 0.0);
  for (int q = 0; q < m; ++q) {
    std::fill(basis.begin(), basis.end(), 0.0);
    const int rq = q / D, bq = q % D;
    for (int a = 0; a < D; ++a) basis[a * D + bq] = U[a * 2 + rq];
    Vec z = apply_L(basis, d, n);
    for (int p = 0; p < m; ++p) {
      const int rp = p / D, bp = p % D;
      double h = 0.0;
      for (int a = 0; a < D; ++a) h += U[a * 2 + rp] * z[a * D + bp];
      H[p * m + q] = h;
    }
  }
  double ev;
  Vec x = least_eigenvector(H, m, ev);
  for (int r = 0; r < 2; ++r)
    for (int b = 0; b < D; ++b)
      V[b * 2 + r] = x[r * D + b];
  return ev;
}

// With V orthonormal, globally minimize over U.
static double optimize_left(Vec& U, const Vec& V, int d, int n) {
  const int D = ipow(d, n), m = 2 * D;
  Vec H(m * m, 0.0), basis(D * D, 0.0);
  for (int q = 0; q < m; ++q) {
    std::fill(basis.begin(), basis.end(), 0.0);
    const int rq = q / D, aq = q % D;
    for (int b = 0; b < D; ++b) basis[aq * D + b] = V[b * 2 + rq];
    Vec z = apply_L(basis, d, n);
    for (int p = 0; p < m; ++p) {
      const int rp = p / D, ap = p % D;
      double h = 0.0;
      for (int b = 0; b < D; ++b) h += V[b * 2 + rp] * z[ap * D + b];
      H[p * m + q] = h;
    }
  }
  double ev;
  Vec x = least_eigenvector(H, m, ev);
  for (int r = 0; r < 2; ++r)
    for (int a = 0; a < D; ++a)
      U[a * 2 + r] = x[r * D + a];
  return ev;
}

int main(int argc, char** argv) {
  if (argc != 7) {
    std::cerr << "usage: " << argv[0]
              << " d n alpha restarts alternations seed\n";
    return 2;
  }
  const int d = std::stoi(argv[1]), n = std::stoi(argv[2]);
  g_alpha = std::stod(argv[3]);
  const int restarts = std::stoi(argv[4]), alternations = std::stoi(argv[5]);
  const uint64_t seed = std::stoull(argv[6]);
  const int D = ipow(d, n);
  std::mt19937_64 rng(seed);
  std::normal_distribution<double> normal;
  double global_best = std::numeric_limits<double>::infinity();
  Vec bestU, bestV;
  std::cout << std::setprecision(17);
  for (int restart = 0; restart < restarts; ++restart) {
    Vec U(D * 2), V(D * 2);
    for (double& z : U) z = normal(rng);
    for (double& z : V) z = normal(rng);
    if (!orthonormalize_left(U, V, D)) continue;
    double old = quotient(U, V, d, n);
    for (int k = 0; k < alternations; ++k) {
      optimize_right(U, V, d, n);
      if (!orthonormalize_right(U, V, D)) break;
      optimize_left(U, V, d, n);
      if (!orthonormalize_left(U, V, D)) break;
      const double now = quotient(U, V, d, n);
      if (std::abs(now - old) < 1e-11) break;
      old = now;
    }
    const double q = quotient(U, V, d, n);
    if (q < global_best) {
      global_best = q;
      bestU = U; bestV = V;
    }
    std::cout << "restart " << restart << " q " << q
              << " global " << global_best << "\n";
  }
  std::cout << "BEST " << global_best << "\n";
  return 0;
}
