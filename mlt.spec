#
# TODO:
# - bconds
# - currently avformat support is broken, the hell knows why
#
Summary:	MLT - open source multimedia framework
Summary(pl):	MLT - szkielet multimedialny o otwartych �r�d�ach
Name:		mlt
Version:	0.2.2
Release:	0.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/mlt/%{name}-%{version}.tar.gz
# Source0-md5:	9d4a3d308b1314a117f692766fb15e90
URL:		http://www.dennedy.org/mlt/twiki/bin/view/MLT/WebHome
BuildRequires:	SDL-devel
BuildRequires:	bluefish
#BuildRequires:	ffmpeg-devel
BuildRequires:	gtk+2-devel
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

%description -l pl
MLT to szkielet multimedialny o otwartych �r�d�ach zaprojektowany i
rozwijany do nadawania telewizji. Udost�pnia zestaw narz�dzi dla
nadawc�w, edytory obrazu, odtwarzacze medi�w, transkodery, narz�dzia
do udost�pniania strumieni przez WWW i wiele innych rodzaj�w
aplikacji. Funkcjonalno�� systemu jest zapewniona poprzez asortyment
gotowych do u�ycia narz�dzi, komponent�w do tworzenia XML-a i
rozszerzalne API oparte na wtyczkach.

%package devel
Summary:	Header files for MLT
Summary(pl):	Pliki nag��wkowe dla MLT
Group:		Development/Libraries
Requires:	mlt

%description devel
This package contains header files for MLT.

%description devel -l pl
Ten pakiet zawiera pliki nag��wkowe dla MLT.

%prep
%setup -q

%build
%configure \
	--disable-avformat \
	--enable-gpl \
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
