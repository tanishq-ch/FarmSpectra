import cv2
import numpy as np
from ultralytics import YOLO

class WheatRustDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def calculate_exg(self, image_rgb):
        img = image_rgb.astype(float)
        b, g, r = img[:, :, 2], img[:, :, 1], img[:, :, 0]
        exg = 2 * g - r - b
        exg_norm = cv2.normalize(exg, None, 0, 255, cv2.NORM_MINMAX).astype("uint8")
        return 255 - exg_norm

    def detect(self, image_rgb):
        results = self.model.predict(
    	source=image_rgb,
    	imgsz=1024,
    	retina_masks=True,
    	conf=0.15,          # <-- IMPORTANT
    	verbose=False
		)[0]


        overlay = image_rgb.copy()
        boxes = []

        if results.masks is not None:
            masks = results.masks.data.cpu().numpy()
            combined_mask = np.sum(masks, axis=0)
            combined_mask = cv2.resize(combined_mask, (image_rgb.shape[1], image_rgb.shape[0]))
            overlay[combined_mask > 0.5] = [255, 0, 0]
            boxes = results.boxes.xyxy.cpu().numpy()

        ai_view = cv2.addWeighted(image_rgb, 0.7, overlay, 0.3, 0)

        exg = self.calculate_exg(image_rgb)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
        exg_enhanced = clahe.apply(exg)

        heatmap = cv2.applyColorMap(exg_enhanced, cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

        return ai_view, heatmap, boxes
