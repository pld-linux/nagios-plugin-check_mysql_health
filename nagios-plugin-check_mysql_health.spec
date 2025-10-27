%define		plugin	check_mysql_health
Summary:	Nagios plugin: monitor various performance-related characteristics of a MySQL DB
Summary(pl.UTF-8):	Wtyczka Nagiosa monitorująca parametry wydajnościowe bazy danych MySQL
Name:		nagios-plugin-%{plugin}
Version:	2.2.2
Release:	2
License:	GPL v2+
Group:		Networking
Source0:	https://github.com/lausser/check_mysql_health/archive/ad90395e08beb1e24c428a056d81bfb7c624c929.zip
# Source0-md5:	0bf1997673ce15f05809e8afaf7edd01
Source1:	%{plugin}.cfg
Patch0:		nobackdoor.patch
Patch1:		ssl.patch
URL:		https://omd.consol.de/docs/plugins/check_mysql_health/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
Requires:	nagios-common >= 3.2.3-3
Obsoletes:	nagios-plugin-check_mysql_perf
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins
%define		statedir	/var/spool/nagios/%{plugin}

%description
Nagios plugin which allows you to monitor various performance-related
characteristics of a MySQL database.

%description -l pl.UTF-8
Wtyczka Nagiosa pozwalająca na monitorowanie różnych parametrów bazy
danych MySQL związanych z wydajnością.

%prep
%setup -q -n %{plugin}-ad90395e08beb1e24c428a056d81bfb7c624c929
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
# NOTE: _target macro becames "noarch" if ./builder passes --target=noarch, so
# be sure use plain rpmbuild.
%configure \
	--host=%{_host} \
	--build=%{_host} \
	--with-perl=%{__perl} \
	--libdir=%{plugindir} \
	--libexecdir=%{plugindir} \
	--with-mymodules-dir=%{plugindir} \
	--with-mymodules-dyn-dir=%{plugindir} \
	--with-statefiles-dir=%{statedir} \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{statedir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
%attr(770,root,nagios) %dir %{statedir}
