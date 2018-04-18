#detect_qr
import timeit
from pyzbar.pyzbar import decode

from PIL import Image

start_time=timeit.default_timer()
[a]=decode(Image.open("/home/pi/Downloads/img1.jpg"))
print a[0]
elapsed=timeit.default_timer()-start_time
print elapsed
