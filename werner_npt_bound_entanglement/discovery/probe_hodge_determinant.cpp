// Discovery probe for the qutrit fourfold Hodge determinant invariant.
// Floating point only; no theorem is inferred from this file.

#include <array>
#include <cmath>
#include <complex>
#include <cstdint>
#include <iomanip>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

using C = std::complex<double>;

int eps(int k, int a, int b) {
  if (k == a || k == b || a == b) return 0;
  const std::array<int, 3> p{k, a, b};
  int inv = 0;
  for (int i = 0; i < 3; ++i)
    for (int j = i + 1; j < 3; ++j) inv += p[i] > p[j];
  return inv & 1 ? -1 : 1;
}

std::vector<C> apply_hodge(const std::vector<C>& x,
                           const std::vector<int>& ks) {
  const int n = static_cast<int>(ks.size());
  int d = 1;
  for (int i = 0; i < n; ++i) d *= 3;
  std::vector<C> y(d);
  for (int out = 0; out < d; ++out) {
    int z = out;
    std::array<int, 8> oi{};
    for (int i = n - 1; i >= 0; --i) {
      oi[i] = z % 3;
      z /= 3;
    }
    for (int in = 0; in < d; ++in) {
      int w = in;
      std::array<int, 8> ii{};
      int coefficient = 1;
      for (int i = n - 1; i >= 0; --i) {
        ii[i] = w % 3;
        w /= 3;
      }
      for (int i = 0; i < n; ++i)
        coefficient *= eps(ks[i], oi[i], ii[i]);
      if (coefficient) y[out] += static_cast<double>(coefficient) * x[in];
    }
  }
  return y;
}

C bilinear(const std::vector<C>& x, const std::vector<C>& y) {
  C z = 0;
  for (std::size_t i = 0; i < x.size(); ++i) z += x[i] * y[i];
  return z;
}

C bilinear_hodge_sparse(const std::vector<C>& x,
                        const std::vector<int>& ks) {
  C out = 0;
  for (int input = 0; input < static_cast<int>(x.size()); ++input) {
    int z = input;
    int output = 0;
    int place = 1;
    int coefficient = 1;
    for (int i = static_cast<int>(ks.size()) - 1; i >= 0; --i) {
      const int a = z % 3;
      z /= 3;
      int b = -1, sign = 0;
      for (int candidate = 0; candidate < 3; ++candidate) {
        const int value = eps(ks[i], candidate, a);
        if (value) {
          b = candidate;
          sign = value;
          break;
        }
      }
      if (b < 0) {
        coefficient = 0;
        break;
      }
      output += b * place;
      place *= 3;
      coefficient *= sign;
    }
    if (coefficient)
      out += static_cast<double>(coefficient) * x[output] * x[input];
  }
  return out;
}

C inner(const std::vector<C>& x, const std::vector<C>& y) {
  C z = 0;
  for (std::size_t i = 0; i < x.size(); ++i) z += std::conj(x[i]) * y[i];
  return z;
}

void normalize(std::vector<C>& x) {
  const double r = std::sqrt(std::real(inner(x, x)));
  for (C& z : x) z /= r;
}

void project_sector(std::vector<C>& x, int mask);

double sector_mass(const std::vector<C>& u, const std::vector<C>& v,
                   int mask) {
  std::vector<C> omega(6561);
  const double scale = 1.0 / std::sqrt(2.0);
  for (int a = 0; a < 81; ++a)
    for (int b = 0; b < 81; ++b)
      omega[81 * a + b] = scale * (u[a] * v[b] - v[a] * u[b]);
  project_sector(omega, mask);
  return std::real(inner(omega, omega));
}

void probe(int n, std::uint64_t seed, bool repetition) {
  int d = 1;
  for (int i = 0; i < n; ++i) d *= 3;
  std::vector<C> u(d), v(d);
  if (repetition) {
    u.front() = 1;
    v.back() = 1;
  } else {
    std::mt19937_64 rng(seed);
    std::normal_distribution<double> normal;
    for (int i = 0; i < d; ++i) {
      u[i] = C(normal(rng), normal(rng));
      v[i] = C(normal(rng), normal(rng));
    }
    normalize(u);
    const C overlap = inner(u, v);
    for (int i = 0; i < d; ++i) v[i] -= overlap * u[i];
    normalize(v);
  }

  C determinant_sum = 0;
  double absolute_sum = 0;
  double square_sum = 0;
  double frobenius_sum = 0;
  int count = 1;
  for (int i = 0; i < n; ++i) count *= 3;
  for (int code = 0; code < count; ++code) {
    int z = code;
    std::vector<int> ks(n);
    for (int i = n - 1; i >= 0; --i) {
      ks[i] = z % 3;
      z /= 3;
    }
    const auto au = apply_hodge(u, ks);
    const auto av = apply_hodge(v, ks);
    const C s00 = bilinear(u, au);
    const C s01 = bilinear(u, av);
    const C s10 = bilinear(v, au);
    const C s11 = bilinear(v, av);
    const C det = s00 * s11 - s01 * s10;
    determinant_sum += det;
    absolute_sum += std::abs(det);
    square_sum += std::norm(det);
    frobenius_sum += std::norm(s00) + std::norm(s01)
                     + std::norm(s10) + std::norm(s11);
  }
  std::cout << "n=" << n << " rep=" << repetition
            << " detsum=" << determinant_sum
            << " abs=" << absolute_sum
            << " sq=" << square_sum
            << " frob=" << frobenius_sum << "\n";
}

