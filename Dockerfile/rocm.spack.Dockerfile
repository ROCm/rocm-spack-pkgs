ARG base_docker_image
FROM ${base_docker_image}

WORKDIR /root
RUN git clone https://github.com/RadeonOpenCompute/rocm-spack
RUN git clone https://github.com/spack/spack && \
    cd spack && \
    git checkout releases/v0.13

#RUN . spack/share/spack/setup-env.sh 
#RUN spack install patch

CMD ["bash"]
