#!/bin/bash

IMAGE_TO_FLASH="${1:-../image/ubuntu-20.04.2-preinstalled-server-arm64+raspi.img}"
DEVICE_TO_FLASH="${2:-null}"

read -p "The storage $DEVICE_TO_FLASH is going to be overwritten. Are you sure ? [Y/n]" response
echo "$response"
case $response in
    [Yy]|"")
        echo "Writing image to $DEVICE_TO_FLASH..."
        ;;
    [Nn])
        echo "Exiting ..."
        exit 1;;

       *)
        echo "Invalid input. Respond just Enter or Y/y as Yes else N/n."
        exit 1;;

esac

echo "Unmounting all partitions on $DEVICE_TO_FLASH"
umount "/dev/$DEVICE_TO_FLASH"* || true
sleep 2


echo "Writing image to $DEVICE_TO_FLASH..."
sudo dd if="$IMAGE_TO_FLASH" of="/dev/$DEVICE_TO_FLASH" bs=32M && sync
sleep 2

# It turns out there are card readers that give their partitions funny names, like
# "/dev/mmcblk0" will be the device, but the partitions are called "/dev/mmcblk0p1"
# for example. Better to just get the name of the partition after we flash it.
SECOND_PARTITION=$(fdisk -l "/dev/$DEVICE_TO_FLASH" | tail -n 1 | awk '{print $1}')
echo $DEVICE_TO_FLASH
echo $IMAGE_TO_FLASH
echo $SECOND_PARTITION
# Check if there is a problem with the boot partition, and fix it if there is.
# parted can identify the problem but apparently can't fix it without user
# interaction.
MISMATCH=$(fdisk -l "/dev/$DEVICE_TO_FLASH" 2>&1 >/dev/null | grep "GPT PMBR size mismatch" || true)
if [ -n "$MISMATCH" ]; then
    echo "Fixing GPT PMBR size mismatch."
    sudo sgdisk -e "/dev/$DEVICE_TO_FLASH"
fi

echo "Resizing rootfs partition to fill all of $DEVICE_TO_FLASH..."
parted -s "/dev/$DEVICE_TO_FLASH" resizepart 2 '100%'
sleep 2
sudo e2fsck -f "$SECOND_PARTITION" || true
sleep 2

echo "Resizing filesystem on $SECOND_PARTITION to match partition size..."
sudo resize2fs -p "$SECOND_PARTITION"
sleep 2

echo "Done!"

