# xow Fedora Packaging

This directory contains packaging files for building xow (Xbox One Wireless driver) RPM packages on Fedora.

## Quick Install

For users who just want to install xow, download the pre-built RPM from the [releases page](https://github.com/RegWin32/xow-fedora-atomic/releases) and install it:

```bash
sudo dnf install ./xow-fedora-atomic-*.rpm
sudo systemctl enable --now xow.service
```

## Building from Source

### Prerequisites

Set up a Fedora development environment (using toolbox is recommended for isolation):

```bash
toolbox enter
```

### Build Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RegWin32/xow-fedora-atomic.git
   cd xow-fedora-atomic
   ```

2. **Install build dependencies:**
   ```bash
   sudo dnf builddep packaging/fedora/xow.spec
   ```

   Or manually install dependencies:
   ```bash
   sudo dnf install gcc-c++ libusb-compat-0.1-devel cabextract make rpm-build rpmdevtools fedora-packager
   ```

3. **Build the RPM package:**
   ```bash
   cd packaging/fedora
   fedpkg --release f42 local
   ```

4. **Install the built package:**
   ```bash
   sudo dnf install ./x86_64/xow-fedora-atomic-*.rpm
   ```

### Alternative Build Methods

#### Using rpmbuild directly:
```bash
rpmdev-setuptree
cp packaging/fedora/xow.spec ~/rpmbuild/SPECS/
wget -O ~/rpmbuild/SOURCES/v0.6.tar.gz https://github.com/RegWin32/xow-fedora-atomic/archive/v0.6.tar.gz
rpmbuild -ba ~/rpmbuild/SPECS/xow.spec
```

#### Using make (if available):
```bash
make rpm
```

## Post-Installation Setup

1. **Enable the systemd service:**
   ```bash
   sudo systemctl enable --now xow.service
   ```

2. **Check service status:**
   ```bash
   sudo systemctl status xow.service
   ```

3. **Connect your Xbox Wireless Adapter:**
    - Plug the adapter into a USB port
    - The LED should start blinking

4. **Pair your controller:**
    - Hold the Xbox button on your controller to turn it on
    - Press and hold the sync button on the controller
    - Press the sync button on the wireless adapter
    - The LED should become solid when paired

## Package Contents

The RPM package includes:
- `/usr/bin/xow` - Main driver executable
- `/usr/bin/xow-get-firmware.sh` - Firmware download script
- `/usr/lib/systemd/system/xow.service` - Systemd service file
- `/usr/lib/udev/rules.d/50-xow.rules` - udev rules for device detection
- `/usr/lib/modules-load.d/xow-uinput.conf` - Module loading configuration
- `/usr/lib/modprobe.d/xow-blacklist.conf` - Blacklist conflicting drivers

## Troubleshooting

### Build Issues

**Problem:** Missing build dependencies
```bash
# Install all required packages
sudo dnf builddep packaging/fedora/xow.spec
```

**Problem:** Firmware download fails during build
- Ensure internet connection is available
- The build downloads Xbox firmware from Microsoft's servers

### Runtime Issues

**Problem:** Service fails to start
```bash
# Check logs
sudo journalctl -u xow.service -f

# Verify adapter is detected
lsusb | grep -i xbox
```

**Problem:** Controller not pairing
- Ensure xow service is running
- Remove conflicting drivers: `sudo modprobe -r xpad`
- Reset controller using small button on back

## Technical Notes

### Changes from Upstream

This fork includes fixes for:
- Compilation issues with modern GCC (missing `#include <cstddef>`)
- Fedora-specific packaging optimizations
- Updated build system integration

### Supported Fedora Versions

Tested on:
- Fedora 42 (primary target)
- Should work on Fedora 40+ with minor adjustments

### License

This packaging is provided under the same license as xow (GPL-2.0-or-later).

**Important:** The Xbox wireless firmware is proprietary and subject to Microsoft's license terms. By building and using this package, you accept Microsoft's license terms for their driver package.

## Contributing

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Test the build process
5. Submit a pull request

For packaging-specific issues, please open an issue in this repository. For xow driver issues, refer to the [upstream project](https://github.com/medusalix/xow).

## Links

- [Upstream xow project](https://github.com/medusalix/xow)
- [Xbox Wireless Adapter support](https://github.com/medusalix/xow#supported-devices)
- [Fedora packaging guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)