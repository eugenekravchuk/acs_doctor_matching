cmake_minimum_required(VERSION 3.15)
project(DoctorSchedule CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_BUILD_TYPE Release)

add_executable(DoctorSchedule algo.cpp)

find_package(Boost 1.71.0 REQUIRED)
target_include_directories(DoctorSchedule PRIVATE ${Boost_INCLUDE_DIR})
target_link_libraries(DoctorSchedule Boost::boost)