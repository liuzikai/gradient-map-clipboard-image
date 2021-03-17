import pasteboard
import io
from PIL import Image
import numpy as np

BG = [58, 63, 74]
FG = [221, 221, 221]

pb = pasteboard.Pasteboard()
in_bytes = pb.get_contents(pasteboard.PNG)

if in_bytes is None:
    print("Clipboard doesn't contain an image")

else:
    in_stream = io.BytesIO(in_bytes)
    img: Image.Image = Image.open(in_stream)

    data = np.array(img.getdata())  # RGBA

    new_data = np.empty((data.shape[0], 3), dtype=np.uint8)  # RGB

    # Apply gradient map on the image
    # Reference: https://community.adobe.com/t5/photoshop/what-is-the-mathmatical-formula-of-gradient-map/td-p/10502214
    for i in range(data.shape[0]):
        lum = (float(data[i][0]) / 255) * 0.30 + (float(data[i][1]) / 255) * 0.59 + (float(data[i][2]) / 255) * 0.11
        new_data[i] = np.array([(1 - lum) * FG[0] + lum * BG[0],
                                (1 - lum) * FG[1] + lum * BG[1],
                                (1 - lum) * FG[2] + lum * BG[2]], dtype=np.uint8)

    new_data = new_data.reshape((img.height, img.width, 3))
    new_img = Image.fromarray(new_data, 'RGB')
    # new_img.show()

    # Put image back to pasteboard
    out_stream = io.BytesIO()
    new_img.save(out_stream, format='png', dpi=(144, 144))
    pb.set_contents(out_stream.getvalue(), type=pasteboard.PNG)

    print("Done")
