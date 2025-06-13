# My Notes

# 2025-05-23

## C++ Rule of Zero, Three, Five

https://flamingdangerzone.com/cxx11/rule-of-zero/

### Rule of Three (pre C++11)

What happens when a copy of an object that owns a resource is made? By default a memberwise copy is performed. This means that the internal resource handle the object stores will be copied, ending up with two objects that own the same resource. This is likely to lead to them both trying to release the resource, and catastrophe follows.

> [!NOTE]
> If a class defines a destructor, copy constructor or copy assignment operator then it should probably explicitly define all three, and not rely on their default implementation.

### Rule of Zero

> [!NOTE]
> Classes should not define any of the special functions (copy/move constructors/assignment, and the destructor) unless they are classes dedicated to resource management.

The goal is to let the compiler provide optimal versions that are automatically maintained when more member variables are added.

If you don’t write the special functions, the compiler generates them for you by trying to apply the expected operation on a member by member basis. So if you use the default move constructor, the compiler will generate a move constructor that simply attempts to move construct all data members (and base classes). As soon as you write a custom move constructor that does some special handling for one data member, you now have to write code to deal with every other member, even if you just need to change the one.

## Provided by Grok
In C++, the **Rule of Zero**, **Rule of Three**, and **Rule of Five** are guidelines for managing resource ownership and ensuring proper behavior of classes that handle resources (e.g., memory, file handles, sockets). These rules help prevent resource leaks, undefined behavior, and other issues related to object lifecycle management. Below is a concise explanation of each rule, including their purpose and implications.

### 1. **Rule of Zero**
**Definition**: Classes should ideally be designed to avoid manually implementing special member functions (constructor, destructor, copy/move operations) by relying on compiler-generated defaults or using resource-managing types (e.g., smart pointers, containers) that handle resources automatically.

**Key Points**:
- **Goal**: Write classes that require no custom resource management, making them simpler and less error-prone.
- **How to Achieve**:
  - Use standard library types like `std::vector`, `std::string`, or `std::unique_ptr` to manage resources.
  - Avoid raw pointers or manual resource management (e.g., `new`/`delete`).
  - Let the compiler generate default implementations of the destructor, copy constructor, copy assignment operator, move constructor, and move assignment operator.
- **When It Applies**: Ideal for classes that don’t directly manage resources or when resources are encapsulated in RAII (Resource Acquisition Is Initialization) types.
- **Example**:
  ```cpp
  class RuleOfZero {
      std::string name;
      std::vector<int> data;
  public:
      // No need to define destructor, copy/move operations
      // Compiler-generated defaults work correctly
  };
  ```
  Here, `std::string` and `std::vector` handle their own resources, so no custom special member functions are needed.

**Benefits**:
- Simplifies class design.
- Reduces bugs from incorrect resource management.
- Leverages modern C++ idioms (e.g., RAII).

### 2. **Rule of Three**
**Definition**: If a class defines any one of the following three special member functions, it should explicitly define all three:
1. **Destructor** (`~ClassName()`)
2. **Copy Constructor** (`ClassName(const ClassName&)` or `ClassName(const ClassName&, ...args)`)
3. **Copy Assignment Operator** (`ClassName& operator=(const ClassName&)`)

**Key Points**:
- **Why It Exists**: Classes that manage resources (e.g., raw pointers) need custom implementations to handle copying and destruction correctly, as compiler-generated defaults may lead to shallow copies or resource leaks.
- **When It Applies**: Common in pre-C++11 code or when managing raw resources (e.g., raw pointers, file handles) without RAII types.
- **Example**:
  ```cpp
  class RuleOfThree {
      int* data;
  public:
      RuleOfThree(int value) : data(new int(value)) {}
      // Destructor
      ~RuleOfThree() { delete data; }
      // Copy Constructor
      RuleOfThree(const RuleOfThree& other) : data(new int(*other.data)) {}
      // Copy Assignment Operator
      RuleOfThree& operator=(const RuleOfThree& other) {
          if (this != &other) {
              delete data;
              data = new int(*other.data);
          }
          return *this;
      }
  };
  ```
  Here, the class manages a raw pointer, so all three functions are defined to prevent shallow copying or memory leaks.

