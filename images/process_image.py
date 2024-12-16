import cv2
import os

face_cascade = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')

for dirpath, dirnames, filenames in os.walk('images'):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        print(f"Processing file: {file_path}")

        # Check if it is a file
        if os.path.isfile(file_path):
            try:
                # Read the image
                image = cv2.imread(file_path)

                # Skip if the file is not an image
                if image is None:
                    print(f"Skipping non-image file: {file_path}")
                    continue

                # Convert to grayscale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect faces
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

                # Print results
                if len(faces) > 0:
                    print(f"Faces detected in file: {file_path}")
                else:
                    print(f"No faces detected in file: {file_path}")
                    # delete the file
                    #os.remove(file_path)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

print("Processing complete.")
