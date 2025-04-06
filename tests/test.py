from pathlib import Path


def test_data_directory_exists():
    data_dir = Path('data')
    assert data_dir.exists() and data_dir.is_dir(), 'Data directory does not exist'


def test_number_of_files():
    files = [f for f in Path('data').iterdir() if f.is_file()]
    assert len(files) == 13, f'Expected 13 files, found {len(files)}'
