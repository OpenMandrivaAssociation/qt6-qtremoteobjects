%define beta beta2
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtremoteobjects
Version:	6.7.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtremoteobjects-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtremoteobjects-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Remote Objects module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}DBus)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Qml)
BuildRequires:	cmake(Qt%{major}Gui)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}QuickTest)
BuildRequires:	cmake(Qt%{major}OpenGL)
BuildRequires:	qt%{major}-cmake
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} Remote Objects module

%global extra_devel_files_RemoteObjects \
%{_qtdir}/include/QtRepParser \
%{_qtdir}/mkspecs/modules/qt_lib_repparser*.pri \
%{_qtdir}/mkspecs/features/rep*.pr? \
%{_qtdir}/mkspecs/features/remoteobjects_repc.prf \
%{_qtdir}/modules/RepParser.json \
%{_libdir}/pkgconfig/Qt6RepParser.pc \
%{_qtdir}/lib/cmake/Qt6RepParser \
%{_qtdir}/libexec/repc

%global extra_files_RemoteObjectsQml \
%{_qtdir}/qml/QtRemoteObjects

%global extra_devel_files_RemoteObjectsQml \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6declarative_remoteobjects*.cmake

%qt6libs RemoteObjects RemoteObjectsQml

%package examples
Summary: Examples for the Qt %{major} RemoteObjects module
Group: Development/KDE and Qt

%description examples
Examples for the Qt %{major} RemoteObjects module

%files examples
%{_qtdir}/examples/remoteobjects

%prep
%autosetup -p1 -n qtremoteobjects%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON \
	-DBUILD_WITH_PCH:BOOL=OFF

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
