# TODO: use system libraries (if possible):
# libjpeg 9c
# libpng 1.6.35
# libtiff 4.0.9+git
# libraw 0.19
# openjpeg 2.1.0+svn
# zlib 1.2.11
# libwebp 1.0.0+git
# LibJXR 1.1+git
# OpenEXR 2.2.1
%define	fver	%(echo %{version} | tr -d .)
Summary:	Library for handling different graphics files formats
Summary(pl.UTF-8):	Biblioteka do manipulacji różnymi formatami plików graficznych
Name:		FreeImage
Version:	3.18.0
Release:	1
License:	GPL and FIPL v1.0 (see the license-fi.txt)
Group:		Libraries
Source0:	http://downloads.sourceforge.net/freeimage/%{name}%{fver}.zip
# Source0-md5:	f8ba138a3be233a3eed9c456e42e2578
Source1:	http://downloads.sourceforge.net/freeimage/%{name}%{fver}.pdf
# Source1-md5:	01d2b93728273caec87f19949fcc4981
URL:		http://freeimage.sourceforge.net/index.html
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	unzip
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
Requires:	libstdc++-devel

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
%setup -q -n %{name}

%build
CFLAGS="%{rpmcflags} -fPIC -fvisibility=hidden" \
CXXFLAGS="%{rpmcxxflags} -fPIC -fvisibility=hidden -Wno-ctor-dtor-privacy" \
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}"

CFLAGS="%{rpmcflags} -fPIC -fvisibility=hidden" \
CXXFLAGS="%{rpmcxxflags} -fPIC -fvisibility=hidden -Wno-ctor-dtor-privacy" \
%{__make} -f Makefile.fip \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install Dist/libfreeimage* $RPM_BUILD_ROOT%{_libdir}
install Dist/*.h $RPM_BUILD_ROOT%{_includedir}

cp -rf Examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -f %{SOURCE1} .

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -sf libfreeimage-%{version}.so \
	$RPM_BUILD_ROOT%{_libdir}/libfreeimage.so
ln -sf libfreeimageplus-%{version}.so \
	$RPM_BUILD_ROOT%{_libdir}/libfreeimageplus.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.linux README.md Whatsnew.txt license-fi.txt
%attr(755,root,root) %{_libdir}/libfreeimage-%{version}.so
%attr(755,root,root) %ghost %{_libdir}/libfreeimage.so.3
%attr(755,root,root) %{_libdir}/libfreeimageplus-%{version}.so
%attr(755,root,root) %ghost %{_libdir}/libfreeimageplus.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreeimage.so
%attr(755,root,root) %{_libdir}/libfreeimageplus.so
%{_includedir}/FreeImage.h
%{_includedir}/FreeImagePlus.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreeimage.a
%{_libdir}/libfreeimageplus.a

%files apidocs
%defattr(644,root,root,755)
%doc FreeImage%{fver}.pdf
