#
# Copyright (C) 2020 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/product_launched_with_o_mr1.mk)

# AxionOS device information (4 GB / 13 MP camera variant).
AXION_CAMERA_REAR_INFO := 13,5
AXION_CAMERA_FRONT_INFO := 8
AXION_MAINTAINER := ikwfahmi
AXION_PROCESSOR := Snapdragon_636

# Retain the device Power HAL and expose only supported hardware features.
TARGET_DISABLE_EPPE := true
TARGET_DISABLES_LIBPERF := false
HBM_SUPPORTED := false
BYPASS_CHARGE_SUPPORTED := false

# Inherit common AxionOS phone configuration after setting its flags.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Inherit from X00TD device
$(call inherit-product, $(LOCAL_PATH)/device.mk)

# Device identifier. This must come after all inclusions.
PRODUCT_NAME := lineage_X00TD
PRODUCT_DEVICE := X00TD
PRODUCT_BRAND := asus
PRODUCT_MODEL := Zenfone Max Pro M1
PRODUCT_MANUFACTURER := asus

PRODUCT_GMS_CLIENTID_BASE := android-asus

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="sdm660_64-user 8.1.0 OPM1 1309 release-keys" \
    BuildFingerprint=asus/WW_X00TD/ASUS_X00T_2:8.1.0/OPM1/15.2016.1805.318-20180712:user/release-keys \
    DeviceProduct=ASUS_X00T
