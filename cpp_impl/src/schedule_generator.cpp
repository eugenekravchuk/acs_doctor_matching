#include "min_cost_max_flow.h"
#include "schedule_generator.h"
#include <fstream>
#include <iostream>
#include <json.hpp>
#include <csv.h>
#include <map>
#include <set>
#include <sstream>
#include <iomanip>
#include <algorithm>

using namespace std;
using json = nlohmann::json;

vector<string> split(const string& s, char delimiter) {
    vector<string> tokens;
    size_t start = 0, end = 0;
    while ((end = s.find(delimiter, start)) != string::npos) {
        tokens.push_back(s.substr(start, end - start));
        start = end + 1;
    }
    tokens.push_back(s.substr(start));
    return tokens;
}

string join(const string& a, const string& b, const string& c, char sep = '|') {
    return a + sep + b + sep + c;
}

void load_inputs(const string& csv_path, const string& json_path,
                 vector<DoctorRow>& doctors,
                 map<string, map<string, vector<string>>>& loc_spec_cabs) {

    io::CSVReader<7, io::trim_chars<' '>, io::double_quote_escape<',','"'>, io::throw_on_overflow> in(csv_path);
    in.read_header(io::ignore_extra_column,
        "Doctor", "Cabinets", "MinShifts", "MaxShifts", "ForbiddenShifts", "RequiredShifts", "Specialization");

    string doctor, cabinets, min_s, max_s, forb, req, spec;
    while (in.read_row(doctor, cabinets, min_s, max_s, forb, req, spec)) {
        DoctorRow d;
        d.name = doctor;
        d.locs = split(cabinets, ',');
        d.specs = split(spec, ',');
        if (!min_s.empty()) d.min_shifts = stoi(min_s) / 4;
        if (!max_s.empty()) d.max_shifts = stoi(max_s) / 4;
        if (!forb.empty()) {
            for (const auto& s : split(forb, ','))
                d.forbidden.insert(s);
        }
        if (!req.empty()) {
            for (const auto& s : split(req, ','))
                d.obligatory.insert(s);
        }
        doctors.push_back(d);
    }

    ifstream jfile(json_path);
    if (!jfile) {
        cerr << "Failed to open JSON file: " << json_path << endl;
        return;
    }
    json j;
    jfile >> j;
    for (const auto& item : j) {
        string loc = item["location"];
        string spec = item["specialization"];
        vector<string> rooms;
        if (item["room"].is_string()) {
            rooms = split(item["room"].get<string>(), ',');
        } else if (item["room"].is_array()) {
            rooms = item["room"].get<vector<string>>();
        } else {
            cerr << "Invalid 'room' field in JSON." << endl;
            continue;
        }
        for (auto& r : rooms) {
            while (!r.empty() && r.front() == ' ') r.erase(r.begin());
            while (!r.empty() && r.back() == ' ') r.pop_back();
        }
        loc_spec_cabs[loc][spec] = rooms;
    }

    cout << "Loaded " << doctors.size() << " doctors and " << loc_spec_cabs.size() << " locations.\n";
}

void generate_week_schedule(int week, const vector<DoctorRow>& doctors,
                            const map<string, map<string, vector<string>>>& loc_spec_cabs,
                            const string& out_path) {
    Graph G;
    string source = "S", sink = "T";
    G[source] = vector<Edge>{};
    G[sink] = vector<Edge>{};

    CostMap cost;
    unordered_map<string, int> dpenalty, cpenalty;
    unordered_map<string, unordered_map<string, bool>> necessary;
    map<string, map<string, map<string, string>>> assignment;

    vector<string> days = {"1", "2", "3", "4", "5", "6", "7"};
    vector<string> shifts = {"1", "2"};
    vector<string> all_shifts;
    for (const auto& d : days)
        for (const auto& s : shifts)
            all_shifts.push_back(d + "." + s);

    for (const auto& doc : doctors) {
        string doc_node = "D|" + doc.name;
        if (doc.min_shifts > 0) {
            string pre = "PRE|" + doc.name;
            G[source].push_back(Edge{pre, doc.min_shifts, 0, 0, source});
            G[pre].push_back(Edge{doc_node, doc.min_shifts, 0, 0, pre});
        }
        G[source].push_back(Edge{doc_node, doc.max_shifts - doc.min_shifts, 0, 0, source});

        for (const auto& loc : doc.locs) {
            for (const auto& spec : doc.specs) {
                if (loc_spec_cabs.count(loc) && loc_spec_cabs.at(loc).count(spec)) {
                    for (const auto& cab : loc_spec_cabs.at(loc).at(spec)) {
                        string lc = loc + "|" + cab;
                        cpenalty[lc] = 0;

                        for (const auto& shift : all_shifts) {
                            if (doc.forbidden.count(shift)) continue;

                            string d_shift = doc.name + "|" + shift;
                            string full = loc + "|" + cab + "|" + shift;

                            G[doc_node].push_back(Edge{d_shift, 1, 0, 0, doc_node});
                            G[d_shift].push_back(Edge{full, 1, 0, 0, d_shift});
                            G[full].push_back(Edge{sink, 1, 0, 0, full});

                            cost[doc_node][d_shift] = 1.0;
                            cost[d_shift][full] = 1.0;

                            if (doc.obligatory.count(shift)) {
                                necessary[d_shift][full] = true;
                                cost[d_shift][full] = 0.0;
                            }
                        }
                    }
                }
            }
        }
    }

    size_t edge_count = 0;
    for (const auto& [from, vec] : G) edge_count += vec.size();
    cout << "Graph has " << G.size() << " nodes and " << edge_count << " edges.\n";

    auto [flow, total_cost, flow_dict] = min_cost_max_flow(G, cost, dpenalty, cpenalty, necessary, source, sink);
    cout << "Flow: " << flow << ", Cost: " << total_cost << endl;

    map<string, map<string, map<string, string>>> schedule;

    for (const auto& [from, edges] : flow_dict) {
        for (const auto& edge : edges) {
            cout << "one";
            if (edge.flow > 0) {
                cout << "two";
                auto to_parts = split(edge.to, '|');
                auto from_parts = split(edge.from, '|');

                if (to_parts.size() == 3 && from_parts.size() == 2) {
                    string loc = to_parts[0];
                    string cab = to_parts[1];
                    string shift = to_parts[2];
                    string doctor = from_parts[0];

                    cout << "[ASSIGN] " << doctor << " -> " << loc << ", " << cab << ", " << shift << endl;
                    schedule[loc][cab][shift] = doctor;
                }
            }
        }
    }



    ofstream out(out_path);
    if (!out.is_open()) {
        cerr << "Failed to write to: " << out_path << endl;
        return;
    }

    vector<string> loc_order;
    for (const auto& [loc, _] : schedule) loc_order.push_back(loc);
    sort(loc_order.begin(), loc_order.end());

    for (const auto& loc : loc_order) {
        out << "Локація: " << loc << "\n========================================\n";
        vector<string> cab_order;
        for (const auto& [cab, _] : schedule[loc]) cab_order.push_back(cab);
        sort(cab_order.begin(), cab_order.end());
        for (const auto& cab : cab_order) {
            out << "Кабінет: " << cab << "\n------------------------------\n";
            for (int d = 1; d <= 7; ++d) {
                for (int s = 1; s <= 2; ++s) {
                    string shift = to_string(d) + "." + to_string(s);
                    out << d << "." << s << " - " << (schedule[loc][cab].count(shift) ? schedule[loc][cab][shift] : "Немає лікаря") << "\n";
                }
            }
            out << "\n";
        }
        out << "\n";
    }
}