void probe_file(const char* path) {
  std::ifstream in(path);
  std::vector<C> u(81), v(81);
  int i;
  double ur, ui, vr, vi;
  while (in >> i >> ur >> ui >> vr >> vi) {
    u[i] = C(ur, ui);
    v[i] = C(vr, vi);
  }
  C overlap = inner(u, v);
  normalize(u);
  for (int j = 0; j < 81; ++j) v[j] -= overlap * u[j];
  normalize(v);

  C determinant_sum = 0;
  double absolute_sum = 0, square_sum = 0, frobenius_sum = 0;
  double filtered_gram_determinant_sum = 0;
  std::array<C, 81> determinant_tensor{};
  std::array<std::array<C, 81>, 8> sector_determinant_tensor{};
  std::array<int, 8> odd_masks{1, 2, 4, 7, 8, 11, 13, 14};
  std::array<std::vector<C>, 8> sector_omega;
  {
    std::vector<C> omega(6561);
    const double scale = 1.0 / std::sqrt(2.0);
    for (int a = 0; a < 81; ++a)
      for (int b = 0; b < 81; ++b)
        omega[81 * a + b] =
            scale * (u[a] * v[b] - v[a] * u[b]);
    for (int r = 0; r < 8; ++r) {
      sector_omega[r] = omega;
      project_sector(sector_omega[r], odd_masks[r]);
    }
  }
  for (int code = 0; code < 81; ++code) {
    int z = code;
    std::vector<int> ks(4);
    for (int j = 3; j >= 0; --j) {
      ks[j] = z % 3;
      z /= 3;
    }
    const auto au = apply_hodge(u, ks);
    const auto av = apply_hodge(v, ks);
    const C s00 = bilinear(u, au), s01 = bilinear(u, av);
    const C s10 = bilinear(v, au), s11 = bilinear(v, av);
    const C det = s00 * s11 - s01 * s10;
    determinant_tensor[code] = det;
    determinant_sum += det;
    absolute_sum += std::abs(det);
    square_sum += std::norm(det);
    frobenius_sum += std::norm(s00) + std::norm(s01)
                     + std::norm(s10) + std::norm(s11);

    C r00 = 0, r01 = 0, r11 = 0;
    for (int basis = 0; basis < 81; ++basis) {
      int w = basis;
      bool retained = true;
      for (int j = 3; j >= 0; --j) {
        const int digit = w % 3;
        w /= 3;
        if (digit == ks[j]) retained = false;
      }
      if (!retained) continue;
      r00 += std::conj(u[basis]) * u[basis];
      r01 += std::conj(u[basis]) * v[basis];
      r11 += std::conj(v[basis]) * v[basis];
    }
    filtered_gram_determinant_sum +=
        std::real(r00 * r11 - r01 * std::conj(r01));

    for (int r = 0; r < 8; ++r) {
      sector_determinant_tensor[r][code] =
          bilinear_hodge_sparse(
              sector_omega[r],
              {ks[0], ks[1], ks[2], ks[3],
               ks[0], ks[1], ks[2], ks[3]});
    }
  }
  double complement_geometric_sum = 0;
  for (int mask : {1, 2, 4, 7}) {
    const double left = sector_mass(u, v, mask);
    const double right = sector_mass(u, v, 15 ^ mask);
    complement_geometric_sum += 2.0 * std::sqrt(left * right);
  }
  double phase_rank_one_residual = 0;
  for (int site = 0; site < 4; ++site) {
    int stride = 1;
    for (int j = site + 1; j < 4; ++j) stride *= 3;
    C reference_ratio[3] = {1.0, 0.0, 0.0};
    bool have_reference[3] = {true, false, false};
    for (int base = 0; base < 81; ++base) {
      const int digit = (base / stride) % 3;
      if (digit != 0) continue;
      const C d0 = determinant_tensor[base];
      if (std::abs(d0) < 1e-8) continue;
      for (int digit2 = 1; digit2 < 3; ++digit2) {
        const C d1 = determinant_tensor[base + digit2 * stride];
        if (std::abs(d1) < 1e-8) continue;
        const C ratio =
            (d1 / std::abs(d1)) / (d0 / std::abs(d0));
        if (!have_reference[digit2]) {
          reference_ratio[digit2] = ratio;
          have_reference[digit2] = true;
        } else {
          phase_rank_one_residual =
              std::max(phase_rank_one_residual,
                       std::min(std::abs(ratio - reference_ratio[digit2]),
                                std::abs(ratio + reference_ratio[digit2])));
        }
      }
    }
  }
  std::cout << "file=" << path << " detsum=" << determinant_sum
            << " abs=" << absolute_sum << " sq=" << square_sum
            << " frob=" << frobenius_sum
            << " gramdet=" << filtered_gram_determinant_sum
            << " oddpair=" << complement_geometric_sum
            << " phase-rank1-resid=" << phase_rank_one_residual << "\n";
  for (int r = 0; r < 8; ++r) {
    double l1 = 0, l2 = 0;
    C sum = 0;
    for (const C value : sector_determinant_tensor[r]) {
      l1 += std::abs(value);
      l2 += std::norm(value);
      sum += value;
    }
    std::cout << "  sector=" << odd_masks[r]
              << " mass=" << std::real(inner(sector_omega[r],
                                               sector_omega[r]))
              << " l1=" << l1 << " l2=" << l2
              << " sum=" << sum << "\n";
  }
  for (int r = 0; r < 4; ++r) {
    double l1 = 0;
    for (int code = 0; code < 81; ++code)
      l1 += std::abs(sector_determinant_tensor[r][code]
                     + sector_determinant_tensor[7 - r][code]);
    std::cout << "  complementary-pair=" << odd_masks[r] << "+"
              << odd_masks[7 - r] << " l1=" << l1 << "\n";
  }
}

