"""Test loader for the Enterprise RAG ingestion pipeline.

Provides test fixtures and a mock loader for unit testing the
pipeline's file loading and markdown conversion capabilities.
"""


from pathlib import Path
from src.pipelines.ingestion.loader import LoaderFactory, FileLoader, PDFLoader


class MockLoader(FileLoader):
    """Mock loader for testing purposes.

    Returns predictable output regardless of file type,
    useful for testing pipeline orchestration without
    actual file format parsers.
    """

    def __init__(self, output: str = "# Mock Content\n\n*Test loader output.*"):
        self._output = output

    def load(self, file_path: Path) -> str:
        """Load file and return mock markdown content.

        Args:
            file_path: Path to the file (ignored in mock mode).

        Returns:
            Pre-configured mock markdown content.
        """
        return self._output


def test_pdf_loader():
    """Test PDF loader with known input."""
    loader = PDFLoader()
    result = loader.load(Path("test.pdf"))
    assert "# PDF Content:" in result
    assert "test.pdf" in result


def test_csv_loader():
    """Test CSV loader with known input."""
    import tempfile

    csv_content = "Name,Age\nAlice,30\nBob,25\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        tmp_path = Path(f.name)

    result = LoaderFactory.load_file(tmp_path)
    assert "| Name" in result
    assert "| Alice" in result


def test_mock_loader():
    """Test mock loader returns predictable output."""
    mock = MockLoader()
    from pathlib import Path
    result = mock.load(Path("any_file.pdf"))
    assert result == "# Mock Content\n\n*Test loader output.*"


def test_loader_factory():
    """Test LoaderFactory can create loaders for supported extensions."""
    for ext in [".pdf", ".csv", ".md"]:
        loader = LoaderFactory.get_loader(Path(f"test{ext}"))
        assert loader is not None


def test_loader_factory_unsupported():
    """Test LoaderFactory raises ValueError for unsupported extensions."""
    try:
        LoaderFactory.get_loader(Path("test.xyz"))
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected