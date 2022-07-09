def map(captures, transform):
    resized_captures = dict()
    for name, capture in captures.items():
        if capture:
            capture = transform(name, capture)
        resized_captures[name] = capture

    return resized_captures

def reduce(captures, reduce, initial):

    current = initial
    for name, capture in captures.items():
        current = reduce(name, capture, initial)
    return current