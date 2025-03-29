import numpy as np
import cv2

from driverless.utils.fsds_loader import load_fsds
fsds = load_fsds()
sim_client1 = fsds.client.FSDSClient()
sim_client1.confirmConnection()  # Example method to confirm connection

simulator_car_controls = fsds.CarControls()

while True:
    while True:
        [img] = sim_client1.simGetImages([fsds.ImageRequest(camera_name = 'cam1', image_type = fsds.ImageType.Scene, pixels_as_float = False, compress = False)], vehicle_name = 'FSCar')
        img_buffer = np.frombuffer(img.image_data_uint8, dtype=np.uint8)
        image = img_buffer.reshape(img.height, img.width, 3)
        # show
        cv2.imshow('Camera Feed', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break