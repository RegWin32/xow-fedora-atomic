Name:           xow-fedora-atomic
Version:        0.6
Release:        1%{?dist}
Summary:        xow Xbox One Wireless driver.

License:        GPLv2
URL:            https://github.com/RegWin32/xow-fedora-atomic

%undefine _disable_source_fetch
Source0:        https://github.com/RegWin32/xow-fedora-atomic/archive/v%{version}.tar.gz

BuildRequires:  libusb-compat-0.1-devel gcc-c++ cabextract make fedora-packager fedora-review
Requires:       systemd

%description

xow is a Linux user mode driver for the Xbox One wireless dongle.
It communicates with the dongle via `libusb` and provides joystick input through the `uinput` kernel module.
The input mapping is based on existing kernel drivers like [xpad](https://github.com/paroj/xpad).

The Xbox One wireless dongle requires a proprietary firmware to operate.
The firmware is included with the *Xbox - Net - 7/11/2017 12:00:00 AM - 1.0.46.1* driver available from *Microsoft Update Catalog*.
The package is automatically downloaded and extracted during the build process due to Microsoft's [Terms of Use](http://www.microsoft.com/en-us/legal/intellectualproperty/copyright/default.aspx), which strictly disallow the distribution of the firmware.
**By using xow, you accept Microsoft's license terms for their driver package.**

%global debug_package %{nil}

%prep
%autosetup


%build
%make_build BUILD=RELEASE BINDIR=%{_bindir} UDEVDIR=%{_udevrulesdir} MODLDIR=%{_modulesloaddir} MODPDIR=%{_modprobedir} SYSDDIR=%{_unitdir}

%install
rm -rf $RPM_BUILD_ROOT
%make_install BINDIR=%{_bindir} UDEVDIR=%{_udevrulesdir} MODLDIR=%{_modulesloaddir} MODPDIR=%{_modprobedir} SYSDDIR=%{_unitdir}

%files
%{_bindir}/xow
%{_bindir}/xow-get-firmware.sh
%{_udevrulesdir}/50-xow.rules
%{_modulesloaddir}/xow-uinput.conf
%{_modprobedir}/xow-blacklist.conf
%{_unitdir}/xow.service

%changelog
* Tue Sep 9 2025 Patrick Klein <Patrick@Kleinsbande.de> - 0.6-1
- Added fix for cstddef compilation issue
- Updated for Fedora packaging

* Thu May 21 2020 Jairo Llopis - 0.5-1
- 1st release
