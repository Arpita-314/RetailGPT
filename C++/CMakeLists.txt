cmake_minimum_required(VERSION 3.10)
project(FluidGame)

set(CMAKE_TOOLCHAIN_FILE "C:/vcpkg/scripts/buildsystems/vcpkg.cmake")
find_package(SFML COMPONENTS system window graphics REQUIRED)

add_executable(FluidGame game.cpp)
target_link_libraries(FluidGame PRIVATE sfml-system sfml-window sfml-graphics)

file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/build)
execute_process(COMMAND ${CMAKE_COMMAND} -E chdir ${CMAKE_CURRENT_BINARY_DIR}/build ${CMAKE_COMMAND} ..)
execute_process(COMMAND ${CMAKE_COMMAND} --build . WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/build)