Summary:	NVidia TV-out tool
Summary(pl):	Narzêdzie do TV-out w kartach firmy NVidia
Name:		nvtv
Version:	0.4.6
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/nv-tv-out/%{name}-%{version}.tar.gz
# Source0-md5:	1ca0b59ab730e95e7dee0606efe73446
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-pipe.patch
URL:		http://www.sourceforge.net/projects/nv-tv-out/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+-devel
BuildRequires:	pciutils-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tool to use the TV-Out capabilities of NVidia graphic cards on Linux.

%description -l pl
Narzêdzie pozwalaj±ce wykorzystaæ pod Linuksem mo¿liwo¶ci TV-Out kart
graficznych NVidia.

%prep
%setup -q

%build
mv -f aclocal.m4 acinclude.m4
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sbindir},%{_bindir},%{_mandir}/man{1,8}}

install src/nvtvd $RPM_BUILD_ROOT%{_sbindir}
install src/nvtv $RPM_BUILD_ROOT%{_bindir}
install man/nvtv.1x $RPM_BUILD_ROOT%{_mandir}/man1/nvtv.1
install man/nvtvd.8 $RPM_BUILD_ROOT%{_mandir}/man8/nvtvd.8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/nvtv
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/nvtv

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

%files
%defattr(644,root,root,755)
%doc ANNOUNCE BUGS ChangeLog FAQ README TODO doc/USAGE doc/*.txt
%attr(754,root,root) /etc/rc.d/init.d/nvtv
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/nvtv
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man*/*
