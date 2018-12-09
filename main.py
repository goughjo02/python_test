"""Main Script."""

from mapper.mapper import Mapper
from grouper.grouper import Grouper


def service(path_to_mappings, path_to_price_catalog):
    """Main app function."""
    mapper = Mapper(path_to_mappings)
    mapped_catalog = mapper.perform_mapping(path_to_price_catalog)
    grouper = Grouper(mapped_catalog)
    result = grouper.gen_json()
    print(result)


if __name__ == "__main__":
    path_to_mappings = './mappings.csv'
    path_to_price_catalog = './pricat.csv'
    service(path_to_mappings, path_to_price_catalog)
