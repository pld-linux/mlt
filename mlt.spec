#
# TODO:
#	- bconds
#	- more bindings
#
Summary:	MLT - open source multimedia framework
Summary(pl.UTF-8):	MLT - szkielet multimedialny o otwartych źródłach
Name:		mlt
Version:	0.8.2
Release:	2
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://downloads.sourceforge.net/mlt/%{name}-%{version}.tar.gz
# Source0-md5:	c7a8c4ca7485bb615cbcf851d8742a1c
URL:		http://www.mltframework.org/
Patch0:		%{name}-linuxppc.patch
Patch1:		ffmpeg10.patch
BuildRequires:	QtGui-devel
BuildRequires:	QtSvg-devel
BuildRequires:	QtXml-devel
BuildRequires:	SDL-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	gtk+2-devel
#BuildRequires:	ladspa-devel
#BuildRequires:	lame-libs-devel
BuildRequires:	libdv-devel >= 0.102
#BuildRequires:	libmad-devel
BuildRequires:	libquicktime-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libvorbis-devel >= 1:1.0.1
BuildRequires:	libxml2-devel >= 2.5
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sox-devel
BuildRequires:	swig-python
BuildRequires:	which
Obsoletes:	mlt++ < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MLT is an open source multimedia framework, designed and developed for
television broadcasting. It provides a toolkit for broadcasters, video
editors, media players, transcoders, web streamers and many more types
of applications. The functionality of the system is provided via an
assortment of ready to use tools, XML authoring components, and an
extendible plug-in based API.

%description -l pl.UTF-8
MLT to szkielet multimedialny o otwartych źródłach zaprojektowany i
rozwijany do nadawania telewizji. Udostępnia zestaw narzędzi dla
nadawców, edytory obrazu, odtwarzacze mediów, transkodery, narzędzia
do udostępniania strumieni przez WWW i wiele innych rodzajów
aplikacji. Funkcjonalność systemu jest zapewniona poprzez asortyment
gotowych do użycia narzędzi, komponentów do tworzenia XML-a i
rozszerzalne API oparte na wtyczkach.

%package -n python-mlt
Summary:	MLT Python bindings
Summary(pl.UTF-8):	Wiązania MLT dla Pythona
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-mlt
Python bindings for MLT - open source multimedia framework.

%package devel
Summary:	Header files for MLT
Summary(pl.UTF-8):	Pliki nagłówkowe dla MLT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	mlt++-devel < %{version}

%description devel
This package contains header files for MLT.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe dla MLT.

%prep
%setup -q
%ifarch ppc ppc64
%patch0 -p1
%endif
%patch1 -p1

%build
%configure \
	--enable-gpl \
%ifarch %{x8664}
	--disable-motion-est \
%else
	--enable-motion-est \
%endif
	--disable-debug \
%ifarch i586 i686 %{x8664}
	--disable-mmx \
%else
	--enable-mmx \
%endif
	--disable-sse2 \
	--avformat-swscale \
	--qimage-includedir=%{_includedir}/qt4 \
	--qimage-libdir=%{_libdir} \
	--swig-languages=python

%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install src/swig/python/{*.py,*.so} $RPM_BUILD_ROOT%{py_sitedir}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %ghost %{_libdir}/*.so.?
%attr(755,root,root) %{_libdir}/*.so.*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_datadir}/mlt*

%files -n python-mlt
%defattr(644,root,root,755)
%{py_sitedir}/*.py[co]
%attr(755,root,root) %{py_sitedir}/*.so

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/*.pc
%{_includedir}/mlt*
%{_libdir}/*.so
