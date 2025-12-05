from typing import Optional

from ....application.interfaces.cache import CacheInterface
from ....application.interfaces.repository import OfficeRepositoryInterface
from ....domain.entities.office import Office


class CachedOfficeRepository(OfficeRepositoryInterface):
    CACHE_KEY_ALL = "offices:all"
    CACHE_KEY_PREFIX = "office:"
    DEFAULT_TTL = 300

    def __init__(
        self,
        repository: OfficeRepositoryInterface,
        cache: CacheInterface,
        ttl_seconds: int = 300,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._ttl = ttl_seconds

    def get_by_id(self, office_id: int) -> Optional[Office]:
        cache_key = f"{self.CACHE_KEY_PREFIX}{office_id}"

        cached = self._cache.get(cache_key)
        if cached:
            return self._dict_to_office(cached)

        office = self._repository.get_by_id(office_id)
        if office:
            self._cache.set(cache_key, self._office_to_dict(office), self._ttl)

        return office

    def find_all(self) -> list[Office]:
        cached = self._cache.get(self.CACHE_KEY_ALL)
        if cached:
            return [self._dict_to_office(item) for item in cached]

        offices = self._repository.find_all()
        if offices:
            cache_data = [self._office_to_dict(office) for office in offices]
            self._cache.set(self.CACHE_KEY_ALL, cache_data, self._ttl)

        return offices

    def save(self, office: Office) -> Office:
        result = self._repository.save(office)

        self._cache.delete(self.CACHE_KEY_ALL)
        self._cache.delete(f"{self.CACHE_KEY_PREFIX}{office.office_id}")

        return result

    @staticmethod
    def _office_to_dict(office: Office) -> dict:
        return {
            "office_id": office.office_id,
            "name": office.name,
            "capacity": office.capacity,
            "description": office.description,
        }

    @staticmethod
    def _dict_to_office(data: dict) -> Office:
        return Office(
            office_id=data["office_id"],
            name=data["name"],
            capacity=data["capacity"],
            description=data["description"],
        )
