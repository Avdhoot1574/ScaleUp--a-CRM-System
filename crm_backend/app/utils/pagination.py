from fastapi import Query

def pagination_params(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
) -> tuple[int, int]:
    return page, limit
