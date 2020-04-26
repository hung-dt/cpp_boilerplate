add_executable(imgui_test imgui_test.cpp)
target_link_libraries(imgui_test PRIVATE ImGui-SFML::ImGui-SFML)

add_executable(spdlog_test spdlog_test.cpp)
target_link_libraries(spdlog_test PRIVATE spdlog::spdlog)

add_executable(docopt_test docopt_test.cpp)
target_link_libraries(docopt_test PRIVATE docopt)

add_executable(catch2_test catch2_test.cpp)
target_link_libraries(catch2_test PRIVATE Catch2::Catch2)

add_executable(doctest_test doctest_test.cpp)
target_link_libraries(doctest_test PRIVATE doctest::doctest)

add_executable(cxxopts_test cxxopts_test.cpp)
target_link_libraries(cxxopts_test PRIVATE cxxopts::cxxopts)

add_executable(sdl_test sdl_test.cpp)
target_include_directories(sdl_test PRIVATE ${SDL2_INCLUDE_DIRS})
target_link_libraries(sdl_test PRIVATE ${SDL2_LIBRARIES})

add_executable(sfml_test sfml_test.cpp)
target_link_libraries(sfml_test PRIVATE sfml-graphics sfml-audio)
