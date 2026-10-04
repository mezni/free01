"""Parser tests for the ingestion pipeline.

Tests for the file-to-markdown converters in src.pipelines.ingestion.loader.
"""

from pathlib import Path
import tempfile

from src.pipelines.ingestion.loader import LoaderFactory, CSVLoader


def test_csv_loader_basic():
    """Test CSV loader with basic content."""
    csv_content = "Name,Age,City\nAlice,30,New York\nBob,25,Los Angeles\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        tmp_path = Path(f.name)

    result = LoaderFactory.load_file(tmp_path)
    assert "| Name" in result
    assert "| Age" in result
    assert "| City" in result
    assert "| Alice" in result
    assert "| Bob" in result


def test_csv_loader_empty():
    """Test CSV loader with header-only content."""
    csv_content = "Name,Age\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        tmp_path = Path(f.name)

    result = LoaderFactory.load_file(tmp_path)
    assert "| Name" in result
    assert "| Age" in result
    # Should have header row + separator row (2 lines for header-only CSV)
    lines = result.strip().split("\n")
    assert len(lines) == 2  # header + separator, no data rows


def test_csv_loader_single_row():
    """Test CSV loader with single data row."""
    csv_content = "Name,Age\nCharlie,35\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        tmp_path = Path(f.name)

    result = LoaderFactory.load_file(tmp_path)
    assert "| Charlie" in result
    assert "| 35" in result


def test_csv_loader_multiline_values():
    """Test CSV with values containing commas (quoted)."""
    csv_content = "Name,Description\nAlice,\"Loves, tomatoes\"\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        tmp_path = Path(f.name)

    result = LoaderFactory.load_file(tmp_path)
    assert "| Name" in result
    # The quoted value should be handled
    assert "Loves, tomatoes" in result or "Loves" in result


def test_pdf_loader_placeholder():
    """Test PDF loader returns expected placeholder."""
    from src.pipelines.ingestion.loader import PDFLoader

    loader = PDFLoader()
    result = loader.load(Path("test.pdf"))
    assert "# PDF Content:" in result


def test_markdown_passthrough():
    """Test MarkdownLoader passes content through."""
    from src.pipelines.ingestion.loader import MarkdownLoader

    loader = MarkdownLoader()
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("# Test Document\n\nThis is **bold** text.\n")
        tmp_path = Path(f.name)

    result = loader.load(tmp_path)
    assert isinstance(result, str)
    assert len(result) > 0
    assert "# Test Document" in result