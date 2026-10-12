# page ordering/signature arrangement logic

def impose_booklet_pages(pages: list) -> list:
    """
    Reorder logical pages into booklet print sequence without inserting
    blank cover pages or padding.

    Pages are arranged in printer order for duplex booklet printing:
    - sheet front: [last, first]
    - sheet back:  [second, second-last]
    - repeated inward

    Args:
        pages: Logical pages in natural reading order.

    Returns:
        A new list in booklet print order.

    Notes:
        This function does not insert blank pages. For best results, the input
        page count should already be a multiple of 4.
    """
    # No pages to impose.
    if not pages:
        return []

    imposed = []
    left = 0
    right = len(pages) - 1

    while left < right:
        imposed.extend([
            pages[right],      # front left
            pages[left],       # front right
        ])

        if left + 1 <= right - 1:
            imposed.extend([
                pages[left + 1],   # back left
                pages[right - 1],  # back right
            ])

        left += 2
        right -= 2

    if left == right:
        imposed.append(pages[left])

    return imposed