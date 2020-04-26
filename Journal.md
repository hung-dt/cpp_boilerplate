# My Journal

- [CMake Build Types](#cmake-build-types)
- [Notes about install folders](#notes-about-install-folders)
- [Compile SFML-2.5.1 in Linux Mint 19.3](#compile-sfml-251-in-linux-mint-193)
- [Compile and install SFML-2.5.1 in Windows using MinGW](#compile-and-install-sfml-251-in-windows-using-mingw)
- [Compile a sample SFML app with cmake](#compile-a-sample-sfml-app-with-cmake)
- [Compile SFML app manually](#compile-sfml-app-manually)
- [Compile and install imgui-sfml](#compile-and-install-imgui-sfml)
  - [Test imgui-sfml](#test-imgui-sfml)
- [Compile and install spdlog (header only lib)](#compile-and-install-spdlog-header-only-lib)
- [docopt.cpp](#docoptcpp)

## CMake Build Types

C++ flags used for each `CMAKE_BUILD_TYPE`

| CMAKE_BUILD_TYPE | C++ flags (GCC/Clang) |
|------------------|-----------------------|
| Debug            | `-g`                  |
| RelWithDebInfo   | `-O2 -g -DNDEBUG`     |
| Release          | `-O3 -DNDEBUG`        |
| MinSizeRel       | `-Os -DNDEBUG`        |

## Notes about install folders

All libraries can be installed to `prefix-dir` directory which will be populated as below:
```
<prefix-dir>
    bin/          --> binary/dll files
    include/      --> header files
    lib/          --> static libs
        cmake/    --> cmake config files
```
For example, `prefix-dir` is `D:\Dev\opt` then sfml will be installed to:
```
  D:\Dev\opt\
            bin\            --> dll files
            include\SFML    --> header files
            lib\cmake\SFML  --> cmake config files
```

CMake uses `CMAKE_INSTALL_PREFIX` to specify install folder when configuring:
```
cmake -DCMAKE_INSTALL_PREFIX=D:\Dev\opt
```

## Compile SFML-2.5.1 in Linux Mint 19.3
- Download SFML source
- Install dependencies:
```
sudo apt-get install libx11-dev
sudo apt-get install xorg-dev
sudo apt-get install freeglut3-dev
sudo apt-get install libudev-dev
sudo apt-get install libopenal-dev
sudo apt-get install libvorbis-dev
sudo apt-get install libflac-dev
```
- Compile with cmake and install to `$HOME/opt/SFML`:
```
cd <SFML_source_dir>
mkdir build && cd build
cmake .. \
-DCMAKE_BUILD_TYPE=Release \
-DCMAKE_INSTALL_PREFIX=~/opt/SFML-2.5.1 \
-DBUILD_SHARED_LIBS=ON \
-DSFML_BUILD_EXAMPLES=OFF
make -j 4
make install
```
- Add to LD_LIBRARY_PATH:
```
export LD_LIBRARY_PATH=$HOME/opt/SFML-2.5.1/lib:$LD_LIBRARY_PATH
```
- Create an environment variable `SFML_HOME` set to `$HOME/opt/SFML-2.5.1`
```
export SFML_HOME=$HOME/opt/SFML-2.5.1
```
## Compile and install SFML-2.5.1 in Windows using MinGW
- Download SFML source: [https://www.sfml-dev.org/files/SFML-2.5.1-sources.zip]
- Compile with cmake and install to `D:\Dev\sfml-2.5.1`
```
cd <SFML_source_dir>
mkdir build && cd build
cmake .. -G Ninja ^
-DCMAKE_BUILD_TYPE=Release ^
-DCMAKE_INSTALL_PREFIX=D:\Dev\sfml-2.5.1 ^
-DBUILD_SHARED_LIBS=ON ^
-DSFML_BUILD_EXAMPLES=OFF
ninja -j 8
cmake --build . --target install
```
- Add `D:\Dev\sfml-2.5.1\bin` to %PATH% so dynamic libs can be found:
- Create an environment variable `SFML_HOME` set to `D:\Dev\sfml-2.5.1`
```
setx SFML_HOME D:\Dev\sfml-2.5.1
```

## Compile a sample SFML app with cmake
- Create a sample SFML app:
```cpp
#include <SFML/Graphics.hpp>

int main()
{
    sf::RenderWindow window(sf::VideoMode(200, 200), "SFML works!");
    sf::CircleShape shape(100.f);
    shape.setFillColor(sf::Color::Green);

    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
        window.draw(shape);
        window.display();
    }

    return 0;
}
```
- Create a `CMakeLists.txt`:
```
cmake_minimum_required(VERSION 3.10)

project(sfml-app)

list(APPEND CMAKE_MODULE_PATH $ENV{SFML_HOME}/lib/cmake/SFML)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_CXX_FLAGS "${CMAXE_CXX_FLAGS} -Wall -O2")

find_package(SFML COMPONENTS graphics window system)

set(INC_DIRS
    $ENV{SFML_HOME}/include
)

set(SRC
    test.cpp
)

add_executable(test01 ${SRC})
target_include_directories(test01
    PRIVATE ${INC_DIRS}
)
target_link_libraries(test01
    PRIVATE sfml-graphics sfml-window sfml-system
)
```
- Build:
```
mkdir build && cd build
cmake ..
make
./sfml-app
```
- If everything works, you should see this in a new window:

![sfml-app](https://www.sfml-dev.org/tutorials/2.5/images/start-linux-app.png "sfml-app window")

## Compile SFML app manually

If you installed SFML to a non-standard path `$HOME/opt/SFML-2.5.1` for example, you'll need to tell the linker where to find the SFML libraries (.so files):

```
g++ test.cpp -o sfml-app -L<sfml-install-path>/lib -lsfml-graphics -lsfml-window -lsfml-system
```

If SFML is not installed in a standard path, you need to tell the dynamic linker where to find the SFML libraries first by specifying LD_LIBRARY_PATH:
```
export LD_LIBRARY_PATH=<sfml-install-path>/lib
```

## Compile and install imgui-sfml

Download [imgui-sfml 2.1](https://github.com/eliasdaler/imgui-sfml/tree/v2.1) and extract to `D:\Dev\tmp`

Download [imgui 1.76](https://github.com/ocornut/imgui/tree/v1.76) and extract to `D:\Dev\tmp`


```
cd D:\Dev\tmp\imgui-sfml-2.1
mkdir build && cd build

cmake .. -G Ninja ^
-DCMAKE_BUILD_TYPE=Release ^
-DCMAKE_INSTALL_PREFIX=D:\Dev\opt ^
-DIMGUI_DIR=D:\Dev\tmp\imgui-1.76 ^
-DSFML_DIR=D:\Dev\sfml-2.5.1 ^
-DBUILD_SHARED_LIBS=ON ^
-DIMGUI_SFML_BUILD_EXAMPLES=OFF

ninja -j 8

cmake --build . --target install

-- Install to:
-- D:\Dev\opt\bin           --> dll
-- D:\Dev\opt\include       --> header files
-- D:\Dev\opt\lib\cmake\ImGui-SFML
```

imgui-sfml will be built as shared lib and installed to `D:\Dev\opt`

### Test imgui-sfml

Sample program:
```cpp
#include "imgui.h"
#include "imgui-SFML.h"

#include <SFML/Graphics/RenderWindow.hpp>
#include <SFML/System/Clock.hpp>
#include <SFML/Window/Event.hpp>
#include <SFML/Graphics/CircleShape.hpp>

int main()
{
  sf::RenderWindow window(sf::VideoMode(640, 480), "ImGui + SFML = <3");
  window.setFramerateLimit(60);
  ImGui::SFML::Init(window);

  sf::CircleShape shape(100.f);
  shape.setFillColor(sf::Color::Green);

  sf::Clock deltaClock;
  while (window.isOpen())
  {
    sf::Event event;
    while (window.pollEvent(event))
    {
      ImGui::SFML::ProcessEvent(event);

      if (event.type == sf::Event::Closed)
      {
        window.close();
      }
    }

    ImGui::SFML::Update(window, deltaClock.restart());

    ImGui::Begin("Hello, world!");
    ImGui::Button("Look at this pretty button");
    ImGui::End();

    window.clear();
    window.draw(shape);
    ImGui::SFML::Render(window);
    window.display();
  }

  ImGui::SFML::Shutdown();
}
```

Create CMakeLists.txt:
```
set(ImGui-SFML_DIR "D:/Dev/opt/lib/cmake/ImGui-SFML")
find_package(ImGui-SFML REQUIRED)

add_executable(test_imgui main.cpp)
target_link_libraries(test_imgui PRIVATE ImGui-SFML::ImGui-SFML)
```

## Compile and install spdlog (header only lib)

Download [spdlog-1.5.0](https://github.com/gabime/spdlog/tree/v1.5.0) and extract to `D:\Dev\Tools`

Compile and install:

```
cd D:\Dev\tmp\spdlog-1.5.0
mkdir build && cd build

cmake .. -G Ninja ^
-DCMAKE_BUILD_TYPE=Release ^
-DCMAKE_INSTALL_PREFIX=D:\Dev\opt ^
-DSPDLOG_BUILD_EXAMPLE=OFF ^
-DSPDLOG_BUILD_TESTS=OFF

cmake --build . --target install

-- Install to:
-- D:\Dev\opt\include\spdlog
-- D:\Dev\opt\lib
-- D:\Dev\opt\lib\cmake\spdlog
```

To use just `#include "spdlog/spdlog.h"`

Sample program:
```cpp
#include "spdlog/spdlog.h"
#include "spdlog/sinks/basic_file_sink.h"

int main()
{

  spdlog::info("Sample Info output.");
  spdlog::warn("Sample Warn output.");
  spdlog::error("Sample Error output.");

  auto filelog = spdlog::basic_logger_mt("sample-logger", "sample-log.txt");

  filelog.get()->info("Sample Info output.");
  filelog.get()->warn("Sample Warn output.");
  filelog.get()->error("Sample Error output.");

  return 0;
}
```

CMakeLists.txt
```
# spdlog
set(spdlog_DIR "D:/Dev/Tools/spdlog-1.5.0/lib/cmake/spdlog")
find_package(spdlog REQUIRED)

add_executable(spdlog_test spdlog_test.cpp)
target_link_libraries(spdlog_test PRIVATE spdlog::spdlog_header_only)
```

## docopt.cpp

Download [docopt.cpp 0.6.2](https://github.com/docopt/docopt.cpp/tree/v0.6.2) and extract to `D:\Dev\tmp`

Compile and install:
```
cd D:\Dev\tmp\docopt.cpp-0.6.2
mkdir build && cd build

cmake .. -G Ninja ^
-DCMAKE_BUILD_TYPE=Release ^
-DCMAKE_INSTALL_PREFIX=D:\Dev\opt ^
-DWITH_TESTS=OFF ^
-DWITH_EXAMPLE=OFF

ninja -j 8

cmake --build . --target install

-- Install to:
-- D:\Dev\opt\lib
-- D:\Dev\opt\include\docopt
-- D:\Dev\opt\lib\cmake\docopt
```
