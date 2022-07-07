def map(captures, transform):
    resized_captures = dict()
    for name, capture in captures.items():
        capture.image = transform(capture.image)
        resized_captures[name] = capture

    return resized_captures