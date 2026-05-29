import tempfile


def save_uploaded_video(uploaded_file):

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    temp_file.write(
        uploaded_file.read()
    )

    temp_file.close()

    return temp_file.name