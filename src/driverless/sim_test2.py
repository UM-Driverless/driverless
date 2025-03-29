import numpy as np
import cv2
import multiprocessing

from driverless.utils.fsds_loader import load_fsds
fsds = load_fsds()
sim_client1 = fsds.client.FSDSClient()
sim_client1.confirmConnection()  # Example method to confirm connection

simulator_car_controls = fsds.CarControls()

def worker(cam_queue):
    client = fsds.FSDSClient() # To get the image. WARNING: THIS IS NOT PICKLABLE, SO IT CANNOT BE PASSED TO A MULTIPROCESSING FUNCTION. HOWEVER, IT CAN BE DEFINED AND USED INSIDE THE WORKER FUNCTION ITSELF
    # Check network connection, exit if not connected
    client.confirmConnection()
    while True:
        [img] = client.simGetImages([fsds.ImageRequest(camera_name = 'cam1', image_type = fsds.ImageType.Scene, pixels_as_float = False, compress = False)], vehicle_name = 'FSCar')
        img_buffer = np.frombuffer(img.image_data_uint8, dtype=np.uint8)
        image = img_buffer.reshape(img.height, img.width, 3)
        cam_queue.put(image)

if __name__ == '__main__':
    cam_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=worker, args=(cam_queue,), daemon=True)
    process.start()
    
    # Show
    while True:
        if not cam_queue.empty():
            image = cam_queue.get()
            cv2.imshow('Camera Feed', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break