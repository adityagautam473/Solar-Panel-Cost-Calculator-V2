import cv2
import numpy as np
from PIL import Image
import io


def analyze_rooftop(image_bytes):
    try:
        # Load image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Noise reduction
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return {"error": "No rooftop detected"}

        # Assume the largest contour is the rooftop
        rooftop_contour = max(contours, key=cv2.contourArea)

        # Pixel area
        pixel_area = cv2.contourArea(rooftop_contour)

        # Heuristic conversion (tunable)
        # Assume ~0.04 m² per pixel (depends on image scale)
        usable_area_m2 = round(pixel_area * 0.04, 2)

        # Each panel ≈ 2 m²
        recommended_panels = int(usable_area_m2 // 2)

        return {
            "usable_area_m2": usable_area_m2,
            "recommended_panels": recommended_panels
        }

    except Exception as e:
        return {
            "error": "Rooftop analysis failed",
            "details": str(e)
        }
