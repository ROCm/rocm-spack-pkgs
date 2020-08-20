# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class HipifyClang(CMakePackage):
    """hipify-clang is a clang-based tool for translation CUDA sources into HIP sources"""

    homepage = "https://github.com/ROCm-Developer-Tools/HIPIFY"
    url      = "https://github.com/ROCm-Developer-Tools/HIPIFY/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.7.0', sha256='dd58c8b88d4b7877f2521b02954de79d570fa36fc751a17d33e56436ee02571e')
    version('3.5.0', sha256='31e7c11d3e221e15a2721456c4f8bceea9c28fd37345464c86ea74cf05ddf2c9')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3.5.1:', type='build', when='@3.5:')
    depends_on('llvm-amdgpu@3.5:', when='@3.5:')
