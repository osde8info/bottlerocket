Name: %{_cross_os}dbus-broker
Version: 21
Release: 1%{?dist}
Summary: D-BUS message broker
License: ASL 2.0
URL: https://github.com/bus1/dbus-broker
Source0: https://github.com/bus1/dbus-broker/archive/v%{version}/dbus-broker-%{version}.tar.xz
Source1: dbus.socket
Source2: dbus-1-system.conf
Source3: dbus-sysusers.conf
BuildRequires: meson
BuildRequires: gcc-%{_cross_target}
BuildRequires: %{_cross_os}glibc-devel
BuildRequires: %{_cross_os}libcap-devel
BuildRequires: %{_cross_os}libexpat-devel
BuildRequires: %{_cross_os}systemd-devel
Requires: %{_cross_os}glibc
Requires: %{_cross_os}libcap
Requires: %{_cross_os}libexpat
Requires: %{_cross_os}systemd

%description
%{summary}.

%prep
%autosetup -n dbus-broker-%{version} -p1

%build
CONFIGURE_OPTS=(
 -Daudit=false
 -Dlauncher=true
)

%cross_meson "${CONFIGURE_OPTS[@]}"
%cross_meson_build

%install
%cross_meson_install

install -d %{buildroot}%{_cross_unitdir}
install -p -m 0644 %{S:1} %{buildroot}%{_cross_unitdir}/dbus.socket

install -d %{buildroot}%{_cross_unitdir}/multi-user.target.wants
ln -s ../dbus-broker.service %{buildroot}%{_cross_unitdir}/multi-user.target.wants

install -d %{buildroot}%{_cross_datadir}/dbus-1/{interfaces,services,system-services,system.d}
install -p -m 0644 %{S:2} %{buildroot}%{_cross_datadir}/dbus-1/system.conf

install -d %{buildroot}%{_cross_sysusersdir}
install -p -m 0644 %{S:3} %{buildroot}%{_cross_sysusersdir}/dbus.conf

%files
%{_cross_bindir}/dbus-broker
%{_cross_bindir}/dbus-broker-launch
%dir %{_cross_datadir}/dbus-1
%{_cross_datadir}/dbus-1/*
%{_cross_journalcatalogdir}/dbus-broker.catalog
%{_cross_journalcatalogdir}/dbus-broker-launch.catalog
%{_cross_sysusersdir}/dbus.conf
%{_cross_unitdir}/dbus-broker.service
%{_cross_unitdir}/dbus.socket
%{_cross_unitdir}/multi-user.target.wants/dbus-broker.service
%exclude %{_cross_userunitdir}/dbus-broker.service

%changelog