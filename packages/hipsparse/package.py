# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hipsparse(CMakePackage):
    """hipSPARSE is a SPARSE marshalling library, with multiple supported
       backends. It sits between the application and a 'worker' SPARSE
       library, marshalling inputs into the backend library and marshalling
       results back to the application. hipSPARSE exports an interface that
       does not require the client to change, regardless of the chosen backend.
       Currently, hipSPARSE supports rocSPARSE and cuSPARSE as backends."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipSPARSE"
    url      = "https://github.com/ROCmSoftwarePlatform/hipSPARSE/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='fa16b2a307a5d9716066c2876febcbc1cef855bf0c96d235d2d8f2206a0fb69d')

    depends_on('cmake@3.5.2', type='build')
    depends_on('hsakmt-roct@3.5.0', type='build')
    depends_on('hsa-rocr-dev@3.5.0', type='build')
    depends_on('hip@3.5.0:', type='build', when='@3.5.0:')
    depends_on('rocm-device-libs@3.5.0:', type='build', when='@3.5.0')
    depends_on('comgr@3.5.0:', type='build', when='@3.5.0')
    depends_on('rocsparse@3.5.0:', type='build', when='@3.5.0')

    def cmake_args(self):
        hsa_rocr_inc_path = self.spec['hsa-rocr-dev'].prefix.include
        args = ['-DCMAKE_CXX_FLAGS=-I {0}'.format(hsa_rocr_inc_path),
                '-DBUILD_CLIENTS_TESTS=OFF',
                '-DBUILD_CLIENTS_BENCHMARKS=OFF',
                '-DBUILD_CLIENTS_SAMPLES=OFF']
        return args
