%?mingw_package_header

Name:           mingw-postgresql
Version:        9.4.5
Release:        1%{?dist}
Summary:        MinGW Windows PostgreSQL library

License:        PostgreSQL
URL:            http://www.postgresql.org/
Source0:        https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2

# Allow linking to MinGW TCL DLL
Patch0:         postgresql-9.4.0-mingw.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw32-libxslt
BuildRequires:  mingw32-openssl
BuildRequires:  mingw32-tcl
BuildRequires:  mingw32-readline
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gettext
BuildRequires:  mingw64-libxml2
BuildRequires:  mingw64-libxslt
BuildRequires:  mingw64-openssl
BuildRequires:  mingw64-readline
BuildRequires:  mingw64-tcl
BuildRequires:  mingw64-zlib

BuildRequires:  bison flex gettext pkgconfig tcl


%description
MinGW Windows copy of PostgreSQL. PostgreSQL is an advanced Object-Relational
database management system (DBMS).


# Win32
%package -n mingw32-postgresql
Summary:        MinGW Windows PostgreSQL library

%description -n mingw32-postgresql
MinGW Windows copy of PostgreSQL. PostgreSQL is an advanced Object-Relational
database management system (DBMS).

# Win64
%package -n mingw64-postgresql
Summary:        MinGW Windows PostgreSQL library

%description -n mingw64-postgresql
MinGW Windows copy of PostgreSQL. PostgreSQL is an advanced Object-Relational
database management system (DBMS).


%?mingw_debug_package


%prep
%setup -q -n postgresql-%{version}
%patch0 -p1


%build
mkdir build_win32
pushd build_win32
%mingw32_configure \
    --with-openssl \
    --enable-thread-safety \
    --enable-integer-datetimes \
    --enable-nls \
    --with-ldap \
    --with-libxml \
    --with-libxslt \
    --with-tcl --with-tclconfig=/usr/i686-w64-mingw32/sys-root/mingw/lib
popd
mkdir build_win64
pushd build_win64
%mingw64_configure \
    --with-openssl \
    --enable-thread-safety \
    --enable-integer-datetimes \
    --enable-nls \
    --with-ldap \
    --with-libxml \
    --with-libxslt \
    --with-tcl --with-tclconfig=/usr/x86_64-w64-mingw32/sys-root/mingw/lib
popd
# Make DLL definition file visible during each arch build
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/libpq/libpqdll.def ./build_win32/src/interfaces/libpq/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/libpq/libpqdll.def ./build_win64/src/interfaces/libpq/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/ecpglib/libecpgdll.def ./build_win32/src/interfaces/ecpg/ecpglib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/ecpglib/libecpgdll.def ./build_win64/src/interfaces/ecpg/ecpglib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/pgtypeslib/libpgtypesdll.def ./build_win32/src/interfaces/ecpg/pgtypeslib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/pgtypeslib/libpgtypesdll.def ./build_win64/src/interfaces/ecpg/pgtypeslib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/compatlib/libecpg_compatdll.def ./build_win32/src/interfaces/ecpg/compatlib/
ln -s %{_builddir}/%{buildsubdir}/src/interfaces/ecpg/compatlib/libecpg_compatdll.def ./build_win64/src/interfaces/ecpg/compatlib/
%mingw_make %{?_smp_mflags}


%install
%mingw_make install DESTDIR=$RPM_BUILD_ROOT

