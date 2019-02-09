#!/bin/bash
#-----------------------------------------------------------------------------
#
# Name: install_flutter.sh
# Description:
# Write a short description of what the program does here.
# A small bash script to install flutter on Ubuntu 16.04
# Installataion instructions are based upon the documentation written here:
# https://flutter.io/docs/get-started/install/linux
# Author: Alex Cantu
# Date: 02/08/2019
#
#
#-----------------------------------------------------------------------------

# VARS -----------------------------------------------------------------------
FLUTTER_VERSION='v1.0.0-stable'
JAVA_VERSION='8'


# MAIN -----------------------------------------------------------------------

set -xe

# Install OS package dependencies
sudo apt install curl git xz-utils libglu1-mesa vim


mkdir -p ~/Development
pushd ~/Development
  # Download flutter tarball
  if ! ls | grep "flutter_linux"; then
      wget https://storage.googleapis.com/flutter_infra/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}.tar.xz
      # Extract the file
      tar xf flutter_linux_${FLUTTER_VERSION}.tar.xz
  fi

  # Adding the flutter tool to path.
  if ! grep "flutter" ~/.bashrc; then
      echo "export PATH="$PATH:`pwd`/flutter/bin"" >> ~/.bashrc
  fi
  
  # Install JAVA version 8
  sudo add-apt-repository ppa:webupd8team/java
  sudo apt-get update
  sudo apt-get install oracle-java8-installer
  sudo apt-get install oracle-java8-set-default

  # Test Java
  javac -version || exit
  # Install android studio
  if ! ls | grep "android-studio-ide"; then
      wget https://dl.google.com/dl/android/studio/ide-zips/3.3.1.0/android-studio-ide-182.5264788-linux.zip
      unzip android-studio-ide-182.5264788-linux.zip
  fi
  mkdir -p ~/Android/Sdk
  if ! grep "ANDROID_HOME" ~/.bashrc; then
      echo "export ANDROID_HOME=~/Android/Sdk" >> ~/.bashrc
      echo "export JAVA_HOME=/usr/lib/jvm/java-8-oracle" >> ~/.bashrc
  fi
popd
source ~/.bashrc
echo "Now install the SDKS via Android Studio"
