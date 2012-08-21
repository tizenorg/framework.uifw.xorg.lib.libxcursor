Summary: Cursor management library
Name: libXcursor
Version: 1.1.13
Release: 1
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
#VCS: git:git://anongit.freedesktop.org/xorg/lib/libXcursor
Source0: %{name}-%{version}.tar.gz

BuildRequires: xorg-x11-xutils-dev
BuildRequires:  pkgconfig(xorg-macros)
BuildRequires:  pkgconfig(xproto)
BuildRequires: libX11-devel
BuildRequires: libXfixes-devel
BuildRequires: libXrender-devel >= 0.8.2


%description
This is  a simple library designed to help locate and load cursors.
Cursors can be loaded from files or memory. A library of common cursors
exists which map to the standard X cursor names.Cursors can exist in
several sizes and the library automatically picks the best size.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Provides: libxcursor-devel 
Requires: %{name} = %{version}-%{release}

%description devel
libXcursor development package.

%prep
%setup -q
iconv --from=ISO-8859-2 --to=UTF-8 COPYING > COPYING.new && \
touch -r COPYING COPYING.new && \
mv COPYING.new COPYING

# Disable static library creation by default.
%define with_static 0

%build
#export CFLAGS="${CFLAGS} $RPM_OPT_FLAGS -DICONDIR=\"%{_datadir}/icons\""
%reconfigure --disable-static \
           LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"
make %{?jobs:-j%jobs}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/default

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/libXcursor.so.1
%{_libdir}/libXcursor.so.1.0.2
%dir %{_datadir}/icons/default
#%{_datadir}/icons/default/index.theme

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11/Xcursor
%{_includedir}/X11/Xcursor/Xcursor.h
%if %{with_static}
%{_libdir}/libXcursor.a
%endif
%{_libdir}/libXcursor.so
%{_libdir}/pkgconfig/xcursor.pc
#%dir %{_mandir}/man3x
#%{_mandir}/man3/Xcursor*.3*