**Implications**:
- Ensures proper resource management during copying and destruction.
- Failure to follow can lead to double deletion, memory leaks, or undefined behavior.
- Pre-C++11, this was critical for resource-owning classes.

### 3. **Rule of Five**
**Definition**: An extension of the Rule of Three for C++11 and later, which adds two move-related special member functions. If a class defines any of the following five special member functions, it should explicitly define all five:
1. **Destructor** (`~ClassName()`)
2. **Copy Constructor** (`ClassName(const ClassName&)` or `ClassName(const ClassName&, ...args)`)
3. **Copy Assignment Operator** (`ClassName& operator=(const ClassName&)`)
4. **Move Constructor** (`ClassName(ClassName&&)` or `ClassName(ClassName&&, ...args)`)
5. **Move Assignment Operator** (`ClassName& operator=(ClassName&&)`)

**Key Points**:
- **Why It Exists**: C++11 introduced move semantics to optimize resource transfer (e.g., moving ownership of a resource instead of copying). If a class manages resources and defines any of the Rule of Three functions, it likely needs move operations to support efficient resource transfer.
- **When It Applies**: For classes managing resources in C++11 or later, especially when move semantics can improve performance (e.g., transferring ownership of a `std::unique_ptr`).
- **Example**:
  ```cpp
  class RuleOfFive {
      int* data;
  public:
      RuleOfFive(int value) : data(new int(value)) {}
      // Destructor
      ~RuleOfFive() { delete data; }
      // Copy Constructor
      RuleOfFive(const RuleOfFive& other) : data(new int(*other.data)) {}
      // Copy Assignment Operator
      RuleOfFive& operator=(const RuleOfFive& other) {
          if (this != &other) {
              delete data;
              data = new int(*other.data);
          }
          return *this;
      }
      // Move Constructor
      RuleOfFive(RuleOfFive&& other) noexcept : data(other.data) {
          other.data = nullptr;
      }
      // Move Assignment Operator
      RuleOfFive& operator=(RuleOfFive&& other) noexcept {
          if (this != &other) {
              delete data;
              data = other.data;
              other.data = nullptr;
          }
          return *this;
      }
  };
  ```
  Here, move operations efficiently transfer ownership of the pointer without copying the underlying resource.

**Implications**:
- Ensures both copy and move semantics are handled correctly.
- Move operations should be `noexcept` to enable optimizations (e.g., in `std::vector`).
- Failure to implement move operations may lead to unnecessary copying, reducing performance.

### Key Differences and Relationships
| Rule              | Special Member Functions                          | When to Use                          | Focus                                     |
| ----------------- | ------------------------------------------------- | ------------------------------------ | ----------------------------------------- |
| **Rule of Zero**  | None (use defaults)                               | Modern C++ with RAII types           | Simplicity, no manual resource management |
| **Rule of Three** | Destructor, Copy Constructor, Copy Assignment     | Pre-C++11 or raw resource management | Correct copy semantics and cleanup        |
| **Rule of Five**  | Rule of Three + Move Constructor, Move Assignment | C++11+ with resource management      | Copy and move semantics, performance      |

