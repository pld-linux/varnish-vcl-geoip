#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Varnish Geo-IP VCL
Name:		varnish-vcl-geoip
Version:	20100210
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons/HTTP
# git clone http://github.com/cosimo/varnish-geoip.git
# tar -cjf varnish-geoip-20100210.tar.bz2 --exclude=.git varnish-geoip
# ../dropin varnish-geoip-20100210.tar.bz2
Source0:	varnish-geoip-%{version}.tar.bz2
# Source0-md5:	58c84b48f3b2a27601c0807bafeadbb5
URL:		http://github.com/cosimo/varnish-geoip/
BuildRequires:	perl-base
%if %{with tests}
BuildRequires:	GeoIP-db-City
BuildRequires:	GeoIP-devel
BuildRequires:	perl-JSON-XS
BuildRequires:	perl-tools-devel >= 1:5.10
%endif
Requires:	GeoIP-devel
Requires:	varnish
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/varnish

%description
This VCL will transparently add a HTTP request header with Geo-IP
information depending on the client IP address that made the request.

%prep
%setup -q -n varnish-geoip

%build
%{__make} geoip.vcl

%if %{with tests}
%{__make} geoip \
	CC="%{__cc}"
	DEBUG="%{rpmcflags}"

%{__make} test -j1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a geoip.vcl $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README examples/default.vcl
%{_sysconfdir}/geoip.vcl
