from pathlib import Path
import pandas as pd
import markdown
from bs4 import BeautifulSoup

def load_data(path: str) -> pd.DataFrame:
    file = Path(path)
    if not file.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    suffix = file.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(file)
    if suffix == ".json":
        return pd.read_json(file)
    if suffix == ".md": 
        raw_text = file.read_text(encoding="utf-8")
        html = markdown.markdown(raw_text)
        clean_text = BeautifulSoup(html, "html.parser").get_text()
        #readable DataFrame
        return pd.DataFrame({"content": [clean_text.strip()]})
        
    raise ValueError(f"Unsupported file type: {suffix}")
