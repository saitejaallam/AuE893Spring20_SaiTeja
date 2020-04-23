# Install script for directory: /home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/people/people_velocity_tracker

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/build/people/people_velocity_tracker/catkin_generated/installspace/people_velocity_tracker.pc")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/people_velocity_tracker/cmake" TYPE FILE FILES
    "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/build/people/people_velocity_tracker/catkin_generated/installspace/people_velocity_trackerConfig.cmake"
    "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/build/people/people_velocity_tracker/catkin_generated/installspace/people_velocity_trackerConfig-version.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/people_velocity_tracker" TYPE FILE FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/people/people_velocity_tracker/package.xml")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/people_velocity_tracker" TYPE PROGRAM FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/build/people/people_velocity_tracker/catkin_generated/installspace/static.py")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/people_velocity_tracker" TYPE PROGRAM FILES "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/build/people/people_velocity_tracker/catkin_generated/installspace/tracker.py")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/people_velocity_tracker/launch" TYPE FILE FILES
    "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/people/people_velocity_tracker/launch/filtered_tracked_detector.launch"
    "/home/nallam/AuE893Spring20_SaiTeja/AuE893Spring20_SaiTeja/catkin_ws/src/people/people_velocity_tracker/launch/tracked_detector.launch"
    )
endif()

