// Batch evaluator for unweighted graph-atlas supports (discovery only).
#define CROSS_SUM_NO_MAIN
#include "search_fast.cpp"

int main() {
  int n;
  std::uint64_t mask;
  long count = 0;
  double best = -std::numeric_limits<double>::infinity();
  double best_product = -std::numeric_limits<double>::infinity();
  std::uint64_t best_mask = 0, best_product_mask = 0;
  double best_bd = 0.0, best_db = 0.0;
  while (std::cin >> n >> mask) {
    Matrix w(n, std::vector<double>(n, 0.0));
    int edge = 0;
    for (int i = 0; i < n; ++i)
      for (int j = i + 1; j < n; ++j, ++edge)
        if (mask & (std::uint64_t(1) << edge)) w[i][j] = w[j][i] = 1.0;
    const double bd = fixation(w, true);
    const double db = fixation(w, false);
    const double excess = bd + db - baseline(n, true) - baseline(n, false);
    const double product_excess =
        bd * db - baseline(n, true) * baseline(n, false);
    ++count;
    if (excess > best) {
      best = excess;
      best_mask = mask;
      best_bd = bd;
      best_db = db;
    }
    if (product_excess > best_product) {
      best_product = product_excess;
      best_product_mask = mask;
    }
  }
  std::cout << "graphs " << count << " best_excess " << std::setprecision(17)
            << best << " Bd " << best_bd << " dB " << best_db << " mask "
            << best_mask << "\n";
  std::cout << "best_product_excess " << best_product << " mask "
            << best_product_mask << "\n";
}
