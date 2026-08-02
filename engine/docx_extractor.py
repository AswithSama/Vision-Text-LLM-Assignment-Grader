from pathlib import Path
from hashlib import sha256
from io import BytesIO

from docx import Document
from docx.document import Document as DocumentType
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from PIL import Image



def iter_document_blocks(document: DocumentType):
    for child in document.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, document)

        elif isinstance(child, CT_Tbl):
            yield Table(child, document)


def extract_images(element, document, image_counter):
    images = []

    for blip in element._element.xpath(".//a:blip"):
        relationship_id = blip.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
        )

        if not relationship_id:
            continue

        image_part = document.part.related_parts[relationship_id]
        image_bytes = image_part.blob

        try:
            image = Image.open(BytesIO(image_bytes))
            width, height = image.size
            image_format = image.format
        except Exception:
            width = None
            height = None
            image_format = None

        image_counter[0] += 1

        images.append(
            {
                "type": "image",
                "image_number": image_counter[0],
                "filename": Path(image_part.partname).name,
                "format": image_format,
                "width": width,
                "height": height,
                "size_bytes": len(image_bytes),
                "sha256": sha256(image_bytes).hexdigest(),
                "bytes": image_bytes,
            }
        )

    return images


def extract_docx_contents(document_path: Path):
    document = Document(document_path)

    contents = []
    image_counter = [0]

    for block_number, block in enumerate(
        iter_document_blocks(document),
        start=1,
    ):
        if isinstance(block, Paragraph):
            contents.append(
                {
                    "block_number": block_number,
                    "type": "paragraph",
                    "text": block.text,
                    "style": block.style.name if block.style else None,
                }
            )

            contents.extend(
                extract_images(
                    block,
                    document,
                    image_counter,
                )
            )

        elif isinstance(block, Table):
            for row_number, row in enumerate(block.rows, start=1):
                row_data = {
                    "block_number": block_number,
                    "type": "table_row",
                    "row_number": row_number,
                    "cells": [],
                }

                for cell_number, cell in enumerate(row.cells, start=1):
                    row_data["cells"].append(
                        {
                            "cell": cell_number,
                            "text": cell.text,
                        }
                    )

                contents.append(row_data)

                for cell_number, cell in enumerate(row.cells, start=1):
                    cell_images = extract_images(
                        cell,
                        document,
                        image_counter,
                    )

                    for image_data in cell_images:
                        image_data["table_block"] = block_number
                        image_data["row"] = row_number
                        image_data["cell"] = cell_number

                        contents.append(image_data)

    print(f"Successfully extracted {document_path.name}")

    return contents