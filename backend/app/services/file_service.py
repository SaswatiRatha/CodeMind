from pathlib import Path

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".swift",
    ".kt",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".md",
    ".txt",
    ".sql",
    ".sh",
}

IGNORED_DIRECTORIES = {

    ".git", 
    "node_modules", 
    "vendor", 
    "dist", 
    "build",
    ".venv", 
    "venv", 
    "__pycache__", 
    ".next"
}

MAX_FILE_SIZE = 500_000 #500 KB

def discover_files(repository_path: str) -> list[Path]:
    root = Path(repository_path)
    discovered_files = []

    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(root)

        if any(part in IGNORED_DIRECTORIES for part in relative_path.parts):
            continue

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        if file_path.stat().st_size > MAX_FILE_SIZE:
            continue

        discovered_files.append(file_path)

    return discovered_files