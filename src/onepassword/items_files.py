# Code generated by op-codegen - DO NO EDIT MANUALLY

from .core import _invoke, _invoke_sync
from typing import Optional, List
from pydantic import TypeAdapter
from .types import DocumentCreateParams, FileAttributes, FileCreateParams, Item


class ItemsFiles:
    def __init__(self, client_id):
        self.client_id = client_id

    async def attach(self, item: Item, file_params: FileCreateParams) -> Item:
        """
        Attach files to Items
        """
        response = await _invoke(
            {
                "invocation": {
                    "clientId": self.client_id,
                    "parameters": {
                        "name": "ItemsFilesAttach",
                        "parameters": {
                            "item": item.model_dump(by_alias=True),
                            "file_params": file_params.model_dump(by_alias=True),
                        },
                    },
                }
            }
        )

        response = TypeAdapter(Item).validate_json(response)
        return response

    async def read(self, vault_id: str, item_id: str, attr: FileAttributes) -> bytes:
        """
        Read file content from the Item
        """
        response = await _invoke(
            {
                "invocation": {
                    "clientId": self.client_id,
                    "parameters": {
                        "name": "ItemsFilesRead",
                        "parameters": {
                            "vault_id": vault_id,
                            "item_id": item_id,
                            "attr": attr.model_dump(by_alias=True),
                        },
                    },
                }
            }
        )

        response = bytes(TypeAdapter(List[int]).validate_json(response))
        return response

    async def delete(self, item: Item, section_id: str, field_id: str) -> Item:
        """
        Delete a field file from Item using the section and field IDs
        """
        response = await _invoke(
            {
                "invocation": {
                    "clientId": self.client_id,
                    "parameters": {
                        "name": "ItemsFilesDelete",
                        "parameters": {
                            "item": item.model_dump(by_alias=True),
                            "section_id": section_id,
                            "field_id": field_id,
                        },
                    },
                }
            }
        )

        response = TypeAdapter(Item).validate_json(response)
        return response

    async def replace_document(
        self, item: Item, doc_params: DocumentCreateParams
    ) -> Item:
        """
        Replace the document file within a document item
        """
        response = await _invoke(
            {
                "invocation": {
                    "clientId": self.client_id,
                    "parameters": {
                        "name": "ItemsFilesReplaceDocument",
                        "parameters": {
                            "item": item.model_dump(by_alias=True),
                            "doc_params": doc_params.model_dump(by_alias=True),
                        },
                    },
                }
            }
        )

        response = TypeAdapter(Item).validate_json(response)
        return response
