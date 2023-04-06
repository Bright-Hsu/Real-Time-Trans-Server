import numpy as np
import urllib.request
import cv2


if __name__ == '__main__':
    # read the image url
    url = 'https://media.geeksforgeeks.org/wp-content/uploads/20211003151646/geeks14.png'

    with urllib.request.urlopen(url) as resp:
        # read image as an numpy array
        image = np.asarray(bytearray(resp.read()), dtype="uint8")

        # use imdecode function
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # display image
        cv2.imshow("Image", image)
        cv2.waitKey(0)