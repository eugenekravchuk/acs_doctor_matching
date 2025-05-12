#ifndef MIN_COST_MAX_FLOW_H
#define MIN_COST_MAX_FLOW_H

#include <vector>
#include <unordered_map>
#include <string>
#include <tuple>

struct Edge {
    std::string to;
    int capacity;
    int cost;
    int flow;
    std::string from;
};

using Graph = std::unordered_map<std::string, std::vector<Edge>>;
using CostMap = std::unordered_map<std::string, std::unordered_map<std::string, double>>;

constexpr double EPSILON = 1e-5;
constexpr double PENALTY_MULTIPLIER = 1.5;

double random_epsilon();

bool bellman_ford(
    const Graph& graph,
    const CostMap& costs,
    const std::unordered_map<std::string, int>& doctor_penalty,
    const std::unordered_map<std::string, int>& cabinet_penalty,
    const std::unordered_map<std::string, std::unordered_map<std::string, bool>>& necessary_shifts,
    const std::string& source,
    const std::string& sink,
    std::vector<std::string>& path,
    std::unordered_map<std::string, std::string>& parent
);

std::tuple<int, double, Graph> min_cost_max_flow(
    Graph& G,
    CostMap& costs,
    std::unordered_map<std::string, int> doctor_penalty,
    std::unordered_map<std::string, int> cabinet_penalty,
    const std::unordered_map<std::string, std::unordered_map<std::string, bool>>& necessary_shifts,
    const std::string& source,
    const std::string& sink
);

#endif // MIN_COST_MAX_FLOW_H
