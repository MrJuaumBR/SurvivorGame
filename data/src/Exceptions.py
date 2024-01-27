
class MissingFilesOrFolders(Exception):
    """Excpetion for missing files"""
    def __init__(self,) -> None:
        """Excpetion for missing files"""
        super().__init__()
        self.message = "Some files/folders are missing. try reinstall the game."