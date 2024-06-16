class StorageError(Exception):
    ...


class UploadingError(StorageError):
    ...


class DownloadingError(StorageError):
    ...


class DeletingError(StorageError):
    ...


class NoSuchKey(StorageError):
    ...