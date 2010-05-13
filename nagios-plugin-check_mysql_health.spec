%define		plugin	check_mysql_health
%include        /usr/lib/rpm/macros.perl
Summary:	Nagios plugin: monitor various performance-related characteristics of a MySQL DB
Summary(pl.UTF-8):	Wtyczka Nagiosa monitorująca parametry wydajnościowe bazy danych MySQL
Name:		nagios-plugin-%{plugin}
Version:	2.1.1
Release:	1
License:	GPL v2+
Group:		Networking
Source0:	http://labs.consol.de/wp-content/uploads/2010/03/check_mysql_health-%{version}.tar.gz
# Source0-md5:	f4ce441cb52d1fb2e422654e37867d5e
Source1:	%{plugin}.cfg
URL:		http://labs.consol.de/lang/de/nagios/check_mysql_health/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
Requires:	nagios-common
Obsoletes:	nagios-plugin-check_mysql_perf
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin which allows you to monitor various performance-related
characteristics of a MySQL database.

%description -l pl.UTF-8
Wtyczka Nagiosa pozwalająca na monitorowanie różnych parametrów bazy
danych MySQL związanych z wydajnością.

%prep
%setup -q -n %{plugin}-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--host=%{_target} \
	--build=%{_target} \
	--libdir=%{plugindir} \
	--libexecdir=%{plugindir} \
	--with-nagios-user=nagios \
	--with-nagios-group=nagios
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
