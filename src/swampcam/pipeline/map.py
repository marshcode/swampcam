def map(captures, transform):
    resized_captures = dict()
    for name, capture in captures.items():
        capture = transform(name, capture)
        resized_captures[name] = capture

    return resized_captures