# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import re

class Hipblas(CMakePackage):
    """hipBLAS is a BLAS marshalling library, with multiple supported backends. It sits between the application and a 'worker' BLAS library, marshalling inputs into the backend library and marshalling results back to the application. hipBLAS exports an interface that does not require the client to change, regardless of the chosen backend. Currently, hipBLAS supports rocBLAS and cuBLAS as backends."""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipBLAS"
    url      = "https://github.com/ROCmSoftwarePlatform/hipBLAS/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='d451da80beb048767da71a090afceed2e111d01b3e95a7044deada5054d6e7b1')
    depends_on('cmake@3.5.2', type='build')
    depends_on('hip@3.5.0:', type='build', when='@3.5.0:')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5.0:', type='build', when='@3.5.0')
    depends_on('rocclr@3.5.0:', type='build', when='@3.5.0')
    depends_on('hsakmt-roct@3.5.0:', type='build', when='@3.5.0:')
    depends_on('hsa-rocr-dev@3.5.0:', type='link', when='@3.5.0:')
    depends_on('rocminfo@3.5.0:', type='build', when='@3.5.0:')
    depends_on('rocblas@3.5.0:', type='build', when='@3.5.0:')
    depends_on('rocsolver@3.5.0:', type='build', when='@3.5.0:')

    def setup_build_environment(self, build_env):
        build_env.unset('PERL5LIB')
        build_env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        build_env.set('DEVICE_LIB_PATH', self.spec['rocm-device-libs'].prefix.lib)


    def setup_run_environment(self, env):
        env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        env.set('ROCM_PATH', self.spec['rocminfo'].prefix)
        env.set('HIP_COMPILER', 'clang')
        env.set('HIP_PLATFORM', 'hip-clang')

    def cmake_args(self):
        spec=self.spec
        # Finding the version of clang
        hipcc = Executable(join_path(self.spec['hip'].prefix.bin, 'hipcc'))
        version = hipcc('--version', output=str)
        print(version)
        version_group = re.search(r"clang version (\S+)", version)
        print(version_group)
        version_number = version_group.group(1)
        print(version_number)
        args = [
                '-DHIP_COMPILER=clang',
                '-DCMAKE_CXX_COMPILER={}/bin/hipcc'.format(self.spec['hip'].prefix),
                '-DUSE_HIP_CLANG=ON',
                '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE',
                '-DCMAKE_PREFIX_PATH={};{}'.format(self.spec['comgr'].prefix,self.spec['llvm-amdgpu'].prefix),
                '-DHIP_CLANG_INCLUDE_PATH={}/lib/clang/{}/include'.format(self.spec['llvm-amdgpu'].prefix, version_number)
               ]

        return args

