import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from ultralytics import YOLO
import math

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Calculation functions...

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_ppi(pixel_height, real_height_cm):
    real_height_in = real_height_cm / 2.54
    return pixel_height / real_height_in

def calculate_real_world_distance(pixel_distance, ppi):
    inches_per_pixel = 1 / ppi
    return pixel_distance * inches_per_pixel * 2.54

@app.post("/process-image")
async def process_image(XFile: UploadFile, User_Height_CM: float): 
    try:
        contents = await XFile.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        model = YOLO('yolov8m-pose.pt')
        results = model(img)

        
        x1, y1, x2, y2 = 0, 0, 0, 0
        for detection in results:
            boxes = detection.boxes.xyxy.cpu().numpy()
            x1, y1, x2, y2 = boxes[0]
            pixel_height = y2 - y1  # Calculate pixel height of the person

        # Calculate PPI
        ppi = calculate_ppi(pixel_height, User_Height_CM)

        for detection in results:
            keypoints = detection.keypoints.cpu().numpy()  
            xy_array = keypoints.xy  
            nose_x = xy_array[0][0][0]
            nose_y = xy_array[0][0][1]
            right_ear_x = xy_array[0][3][0]
            right_ear_y = xy_array[0][3][1]
            left_ear_x = xy_array[0][4][0]
            left_ear_y = xy_array[0][4][1]
            right_shoulder_x = xy_array[0][5][0]
            right_shoulder_y = xy_array[0][5][1]
            left_shoulder_x = xy_array[0][6][0]
            left_shoulder_y = xy_array[0][6][1] 
            left_elbow_x = xy_array[0][8][0]
            left_elbow_y = xy_array[0][8][1] 
            left_wrist_x = xy_array[0][10][0]
            left_wrist_y = xy_array[0][10][1]
            right_hip_x = xy_array[0][11][0]
            left_hip_x = xy_array[0][12][0]
            left_ankle_x = xy_array[0][16][0]
            left_ankle_y = xy_array[0][16][1]

        #------------------------Claculation--------------------------------------------
        # Modify shoulder position
        left_shoulder_x= left_shoulder_x-47
        left_shoulder_y= left_shoulder_y-42
        right_shoulder_x=right_shoulder_x+47
        right_shoulder_y=right_shoulder_y-42

        # Modify hip position
        left_hip_x=left_hip_x-51.50
        right_hip_x=right_hip_x+51.50

        #distance between Ear to ear
        EarToEar_pixel_distance = calculate_distance(left_ear_x, left_ear_y, right_ear_x, right_ear_y)
        EarToEar_real_world_distance_cm = calculate_real_world_distance(EarToEar_pixel_distance, ppi)
        EarToEar_measurements=EarToEar_real_world_distance_cm; 

        # distance between Shoulder to Shoulder
        Sh_pixel_distance = calculate_distance(left_shoulder_x, left_shoulder_y, right_shoulder_x, right_shoulder_y)
        Sh_real_world_distance_cm = calculate_real_world_distance(Sh_pixel_distance, ppi)
        Shoulders_measurements=Sh_real_world_distance_cm; 

        # distance between Shoulder to elbow
        ShEl_pixel_distance = calculate_distance(left_shoulder_x, left_shoulder_y, left_elbow_x, left_elbow_y)
        ShEl_real_world_distance_cm = calculate_real_world_distance(ShEl_pixel_distance, ppi)
        ShEl_measurements=ShEl_real_world_distance_cm; 

        # distance between Elbow to wrist
        ElWr_pixel_distance = calculate_distance(left_elbow_x, left_elbow_y, left_wrist_x, left_wrist_y)
        ElWr_real_world_distance_cm = calculate_real_world_distance(ElWr_pixel_distance, ppi)
        ElWr_measurements=ElWr_real_world_distance_cm; 

        # distance between Nose to ankle 
        noseAn_pixel_distance = calculate_distance(nose_x, nose_y, left_ankle_x, left_ankle_y)
        noseAn_real_world_distance_cm = calculate_real_world_distance(noseAn_pixel_distance, ppi)
        noseAn_measurements=noseAn_real_world_distance_cm; 
        
        #calculation of hips width
        hipMeasurements=EarToEar_measurements*6.5; 
        #cal arm
        Arms=ShEl_measurements + ElWr_measurements; 
        

        # Return placeholder results  
        return {
                "Shoulder": round(Shoulders_measurements, 2),
                "Arm": round(Arms, 2),
                "Hips": round(hipMeasurements, 2),
                "Height": round(noseAn_measurements, 2)    
            }
    except Exception as e:
        logger.error(f"Failed to process image: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to process image", "error": str(e)}
        )       
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": f"An internal server error occurred: {exc}"}
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
