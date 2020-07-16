# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocsolver(CMakePackage):
    """rocSOLVER is a work-in-progress implementation of a subset of LAPACK functionality on the ROCm platform."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSOLVER"
    url      = "https://github.com/ROCmSoftwarePlatform/rocSOLVER/archive/3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.6beta', sha256='a3cc6498e3afdf109da18e8b0a799b62ee1877567092ae4795307cad9f6632d3')
    depends_on('cmake@3.5.2', type='build')
    depends_on('hip@3.5.0:', type='build', when='@3.5.0:')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5.0:', type='build', when='@3.5.0')
    depends_on('rocclr@3.5.0:', type='build', when='@3.5.0')
    depends_on('hsakmt-roct@3.5.0:', type='build', when='@3.5.0:')
    depends_on('hsa-rocr-dev@3.5.0:', type='link', when='@3.5.0:')
    depends_on('rocminfo@3.5.0:', type='build', when='@3.5.0:')
    depends_on('rocblas@3.5.0:', type='build', when='@3.5.0:')

    def setup_build_environment(self, build_env):
        build_env.unset('PERL5LIB')
        build_env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        build_env.set('DEVICE_LIB_PATH', self.spec['rocm-device-libs'].prefix.lib)


    def setup_run_environment(self, env):
        env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        env.set('ROCM_PATH', self.spec['rocminfo'].prefix)
        env.set('HIP_COMPILER', 'clang')
        env.set('HIP_PLATFORM', 'hip-clang')
        #env.set('DEVICE_LIB_PATH', self.spec['rocm-device-libs'].prefix.lib)

    def cmake_args(self):
        spec=self.spec
        args = [
                '-DHIP_COMPILER=clang',
                '-DCMAKE_CXX_COMPILER={}/bin/hipcc'.format(self.spec['hip'].prefix),
                '-DUSE_HIP_CLANG=ON',
                '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE',
                '-DCMAKE_PREFIX_PATH={};{}'.format(self.spec['comgr'].prefix,self.spec['llvm-amdgpu'].prefix),
                '-DHIP_CLANG_INCLUDE_PATH={}/lib/clang/11.0.0/include'.format(self.spec['llvm-amdgpu'].prefix)
               ]

        return args
