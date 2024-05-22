import os

import logging
import pyinsane2
from PIL import Image

resolution = 300
dstdir = os.path.join("/tmp", 'document')
mode = "color"
source="Flatbed"

device_name = 'hpaio:/usb/Deskjet_1510_series?serial=CN3C71HM1B05YR'

""" logger = logging.getLogger()
sh = logging.StreamHandler()
formatter = logging.Formatter(
        '%(levelname)-6s %(name)-30s %(message)s'
    )
sh.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(sh) """

pyinsane2.init()

devices = pyinsane2.get_devices()
if not device_name and devices:
    device = devices[0]
else:
    for device_ in devices:
        if device_.name == device_name:
            print("Found scanner: %s" % device_.name)
            device = device_
            break


if not devices:
    raise Exception("No scanner found")

print("Setting options ...", pyinsane2.__file__)
pyinsane2.set_scanner_opt(device, 'source', [source])
pyinsane2.set_scanner_opt(device, 'resolution', [resolution])
pyinsane2.set_scanner_opt(device, 'mode', [mode])
pyinsane2.maximize_scan_area(device)
try:
    print("Scanning ...")
    scan_session = device.scan(multiple=True)
    images_list = []
    while True:
        try:
            scan_session.scan.read()
        except EOFError:
            print("Got page %d" % (len(scan_session.images)))
            img = scan_session.images[-1]
            file_name = "%s_%d.jpeg" % (dstdir, len(scan_session.images))
            images_list.append(file_name)
            img.save(file_name, "jpeg")
except StopIteration:
    
    if scan_session.images:
        print("Got %d pages" % len(scan_session.images))
        img = scan_session.images[0]
        img.save("%s.pdf" % dstdir, "PDF", resolution=100.0, save_all=True, append_images=images_list[1:])
    else:
        print("No pages")    
    print("Done")
pyinsane2.exit()