"""
MAIN script to run all the others. Shall contain the main classes, top level functions etc.

# REFERENCES
https://github.com/UM-Driverless/Deteccion_conos/tree/Test_Portatil
vulture . --min-confidence 100

- Wanted to make visualize work in a thread and for any resolution, but now it works for any resolution, don't know why, and it's always about 3ms so it's not worth it for now.

# STUFF
To stop: Ctrl+C in the terminal

# INFO
- In ruben laptop:
    - torch.hub.load(): YOLOv5 🚀 2023-1-31 Python-3.10.8 torch-1.13.0+cu117 CUDA:0 (NVIDIA GeForce GTX 1650, 3904MiB)
    - ( torch.hub.load(): YOLOv5 🚀 2023-4-1 Python-3.10.6 torch-1.11.0+cu102 CUDA:0 (NVIDIA GeForce GTX 1650, 3904MiB) )
- ORIN VERSIONS:
    - Jetpack 5.1.1 (installs CUDA11.4), pytorch 2.0.0+nv23.05 (for arm64 with cuda), torchvision version 0.15.1 with cuda, for that run this code:
        ```bash
        $ sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libopenblas-dev libavcodec-dev libavformat-dev libswscale-dev
        $ git clone --branch v0.15.1 https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
        $ cd torchvision
        $ export BUILD_VERSION=0.15.1 # where 0.x.0 is the torchvision version  
        $ python3 setup.py install --user
        ```
    
- S_b: Body Coordinate system, origin in camera focal point:
    - X: Forwards
    - Y: Left
    - Z: Up

"""

if __name__ == '__main__': # multiprocessing creates child processes that import this file, with __name__ = '__mp_main__'
    import numpy as np
    import matplotlib.pyplot as plt # For representation of time consumed
    from my_utils.time_counter import Time_Counter
    
    from driverless.car import Car

    from driverless.visualization_utils.visualizer_yolo_det import Visualizer

    # INITIALIZE things
    dv_car = Car()
    
    # READ TIMES
    timer = Time_Counter()

    ## Data visualization
    visualizer = Visualizer()

    # Main loop ------------------------
    try:
        print("Starting main loop...")
        while True:
            timer.add_time()

            dv_car.get_data()
            
            timer.add_time()
            # Detect cones
            print(f'--------Loop counter:   {dv_car.loop_counter}--------')
            dv_car.cones = dv_car.detector.detect_cones(dv_car.image, dv_car.state)
            timer.add_time()
            dv_car.agent.get_target(dv_car.cones, dv_car.state, dv_car.actuation)
            timer.add_time()
            dv_car.comm.send_actuation(dv_car.actuation)
            # VISUALIZE
            # TODO add parameters to class
            timer.add_time()
            visualizer.visualize(dv_car.actuation,
                                dv_car.state,
                                dv_car.image,
                                dv_car.cones,
                                save_frames=False,
                                visualize=dv_car.config['VISUALIZE'])

            if dv_car.config['LOGGER']:
                dv_car.logger.write(f'Iter {dv_car.loop_counter}, FPS: {dv_car.state["fps"]:.1f}, STATE: {dv_car.state}, ACTUATION: {dv_car.actuation}')
            # Save times
            timer.add_time()
            dv_car.state['fps'] = 1 / (timer.recorded_times[-1] - timer.recorded_times[0])
            timer.new_iter()
            dv_car.loop_counter += 1
            
            # TESTING
            # print(f"STEER: {dv_car.actuation['steer']} -> {int((dv_car.actuation['steer'] + 1) / 2 * 90)}")
    finally:
        print("------------")
        dv_car.stop()
        if dv_car.config['LOGGER']:
            dv_car.logger.write(f'{np.array(timer.times_integrated) / timer.loop_counter}')
        ## Plot the times
        fig = plt.figure(figsize=(12, 4))
        plt.bar(['get_data()','detect_cones()','calculate_actuation()','send_actuation'],np.array(timer.times_integrated) / timer.loop_counter)
        plt.ylabel("Average time taken [s]")
        plt.figtext(.8,.8,f'{1/(timer.times_integrated[-1] - timer.times_integrated[0]):.2f}Hz')
        plt.title("Execution time per section of main loop")
        plt.savefig("logs/times.png")
        

