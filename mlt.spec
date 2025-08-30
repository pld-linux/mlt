#
# TODO:
#	- Newtek NDI SDK support (MOD_NDI): https://www.newtek.com/ndi/sdk/
#	- bconds and module subpackages
#	- more bindings (restore python; add csharp, java, lua, nodejs, perl, php, ruby, tcl)
#
# Conditional build:
%bcond_without	opencv		# OpenCV module
%bcond_with	spatialaudio	# SpatialAudio support (needs > 0.3.0?)
%bcond_without	python3		# Python (3.x) binding
#
%define	qt6_ver	6.8.2
Summary:	MLT - open source multimedia framework
Summary(pl.UTF-8):	MLT - szkielet multimedialny o otwartych źródłach
Name:		mlt
Version:	7.32.0
Release:	2
License:	GPL v3+ (LGPL v2.1+ code linked with GPL v2/GPL v3 libraries)
Group:		X11/Applications/Multimedia
#Source0Download: https://github.com/mltframework/mlt/releases
Source0:	https://github.com/mltframework/mlt/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d8ade248452e023366f4a0e3d20612ca
URL:		https://www.mltframework.org/
BuildRequires:	OpenGL-devel
BuildRequires:	Qt6Core-devel >= %{qt6_ver}
BuildRequires:	Qt6DBus-devel >= %{qt6_ver}
BuildRequires:	Qt6Gui-devel >= %{qt6_ver}
BuildRequires:	Qt6Network-devel >= %{qt6_ver}
BuildRequires:	Qt6OpenGL-devel >= %{qt6_ver}
BuildRequires:	Qt6Qt5Compat-devel >= %{qt6_ver}
BuildRequires:	Qt6Svg-devel >= %{qt6_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt6_ver}
BuildRequires:	Qt6Xml-devel >= %{qt6_ver}
BuildRequires:	SDL-devel >= 1.2
BuildRequires:	SDL2-devel >= 2
BuildRequires:	SDL_image-devel
BuildRequires:	cmake >= 3.14
# libavcodec libavdevice libavfilter >= 4.11.100 libavformat libavutil libswscale
BuildRequires:	ffmpeg-devel >= 2.3
BuildRequires:	fftw3-devel >= 3
BuildRequires:	fontconfig-devel
BuildRequires:	frei0r-devel
BuildRequires:	gcc >= 6:4.7
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	ladspa-devel
BuildRequires:	libarchive-devel >= 0.102
BuildRequires:	libdv-devel >= 0.102
BuildRequires:	libebur128-devel
BuildRequires:	libexif-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libvorbis-devel >= 1:1.0.1
BuildRequires:	libxml2-devel >= 1:2.5
BuildRequires:	lilv-devel
BuildRequires:	movit-devel
BuildRequires:	ninja
%{?with_opencv:BuildRequires:	opencv-devel >= 3.1.0}
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	rtaudio-devel
BuildRequires:	rubberband-devel
BuildRequires:	sox-devel
%{?with_spatialaudio:BuildRequires:	spatialaudio-devel > 0.3.0}
%{?with_python3:BuildRequires:	swig-python >= 2}
BuildRequires:	vid.stab-devel >= 0.98
BuildRequires:	which
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.5.0
Requires:	xorg-lib-libxkbcommon >= 0.5.0
Obsoletes:	mlt++ < 0.4
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

%package devel
Summary:	Header files for MLT
Summary(pl.UTF-8):	Pliki nagłówkowe dla MLT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	mlt++-devel < 0.4

%description devel
This package contains header files for MLT.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe dla MLT.

%package -n python3-mlt
Summary:	MLT Python bindings
Summary(pl.UTF-8):	Wiązania MLT dla Pythona
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python-mlt < 7

%description -n python3-mlt
Python bindings for MLT - open source multimedia framework.

%description -n python3-mlt -l pl.UTF-8
Wiązadania Pythona do MLT - szkieletu multimedialnego o otwartych
źródłach.

%prep
%setup -q

%build
%cmake -B build \
	-G Ninja \
	-DMOD_GLAXNIMATE_QT6=ON \
	-DMOD_GLAXNIMATE=OFF \
	-DMOD_QT6=ON \
	-DMOD_QT=OFF \
	%{!?with_spatialaudio:-DMOD_SPATIALAUDIO=OFF} \
	%{?with_opencv:-DMOD_OPENCV=ON} \
	%{?with_python3:-DSWIG_PYTHON=ON}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

#cp -p src/swig/python/{*.py,*.so} $RPM_BUILD_ROOT%{py_sitedir}

%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
#%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/melt
%attr(755,root,root) %{_bindir}/melt-7
%attr(755,root,root) %{_libdir}/libmlt-7.so.*.*.*
%ghost %{_libdir}/libmlt-7.so.7
%attr(755,root,root) %{_libdir}/libmlt++-7.so.*.*.*
%ghost %{_libdir}/libmlt++-7.so.7
%dir %{_libdir}/%{name}-7
%attr(755,root,root) %{_libdir}/%{name}-7/libmlt*.so
%{_datadir}/mlt-7
%{_mandir}/man1/melt-7.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmlt-7.so
%{_libdir}/libmlt++-7.so
%{_libdir}/cmake/Mlt7
%{_includedir}/mlt-7
%{_pkgconfigdir}/mlt-framework-7.pc
%{_pkgconfigdir}/mlt++-7.pc

%if %{with python3}
%files -n python3-mlt
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_mlt7.so
%{py3_sitedir}/mlt7.py
%{py3_sitedir}/__pycache__/mlt7.cpython-*.py[co]
%endif
