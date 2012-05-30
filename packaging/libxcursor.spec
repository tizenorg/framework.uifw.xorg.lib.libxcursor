Name:       libxcursor
Summary:    X cursor management library
Version:    1.1.11
Release:    2.7
Group:      System/Libraries
License:    MIT
Source0:    libxcursor-%{version}.tar.gz
Source1001: packaging/libxcursor.manifest 
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xproto)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xorg-macros)

%description
Xcursor is a simple library designed to help locate and load cursors for the
X Window System. Cursors can be loaded from files or memory and can exist in
several sizes; the library automatically picks the best size. When using
images loaded from files, Xcursor prefers to use the Render extension's
CreateCursor request for rendering cursors. Where the Render extension is
not supported, Xcursor maps the cursor image to a standard X cursor and uses
the core X protocol CreateCursor request.



%package devel
Summary:    X cursor management library (development files)
Group:      TO_BE/FILLED
Requires:   %{name} = %{version}-%{release}

%description devel
Header files and a static version of the X cursor management library are
provided by this package.
.
See the libxcursor1 package for further information.



%prep
%setup -q -n %{name}-%{version}


%build
cp %{SOURCE1001} .
export LDFLAGS+="-lXrender -lXfixes"
export LDFLAGS+=" -Wl,--hash-style=both -Wl,--as-needed"
#chmod +x autogen.sh
#libtoolize -f -c
./autogen.sh
%configure 

make %{?jobs:-j%jobs}

%install
%make_install
rm -rf %{buildroot}/usr/share/man

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest libxcursor.manifest
/usr/lib/*.so.*


%files devel
%manifest libxcursor.manifest
/usr/include/*
/usr/lib/*.so
/usr/lib/pkgconfig/xcursor.pc

