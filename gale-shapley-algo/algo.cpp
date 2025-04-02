#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <unordered_map>
#include <algorithm>

struct Doctor {
    std::string name;
    int needed_shifts;
    std::vector<std::string> preferences;
    std::vector<std::string> specialties;
};

struct Cabinet {
    std::string room;
    std::vector<std::string> specialties;
};

struct pair_hash {
    template <class T1, class T2>
    std::size_t operator ()(const std::pair<T1, T2>& p) const {
        auto h1 = std::hash<T1>{}(p.first);
        auto h2 = std::hash<T2>{}(p.second);
        return h1 ^ (h2 << 1);
    }
};

std::unordered_map<std::string, Doctor> doctors;
std::unordered_map<std::string, Cabinet> cabinets;
std::unordered_map<std::pair<std::string, std::string>, std::string, pair_hash> assignments;
std::unordered_map<std::string, int> doctor_assigned_counts;
std::unordered_map<std::string, int> doctor_current_index;

void loadDoctorPrefs(const std::string& filename) {
    std::ifstream file(filename);
    std::string line;
    std::getline(file, line);
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string name, shifts, token;
        std::getline(ss, name, ',');
        std::getline(ss, shifts, ',');
        Doctor doc{name, std::stoi(shifts)};
        while (std::getline(ss, token, ',')) {
            doc.preferences.push_back(token);
        }
        doctors[name] = doc;
        doctor_current_index[name] = 0;
    }
}

void loadDoctorSpecialties(const std::string& filename) {
    std::ifstream file(filename);
    std::string line;
    std::getline(file, line);
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string name, spec;
        std::getline(ss, name, ',');
        std::getline(ss, spec);
        doctors[name].specialties.push_back(spec);
    }
}

void loadCabinetInfo(const std::string& filename) {
    std::ifstream file(filename);
    std::string line;
    std::getline(file, line);
    int id = 1;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string room, spec;
        std::getline(ss, room, ',');
        std::getline(ss, spec);
        cabinets[std::to_string(id++)] = {room, {spec}};
    }
}

void assignShifts() {
    bool progress = true;
    while (progress) {
        progress = false;
        for (auto& [doctorName, doc] : doctors) {
            if (doctor_assigned_counts[doctorName] >= doc.needed_shifts)
                continue;
            if (doctor_current_index[doctorName] >= doc.preferences.size())
                continue;

            std::string pref = doc.preferences[doctor_current_index[doctorName]++];

            for (auto& [cabId, cab] : cabinets) {
                if (assignments.find({cabId, pref}) == assignments.end() &&
                    std::any_of(cab.specialties.begin(), cab.specialties.end(), [&](const std::string& s) {
                        return std::find(doc.specialties.begin(), doc.specialties.end(), s) != doc.specialties.end();
                    })) {
                    assignments[{cabId, pref}] = doctorName;
                    doctor_assigned_counts[doctorName]++;
                    progress = true;
                    break;
                }
            }
        }
    }

    for (auto& [slot, assigned] : assignments) {
        if (assigned.empty()) {
            std::string cabId = slot.first;
            std::string shiftCode = slot.second;
            for (auto& [doctorName, doc] : doctors) {
                if (doctor_assigned_counts[doctorName] >= doc.needed_shifts)
                    continue;
                if (std::any_of(cabinets[cabId].specialties.begin(), cabinets[cabId].specialties.end(), [&](const std::string& s) {
                    return std::find(doc.specialties.begin(), doc.specialties.end(), s) != doc.specialties.end();
                })) {
                    assignments[slot] = doctorName;
                    doctor_assigned_counts[doctorName]++;
                    break;
                }
            }
        }
    }
}

void outputSchedule(const std::string& filename) {
    std::ofstream out(filename);
    std::map<std::string, std::vector<std::pair<std::string, std::string>>> schedule;
    for (auto& [slot, doctor] : assignments) {
        schedule[cabinets[slot.first].room].emplace_back(slot.second, doctor);
    }
    for (auto& [room, shifts] : schedule) {
        out << "Cabinet: " << room << "\n";
        std::sort(shifts.begin(), shifts.end());
        for (auto& [shift, doctor] : shifts) {
            out << "  Shift: " << shift << " -> Doctor: " << doctor << "\n";
        }
        out << "\n";
    }
}

int main() {
    loadDoctorPrefs("./data/doctors_schedule_160.csv");
    loadDoctorSpecialties("./data/doctors_160.csv");
    loadCabinetInfo("./data/rooms_80.csv");
    assignShifts();
    outputSchedule("schedule_output.txt");
    std::cout << "Schedule written to schedule_output.txt\n";
    return 0;
}
