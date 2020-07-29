
# input: 
# COMPILER   should be something like gcc@6.4.0 format coming from modules.sh

BASE=`dirname $0`


#
# MPI - openmpi only for now
# TODO: add support for mpich
#
XXXX=`mpic++ --showme:version | sed -e "s/.*Open/Open/" -e "s/MPI.*/MPI/"`
MPI_PACKAGE="unknown"
if [ "$XXXX" = "Open MPI" ]; then
    MPI_PACKAGE="openmpi"
else
    echo "ERROR: $0: MPI is not OpenMPI and others are not supported yet"
    exit 1
fi
MPI_VERSION=`mpiexec --version | head -1 | sed -e "s/[^0-9]* //"`
MPI_PATH=`which mpiexec`
MPI_PATH=`dirname $MPI_PATH`
MPI_PATH=`dirname $MPI_PATH`

#
# PYTHON
#
PYTHON_VERSION=`python3 --version | sed -e "s/[^0-9]* //"`
PYTHON_PATH=`which python3`
PYTHON_PATH=`dirname $PYTHON_PATH`
PYTHON_PATH=`dirname $PYTHON_PATH`

#
# CMAKE
#
CMAKE_VERSION=`cmake --version | sed -e "s/[^0-9]* //" -e "s/[^0-9\.].*//"`
CMAKE_PATH=`which cmake`
CMAKE_PATH=`dirname $CMAKE_PATH`
CMAKE_PATH=`dirname $CMAKE_PATH`

echo "Set up $BASE/packages.yaml with "
echo "    compiler = $COMPILER"
echo "    MPI package = $MPI_PACKAGE"
echo "        version = $MPI_VERSION"
echo "        path = $MPI_PATH"
echo "    PYTHON"
echo "        version = $PYTHON_VERSION"
echo "        path = $PYTHON_PATH"
echo "    CMAKE" 
echo "        version $CMAKE_VERSION"
echo "        path = $CMAKE_PATH"

# Replace / with \/ in paths
MPI_PATH=${MPI_PATH//\//\\\/}
PYTHON_PATH=${PYTHON_PATH//\//\\\/}
CMAKE_PATH=${CMAKE_PATH//\//\\\/}

cat $BASE/packages.yaml.in | \
    sed -e "s/#COMPILER#/${COMPILER}/" \
        -e "s/#MPI_PACKAGE#/${MPI_PACKAGE}/" \
        -e "s/#MPI_PATH#/${MPI_PATH}/" \
        -e "s/#PYTHON_PATH#/${PYTHON_PATH}/" \
        -e "s/#CMAKE_PATH#/${CMAKE_PATH}/" \
    > $BASE/packages.yaml



