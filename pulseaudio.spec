Summary:	Sound server
Name:		pulseaudio
Version:	5.0
Release:	2
License:	GPL v2+ (server and libpulsecore), LGPL v2+ (libpulse)
Group:		Libraries
Source0:	http://freedesktop.org/software/pulseaudio/releases/%{name}-%{version}.tar.gz
# Source0-md5:	32431855be1d0e938d8e28ee2717a8cc
Source1:	%{name}-tmpfiles.conf
URL:		http://pulseaudio.org/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-devel
BuildRequires:	dbus-devel
BuildRequires:	fftw3-single-devel
BuildRequires:	glib-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	json-c-devel >= 0.11-2
BuildRequires:	libasyncns-devel
BuildRequires:	libatomic_ops
BuildRequires:	libcap-devel
BuildRequires:	libltdl-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsbc-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtool
BuildRequires:	orc-devel
BuildRequires:	pkg-config
BuildRequires:	speex-devel
BuildRequires:	webrtc-audio-processing-devel
BuildRequires:	xmltoman
BuildRequires:	xorg-libSM-devel
BuildRequires:	xorg-libX11-devel
Requires(pre,postun):	pwdutils
Requires(pre):	coreutils
Requires:	%{name}-libs = %{version}-%{release}
Provides:	group(pulse)
Provides:	group(pulse-access)
Provides:	user(pulse)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PulseAudio (previously known as PolypAudio) is a sound server for
POSIX and Win32 operating systems. It allows you to do advanced
operations on your sound data as it passes between your application
and your hardware. Things like transferring the audio to a different
machine, changing the sample format or channel count and mixing
several sounds into one are easily achieved using a sound server.

%package libs
Summary:	PulseAudio libraries
Group:		Libraries

%description libs
PulseAudio libraries.

%package devel
Summary:	Development files for PulseAudio libraries
License:	GPL v2+ (libpulsecore), LGPL v2+ (libpulse)
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for PulseAudio libraries.

%package bluetooth
Summary:	Bluetooth module for PulseAudio
License:	GPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bluez4

%description bluetooth
Bluetooth module for PulseAudio.

%package gconf
Summary:	GConf module for PulseAudio
License:	GPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	GConf

%description gconf
GConf adapter for PulseAudio.

%package jack
Summary:	JACK modules for PulseAudio
License:	GPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	jack-audio-connection-kit

%description jack
JACK modules for PulseAudio.

%package zeroconf
Summary:	Zeroconf module for PulseAudio
License:	GPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	avahi

%description zeroconf
Zeroconf module for PulseAudio.

%package x11
Summary:	X11 module for PulseAudio
License:	GPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description x11
X11 module for PulseAudio.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-bluez4		    \
	--disable-default-build-tests	    \
	--disable-esound		    \
	--disable-gconf			    \
	--disable-hal-compat		    \
	--disable-lirc			    \
	--disable-oss-output		    \
	--disable-oss-wrapper		    \
	--disable-silent-rules		    \
	--disable-solaris		    \
	--disable-static		    \
	--disable-tcpwrap		    \
	--disable-xen			    \
	--enable-systemd		    \
	--with-access-group=pulse-access    \
	--with-system-group=pulse	    \
	--with-system-user=pulse	    \
	--with-udev-rules-dir=/usr/lib/udev/rules.d
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/pulse

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/pulse.conf

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%pre
%groupadd -g 106 pulse
%groupadd -g 107 pulse-access
%useradd -u 106 -g 106 -d /run/pulse -s /bin/false -c "Pulseaudio user" pulse

%postun
if [ "$1" = "0" ]; then
	%userremove pulse
	%groupremove pulse-access
	%groupremove pulse
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README

%dir %{_datadir}/pulseaudio
%dir %{_libdir}/pulse-*
%dir %{_libdir}/pulse-*/modules
%dir %{_sysconfdir}/pulse

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pulse/client.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pulse/system.pa
%{_sysconfdir}/dbus-1/system.d/pulseaudio-system.conf
/usr/lib/udev/rules.d/90-pulseaudio.rules
%{systemdtmpfilesdir}/pulse.conf
%attr(0700, pulse, pulse) %dir /var/lib/pulse

%attr(755,root,root) %{_bindir}/pacat
%attr(755,root,root) %{_bindir}/pacmd
%attr(755,root,root) %{_bindir}/pactl
%attr(755,root,root) %{_bindir}/pamon
%attr(755,root,root) %{_bindir}/paplay
%attr(755,root,root) %{_bindir}/parec
%attr(755,root,root) %{_bindir}/parecord
%attr(755,root,root) %{_bindir}/pasuspender
%attr(755,root,root) %{_bindir}/pax11publish
%attr(755,root,root) %{_bindir}/pulseaudio

