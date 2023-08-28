# Chapter 1 - Learning Modern Core Language Features

## Using `auto` whenever possible

Important benefits of using the `auto` instead of actual types:
* It is **not** possible to leave a variable uninitialized, because `auto` requires an initialization of the variable in order to deduce the type.
* Ensures that you always use the correct type and that implicit conversion will not occur.
```cpp
auto v = std::vector<int>{1,2,3};
int size1 = v.size();   // implicit conversion, possible loss of data
auto size2 = v.size();  // OK, type is std::size_t
```
* Promotes good OOP practices such as preferring interfaces over implementation.
* Less typing and less concern for actual types that we don't care about anyway.

Some gotchas:
* Is only a placeholder for the type, not for the `const/volatile` and references specifiers. You need to specify them explicitly.
```cpp
class foo {
  int x_;
public:
  foo(int const x = 0) : x_{ x } {}
  int& get() { return x_; }
};

foo f(42);
auto x = f.get();   // type of x is int not int&
auto& xr = f.get(); // type of x is int&
```
* It is not possible to use `auto` for types that are not movable. <???>
```cpp
auto ai = std::atomic<int>(42); // error
```
* It is not possible to use `auto` for multi-word types such as `long long, long double` or `struct foo`. We can work around by using literals or type aliases.
```cpp
  auto l1 = long long{ 42 };  // error

  using llong = long long;
  auto l2 = llong{ 42 };    // OK
```
* `auto` can be used to specify the return type from a function (since C++14)
* `decltype(auto)` <???>
* As of C++14, both lambda return types and parameter types can be `auto`. Such lambda is called a *generic lambda* because the closure type defined by the lambda has a templated call operator(). <???>

## Creating type aliases and alias templates

`typedef` cannot be used with templates to create template type aliases. `std::vector<T>` is not a type (`std::vector<int>` is a type)

Create type aliases as follow:
```cpp
using byte = unsigned char;
using byte_ptr = unsigned char*;
using array_t = int[10];
using fn = void(byte, double);
```

Create alias templates as follow:
```cpp
template<typename T>
using vec_t = std::vector<T>;

vec_t<int> vi;
vec_t<std::string> vs;
```

For consistency and readability, you should do:
* Not mix `typedef` and `using` when creating aliases.
* Prefer the `using` syntax to create names of function pointer types.

## Understanding uniform initialization

Brace-initialization form {} can be used for both direct initialization and copy initialization.
```cpp
T object{other};     // direct-list initialization
T object = {other};  // copy-list initialization
```

> A Plain Old Data (POD) type is a type that is both trivial and has a standard layout.

Initialization of standard containers, such as vector and map, is possible because all standard containers have an additional constructor in C++11 that takes an argument of the type `std::intializer_list<T>`

Brace-initializaion does not allow narrowing conversion.
```cpp
int i{ 1.2 };  // error
double d = 47 / 13;
float f1{ d };  // error
```

To fix this error, an explicit conversion must be done:
```cpp
int i{ static_cast<int>(1.2) };

double d = 47/13;
float f1{ static_cast<float>(d) };
```

## Understanding the various forms of non-static member initialization

From C++11 allows the initialization of non-statics in the class declaration. This is called *default member initialization*.

- Use default member intialization for constants, both static and non-static.
- Use default member initializaion to provide default values for members of classes with multiple constructors that would use a common initializer for those members.
- Use the constructor initializer list to initialize members that don't have default values, but depend on constructor parameters.

> It is important to note that the order in which non-static data members are initialized is the order in which they were declared in the class, and not the order of their initialization in a constructor initializer list.

Default member initialization is intended for constants and for members that are not initialized based on constructor parameters 
(in other words, members whose value does not depend on the way the object is constructed)

## Controlling and querying object alignment

C++ compilers align variables based on the size of their data type. The standard only specifies the sizes of char, signed char, unsigned char, char8_t, and std::byte, which must be 1. It also requires that the size of short must be at least 16 bits, the size of long must be at least 32 bits, and that the size of long long must be at least 64 bits.

In C++11, specifying the alignment of an object or type is done using the `alignas` specifier. This can take either an expression (an integral constant expression that evaluates to 0 or a valid value for an alignment), a type-id, or a parameter pack. The alignas specifier can be applied to the declaration of a variable or a class data member that does not represent a bit field, or to the declaration of a class, union, or enumeration.

## Using scoped enumerations

- Possible to fully qualify the names of the enumerators.
```cpp
enum class Status { Unknown, Created, Connected };
enum class Codes { OK, Failure, Unknown };          // OK, no clash with Status::Unknown
auto status = Status::Created;                      // OK, fully qualified name
```
- By specifying the underlying type, we can forward declare the scoped enumerators.
- Values of scoped enumerations no longer convert implicitly to int.
```cpp
Codes c1 = Codes::OK;    // OK
int c2 = Codes::Failure;  // error
int c3 = static_cast<int>(Codes::Failure);    // OK
```

## Using `override` and `final` for virtual methods

Both the `override` and `final` keywords are special identifiers that have a meaning only in a member function declaration or definition. They are not reserved keywords and can still be used elsewhere in a program as user-defined identifiers.

## Using range-based for loops to iterate on a range

It is important to note that if a class contains any members (function, data member, or enumerators) called begin or end, regardless of their type and accessibility, they will be picked for begin_expr and end_expr. Therefore, such a class type cannot be used in range-based for loops.
