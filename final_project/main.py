"""
Final project implementation.
"""

# pylint: disable=unused-import
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from lab_6_pipeline.pipeline import UDPipeAnalyzer


def main(corpus_path: Path, dist_path: Path) -> None:
    """
    Generate conllu file for provided corpus of texts.

    Args:
        corpus_path (Path): Path to folder containing text files.
        dist_path (Path): Path to folder for saving auto_annotated.conllu.
    """
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus folder does not exist: {corpus_path}")
    raw_files = sorted(corpus_path.glob("*.txt"))
    if not raw_files:
        raise ValueError(f"No .txt files found in {corpus_path}")
    dist_path.mkdir(parents=True, exist_ok=True)
    analyzer = UDPipeAnalyzer()
    all_results = []
    for file in raw_files:
        content = file.read_text(encoding="utf-8").strip()
        normalized = unicodedata.normalize("NFC", content)
        if not normalized:
            continue
        results = analyzer.analyze([normalized])
        if results and results[0]:
            all_results.append(results[0])
    if not all_results:
        raise ValueError("UDPipe analysis result is empty")
    result = "\n\n".join(all_results)
    output_file = dist_path / "auto_annotated.conllu"
    output_file.write_text(result, encoding="utf-8")
    if not result.endswith('\n'):
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write('\n')


if __name__ == "__main__":
    main(
        Path(__file__).parent / "assets" / "articles", 
        Path(__file__).parent / "dist"
    )