### Practical Guidelines
- **Prefer Rule of Zero**: In modern C++ (C++11 and later), design classes to follow the Rule of Zero by using RAII types like `std::unique_ptr`, `std::shared_ptr`, or `std::vector`. This avoids the need to write any special member functions.
- **Use Rule of Three for Legacy Code**: If you must manage raw resources (e.g., in pre-C++11 code or when RAII types are not feasible), follow the Rule of Three to handle copying and destruction correctly.
- **Use Rule of Five for Performance**: In C++11 and later, if a class manages resources and needs custom copy operations, also implement move operations to enable efficient resource transfer.
- **Explicitly Define or Disable**: If you define one special member function, explicitly define or `=delete` the others to avoid unexpected compiler-generated behavior. For example:
  ```cpp
  class NonCopyable {
  public:
      NonCopyable() = default;
      NonCopyable(const NonCopyable&) = delete; // Disable copy constructor
      NonCopyable& operator=(const NonCopyable&) = delete; // Disable copy assignment
  };
  ```

### Example Combining All Rules
```cpp
#include <memory>
#include <vector>

// Rule of Zero: No custom special member functions
class ZeroExample {
    std::vector<int> data;
    std::unique_ptr<int> ptr;
public:
    ZeroExample() = default; // Compiler handles everything
};

// Rule of Three: Pre-C++11 style with raw pointer
class ThreeExample {
    int* data;
public:
    ThreeExample(int val) : data(new int(val)) {}
    ~ThreeExample() { delete data; }
    ThreeExample(const ThreeExample& other) : data(new int(*other.data)) {}
    ThreeExample& operator=(const ThreeExample& other) {
        if (this != &other) {
            delete data;
            data = new int(*other.data);
        }
        return *this;
    }
};

// Rule of Five: C++11+ with move semantics
class FiveExample {
    int* data;
public:
    FiveExample(int val) : data(new int(val)) {}
    ~FiveExample() { delete data; }
    FiveExample(const FiveExample& other) : data(new int(*other.data)) {}
    FiveExample& operator=(const FiveExample& other) {
        if (this != &other) {
            delete data;
            data = new int(*other.data);
        }
        return *this;
    }
    FiveExample(FiveExample&& other) noexcept : data(other.data) {
        other.data = nullptr;
    }
    FiveExample& operator=(FiveExample&& other) noexcept {
        if (this != &other) {
            delete data;
            data = other.data;
            other.data = nullptr;
        }
        return *this;
    }
};
```

### Conclusion
- **Rule of Zero** is the modern C++ ideal, leveraging RAII to avoid manual resource management.
- **Rule of Three** ensures correct copy semantics and cleanup for resource-owning classes in pre-C++11 or raw-resource scenarios.
- **Rule of Five** extends the Rule of Three to include move semantics for better performance in C++11 and later.
By following these rules, you ensure safe resource management, prevent bugs, and optimize performance in C++ programs. Always aim for the Rule of Zero when possible, falling back to the Rule of Three or Five only when necessary.

# 2025-06-07

To integrate `clang-tidy` and `cppcheck` into a CMake-based C++ project for static analysis, you can configure your CMake build system to run these tools automatically during the build process or as separate targets. Below is a step-by-step guide to set up both tools with CMake, including practical examples and best practices.

### Prerequisites
- **Install `clang-tidy`**:
  - On Ubuntu: `sudo apt-get install clang-tidy`
  - On macOS: `brew install llvm` (ensure `clang-tidy` is in your PATH)
  - On Windows: Install via LLVM installer or package manager like MSYS2/Choco.
- **Install `cppcheck`**:
  - On Ubuntu: `sudo apt-get install cppcheck`
  - On macOS: `brew install cppcheck`
  - On Windows: Install via MSYS2 or download the binary.
- **CMake**: Ensure you have CMake 3.6 or later (for `clang-tidy` integration).
- **C++ Project**: A CMake-based project with source files to analyze.

### 1. **Using `clang-tidy` with CMake**
`clang-tidy` is a powerful tool for static analysis, checking for style violations, bug-prone patterns, and modern C++ best practices. CMake has built-in support for `clang-tidy` via the `CMAKE_<LANG>_CLANG_TIDY` variable.

