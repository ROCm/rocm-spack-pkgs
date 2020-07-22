# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import re

class Rocrand(CMakePackage):
    """The rocRAND project provides functions that generate pseudo-random and quasi-random numbers."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocRAND"
    url      = "https://github.com/ROCmSoftwarePlatform/rocRAND/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='592865a45e7ef55ad9d7eddc8082df69eacfd2c1f3e9c57810eb336b15cd5732')

    depends_on('cmake@3.5.2', type='build')
    depends_on('hip@3.5.0:', type='build', when='@3.5.0:')
    depends_on('comgr@3.5.0:', type='build', when='@3.5.0')
    depends_on('rocm-device-libs@3.5.0:', type='build', when='@3.5.0')
    depends_on('llvm-amdgpu@3.5.0:', type='build', when='@3.5.0')
    depends_on('rocminfo@3.5.0:', type='build', when='@3.5.0')
    depends_on('hsa-rocr-dev@3.5.0:', type='build', when='@3.5.0')


    def setup_build_environment(self, build_env):
        build_env.unset('PERL5LIB')
        build_env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)

    def setup_run_environment(self, env):
        env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        env.set('ROCM_PATH', self.spec['rocminfo'].prefix)
        env.set('HIP_COMPILER', 'clang')
        env.set('DEVICE_LIB_PATH', self.spec['rocm-device-libs'].prefix.lib)

    def cmake_args(self):

        # Finding the version of clang
        hipcc = Executable(join_path(self.spec['hip'].prefix.bin, 'hipcc'))
        version = hipcc('--version', output=str)
        version_group = re.search(r"clang version (\S+)", version)
        version_number=version_group.group(1)

        args = [ '-DCMAKE_CXX_COMPILER={}/bin/hipcc'.format(self.spec['hip'].prefix),
                 '-DBUILD_BENCHMARK=ON',
                 '-DBUILD_TEST=OFF',
                 '-DHIP_CLANG_INCLUDE_PATH={}/lib/clang/{}/include'.format(self.spec['llvm-amdgpu'].prefix, version_number)
                ]
        return args
