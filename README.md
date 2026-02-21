# Image Color Analyzer

A Flask web application that analyzes uploaded images to extract dominant colors using K-Means clustering algorithm. The application identifies color names and calculates their percentage distribution in the image.

## Features

- **Image Upload**: Supports JPEG, PNG, GIF, BMP, and WEBP formats
- **Color Extraction**: Uses K-Means clustering to identify dominant colors
- **Color Naming**: Automatically maps RGB values to nearest CSS color names
- **Percentage Analysis**: Calculates the proportional representation of each color
- **Responsive UI**: Built with Flask-Bootstrap for clean interface
- **Secure File Handling**: UUID-based filename generation to prevent conflicts

## Installation

Installation
1. Clone the repository
git clone <repository-url>
cd image-color-analyzer
2. Install required dependencies
pip install flask flask-wtf flask-bootstrap numpy pillow pandas scikit-learn webcolors python-dotenv werkzeug
3. Create a .env file in the project root
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216
4. Run the application
python app.py
Usage

Navigate to:

http://localhost:5000

Upload an image file using the form.

Specify the number of dominant colors to extract (integer value).

View the results, including:

Color name

RGB values

Hex code

Pixel count

Percentage distribution

Project Structure
.
├── app.py                 # Main Flask application
├── static/                # Uploaded images storage
├── templates/             # HTML templates
│   └── index.html
├── .env                   # Environment variables
└── README.md              # This file
Dependencies
Package	Purpose
Flask	Web framework
Flask-WTF	Form handling and CSRF protection
Flask-Bootstrap	UI styling
NumPy	Numerical operations
Pillow (PIL)	Image processing
Pandas	Data manipulation
scikit-learn	K-Means clustering
webcolors	Color name mapping
python-dotenv	Environment variable management
werkzeug	Secure file handling
API Endpoints
GET /

Renders the upload form and displays analysis results after submission.

Form Parameters

file – Image file (JPEG, PNG, GIF, BMP, WEBP)

number – Integer specifying number of colors to extract

Core Functions
im_process(filename, number_of_clusters)

Processes the uploaded image and returns a DataFrame with color analysis.

Parameters:

filename – Path to the image file

number_of_clusters – Number of dominant colors to extract

Returns:
Pandas DataFrame with columns:

name – CSS color name

color – RGB tuple

count – Number of pixels

hex – Hexadecimal color code

percentage – Color distribution percentage

get_colour_name(requested_colour)

Maps RGB values to CSS color names.

closest_colour(requested_colour)

Finds the nearest named color using Euclidean distance in RGB space.

Configuration
Variable	Description	Default
SECRET_KEY	Flask session security key	Required
UPLOAD_FOLDER	Directory for uploaded images	static/
MAX_CONTENT_LENGTH	Maximum file upload size	From .env
Error Handling

Unsupported image formats raise ValueError

Image processing errors are logged and raised with descriptive messages

Secure filename handling prevents directory traversal attacks

License

MIT License

Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
