cmake_minimum_required(VERSION 3.15)
project(ScheduleGenerator)

find_package(Threads REQUIRED)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(
        include
        ${CMAKE_SOURCE_DIR}
)

add_executable(schedule_gen
        main.cpp
        src/schedule_generator.cpp
        src/min_cost_max_flow.cpp
)

target_link_libraries(schedule_gen PRIVATE Threads::Threads)
