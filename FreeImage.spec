%define	_ver	%(echo %{version} | tr -d .)
Summary:	Library for handling different graphics files formats
Summary(pl.UTF-8):	Biblioteka do manipulacji różnymi formatami plików graficznych
Name:		FreeImage
Version:	3.9.3
Release:	1
License:	GPL and FIPL (see the license-fi.txt)
Group:		Libraries
Source0:	http://dl.sourceforge.net/freeimage/%{name}%{_ver}.zip
# Source0-md5:	bf3574fa4e6135cf511d5ff4bc871ec3
Source1:	http://dl.sourceforge.net/freeimage/%{name}%{_ver}.pdf
# Source1-md5:	5a59f1d2c380da666f1cd42e082e8041
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

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	COMPILERFLAGS="%{rpmcflags} -fPIC"

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
%doc FreeImage%{_ver}.pdf
%attr(755,root,root) %{_libdir}/libfreeimage.so
%{_includedir}/FreeImage.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreeimage.a