#### Steps to Integrate `clang-tidy`
1. **Enable `clang-tidy` in CMake**:
   Add the following to your `CMakeLists.txt` to enable `clang-tidy` for all C++ targets:
   ```cmake
   set(CMAKE_CXX_CLANG_TIDY
       clang-tidy;
       -header-filter=.;
       -checks=*,-llvmlibc-*,-android-*,-google-*; # Customize checks as needed
       -warnings-as-errors=*; # Optional: Treat warnings as errors
   )
   ```
   - `-header-filter=.*`: Analyzes headers in your project (adjust regex to match your project structure).
   - `-checks=*,-llvmlibc-*,-android-*,-google-*`: Enables most checks but excludes specific ones (customize based on your needs; run `clang-tidy --list-checks` to see available checks).
   - `-warnings-as-errors=*`: Forces the build to fail on warnings (optional).

2. **Create a `.clang-tidy` Configuration File (Optional)**:
   For more control, create a `.clang-tidy` file in your project root to specify checks and options:
   ```yaml
   Checks: '*,-llvmlibc-*,-android-*,-google-*'
   HeaderFilterRegex: '.*'
   FormatStyle: 'file'
   ```
   Then, tell `clang-tidy` to use this file:
   ```cmake
   set(CMAKE_CXX_CLANG_TIDY
       clang-tidy;
       --config-file=${CMAKE_SOURCE_DIR}/.clang-tidy;
   )
   ```

3. **Run `clang-tidy` During Build**:
   - When `CMAKE_CXX_CLANG_TIDY` is set, `clang-tidy` runs automatically during compilation for each C++ source file.
   - Build your project as usual:
     ```bash
     mkdir build && cd build
     cmake ..
     make
     ```
   - If `clang-tidy` finds issues, they will be reported in the build output, and the build may fail if warnings are treated as errors.

4. **Create a Dedicated `clang-tidy` Target (Optional)**:
   To run `clang-tidy` without building, create a custom target:
   ```cmake
   find_program(CLANG_TIDY_EXECUTABLE NAMES clang-tidy)
   if(CLANG_TIDY_EXECUTABLE)
       file(GLOB_RECURSIVE SOURCES "${CMAKE_SOURCE_DIR}/src/*.cpp" "${CMAKE_SOURCE_DIR}/include/*.h")
       add_custom_target(
           clang-tidy
           COMMAND ${CLANG_TIDY_EXECUTABLE}
                   -p ${CMAKE_BINARY_DIR}
                   --config-file=${CMAKE_SOURCE_DIR}/.clang-tidy
                   ${SOURCES}
           WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
           COMMENT "Running clang-tidy"
       )
   endif()
   ```
   - Run with: `make clang-tidy` in the build directory.
   - `-p ${CMAKE_BINARY_DIR}`: Uses the compilation database (`compile_commands.json`) generated by CMake (enable it with `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)`).
   - `${SOURCES}`: Lists all source and header files to analyze.

5. **Fix Issues Automatically**:
   `clang-tidy` can apply fixes for certain issues:
   ```bash
   clang-tidy -fix -p build/ src/*.cpp
   ```
   To integrate this into CMake, modify the custom target:
   ```cmake
   add_custom_target(
       clang-tidy-fix
       COMMAND ${CLANG_TIDY_EXECUTABLE}
               -fix
               -p ${CMAKE_BINARY_DIR}
               --config-file=${CMAKE_SOURCE_DIR}/.clang-tidy
               ${SOURCES}
       WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
       COMMENT "Running clang-tidy with fixes"
   )
   ```
   Run with: `make clang-tidy-fix`.

### 2. **Using `cppcheck` with CMake**
`cppcheck` is another static analysis tool focused on detecting bugs, memory leaks, and undefined behavior. Unlike `clang-tidy`, CMake does not have built-in support for `cppcheck`, so you need to create custom targets.

