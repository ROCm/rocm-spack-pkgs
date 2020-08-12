# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import re


class Rocblas(CMakePackage):
    """rocBLAS is AMD's library for BLAS on ROCm. It is implemented in the HIP programming language and optimized 
    for AMD's GPUs."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocBLAS"
    url      = "https://github.com/ROCmSoftwarePlatform/rocBLAS/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='8560fabef7f13e8d67da997de2295399f6ec595edfd77e452978c140d5f936f0')
    variant('build_type', default='Release', description='CMake build type')
   
    resource(name='Tensile',
             git='https://github.com/ROCmSoftwarePlatform/Tensile.git',
             commit='f842a1a4427624eff6cbddb2405c36dec9a210cd',
             expand=True,
             destination='',
             placement='')
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-virtualenv', type='test')
    depends_on('py-pip', type=('build', 'run'))
    depends_on('googletest', type='test')
    depends_on('cmake@3.5.2', type='build')
    depends_on('hip@3.5.0:', type='build', when='@3.5.0:')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5.0:', type='build', when='@3.5.0')
    depends_on('rocclr@3.5.0:', type='build', when='@3.5.0')
    depends_on('hsakmt-roct@3.5.0:', type='build', when='@3.5.0:')
    depends_on('hsa-rocr-dev@3.5.0:', type='link', when='@3.5.0:')
    depends_on('rocminfo@3.5.0:', type='build', when='@3.5.0:')
    depends_on('llvm-amdgpu@3.5.0:', type=('build', 'run'), when='@3.5.0')
    depends_on('llvm@6.0.1 -clang -lld -lldb -libcxx -internal_unwind -compiler-rt', type='build')
    depends_on('lapack')
    depends_on('boost')
    depends_on('zlib', type= 'build', when='@3.5.0:')

    def setup_build_environment(self, build_env):
        build_env.unset('PERL5LIB')
        build_env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        build_env.set('DEVICE_LIB_PATH', self.spec['rocm-device-libs'].prefix.lib)
        build_env.set('ROCM_AGENT_ENUM', self.spec['rocminfo'].prefix)
        build_env.set('ROCM_PATH', self.spec['rocminfo'].prefix)
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
        version_group = re.search(r"clang version (\S+)", version)
        version_number = version_group.group(1)

        args = [
                '-DHIP_COMPILER=clang',
                '-DCMAKE_CXX_COMPILER={}/bin/hipcc'.format(self.spec['hip'].prefix),
                '-DUSE_HIP_CLANG=ON',
                '-DTensile_COMPILER=hipcc',
                '-DTensile_CODE_OBJECT_VERSION=V3',
                '-DRUN_HEADER_TESTING=OFF',
                '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE',
                '-DLLVMObjectYAML_LIBRARY={}/lib/libLLVMObjectYAML.a'.format(self.spec['llvm'].prefix),
                '-DLLVM_DIR={}/lib/cmake/llvm/'.format(self.spec['llvm'].prefix),
                '-DLLVM_INCLUDE_DIRS={}/include/'.format(self.spec['llvm'].prefix),
                '-DHIP_CLANG_INCLUDE_PATH={}/lib/clang/{}/include'.format(self.spec['llvm-amdgpu'].prefix, version_number)
               ]
        return args
