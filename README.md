# acs_doctor_matching
ACS project for the clinic of saint Paraskeva. The aim of the project is to create an algorithm for stable pairing of doctors and cabinets.

## Problem Statement

Scheduling doctors efficiently is a complex task involving:
- Doctor availability, specialties & preferences
- Different locations around the city
- Cabinet specialties

## Theoretical part
All our work, ideas, conversations with mentor, future plans you can find in the report of our work available in **aks2025.pdf**

## Algorithms

- Gale-Shapley algo - Python and C++ implementation (/gale_shapley_algo)
- Basic SPA - Python (/basic_algo)
- Flow-based algorithm - Python and C++ implementation (/new_algo and /cpp_impl)

## Metrics for preferences including algorithms

Each doctor is evaluated using a happiness score:  
- Preferences ranked at the top = more "satisfaction"
- Weighted scoring (e.g., 12*2 for best, 1 for others)
  More detailed in report 
