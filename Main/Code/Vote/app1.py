from flask import Flask, render_template, request, jsonify
import csv
import random
import os

app = Flask(__name__)

# CSV file to store user data
CSV_FILE = 'users_data.csv'
IMAGE_FOLDER = '../Generate_images/Images/'

@app.route('/')
def index():
    random_image = get_random_image()
    return render_template('index1.html', random_image=random_image)

@app.route('/record_choice', methods=['POST'])
def record_choice():
    user_choice = request.form.get('choice')
    image_filename = request.form.get('image_filename')

    # Write user choice and image filename to the CSV file
    with open(CSV_FILE, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([user_choice, image_filename])

    return 'Choice recorded successfully'

@app.route('/get_random_image', methods=['GET'])
def get_random_image():
    random_image = choose_random_image()
    return jsonify({'random_image': random_image})

def choose_random_image():
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
    if image_files:
        random_image_filename = random.choice(image_files)
        return os.path.join('../Generate_images/Images/', random_image_filename[0:])
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
