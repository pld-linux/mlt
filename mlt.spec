#
# TODO:
#	- Newtek NDI SDK support (MOD_NDI): https://www.newtek.com/ndi/sdk/
#	- bconds and module subpackages
#	- more bindings (restore python; add csharp, java, lua, nodejs, perl, php, ruby, tcl)
#	- qt6 (Core,Gui,Xml,SvgWidgets,Core5Compat for MOD_QT6, Core,Gui,Widgets,Xml for MOD_GLAXNIMATE_QT6)
#
# Conditional build:
%bcond_without	opencv	# OpenCV module
#
Summary:	MLT - open source multimedia framework
Summary(pl.UTF-8):	MLT - szkielet multimedialny o otwartych źródłach
Name:		mlt
Version:	7.28.0
Release:	1
License:	GPL v3+ (LGPL v2.1+ code linked with GPL v2/GPL v3 libraries)
Group:		X11/Applications/Multimedia
#Source0Download: https://github.com/mltframework/mlt/releases
Source0:	https://github.com/mltframework/mlt/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	dab096e465078ac5a1d5e1145c14461c
URL:		https://www.mltframework.org/
BuildRequires:	OpenGL-devel
BuildRequires:	Qt6Core-devel >= 5
BuildRequires:	Qt6Gui-devel >= 5
BuildRequires:	Qt6OpenGL-devel >= 5
BuildRequires:	Qt6Svg-devel >= 5
BuildRequires:	Qt6Widgets-devel >= 5
BuildRequires:	Qt6Xml-devel >= 5
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
BuildRequires:	libdv-devel >= 0.102
BuildRequires:	libebur128-devel
BuildRequires:	libexif-devel
#BuildRequires:	libquicktime-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libvorbis-devel >= 1:1.0.1
BuildRequires:	libxml2-devel >= 1:2.5
BuildRequires:	movit-devel
BuildRequires:	ninja
%{?with_opencv:BuildRequires:	opencv-devel >= 3.1.0}
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	rtaudio-devel
BuildRequires:	rubberband-devel
BuildRequires:	sox-devel
#BuildRequires:	spatialaudio-devel
BuildRequires:	swig-python
BuildRequires:	vid.stab-devel >= 0.98
BuildRequires:	which
BuildRequires:	xorg-lib-libX11-devel
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

%package -n python-mlt
Summary:	MLT Python bindings
Summary(pl.UTF-8):	Wiązania MLT dla Pythona
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-mlt
Python bindings for MLT - open source multimedia framework.

%description -n python-mlt -l pl.UTF-8
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
	-DMOD_SPATIALAUDIO=OFF \
	%{?with_opencv:-DMOD_OPENCV=ON}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

#cp -p src/swig/python/{*.py,*.so} $RPM_BUILD_ROOT%{py_sitedir}

#%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
#%py_comp $RPM_BUILD_ROOT%{py_sitedir}
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

#%files -n python-mlt
#%defattr(644,root,root,755)
#%attr(755,root,root) %{py_sitedir}/_mlt.so
#%{py_sitedir}/codecs.py[co]
#%{py_sitedir}/getimage.py[co]
#%{py_sitedir}/mlt.py[co]
#%{py_sitedir}/play.py[co]
#%{py_sitedir}/switcher.py[co]
#%{py_sitedir}/test_animation.py[co]
#%{py_sitedir}/waveforms.py[co]
#%{py_sitedir}/webvfx_generator.py[co]
