Summary:	NVidia tv-out tool
Name:		nvtv
Version:	0.4.3
Release:	0.9
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.sourceforge.net/projects/nv-tv-out/
BuildRequires:	autoconf
BuildRequires:	gtk+-devel
BuildRequires:	pciutils-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tool to use the TV-Out capabilities of NVidia graphic cards on Linux.

%prep
%setup -q -n %{name}

%build
mv -f aclocal.m4 acinclude.m4
%{__aclocal}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sbindir},%{_mandir}/man{1,8}}

install src/nvtv* $RPM_BUILD_ROOT%{_sbindir}
install doc/man/nvtv.1x $RPM_BUILD_ROOT%{_mandir}/man1/nvtv.1
install doc/man/nvtvd.8 $RPM_BUILD_ROOT%{_mandir}/man8/nvtvd.8
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
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
