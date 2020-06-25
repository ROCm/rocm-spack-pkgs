from spack import *
from os import popen

class RocmSmiLib(CMakePackage):
    """It is a C library for Linux that provides a user space interface for applications to monitor and control GPU applications."""

    homepage = "https://github.com/RadeonOpenCompute/rocm_smi_lib"
    url      = "https://github.com/RadeonOpenCompute/rocm_smi_lib/archive/rocm-3.5.0.tar.gz"

    # maintainers = ['github_user1', 'github_user2']

    version('3.5.0', sha256='a5d2ec3570d018b60524f0e589c4917f03d26578443f94bde27a170c7bb21e6e')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')
    depends_on('cmake@3.5.2', type='build')

    def cmake_args(self):
        args=[
              '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH="FALSE"',
              '-DCMAKE_VERBOSE_MAKEFILE=1'
             ]
        return args

    @run_after('install')
    def post_install(self):
        popen('cp -R {}/rocm_smi/lib {}'.format(self.prefix, self.prefix))
        popen('cp -R {}/rocm_smi/include {}'.format(self.prefix, self.prefix))
        popen('rm -R {}/rocm_smi'.format(self.prefix))