# move DLLs to bin
mv $RPM_BUILD_ROOT%{mingw32_libdir}/*.dll \
   $RPM_BUILD_ROOT%{mingw32_bindir}
mv $RPM_BUILD_ROOT%{mingw64_libdir}/*.dll \
   $RPM_BUILD_ROOT%{mingw64_bindir}

# due to Fedora packaging policy, delete executables
rm $RPM_BUILD_ROOT%{mingw32_bindir}/*.exe
rm $RPM_BUILD_ROOT%{mingw64_bindir}/*.exe
rm -rf $RPM_BUILD_ROOT%{mingw32_libdir}/postgresql/
rm -rf $RPM_BUILD_ROOT%{mingw64_libdir}/postgresql/

# remove server support files
rm -rf $RPM_BUILD_ROOT%{mingw32_bindir}/pltcl*
rm -rf $RPM_BUILD_ROOT%{mingw64_bindir}/pltcl*
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}

# remove static libraries
rm -rf $RPM_BUILD_ROOT%{mingw32_libdir}/libpgcommon*.a
rm -rf $RPM_BUILD_ROOT%{mingw64_libdir}/libpgcommon*.a

# rename import libraries
mv $RPM_BUILD_ROOT%{mingw32_libdir}/libecpg.a $RPM_BUILD_ROOT%{mingw32_libdir}/libecpg.dll.a
mv $RPM_BUILD_ROOT%{mingw32_libdir}/libecpg_compat.a $RPM_BUILD_ROOT%{mingw32_libdir}/libecpg_compat.dll.a
mv $RPM_BUILD_ROOT%{mingw32_libdir}/libpgport.a $RPM_BUILD_ROOT%{mingw32_libdir}/libpgport.dll.a
mv $RPM_BUILD_ROOT%{mingw32_libdir}/libpgtypes.a $RPM_BUILD_ROOT%{mingw32_libdir}/libpgtypes.dll.a
mv $RPM_BUILD_ROOT%{mingw32_libdir}/libpostgres.a $RPM_BUILD_ROOT%{mingw32_libdir}/libpostgres.dll.a
mv $RPM_BUILD_ROOT%{mingw32_libdir}/libpq.a $RPM_BUILD_ROOT%{mingw32_libdir}/libpq.dll.a
mv $RPM_BUILD_ROOT%{mingw64_libdir}/libecpg.a $RPM_BUILD_ROOT%{mingw64_libdir}/libecpg.dll.a
mv $RPM_BUILD_ROOT%{mingw64_libdir}/libecpg_compat.a $RPM_BUILD_ROOT%{mingw64_libdir}/libecpg_compat.dll.a
mv $RPM_BUILD_ROOT%{mingw64_libdir}/libpgport.a $RPM_BUILD_ROOT%{mingw64_libdir}/libpgport.dll.a
mv $RPM_BUILD_ROOT%{mingw64_libdir}/libpgtypes.a $RPM_BUILD_ROOT%{mingw64_libdir}/libpgtypes.dll.a
mv $RPM_BUILD_ROOT%{mingw64_libdir}/libpostgres.a $RPM_BUILD_ROOT%{mingw64_libdir}/libpostgres.dll.a
mv $RPM_BUILD_ROOT%{mingw64_libdir}/libpq.a $RPM_BUILD_ROOT%{mingw64_libdir}/libpq.dll.a

# Win32
%files -n mingw32-postgresql
%license COPYRIGHT
%{mingw32_bindir}/libecpg.dll
%{mingw32_bindir}/libecpg_compat.dll
%{mingw32_bindir}/libpgtypes.dll
%{mingw32_bindir}/libpq.dll
%{mingw32_includedir}/libpq/
%{mingw32_includedir}/postgresql/
%{mingw32_includedir}/ecpg*.h
%{mingw32_includedir}/libpq-events.h
%{mingw32_includedir}/libpq-fe.h
%{mingw32_includedir}/pg*.h
%{mingw32_includedir}/postgres_ext.h
%{mingw32_includedir}/sql*.h
%{mingw32_libdir}/libecpg.dll.a
%{mingw32_libdir}/libecpg_compat.dll.a
%{mingw32_libdir}/libpgport.dll.a
%{mingw32_libdir}/libpgtypes.dll.a
%{mingw32_libdir}/libpostgres.dll.a
%{mingw32_libdir}/libpq.dll.a
%{mingw32_libdir}/pkgconfig/*.pc


# Win64
%files -n mingw64-postgresql
%license COPYRIGHT
%{mingw64_bindir}/libecpg.dll
%{mingw64_bindir}/libecpg_compat.dll
%{mingw64_bindir}/libpgtypes.dll
%{mingw64_bindir}/libpq.dll
%{mingw64_includedir}/libpq/
%{mingw64_includedir}/postgresql/
%{mingw64_includedir}/ecpg*.h
%{mingw64_includedir}/libpq-events.h
%{mingw64_includedir}/libpq-fe.h
%{mingw64_includedir}/pg*.h
%{mingw64_includedir}/postgres_ext.h
%{mingw64_includedir}/sql*.h
%{mingw64_libdir}/libecpg.dll.a
%{mingw64_libdir}/libecpg_compat.dll.a
%{mingw64_libdir}/libpgport.dll.a
%{mingw64_libdir}/libpgtypes.dll.a
%{mingw64_libdir}/libpostgres.dll.a
%{mingw64_libdir}/libpq.dll.a
%{mingw64_libdir}/pkgconfig/*.pc


%changelog
* Mon Dec 28 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.5-1
- New upstream release.

* Mon Jul 27 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.4-1
- New upstream release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.2-1
- New upstream release.

* Wed Feb 25 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.1-1
- New upstream release.

* Tue Feb 03 2015 Michael Cronenworth <mike@cchtml.com> - 9.4.0-1
- New upstream release.

* Sat Aug 16 2014 Michael Cronenworth <mike@cchtml.com> - 9.3.5-1
- New upstream release.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Michael Cronenworth <mike@cchtml.com> - 9.3.4-1
- New upstream release.

* Thu Mar 06 2014 Michael Cronenworth <mike@cchtml.com> - 9.3.3-1
- New upstream release.

* Tue Jan 07 2014 Michael Cronenworth <mike@cchtml.com> - 9.3.2-1
- New upstream release.

* Mon Oct 28 2013 Michael Cronenworth <mike@cchtml.com> - 9.3.1-1
- Rebase to 9.3 branch.

* Thu Aug 22 2013 Michael Cronenworth <mike@cchtml.com> - 9.2.4-4
- Use upstream patch for Windows error checking

* Thu Aug 15 2013 Michael Cronenworth <mike@cchtml.com> - 9.2.4-3
- Enable NLS, LDAP, TCL, and XML features.
- Patch for Windows error checking (RHBZ# 996529)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Michael Cronenworth <mike@cchtml.com> - 9.2.4-1
- Initial RPM release

