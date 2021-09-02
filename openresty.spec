Name:           openresty
Version:        1.19.3.1
Release:        1%{?dist}
Summary:        OpenResty, scalable web platform by extending NGINX with Lua

Group:          System Environment/Daemons

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        BSD
URL:            https://openresty.org/

Source0:        https://openresty.org/download/openresty-%{version}.tar.gz

%if 0%{?amzn} >= 2 || 0%{?suse_version} || 0%{?fedora} || 0%{?rhel} >= 7
%define         use_systemd   1
%endif

Source1:        openresty.service
Source2:        openresty.init

Patch1:		0001-add-option-out-dir-on-configure.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-File-Temp
BuildRequires:  ccache, gcc, make, perl, systemtap-sdt-devel
BuildRequires:  openresty-zlib-devel >= 1.2.11-3
BuildRequires:  openresty-openssl111-devel >= 1.1.1h-1
BuildRequires:  openresty-pcre-devel >= 8.44-1
Requires:       openresty-zlib >= 1.2.11-3
Requires:       openresty-openssl111 >= 1.1.1h-1
Requires:       openresty-pcre >= 8.44-1


%if 0%{?suse_version}

# for /sbin/service
Requires(post):  insserv-compat
Requires(preun): insserv-compat

BuildRequires:  systemd

%else

%if 0%{?use_systemd}

BuildRequires:  systemd
Requires:       systemd

%else

# for /sbin/service
Requires(post):  chkconfig
Requires(preun): chkconfig, initscripts

%endif

%endif

AutoReqProv:        no

%define orprefix            %{_usr}/local/%{name}
%define zlib_prefix         %{orprefix}/zlib
%define pcre_prefix         %{orprefix}/pcre
%define openssl_prefix      %{orprefix}/openssl111

%global debug_package %{nil}

# Remove source code from debuginfo package.
%define __debug_install_post \
  %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"; \
  rm -rf "${RPM_BUILD_ROOT}/usr/src/debug"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/openresty-%{version}"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/tmp"; \
  mkdir -p "${RPM_BUILD_ROOT}/usr/src/debug/builddir"; \
%{nil}

%if 0%{?fedora} >= 27
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%if 0%{?rhel} >= 8
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%if 0%{?openEuler} >= 2
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%endif

%description
This package contains the core server for OpenResty. Built for production
uses.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.

By taking advantage of various well-designed Nginx modules (most of which
are developed by the OpenResty team themselves), OpenResty effectively
turns the nginx server into a powerful web app server, in which the web
developers can use the Lua programming language to script various existing
nginx C modules and Lua modules and construct extremely high-performance
web applications that are capable to handle 10K ~ 1000K+ connections in
a single box.


%package resty

Summary:        OpenResty command-line utility, resty
Group:          Development/Tools
Requires:       perl, openresty >= %{version}-%{release}
Requires:       perl(File::Spec), perl(FindBin), perl(List::Util), perl(Getopt::Long), perl(File::Temp), perl(POSIX), perl(Time::HiRes)

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6 || 0%{?%openEuler} >= 2
BuildArch:      noarch
%endif


%description resty
This package contains the "resty" command-line utility for OpenResty, which
runs OpenResty Lua scripts on the terminal using a headless NGINX behind the
scene.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.


%package doc

Summary:        OpenResty documentation tool, restydoc
Group:          Development/Tools
Requires:       perl, perl(Getopt::Std), perl(File::Spec), perl(FindBin), perl(Cwd), perl(File::Temp), perl(Pod::Man), perl(Pod::Text)

%if (!0%{?rhel} || 0%{?rhel} < 7) && !0%{?fedora}
Requires:       groff
%endif

%if (0%{?rhel} && 0%{?rhel} >= 7) || 0%{?fedora} || 0%{?%openEuler} >= 2
Requires:       groff-base
%endif

Provides:       restydoc, restydoc-index, md2pod.pl

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6 || 0%{?%openEuler} >= 2
BuildArch:      noarch
%endif


%description doc
This package contains the official OpenResty documentation index and
the "restydoc" command-line utility for viewing it.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.


%package opm

