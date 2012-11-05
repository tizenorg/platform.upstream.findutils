Name:           findutils
Url:            http://www.gnu.org/software/findutils/
Version:        4.5.10
Release:        0
Summary:        The GNU versions of find utilities (find and xargs)
License:        GPL-3.0+
Group:          Productivity/File utilities
# retrieved from http://alpha.gnu.org/pub/gnu/findutils/findutils-4.5.10.tar.gz
Source:         findutils-%{version}.tar.bz2
Source1:        sysconfig.locate

%description
The findutils package contains programs which will help you locate
files on your system.  The find utility searches through a hierarchy
of directories looking for files which match a certain set of criteria
(such as a file name pattern).  The xargs utility builds and executes
command lines from standard input arguments (usually lists of file
names generated by the find command).

You should install findutils because it includes tools that are very
useful for finding things on your system.


%lang_package
%package locate
Summary:        Tool for Locating Files (findutils subpackage)
Group:          Productivity/File utilities
Provides:       findutils:/usr/bin/locate
Requires:       findutils = %{version}

%description locate
This package contains the locate program which is part of the GNU
findutils software suite.

You can find files fast using locate.  On installing findutils-locate
an additional daily cron job will be added to the cron system. This
job will update the files database every night or shortly after
switching on the computer.

%prep
%setup -q

%build
%ifarch %arm armv5tel armv7l armv7el armv5el
# this is a workaround for a qemu-user bug, we hit. A qemu patch is being discussed, but for now ...
export DEFAULT_ARG_SIZE="(31u * 1024u)"
%endif
%configure \
  --libexecdir=%{_libdir}/find \
  --localstatedir=/var/lib \
  --without-included-regex \
  --without-fts \
  --enable-d_type-optimisation
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/locate
rm -f $RPM_BUILD_ROOT%{_bindir}/oldfind
rm -f $RPM_BUILD_ROOT%{_bindir}/ftsfind
rm -f $RPM_BUILD_ROOT%{_infodir}/find-maint*
%find_lang %{name}

%docs_package

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/find
%{_bindir}/xargs

%files locate
%defattr(-,root,root,-)
%{_bindir}/locate
%{_bindir}/updatedb
%{_libdir}/find
%config(noreplace) %{_sysconfigdir}/sysconfig/locate

%changelog
