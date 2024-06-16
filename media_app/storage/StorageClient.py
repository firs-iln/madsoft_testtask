from abc import abstractmethod


class StorageClient:
    @abstractmethod
    async def upload_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    async def delete_file(self, object_name: str):
        pass

    @abstractmethod
    async def get_file(self, object_name: str) -> bytes:
        pass