#### Steps to Integrate `cppcheck`
1. **Find `cppcheck` Executable**:
   Add the following to your `CMakeLists.txt` to locate `cppcheck`:
   ```cmake
   find_program(CPPCHECK_EXECUTABLE NAMES cppcheck)
   if(NOT CPPCHECK_EXECUTABLE)
       message(WARNING "cppcheck not found. Static analysis target will not be available.")
   endif()
   ```

2. **Create a Custom `cppcheck` Target**:
   Define a custom target to run `cppcheck` on your source files:
   ```cmake
   if(CPPCHECK_EXECUTABLE)
       file(GLOB_RECURSIVE SOURCES "${CMAKE_SOURCE_DIR}/src/*.cpp" "${CMAKE_SOURCE_DIR}/include/*.h")
       add_custom_target(
           cppcheck
           COMMAND ${CPPCHECK_EXECUTABLE}
                   --enable=all
                   --std=c++17 # Adjust to your C++ standard
                   --suppress=missingIncludeSystem
                   --project=${CMAKE_BINARY_DIR}/compile_commands.json
                   --quiet
                   --inline-suppr
                   ${SOURCES}
           WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
           COMMENT "Running cppcheck"
       )
   endif()
   ```
   - `--enable=all`: Enables all checks (style, performance, portability, etc.).
   - `--std=c++17`: Specifies the C++ standard (adjust as needed).
   - `--suppress=missingIncludeSystem`: Ignores warnings about missing system headers.
   - `--project=${CMAKE_BINARY_DIR}/compile_commands.json`: Uses the compilation database for accurate analysis.
   - `--quiet`: Reduces output verbosity.
   - `${SOURCES}`: Lists source and header files (optional if using `--project`).

3. **Enable Compilation Database**:
   Ensure CMake generates `compile_commands.json`:
   ```cmake
   set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
   ```

4. **Run `cppcheck`**:
   - Build the `cppcheck` target:
     ```bash
     mkdir build && cd build
     cmake ..
     make cppcheck
     ```
   - `cppcheck` will analyze the project and report issues in the terminal.

5. **Optional: Generate Reports**:
   To generate an HTML report for `cppcheck`:
   ```cmake
   add_custom_target(
       cppcheck-html
       COMMAND ${CPPCHECK_EXECUTABLE}
               --enable=all
               --std=c++17
               --suppress=missingIncludeSystem
               --project=${CMAKE_BINARY_DIR}/compile_commands.json
               --quiet
               --inline-suppr
               --xml
               ${SOURCES}
               2> cppcheck.xml
       COMMAND cppcheck-htmlreport
               --file=cppcheck.xml
               --report-dir=cppcheck-report
               --source-dir=${CMAKE_SOURCE_DIR}
       WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
       COMMENT "Generating cppcheck HTML report"
   )
   ```
   - Install `cppcheck-htmlreport` (may require a separate installation, e.g., `sudo apt-get install cppcheck-htmlreport` on Ubuntu).
   - Run with: `make cppcheck-html`.
   - The report will be generated in `build/cppcheck-report/`.

### 3. **Example `CMakeLists.txt`**
Here’s a complete `CMakeLists.txt` integrating both `clang-tidy` and `cppcheck`:
```cmake
cmake_minimum_required(VERSION 3.6)
project(MyProject LANGUAGES CXX)

# Enable compilation database for clang-tidy and cppcheck
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
file(GLOB_RECURSIVE SOURCES "${CMAKE_SOURCE_DIR}/src/*.cpp")
file(GLOB_RECURSIVE HEADERS "${CMAKE_SOURCE_DIR}/include/*.h")

# Main executable
add_executable(myproject ${SOURCES} ${HEADERS})

# clang-tidy setup
find_program(CLANG_TIDY_EXECUTABLE NAMES clang-tidy)
if(CLANG_TIDY_EXECUTABLE)
    set(CMAKE_CXX_CLANG_TIDY
        clang-tidy;
        --config-file=${CMAKE_SOURCE_DIR}/.clang-tidy;
    )
    add_custom_target(
        clang-tidy
        COMMAND ${CLANG_TIDY_EXECUTABLE}
                -p ${CMAKE_BINARY_DIR}
                --config-file=${CMAKE_SOURCE_DIR}/.clang-tidy
                ${SOURCES} ${HEADERS}
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Running clang-tidy"
    )
endif()

# cppcheck setup
find_program(CPPCHECK_EXECUTABLE NAMES cppcheck)
if(CPPCHECK_EXECUTABLE)
    add_custom_target(
        cppcheck
        COMMAND ${CPPCHECK_EXECUTABLE}
                --enable=all
                --std=c++17
                --suppress=missingIncludeSystem
                --project=${CMAKE_BINARY_DIR}/compile_commands.json
                --quiet
                --inline-suppr
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Running cppcheck"
    )
endif()
```

