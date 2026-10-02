
A web-based image contour analysis tool built with **Python, OpenCV, NumPy, and Streamlit**.

The application allows users to upload an image, adjust image-processing parameters, detect contours, and analyze the detected objects through visual and numerical outputs.

## Features

* Upload JPG, JPEG, and PNG images
* Preview the uploaded image
* Convert images to grayscale
* Apply Gaussian Blur
* Perform Canny Edge Detection
* Apply Morphological Closing
* Detect external contours
* Filter contours based on:

  * Minimum contour area
  * Maximum aspect ratio
* Draw detected contours
* Generate bounding boxes
* Display contour numbers and areas
* Calculate:

  * Contour area
  * Area percentage
  * Perimeter
  * Bounding box
  * Aspect ratio
* Interactive processing controls through the Streamlit sidebar

## Processing Pipeline

```text
Image Upload
     ↓
Grayscale Conversion
     ↓
Gaussian Blur
     ↓
Canny Edge Detection
     ↓
Morphological Closing
     ↓
Contour Detection
     ↓
Contour Filtering
     ↓
Contour Analysis
     ↓
Visual + Numerical Results
```

## Technologies Used

* Python
* OpenCV
* NumPy
* Streamlit

## Project Structure

```text
OpenCV-Contour-Analyzer/
│
├── app.py
├── requirements.txt
└── README.md
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/02-Yuvraj/OpenCV-Contour-Analyzer.git
```

Navigate to the project directory:

```bash
cd OpenCV-Contour-Analyzer
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Open the application.
2. Upload an image using the **Browse** button.
3. Adjust the processing parameters from the sidebar.
4. View the Canny edge output.
5. View the morphologically closed edge output.
6. View the detected contours and bounding boxes.
7. Review the numerical contour information.

## Parameters

| Parameter             | Purpose                                     |
| --------------------- | ------------------------------------------- |
| Gaussian Blur Kernel  | Controls image smoothing                    |
| Canny Lower Threshold | Sets the lower edge-detection threshold     |
| Canny Upper Threshold | Sets the upper edge-detection threshold     |
| Morphological Kernel  | Controls morphological closing              |
| Minimum Contour Area  | Removes contours below the selected area    |
| Maximum Aspect Ratio  | Filters contours based on shape proportions |

## Use Cases

This tool can be used for experimentation and analysis in areas such as:

* Computer vision
* Image processing
* Object boundary detection
* Shape analysis
* Image preprocessing
* Contour-based segmentation

## License

This project is available for educational and personal use.
