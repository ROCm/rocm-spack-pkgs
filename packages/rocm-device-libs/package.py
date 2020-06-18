from spack import *

class RocmDeviceLibs(CMakePackage):
    """set of AMD specific device-side language runtime libraries"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs"
    url      = "https://github.com/RadeonOpenCompute/ROCm-Device-Libs/archive/rocm-3.5.0.tar.gz"

    # maintainers = ['github_user1', 'github_user2']

    version('3.5.0', sha256='dce3a4ba672c4a2da4c2260ee4dc96ff6dd51877f5e7e1993cb107372a35a378')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3.5.2', type='build')
    depends_on('rocm-cmake@3.5:', type='build', when='@3.5:')
    depends_on('llvm-amdgpu@3.5:', type='build', when='@3.5:')

    def cmake_args(self):
        spec=self.spec

        args = [
                '-DCMAKE_VERBOSE_MAKEFILE=1',
                '-DLLVM_DIR={}'.format(spec['llvm-amdgpu'].prefix),
                '-DCMAKE_C_COMPILER={}/bin/clang'.format(spec['llvm-amdgpu'].prefix),
                '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH="FALSE"'
               ]

        return args
