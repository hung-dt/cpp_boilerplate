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
