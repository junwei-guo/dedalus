#git config --global user.name "junwei-guo"
#git config --global user.email guo_junwei@hotmail.com

git clone --branch tgv --single-branch https://github.com/junwei-guo/dedalus.git
cd dedalus

MPI_HOME=/Users/guo/homebrew/Cellar/open-mpi/5.0.7
GCC_HOME=/Users/guo/homebrew/Cellar/gcc/15.1.0
FFTW_HOME=/Users/guo/homebrew/Cellar/fftw/3.3.10_2

echo $MPI_HOME
echo $FFTW_HOME
echo $GCC_HOME
 
# export CC=mpicc
# export MPICC=mpicc
# export HDF5_DIR=/path/to/hdf5
# export FFTW_DIR=/path/to/fftw

export MPI_PATH=$MPI_HOME
export FFTW_PATH=$FFTW_HOME
export MPI_PREFIX=$MPI_HOME
export FFTW_PREFIX=$FFTW_HOME

#  Cannot find MPI_PATH, MPI_PREFIX, or libraries matching mpi.
#   Cannot find FFTW_PATH, FFTW_PREFIX, or libraries matching fftw.



rm -rf  dedalus-env
python3 -m venv dedalus-env
source dedalus-env/bin/activate
python3 -m pip install numpy scipy sympy Cython mpi4py h5py     
python3 -m pip install  docopt tblib coverage pytest setuptools

#python3 -m pip install pytest==7.4.4 
#pip install pytest==7.4.4 
# petsc petsc4py docopt
#pytest
python3 setup.py build
python3 setup.py install

export OMP_NUM_THREADS=1
python3 -c "import dedalus; print(dedalus.__version__)"


mpirun -np 4 python3 -m dedalus test


 python3 -m pip install matplotlib numexpr xarray py pytest-benchmark pytest-cov pytest-parallel