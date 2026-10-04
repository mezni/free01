"""Loader module to convert various file formats to markdown.

This module provides utilities to read different file types (PDF, Word,
HTML, etc.) and convert their content to markdown format for downstream
processing in the RAG pipeline.
"""


import abc
import io
from pathlib import Path
from typing import Optional


class FileLoader(abc.ABC):
    """Abstract base class for file loaders.

    Subclasses should implement the `load` method to convert specific
    file types to markdown text.
    """

    @abc.abstractmethod
    def load(self, file_path: Path) -> str:
        """Load and convert a file to markdown.

        Args:
            file_path: Path to the file to load.

        Returns:
            Markdown-formatted text content of the file.
        """
        raise NotImplementedError


class PDFLoader(FileLoader):
    """Loader for PDF files converting to markdown.

    Uses layout-aware parsing to preserve document structure.
    """

    def load(self, file_path: Path) -> str:
        """Load a PDF file and convert to markdown.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Markdown-formatted text extracted from the PDF.
        """
        # Placeholder for PDF parsing logic
        # In production, would use layout-aware PDF extraction
        return f"# PDF Content: {file_path.name}\n\n*PDF content would be extracted here using layout-aware parsing.*"


class WordLoader(FileLoader):
    """Loader for Microsoft Word documents (.docx) converting to markdown."""

    def load(self, file_path: Path) -> str:
        """Load a Word document and convert to markdown.

        Args:
            file_path: Path to the .docx file.

        Returns:
            Markdown-formatted text extracted from the Word document.
        """
        # Placeholder for Word document parsing
        return f"# Word Document: {file_path.name}\n\n*Word content would be extracted here.*"


class CSVLoader(FileLoader):
    """Loader for CSV files converting to markdown tables."""

    def load(self, file_path: Path) -> str:
        """Load a CSV file and convert to markdown table.

        Args:
            file_path: Path to the CSV file.

        Returns:
            Markdown-formatted text with the CSV content as a table.
        """
        lines = file_path.read_text(encoding="utf-8").strip().splitlines()
        if not lines:
            return ""

        markdown_lines = ["| " + " | ".join(lines[0].split(",")) + " |"]
        markdown_lines.append("|" + "|".join(["---"] * len(lines[0].split(","))) + "|")

        for line in lines[1:]:
            markdown_lines.append("| " + " | ".join(line.split(",")) + " |")

        return "\n".join(markdown_lines)


class MarkdownLoader(FileLoader):
    """Loader for existing markdown files."""

    def load(self, file_path: Path) -> str:
        """Load a markdown file as-is.

        Args:
            file_path: Path to the markdown file.

        Returns:
            The markdown content of the file.
        """
        return file_path.read_text(encoding="utf-8")


class LoaderFactory:
    """Factory class to get the appropriate loader for a file type."""

    _loaders = {
        ".pdf": PDFLoader,
        ".docx": WordLoader,
        ".csv": CSVLoader,
        ".md": MarkdownLoader,
    }

    @classmethod
    def get_loader(cls, file_path: Path) -> FileLoader:
        """Get the appropriate loader for the given file path.

        Args:
            file_path: Path to the file.

        Returns:
            An instance of the appropriate FileLoader subclass.

        Raises:
            ValueError: If no loader is found for the file extension.
        """
        extension = file_path.suffix.lower()
        loader_class = cls._loaders.get(extension)
        if loader_class is None:
            raise ValueError(f"No loader found for extension: {extension}")
        return loader_class()

    @classmethod
    def load_file(cls, file_path: Path) -> str:
        """Convenience method to load a file directly.

        Args:
            file_path: Path to the file to load.

        Returns:
            Markdown-formatted text content of the file.

        Raises:
            ValueError: If no loader is found for the file extension.
        """
        loader = cls.get_loader(file_path)
        return loader.load(file_path)