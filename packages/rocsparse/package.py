# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import re

class Rocsparse(CMakePackage):
    """ Radeon Open Compute SPARSE library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSPARSE"
    url      = "https://github.com/ROCmSoftwarePlatform/rocSPARSE/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='9ca6bae7da78abbb47143c3d77ff4a8cd7d63979875fc7ebc46b400769fd9cb5')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3.5.2')
    depends_on('boost')
    depends_on('hip@3.5:', type='build', when='@3.5:')
    depends_on('rocprim@3.5:', type='build', when='@3.5:')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5:', type='build', when='@3.5:')
    depends_on('hsa-rocr-dev@3.5.0:', type='build', when='@3.5:')

    def cmake_args(self):
        spec=self.spec

        args = [
                '-DCMAKE_CXX_COMPILER={}/hipcc'.format(spec['hip'].prefix.bin),
               ]

        return args