%attr(755,root,root) %{_libdir}/pulse-*/modules/libalsa-util.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/libcli.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/libprotocol-cli.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/libprotocol-http.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/libprotocol-native.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/libprotocol-simple.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/librtp.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/libwebrtc-util.so

%attr(755,root,root) %{_libdir}/pulse-*/modules/module-alsa-card.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-alsa-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-alsa-source.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-always-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-augment-properties.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-bluetooth-policy.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-card-restore.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-cli-protocol-tcp.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-cli-protocol-unix.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-cli.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-combine-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-combine.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-console-kit.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-dbus-protocol.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-default-device-restore.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-detect.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-device-manager.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-device-restore.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-echo-cancel.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-equalizer-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-filter-apply.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-filter-heuristics.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-http-protocol-tcp.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-http-protocol-unix.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-intended-roles.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-ladspa-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-loopback.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-match.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-mmkbd-evdev.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-native-protocol-fd.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-native-protocol-tcp.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-native-protocol-unix.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-null-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-null-source.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-pipe-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-pipe-source.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-position-event-sounds.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-remap-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-remap-source.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-rescue-streams.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-role-cork.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-role-ducking.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-rtp-recv.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-rtp-send.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-rygel-media-server.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-simple-protocol-tcp.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-simple-protocol-unix.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-sine-source.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-sine.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-stream-restore.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-suspend-on-idle.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-switch-on-connect.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-switch-on-port-available.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-systemd-login.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-tunnel-sink-new.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-tunnel-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-tunnel-source-new.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-tunnel-source.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-udev-detect.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-virtual-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-virtual-source.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-virtual-surround-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-volume-restore.so

%{_datadir}/pulseaudio/alsa-mixer

%{_mandir}/man1/pacat.1*
%{_mandir}/man1/pacmd.1*
%{_mandir}/man1/pactl.1*
%{_mandir}/man1/padsp.1*
%{_mandir}/man1/paplay.1*
%{_mandir}/man1/pasuspender.1*
%{_mandir}/man1/pulseaudio.1*
%{_mandir}/man5/default.pa.5*
%{_mandir}/man5/pulse-cli-syntax.5*
%{_mandir}/man5/pulse-client.conf.5*
%{_mandir}/man5/pulse-daemon.conf.5*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libpulse-mainloop-glib.so.?
%attr(755,root,root) %ghost %{_libdir}/libpulse-simple.so.?
%attr(755,root,root) %ghost %{_libdir}/libpulse.so.?
%attr(755,root,root) %{_libdir}/libpulse*-*.so
%attr(755,root,root) %{_libdir}/libpulse-mainloop-glib.so.*.*.*
%attr(755,root,root) %{_libdir}/libpulse-simple.so.*.*.*
%attr(755,root,root) %{_libdir}/libpulse.so.*.*.*
%dir %{_libdir}/pulseaudio
%attr(755,root,root) %{_libdir}/pulseaudio/libpulsecommon-*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpulse.so
%attr(755,root,root) %{_libdir}/libpulse-mainloop-glib.so
%attr(755,root,root) %{_libdir}/libpulse-simple.so
%{_includedir}/pulse
%{_pkgconfigdir}/libpulse.pc
%{_pkgconfigdir}/libpulse-mainloop-glib.pc
%{_pkgconfigdir}/libpulse-simple.pc
%{_datadir}/vala/vapi/libpulse-mainloop-glib.deps
%{_datadir}/vala/vapi/libpulse-mainloop-glib.vapi
%{_datadir}/vala/vapi/libpulse.deps
%{_datadir}/vala/vapi/libpulse.vapi
%{_libdir}/cmake/PulseAudio

%files bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pulse-*/modules/libbluez5-util.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-bluetooth-discover.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-bluez5-device.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-bluez5-discover.so

%files jack
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-jack-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-jack-source.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-jackdbus-detect.so

%files zeroconf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pulse-*/modules/libavahi-wrap.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/libraop.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-raop-discover.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-raop-sink.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-zeroconf-discover.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-zeroconf-publish.so

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/start-pulseaudio-x11
%{_sysconfdir}/xdg/autostart/pulseaudio.desktop
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-x11-bell.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-x11-cork-request.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-x11-publish.so
%attr(755,root,root) %{_libdir}/pulse-*/modules/module-x11-xsmp.so
%{_mandir}/man1/pax11publish.1*
%{_mandir}/man1/start-pulseaudio-x11.1*

