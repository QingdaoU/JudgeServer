FROM judger
RUN apt-get update && apt-get install -y cmake vim
RUN cd /tmp && rm -rf pyfadeaway && git clone https://github.com/nikoloss/pyfadeaway.git && cd pyfadeaway && python setup.py install
RUN cd /tmp && rm -rf Judger && git clone https://github.com/QingdaoU/Judger.git && cd Judger && git checkout newnew && mkdir build && cd build && cmake .. && make && make install && cd ../bindings/Python && python setup.py install
RUN pip install psutil