
import cv2
import numpy as np
import streamlit as st


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Image Contour Analyzer",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("Image Contour Analyzer")

st.write(
    "Upload an image and adjust the OpenCV processing "
    "parameters to analyze its contours."
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Processing Parameters")


# ==========================================
# IMAGE UPLOAD
# ==========================================

uploaded_file = st.sidebar.file_uploader(
    "Browse and upload an image",
    type=["jpg", "jpeg", "png"]
)


# ==========================================
# PROCESSING CONTROLS
# ==========================================

st.sidebar.subheader("Gaussian Blur")

blur_kernel_size = st.sidebar.slider(
    "Kernel Size",
    min_value=1,
    max_value=15,
    value=5,
    step=2,
    key="blur_kernel_size"
)


st.sidebar.subheader("Canny Edge Detection")

canny_lower = st.sidebar.slider(
    "Lower Threshold",
    min_value=0,
    max_value=255,
    value=50,
    key="canny_lower"
)

canny_upper = st.sidebar.slider(
    "Upper Threshold",
    min_value=0,
    max_value=255,
    value=150,
    key="canny_upper"
)


st.sidebar.subheader("Morphological Closing")

morph_kernel_size = st.sidebar.slider(
    "Kernel Size",
    min_value=1,
    max_value=15,
    value=5,
    step=2,
    key="morph_kernel_size"
)


st.sidebar.subheader("Contour Filtering")

min_area_percentage = st.sidebar.slider(
    "Minimum Contour Area (%)",
    min_value=0.01,
    max_value=5.0,
    value=0.03,
    step=0.01,
    key="min_area_percentage"
)

max_aspect_ratio = st.sidebar.slider(
    "Maximum Aspect Ratio",
    min_value=0.5,
    max_value=10.0,
    value=4.0,
    step=0.1,
    key="max_aspect_ratio"
)


# ==========================================
# PROCESS IMAGE
# ==========================================

if uploaded_file is not None:

    # ------------------------------------------
    # READ IMAGE
    # ------------------------------------------

    file_bytes = uploaded_file.read()

    image = cv2.imdecode(
        np.frombuffer(file_bytes, np.uint8),
        cv2.IMREAD_COLOR
    )


    # ------------------------------------------
    # CHECK IMAGE
    # ------------------------------------------

    if image is None:

        st.error("Could not read the uploaded image.")

        st.stop()


    # ==========================================
    # SIDEBAR IMAGE PREVIEW
    # ==========================================

    st.sidebar.subheader("Uploaded Image")

    st.sidebar.image(
        cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        ),
        use_container_width=True
    )


    # ==========================================
    # GRAYSCALE CONVERSION
    # ==========================================

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # ==========================================
    # GAUSSIAN BLUR
    # ==========================================

    blur = cv2.GaussianBlur(
        gray,
        (blur_kernel_size, blur_kernel_size),
        0
    )


    # ==========================================
    # CANNY EDGE DETECTION
    # ==========================================

    edges = cv2.Canny(
        blur,
        canny_lower,
        canny_upper
    )


    # ==========================================
    # MORPHOLOGICAL CLOSING
    # ==========================================

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (
            morph_kernel_size,
            morph_kernel_size
        )
    )


    closed = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        kernel
    )


    # ==========================================
    # FIND CONTOURS
    # ==========================================

    contours, hierarchy = cv2.findContours(
        closed,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    # ==========================================
    # IMAGE INFORMATION
    # ==========================================

    height, width = image.shape[:2]

    image_area = height * width


    # ==========================================
    # ADAPTIVE MINIMUM CONTOUR AREA
    # ==========================================

    min_area = image_area * (
        min_area_percentage / 100
    )


    # ==========================================
    # STORE FILTERED CONTOURS
    # ==========================================

    filtered_contours = []

    contour_information = []


    # ==========================================
    # PROCESS EACH CONTOUR
    # ==========================================

    for i, contour in enumerate(contours):

        # --------------------------------------
        # CONTOUR AREA
        # --------------------------------------

        area = cv2.contourArea(
            contour
        )


        # --------------------------------------
        # BOUNDING BOX
        # --------------------------------------

        x, y, w, h = cv2.boundingRect(
            contour
        )


        # --------------------------------------
        # AVOID DIVISION BY ZERO
        # --------------------------------------

        if h == 0:
            continue


        # --------------------------------------
        # ASPECT RATIO
        # --------------------------------------

        aspect_ratio = w / h


        # --------------------------------------
        # FILTER CONTOUR
        # --------------------------------------

        if (
            area > min_area
            and aspect_ratio < max_aspect_ratio
        ):

            filtered_contours.append(
                contour
            )


            # ----------------------------------
            # PERIMETER
            # ----------------------------------

            perimeter = cv2.arcLength(
                contour,
                True
            )


            # ----------------------------------
            # AREA PERCENTAGE
            # ----------------------------------

            area_percentage = (
                area / image_area
            ) * 100


            # ----------------------------------
            # STORE INFORMATION
            # ----------------------------------

            contour_information.append({

                "number": i + 1,

                "area": area,

                "area_percentage": area_percentage,

                "perimeter": perimeter,

                "x": x,

                "y": y,

                "w": w,

                "h": h,

                "aspect_ratio": aspect_ratio
            })


            # ----------------------------------
            # DRAW GREEN CONTOUR
            # ----------------------------------

            cv2.drawContours(
                image,
                [contour],
                -1,
                (0, 255, 0),
                2
            )


            # ----------------------------------
            # DRAW BLUE BOUNDING BOX
            # ----------------------------------

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )


            # ----------------------------------
            # DISPLAY CONTOUR NUMBER + AREA
            # ----------------------------------

            cv2.putText(
                image,
                f"C{i + 1}: {area:.1f}",
                (x, max(y - 10, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1
            )


    # ==========================================
    # PREPROCESSING RESULTS
    # ==========================================

    st.subheader("Preprocessing Results")


    col1, col2 = st.columns(2)


    with col1:

        st.write("Canny Edges")

        st.image(
            edges,
            channels="GRAY",
            use_container_width=True
        )


    with col2:

        st.write("Closed Edges")

        st.image(
            closed,
            channels="GRAY",
            use_container_width=True
        )


    # ==========================================
    # FINAL RESULT
    # ==========================================

    st.subheader("Detected Contours")


    st.image(
        cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        ),
        caption="Detected Contours and Bounding Boxes",
        use_container_width=True
    )


    # ==========================================
    # IMAGE INFORMATION
    # ==========================================

    st.subheader("Image Information")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Contours Detected",
            len(contours)
        )


    with col2:

        st.metric(
            "Contours After Filtering",
            len(filtered_contours)
        )


    with col3:

        st.metric(
            "Image Dimensions",
            f"{width} × {height}"
        )


    st.write(
        "Image area:",
        image_area
    )


    st.write(
        "Minimum contour area:",
        min_area
    )


    # ==========================================
    # CURRENT SETTINGS
    # ==========================================

    st.subheader("Current Processing Settings")


    st.write(
        "Gaussian Blur Kernel:",
        f"{blur_kernel_size} × {blur_kernel_size}"
    )


    st.write(
        "Canny Thresholds:",
        canny_lower,
        "-",
        canny_upper
    )


    st.write(
        "Morphological Kernel:",
        f"{morph_kernel_size} × {morph_kernel_size}"
    )


    st.write(
        "Minimum Contour Area:",
        f"{min_area_percentage}%"
    )


    st.write(
        "Maximum Aspect Ratio:",
        max_aspect_ratio
    )


    # ==========================================
    # FILTERED CONTOUR INFORMATION
    # ==========================================

    st.subheader("Filtered Contour Information")


    for contour in contour_information:

        st.write(
            f"### Contour {contour['number']}"
        )


        st.write(
            "Area:",
            contour["area"]
        )


        st.write(
            "Area percentage:",
            contour["area_percentage"],
            "%"
        )


        st.write(
            "Perimeter:",
            contour["perimeter"]
        )


        st.write(
            "Bounding Box:",
            contour["x"],
            contour["y"],
            contour["w"],
            contour["h"]
        )


        st.write(
            "Aspect Ratio:",
            contour["aspect_ratio"]
        )