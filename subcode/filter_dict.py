def remove_non_player(fusion_dict):
    """
    If team placements are only 0 or -1, remove the entry from the fusion_dict.
    """
    keys_to_remove = []
    for team_id, team_data in fusion_dict.items():
        if all(round['placement'] <= 0 for round in team_data['rounds']):
            keys_to_remove.append(team_id)

    for key in keys_to_remove:
        del fusion_dict[key]

    return fusion_dict