Summary:        OpenResty Package Manager
Group:          Development/Tools
Requires:       perl, openresty >= %{version}-%{release}, perl(Digest::MD5)
Requires:       openresty-doc >= %{version}-%{release}, openresty-resty >= %{version}-%{release}
Requires:       curl, tar, gzip
#BuildRequires:  perl(Digest::MD5)
Requires:       perl(Encode), perl(FindBin), perl(File::Find), perl(File::Path), perl(File::Spec), perl(Cwd), perl(Digest::MD5), perl(File::Copy), perl(File::Temp), perl(Getopt::Long)

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6 || 0%{?centos} >= 6
BuildArch:      noarch
%endif


%description opm
This package provides the client side tool, opm, for OpenResty Pakcage Manager (OPM).


%package debug
Summary:        The debug version of OpenResty
Group:          System Environment/Daemons

BuildRequires:  openresty-openssl111-debug-devel >= 1.1.1h-1
Requires:       openresty-zlib >= 1.2.11-3
Requires:       openresty-openssl111-debug >= 1.1.1h-1
Requires:       openresty-pcre >= 8.44-1

AutoReqProv:        no

%define orprefix_debug    	%{_usr}/local/openresty-debug
%define openssl_prefix_debug  	%{_usr}/local/openresty-debug/openssl111
%define zlib_prefix_debug       %{_usr}/local/openresty/zlib
%define pcre_prefix_debug       %{_usr}/local/openresty/pcre

%description debug
This package contains the debug version of the core server for OpenResty.
Built for development purposes only.

DO NOT USE THIS PACKAGE IN PRODUCTION!

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.

By taking advantage of various well-designed Nginx modules (most of which
are developed by the OpenResty team themselves), OpenResty effectively
turns the nginx server into a powerful web app server, in which the web
developers can use the Lua programming language to script various existing
nginx C modules and Lua modules and construct extremely high-performance
web applications that are capable to handle 10K ~ 1000K+ connections in
a single box.

%prep
%setup -q -n "openresty-%{version}"

%patch1 -p1

%build
./configure \
    --out-dir='build' \
    --prefix="%{orprefix}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-cc-opt="-DNGX_LUA_ABORT_AT_PANIC -I%{zlib_prefix}/include -I%{pcre_prefix}/include -I%{openssl_prefix}/include" \
    --with-ld-opt="-L%{zlib_prefix}/lib -L%{pcre_prefix}/lib -L%{openssl_prefix}/lib -Wl,-rpath,%{zlib_prefix}/lib:%{pcre_prefix}/lib:%{openssl_prefix}/lib" \
    --with-pcre-jit \
    --without-http_rds_json_module \
    --without-http_rds_csv_module \
    --without-lua_rds_parser \
    --with-stream \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-http_v2_module \
    --without-mail_pop3_module \
    --without-mail_imap_module \
    --without-mail_smtp_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_secure_link_module \
    --with-http_random_index_module \
    --with-http_gzip_static_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-threads \
    --with-compat \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT' \
    %{?_smp_mflags}

make -f 'Makefile-build' %{?_smp_mflags}


./configure \
    --out-dir='build-debug' \
    --prefix="%{orprefix_debug}" \
    --with-cc='ccache gcc -fdiagnostics-color=always' \
    --with-debug \
    --with-cc-opt="-I%{zlib_prefix_debug}/include -I%{pcre_prefix_debug}/include -I%{openssl_prefix_debug}/include -O0" \
    --with-ld-opt="-L%{zlib_prefix_debug}/lib -L%{pcre_prefix_debug}/lib -L%{openssl_prefix_debug}/lib -Wl,-rpath,%{zlib_prefix_debug}/lib:%{pcre_prefix_debug}/lib:%{openssl_prefix_debug}/lib" \
    --with-pcre-jit \
    --without-http_rds_json_module \
    --without-http_rds_csv_module \
    --without-lua_rds_parser \
    --with-stream \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-http_v2_module \
    --without-mail_pop3_module \
    --without-mail_imap_module \
    --without-mail_smtp_module \
    --with-http_stub_status_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_secure_link_module \
    --with-http_random_index_module \
    --with-http_gzip_static_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-threads \
    --with-poll_module \
    --with-compat \
    --with-luajit-xcflags='-DLUAJIT_NUMMODE=2 -DLUAJIT_ENABLE_LUA52COMPAT -O0' \
    %{?_smp_mflags}

make -f 'Makefile-build-debug' %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install -f 'Makefile-build' DESTDIR=%{buildroot}

