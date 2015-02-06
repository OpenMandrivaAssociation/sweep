Summary:	Sound sample editor
Name:		sweep
Version:	0.9.3
Release:	8
License:	GPLv2+
Group:		Sound
Url:		http://sweep.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/sweep/%{name}-%{version}.tar.gz
#gw received by mail from Pavel Fric
Source1:	cs.po
Patch0:		sweep-0.9.3-add-cs-po.patch
Patch1:		sweep-0.9.3-multithread.patch
BuildRequires:	desktop-file-utils
BuildRequires:	librsvg
BuildRequires:	libtool
#gw aclocal
Buildrequires:	gettext-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(vorbis)
#gw lam also has a binary named sweep
Conflicts:	lam-runtime

%description
Sweep is an audio editor and live playback tool for GNU/Linux, BSD and
compatible systems. It supports many music and voice formats including
WAV, AIFF, Ogg Vorbis, Speex and MP3, with multichannel editing and
LADSPA effects plugins. Inside lives a pesky little virtual stylus called
Scrubby who enjoys mixing around in your files.

%files -f %{name}.lang
%doc README ABOUT-NLS AUTHORS COPYING ChangeLog NEWS
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%dir %{_libdir}/sweep/
%{_libdir}/sweep/*.so
%dir %{_datadir}/sweep/
%{_datadir}/sweep/sweep_splash.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

#----------------------------------------------------------------------------

%package devel
Summary:	C headers for developing Sweep plugins
Group:		Development/C

%description devel
Sweep is an audio editor and live playback tool for GNU/Linux, BSD and
compatible systems. It supports many music and voice formats including
WAV, AIFF, Ogg Vorbis, Speex and MP3, with multichannel editing and
LADSPA effects plugins. Inside lives a pesky little virtual stylus called
Scrubby who enjoys mixing around in your files.

This package contains the C headers needed to compile plugins for Sweep.

%files devel
%doc doc/*.txt
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1
%patch1 -p1
cp %{SOURCE1} po/

%build
autoreconf -fi
# fix for wrongly set plugin dir on 64-bit
sed -i 's/sweep_plugin_dir=.*/sweep_plugin_dir="$PACKAGE_PLUGIN_DIR"/' configure
LDFLAGS="-lgmodule-2.0 -lX11" %configure2_5x --enable-alsa

%make

%install
%makeinstall_std MKINSTALLDIRS=`pwd`/mkinstalldirs
rm -rf %{buildroot}%{_datadir}/locale/en_AU

%find_lang %{name}

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --add-category="AudioVideo" \
  --add-category="Audio" \
  --add-category="Sequencer" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -d %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
install -m644 %{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/

