%define _name modsecurity-apache_2.1.1-rc1
%define include_pcre /usr/include/pcre
%define include_libxml2 /usr/include/libxml2
%define _apacheroot /usr/lib/httpd

%{?with_pcre: %define include_pcre %{with_pcre}}
%{?with_libxml2: %define include_libxml2 %{with_libxml2}}

Summary: ModSecurity Open Source Web Application Firewall
Name: modsecurity-apache2
Version: 2.1.1
Release: rc1.1
License: GPL
Group: System Environment/Daemons
URL: http://www.modsecurity.org/index.php
Source0: http://www.modsecurity.org/download/%{_name}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: httpd-devel >= 2.0
BuildRequires: /usr/sbin/apxs
BuildRequires: libxml2-devel
BuildRequires: pcre-devel
Requires: httpd >= 2.0
Requires: libxml2-devel

%description
ModSecurity(TM) is an open source intrusion detection and prevention engine for web applications (or a web application firewall). Operating as an Apache Web server module or standalone, the purpose of ModSecurity is to increase web application security, protecting web applications from known and unknown attacks.

%prep
%setup -n %{_name}
cd apache2
echo "ApacheRoot %{_apacheroot}"

sed -e " s#^top_dir.*#top_dir	= %{_apacheroot}#; " < Makefile > Makefile.rhel && mv Makefile.rhel Makefile
cd -

%build
cd apache2
make
cd -

%install
mkdir -p %{buildroot}/etc/httpd/modules 
mkdir -p %{buildroot}/etc/httpd/conf.d/modsecurity2
mkdir -p %{buildroot}%{_libdir}
if [ -d doc ]; then
 mkdir -p %{buildroot}/usr/share/doc/mod_security-%{version}
fi
install -m 0755 apache2/.libs/mod_security2.so %{buildroot}/etc/httpd/modules/
install -m 0644 modsecurity.conf-minimal %{buildroot}/etc/httpd/conf.d/modsecurity.conf
install -m 0644 apache2/mod_security2.la %{buildroot}%{_libdir}
if [ -d doc ]; then
 cp -pr doc/* %{buildroot}/usr/share/doc/mod_security-%{version}/
fi
cp -pr rules/* -d %{buildroot}/etc/httpd/conf.d/modsecurity2/
find %{buildroot} -type f | grep -v '/etc/httpd/conf.d/modsecurity.conf' | \
 sed -e " s#%{buildroot}##; s#/etc/httpd/conf.d/modsecurity2/#\%config\(noreplace\)/etc/httpd/conf.d/modsecurity2/#g; " > filelist

%clean
%{__rm} -rf %{buildroot}

%post
if ! grep mod_security /etc/httpd/conf/httpd.conf > /dev/null ;
 then
	echo "Activating Apachemodule Modsecurity"
	echo "Creating /etc/httpd/conf/httpd.conf as /etc/httpd/conf/httpd.conf.rpmnew"
	if [ ! -f %{_libdir}/libxml2.so ]; then
	 echo "You need libxml2.so. Install with yum install libxml2-devel"
	 echo "Add the following lines to your config after installing libxml2-devel"
	 echo ""; echo "LoadFile /usr/lib/libxml2.so"
	 echo "LoadModule unique_id_module modules/mod_unique_id.so"
	 echo "LoadModule security2_module modules/mod_security2.so"
	else 
 	 	if test %{_target_cpu} == x86_64; then 
	  		cat /etc/httpd/conf/httpd.conf | \
	  		perl -e 'undef $/; while (<>) { s#^(LoadModule.*?)\n\n#$1\nLoadFile /usr/lib64/libxml2.so\nLoadModule unique_id_module modules/mod_unique_id.so\nLoadModule security2_module modules/mod_security2.so\n\n#mgs; print; }' > \
	 		/etc/httpd/conf/httpd.conf.rpmnew
	 	else
	  		cat /etc/httpd/conf/httpd.conf | \
	  		perl -e 'undef $/; while (<>) { s#^(LoadModule.*?)\n\n#$1\nLoadFile /usr/lib/libxml2.so\nLoadModule unique_id_module modules/mod_unique_id.so\nLoadModule security2_module modules/mod_security2.so\n\n#mgs; print; }' > \
	 		/etc/httpd/conf/httpd.conf.rpmnew
		fi
	 	apachectl -t -f /etc/httpd/conf/httpd.conf.rpmnew && mv /etc/httpd/conf/httpd.conf.rpmnew /etc/httpd/conf/httpd.conf
	fi
fi

# Make sure the modules in installed in right selinux context:
test -f /sbin/restorecon && restorecon /usr/lib/httpd/modules/mod_security2.so

%files -f filelist
%defattr(-, root, root, 0755)
%doc LICENSE README.TXT
%config(noreplace) /etc/httpd/conf.d/modsecurity.conf

%changelog
* Thu Apr  5 2007 Jan-Frode Myklebust <janfrode@tanso.net>
	 Fixed security context using correct path, since restorecon didn't like following symlinks.
	 Ported to RHEL5.
* Tue Apr  3 2007 Jan-Frode Myklebust <janfrode@tanso.net>
	 Fixed libxml2.so path for x86_64
	 Set correct security context on /etc/httpd/modules/mod_security2.so
