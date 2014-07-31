# TODO: use system libraries (if possible):
# libjpeg 9a
# libpng 1.6.10
# libtiff 4.0.3+CVS
# libraw 0.16.0
# openjpeg 2.1.0+svn
# zlib 1.2.8
# libwebp 0.4.0+git
# LibJXR 1.1+git
# OpenEXR 1.7.1
%define	fver	%(echo %{version} | tr -d .)
Summary:	Library for handling different graphics files formats
Summary(pl.UTF-8):	Biblioteka do manipulacji różnymi formatami plików graficznych
Name:		FreeImage
Version:	3.16.0
Release:	1
License:	GPL and FIPL v1.0 (see the license-fi.txt)
Group:		Libraries
Source0:	http://downloads.sourceforge.net/freeimage/%{name}%{fver}.zip
# Source0-md5:	1a2d1fff6204adbd479cc98818892fc1
Source1:	http://downloads.sourceforge.net/freeimage/%{name}%{fver}.pdf
# Source1-md5:	f8df04e0c5fb7a9af850a23df7ac244e
Patch0:		%{name}-includes.patch
URL:		http://freeimage.sourceforge.net/index.html
BuildRequires:	libstdc++-devel
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

%prep
%setup -q -n %{name}
%patch0 -p1

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
%doc README.linux Whatsnew.txt license-fi.txt
%attr(755,root,root) %{_libdir}/libfreeimage-*.*.*.so
%attr(755,root,root) %ghost %{_libdir}/libfreeimage.so.3
%attr(755,root,root) %{_libdir}/libfreeimageplus-*.*.*.so
%attr(755,root,root) %ghost %{_libdir}/libfreeimageplus.so.3

%files devel
%defattr(644,root,root,755)
%doc FreeImage%{fver}.pdf
%attr(755,root,root) %{_libdir}/libfreeimage.so
%attr(755,root,root) %{_libdir}/libfreeimageplus.so
%{_includedir}/FreeImage.h
%{_includedir}/FreeImagePlus.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreeimage.a
%{_libdir}/libfreeimageplus.a
