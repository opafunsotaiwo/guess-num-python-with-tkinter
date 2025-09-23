import cv2
import numpy as np


# Read and display an image
def basic_image_operations():
    # Read image
    img = cv2.imread('image.jpg')

    # Check if image loaded successfully
    if img is None:
        print("Error: Image not found! Using sample image instead.")
        # Create a sample image
        img = np.zeros((300, 400, 3), dtype=np.uint8)
        cv2.putText(img, 'Sample Image', (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Get image properties
    height, width, channels = img.shape
    print(f"Image dimensions: {width}x{height}")

    # Display image
    cv2.imshow('Original Image', img)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale Image', gray)

    # Wait for key press and close windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()


basic_image_operations()