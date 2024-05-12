from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.xception import preprocess_input
from moviepy.video.io.VideoFileClip import VideoFileClip
import cloudinary
import cloudinary.uploader
import os

app = Flask(__name__)

# Set the path for the static files (images, CSS, JS, etc.)
STATIC_FOLDER = 'static'
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Load the pre-trained model
model = load_model('xception_deepfake_image.h5')
model1 = load_model('videomodel.h5')

cloudinary.config(
    cloud_name="winterns",
    api_key="681982841241158",
    api_secret="GefJP69Ab-enTguwrYy_mpagCH4"
)

# Load the Haarcascades face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        response_data = {'status': 'No file part'}
        return render_template('index.html', res=response_data)
    
    file = request.files['file']

    if file.filename == '':
        response_data = {'status': 'No selected file'}
        return render_template('index.html', res=response_data)
    
    file_path = os.path.join(os.getcwd(), "static/sample."+file.filename.split('.')[1])
    file.save(file_path)

    if file and allowed_image_file(file.filename):
        try:
            # Read and preprocess the image
            img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

            result = cloudinary.uploader.upload(
                file_path,
                folder="deepguard",
                resource_type="image")
            
            photo_url = result['url']

            # Ensure the image is successfully decoded
            if img is None:
                response_data = {'status': 'Failed to decode image'}
                return render_template('index.html', res=response_data)
                    
            # If the image has an alpha channel, remove it
            if img.shape[-1] == 4:
                img = img[:, :, :3]

            # Ensure the image has 3 channels (for compatibility with preprocess_input)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) if img.shape[-1] == 1 else img

            # Detect faces in the image
            faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            if len(faces) == 0:
                response_data = {'status': 'No face detected'}
                return render_template('index.html', res=response_data)

            if len(faces) > 1:
                response_data = {'status': 'Multiple faces detected'}
                return render_template('index.html', res=response_data)

            # Crop the first detected face
            x, y, w, h = faces[0]
            cropped_face = img[y:y+h, x:x+w]

            # Resize the cropped face to match the input size expected by the model
            cropped_face = cv2.resize(cropped_face, (224, 224))
            cv2.imwrite('cropped_face.jpg', cropped_face)

            cropped_face = preprocess_input(cropped_face.reshape(1, 224, 224, 3))

            # Make prediction
            prediction = model.predict(cropped_face)

            # Convert the prediction to a human-readable label
            label = 'FAKE' if prediction[0][0] > 0.5 else 'REAL'

            # Send the JSON response
            response_data = {'status': label}
            return render_template('index.html', res=response_data, p_url=photo_url)
        except Exception as e:
            response_data = {'status': f'Error processing image: {str(e)}'}
            return render_template('index.html', res=response_data)
        
    elif file and allowed_video_file(file.filename):
        try:
            output_thumbnail_path = os.path.join(os.getcwd(), "static/thumbnail.jpg")
            create_thumbnail(file_path, output_thumbnail_path)

            result = cloudinary.uploader.upload(
                output_thumbnail_path,
                folder="deepguard",
                resource_type="image")
            
            photo_url = result['url']
            
            print(f"Test video path: {file_path}")
            print(2)
            label = "FAKE" if sequence_prediction(file_path)>=0.5 else "REAL" 
            print(1)

            # Send the JSON response
            response_data = {'status': label}
            return render_template('index.html', res=response_data, p_url=photo_url)
        except Exception as e:
            response_data = {'status': f'Error processing image: {str(e)}'}
            return render_template('index.html', res=response_data)
        
    else:
        return jsonify({'status': 'Invalid file or file type not allowed'})
    

def create_thumbnail(video_path, output_path, time_in_seconds=5):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Get the frame at the specified time (in seconds)
    thumbnail_frame = video_clip.get_frame(time_in_seconds)

    # Save the frame as an image (thumbnail)
    cv2.imwrite(output_path, cv2.cvtColor(thumbnail_frame, cv2.COLOR_RGB2BGR))

        
IMG_SIZE = 224
MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048

def build_feature_extractor():
    feature_extractor = keras.applications.InceptionV3(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    preprocess_input = keras.applications.inception_v3.preprocess_input

    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    preprocessed = preprocess_input(inputs)

    outputs = feature_extractor(preprocessed)
    return keras.Model(inputs, outputs, name="feature_extractor")

feature_extractor = build_feature_extractor()

def crop_center_square(frame):
    y, x = frame.shape[0:2]
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y : start_y + min_dim, start_x : start_x + min_dim]

def load_video(path, max_frames=0, resize=(IMG_SIZE, IMG_SIZE)):
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frame = frame[:, :, [2, 1, 0]]
            frames.append(frame)

            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames)

def sequence_prediction(path):
    frames = load_video(path)
    frame_features, frame_mask = prepare_single_video(frames)
    print(3)
    return model1.predict([frame_features, frame_mask])[0]
        
def prepare_single_video(frames):
    frames = frames[None, ...]
    frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH,), dtype="bool")
    frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")

    for i, batch in enumerate(frames):
        video_length = batch.shape[0]
        length = min(MAX_SEQ_LENGTH, video_length)
        for j in range(length):
            frame_features[i, j, :] = feature_extractor.predict(batch[None, j, :])
        frame_mask[i, :length] = 1  # 1 = not masked, 0 = masked

    return frame_features, frame_mask

# Helper function to check if the image file extension is allowed
def allowed_image_file(filename):
    ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}  # Add more image extensions as needed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

# Helper function to check if the video file extension is allowed
def allowed_video_file(filename):
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov'}  # Add more video extensions as needed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
