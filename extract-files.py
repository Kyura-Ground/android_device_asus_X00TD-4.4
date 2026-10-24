#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools

extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_17_2'

from extract_utils.bp_builder import BpBuilder
from extract_utils.bp_encoder import BpJSONEncoder
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.makefiles import (
    MakefilesCtx,
    ProductPackagesCtx,
    write_packages_inclusion,
)

namespace_imports = [
    'device/asus/sdm660-common',
    'vendor/asus/sdm660-common',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


def write_camera_calibration(ctx: MakefilesCtx, packages_ctx: ProductPackagesCtx):
    # Keep calibration data in vendor/lib beside the 32-bit camera blobs.
    name = 'dualcali_dump.bin'
    (
        BpBuilder(BpJSONEncoder(legacy=ctx.legacy))
        .set_rule_name('prebuilt_renderscript_bitcode')
        .name(name)
        .set('src', f'{packages_ctx.vendor_prop_rel_sub_path}/vendor/lib/{name}')
        .set('filename', name)
        .set('compile_multilib', '32')
        .set('soc_specific', True)
        .write(ctx.bp_out)
    )
    write_packages_inclusion([name], ctx.product_mk_out)


blob_fixups: blob_fixups_user_type = {
    'product/etc/permissions/qti_fingerprint_interface.xml': blob_fixup()
        .regex_replace('/system/framework/', '/system/product/framework/'),
    'vendor/etc/init/android.hardware.biometrics.fingerprint@2.1-service_asus.rc': blob_fixup()
        .regex_replace(r'android\.hardware\.biometrics\.fingerprint@2\.1-service(?=\s|$)', 'android.hardware.biometrics.fingerprint@2.1-service_asus'),
    ('vendor/lib/libmmcamera_faceproc.so', 'vendor/lib/libmmcamera_faceproc2.so'): blob_fixup()
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),
    'vendor/lib64/hw/cdfinger.fingerprint.default.so': blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib/hw/camera.sdm660.so': blob_fixup()
        .remove_needed('android.hidl.base@1.0.so'),
    ('vendor/lib64/libvendor.goodix.hardware.fingerprint@1.0.so', 'vendor/lib64/libvendor.goodix.hardware.fingerprint@1.0-service.so'): blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'X00TD',
    'asus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=False,
    skip_main_proprietary_file=True,
)
module.add_proprietary_file(
    'proprietary-files.txt',
    post_makefile_generation_fn=write_camera_calibration,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'sdm660-common')
    utils.run()
