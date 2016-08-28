#
# TODO:
#	- bconds
#	- more bindings
#	- movit library - http://libregraphicsworld.org/blog/entry/introducing-movit-free-library-for-gpu-side-video-processing
#
Summary:	MLT - open source multimedia framework
Summary(pl.UTF-8):	MLT - szkielet multimedialny o otwartych źródłach
Name:		mlt
Version:	6.2.0
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://downloads.sourceforge.net/mlt/%{name}-%{version}.tar.gz
# Source0-md5:	cdbc5d1d686b75dd2b8fd14059bdd9d4
Patch0:		%{name}-qt5.patch
URL:		http://www.mltframework.org/
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Svg-devel
BuildRequires:	Qt5Xml-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	exiv2-devel
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
BuildRequires:	swfdec-devel
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
%patch0 -p1

# Don't overoptimize (breaks debugging)
sed -i -e '/fomit-frame-pointer/d' configure
sed -i -e '/ffast-math/d' configure

%build
%configure \
	--enable-gpl \
	--enable-gpl3 \
	--enable-motion-est \
	--disable-debug \
%ifarch i586 i686 %{x8664}
	--enable-mmx \
%else
	--disable-mmx \
%endif
%ifarch %{x8664}
	--enable-sse \
	--enable-sse2 \
%else
	--disable-sse \
	--disable-sse2 \
%endif
	--swig-languages=python

sed -i -e 's#OPTIMISATIONS=#OPTIMISATIONS=%{rpmcflags} %{rpmcppflags}#g' config.mak

%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p src/swig/python/{*.py,*.so} $RPM_BUILD_ROOT%{py_sitedir}

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
