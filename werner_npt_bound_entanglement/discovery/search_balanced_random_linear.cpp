// Discovery-only exploration of the complement-balanced manifold.
//
// This includes the existing contraction/search implementation and adds a
// random linear functional of the code projection.  Its purpose is to move
// along the large zero set of the odd-sector balance loss rather than merely
// project a random frame to the nearest feasible point.

#define main search_n4_complex_sector_target_original_main
#include "search_n4_complex_sector_target.cpp"
#undef main

namespace {

double linear_value(const Search& search, const Vec& frame,
                    const std::array<double, kD>& diagonal) {
  const Vec projection = search.projection(frame);
  double value = 0.0;
  for (int i = 0; i < kD; ++i)
    value += diagonal[i] * std::real(projection[i * kD + i]);
  return value;
}

Evaluation descend_random_linear(
    const Search& search, Vec& frame,
    const std::array<double, kD>& diagonal, double penalty,
    double linear_weight, int iterations, double initial_step) {
  Evaluation best = search.evaluate(frame, 0.0, nullptr);
  Vec best_frame = frame;
  double best_objective =
      penalty * best.target_loss +
      linear_weight * linear_value(search, frame, diagonal);
  double step = initial_step;

  for (int iteration = 0; iteration < iterations; ++iteration) {
    Vec gradient;
    const Evaluation current =
        search.evaluate(frame, penalty, &gradient);
    const double current_objective =
        penalty * current.target_loss +
        linear_weight * linear_value(search, frame, diagonal);

    for (int i = 0; i < kD; ++i)
      for (int logical = 0; logical < 2; ++logical)
        gradient[2 * i + logical] +=
            2.0 * linear_weight * diagonal[i] *
            frame[2 * i + logical];
    search.project_tangent(frame, gradient);
    const double gradient_squared = norm_squared(gradient);
    if (gradient_squared < 1e-24) break;

    bool accepted = false;
    double trial_step = step;
    for (int backtrack = 0; backtrack < 35; ++backtrack) {
      Vec trial = frame;
      for (int k = 0; k < 2 * kD; ++k)
        trial[k] -= trial_step * gradient[k];
      search.orthonormalize(trial);
      const Evaluation trial_value =
          search.evaluate(trial, 0.0, nullptr);
      const double trial_objective =
          penalty * trial_value.target_loss +
          linear_weight * linear_value(search, trial, diagonal);
      if (trial_objective <=
          current_objective -
              1e-4 * trial_step * gradient_squared) {
        frame.swap(trial);
        step = std::min(initial_step, 1.2 * trial_step);
        accepted = true;
        if (trial_objective < best_objective) {
          best_objective = trial_objective;
          best = trial_value;
          best_frame = frame;
        }
        break;
      }
      trial_step *= 0.5;
    }
    if (!accepted) break;
  }
  frame = best_frame;
  return best;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 5) {
    std::cerr << "usage: search_balanced_random_linear"
              << " input output seed rounds\n";
    return 2;
  }
  const std::string input = argv[1];
  const std::string output = argv[2];
  const std::uint64_t seed = std::stoull(argv[3]);
  const int rounds = std::stoi(argv[4]);

  Search search(seed, 3, false, false, false, true, true);
  Vec frame = search.load(input);
  search.orthonormalize(frame);

  std::array<double, kD> diagonal{};
  for (double& value : diagonal) value = search.normal(search.rng);
  double mean = 0.0;
  for (double value : diagonal) mean += value / kD;
  double norm = 0.0;
  for (double& value : diagonal) {
    value -= mean;
    norm += value * value;
  }
  norm = std::sqrt(norm);
  for (double& value : diagonal) value /= norm;

  for (int round = 0; round < rounds; ++round) {
    const double weight = std::pow(0.35, round);
    const std::array<double, 5> penalties =
        {1e4, 1e5, 1e6, 1e7, 1e8};
    for (double penalty : penalties)
      descend_random_linear(search, frame, diagonal, penalty, weight,
                            500, 0.05);
    const Evaluation value = search.evaluate(frame, 0.0, nullptr);
    std::cout << "round " << round << " weight "
              << std::setprecision(17) << weight
              << " loss " << value.target_loss
              << " linear " << linear_value(search, frame, diagonal)
              << "\n";
  }

  // Remove the final finite-penalty displacement without choosing a new
  // objective along the balanced zero set.
  search.descend(frame, 1e8, 3000, 0.03);
  const Evaluation value = search.evaluate(frame, 0.0, nullptr);
  search.print(frame, value);
  search.save(frame, output);
  return 0;
}
