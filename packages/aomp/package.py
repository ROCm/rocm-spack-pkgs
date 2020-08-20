# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

tools_url = 'https://github.com/ROCm-Developer-Tools'
compute_url = 'https://github.com/RadeonOpenCompute'
aomp_sha = 'e4526489833896bbc47ba865e0d115fab278ce269789a8c99a97f444595f5f6a'
devlib_sha = 'dce3a4ba672c4a2da4c2260ee4dc96ff6dd51877f5e7e1993cb107372a35a378'
llvm_sha = 'b4fd7305dc57887eec17cce77bbf42215db46a4a3d14d8e517ab92f4e200b29d'
flang_sha = 'cc27f8bfb49257b7a4f0b03f4ba5e06a28dcb6c337065c4201b6075dd2d5bc48'
extras_sha = '5dbf27f58b8114318208b97ba99a90483b78eebbcad4117cac6881441977e855'
hip_sha = '86eb7749ff6f6c5f6851cd6c528504d42f9286967324a50dd0dd54a6a74cacc7'
vdi_sha = 'b21866c7c23dc536356db139b88b6beb3c97f58658836974a7fc167feb31ad7f'
opencl_sha = '8963fcd5a167583b3db8b94363778d4df4593bfce8141e1d3c32a59fb64a0cf6'