rm -rf %{buildroot}%{orprefix}/luajit/share/man
rm -rf %{buildroot}%{orprefix}/luajit/lib/libluajit-5.1.a

mkdir -p %{buildroot}/usr/bin
ln -sf %{orprefix}/bin/resty %{buildroot}/usr/bin/
ln -sf %{orprefix}/bin/restydoc %{buildroot}/usr/bin/
ln -sf %{orprefix}/bin/opm %{buildroot}/usr/bin/
ln -sf %{orprefix}/nginx/sbin/nginx %{buildroot}/usr/bin/%{name}

%if 0%{?use_systemd}

mkdir -p %{buildroot}%{_unitdir}
%{__install} -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

%else

mkdir -p %{buildroot}/etc/init.d
%{__install} -p -m 0755 %{SOURCE2} %{buildroot}/etc/init.d/%{name}

%endif

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


make install -f 'Makefile-build-debug' DESTDIR=%{buildroot}

rm -rf %{buildroot}%{orprefix_debug}/luajit/share/man
rm -rf %{buildroot}%{orprefix_debug}/luajit/lib/libluajit-5.1.a
rm -rf %{buildroot}%{orprefix_debug}/bin/resty
rm -rf %{buildroot}%{orprefix_debug}/bin/restydoc
rm -rf %{buildroot}%{orprefix_debug}/bin/restydoc-index
rm -rf %{buildroot}%{orprefix_debug}/bin/md2pod.pl
rm -rf %{buildroot}%{orprefix_debug}/bin/nginx-xml2pod
rm -rf %{buildroot}%{orprefix_debug}/bin/opm
rm -rf %{buildroot}%{orprefix_debug}/pod/*
rm -rf %{buildroot}%{orprefix_debug}/resty.index

mkdir -p %{buildroot}/usr/bin
ln -sf %{orprefix_debug}/nginx/sbin/nginx %{buildroot}/usr/bin/%{name}-debug
%clean
rm -rf %{buildroot}


%post

%if 0%{?use_systemd}
%systemd_post openresty.service
%else
%if ! 0%{?suse_version}
/sbin/chkconfig --add %{name}
%endif
%endif


%preun
%if 0%{?use_systemd}
%systemd_preun openresty.service
%else
%if ! 0%{?suse_version}
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif
%endif


%if 0%{?use_systemd}
%postun
%systemd_postun_with_restart openresty.service
%endif


%files
%defattr(-,root,root,-)

%if 0%{?use_systemd}
%{_unitdir}/%{name}.service
%else
/etc/init.d/%{name}
%endif
/usr/bin/%{name}
%{orprefix}/bin/openresty
%{orprefix}/site/lualib/
%{orprefix}/luajit/*
%{orprefix}/lualib/*
%{orprefix}/nginx/html/*
%{orprefix}/nginx/logs/
%{orprefix}/nginx/sbin/*
%config(noreplace) %{orprefix}/nginx/conf/*
%{orprefix}/COPYRIGHT


%files resty
%defattr(-,root,root,-)

/usr/bin/resty
%{orprefix}/bin/resty


%files doc
%defattr(-,root,root,-)

/usr/bin/restydoc
%{orprefix}/bin/restydoc
%{orprefix}/bin/restydoc-index
%{orprefix}/bin/md2pod.pl
%{orprefix}/bin/nginx-xml2pod
%{orprefix}/pod/*
%{orprefix}/resty.index


%files opm
%defattr(-,root,root,-)

/usr/bin/opm
%{orprefix}/bin/opm
%{orprefix}/site/manifest/
%{orprefix}/site/pod/


%files debug
%defattr(-,root,root,-)

/usr/bin/%{name}-debug
%{orprefix_debug}/bin/openresty
%{orprefix_debug}/site/lualib/
%{orprefix_debug}/luajit/*
%{orprefix_debug}/lualib/*
%{orprefix_debug}/nginx/html/*
%{orprefix_debug}/nginx/logs/
%{orprefix_debug}/nginx/sbin/*
%config(noreplace) %{orprefix_debug}/nginx/conf/*
%{orprefix_debug}/COPYRIGHT

%changelog
* Fri Jul 23 2021 Fu Changjie <fu_changjie@qq.com> 1.19.3.1-1
- Package init with openresty 1.19.3.1, without asan package
