import os
from Ask_gpt import *
from pptx import Presentation


def read_slide(slide):
    """
    Retrieves the text content from a slide.
    :param slide: The slide object from which to extract the text.
    :return: A string containing the combined text content from the slide's text frames.
    """
    text_frames = [shape.text_frame.text for shape in slide.shapes if shape.has_text_frame]
    return '\n'.join(text_frames)


def process_slide(i, slide):
    """
    Processes a slide by writing its content to a file after a delay and obtaining a response using external processing.
    :param i: The index of the slide.
    :param slide: The text content of the slide
    :return:   The processed slide content as a string.
    """
    processed_content = "Page " + str(i) + "\n\n"
    time.sleep(20)
    response = explain_page(slide)
    print(response)
    processed_content += response
    processed_content += "\n\n-------------------------\n"
    return processed_content


def get_presentation():
    """
     Retrieves a presentation file and initializes the Presentation object.
    :return:  A dictionary containing the name of the presentation file and the Presentation object.
    """
    file_path = input("Please enter the path of the presentation file:\n")
    ptt = None
    while ptt is None:
        try:
            ptt = Presentation(file_path)
        except Exception as e:
            print("Error:", e)
            file_path = input("Please enter the correct path of the presentation file:\n")
    file_name = os.path.basename(file_path)[:-5]
    return {"name": file_name, "presentation": ptt}


def main():
    ptt = get_presentation()

    # read the slides of the presentation into list
    slides_text = []
    for slide in ptt["presentation"].slides:
        x = read_slide(slide)
        slides_text.append(x)

    # get the explanation of the slides from chat gpt
    slides_explanation = []
    for slide_num, page in enumerate(slides_text, start=1):
        slides_explanation.append(process_slide(slide_num, page))

    # write the explanation of the slides into file
    with open(ptt["name"] + ".txt", "w") as file:
        for slide in slides_explanation:
            file.write(slide)


if __name__ == '__main__':
    main()
