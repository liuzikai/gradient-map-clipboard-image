import argparse
import distutils
import pasteboard
from io import BytesIO
from PIL import Image
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--invert", default=False, action='store_true', help="Invert the image")
args = parser.parse_args()

BG = [58, 63, 74]
FG = [221, 221, 221]

pb = pasteboard.Pasteboard()
in_bytes = pb.get_contents(pasteboard.PNG) or pb.get_contents(pasteboard.TIFF)

if in_bytes is None:
    print("Clipboard doesn't contain an image")

else:
    in_stream = BytesIO(in_bytes)
    img: Image.Image = Image.open(in_stream)

    data = np.array(img.getdata())[:, :3] / 255  # RGB(A) to RGB, normalized

    if args.invert:
        data = 1.0 - data

    # Apply gradient map on the image
    # Reference: https://community.adobe.com/t5/photoshop/what-is-the-mathmatical-formula-of-gradient-map/td-p/10502214
    lum = np.dot(data, [0.3, 0.59, 0.11])

    new_data = (np.outer(1 - lum, FG) + np.outer(lum, BG)).astype(np.uint8)

    new_data = new_data.reshape((img.height, img.width, 3))

    new_img = Image.fromarray(new_data, 'RGB')
    # new_img.show()

    # Put image back to pasteboard
    out_stream = BytesIO()
    new_img.save(out_stream, format='png', dpi=(144, 144))
    pb.set_contents(out_stream.getvalue(), type=pasteboard.PNG)

    print("Done")
