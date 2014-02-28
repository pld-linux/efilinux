Summary:	UEFI bootloader
Summary(pl.UTF-8):	Bootloader UEFI
Name:		efilinux
Version:	1.1
Release:	1
License:	BSD
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/utils/boot/efilinux/%{name}-%{version}.tar.xz
# Source0-md5:	2d3c46111cd661e65c912a7450cf40e3
BuildRequires:	gnu-efi
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# not supported by gnu-efi toolchain
%define		_fortify_cflags	%{nil}
%define		_ssp_cflags	%{nil}

%description
efilinux is a UEFI OS loader. It was created as a reference
implementation with the aim of being well documented and containing
well written source code.

%description -l pl.UTF-8
efilinux to bootloader systemów operacyjnych dla UEFI. Powstał jako
wzorcowa implementacja, której głównym celem jest dobra dokumentacja i
dobrze napisany kod źródłowy.

%prep
%setup -q

%{__sed} -i -e 's/^CFLAGS=/CFLAGS=$(OPTFLAGS) /' Makefile
# entry.c:457:6: error: 'cmdline' may be used uninitialized in this function [-Werror=uninitialized]
# entry.c:457:6: error: 'name' may be used uninitialized in this function [-Werror=uninitialized]
%{__sed} -i -e 's/-Werror//' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -D efilinux.efi $RPM_BUILD_ROOT/boot/efi/efilinux.efi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%dir /boot/efi
/boot/efi/efilinux.efi
