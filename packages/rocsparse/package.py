# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import re

class Rocsparse(CMakePackage):
    """rocSPARSE exposes a common interface that provides Basic Linear Algebra Subroutines for 
       sparse computation implemented on top of AMD's Radeon Open eCosystem Platform ROCm runtime 
       and toolchains. rocSPARSE is created using the HIP programming language and optimized for AMD's latest discrete GPUs."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSPARSE"
    url      = "https://github.com/ROCmSoftwarePlatform/rocSPARSE/archive/rocm-3.5.0.tar.gz"

    # maintainers = ['github_user1', 'github_user2']

    version('3.5.0', sha256='9ca6bae7da78abbb47143c3d77ff4a8cd7d63979875fc7ebc46b400769fd9cb5')

    depends_on('cmake@3.5.2', type='build')
    depends_on('hip@3.5.0:', type='build', when='@3.5.0:')
    depends_on('comgr@3.5.0:', type='build', when='@3.5.0')
    depends_on('rocm-device-libs@3.5.0:', type='build', when='@3.5.0')
    depends_on('llvm-amdgpu@3.5.0:', type='build', when='@3.5.0')
    depends_on('rocminfo@3.5.0:', type='build', when='@3.5.0')
    depends_on('hsa-rocr-dev@3.5.0:', type='build', when='@3.5.0')
    depends_on('rocprim@3.5.0:', type='build', when='@3.5.0')
    depends_on('boost', type='build')    
    depends_on('googletest', type='build')    
    
    def setup_build_environment(self, build_env):
        build_env.unset('PERL5LIB')

    def setup_run_environment(self, env):
        env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        env.set('ROCM_PATH', self.spec['rocminfo'].prefix)
        env.set('HIP_COMPILER', 'clang')
        env.set('DEVICE_LIB_PATH', self.spec['rocm-device-libs'].prefix.lib)
        env.set('Boost_INCLUDE_DIRS', self.spec['boost'].prefix.lib)
    

    def cmake_args(self):
        # Finding the version of clang
        hipcc = Executable(join_path(self.spec['hip'].prefix.bin, 'hipcc'))
        version = hipcc('--version', output=str)
        version_group = re.search(r"clang version (\S+)", version)
        version_number=version_group.group(1)
        args = [ '-DCMAKE_CXX_COMPILER={}/bin/hipcc'.format(self.spec['hip'].prefix),
                 '-DHIP_CLANG_INCLUDE_PATH={}/lib/clang/{}/include'.format(self.spec['llvm-amdgpu'].prefix, version_number),
                 '-DBoost_INCLUDE_DIRS={}'.format(self.spec['boost'].prefix.include)
               ]

        return args
