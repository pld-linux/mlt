#
# TODO:
# - bconds
# - currently avformat support is broken, the hell knows why
#
Summary:	MLT - open source multimedia framework
Summary(pl.UTF-8):	MLT - szkielet multimedialny o otwartych źródłach
Name:		mlt
Version:	0.2.2
Release:	0.2
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/mlt/%{name}-%{version}.tar.gz
# Source0-md5:	9d4a3d308b1314a117f692766fb15e90
URL:		http://www.dennedy.org/mlt/twiki/bin/view/MLT/WebHome
Patch0:		mlt-sox.patch
Patch1:		mlt-linuxppc.patch
BuildRequires:	SDL-devel
#BuildRequires:	ffmpeg-devel
BuildRequires:	gtk+2-devel
BuildRequires:	ladspa-devel
BuildRequires:	lame-libs-devel
BuildRequires:	libdv-devel >= 0.102
BuildRequires:	libmad-devel
BuildRequires:	libquicktime-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libvorbis-devel >= 1:1.0.1
BuildRequires:	libxml2-devel >= 2.5
BuildRequires:	pkgconfig
BuildRequires:	qt-devel
BuildRequires:	sox-devel
BuildRequires:	which
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
Requires:	mlt

%description devel
This package contains header files for MLT.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe dla MLT.

%prep
%setup -q
%patch0 -p0

%ifarch ppc ppc64
%patch1 -p1
%endif

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
	--qimage-includedir=%{_includedir}/qt \
	--qimage-libdir=%{_libdir}
	
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so*
%{_datadir}/mlt*

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/*.pc
%{_includedir}/mlt*