int swapped_index(int pair_index, int site) {
  int left = pair_index / 81, right = pair_index % 81;
  int stride = 1;
  for (int i = 0; i < 3 - site; ++i) stride *= 3;
  const int a = (left / stride) % 3;
  const int b = (right / stride) % 3;
  left += (b - a) * stride;
  right += (a - b) * stride;
  return 81 * left + right;
}

void project_sector(std::vector<C>& x, int mask) {
  for (int site = 0; site < 4; ++site) {
    std::vector<C> y(x.size());
    const double sign = (mask >> site) & 1 ? -1.0 : 1.0;
    for (int i = 0; i < 6561; ++i)
      y[i] = 0.5 * (x[i] + sign * x[swapped_index(i, site)]);
    x.swap(y);
  }
}

void probe_uniform_odd(std::uint64_t seed) {
  std::mt19937_64 rng(seed);
  std::normal_distribution<double> normal;
  std::vector<C> omega(6561);
  for (int mask = 1; mask < 16; mask += 2) {
    std::vector<C> x(6561);
    for (C& z : x) z = C(normal(rng), normal(rng));
    project_sector(x, mask);
    normalize(x);
    for (int i = 0; i < 6561; ++i) omega[i] += x[i] / std::sqrt(8.0);
  }
  double absolute_sum = 0;
  C determinant_sum = 0;
  for (int code = 0; code < 81; ++code) {
    int z = code;
    std::array<int, 4> ks{};
    for (int j = 3; j >= 0; --j) {
      ks[j] = z % 3;
      z /= 3;
    }
    C value = 0;
    for (int pair = 0; pair < 6561; ++pair) {
      int left = pair / 81, right = pair % 81;
      int out_left = 0, out_right = 0;
      int coefficient = 1;
      for (int site = 0; site < 4; ++site) {
        int stride = 1;
        for (int j = 0; j < 3 - site; ++j) stride *= 3;
        const int a = (left / stride) % 3;
        const int b = (right / stride) % 3;
        int oa = -1, ob = -1, ca = 0, cb = 0;
        for (int candidate = 0; candidate < 3; ++candidate) {
          const int ea = eps(ks[site], candidate, a);
          const int eb = eps(ks[site], candidate, b);
          if (ea) { oa = candidate; ca = ea; }
          if (eb) { ob = candidate; cb = eb; }
        }
        if (oa < 0 || ob < 0) { coefficient = 0; break; }
        out_left += oa * stride;
        out_right += ob * stride;
        coefficient *= ca * cb;
      }
      if (coefficient)
        value += static_cast<double>(coefficient) * omega[pair]
                 * omega[81 * out_left + out_right];
    }
    determinant_sum += value;
    absolute_sum += std::abs(value);
  }
  std::cout << "uniform-odd seed=" << seed
            << " detsum=" << determinant_sum
            << " abs=" << absolute_sum << "\n";
}

int main(int argc, char** argv) {
  std::cout << std::setprecision(14);
  if (argc == 2) {
    probe_file(argv[1]);
    return 0;
  }
  probe_uniform_odd(11);
  probe_uniform_odd(12);
  for (int n = 1; n <= 4; ++n) {
    probe(n, 100 + n, false);
    probe(n, 0, true);
  }
}
