from spack import *

class HsakmtRoct(CMakePackage):
    """This is a thunk python recipe to build and install Thunk Interface. Thunk Interface is a user-mode API interfaces used to interact with the ROCk driver."""

    homepage = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface"
    url      = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface/archive/rocm-3.5.0.tar.gz"

    # maintainers = ['github_user1', 'github_user2']

    version('3.5.0', sha256='d9f458c16cb62c3c611328fd2f2ba3615da81e45f3b526e45ff43ab4a67ee4aa')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3.5.2', type='build')

    install_targets = ['install', 'install-dev']

    def cmake_args(self):
        args=[
              '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH="FALSE"',
              '-DBUILD_SHARED_LIBS="on"',
              '-DHSAKMT_WERROR=1'
             ]
        return args
