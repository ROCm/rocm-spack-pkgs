from spack import *

class RocmCmake(CMakePackage):
    """ROCM cmake modules provides cmake modules for common build tasks needed for the ROCM software stack"""

    homepage = "https://github.com/RadeonOpenCompute/rocm-cmake"
    url      = "https://github.com/RadeonOpenCompute/rocm-cmake/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', sha256='5fc09e168879823160f5fdf4fd1ace2702d36545bf733e8005ed4ca18c3e910f')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3.5.2', type='build')

    def cmake_args(self):
        args=[
              '-DCMAKE_VERBOSE_MAKEFILE=1',
              '-DROCM_DISABLE_LDCONFIG=ON'
             ]
        return args
