#ifndef SCHEDULE_GENERATOR_H
#define SCHEDULE_GENERATOR_H

#include "min_cost_max_flow.h"
#include <string>
#include <vector>
#include <map>
#include <set>

struct DoctorRow {
    std::string name;
    std::vector<std::string> specs;
    std::vector<std::string> locs;
    int min_shifts = 0;
    int max_shifts = 6;
    std::set<std::string> forbidden;
    std::set<std::string> obligatory;
};

void load_inputs(const std::string& csv_path, const std::string& json_path,
                 std::vector<DoctorRow>& doctors,
                 std::map<std::string, std::map<std::string, std::vector<std::string>>>& loc_spec_cabs);

void generate_week_schedule(int week, const std::vector<DoctorRow>& doctors,
                            const std::map<std::string, std::map<std::string, std::vector<std::string>>>& loc_spec_cabs,
                            const std::string& out_path);

#endif // SCHEDULE_GENERATOR_H