### 4. **Sample `.clang-tidy` File**
Place this in your project root:
```yaml
Checks: '*,-llvmlibc-*,-android-*,-google-*,-fuchsia-*'
HeaderFilterRegex: '.*'
CheckOptions:
  - key: readability-identifier-naming.ClassCase
    value: CamelCase
  - key: readability-identifier-naming.VariableCase
    value: camelBack
```

### 5. **Running the Analysis**
- **Build and analyze with `clang-tidy`**:
  ```bash
  mkdir build && cd build
  cmake ..
  make
  ```
  `clang-tidy` runs during compilation.

- **Run `clang-tidy` separately**:
  ```bash
  make clang-tidy
  ```

- **Run `cppcheck`**:
  ```bash
  make cppcheck
  ```

- **Generate `cppcheck` HTML report** (if configured):
  ```bash
  make cppcheck-html
  ```

### 6. **Best Practices**
- **Use Compilation Database**: Both tools rely on `compile_commands.json` for accurate analysis. Always enable `CMAKE_EXPORT_COMPILE_COMMANDS ON`.
- **Customize Checks**: Tailor `clang-tidy` checks and `cppcheck` options to your project’s needs to avoid noise.
- **CI Integration**: Add `make clang-tidy` and `make cppcheck` to your CI pipeline to enforce static analysis on every commit.
- **Separate Targets**: Use custom targets for flexibility, allowing developers to run analysis without rebuilding.
- **Fix Warnings Gradually**: Both tools may produce many warnings initially. Prioritize critical issues (e.g., `cppcheck`’s `error` severity or `clang-tidy`’s bug-related checks).

### 7. **Common Issues and Solutions**
- **Missing `compile_commands.json`**:
  Ensure `CMAKE_EXPORT_COMPILE_COMMANDS ON` is set, and the build directory contains `compile_commands.json`.
- **`clang-tidy` Slows Down Builds**:
  Run `clang-tidy` as a separate target (`make clang-tidy`) instead of during compilation, or limit checks.
- **False Positives**:
  Suppress specific `cppcheck` warnings with `--suppress` or inline comments (`// cppcheck-suppress ruleName`).
  For `clang-tidy`, use `// NOLINT` or `// NOLINTNEXTLINE` in code.
- **Header Files Not Analyzed**:
  Ensure `header-filter` (for `clang-tidy`) or source file globs (for both tools) include your headers.

### Conclusion
By integrating `clang-tidy` and `cppcheck` into your CMake project, you can catch potential bugs, enforce coding standards, and improve code quality. Use `CMAKE_CXX_CLANG_TIDY` for seamless `clang-tidy` integration during builds, and create custom targets for `cppcheck` and optional `clang-tidy` runs. Customize configurations to suit your project, and consider automating these checks in your CI pipeline for consistent code quality.

# 2025-06-12

## Recommended clang-tidy checks

For a modern C++ project (e.g., using C++11/14/17/20), `clang-tidy` offers targeted checks to enforce best practices, improve code quality, and catch potential issues. Below are recommended `clang-tidy` checks, focusing on modern C++ features, performance, readability, and bug prevention. These are concise and prioritized for a typical modern C++ project.

