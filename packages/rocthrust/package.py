from spack import *

import os
import shutil

class Rocthrust(CMakePackage):
    """Thrust is a parallel algorithm library. This library has been ported to HIP/ROCm platform, which uses the rocPRIM library. The HIP ported library works on HIP/ROCm platforms"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocThrust"
    url      = "https://github.com/ROCmSoftwarePlatform/rocThrust/archive/rocm-3.5.0.tar.gz"

    # maintainers = ['github_user1', 'github_user2']

    version('3.5.0', sha256='0d1bac1129d17bb1259fd06f5c9cb4c1620d1790b5c295b866fb3442d18923cb')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')
    variant('clients', default=True, description='Build clients and move them to the install directory')

    depends_on('cmake@3.5.2')
    depends_on('hip@3.5:', type='build', when='@3.5:')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5:', type='build', when='@3.5:')
    depends_on('hsa-rocr-dev@3.5:', type='build', when='@3.5:')
    depends_on('rocprim@3.5:', type='build', when='@3.5:')

    def cmake_args(self):
        spec=self.spec

        args = [
                '-DCMAKE_CXX_COMPILER={}/hipcc'.format(spec['hip'].prefix.bin),
                '-DUSE_HIP_CLANG=ON',
                '-DCMAKE_MODULE_PATH={}/cmake'.format(spec['hip'].prefix),
                '-DHIP_CLANG_INCLUDE_PATH={}/lib/clang/11.0.0/include'.format(self.spec['llvm-amdgpu'].prefix)
               ]

        if spec.variants['clients'].value == True:
            args += [
                     '-DBUILD_BENCHMARK=ON',
                     '-DBUILD_TEST=ON',
                    ]

        return args

    @run_after('install')
    def move_clients(self):
        if self.spec.variants['clients'].value == True:
            print("Moving clients to install directory")
            buildPath = os.path.join(self.stage.path, 'spack-build')
            src = buildPath
            dest = os.path.join(self.prefix, 'clients/')
            destination = shutil.copytree(src, dest, copy_function = shutil.copy)

