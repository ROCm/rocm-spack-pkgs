#!/bin/bash

rocm_driver_version=$1

# Build Base Docker Image
rocm_spack_base_image=computecqe/rocm-spack-base-"$rocm_driver_version":ub18.04
echo $rocm_spack_base_image
docker build -f ./UB18.04_base.Dockerfile . --build-arg rocm_rel=${rocm_driver_version} --no-cache -t ${rocm_spack_base_image}
if [ $? -ne 0 ]; then { echo "ERROR: failed to build base docker image!!!" ; exit 1; } fi

# Build ROCm Spack Docker Image
rocm_spack_image=computecqe/rocm-spack-"$rocm_driver_version":ub18.04
echo $rocm_spack_image
docker build -f ./rocm.spack.Dockerfile . --build-arg base_docker_image=${rocm_spack_base_image} --no-cache -t ${rocm_spack_image}
