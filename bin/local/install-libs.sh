#!/bin/bash

# location of the flow123d
FLOW_LOC=$1
# specify location where libs will be build
LIBS_ROOT=$2
# set current dir manually because when using qsub, location is elsewhere
DIR=$3

_SEP_="--------------------------------------------------------------------------"

cd $DIR
mkdir -p $LIBS_ROOT


# ------------------------------------------------------------------------------
# ------------------------------------------------------------ YAML-CPP LIB ----
# ------------------------------------------------------------------------------
# default build type
BUILD_TYPE=Release
# default location for building
BUILD_TREE=$LIBS_ROOT/yamlcpp
# ------------------------------------------------------------------------------
echo "Building project YAML-CPP ($BUILD_TYPE)"
echo "Build directory set to: "
echo "  $BUILD_TREE"
echo $_SEP_


make -C $DIR/yamlcpp \
    BUILD_TYPE=$BUILD_TYPE \
    BUILD_TREE=$BUILD_TREE \
    build

# fix installation, since flow123d FindYamlCPP expect .a file
# to be in lib folder, we do it manually without package call
mkdir -p $BUILD_TREE/$BUILD_TYPE/lib
cp $BUILD_TREE/$BUILD_TYPE/libyaml-cpp.a $BUILD_TREE/$BUILD_TYPE/lib/libyaml-cpp.a
echo $_SEP_


# ------------------------------------------------------------------------------
# --------------------------------------------------------------- PETSC LIB ----
# ------------------------------------------------------------------------------
# default build type
BUILD_TYPE=Release
# default location for building
PETSC_DIR=$LIBS_ROOT/petsc
PETSC_ARCH=linux-$BUILD_TYPE
# ------------------------------------------------------------------------------
echo "Building project PETSC ($BUILD_TYPE)"
echo "Build directory set to: "
echo "  PETSC_DIR=$PETSC_DIR"
echo "Architecture set to: "
echo "  PETSC_ARCH=$PETSC_ARCH"

echo $_SEP_


# create config file which will configure petsc project
CONFIG_FILE=$DIR/petsc/config/$BUILD_TYPE.config.sh
cat <<EOT > $CONFIG_FILE
#!/bin/bash
mkdir -p @PETSC_DIR@
cp -r @INSTALL_DIR@/src/* @PETSC_DIR@
cd @PETSC_DIR@

module list

./configure \
        PETSC_ARCH=@PETSC_ARCH@ \
        --download-metis=yes --download-parmetis=yes \
        --download-blacs=yes --download-scalapack=yes --download-mumps=yes --download-hypre=yes \
        --with-debugging=0 --with-shared-libraries=0 \
        --with-make-np @MAKE_NUMCPUS@ --CFLAGS="-O3" --CXXFLAGS="-O3 -Wall -Wno-unused-local-typedefs -std=c++11"
EOT
chmod +x $CONFIG_FILE

make -C $DIR/petsc \
    BUILD_TYPE=$BUILD_TYPE \
    PETSC_DIR=$PETSC_DIR \
    build

echo $_SEP_


# ------------------------------------------------------------------------------
# ----------------------------------------------------------- ARMADILLO LIB ----
# ------------------------------------------------------------------------------
# default build type
BUILD_TYPE=Release
USE_PETSC=On
# default location for building
BUILD_TREE=$LIBS_ROOT/armadillo
# ------------------------------------------------------------------------------
echo "Building project ARMADILLO ($BUILD_TYPE)"
echo "Build directory set to: "
echo "  $BUILD_TREE"
echo $_SEP_


make -C $DIR/armadillo \
    BUILD_TYPE=$BUILD_TYPE \
    BUILD_TREE=$BUILD_TREE \
    USE_PETSC=$USE_PETSC \
    PETSC_DIR=$PETSC_DIR \
    PETSC_ARCH=$PETSC_ARCH \
    build

echo $_SEP_



# ------------------------------------------------------------------------------
# -------------------------------------------------------------- BDDCML LIB ----
# ------------------------------------------------------------------------------
# default build type
BUILD_TYPE=Release
USE_PETSC=On
# default location for building
BUILD_TREE=$LIBS_ROOT/bddcml
# ------------------------------------------------------------------------------
echo "Building project BDDCML ($BUILD_TYPE)"
echo "Build directory set to: "
echo "  $BUILD_TREE"
echo $_SEP_


make -C $DIR/bddcml \
    BUILD_TYPE=$BUILD_TYPE \
    BUILD_TREE=$BUILD_TREE \
    USE_PETSC=$USE_PETSC \
    PETSC_DIR=$PETSC_DIR \
    PETSC_ARCH=$PETSC_ARCH \
    build

echo $_SEP_

echo "# Configuration for metacentrum"    >  config.cmake
echo "set(FLOW_BUILD_TYPE release)"       >> config.cmake
echo "set(CMAKE_VERBOSE_MAKEFILE on)"     >> config.cmake
echo "set(LIBS_ROOT $LIBS_ROOT)"          >> config.cmake
echo "set(LIB_BUILD_TYPE Release)"        >> config.cmake
cat <<EOT > config.cmake
# Configuration for metacentrum
set(FLOW_BUILD_TYPE release)
set(CMAKE_VERBOSE_MAKEFILE on)

# external libraries
set(PETSC_DIR           "$LIBS_ROOT/petsc/")
set(PETSC_ARCH          "linux-$BUILD_TYPE")

set(BDDCML_ROOT         "$LIBS_ROOT/bddcml/bddcml/$BUILD_TYPE")
set(YamlCpp_ROOT_HINT   "$LIBS_ROOT/yamlcpp/$BUILD_TYPE")
set(Armadillo_ROOT_HINT "$LIBS_ROOT/armadillo/$BUILD_TYPE")


# additional info
set(USE_PYTHON          "yes")
set(PLATFORM_NAME       "linux_x86_64")
EOT


cp $DIR/config.cmake $FLOW_LOC/config.cmake