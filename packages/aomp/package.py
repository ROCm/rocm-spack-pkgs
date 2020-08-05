# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Aomp(Package):
    """llvm openmp compiler from AMD."""

    homepage = "https://github.com/ROCm-Developer-Tools/aomp"
    url      = "https://github.com/ROCm-Developer-Tools/aomp/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'estewart08']
    version('3.5.0', sha256='2703b8feef079c1b1405a53e562c0b5c00a091d92ba204d441b8ae1724b0607f')

    depends_on('cmake@3.5.2', type='build')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')
    depends_on('hsakmt-roct@3.5:', type='build', when='@3.5:')
    depends_on('hsa-rocr-dev@3.5:', type='build', when='@3.5:')
    depends_on('comgr@3.5:', type='build', when='@3.5:')

    resource(name='rocm-device-libs',
             url='https://github.com/RadeonOpenCompute/ROCm-Device-Libs/archive/roc-3.5.0.tar.gz',
             sha256='dce3a4ba672c4a2da4c2260ee4dc96ff6dd51877f5e7e1993cb107372a35a378',
             expand=True,
             destination='aomp-dir',
             placement='rocm-device-libs')

    resource(name='amd-llvm-project',
             url='https://github.com/ROCm-Developer-Tools/amd-llvm-project/archive/rocm-3.5.0.tar.gz',
             sha256='b4fd7305dc57887eec17cce77bbf42215db46a4a3d14d8e517ab92f4e200b29d',
             expand=True,
             destination='aomp-dir',
             placement='amd-llvm-project')

    resource(name='flang',
             url='https://github.com/ROCm-Developer-Tools/flang/archive/rocm-3.5.0.tar.gz',
             sha256='cc27f8bfb49257b7a4f0b03f4ba5e06a28dcb6c337065c4201b6075dd2d5bc48',
             expand=True,
             destination='aomp-dir',
             placement='flang')

    resource(name='aomp-extras',
             url='https://github.com/ROCm-Developer-Tools/aomp-extras/archive/rocm-3.5.0.tar.gz',
             sha256='5dbf27f58b8114318208b97ba99a90483b78eebbcad4117cac6881441977e855',
             expand=True,
             destination='aomp-dir',
             placement='aomp-extras')

    resource(name='hip-on-vdi',
             url='https://github.com/ROCm-Developer-Tools/hip/archive/master-next.tar.gz',
             expand=True,
             destination='aomp-dir',
             placement='hip-on-vdi')

    resource(name='vdi',
             url='https://github.com/ROCm-Developer-Tools/rocclr/archive/master.tar.gz',
             expand=True,
             destination='aomp-dir',
             placement='vdi')

    resource(name='opencl-on-vdi',
             url='https://github.com/RadeonOpenCompute/ROCm-OpenCL-Runtime/archive/master.tar.gz',
             expand=True,
             destination='aomp-dir',
             placement='opencl-on-vdi')

    def setup_build_environment(self, build_env):
        spec=self.spec
        build_env.set('AOMP', self.spec['aomp'].prefix)
        build_env.set('FC', '{}/bin/flang'.format(self.spec['aomp'].prefix))
        build_env.set('GFXLIST', 'gfx700 gfx701 gfx801 gfx803 gfx900 gfx902 gfx906 gfx908')

    def install(self, spec, prefix):
        filter_file('{ROCM_DIR}/lib/bitcode', '{DEVICE_LIBS_DIR}', '{}/aomp-dir/aomp-extras/aomp-device-libs/aompextras/CMakeLists.txt'.format(self.stage.source_path),
                                                                   '{}/aomp-dir/aomp-extras/aomp-device-libs/libm/CMakeLists.txt'.format(self.stage.source_path),
                                                                   '{}/aomp-dir/amd-llvm-project/openmp/libomptarget/deviceRTLs/hostcall/CMakeLists.txt'.format(self.stage.source_path),
                                                                   '{}/aomp-dir/amd-llvm-project/openmp/libomptarget/deviceRTLs/amdgcn/CMakeLists.txt'.format(self.stage.source_path),
                                                                   string=True)

        filter_file('\${ROCM_DIR}/hsa/include \${ROCM_DIR}/hsa/include/hsa', '${HSA_INCLUDE}/hsa/include ${HSA_INCLUDE}/hsa/include/hsa', '{}/aomp-dir/amd-llvm-project/openmp/libomptarget/plugins/hsa/CMakeLists.txt'.format(self.stage.source_path))
        filter_file('{ROCM_DIR}/hsa/lib', '{HSA_LIB}', '{}/aomp-dir/amd-llvm-project/openmp/libomptarget/plugins/hsa/CMakeLists.txt'.format(self.stage.source_path))
        filter_file('{ROCM_DIR}/lib', '{HSAKMT_LIB}', '{}/aomp-dir/amd-llvm-project/openmp/libomptarget/plugins/hsa/CMakeLists.txt'.format(self.stage.source_path))
        filter_file('{ROCM_DIR}/include', '{COMGR_INCLUDE}', '{}/aomp-dir/amd-llvm-project/openmp/libomptarget/plugins/hsa/CMakeLists.txt'.format(self.stage.source_path))
        filter_file('-L\${LLVM_LIBDIR}\${OPENMP_LIBDIR_SUFFIX}', '-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX} -L${COMGR_LIB}', '{}/aomp-dir/amd-llvm-project/openmp/libomptarget/plugins/hsa/CMakeLists.txt'.format(self.stage.source_path))
        filter_file('rpath,\${LLVM_LIBDIR}\${OPENMP_LIBDIR_SUFFIX}', 'rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX} -Wl,-rpath,${COMGR_LIB}', '{}/aomp-dir/amd-llvm-project/openmp/libomptarget/plugins/hsa/CMakeLists.txt'.format(self.stage.source_path))

        components = dict()
        components['amd-llvm-project'] = [
                                          '../aomp-dir/amd-llvm-project/llvm',
                                          '-DLLVM_ENABLE_PROJECTS=clang;lld;compiler-rt',
                                          '-DCMAKE_BUILD_TYPE=release',
                                          '-DLLVM_ENABLE_ASSERTIONS=ON',
                                          '-DLLVM_TARGETS_TO_BUILD=AMDGPU;X86',
                                          '-DCMAKE_C_COMPILER=/usr/bin/gcc-7',
                                          '-DCMAKE_CXX_COMPILER=/usr/bin/g++-7',
                                          '-DBUG_REPORT_URL=https://github.com/ROCm-Developer-Tools/aomp',
                                          '-DLLVM_ENABLE_BINDINGS=OFF',
                                          '-DLLVM_INCLUDE_BENCHMARKS=OFF',
                                          '-DLLVM_BUILD_TESTS=OFF',
                                          '-DLLVM_INCLUDE_TESTS=OFF',
                                          '-DCLANG_INCLUDE_TESTS=OFF',
                                          '-DCMAKE_VERBOSE_MAKEFILE=1',
                                          '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE'
                                         ]

        components['vdi'] =              [
                                          '../aomp-dir/vdi',
                                          '-DUSE_COMGR_LIBRARY=yes',
                                          '-DOPENCL_DIR={}/aomp-dir/opencl-on-vdi/api/opencl'.format(self.stage.source_path)
                                         ]

        components['hip-on-vdi'] =       [
                                          '../aomp-dir/hip-on-vdi',
                                          '-DVDI_ROOT={}/aomp-dir/vdi'.format(self.stage.source_path),
                                          '-DHIP_COMPILER=clang',
                                          '-DHIP_PLATFORM=vdi',
                                          '-DVDI_DIR={}/aomp-dir/vdi'.format(self.stage.source_path),
                                          '-DHSA_PATH={}'.format(self.spec['hsa-rocr-dev'].prefix),
                                          '-DLIBVDI_STATIC_DIR={}/spack-build-vdi'.format(self.stage.source_path),
                                          '-DCMAKE_CXX_FLAGS=-Wno-ignored-attributes'
                                         ]

        components['aomp-extras'] =      [
                                          '../aomp-dir/aomp-extras',
                                          '-DROCM_PATH=$ROCM_DIR ',
                                          '-DDEVICE_LIBS_DIR={}/lib'.format(self.spec['rocm-device-libs'].prefix),
                                          '-DAOMP_STANDALONE_BUILD=0',
                                          '-DDEVICELIBS_ROOT={}/aomp-dir/rocm-device-libs'.format(self.stage.source_path)
                                         ]

        components['openmp'] =           [
                                          '../aomp-dir/amd-llvm-project/openmp',
                                          '-DROCM_DIR={}'.format(self.spec['hsa-rocr-dev'].prefix),
                                          '-DDEVICE_LIBS_DIR={}/lib'.format(self.spec['rocm-device-libs'].prefix),
                                          '-DAOMP_STANDALONE_BUILD=0',
                                          '-DDEVICELIBS_ROOT={}/aomp-dir/rocm-device-libs'.format(self.stage.source_path),
                                          '-DOPENMP_ENABLE_LIBOMPTARGET=1',
                                          '-DOPENMP_TEST_C_COMPILER=$AOMP/bin/clang',
                                          '-DOPENMP_TEST_CXX_COMPILER=$AOMP/bin/clang++',
                                          '-DLIBOMPTARGET_AMDGCN_GFXLIST=gfx700;gfx701;gfx801;gfx803;gfx900;gfx902;gfx906;gfx908',
                                          '-DLIBOMP_COPY_EXPORTS=OFF',
                                          '-DHSA_INCLUDE={}'.format(self.spec['hsa-rocr-dev'].prefix),
                                          '-DHSA_LIB={}/lib'.format(self.spec['hsa-rocr-dev'].prefix),
                                          '-DHSAKMT_LIB={}/lib'.format(self.spec['hsakmt-roct'].prefix),
                                          '-DCOMGR_INCLUDE={}/include'.format(self.spec['comgr'].prefix),
                                          '-DCOMGR_LIB={}/lib'.format(self.spec['comgr'].prefix),
                                         ]
        components['openmp-debug'] =           [
                                          '../aomp-dir/amd-llvm-project/openmp',
                                          '-DROCM_DIR={}'.format(self.spec['hsa-rocr-dev'].prefix),
                                          '-DDEVICE_LIBS_DIR={}/lib'.format(self.spec['rocm-device-libs'].prefix),
                                          '-DAOMP_STANDALONE_BUILD=0',
                                          '-DDEVICELIBS_ROOT={}/aomp-dir/rocm-device-libs'.format(self.stage.source_path),
                                          '-DOPENMP_ENABLE_LIBOMPTARGET=1',
                                          '-DOPENMP_TEST_C_COMPILER=$AOMP/bin/clang',
                                          '-DOPENMP_TEST_CXX_COMPILER=$AOMP/bin/clang++',
                                          '-DLIBOMPTARGET_AMDGCN_GFXLIST=gfx700;gfx701;gfx801;gfx803;gfx900;gfx902;gfx906;gfx908',
                                          '-DLIBOMP_COPY_EXPORTS=OFF',
                                          '-DHSA_INCLUDE={}'.format(self.spec['hsa-rocr-dev'].prefix),
                                          '-DHSA_LIB={}/lib'.format(self.spec['hsa-rocr-dev'].prefix),
                                          '-DHSAKMT_LIB={}/lib'.format(self.spec['hsakmt-roct'].prefix),
                                          '-DCOMGR_INCLUDE={}/include'.format(self.spec['comgr'].prefix),
                                          '-DCOMGR_LIB={}/lib'.format(self.spec['comgr'].prefix),
                                          '-DLIBOMPTARGET_NVPTX_DEBUG=ON'
                                         ]

        components['pgmath'] =           [
                                          '../aomp-dir/flang/runtime/libpgmath',
                                          '-DLLVM_ENABLE_ASSERTIONS=ON',
                                          '-DLLVM_CONFIG={}/bin/llvm-config'.format(self.spec['aomp'].prefix),
                                          '-DCMAKE_CXX_COMPILER={}/bin/clang++'.format(self.spec['aomp'].prefix),
                                          '-DCMAKE_C_COMPILER={}/bin/clang'.format(self.spec['aomp'].prefix),
                                          '-DCMAKE_Fortran_COMPILER={}/bin/flang'.format(self.spec['aomp'].prefix),
                                          '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
                                          '-DCMAKE_AR=/usr/bin/ar'
                                         ]

        components['flang'] =            [
                                          '../aomp-dir/flang',
                                          '-DLLVM_ENABLE_ASSERTIONS=ON',
                                          '-DLLVM_CONFIG={}/bin/llvm-config'.format(self.spec['aomp'].prefix),
                                          '-DCMAKE_CXX_COMPILER={}/bin/clang++'.format(self.spec['aomp'].prefix),
                                          '-DCMAKE_C_COMPILER={}/bin/clang'.format(self.spec['aomp'].prefix),
                                          '-DCMAKE_Fortran_COMPILER={}/bin/flang'.format(self.spec['aomp'].prefix),
                                          '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
                                          '-DFLANG_OPENMP_GPU_AMD=ON',
                                          '-DFLANG_OPENMP_GPU_NVIDIA=ON'
                                         ]

        components['flang-runtime'] =    [
                                          '../aomp-dir/flang',
                                          '-DLLVM_ENABLE_ASSERTIONS=ON',
                                          '-DLLVM_CONFIG={}/bin/llvm-config'.format(self.spec['aomp'].prefix),
                                          '-DCMAKE_CXX_COMPILER={}/bin/clang++'.format(self.spec['aomp'].prefix),
                                          '-DCMAKE_C_COMPILER={}/bin/clang'.format(self.spec['aomp'].prefix),
                                          '-DCMAKE_Fortran_COMPILER={}/bin/flang'.format(self.spec['aomp'].prefix),
                                          '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
                                          '-DLLVM_INSTALL_RUNTIME=ON',
                                          '-DFLANG_BUILD_RUNTIME=ON'
                                         ]
        build_order = ["amd-llvm-project", "vdi", "hip-on-vdi", "aomp-extras", "openmp", "openmp-debug", "pgmath", "flang", "flang-runtime"]
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
