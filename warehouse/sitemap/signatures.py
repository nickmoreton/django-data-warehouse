from dataclasses import dataclass, field

from bs4 import BeautifulSoup


@dataclass
class SignatureBuilder:
    """Builds a list of signatures from a BeautifulSoup object.
    The signatures are a list of tags that can be used to identify patterns in the HTML.
    The signatures are built from the top level tags of the soup object starting from the parent_tag using recursion.
    A possible use case is to use the signatures as a dictionary key to provide a mapping to a function or other data.

    As this produces a list of signatures for a single HTML page, it is recommended to concatenate the signatures
    from multiple pages to get a more complete list of signatures.
    You'll likely want to remove duplicates from the list of signatures as well.

    Args:
        soup (BeautifulSoup): BeautifulSoup object
        parent_tag (str): Parent tag to start from. Defaults to None.

    Returns:
        SignatureBuilder: Returns a SignatureBuilder object.

    Examples:
        >>> soup = BeautifulSoup(html_content, 'html.parser')
        >>> signature_builder = SignatureBuilder(soup, 'main').run()
        >>> signature_builder.get_signatures
        ['h1', 'div>div>h2', 'div>div>p', 'div>h1', 'p', 'p']
        >>> signature_builder.get_unique_signatures
        ['h1', 'div>div>h2', 'div>div>p', 'div>h1', 'p']

    Debug:
        >>> signature_builder = SignatureBuilder(soup, 'main').run(debug=True)
        signatures: ['h1', 'div>div>h2', 'div>div>p', 'div>h1', 'p', 'p']... plus more
    """

    soup: BeautifulSoup
    parent_tag: str = field(default=None)

    current_tree: list[str] = field(default_factory=list)
    top_level_tags: list[BeautifulSoup.object_was_parsed] = field(default_factory=list)
    signatures: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Initializes the SignatureBuilder object."""
        if self.parent_tag is None:
            self.top_level_tags = self.soup.findChildren(recursive=False)
        else:
            self.top_level_tags = self.soup.find(self.parent_tag).findChildren(
                recursive=False
            )

        self.current_tag = None

    def run(self, debug=False):
        """Call this method to run the SignatureBuilder."""
        for tag in self.top_level_tags:
            if not tag.findChildren(recursive=False):  # no children
                self.signatures.append(tag.name)
            else:  # has children so parse them to get the signatures
                self.current_tree.append(tag.name)
                self.parse_children(tag)
                self.current_tree.pop()

        self._debug() if debug else None

        return self

    def parse_children(self, tag):
        """Recursively parses the children of a tag to get the signatures."""
        for child in tag.findChildren(recursive=False):
            if not child.findChildren(recursive=False):
                self.signatures.append(">".join(self.current_tree + [child.name]))
            else:
                self.current_tree.append(child.name)
                self.parse_children(child)  # recursive call
                self.current_tree.pop()

    @property
    def get_signatures(self):
        """Returns the signatures, depending on the HTML structure, this may contain duplicates."""
        return self.signatures

    @property
    def get_unique_signatures(self):
        """Returns unique signatures only. This is useful if you want to use the signatures as a dictionary key."""
        unique_signatures = []
        for signature in self.signatures:
            unique_signatures.append(
                signature
            ) if signature not in unique_signatures else None
        return unique_signatures

    def _debug(self):
        """Prints useful SignatureBuilder information."""
        print("signatures:", self.signatures, "\n")
        print("unique_signatures:", self.get_unique_signatures, "\n")
        print("soup:", self.soup, "\n")
        print("parent_tag:", self.parent_tag, "\n")
        print("current_tree:", self.current_tree, "\n")
        print("top_level_tags:", self.top_level_tags, "\n")


# Example Usage

# if __name__ == "__main__":
#     html_content = """
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <title>My Title</title>
#         </head>
#         <body>
#             <header>
#                 <div>
#                     <h1>This is sample text</h1>
#                     <p>Some random text</p>
#                 </div>
#             </header>

#             <main>
#                 <h1 class="title">This is sample text</h1>
#                 <div>
#                     <div>
#                         <h2>This is sample text</h2>
#                         <p>Some random text</p>
#                     </div>
#                 </div>
#                 <div>
#                     <h1>This is sample text</h1>
#                     <p>Some random text</p>
#                 </div>
#                 <p>Some random text</p>
#                 <p>Some random text</p>
#             </main>

#             <footer>
#                 <h1>This is sample text</h1>
#                 <p>Some random text</p>
#             </footer>
#         </body>
#     </html>
#     """

#     soup = BeautifulSoup(html_content, "html.parser")
#     signature_builder = SignatureBuilder(soup, "main").run()
#     signatures = signature_builder.get_signatures
#     assert isinstance(signatures, list)
#     assert signatures == ["h1", "div>div>h2", "div>div>p", "div>h1", "div>p", "p", "p"]
#     unique_signatures = signature_builder.get_unique_signatures
#     assert isinstance(unique_signatures, list)
#     assert unique_signatures == [
#         "h1",
#         "div>div>h2",
#         "div>div>p",
#         "div>h1",
#         "div>p",
#         "p",
#     ]

# Optional debug
# signature_builder = SignatureBuilder(soup, "main").run(debug=True)
