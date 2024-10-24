%define install_dir /opt/epa
%define debug_package %{nil}
Name: log4cxx_epa
Version: 1.3.0
Release: 1%{?dist}
Summary: Log4cxx library built with ODBC appender for EPA.

Vendor: Fedora Project
License: Apache-2.0
URL: http://logging.apache.org/log4cxx/index.html
Source0: https://dlcdn.apache.org/logging/log4cxx/%{version}/apache-log4cxx-%{version}.tar.gz

BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: cmake
BuildRequires: unixODBC-devel

%description
Log4cxx is a popular logging library written in C++. One of its distinctive
features is the notion of inheritance in loggers. Using a logger hierarchy it
is possible to control which log statements are output at arbitrary
granularity. This helps reduce the volume of logged output and minimize the
cost of logging.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Header files and documentation used to develop with %{name}.

%description devel
Header files and documentation you can use to develop with %{name}.

%prep
%setup -q -n apache-log4cxx-%{version}

%build
cmake -S . -B "build" \
  -DBUILD_TESTING=OFF \
  -DCMAKE_INSTALL_PREFIX=%{install_dir} \
  -DBUILD_SHARED_LIBS=ON \
  -DLOG4CXX_ENABLE_ODBC=ON \
  -DCMAKE_CXX_STANDARD=14 \
  -DCMAKE_BUILD_TYPE=Release
cmake --build "build" -j2 --verbose

%install
DESTDIR=%{buildroot} cmake --install "build"

%files
%{install_dir}/lib64/liblog4cxx.so.*

%files devel
%{install_dir}/include/log4cxx
%{install_dir}/lib64/liblog4cxx.so
%{install_dir}/lib64/pkgconfig/liblog4cxx.pc
%{install_dir}/lib64/cmake/log4cxx
