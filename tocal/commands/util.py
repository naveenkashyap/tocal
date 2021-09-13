from typing import List
from pathlib import Path

package_root: Path = Path('/', 'Users', 'naveen', 'dev', 'tocal', 'tocal')

# calendar configs
SECRETS_PATH: Path = Path(package_root, 'secrets', 'google', 'client_secret.json')
CREDS_PATH: Path = Path(package_root, 'creds', 'google', 'creds.pickle')
SCOPES: List[str] = ['https://www.googleapis.com/auth/calendar.events']
SERVICE_NAME: str = 'calendar'
SERVICE_VERSION: str = 'v3'

# todo configs
TODOLIST_FILEPATH: Path = Path(package_root, 'data', 'todo', 'list.pickle')
