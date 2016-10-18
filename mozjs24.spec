# parallel-installable with js185, js, mozjs17 or future mozjs >= 25
Summary:	SpiderMonkey 24 - JavaScript 1.8.5+ implementation
Summary(pl.UTF-8):	SpiderMonkey 24 - implementacja języka JavaScript 1.8.5+
Name:		mozjs24
Version:	24.2.0
Release:	4
License:	MPL v2.0
Group:		Libraries
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/mozjs-%{version}.tar.bz2
# Source0-md5:	5db79c10e049a2dc117a6e6a3bc78a8e
Patch0:		%{name}-system-virtualenv.patch
Patch1:		Disable-js-JIT-on-x32.patch
Patch2:		perl.patch
URL:		http://www.mozilla.org/js/
BuildRequires:	gcc-c++ >= 6:4.4
BuildRequires:	libffi-devel >= 5:3.0.9
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 4.9.2
BuildRequires:	perl-base >= 1:5.6
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi) >= 3.0.9
BuildRequires:	python >= 1:2.5
BuildRequires:	python-virtualenv >= 1.9.1-4
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.294
BuildRequires:	zlib-devel >= 1.2.3
Requires:	nspr >= 4.9.2
Requires:	zlib >= 1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JavaScript Reference Implementation (codename SpiderMonkey). The
package contains JavaScript runtime (compiler, interpreter,
decompiler, garbage collector, atom manager, standard classes) and
small "shell" program that can be used interactively and with .js
files to run scripts.

%description -l pl.UTF-8
Wzorcowa implementacja JavaScriptu (o nazwie kodowej SpiderMonkey).
Pakiet zawiera środowisko uruchomieniowe (kompilator, interpreter,
dekompilator, odśmiecacz, standardowe klasy) i niewielką powłokę,
która może być używana interaktywnie lub z plikami .js do uruchamiania
skryptów.

%package devel
Summary:	Header files for JavaScript reference library
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki JavaScript
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	nspr-devel >= 4.9.2

%description devel
Header files for JavaScript reference library.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki JavaScript.

%package static
Summary:	Static JavaScript reference library
Summary(pl.UTF-8):	Statyczna biblioteka JavaScript
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of JavaScript reference library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki JavaScript.

%prep
%setup -q -n mozjs-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd js/src
%configure2_13 \
	--enable-readline \
	--enable-system-ffi \
	--enable-threadsafe \
	--with-system-nspr

%{__make} \
	HOST_OPTIMIZE_FLAGS= \
	MODULE_OPTIMIZE_FLAGS= \
	MOZ_OPTIMIZE_FLAGS="-freorder-blocks" \
	MOZ_PGO_OPTIMIZE_FLAGS= \
	MOZILLA_VERSION=%{version}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C js/src install \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZILLA_VERSION=%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README js/src/README.html
%attr(755,root,root) %{_bindir}/js24
%attr(755,root,root) %{_libdir}/libmozjs-24.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/js24-config
%{_includedir}/mozjs-24
%{_pkgconfigdir}/mozjs-24.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmozjs-24.a