### Recommended `clang-tidy` Checks
1. **Modernize Checks** (`modernize-*`):
   - `modernize-use-auto`: Use `auto` for type inference to improve readability and flexibility.
   - `modernize-use-override`: Enforce `override` keyword for virtual functions to prevent errors.
   - `modernize-use-nullptr`: Replace `NULL` or `0` with `nullptr` for type safety.
   - `modernize-use-emplace`: Prefer `emplace` over `push` for containers to avoid unnecessary copies.
   - `modernize-loop-convert`: Convert compatible `for` loops to range-based `for` loops.
   - `modernize-make-unique` / `modernize-make-shared`: Use `std::make_unique`/`std::make_shared` for safer smart pointer creation.

2. **Performance Checks** (`performance-*`):
   - `performance-unnecessary-copy-initialization`: Avoid unnecessary copies in variable initialization.
   - `performance-for-range-copy`: Prevent copying in range-based `for` loops when references suffice.
   - `performance-inefficient-string-concatenation`: Detect inefficient string concatenation (e.g., using `+` instead of `+=`).

3. **Readability Checks** (`readability-*`):
   - `readability-identifier-naming`: Enforce consistent naming conventions (e.g., camelCase for variables, PascalCase for types).
   - `readability-braces-around-statements`: Require braces for single-statement blocks to prevent errors.
   - `readability-simplify-boolean-expr`: Simplify complex boolean expressions for clarity.
   - `readability-else-after-return`: Avoid unnecessary `else` after `return` statements.

4. **Bugprone Checks** (`bugprone-*`):
   - `bugprone-use-after-move`: Catch invalid use of objects after being moved.
   - `bugprone-undefined-memory-manipulation`: Detect misuse of uninitialized memory.
   - `bugprone-narrowing-conversions`: Flag potentially unsafe type conversions.
   - `bugprone-exception-escape`: Ensure exceptions don’t escape where prohibited.

5. **CERT C++ Checks** (`cert-*`):
   - `cert-err58-cpp`: Avoid static initialization order fiasco.
   - `cert-oop54-cpp`: Enforce proper copy/move operator overloads.
   - `cert-dcl50-cpp`: Prevent unsafe use of `goto` or problematic declarations.

### Configuring in CMake
Add these checks to your `CMakeLists.txt`:
```cmake
set(CMAKE_CXX_CLANG_TIDY "clang-tidy;-checks=modernize-*,performance-*,readability-*,bugprone-*,cert-*;-header-filter=.*")
```
- The `-header-filter=.*` ensures headers are also checked.
- Optionally, create a `.clang-tidy` file in your project root to fine-tune checks or suppress unwanted ones:
  ```yaml
  Checks: 'modernize-*,performance-*,readability-*,bugprone-*,cert-*'
  CheckOptions:
    - key: readability-identifier-naming.VariableCase
      value: camelCase
  ```

### Notes
- **Customization**: Adjust checks based on your project’s needs (e.g., disable `readability-identifier-naming` if naming conventions are already enforced elsewhere).
- **Exclusions**: Exclude noisy checks like `modernize-use-trailing-return-type` if C++20 trailing return types aren’t desired:
  ```cmake
  set(CMAKE_CXX_CLANG_TIDY "clang-tidy;-checks=modernize-*,-modernize-use-trailing-return-type,performance-*,readability-*,bugprone-*,cert-*")
  ```
- **Run Regularly**: Integrate into your build or CI pipeline to catch issues early.
- **Balance**: Avoid enabling all checks (`-checks=*`) to prevent overwhelming output; start with the above and expand as needed.

These checks align with modern C++ practices, emphasizing safety, performance, and maintainability, complementing compiler warnings (e.g., `gcc -Wall`) by catching deeper issues. For comparison with `gcc` and `cppcheck`, refer to the prior response.