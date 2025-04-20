Notes for the course: [C++ Setup and Installation Tools – CMake, vcpkg, Docker & Copilot](https://youtu.be/0ffwhxW-uyw?si=3Dvuj_-qPYKmGoma)

# Windows Setup

## Install compiler and IDE

### Visual Studio IDE

https://github.com/rutura/cpp23m/blob/main/02.EnvironmentSetup/03.Windows_setup.md

### MSYS2 and MinGW-w64

#### Download & Install MSYS2

Download [here](https://www.msys2.org/)

Just launch the installer and keep clicking "Next". Change Installation folder to `D:\Dev\Tools\msys64`

Run MSYS2, type the following command:
```
pacman -Syu
```
`pacman` is the package manager used by MSYS2. `-S` means "sync". `-y` means "download fresh package databases from the server". `-u` means "upgrade installed packages".

This command will update the packages info, so you get the latest packages. It will prompt you like this, and you type `y` and hit enter.

MSYS2 offers different [environments](https://www.msys2.org/docs/environments/) for compiling, each with its own C runtime library and build toolchain. For most users, UCRT64 (Universal C Runtime Library) is generally recommended due to its compatibility with newer Windows systems and potential better integration with Visual Studio. MINGW64 uses the older MSVCRT, while MSYS is a base environment providing Unix-like tools and utilities.

For most users, UCRT64 is the recommended default. If you need to build binaries for older Windows versions that might not have the UCRT libraries, then MINGW64 would be necessary. MSYS is the underlying base environment for both.

Relaunch MSYS2 from your start menu and run this command to install MinGW-w64 toolchain:
```
pacman -S --needed base-devel mingw-w64-ucrt-x86_64-toolchain
```
Accept the default number of packages in the toolchain group by pressing `Enter`.
![image](https://github.com/user-attachments/assets/75e512bb-d7d0-453e-877a-03662f430ec2)

After installation, add `D:\Dev\Tools\msys64\ucrt64\bin` to Windows' PATH environment variable and test it.
```
C:\Users\HungDT>gcc --version
gcc (Rev3, Built by MSYS2 project) 14.2.0
Copyright (C) 2024 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

### Install clang

With MSYS2 ucrt:
```
pacman -S mingw-w64-ucrt-x86_64-clang mingw-w64-ucrt-x86_64-clang-tools-extra
```

Verify:
```
C:\Users\HungDT>clang --version
clang version 20.1.2
Target: x86_64-w64-windows-gnu
Thread model: posix
InstalledDir: E:/Dev/Tools/msys64/ucrt64/bin

C:\Users\HungDT>clang-format --version
clang-format version 20.1.2

C:\Users\HungDT>clang-tidy --version
LLVM (http://llvm.org/):
  LLVM version 20.1.2
  Optimized build.
```

### MinGW-w64 from WinLibs

https://winlibs.com/

## Install CMake & Ninja

CMake is essential for building C++ projects. Download and install the latest version from [CMake's official site](https://cmake.org/download/). After installation, do the following:

- Add CMake `bin` directory to your system PATH during installation.
- Verify the installation by running `cmake --version` in a new terminal or powershell window. You should see the installed version of CMake like below:
```
C:\Users\HungDT>cmake --version
cmake version 3.31.7

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

Ninja is a fast build system used with CMake. Install it for MSYS2 ucrt64:
```
pacman -S mingw-w64-ucrt-x86_64-ninja
```

## Install Git

Git is a popular version control system used by many developers. Download the portable version and install it from [Git's official site](https://git-scm.com/). After installation, do the following:

- Add Git `E:\Dev\Tools\PortableGit\bin` to your system PATH during installation.
- Verify the installation by running `git --version` in a new terminal or powershell window. You should see the installed version of Git like below:
```
C:\Users\HungDT>git --version
git version 2.49.0.windows.1
```

## Install Vcpkg

`vcpkg` is a C/C++ package manager, which makes using libraries much easier (almost as easy as using `pip` in python). We will install it through Git. To install it:

- Open a new terminal or PowerShell window.
- cd into `E:\Dev\Workspace` and download `vcpkg` through git:
```
git clone https://github.com/microsoft/vcpkg.git
```
- This will download and create a new folder named `vcpkg` in the root directory.
- Change into the vcpkg directory and run the following command:
```
.\bootstrap-vcpkg.bat
```
- This will build the vcpkg executable.
- Confirm that you have access to the vcpkg executable by running `vcpkg --version` inside the vcpkg directory
- You should see the installed version of vcpkg like below:
```
PS E:\Dev\Workspace\vcpkg> .\vcpkg.exe --version
vcpkg package management program version 2025-04-07-b8b513ba8778c918cff49c3e837aae5999d5d2aa

See LICENSE.txt for license information.
```
- Create a new env variable `VCPKG_ROOT` to point to the vcpkg directory `E:\Dev\Workspace\vcpkg`.

## Install Visual Studio Code

- Install following extensions:
  -   C/C++ (Microsoft)
  -   C/C++ Themes (Microsoft)
  -   Better C++ Syntax
  -   CMake Tools (Microsoft)
  -   CMake (twxs)
  -   clangd (LLVM)
  -   CodeLLDB (from Vadim Chugunov)
  -   Trailing Spaces
- CodeLLDB seems to work only with binary compiled using MSVC cl or clang.
