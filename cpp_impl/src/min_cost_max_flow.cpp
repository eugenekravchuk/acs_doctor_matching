#include "min_cost_max_flow.h"

#include <random>
#include <algorithm>
#include <map>

double random_epsilon() {
    static std::default_random_engine gen(std::random_device{}());
    static std::uniform_real_distribution<double> dist(0.0, EPSILON);
    return dist(gen);
}

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
) {
    std::unordered_map<std::string, double> dist;
    for (const auto& [u, _] : graph)
        dist[u] = std::numeric_limits<double>::infinity();
    dist[source] = 0.0;

    for (size_t i = 0; i < graph.size() - 1; ++i) {
        for (const auto& [u, edges] : graph) {
            for (const auto& edge : edges) {
                if (edge.capacity <= edge.flow) continue;

                double cost = 0.0;
                if (!(necessary_shifts.count(edge.from) && necessary_shifts.at(edge.from).count(edge.to)) &&
                    costs.count(edge.from) && costs.at(edge.from).count(edge.to)) {

                    cost = costs.at(edge.from).at(edge.to);
                    double doctor_pen = doctor_penalty.count(edge.from) ? doctor_penalty.at(edge.from) : 0;
                    double cab_pen = cabinet_penalty.count(edge.to) ? cabinet_penalty.at(edge.to) : 0;
                    cost += (doctor_pen + cab_pen) * PENALTY_MULTIPLIER;
                }

                cost += random_epsilon();

                if (dist[u] + cost < dist[edge.to]) {
                    dist[edge.to] = dist[u] + cost;
                    parent[edge.to] = u;
                }
            }
        }
    }

    if (dist[sink] == std::numeric_limits<double>::infinity())
        return false;

    path.clear();
    std::string curr = sink;
    while (curr != source) {
        path.push_back(curr);
        curr = parent[curr];
    }
    path.push_back(source);
    std::reverse(path.begin(), path.end());
    return true;
}

std::tuple<int, double, Graph> min_cost_max_flow(
    Graph& G,
    CostMap& costs,
    std::unordered_map<std::string, int> doctor_penalty,
    std::unordered_map<std::string, int> cabinet_penalty,
    const std::unordered_map<std::string, std::unordered_map<std::string, bool>>& necessary_shifts,
    const std::string& source,
    const std::string& sink
) {
    Graph residual;
    for (const auto& [u, edges] : G) {
        for (const auto& e : edges) {
            residual[u].push_back(e);
            residual[e.to].push_back({u, 0, -e.cost, 0, e.to});
        }
    }

    int max_flow = 0;
    double min_cost = 0;

    std::map<std::pair<std::string, std::string>, int> flow_map;

    std::vector<std::string> path;
    std::unordered_map<std::string, std::string> parent;

    while (bellman_ford(residual, costs, doctor_penalty, cabinet_penalty, necessary_shifts, source, sink, path, parent)) {
        int path_flow = std::numeric_limits<int>::max();

        for (size_t i = 0; i + 1 < path.size(); ++i) {
            const std::string& u = path[i];
            const std::string& v = path[i + 1];
            for (auto& e : residual[u]) {
                if (e.to == v && e.capacity > e.flow) {
                    path_flow = std::min(path_flow, e.capacity - e.flow);
                    break;
                }
            }
        }

        for (size_t i = 0; i + 1 < path.size(); ++i) {
            const std::string& u = path[i];
            const std::string& v = path[i + 1];
            for (auto& e : residual[u]) {
                if (e.to == v) {
                    e.flow += path_flow;
                    break;
                }
            }
            for (auto& e : residual[v]) {
                if (e.to == u) {
                    e.flow -= path_flow;
                    break;
                }
            }

            flow_map[{u, v}] += path_flow;

            if (costs.count(u) && costs.at(u).count(v)) {
                min_cost += costs.at(u).at(v) * path_flow;
            }

            doctor_penalty[u]++;
            cabinet_penalty[v]++;
        }

        max_flow += path_flow;
    }

    Graph flow_dict;
    for (const auto& entry : flow_map) {
        const std::string& from = entry.first.first;
        const std::string& to = entry.first.second;
        int f = entry.second;

        if (f > 0) {
            flow_dict[from].push_back({to, f, 0, f, from});
        }
    }

    return {max_flow, min_cost, flow_dict};
}

