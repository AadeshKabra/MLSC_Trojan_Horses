# FLASKQUEST: Flask-based Question Generation from YouTube Videos

## Project Description
Our project is a Flask-based web application that can generate quiz questions from YouTube videos. Users can input the URL of a YouTube video, and our application will extract the audio from the video and convert it into text. We then use GenR AI API to check the grammar of the extracted text and correct any errors. After that, we use GenR AI's Generate Questions circuit element to generate quiz questions from the corrected text. Our application also supports multi-language translations of the generated questions, allowing users to create quizzes in different languages using GenR AI's translate text circuit element.

## Installation
To run the application locally, you must have Python 3.7 or later installed on your machine. You can install the required dependencies by running:

## Usage
To start the application, run the following command in your terminal:
python app.py

Then, open your web browser and navigate to http://localhost:5000. You should see the FLASKQUEST homepage, where you can enter a YouTube video link to generate quiz questions.

## Credits
FLASKQUEST was developed by - 
Ketan Gangwal
Aadesh Kabra
Ashutosh Kabra
Kshitij Chaudhari

Special Thanks to Developers of Genr.AI API. 
https://docs.genr.ai/docs/genr/05863e3f97d8f-genr-product-info