class Aomp(Package):
    """llvm openmp compiler from AMD."""

    homepage = tools_url + "/aomp"
    url      = tools_url + "/aomp/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'estewart08']
    version('3.5.0', sha256=aomp_sha)

    depends_on('cmake@3.5.2', type='build')
    depends_on('binutils', type='build')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')
    depends_on('hsakmt-roct@3.5:', type='build', when='@3.5:')
    depends_on('hsa-rocr-dev@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5:', type='build', when='@3.5:')
    depends_on('mesa~llvm@18.3:', type=('build', 'link'), when='@3.5:')
    depends_on('py-setuptools@44.1.0', when='@3.5:')
    depends_on('python@2.7.18', when='@3.5:')
    depends_on('perl-data-dumper', type='build', when='@3.5:')
    depends_on('gawk', type='build', when='@3.5:')

    resource(
        name='rocm-device-libs',
        url=compute_url + '/ROCm-Device-Libs/archive/roc-3.5.0.tar.gz',
        sha256=devlib_sha,
        expand=True,
        destination='aomp-dir',
        placement='rocm-device-libs')

    resource(
        name='amd-llvm-project',
        url=tools_url + '/amd-llvm-project/archive/rocm-3.5.0.tar.gz',
        sha256=llvm_sha,
        expand=True,
        destination='aomp-dir',
        placement='amd-llvm-project')

    resource(
        name='flang',
        url=tools_url + '/flang/archive/rocm-3.5.0.tar.gz',
        sha256=flang_sha,
        expand=True,
        destination='aomp-dir',
        placement='flang')

    resource(
        name='aomp-extras',
        url=tools_url + '/aomp-extras/archive/rocm-3.5.0.tar.gz',
        sha256=extras_sha,
        expand=True,
        destination='aomp-dir',
        placement='aomp-extras')

    resource(
        name='hip-on-vdi',
        url=tools_url + '/hip/archive/aomp-3.5.0.tar.gz',
        sha256=hip_sha,
        expand=True,
        destination='aomp-dir',
        placement='hip-on-vdi')

    resource(
        name='vdi',
        url=tools_url + '/rocclr/archive/aomp-3.5.0.tar.gz',
        sha256=vdi_sha,
        expand=True,
        destination='aomp-dir',
        placement='vdi')

    resource(
        name='opencl-on-vdi',
        sha256=opencl_sha,
        url=compute_url + '/ROCm-OpenCL-Runtime/archive/aomp-3.5.0.tar.gz',
        expand=True,
        destination='aomp-dir',
        placement='opencl-on-vdi')

    def patch(self):
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        with working_dir('aomp-dir/hip-on-vdi'):
            match = '^#!/usr/bin/python'
            python = self.spec['python'].command
            substitute = "#!{python}".format(python=python)
            files = [
                'hip_prof_gen.py', 'vdi/hip_prof_gen.py'
            ]
            filter_file(match, substitute, *files, **kwargs)
        src = self.stage.source_path
        libomptarget = '{}/aomp-dir/amd-llvm-project/openmp/libomptarget'
        aomp_extras = '{}/aomp-dir/aomp-extras/aomp-device-libs'
        filter_file(
            '{ROCM_DIR}/lib/bitcode', '{DEVICE_LIBS_DIR}',
            aomp_extras.format(src) + '/aompextras/CMakeLists.txt',
            aomp_extras.format(src) + '/libm/CMakeLists.txt',
            libomptarget.format(src) + '/deviceRTLs/hostcall/CMakeLists.txt',
            libomptarget.format(src) + '/deviceRTLs/amdgcn/CMakeLists.txt',
            string=True)

        filter_file(
            '\${ROCM_DIR}/hsa/include \${ROCM_DIR}/hsa/include/hsa',
            '${HSA_INCLUDE}/hsa/include ${HSA_INCLUDE}/hsa/include/hsa',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/hsa/lib', '{HSA_LIB}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/lib\)',
            '{HSAKMT_LIB})\nset(HSAKMT_LIB64 ${HSAKMT_LIB64})',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '-L\${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}',
            '-L${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS} -L${HSAKMT_LIB64}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '-rpath,\${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}',
            '-rpath,${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}' +
            ',-rpath,${HSAKMT_LIB64}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/include', '{COMGR_INCLUDE}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/include', '{COMGR_INCLUDE}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '-L\${LLVM_LIBDIR}\${OPENMP_LIBDIR_SUFFIX}',
            '-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX} -L${COMGR_LIB}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            'rpath,\${LLVM_LIBDIR}\${OPENMP_LIBDIR_SUFFIX}',
            'rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}' +
            '-Wl,-rpath,${COMGR_LIB}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

    def setup_build_environment(self, build_env):
        aomp_prefix = self.spec['aomp'].prefix
        build_env.set('AOMP', '{}'.format(format(aomp_prefix)))
        build_env.set('FC', '{}/bin/flang'.format(format(aomp_prefix)))
        build_env.set(
            'GFXLIST',
            'gfx700 gfx701 gfx801 gfx803 gfx900 gfx902 gfx906 gfx908')

    def install(self, spec, prefix):
        src = self.stage.source_path
        gfx_list = "gfx700;gfx701;gfx801;gfx803;gfx900;gfx902;gfx906;gfx908"
        aomp_prefix = self.spec['aomp'].prefix
        devlibs_prefix = self.spec['rocm-device-libs'].prefix
        hsa_prefix = self.spec['hsa-rocr-dev'].prefix
        hsakmt_prefix = self.spec['hsakmt-roct'].prefix
        comgr_prefix = self.spec['comgr'].prefix
        components = dict()
        components['amd-llvm-project'] = [
            '../aomp-dir/amd-llvm-project/llvm',
            '-DLLVM_ENABLE_PROJECTS=clang;lld;compiler-rt',
            '-DCMAKE_BUILD_TYPE=release',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;X86',
            '-DCMAKE_C_COMPILER={}'.format(self.compiler.cc),
            '-DCMAKE_CXX_COMPILER={}'.format(self.compiler.cxx),
            '-DCMAKE_ASM_COMPILER={}'.format(self.compiler.cc),
            '-DBUG_REPORT_URL=https://github.com/ROCm-Developer-Tools/aomp',
            '-DLLVM_ENABLE_BINDINGS=OFF',
            '-DLLVM_INCLUDE_BENCHMARKS=OFF',
            '-DLLVM_BUILD_TESTS=OFF',
            '-DLLVM_INCLUDE_TESTS=OFF',
            '-DCLANG_INCLUDE_TESTS=OFF',
            '-DCMAKE_VERBOSE_MAKEFILE=1',
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE'
        ]

        components['vdi'] = [
            '../aomp-dir/vdi',
            '-DUSE_COMGR_LIBRARY=yes',
            '-DOPENCL_DIR={}/aomp-dir/opencl-on-vdi/api/opencl'.format(src)
        ]

        components['hip-on-vdi'] = [
            '../aomp-dir/hip-on-vdi',
            '-DVDI_ROOT={}/aomp-dir/vdi'.format(src),
            '-DHIP_COMPILER=clang',
            '-DHIP_PLATFORM=vdi',
            '-DVDI_DIR={}/aomp-dir/vdi'.format(src),
            '-DHSA_PATH={}'.format(hsa_prefix),
            '-DLIBVDI_STATIC_DIR={}/spack-build-vdi'.format(src),
            '-DCMAKE_CXX_FLAGS=-Wno-ignored-attributes'
        ]

        components['aomp-extras'] = [
            '../aomp-dir/aomp-extras',
            '-DROCM_PATH=$ROCM_DIR ',
            '-DDEVICE_LIBS_DIR={}/lib'.format(devlibs_prefix),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={}/aomp-dir/rocm-device-libs'.format(src)
        ]

        components['openmp'] = [
            '../aomp-dir/amd-llvm-project/openmp',
            '-DROCM_DIR={}'.format(hsa_prefix),
            '-DDEVICE_LIBS_DIR={}/lib'.format(devlibs_prefix),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={}/aomp-dir/rocm-device-libs'.format(src),
            '-DOPENMP_ENABLE_LIBOMPTARGET=1',
            '-DOPENMP_TEST_C_COMPILER=$AOMP/bin/clang',
            '-DOPENMP_TEST_CXX_COMPILER=$AOMP/bin/clang++',
            '-DLIBOMPTARGET_AMDGCN_GFXLIST={}'.format(gfx_list),
            '-DLIBOMP_COPY_EXPORTS=OFF',
            '-DHSA_INCLUDE={}'.format(hsa_prefix),
            '-DHSA_LIB={}/lib'.format(hsa_prefix),
            '-DHSAKMT_LIB={}/lib'.format(hsakmt_prefix),
            '-DHSAKMT_LIB64={}/lib64'.format(hsakmt_prefix),
            '-DCOMGR_INCLUDE={}/include'.format(comgr_prefix),
            '-DCOMGR_LIB={}/lib'.format(comgr_prefix),
        ]

        components['openmp-debug'] = [
            '../aomp-dir/amd-llvm-project/openmp',
            '-DROCM_DIR={}'.format(hsa_prefix),
            '-DDEVICE_LIBS_DIR={}/lib'.format(devlibs_prefix),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={}/aomp-dir/rocm-device-libs'.format(src),
            '-DOPENMP_ENABLE_LIBOMPTARGET=1',
            '-DOPENMP_TEST_C_COMPILER=$AOMP/bin/clang',
            '-DOPENMP_TEST_CXX_COMPILER=$AOMP/bin/clang++',
            '-DLIBOMPTARGET_AMDGCN_GFXLIST={}'.format(gfx_list),
            '-DLIBOMP_COPY_EXPORTS=OFF',
            '-DHSA_INCLUDE={}'.format(hsa_prefix),
            '-DHSA_LIB={}/lib'.format(hsa_prefix),
            '-DHSAKMT_LIB={}/lib'.format(hsakmt_prefix),
            '-DHSAKMT_LIB64={}/lib64'.format(hsakmt_prefix),
            '-DCOMGR_INCLUDE={}/include'.format(comgr_prefix),
            '-DCOMGR_LIB={}/lib'.format(comgr_prefix),
            '-DLIBOMPTARGET_NVPTX_DEBUG=ON'
        ]

        components['pgmath'] = [
            '../aomp-dir/flang/runtime/libpgmath',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={}/bin/llvm-config'.format(aomp_prefix),
            '-DCMAKE_CXX_COMPILER={}/bin/clang++'.format(aomp_prefix),
            '-DCMAKE_C_COMPILER={}/bin/clang'.format(aomp_prefix),
            '-DCMAKE_Fortran_COMPILER={}/bin/flang'.format(aomp_prefix),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
            '-DCMAKE_AR={}/bin/ar'.format(self.spec['binutils'].prefix)
        ]

        components['flang'] = [
            '../aomp-dir/flang',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={}/bin/llvm-config'.format(aomp_prefix),
            '-DCMAKE_CXX_COMPILER={}/bin/clang++'.format(aomp_prefix),
            '-DCMAKE_C_COMPILER={}/bin/clang'.format(aomp_prefix),
            '-DCMAKE_Fortran_COMPILER={}/bin/flang'.format(aomp_prefix),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
            '-DFLANG_OPENMP_GPU_AMD=ON',
            '-DFLANG_OPENMP_GPU_NVIDIA=ON'
        ]

        components['flang-runtime'] = [
            '../aomp-dir/flang',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={}/bin/llvm-config'.format(aomp_prefix),
            '-DCMAKE_CXX_COMPILER={}/bin/clang++'.format(aomp_prefix),
            '-DCMAKE_C_COMPILER={}/bin/clang'.format(aomp_prefix),
            '-DCMAKE_Fortran_COMPILER={}/bin/flang'.format(aomp_prefix),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
            '-DLLVM_INSTALL_RUNTIME=ON',
            '-DFLANG_BUILD_RUNTIME=ON'
        ]

        build_order = [
            "amd-llvm-project", "vdi", "hip-on-vdi", "aomp-extras",
            "openmp", "openmp-debug", "pgmath", "flang", "flang-runtime"
        ]

        # Override standard CMAKE_BUILD_TYPE
        std_cmake_args.remove("-DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo")
        for component in build_order:
            with working_dir('spack-build-{}'.format(component), create=True):
                cmake_args = components[component]
                cmake_args.extend(std_cmake_args)
                # OpenMP build needs to be run twice(Release, Debug)
                if component == "openmp-debug":
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Debug")
                else:
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
                cmake(*cmake_args)
                make()
                make("install")
