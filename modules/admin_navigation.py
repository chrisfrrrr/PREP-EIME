"""Pure navigation helpers: never navigate using a list position across attempts."""

def resolve_attempt(active_id, visible_ids):
    ids = sorted(set(visible_ids))
    if not ids:
        return None
    return active_id if active_id in ids else ids[0]


def resolve_answer(current_id, pending_id, available_ids):
    if pending_id in available_ids:
        return pending_id
    if current_id in available_ids:
        return current_id
    return available_ids[0] if available_ids else None


def next_answer(current_id, available_ids):
    if current_id not in available_ids:
        return None
    idx = available_ids.index(current_id)
    return available_ids[idx + 1] if idx + 1 < len(available_ids) else None
