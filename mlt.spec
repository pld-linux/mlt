#
# TODO:
# - bconds
# - currently avformat support is broken, the hell knows why
#
Summary:	MLT
Summary(pl):	MLT
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
BuildRequires:	libdv-devel >= 0.102
BuildRequires:	libsamplerate-devel
BuildRequires:	libvorbis-devel >= 1.0.1
BuildRequires:	libxml2-devel >= 2.5
BuildRequires:	quicktime4linux-devel
BuildRequires:	sox-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MLT is an open source multimedia framework, designed and developed for
television broadcasting. It provides a toolkit for broadcasters, video
editors, media players, transcoders, web streamers and many more types
of applications. The functionality of the system is provided via an
assortment of ready to use tools, xml authoring components, and an
extendible plug-in based API.

#%description -l pl

%package devel
Summary:        Header files for MLT
Summary(pl):    Pliki nag³ówkowe dla MLT
Group:          Development/Libraries

%description devel
Header files for MLT

#%description devel -l pl

%prep
%setup -q

%build
%configure \
	--disable-avformat
%{__make}
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

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
%{_libdir}/pkgconfig/*.pc
%{_includedir}/mlt*
