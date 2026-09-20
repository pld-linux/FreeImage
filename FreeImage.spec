#
# Conditional build:
%bcond_without	static_libs	# static library

# require at least bundled versions (except for libjpeg v9d, where we use libjpeg-turbo, which provides v8)
%define		imath_ver	3.1.12
%define		openexr_ver	3.3.13
%define		jxrlib_ver	1.1-0.2019.10.9.2
%define		libdeflate_ver	1.18
%define		libjpeg_ver	8
%define		libpng_ver	2:1.6.39
%define		libtiff_ver	4.6.0
%define		libwebp_ver	1.6.0
%define		libraw_ver	0.21.1
%define		openjp2_ver	2.5.4
%define		zlib_ver	1.3.2

Summary:	Library for handling different graphics files formats
Summary(pl.UTF-8):	Biblioteka do manipulacji różnymi formatami plików graficznych
Name:		FreeImage
Version:	3.19.15
Release:	1
License:	GPL and FIPL v1.0 (see the license-fi.txt)
Group:		Libraries
#Source0Download: https://github.com/danoli3/FreeImage/releases
Source0:	https://github.com/danoli3/FreeImage/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	00748dfb77cf611f1cf92deb9ca83b3b
Source1:	https://downloads.sourceforge.net/freeimage/%{name}3180.pdf
# Source1-md5:	01d2b93728273caec87f19949fcc4981
Patch0:		%{name}-openjp2.patch
Patch1:		%{name}-cmake-with-plus.patch
# original project at https://freeimage.sourceforge.io/ (stopped at 3.18.0), here is maintained fork
URL:		https://github.com/danoli3/FreeImage/releases
BuildRequires:	Imath-devel >= %{imath_ver}
BuildRequires:	OpenEXR-devel >= %{openexr_ver}
BuildRequires:	jxrlib-devel >= %{jxrlib_ver}
BuildRequires:	libdeflate-devel >= %{libdeflate_ver}
BuildRequires:	libjpeg-devel >= %{libjpeg_ver}
BuildRequires:	libpng-devel >= %{libpng_ver}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libtiff-devel >= %{libtiff_ver}
BuildRequires:	libwebp-devel >= %{libwebp_ver}
BuildRequires:	libraw-devel >= %{libraw_ver}
BuildRequires:	openjpeg2-devel >= %{openjp2_ver}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	zlib-devel >= %{zlib_ver}
Requires:	Imath >= %{imath_ver}
Requires:	OpenEXR >= %{openexr_ver}
Requires:	jxrlib >= %{jxrlib_ver}
Requires:	libdeflate >= %{libdeflate_ver}
Requires:	libjpeg >= %{libjpeg_ver}
Requires:	libpng >= %{libpng_ver}
Requires:	libtiff >= %{libtiff_ver}
Requires:	libwebp >= %{libwebp_ver}
Requires:	openjpeg2 >= %{openjp2_ver}
Requires:	zlib >= %{zlib_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FreeImage is a library project for developers who would like to
support popular graphics image formats like PNG, BMP, JPEG, TIFF and
others as needed by multimedia applications. FreeImage is easy to use,
fast, multithreading, safe.

%description -l pl.UTF-8
FreeImage jest projektem biblioteki dla programistów chcących
obsługiwać popularne formaty plików graficznych takie jak PNG, BMP,
JPEG, TIFF i inne wykorzystywane w aplikacjach multimedialnych.
FreeImage jest łatwy w użyciu, szybki, wielowątkowy i bezpieczny.

%package devel
Summary:	Header files for FreeImage library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FreeImage
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Imath-devel >= %{imath_ver}
Requires:	OpenEXR-devel >= %{openexr_ver}
Requires:	jxrlib-devel >= %{jxrlib_ver}
Requires:	libjpeg-devel >= %{libjpeg_ver}
Requires:	libpng-devel >= %{libpng_ver}
Requires:	libstdc++-devel >= 6:7
Requires:	libtiff-devel >= %{libtiff_ver}
Requires:	libwebp-devel >= %{libwebp_ver}
Requires:	openjpeg2-devel >= %{openjp2_ver}
Requires:	zlib-devel >= %{zlib_ver}

%description devel
Header files for FreeImage library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FreeImage.

%package static
Summary:	Static FreeImage library
Summary(pl.UTF-8):	Statyczna biblioteka FreeImage
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FreeImage library.

%description static -l pl.UTF-8
Statyczna biblioteka FreeImage.

%package apidocs
Summary:	Documentation for FreeImage library
Summary(pl.UTF-8):	Dokumentacja do biblioteki FreeImage
Group:		Documentation
BuildArch:	noarch

%description apidocs
Documentation for FreeImage library.

%description apidocs -l pl.UTF-8
Dokumentacja do biblioteki FreeImage.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%if %{with static_libs}
%cmake -B build-static \
	-DBUILD_JXR=ON \
	-DCMAKE_CXX_STANDARD=17 \
	-DFREEIMAGE_STATIC=ON \
	-DFREEIMAGE_USE_SYSTEM_LIBS=ON \
	-DFREEIMAGE_VERSION="%{version}"

%{__make} -C build-static
%endif

%cmake -B build \
	-DBUILD_JXR=ON \
	-DCMAKE_CXX_STANDARD=17 \
	-DFREEIMAGE_USE_SYSTEM_LIBS=ON \
	-DFREEIMAGE_VERSION="%{version}"

%{__make} -C build

%if 0
CFLAGS="%{rpmcflags} -fPIC -fvisibility=hidden" \
CXXFLAGS="%{rpmcxxflags} -fPIC -fvisibility=hidden -Wno-ctor-dtor-privacy" \
%{__make} -f Makefile.fip \
	CC="%{__cc}" \
	CXX="%{__cxx}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}
install -d $RPM_BUILD_ROOT%{_examplesdir}

#install Dist/libfreeimage* $RPM_BUILD_ROOT%{_libdir}
#install Dist/*.h $RPM_BUILD_ROOT%{_includedir}

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -pr Examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p %{SOURCE1} .

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.linux README.md Whatsnew.txt license-fi.txt
%{_libdir}/libfreeimage.so.*.*.*
%ghost %{_libdir}/libfreeimage.so.3
%{_libdir}/libfreeimageplus.so.*.*.*
%ghost %{_libdir}/libfreeimageplus.so.3

%files devel
%defattr(644,root,root,755)
%{_libdir}/libfreeimage.so
%{_libdir}/libfreeimageplus.so
%{_includedir}/FreeImage.h
%{_includedir}/FreeImagePlus.h
%{_libdir}/cmake/FreeImage
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfreeimage.a
%{_libdir}/libfreeimageplus.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc FreeImage3180.pdf
