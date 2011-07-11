Summary: Revision Control System (RCS) file version management tools
Name: rcs
Version: 5.7
Release: 37%{?dist}
License: GPLv2+
Group: Development/Tools
URL: http://www.gnu.org/software/rcs/
Source: ftp://ftp.gnu.org/gnu/rcs/%{name}-%{version}.tar.gz
Patch0: rcs-5.7-build-tweaks.patch
Patch1: rcs-5.7-security.patch
Patch2: rcs-5.7-sameuserlocks.patch
Patch3: rcs-5.7-option.patch
Patch4: rcs-5.7-newsvnsyntax.patch
Patch5: rcs-5.7-DESTDIR.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: autoconf
BuildRequires: groff
BuildRequires: ghostscript
BuildRequires: sendmail
BuildRequires: ed
Requires: diffutils

%description
The Revision Control System (RCS) is a system for managing multiple
versions of files.  RCS automates the storage, retrieval, logging,
identification and merging of file revisions.  RCS is useful for text
files that are revised frequently (for example, programs,
documentation, graphics, papers and form letters).

The rcs package should be installed if you need a system for managing
different versions of files.

%package docs
Summary:	Documentation for Revision Control System (RCS)
Group:		Development/Tools
BuildArch:      noarch
Requires:	%{name} = %{version}-%{release}

%description docs
Additional pdf documentation for Revision Control System (RCS).

%prep
%setup -q
%patch0 -p1 -b .debiantweaks
%patch1 -p1 -b .security
%patch2 -p1 -b .sameuserlocks
%patch3 -p1 -b .option
%patch4 -p1 -b .newsvnsyntax
%patch5 -p1 -b .DESTDIR
autoconf

%build
%configure --with-diffutils
make %{?_smp_mflags}
for f in rcs rcs_func ; do
    groff -p -Tps -ms $f.ms | ps2pdf - $f.pdf
done

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

%check
# hack: make path to "co" relative in order to test the built one; the real
# executables were already installed out of the way in %%install
sed -i -e 's|"%{_bindir}/co"|"co"|' src/conf.h ; make %{?_smp_mflags} -C src
PATH="`pwd`/src:${PATH}" make installdebug
# ...and hack it back for sources in -debuginfo
sed -i -e 's|"co"|"%{_bindir}/co"|' src/conf.h

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING CREDITS NEWS README REFS
%{_bindir}/*
%{_mandir}/man[15]/*

%files docs
%defattr(-,root,root,-)
%doc rcs_func.pdf rcs.pdf


%changelog
* Tue Jun 22 2010 Ondrej Vasik <ovasik@redhat.com> - 5.7-37
- ship generated documentation in doc subpackage(#605108)

* Tue Jan 11 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 5.7-36
- fixes based on review
- Add dependency on diffutils.
- Apply build tweaks patch from Debian (incl installing rcsfreeze).
- BuildRequire autoconf instead of automake.
- Actually configure instead of shipping a pregenerated conf.h (#226356).
- Ship docs as PDF rather than troff source.
- Run test suite during build.
- Include COPYING.
- Resolves: #543948

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 5.7-35.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.7-33
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.7-32
- Autorebuild for GCC 4.3

* Tue Jul 17 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 5.7-31
- Addded support for new svn syntax.
- Resolves: #247998

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.7-30.1
- rebuild

* Mon Jun 12 2006 Jesse Keating <jkeating@redhat.com> - 5.7-30
- Add missing BR automake

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.7-29.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.7-29.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 10 2005 Phil Knirsch <pknirsch@redhat.com> 5.7-29
- Fixed bug with obsolete and changed -u option for diff (#165071)

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 5.7-28
- bump release and rebuild with gcc 4

* Sun Feb 13 2005 Florian La Roche <laroche@redhat.com> 5.7-27
- add spec change from #144485

* Tue Sep 21 2004 Phil Knirsch <pknirsch@redhat.com> 5.7-26
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 5.7-25
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 5.7-24
- rebuilt

* Wed Feb 04 2004 Phil Knirsch <pknirsch@redhat.com> 5.7-23
- Switched copyright to license. :-)

* Fri Oct 31 2003 Phil Knirsch <pknirsch@redhat.com> 5.7-22
- Included sameuserlocks patch from James Olin Oden (#107947).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 5.7-19
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Jan 05 2001 Preston Brown <pbrown@redhat.com>
- tmpfile security patch from Olaf Kirch <okir@lst.de>

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed the spec file; added BuildRoot

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
-built against glibc
