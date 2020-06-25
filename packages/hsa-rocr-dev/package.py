from spack import *

class HsaRocrDev(CMakePackage):
    """This repository includes the user mode API nterfaces and libraries necessary for host applications to launch computer kernels to available HSA ROCm kernel agents.
       AMD Heterogeneous System Architecture HSA - Linux HSA Runtime for Boltzmann (ROCm) platforms
    """

    homepage = "https://github.com/RadeonOpenCompute/ROCR-Runtime"
    url      = "https://github.com/RadeonOpenCompute/ROCR-Runtime/archive/rocm-3.5.0.tar.gz"

    # maintainers = ['github_user1', 'github_user2']

    version('3.5.0', sha256='52c12eec3e3404c0749c70f156229786ee0c3e6d3c979aed9bbaea500fa1f3b8')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('libelf@0.8:', type = 'build', when ="@3.5:")
    depends_on("cmake@3.5.2", type="build")
    depends_on('hsakmt-roct@3.5:', type=('link', 'run'), when="@3.5:")

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        args = [
                '-DCMAKE_BUILD_WITH_INSTALL_RPATH=1',
                '-DCMAKE_VERBOSE_MAKEFILE=1',
                '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE'
               ]
        return args

