# page ordering/signature arrangement logic

def impose_booklet_pages(pages: list) -> list:
    """
    Reorder logical pages into printer-ready booklet sequence.

    This function performs page imposition for saddle-stitched booklet printing:
    pages are arranged so that, after duplex printing, stacking, and folding,
    the pages appear in normal reading order.

    The algorithm:
    - Adds a blank cover page at the start of the booklet.
    - Ensures the total page count is a multiple of 4 (required for booklet signatures)
      by appending `None` placeholders for blank pages.
    - Uses a two-pointer strategy (`left` from start, `right` from end) to emit
      pages in groups of four corresponding to one physical sheet (front + back):
        1) outer front:  [last, first]
        2) outer back:   [second, second-last]
    - Repeats inward until all sheets are imposed.

    Args:
        pages: Ordered list of logical page objects in natural reading order.
               Elements may be any page-like object understood by the caller's
               rendering pipeline.

    Returns:
        A new list in booklet print order. `None` entries represent inserted blank
        pages needed to pad signatures to multiples of 4.

    Example:
        Input pages: [1, 2, 3, 4, 5]
        Padded to:   [None, 1, 2, 3, 4, 5, None, None]
        Output:      [None, 1, 2, None, None, 3, 4, 5]
    """
    # No pages to impose.
    if not pages:
        return []

    padded_pages = pages.copy()

    # the cover page should always be blank for booklets
    padded_pages.insert(0, None)

    # Pad to a multiple of 4 because each folded sheet contributes 4 booklet pages.
    while len(padded_pages) % 4 != 0:
        padded_pages.append(None)

    imposed = []
    left = 0 # beginning of list
    right = len(padded_pages) - 1 # end of list

    # Build imposed order one sheet at a time (4 logical pages per physical sheet).
    while left < right:
        imposed.extend([
            padded_pages[right],      # outer-front left
            padded_pages[left],       # outer-front right
            padded_pages[left + 1],   # outer-back left
            padded_pages[right - 1],  # outer-back right
        ])
        left += 2
        right -= 2

    return imposed