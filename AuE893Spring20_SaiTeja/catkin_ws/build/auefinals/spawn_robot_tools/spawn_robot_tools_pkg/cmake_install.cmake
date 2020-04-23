# Install script for directory: /home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/auefinals/spawn_robot_tools/spawn_robot_tools_pkg

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  include("/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/build/auefinals/spawn_robot_tools/spawn_robot_tools_pkg/catkin_generated/safe_execute_install.cmake")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/build/auefinals/spawn_robot_tools/spawn_robot_tools_pkg/catkin_generated/installspace/spawn_robot_tools_pkg.pc")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/spawn_robot_tools_pkg/cmake" TYPE FILE FILES
    "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/build/auefinals/spawn_robot_tools/spawn_robot_tools_pkg/catkin_generated/installspace/spawn_robot_tools_pkgConfig.cmake"
    "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/build/auefinals/spawn_robot_tools/spawn_robot_tools_pkg/catkin_generated/installspace/spawn_robot_tools_pkgConfig-version.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/spawn_robot_tools_pkg" TYPE FILE FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/auefinals/spawn_robot_tools/spawn_robot_tools_pkg/package.xml")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/spawn_robot_tools_pkg" TYPE DIRECTORY FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/auefinals/spawn_robot_tools/spawn_robot_tools_pkg/launch")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/spawn_robot_tools_pkg" TYPE DIRECTORY FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/auefinals/spawn_robot_tools/spawn_robot_tools_pkg/rviz_config")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/spawn_robot_tools_pkg" TYPE DIRECTORY FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/auefinals/spawn_robot_tools/spawn_robot_tools_pkg/worlds")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/spawn_robot_tools_pkg" TYPE DIRECTORY FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/auefinals/spawn_robot_tools/spawn_robot_tools_pkg/scripts" USE_SOURCE_PERMISSIONS)
endif()
