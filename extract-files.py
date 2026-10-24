#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools

extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_17_2'

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

namespace_imports = [
    'device/asus/sdm660-common',
    'vendor/asus/sdm660-common',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


blob_fixups: blob_fixups_user_type = {
    'product/etc/permissions/qti_fingerprint_interface.xml': blob_fixup()
        .regex_replace('/system/framework/', '/system/product/framework/'),
    'vendor/etc/init/android.hardware.biometrics.fingerprint@2.1-service_asus.rc': blob_fixup()
        .regex_replace(r'android\.hardware\.biometrics\.fingerprint@2\.1-service(?=\s|$)', 'android.hardware.biometrics.fingerprint@2.1-service_asus'),
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
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'sdm660-common')
    utils.run()
