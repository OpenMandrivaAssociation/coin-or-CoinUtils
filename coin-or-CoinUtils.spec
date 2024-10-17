%global		_disable_ld_no_undefined	1
%global		module		CoinUtils

Name:		coin-or-%{module}

Summary:	Coin-or Utilities
Version:	2.9.7
Release:	3%{?dist}
License:	EPL
URL:		https://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
Source1:	%{name}.rpmlintrc
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-Sample
BuildRequires:	doxygen
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

# Properly handle DESTDIR
Patch0:		%{name}-pkgconfig.patch

# Install documentation in standard rpm directory
Patch1:		%{name}-docdir.patch

# Correct undefined non weak symbols
Patch2:		%{name}-underlink.patch

# Correct -Werror=format-security
Patch3:		%{name}-format.patch

%description
CoinUtils (Coin-or Utilities) is an open-source collection of classes
and functions that are generally useful to more than one COIN-OR project.
These utilities include:

  * Vector classes
  * Matrix classes
  * MPS file reading
  * Comparing floating point numbers with a tolerance

%package	devel
Summary:	Development files for %{name}

Requires:	coin-or-Sample
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}

Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export CFLAGS="%{optflags} -Werror=format-security"
export CXXFLAGS="$CFLAGS"
%configure2_5x
make %{?_smp_flags} all doxydoc

%install
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check
make test

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/coinutils_addlibs.txt
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%{_libdir}/*.so.*

%files		devel
%{_includedir}/coin
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Mon Dec 16 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.7-3
- Correct build with -Werror=format-security (#1037021)

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.7-2
- Use proper _smp_flags macro (#894586#c6).
- Make package owner of /usr/include/coin (#894586#c6)

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.7-1
- Update to latest upstream release.

* Wed Aug  7 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.0-3
- Switch to unversioned docdir (#993706)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.9.0-1
- Update to latest upstream release.
- Switch to the new upstream tarballs without bundled dependencies.
- Split documentation in a new subpackage (#894585#3)
- Correct undefined non weak symbols (#894585#3)
- Removed unneeded atlas, blas, glpk and lapack build requires (#894585#3)

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.8-1
- Add coin-or-Sample to build requires (#894610#c4).
- Update to latest upstream release.

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.7-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.7-2
- Rename package to coin-or-CoinUtils
- Do not package Thirdy party data or data without clean license.

* Wed Sep 26 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 2.8.7-1
- Initial coinor-CoinUtils spec.
