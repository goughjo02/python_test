"""Module to create clss to convert nd_array into json."""
import json
from collections import Counter, defaultdict
import pdb


class Grouper:
    """Class to group into json for exaple."""

    def __init__(self, data_source):
        """Initializer."""
        self.data = []
        for row in data_source[1:, :]:
            number = 0
            # If there re no entries for the supplier
            if row[1] not in [e["supplier"] for e in self.data]:
                new_data = defaultdict(list)
                new_data["supplier"] = row[1]
                new_data["brands"] = [{
                    "name": row[2],
                    "articles": [{
                        "name": row[6],
                        "amount": 1,
                        "variants": [{
                            "color": row[9],
                            "size": row[10],
                            "amount": 1
                        }]
                    }]
                }]
                self.data.append(new_data)
            else:
                current_supplier = next((item for item in self.data if item['supplier'] == row[1]), None)
                # If there are no entries for this brand
                if row[2] not in [e["name"] for e in current_supplier['brands']]:
                    print(row[2], current_supplier['brands'])
                    current_supplier['brands'].append({
                        "name": row[2],
                        "articles": [{
                            "name": row[6],
                            "amount": 1,
                            "variants": [{
                                "color": row[9],
                                "size": row[10],
                                "amount": 1
                            }]
                        }]
                    })
                else:
                    current_brand = next((item for item in current_supplier["brands"] if item['name'] == row[2]), None)
                    # if there are no entries for this article
                    if row[6] not in [e["name"] for e in current_brand["articles"]]:
                        current_brand["articles"].append({
                            "name": row[6],
                            "amount": 1,
                            "variants": [{
                                "color": row[9],
                                "size": row[10],
                                "amount": 1
                            }]
                        })
                    else:
                        current_article = next((item for item in current_brand["articles"] if item['name'] == row[6]), None)
                        for i in current_article["variants"]:
                            if i["color"] == row[9] and i["size"] == row[10]:
                                i["amount"] += 1
                            else:
                                current_article["variants"].append({
                                    "color": row[9],
                                    "size": row[10],
                                    "amount": 1
                                })
                                break

    def gen_json(self):
        """Function to group into json."""
        return json.dumps(self.data, indent=4, sort_keys=True)
