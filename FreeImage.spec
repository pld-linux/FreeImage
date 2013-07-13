# TODO: use system libraries (if possible)
%define	fver	%(echo %{version} | tr -d .)
Summary:	Library for handling different graphics files formats
Summary(pl.UTF-8):	Biblioteka do manipulacji różnymi formatami plików graficznych
Name:		FreeImage
Version:	3.15.4
Release:	1
License:	GPL and FIPL v1.0 (see the license-fi.txt)
Group:		Libraries
Source0:	http://downloads.sourceforge.net/freeimage/%{name}%{fver}.zip
# Source0-md5:	9f9a3b2c3c1b4fd24fe479e8aaee86b1
Source1:	http://downloads.sourceforge.net/freeimage/%{name}%{fver}.pdf
# Source1-md5:	acfbb9bcf5f5ee5ab77824c666a39a15
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
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS='%{rpmcflags} -fPIC -fvisibility=hidden -DNO_LCMS $(INCLUDE)' \
	CXXFLAGS='%{rpmcxxflags} -fPIC -fvisibility=hidden -Wno-ctor-dtor-privacy $(INCLUDE)'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install Dist/libfreeimage* $RPM_BUILD_ROOT%{_libdir}
install Dist/*.h $RPM_BUILD_ROOT%{_includedir}

cp -rf Examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -f %{SOURCE1} .

ln -sf libfreeimage-%{version}.so \
	$RPM_BUILD_ROOT%{_libdir}/libfreeimage.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.linux Whatsnew.txt license-fi.txt
%attr(755,root,root) %{_libdir}/libfreeimage-*.*.*.so

%files devel
%defattr(644,root,root,755)
%doc FreeImage%{fver}.pdf
%attr(755,root,root) %{_libdir}/libfreeimage.so
%{_includedir}/FreeImage.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreeimage.a
