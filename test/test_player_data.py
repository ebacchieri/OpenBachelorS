import os
import json

from openbachelors.util.const_json_loader import ConstJson
from openbachelors.const.filepath import TMP_DIRPATH
from openbachelors.util.player_data import DeltaJson, OverlayJson, player_data_template


def test_writable_overlay_json():
    base_json = ConstJson(
        {
            "k0": {"k1": 0},
            "k2": 0,
        }
    )

    delta_json = DeltaJson()

    overlay_json = OverlayJson(base_json, delta_json)

    overlay_json["k0"] = 1

    assert overlay_json.copy() == {"k2": 0, "k0": 1}
    assert delta_json.modified_dict == {"k0": 1}
    assert delta_json.deleted_dict == {"k0": None}

    overlay_json["k0"] = {}

    assert overlay_json.copy() == {"k2": 0, "k0": {}}
    assert delta_json.modified_dict == {"k0": {}}
    assert delta_json.deleted_dict == {"k0": None}

    overlay_json["k2"] = {
        "k3": {"k4": 2, "k5": {}},
        "k6": {},
    }

    assert overlay_json.copy() == {
        "k0": {},
        "k2": {"k3": {"k4": 2, "k5": {}}, "k6": {}},
    }
    assert delta_json.modified_dict == {
        "k0": {},
        "k2": {"k3": {"k4": 2, "k5": {}}, "k6": {}},
    }
    assert delta_json.deleted_dict == {"k0": None, "k2": None}

    del overlay_json["k2"]["k3"]

    assert overlay_json.copy() == {
        "k0": {},
        "k2": {"k6": {}},
    }
    assert delta_json.modified_dict == {
        "k0": {},
        "k2": {"k6": {}},
    }
    assert delta_json.deleted_dict == {"k0": None, "k2": None}

    overlay_json["k2"]["k6"] = 3

    assert overlay_json.copy() == {
        "k0": {},
        "k2": {"k6": 3},
    }
    assert delta_json.modified_dict == {
        "k0": {},
        "k2": {"k6": 3},
    }
    assert delta_json.deleted_dict == {"k0": None, "k2": None}

    overlay_json["k2"] = {"k7": {"k8": {}}}

    overlay_json["k2"] = {}

    overlay_json["k2"]["k7"] = {}

    assert overlay_json.copy() == {
        "k0": {},
        "k2": {"k6": 3, "k7": {"k8": {}}},
    }
    assert delta_json.modified_dict == {
        "k0": {},
        "k2": {"k6": 3, "k7": {"k8": {}}},
    }
    assert delta_json.deleted_dict == {"k0": None, "k2": None}

    # ---

    base_json = ConstJson(
        {
            "k0": {"k1": 1, "k3": {"k4": 2}},
            "k2": 0,
        }
    )

    delta_json = DeltaJson()

    overlay_json = OverlayJson(base_json, delta_json)

    overlay_json["k0"]["k1"] = {}

    assert overlay_json.copy() == {"k0": {"k3": {"k4": 2}, "k1": {}}, "k2": 0}
    assert delta_json.modified_dict == {"k0": {"k1": {}}}
    assert delta_json.deleted_dict == {"k0": {"k1": None}}

    overlay_json["k0"]["k5"] = 3

    assert overlay_json.copy() == {"k0": {"k3": {"k4": 2}, "k1": {}, "k5": 3}, "k2": 0}
    assert delta_json.modified_dict == {"k0": {"k1": {}, "k5": 3}}
    assert delta_json.deleted_dict == {"k0": {"k1": None}}

    # print(overlay_json.copy(), delta_json.modified_dict, delta_json.deleted_dict)


def test_player_data_template():
    os.makedirs(TMP_DIRPATH, exist_ok=True)
    with open(
        os.path.join(TMP_DIRPATH, "player_data_template.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(player_data_template.copy(), f, ensure_ascii=False, indent=4)


# def test_player_data():
#     @player_data_decorator
#     def f(player_data):
#         player_data["status"]["ap"] = 789
#         response = {}
#         return response

#     response = f()

#     response.pop("pushMessage", None)

#     assert response == {
#         "playerDataDelta": {"modified": {"status": {"ap": 789}}, "deleted": {}}
#     }
