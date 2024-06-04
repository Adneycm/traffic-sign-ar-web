import requests
from PIL import Image
from roboflow import Roboflow

def overlay_image_on_bad_traffic_signs(filepath, overlay_path, model, confidence=40, overlap=30):
    print(f"filepath in the function: {filepath}")
    
    # infer on a local image
    response = model.predict(filepath, confidence=confidence, overlap=overlap).json()

    # Load the original image and the overlay image
    original_image = Image.open(filepath)
    overlay_image = Image.open(overlay_path)

    # Ensure the overlay image has an alpha channel
    if overlay_image.mode != 'RGBA':
        overlay_image = overlay_image.convert('RGBA')

    # Draw on the original image
    for prediction in response['predictions']:
        if prediction['class'] == 'Bad-Traffic-Sign' and prediction['confidence'] > 0.84:
            # Get the bounding box coordinates
            x, y, width, height = prediction['x'], prediction['y'], prediction['width'], prediction['height']
            left, top = x - width / 2, y - height / 2

            # Resize the overlay image to fit the bounding box
            resized_overlay = overlay_image.resize((int(width), int(height)), Image.LANCZOS)

            # Paste the overlay image onto the original image
            original_image.paste(resized_overlay, (int(left), int(top)), resized_overlay)

    # Save the modified image
    output_path = filepath.replace('.jpg', '_prediction.jpg').replace('.jpeg', '_prediction.jpg').replace('.png', '_prediction.png')
    original_image.save(output_path)
    print(f"Modified image saved at {output_path}")

    return output_path
