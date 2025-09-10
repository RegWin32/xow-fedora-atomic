Name:           xow-fedora-atomic
Version:        0.6.5
Release:        1%{?dist}
Summary:        xow Xbox One Wireless driver with firmware

License:        GPLv2
URL:            https://github.com/RegWin32/xow-fedora-atomic

%undefine _disable_source_fetch
Source0:        https://github.com/RegWin32/xow-fedora-atomic/archive/v%{version}.tar.gz

BuildRequires:  libusb-compat-0.1-devel gcc-c++ cabextract make fedora-packager fedora-review curl
Requires:       systemd

%description
xow is a Linux user mode driver for the Xbox One wireless dongle.
It communicates with the dongle via `libusb` and provides joystick input through the `uinput` kernel module.
The input mapping is based on existing kernel drivers like xpad.

Includes Xbox One wireless dongle firmware extracted from Microsoft's official driver package.
By installing this package, you accept Microsoft's license terms for their driver package.

%global debug_package %{nil}

%prep
%autosetup -n xow-fedora-atomic-%{version}

%build
%make_build BUILD=RELEASE BINDIR=%{_bindir} UDEVDIR=%{_udevrulesdir} MODLDIR=%{_modulesloaddir} MODPDIR=%{_modprobedir} SYSDDIR=%{_unitdir}

%install
rm -rf $RPM_BUILD_ROOT
%make_install BINDIR=%{_bindir} UDEVDIR=%{_udevrulesdir} MODLDIR=%{_modulesloaddir} MODPDIR=%{_modprobedir} SYSDDIR=%{_unitdir}

# Download and install firmware during install phase
mkdir -p %{buildroot}/lib/firmware
curl -o driver.cab http://download.windowsupdate.com/c/msdownload/update/driver/drvs/2017/07/1cd6a87c-623f-4407-a52d-c31be49e925c_e19f60808bdcbfbd3c3df6be3e71ffc52e43261e.cab
cabextract -F FW_ACC_00U.bin driver.cab
echo "48084d9fa53b9bb04358f3bb127b7495dc8f7bb0b3ca1437bd24ef2b6eabdf66 FW_ACC_00U.bin" | sha256sum -c
cp FW_ACC_00U.bin %{buildroot}/lib/firmware/xow_dongle.bin
rm -f driver.cab FW_ACC_00U.bin


%files
%{_bindir}/xow
%{_bindir}/xow-get-firmware.sh
%{_udevrulesdir}/50-xow.rules
%{_modulesloaddir}/xow-uinput.conf
%{_modprobedir}/xow-blacklist.conf
%{_unitdir}/xow.service
/lib/firmware/xow_dongle.bin

%changelog
* Tue Sep 9 2025 Patrick Klein <Patrick@Kleinsbande.de> - 0.6-2
- Include firmware in RPM for Silverblue compatibility
* Tue Sep 9 2025 Patrick Klein <Patrick@Kleinsbande.de> - 0.6-1
- Added fix for cstddef compilation issue
- Updated for Fedora packaging

* Thu May 21 2020 Jairo Llopis - 0.5-1
- 1st release
