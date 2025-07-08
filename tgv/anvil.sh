#git config --global user.name "junwei-guo"
#git config --global user.email guo_junwei@hotmail.com


git clone --branch tgv --single-branch https://github.com/junwei-guo/dedalus.git



cd dedalus

python3 -m venv dedalus-env
source dedalus-env/bin/activate


python -m pip install numpy scipy

python setup.py build
python setup.py install