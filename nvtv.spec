Summary:	NVidia (and others) TV-out tool
Summary(pl):	Narzêdzie do TV-out w kartach firmy NVidia (i innych)
Name:		nvtv
Version:	0.4.7
%define	libver	0.4.7a
Release:	2
License:	GPL v2+
Group:		Applications/System
Source0:	http://dl.sourceforge.net/nv-tv-out/%{name}-%{version}.tar.gz
# Source0-md5:	35348d7608f94b7d114cd6ef46b66fc7
Source1:	http://dl.sourceforge.net/nv-tv-out/libnvtvsimple-%{libver}.tar.gz
# Source1-md5:	8c97d39818dc1e50704d8bb9ba5e7f06
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-opt.patch
URL:		http://www.sourceforge.net/projects/nv-tv-out/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	libtool
BuildRequires:	pciutils-devel
BuildRequires:	pkgconfig
BuildRequires:	xrender-devel
# uses <sys/io.h> interface to setup some adapters
ExclusiveArch:	alpha arm %{ix86} ia64 sh amd64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tool to use the TV-Out capabilities of NVidia graphic cards on Linux.
Now it supports not only NVidia chips.

%description -l pl
Narzêdzie pozwalaj±ce wykorzystaæ pod Linuksem mo¿liwo¶ci TV-Out kart
graficznych NVidia, od niedawna tak¿e innych.

%package -n libnvtvsimple
Summary:	Simple API library for nvtv
Summary(pl):	Prosta biblioteka do nvtv
Group:		Libraries

%description -n libnvtvsimple
This is the simple API library for nvtv, which uses the client backend
to access nvtvd.

%description -n libnvtvsimple -l pl
Ten pakiet zawiera prost± bibliotekê do nvtv, u¿ywaj±c± backendu
klienckiego do dostêpu do nvtvd.

%package -n libnvtvsimple-devel
Summary:	Header file for libnvtvsimple library
Summary(pl):	Plik nag³ówkowy biblioteki libnvtvsimple
Group:		Development/Libraries
Requires:	libnvtvsimple = %{version}-%{release}

%description -n libnvtvsimple-devel
Header file for libnvtvsimple library.

%description -n libnvtvsimple-devel -l pl
Plik nag³ówkowy biblioteki libnvtvsimple.

%package -n libnvtvsimple-static
Summary:	Static libnvtvsimple library
Summary(pl):	Statyczna biblioteka libnvtvsimple
Group:		Development/Libraries
Requires:	libnvtvsimple-devel = %{version}-%{release}

%description -n libnvtvsimple-static
Static libnvtvsimple library.

%description -n libnvtvsimple-static -l pl
Statyczna biblioteka libnvtvsimple.

%prep
%setup -q -b1
%patch0 -p1

%build
cp -f /usr/share/automake/config.* .
mv -f aclocal.m4 acinclude.m4
%{__aclocal}
%{__autoconf}
%configure \
	%{!?debug:--disable-debug} \
	--with-gtk=gtk2

%{__make}

cd lib
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sbindir},%{_bindir},%{_mandir}/man{1,8}}

%{__make} -C lib install \
	DESTDIR=$RPM_BUILD_ROOT

install src/nvtvd $RPM_BUILD_ROOT%{_sbindir}
install src/nvtv $RPM_BUILD_ROOT%{_bindir}
install man/nvtv.1x $RPM_BUILD_ROOT%{_mandir}/man1/nvtv.1
install man/nvtvd.8 $RPM_BUILD_ROOT%{_mandir}/man8/nvtvd.8
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/nvtv
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/nvtv

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add nvtv
if [ -f /var/lock/subsys/nvtv ]; then
	/etc/rc.d/init.d/nvtv restart >&2
else
	echo "Run \"/etc/rc.d/init.d/nvtv start\" to start NvTV daemon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/nvtv ]; then
		/etc/rc.d/init.d/nvtv stop >&2
	fi
	/sbin/chkconfig --del nvtv
fi

%post	-n libnvtvsimple -p /sbin/ldconfig
%postun	-n libnvtvsimple -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ANNOUNCE BUGS ChangeLog FAQ README TODO doc/USAGE doc/*.txt
%attr(754,root,root) /etc/rc.d/init.d/nvtv
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/nvtv
%attr(755,root,root) %{_bindir}/nvtv
%attr(755,root,root) %{_sbindir}/nvtvd
%{_mandir}/man1/nvtv.1*
%{_mandir}/man8/nvtvd.8*

%files -n libnvtvsimple
%defattr(644,root,root,755)
%doc lib/README
%attr(755,root,root) %{_libdir}/libnvtvsimple.so.*.*.*

%files -n libnvtvsimple-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnvtvsimple.so
%{_libdir}/libnvtvsimple.la
%{_includedir}/nvtv
%{_pkgconfigdir}/nvtvsimple.pc

%files -n libnvtvsimple-static
%defattr(644,root,root,755)
%{_libdir}/libnvtvsimple.a
