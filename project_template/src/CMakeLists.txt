# add_subdirectory(lib)

# add_subdirectory(app1)
# add_subdirectory(app2)

add_executable(main main.cpp)
target_link_libraries(main PRIVATE fmt::fmt)