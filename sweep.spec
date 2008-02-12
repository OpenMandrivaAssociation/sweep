%define name    sweep 
%define version 0.9.2
%define release %mkrel 1

Summary: 	Sound sample editor 
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
URL: 		http://sweep.sourceforge.net/
Source:	 	http://prdownloads.sourceforge.net/sweep/%{name}-%{version}.tar.bz2
License: 	GPL 
Group: 		Sound
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires:  gtk+2-devel
BuildRequires:  libmad-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libsndfile-devel >= 1.0.2
BuildRequires:  libspeex-devel
BuildRequires:  libalsa-devel
BuildRequires:  libtdb-devel
BuildRequires:  libvorbis-devel
BuildRequires:  librsvg
BuildRequires:  desktop-file-utils
#gw aclocal
Buildrequires: gettext-devel
#gw lam also has a binary named sweep
Conflicts:	lam-runtime
%description
Sweep is an audio editor and live playback tool for GNU/Linux, BSD and
compatible systems. It supports many music and voice formats including
WAV, AIFF, Ogg Vorbis, Speex and MP3, with multichannel editing and
LADSPA effects plugins. Inside lives a pesky little virtual stylus called
Scrubby who enjoys mixing around in your files.

%package devel
Summary: C headers for developing Sweep plugins
Group: Development/C
Requires: %name = %version

%description devel
Sweep is an audio editor and live playback tool for GNU/Linux, BSD and
compatible systems. It supports many music and voice formats including
WAV, AIFF, Ogg Vorbis, Speex and MP3, with multichannel editing and
LADSPA effects plugins. Inside lives a pesky little virtual stylus called
Scrubby who enjoys mixing around in your files.

This package contains the C headers needed to compile plugins for Sweep.


%prep
%setup -q
aclocal
autoconf
automake -a -c

%build
%configure2_5x --enable-alsa

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std MKINSTALLDIRS=`pwd`/mkinstalldirs
rm -rf %buildroot%_datadir/locale/en_AU
%{find_lang} %{name}

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --add-category="AudioVideo" \
  --add-category="Audio" \
  --add-category="Sequencer" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


mkdir -p %buildroot{%_iconsdir,%_liconsdir,%_miconsdir}
rsvg -w 48 -h 48 %name.svg %buildroot%_liconsdir/%name.png
rsvg -w 32 -h 32 %name.svg %buildroot%_iconsdir/%name.png
rsvg -w 16 -h 16 %name.svg %buildroot%_miconsdir/%name.png


%post
/sbin/ldconfig
%{update_menus}
 
%postun
/sbin/ldconfig
%{clean_menus}  

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc README ABOUT-NLS AUTHORS COPYING ChangeLog INSTALL NEWS
%{_bindir}/*
%{_mandir}/man1/*
%_datadir/applications/%name.desktop
%{_datadir}/pixmaps/*
%dir %_libdir/sweep/
%_libdir/sweep/*.so*
%dir %_datadir/sweep/
%_datadir/sweep/sweep_splash.png
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png

%files devel 
%defattr(-,root,root)
%doc doc/*.txt
%dir %_includedir/%name
%_includedir/%name/*.h


