#include "min_cost_max_flow.h"
#include "schedule_generator.h"
#include <map>
#include <vector>
#include <string>
#include <iostream>

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <input_csv> <locations_json> <output_prefix>\n";
        return 1;
    }

    std::string input_csv = argv[1];
    std::string locs_json = argv[2];
    std::string output_prefix = argv[3];

    std::vector<DoctorRow> doctors;
    std::map<std::string, std::map<std::string, std::vector<std::string>>> loc_spec_cabs;

    load_inputs(input_csv, locs_json, doctors, loc_spec_cabs);

    for (int week = 1; week <= 4; ++week) {
        std::string out_file = output_prefix + "_week_" + std::to_string(week) + ".txt";
        generate_week_schedule(week, doctors, loc_spec_cabs, out_file);
    }

    std::cout << "Schedule created.\n";
    return 0;
}