import json
from inventory.models import Item, Area

with open("inventory.json") as f:
    item_json = json.load(f)

for item in item_json:
    all_areas = Area.objects.all()
    all_areas.get(name=item["Area"])
    # area.save()
    if item["Image"] == "None":
        item = Item(uid=item["UID"], description=item["Description"], image=None, quantity=item["Quantity"], code=item["Code"], area=area)
        item.save()
    else:
        item = Item(uid=item["UID"], description=item["Description"], image=item['Image'], quantity=item["Quantity"], code=item["Code"], area=area)
        item.save()
