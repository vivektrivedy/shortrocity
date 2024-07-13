import captacity
print("Successfully imported captacity")

fn = '/Users/vivektrivedy/Downloads/ContentPal - 8 July 2024.mp4'
captacity.add_captions(
    video_file=fn,
    output_file="my_short_with_captions.mp4",
    print_info=True,
    font = "super-boys-font/SuperBoys-vmW67.ttf",
    font_size = 130,
    font_color = "purple",

    stroke_width = 3,
    stroke_color = "black",

    shadow_strength = 1.0,
    shadow_blur = 0.1,

    highlight_current_word = True,
    word_highlight_color = "orange",

    line_count=1,

    padding = 50,
)