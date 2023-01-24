from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.generator import generator_schema, user_crud
from datetime import datetime

from itertools import accumulate
from bisect import bisect
from random import randrange
from unicodedata import name as unicode_name

router = APIRouter(
    prefix="/api/user",
)

# Set the unicode version.
# Your system may not support Unicode 7.0 charecters just yet! So hipster.
UNICODE_VERSION = 6

# Sauce: http://www.unicode.org/charts/PDF/U1F300.pdf
EMOJI_RANGES_UNICODE = {
    6: [('\U0001F300', '\U0001F320'), ('\U0001F330', '\U0001F335'),
        ('\U0001F337', '\U0001F37C'), ('\U0001F380', '\U0001F393'),
        ('\U0001F3A0', '\U0001F3C4'), ('\U0001F3C6', '\U0001F3CA'),
        ('\U0001F3E0', '\U0001F3F0'), ('\U0001F400', '\U0001F43E'),
        ('\U0001F440',), ('\U0001F442', '\U0001F4F7'),
        ('\U0001F4F9', '\U0001F4FC'), ('\U0001F500', '\U0001F53C'),
        ('\U0001F540', '\U0001F543'), ('\U0001F550', '\U0001F567'),
        ('\U0001F5FB', '\U0001F5FF')],
    7: [('\U0001F300', '\U0001F32C'), ('\U0001F330', '\U0001F37D'),
        ('\U0001F380', '\U0001F3CE'), ('\U0001F3D4', '\U0001F3F7'),
        ('\U0001F400', '\U0001F4FE'), ('\U0001F500', '\U0001F54A'),
        ('\U0001F550', '\U0001F579'), ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')],
    8: [('\U0001F300', '\U0001F579'), ('\U0001F57B', '\U0001F5A3'),
        ('\U0001F5A5', '\U0001F5FF')]
}

NO_NAME_ERROR = '(No name found for this codepoint)'


def random_emoji(unicode_version=6):
    if unicode_version in EMOJI_RANGES_UNICODE:
        emoji_ranges = EMOJI_RANGES_UNICODE[unicode_version]
    else:
        emoji_ranges = EMOJI_RANGES_UNICODE[-1]

    # Weighted distribution
    count = [ord(r[-1]) - ord(r[0]) + 1 for r in emoji_ranges]
    weight_distr = list(accumulate(count))

    # Get one point in the multiple ranges
    point = randrange(weight_distr[-1])

    # Select the correct range
    emoji_range_idx = bisect(weight_distr, point)
    emoji_range = emoji_ranges[emoji_range_idx]

    # Calculate the index in the selected range
    point_in_range = point
    if emoji_range_idx != 0:
        point_in_range = point - weight_distr[emoji_range_idx - 1]

    # Emoji 😄
    emoji = chr(ord(emoji_range[0]) + point_in_range)
    emoji_name = unicode_name(emoji, NO_NAME_ERROR).capitalize()
    emoji_codepoint = "U+{}".format(hex(ord(emoji))[2:].upper())

    return (emoji)


@router.get("/list", response_model=list[generator_schema.User])
def user_list(db: Session = Depends(get_db)):
    _user_list = user_crud.get_user_list(db)
    return _user_list


@router.get("/chart")
def chart_create(db: Session = Depends(get_db)):
    _user_list = user_crud.get_user_name_list(db)
    user_name_list = dict(_user_list)

    area_before = [
        "사관실", "독사", "마대", "마대", "마대", "사이드", "휴체", "휴체", "휴체", "신세", "신세", "화장실",
        "화장실", "화장실", "화장실"
    ]

    area_after = [
        "독사", "마대", "마대", "마대", "사이드", "휴체", "휴체", "휴체", "신세", "신세", "화장실",
        "화장실", "화장실", "화장실"
    ]

    # 1 False 인원 제거
    lst = [i for i, j in user_name_list.items() if j == True]

    # 2 청소표 인원 맞추기
    if datetime.today().day < 16:
        while len(lst) != len(area_before):
            lst.pop(0)
    else:
        while len(lst) != len(area_after):
            lst.pop(0)

    result_text = f"{random_emoji(UNICODE_VERSION)} {datetime.today().year}년 {datetime.today().month}월 {datetime.today().day}일 {random_emoji(UNICODE_VERSION)}\n"

    if datetime.today().day < 16:
        for i in range(len(area_before)):
            result_text += f"{lst[i]} - {area_before[i]}\n"
    else:
        for i in range(len(area_after)):
            result_text += f"{lst[i]} - {area_after[i]}\n"

    return result_text


@router.get("/detail/{user_id}", response_model=generator_schema.User)
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id=user_id)
    return user


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: generator_schema.UserCreate,
                db: Session = Depends(get_db)):
    user_crud.create_user(db=db, user_create=_user_create)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def user_update(_user_update: generator_schema.UserUpdate,
                db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=_user_update.user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")

    user_crud.update_user(db=db, db_user=db_user,
                          user_update=_user_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def user_delete(_user_delete: generator_schema.UserDelete, db: Session = Depends(get_db)):
    #    current_user: User = Depends(get_current_user)):
    db_user = user_crud.get_user(db, user_id=_user_delete.user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    user_crud.delete_user(db=db, db_user=db_user)
