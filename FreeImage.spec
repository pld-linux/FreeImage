Summary:	Library for handling different graphics files formats
Summary(pl.UTF-8):	Biblioteka do manipulacji różnymi formatami plików graficznych
Name:		FreeImage
Version:	3.9.2
Release:	1
License:	GPL and FIPL (see the license-fi.txt)
Group:		Libraries
Source0:	http://dl.sourceforge.net/freeimage/%{name}392.zip
# Source0-md5:	e7a3e2429a0db52fb377bed7da61e5a5
Source1:	http://dl.sourceforge.net/freeimage/%{name}392.pdf
# Source1-md5:	ecbc9eedf5b4e04495deaaee8935c0fd
URL:		http://freeimage.sourceforge.net/index.html
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FreeImage is a library project for developers who would like to
support popular graphics image formats like PNG, BMP, JPEG, TIFF and
others as needed by multimedia applications. FreeImage is easy to use,
fast, multithreading, safe.

%description -l pl.UTF-8
FreeImage jest projektem biblioteki dla deweloperów, którzy chcą
wspierać popularne formaty plików graficznych takie jak PNG, BMP,
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
	COMPILERFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install Dist/libfreeimage* $RPM_BUILD_ROOT%{_libdir}
install Dist/*.h $RPM_BUILD_ROOT%{_includedir}

cp -rf Examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -f %{SOURCE1} .

cd Dist
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
%doc FreeImage392.pdf
%attr(755,root,root) %{_libdir}/libfreeimage.so
%{_includedir}/*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
