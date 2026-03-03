import requests
import json
from time import sleep

BASE_URL = "https://www.auroragov.org/portal/svc/ContentItemSvc.asmx/GetItemList"

session = requests.Session()

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "https://www.auroragov.org",
    "Referer": "https://www.auroragov.org/city_hall/boards___commissions/planning___zoning_commission",
    "X-Requested-With": "XMLHttpRequest",
    "requestfrom": "contentItem",
    "User-Agent": "Mozilla/5.0"
}

COMMON_PARAMS = {
    "ContextId": 16431824,
    "OneLink": "/cms/One.aspx",
    "Extension": "492960",
    "ClientId": "ctl00_ContentPlaceHolder1_ctl23",
    "Place": "cms",
    "PortalId": "16242704",
    "PageId": "16431813",
    "HideDescription": True,
    "ShowDispSettings": False,
    "ShowSecurity": False,
    "ShowActivity": False,
    "ShowSubscription": True,
    "id": 5,
    "searchVal": "",
    "InstanceId": "492960"
}

TOP_LEVEL_IDS = [16431863, 16431857, 16431856, 16446465, 18257690, 16446464]

all_parent_ids = []

# ---------------------------
# STEP 1: Get child ItemIds
# ---------------------------
for parent_id in TOP_LEVEL_IDS:

    payload = {
        "parentId": parent_id,
        "Params": json.dumps({
            **COMMON_PARAMS,
            "RawUrl": "/city_hall/boards___commissions/planning___zoning_commission"
        })
    }

    response = session.post(BASE_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    data = response.json()
    documents = data.get("d", {}).get("DataObject", [])

    for doc in documents:
        item_id = doc.get("ItemId")
        if item_id:
            all_parent_ids.append(item_id)

print(f"Collected {len(all_parent_ids)} child parent IDs")


# ---------------------------
# STEP 2: Get PDFs from each child
# ---------------------------
for child_parent_id in all_parent_ids:

    print(f"\nProcessing ParentID: {child_parent_id}")

    payload = {
        "parentId": child_parent_id,
        "Params": json.dumps({
            **COMMON_PARAMS,
            "RawUrl": "/city_hall/mayor___city_council/council_meetings"
        })
    }

    response = session.post(BASE_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    data = response.json()
    documents = data.get("d", {}).get("DataObject", [])

    for document in documents:
        filename = document.get("Name")
        pdf_link = document.get("DownloadLink")

        if pdf_link:
            if not pdf_link.startswith("http"):
                pdf_link = "https://www.auroragov.org" + pdf_link

            print(f"{filename}: {pdf_link}")

    sleep(1)  # polite delay