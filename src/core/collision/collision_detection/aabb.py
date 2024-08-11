from ...utils import Pos, Rect


def aabb_algorithm(rect_1: Rect, rect_2: Rect) -> Pos | None:
    def check(rect_1: Rect, rect_2: Rect) -> bool:
        return (
            rect_1.left <= rect_2.right
            and rect_1.right >= rect_2.left
            and rect_1.top <= rect_2.bottom
            and rect_1.bottom >= rect_2.top
        )

    collide = check(rect_1, rect_2) or check(rect_2, rect_1)
    if not collide:
        return None
    return calculate_minimal_translation_vector_between_rects(rect_1, rect_2)


def calculate_minimal_translation_vector_between_rects(
    rect_1: Rect, rect_2: Rect
) -> Pos:
    candidates: list[tuple[Pos, int]] = []
    value = max(rect_2.bottom - rect_1.top, 0)
    candidates.append((Pos(0, value), abs(value)))
    value = min(rect_2.top - rect_1.bottom, 0)
    candidates.append((Pos(0, value), abs(value)))
    value = max(rect_2.right - rect_1.left, 0)
    candidates.append((Pos(value, 0), abs(value)))
    value = min(rect_2.left - rect_1.right, 0)
    candidates.append((Pos(value, 0), abs(value)))
    return sorted(candidates, key=lambda x: x[1])[0][0]
