# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class MiopenOpencl(CMakePackage):
    """AMD's library for high performance machine learning primitives."""

    homepage = "https://github.com/ROCmSoftwarePlatform/MIOpen"
    url = "https://github.com/ROCmSoftwarePlatform/MIOpen/archive/2.4.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version(
        '2.4.0', sha256='6ba3e57df57024ad4989ad782c58c34a73e3a8929b7b348e441ac843bafea9a2')
    variant('build_type', default='Release', description='CMake build type')

    depends_on('cmake@3.5.2', type='build')
    depends_on('rocm-cmake@3.5:', type='build', when='@2.4.0')
    depends_on('hip@3.5.0:', when='@2.4.0:')
    depends_on('comgr@3.5.0:', type='link', when='@2.4.0')
    depends_on('llvm-amdgpu@3.5.0:', when='@2.4.0')
    depends_on('rocm-opencl@3.5:', when='@2.4.0')
    depends_on('miopengemm@1.1.6:', type='link', when='@2.4.0')
    depends_on('boost@1.72.0', type='link')
    depends_on('sqlite', type='link')
    depends_on('half', type='build')
    depends_on('bzip2', type='link')
    depends_on('pkg-config', type='build')

    def cmake_args(self):
        args = [
            '-DMIOPEN_BACKEND=OpenCL',
            '-DMIOPEN_HIP_COMPILER={}/bin/clang++'
            .format(self.spec['llvm-amdgpu'].prefix),
            '-DHIP_CXX_COMPILER={}/bin/clang++'
            .format(self.spec['llvm-amdgpu'].prefix),
            '-DBoost_USE_STATIC_LIBS=Off'
        ]
        return args
