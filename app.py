# import math
# import time
# import streamlit as st

# st.set_page_config(page_title="Shell Beat", page_icon="⚛️", layout="wide")

# # (원자번호, 원소 기호, 원소 이름)
# elements = [
#     (1, "H", "수소"), (2, "He", "헬륨"), (3, "Li", "리튬"), (4, "Be", "베릴륨"),
#     (5, "B", "붕소"), (6, "C", "탄소"), (7, "N", "질소"), (8, "O", "산소"),
#     (9, "F", "플루오린"), (10, "Ne", "네온"), (11, "Na", "나트륨"), (12, "Mg", "마그네슘"),
#     (13, "Al", "알루미늄"), (14, "Si", "규소"), (15, "P", "인"), (16, "S", "황"),
#     (17, "Cl", "염소"), (18, "Ar", "아르곤"), (19, "K", "칼륨"), (20, "Ca", "칼슘"),
#     (21, "Sc", "스칸듐"), (22, "Ti", "티타늄"), (23, "V", "바나듐"), (24, "Cr", "크로뮴"),
#     (25, "Mn", "망가니즈"), (26, "Fe", "철"), (27, "Co", "코발트"), (28, "Ni", "니켈"),
#     (29, "Cu", "구리"), (30, "Zn", "아연"), (31, "Ga", "갈륨"), (32, "Ge", "저마늄"),
#     (33, "As", "비소"), (34, "Se", "셀레늄"), (35, "Br", "브로민"), (36, "Kr", "크립톤"),
#     (37, "Rb", "루비듐"), (38, "Sr", "스트론튬"), (39, "Y", "이트륨"), (40, "Zr", "지르코늄"),
#     (41, "Nb", "나이오븀"), (42, "Mo", "몰리브데넘"), (43, "Tc", "테크네튬"), (44, "Ru", "루테늄"),
#     (45, "Rh", "로듐"), (46, "Pd", "팔라듐"), (47, "Ag", "은"), (48, "Cd", "카드뮴"),
#     (49, "In", "인듐"), (50, "Sn", "주석"), (51, "Sb", "안티모니"), (52, "Te", "텔루륨"),
#     (53, "I", "아이오딘"), (54, "Xe", "제논"), (55, "Cs", "세슘"), (56, "Ba", "바륨"),
#     (57, "La", "란타넘"), (58, "Ce", "세륨"), (59, "Pr", "프라세오디뮴"), (60, "Nd", "네오디뮴"),
#     (61, "Pm", "프로메튬"), (62, "Sm", "사마륨"), (63, "Eu", "유로퓸"), (64, "Gd", "가돌리늄"),
#     (65, "Tb", "터븀"), (66, "Dy", "디스프로슘"), (67, "Ho", "홀뮴"), (68, "Er", "어븀"),
#     (69, "Tm", "툴륨"), (70, "Yb", "이터븀"), (71, "Lu", "루테튬"), (72, "Hf", "하프늄"),
#     (73, "Ta", "탄탈럼"), (74, "W", "텅스텐"), (75, "Re", "레늄"), (76, "Os", "오스뮴"),
#     (77, "Ir", "이리듐"), (78, "Pt", "백금"), (79, "Au", "금"), (80, "Hg", "수은"),
#     (81, "Tl", "탈륨"), (82, "Pb", "납"), (83, "Bi", "비스무트"), (84, "Po", "폴로늄"),
#     (85, "At", "아스타틴"), (86, "Rn", "라돈"), (87, "Fr", "프랑슘"), (88, "Ra", "라듐"),
#     (89, "Ac", "악티늄"), (90, "Th", "토륨"), (91, "Pa", "프로트악티늄"), (92, "U", "우라늄"),
# ]

# shell_capacities = [2, 8, 18, 32, 32, 18, 8]
# approach_start_radius = 285
# contact_tolerance = 14
# landing_grace_seconds = 0.30

# difficulty_settings = {
#     "쉬움": {"min_number": 1, "max_number": 10, "approach_seconds": 2.3, "orbit_speed": 1.5},
#     "보통": {"min_number": 11, "max_number": 36, "approach_seconds": 1.6, "orbit_speed": 2.0},
#     "어려움": {"min_number": 37, "max_number": 92, "approach_seconds": 1.1, "orbit_speed": 2.6},
# }


# def get_atoms(level):
#     """난이도에 해당하는 원자 목록을 반환한다."""
#     setting = difficulty_settings[level]
#     atom_list = []

#     for atom in elements:
#         if setting["min_number"] <= atom[0] <= setting["max_number"]:
#             atom_list.append(atom)

#     return atom_list


# def get_shell_slot(electron_index):
#     """전자 번호를 껍질 번호와 껍질 안의 슬롯 번호로 바꾼다."""
#     remaining = electron_index

#     for shell_index, capacity in enumerate(shell_capacities):
#         if remaining < capacity:
#             return shell_index, remaining, capacity
#         remaining -= capacity

#     return len(shell_capacities) - 1, 0, shell_capacities[-1]


# def shell_radius(shell_index):
#     """그림과 판정에 공통으로 사용하는 궤도 반지름이다."""
#     return 64 + 45 * shell_index


# def approach_distance(active, now):
#     """다가오는 전자와 원자핵 사이의 현재 거리를 반환한다."""
#     progress = min(
#         1.0,
#         max(0.0, (now - active["started"]) / active["duration"]),
#     )
#     radius = shell_radius(active["shell"])
#     return approach_start_radius - progress * (approach_start_radius - radius)


# def create_game(level):
#     """새 게임의 상태를 만들어 반환한다."""
#     return {
#         "level": level,
#         "atom_list": get_atoms(level),
#         "atom_index": 0,
#         "electron_index": 0,
#         "occupied": [],
#         "score": 0,
#         "lives": 3,
#         "screen": "countdown",
#         "countdown_started": time.monotonic(),
#         "last_update": time.monotonic(),
#         "atom_started": time.monotonic(),
#         "active_electron": None,
#     }


# def current_atom():
#     game = st.session_state.game
#     return game["atom_list"][game["atom_index"]]


# def start_electron(now):
#     """현재 원자에 채울 다음 전자를 궤도 바깥에서 출발시킨다."""
#     game = st.session_state.game
#     shell_index, slot_index, capacity = get_shell_slot(game["electron_index"])
#     angle = math.pi / 2 + slot_index * (2 * math.pi / capacity)
#     speed = difficulty_settings[game["level"]]["approach_seconds"]

#     game["active_electron"] = {
#         "phase": "approach",
#         "started": now,
#         "duration": speed,
#         "angle": angle,
#         "target_angle": angle,
#         "shell": shell_index,
#         "slot": slot_index,
#         "capacity": capacity,
#         "landed_at": None,
#         "orbit_started": None,
#     }


# def update_game_clock(now):
#     """카운트다운과 전자 공전을 갱신하고, 세 바퀴가 지나면 목숨을 깎는다."""
#     game = st.session_state.game
#     game["last_update"] = now

#     if game["screen"] == "countdown":
#         if now - game["countdown_started"] >= 3:
#             game["screen"] = "playing"
#             start_electron(now)
#         return

#     active = game["active_electron"]
#     if game["screen"] != "playing" or active is None:
#         return

#     if active["phase"] == "approach":
#         if now - active["started"] >= active["duration"]:
#             active["phase"] = "landing"
#             active["landed_at"] = active["started"] + active["duration"]

#     elif active["phase"] == "landing":
#         if now - active["landed_at"] >= landing_grace_seconds:
#             active["phase"] = "orbit"
#             active["orbit_started"] = now

#     elif active["phase"] == "orbit":
#         orbit_progress = difficulty_settings[game["level"]]["orbit_speed"] * (
#             now - active["orbit_started"]
#         )
#         active["angle"] = active["target_angle"] + orbit_progress

#         if orbit_progress >= 3 * 2 * math.pi:
#             lose_life("전자 공전 3회 초과")


# def lose_life(reason):
#     """오입력 또는 제한 시간 초과로 목숨을 하나 줄인다."""
#     game = st.session_state.game
#     game["lives"] -= 1
#     game["last_message"] = f"{reason}: 목숨 -1"

#     if game["lives"] <= 0:
#         game["screen"] = "ended"
#         return

#     start_electron(time.monotonic())


# def place_electron(points):
#     """전자 하나를 안착시키고 점수 및 원자 진행 상태를 갱신한다."""
#     game = st.session_state.game
#     active = game["active_electron"]

#     game["score"] += points
#     game["occupied"].append(
#         (active["shell"], active["slot"], active["capacity"])
#     )
#     game["electron_index"] += 1
#     game["last_message"] = f"성공 +{points}점"
#     game["active_electron"] = None

#     atom = current_atom()
#     if game["electron_index"] >= atom[0]:
#         game["atom_index"] += 1

#         if game["atom_index"] >= len(game["atom_list"]):
#             game["screen"] = "ended"
#             game["completed"] = True
#             return

#         game["electron_index"] = 0
#         game["occupied"] = []
#         game["atom_started"] = time.monotonic()

#     start_electron(time.monotonic())


# def handle_click():
#     """마우스로 누른 전자 선택 버튼의 타이밍을 판정한다."""
#     game = st.session_state.game
#     if game["screen"] != "playing":
#         return

#     active = game["active_electron"]
#     if active is None:
#         lose_life("잘못된 입력")
#         return

#     now = time.monotonic()

#     if active["phase"] == "approach":
#         distance_to_shell = (
#             approach_distance(active, now) - shell_radius(active["shell"])
#         )

#         if distance_to_shell <= contact_tolerance:
#             place_electron(3)
#         else:
#             lose_life("도착 타이밍을 놓침")

#     elif active["phase"] == "landing":
#         place_electron(3)

#     elif active["phase"] == "orbit":
#         target_angle = active["target_angle"]
#         orbit_progress = active["angle"] - target_angle
#         difference = (
#             (active["angle"] - target_angle + math.pi) % (2 * math.pi)
#             - math.pi
#         )

#         if orbit_progress >= 2 * math.pi - 0.18 and abs(difference) <= 0.18:
#             place_electron(1)
#         else:
#             lose_life("궤도 타깃 밖에서 입력")


# def render_orbit():
#     """원자와 공전하는 전자를 SVG 도형으로 만들어 Streamlit에 표시한다."""
#     game = st.session_state.game
#     atom = current_atom()
#     active = game["active_electron"]
#     now = time.monotonic()
#     center = 310

#     total = atom[0]
#     shell_count = 0
#     for capacity in shell_capacities:
#         shell_count += 1
#         total -= capacity
#         if total <= 0:
#             break

#     radii = [shell_radius(index) for index in range(shell_count)]

#     def point(angle, radius):
#         return (
#             center + radius * math.cos(angle),
#             center - radius * math.sin(angle),
#         )

#     parts = [
#         '<svg xmlns="http://www.w3.org/2000/svg" width="620" '
#         'height="620" viewBox="0 0 620 620">',
#         '<defs><radialGradient id="bg">'
#         '<stop stop-color="#172b49"/>'
#         '<stop offset="1" stop-color="#07111f"/>'
#         '</radialGradient>',
#         '<radialGradient id="nucleus">'
#         '<stop stop-color="#d4fff7"/>'
#         '<stop offset="0.5" stop-color="#57e5d1"/>'
#         '<stop offset="1" stop-color="#178a9a"/>'
#         '</radialGradient>',
#         '<filter id="glow">'
#         '<feGaussianBlur stdDeviation="5" result="blur"/>'
#         '<feMerge><feMergeNode in="blur"/>'
#         '<feMergeNode in="SourceGraphic"/></feMerge>'
#         '</filter></defs>',
#         '<rect width="620" height="620" rx="30" fill="url(#bg)"/>',
#     ]

#     for radius in radii:
#         parts.append(
#             f'<circle cx="{center}" cy="{center}" r="{radius}" '
#             'fill="none" stroke="#496787" stroke-width="2" '
#             'stroke-opacity="0.7"/>'
#         )

#     # 이미 채운 전자들도 계속 공전한다.
#     rotation = (now - game["atom_started"]) * 0.55

#     for shell_index, slot_index, capacity in game["occupied"]:
#         radius = radii[shell_index]
#         angle = (
#             math.pi / 2
#             + slot_index * (2 * math.pi / capacity)
#             + rotation
#         )
#         x, y = point(angle, radius)
#         parts.append(
#             f'<circle cx="{x:.2f}" cy="{y:.2f}" r="6" '
#             'fill="#91b7ff" filter="url(#glow)"/>'
#         )

#     if active is not None:
#         radius = radii[active["shell"]]
#         target_angle = active["target_angle"]

#         # 초록 호는 처음 안착하는 위치에 고정된다.
#         x1, y1 = point(target_angle - 0.18, radius)
#         x2, y2 = point(target_angle + 0.18, radius)
#         parts.append(
#             f'<path d="M {x1:.2f} {y1:.2f} '
#             f'A {radius} {radius} 0 0 0 {x2:.2f} {y2:.2f}" '
#             'fill="none" stroke="#56efd1" stroke-width="9" '
#             'stroke-linecap="round" filter="url(#glow)"/>'
#         )

#         if active["phase"] == "approach":
#             distance = approach_distance(active, now)
#         else:
#             distance = radius

#         x, y = point(active["angle"], distance)
#         parts.append(
#             f'<circle cx="{x:.2f}" cy="{y:.2f}" r="10" '
#             'fill="#ffe5a1" filter="url(#glow)"/>'
#         )

#     parts.append(
#         f'<circle cx="{center}" cy="{center}" r="38" '
#         'fill="url(#nucleus)" filter="url(#glow)"/>'
#     )
#     parts.append(
#         f'<text x="{center}" y="{center + 10}" '
#         'text-anchor="middle" font-family="sans-serif" '
#         'font-size="28" font-weight="800" fill="#092030">'
#         f'{atom[1]}</text>'
#     )
#     parts.append("</svg>")

#     st.image(
#         "".join(parts),
#         width=620,
#         alt=f"{atom[2]} 원자와 전자껍질",
#     )
#     st.caption(
#         "파란 전자: 안착 후 공전 · 노란 전자: 현재 전자 · "
#         "초록 호: 처음 안착하고 다시 돌아오는 자리"
#     )


# def render_menu():
#     st.title("⚛️ Shell Beat")
#     st.subheader("전자껍질을 리듬에 맞춰 채워라")
#     st.write(
#         "전자가 초록 호에 처음 닿을 때 클릭하면 3점, "
#         "한 바퀴 이상 돌아 같은 호에 다시 닿을 때 클릭하면 1점입니다."
#     )

#     level = st.selectbox("난이도", list(difficulty_settings.keys()))
#     st.caption("쉬움: H–Ne · 보통: Na–Kr · 어려움: Rb–U")

#     if st.button("게임 시작", type="primary"):
#         st.session_state.game = create_game(level)
#         st.session_state.game["last_message"] = ""
#         st.session_state.screen = "game"
#         st.rerun()


# @st.fragment(run_every=0.08)
# def render_game():
#     if "game" not in st.session_state:
#         st.session_state.screen = "menu"
#         st.rerun()
#         return

#     update_game_clock(time.monotonic())
#     game = st.session_state.game

#     if game["screen"] == "ended":
#         st.title("게임 종료")
#         st.metric("최종 점수", game["score"])

#         if game.get("completed", False):
#             st.success("선택한 난이도의 모든 원소를 완성했습니다!")
#         else:
#             st.info("목숨을 모두 사용했습니다. 다시 도전해 보세요.")

#         left, right = st.columns(2)

#         if left.button("메뉴로 돌아가기"):
#             st.session_state.screen = "menu"
#             st.rerun()

#         if right.button("다시 하기", type="primary"):
#             st.session_state.game = create_game(game["level"])
#             st.session_state.game["last_message"] = ""
#             st.rerun()

#         return

#     atom = current_atom()
#     next_atom_index = game["atom_index"] + 1
#     next_symbol = (
#         game["atom_list"][next_atom_index][1]
#         if next_atom_index < len(game["atom_list"])
#         else "완성"
#     )

#     left, spacer, right = st.columns([1, 2, 1])

#     with left:
#         st.metric("목숨", "♥ " * game["lives"])

#     with right:
#         st.metric("현재 점수", game["score"])
#         st.metric("다음 원소", next_symbol)

#     st.subheader(f"{atom[2]} ({atom[1]}) · 원자번호 {atom[0]}")
#     st.write(
#         f"전자 채우기: "
#         f"{min(game['electron_index'], atom[0])} / {atom[0]}"
#     )

#     if game["screen"] == "countdown":
#         remaining = max(
#             1,
#             3 - int(time.monotonic() - game["countdown_started"]),
#         )
#         st.info(f"시작까지 {remaining}초")
#     else:
#         render_orbit()

#         if game.get("last_message"):
#             st.caption(game["last_message"])

#         if st.button(
#             "전자 선택 · 클릭",
#             type="primary",
#             use_container_width=True,
#         ):
#             handle_click()

#         st.caption(
#             "노란 전자가 초록 호에 처음 닿으면 3점, "
#             "한 바퀴 돌아 다시 닿으면 1점입니다."
#         )


# def main():
#     if "screen" not in st.session_state:
#         st.session_state.screen = "menu"

#     if st.session_state.screen == "menu":
#         render_menu()
#     else:
#         render_game()


# main()
import math
import time
import streamlit as st

st.set_page_config(page_title="Shell Beat", page_icon="⚛️", layout="wide")

# (원자번호, 원소 기호, 원소 이름)
ELEMENTS = [
    (1, "H", "수소"), (2, "He", "헬륨"), (3, "Li", "리튬"), (4, "Be", "베릴륨"),
    (5, "B", "붕소"), (6, "C", "탄소"), (7, "N", "질소"), (8, "O", "산소"),
    (9, "F", "플루오린"), (10, "Ne", "네온"), (11, "Na", "나트륨"), (12, "Mg", "마그네슘"),
    (13, "Al", "알루미늄"), (14, "Si", "규소"), (15, "P", "인"), (16, "S", "황"),
    (17, "Cl", "염소"), (18, "Ar", "아르곤"), (19, "K", "칼륨"), (20, "Ca", "칼슘"),
    (21, "Sc", "스칸듐"), (22, "Ti", "티타늄"), (23, "V", "바나듐"), (24, "Cr", "크로뮴"),
    (25, "Mn", "망가니즈"), (26, "Fe", "철"), (27, "Co", "코발트"), (28, "Ni", "니켈"),
    (29, "Cu", "구리"), (30, "Zn", "아연"), (31, "Ga", "갈륨"), (32, "Ge", "저마늄"),
    (33, "As", "비소"), (34, "Se", "셀레늄"), (35, "Br", "브로민"), (36, "Kr", "크립톤"),
    (37, "Rb", "루비듐"), (38, "Sr", "스트론튬"), (39, "Y", "이트륨"), (40, "Zr", "지르코늄"),
    (41, "Nb", "나이오븀"), (42, "Mo", "몰리브데넘"), (43, "Tc", "테크네튬"), (44, "Ru", "루테늄"),
    (45, "Rh", "로듐"), (46, "Pd", "팔라듐"), (47, "Ag", "은"), (48, "Cd", "카드뮴"),
    (49, "In", "인듐"), (50, "Sn", "주석"), (51, "Sb", "안티모니"), (52, "Te", "텔루륨"),
    (53, "I", "아이오딘"), (54, "Xe", "제논"), (55, "Cs", "세슘"), (56, "Ba", "바륨"),
    (57, "La", "란타넘"), (58, "Ce", "세륨"), (59, "Pr", "프라세오디뮴"), (60, "Nd", "네오디뮴"),
    (61, "Pm", "프로메튬"), (62, "Sm", "사마륨"), (63, "Eu", "유로퓸"), (64, "Gd", "가돌리늄"),
    (65, "Tb", "터븀"), (66, "Dy", "디스프로슘"), (67, "Ho", "홀뮴"), (68, "Er", "어븀"),
    (69, "Tm", "툴륨"), (70, "Yb", "이터븀"), (71, "Lu", "루테튬"), (72, "Hf", "하프늄"),
    (73, "Ta", "탄탈럼"), (74, "W", "텅스텐"), (75, "Re", "레늄"), (76, "Os", "오스뮴"),
    (77, "Ir", "이리듐"), (78, "Pt", "백금"), (79, "Au", "금"), (80, "Hg", "수은"),
    (81, "Tl", "탈륨"), (82, "Pb", "납"), (83, "Bi", "비스무트"), (84, "Po", "폴로늄"),
    (85, "At", "아스타틴"), (86, "Rn", "라돈"), (87, "Fr", "프랑슘"), (88, "Ra", "라듐"),
    (89, "Ac", "악티늄"), (90, "Th", "토륨"), (91, "Pa", "프로트악티늄"), (92, "U", "우라늄"),
]

SHELL_CAPACITIES = [2, 8, 18, 32, 32, 18, 8]
APPROACH_START_RADIUS = 295
CONTACT_TOLERANCE = 14
LANDING_GRACE_SECONDS = 0.30

DIFFICULTY_SETTINGS = {
    "쉬움": {"min_number": 1, "max_number": 10, "approach_seconds": 2.3, "orbit_speed": 1.5},
    "보통": {"min_number": 11, "max_number": 36, "approach_seconds": 1.6, "orbit_speed": 2.0},
    "어려움": {"min_number": 37, "max_number": 92, "approach_seconds": 1.1, "orbit_speed": 2.6},
}


def get_atoms(level):
    """난이도에 해당하는 원자 목록을 반환한다."""
    setting = DIFFICULTY_SETTINGS[level]
    atom_list = []

    for atom in ELEMENTS:
        if setting["min_number"] <= atom[0] <= setting["max_number"]:
            atom_list.append(atom)

    return atom_list


def get_shell_slot(electron_index):
    """전자 번호를 껍질 번호와 껍질 안의 슬롯 번호로 바꾼다."""
    remaining = electron_index

    for shell_index, capacity in enumerate(SHELL_CAPACITIES):
        if remaining < capacity:
            return shell_index, remaining, capacity
        remaining -= capacity

    return len(SHELL_CAPACITIES) - 1, 0, SHELL_CAPACITIES[-1]


def shell_radius(shell_index):
    """그림과 판정에 공통으로 사용하는 궤도 반지름이다 (최대 7껍질 = 262)."""
    return 58 + 34 * shell_index


def approach_distance(active, now):
    """다가오는 전자와 원자핵 사이의 현재 거리를 반환한다."""
    progress = min(
        1.0,
        max(0.0, (now - active["started"]) / active["duration"]),
    )
    radius = shell_radius(active["shell"])
    return APPROACH_START_RADIUS - progress * (APPROACH_START_RADIUS - radius)


def create_game(level):
    """새 게임의 상태를 만들어 반환한다."""
    now = time.monotonic()
    return {
        "level": level,
        "atom_list": get_atoms(level),
        "atom_index": 0,
        "electron_index": 0,
        "occupied": [],
        "score": 0,
        "lives": 3,
        "screen": "countdown",
        "countdown_started": now,
        "last_update": now,
        "atom_started": now,
        "active_electron": None,
        "last_message": "",
    }


def current_atom():
    game = st.session_state.game
    return game["atom_list"][game["atom_index"]]


def start_electron(now):
    """현재 원자에 채울 다음 전자를 궤도 바깥에서 출발시킨다."""
    game = st.session_state.game
    shell_index, slot_index, capacity = get_shell_slot(game["electron_index"])
    angle = math.pi / 2 + slot_index * (2 * math.pi / capacity)
    speed = DIFFICULTY_SETTINGS[game["level"]]["approach_seconds"]

    game["active_electron"] = {
        "phase": "approach",
        "started": now,
        "duration": speed,
        "angle": angle,
        "target_angle": angle,
        "shell": shell_index,
        "slot": slot_index,
        "capacity": capacity,
        "landed_at": None,
        "orbit_started": None,
    }


def update_game_clock(now):
    """카운트다운과 전자 공전을 갱신하고, 세 바퀴가 지나면 목숨을 깎는다."""
    game = st.session_state.game
    game["last_update"] = now

    if game["screen"] == "countdown":
        if now - game["countdown_started"] >= 3:
            game["screen"] = "playing"
            start_electron(now)
        return

    active = game["active_electron"]
    if game["screen"] != "playing" or active is None:
        return

    if active["phase"] == "approach":
        if now - active["started"] >= active["duration"]:
            active["phase"] = "landing"
            active["landed_at"] = active["started"] + active["duration"]

    elif active["phase"] == "landing":
        if now - active["landed_at"] >= LANDING_GRACE_SECONDS:
            active["phase"] = "orbit"
            active["orbit_started"] = now

    elif active["phase"] == "orbit":
        orbit_progress = DIFFICULTY_SETTINGS[game["level"]]["orbit_speed"] * (
            now - active["orbit_started"]
        )
        active["angle"] = active["target_angle"] + orbit_progress

        if orbit_progress >= 3 * 2 * math.pi:
            lose_life("전자 공전 3회 초과")


def lose_life(reason):
    """오입력 또는 제한 시간 초과로 목숨을 하나 줄인다."""
    game = st.session_state.game
    game["lives"] -= 1
    game["last_message"] = f"{reason}: 목숨 -1"

    if game["lives"] <= 0:
        game["screen"] = "ended"
        return

    start_electron(time.monotonic())


def place_electron(points):
    """전자 하나를 안착시키고 점수 및 원자 진행 상태를 갱신한다."""
    game = st.session_state.game
    active = game["active_electron"]

    game["score"] += points
    game["occupied"].append(
        (active["shell"], active["slot"], active["capacity"])
    )
    game["electron_index"] += 1
    game["last_message"] = f"성공 +{points}점"
    game["active_electron"] = None

    atom = current_atom()
    if game["electron_index"] >= atom[0]:
        game["atom_index"] += 1

        if game["atom_index"] >= len(game["atom_list"]):
            game["screen"] = "ended"
            game["completed"] = True
            return

        game["electron_index"] = 0
        game["occupied"] = []
        game["atom_started"] = time.monotonic()

    start_electron(time.monotonic())


def handle_click():
    """마우스로 누른 전자 선택 버튼의 타이밍을 판정한다."""
    game = st.session_state.game
    if game["screen"] != "playing":
        return

    active = game["active_electron"]
    if active is None:
        lose_life("잘못된 입력")
        return

    now = time.monotonic()

    if active["phase"] == "approach":
        distance_to_shell = abs(
            approach_distance(active, now) - shell_radius(active["shell"])
        )

        if distance_to_shell <= CONTACT_TOLERANCE:
            place_electron(3)
        else:
            lose_life("도착 타이밍을 놓침")

    elif active["phase"] == "landing":
        place_electron(3)

    elif active["phase"] == "orbit":
        target_angle = active["target_angle"]
        orbit_progress = active["angle"] - target_angle
        difference = (
            (active["angle"] - target_angle + math.pi) % (2 * math.pi)
            - math.pi
        )

        if orbit_progress >= 2 * math.pi - 0.18 and abs(difference) <= 0.18:
            place_electron(1)
        else:
            lose_life("궤도 타깃 밖에서 입력")


def render_orbit():
    """원자와 공전하는 전자를 SVG 도형으로 만들어 Streamlit에 표시한다."""
    game = st.session_state.game
    atom = current_atom()
    active = game["active_electron"]
    now = time.monotonic()
    center = 310

    total = atom[0]
    shell_count = 0
    for capacity in SHELL_CAPACITIES:
        shell_count += 1
        total -= capacity
        if total <= 0:
            break

    radii = [shell_radius(index) for index in range(shell_count)]

    def point(angle, radius):
        return (
            center + radius * math.cos(angle),
            center - radius * math.sin(angle),
        )

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="620" '
        'height="620" viewBox="0 0 620 620">',
        '<defs><radialGradient id="bg">'
        '<stop stop-color="#172b49"/>'
        '<stop offset="1" stop-color="#07111f"/>'
        '</radialGradient>',
        '<radialGradient id="nucleus">'
        '<stop stop-color="#d4fff7"/>'
        '<stop offset="0.5" stop-color="#57e5d1"/>'
        '<stop offset="1" stop-color="#178a9a"/>'
        '</radialGradient>',
        '<filter id="glow">'
        '<feGaussianBlur stdDeviation="5" result="blur"/>'
        '<feMerge><feMergeNode in="blur"/>'
        '<feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter></defs>',
        '<rect width="620" height="620" rx="30" fill="url(#bg)"/>',
    ]

    for radius in radii:
        parts.append(
            f'<circle cx="{center}" cy="{center}" r="{radius}" '
            'fill="none" stroke="#496787" stroke-width="2" '
            'stroke-opacity="0.7"/>'
        )

    # 이미 채운 전자들도 계속 공전한다.
    rotation = (now - game["atom_started"]) * 0.55

    for shell_index, slot_index, capacity in game["occupied"]:
        radius = radii[shell_index]
        angle = (
            math.pi / 2
            + slot_index * (2 * math.pi / capacity)
            + rotation
        )
        x, y = point(angle, radius)
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="6" '
            'fill="#91b7ff" filter="url(#glow)"/>'
        )

    if active is not None:
        radius = radii[active["shell"]]
        target_angle = active["target_angle"]

        # 초록 호는 처음 안착하는 위치에 고정된다.
        x1, y1 = point(target_angle - 0.18, radius)
        x2, y2 = point(target_angle + 0.18, radius)
        parts.append(
            f'<path d="M {x1:.2f} {y1:.2f} '
            f'A {radius} {radius} 0 0 0 {x2:.2f} {y2:.2f}" '
            'fill="none" stroke="#56efd1" stroke-width="9" '
            'stroke-linecap="round" filter="url(#glow)"/>'
        )

        if active["phase"] == "approach":
            distance = approach_distance(active, now)
        else:
            distance = radius

        x, y = point(active["angle"], distance)
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="10" '
            'fill="#ffe5a1" filter="url(#glow)"/>'
        )

    parts.append(
        f'<circle cx="{center}" cy="{center}" r="38" '
        'fill="url(#nucleus)" filter="url(#glow)"/>'
    )
    parts.append(
        f'<text x="{center}" y="{center + 10}" '
        'text-anchor="middle" font-family="sans-serif" '
        'font-size="28" font-weight="800" fill="#092030">'
        f'{atom[1]}</text>'
    )
    parts.append("</svg>")

    st.image(
        "".join(parts),
        width=620,
        alt=f"{atom[2]} 원자와 전자껍질",
    )
    st.caption(
        "파란 전자: 안착 후 공전 · 노란 전자: 현재 전자 · "
        "초록 호: 처음 안착하고 다시 돌아오는 자리"
    )


def render_menu():
    st.title("⚛️ Shell Beat")
    st.subheader("전자껍질을 리듬에 맞춰 채워라")
    st.write(
        "전자가 초록 호에 처음 닿을 때 클릭하면 3점, "
        "한 바퀴 이상 돌아 같은 호에 다시 닿을 때 클릭하면 1점입니다."
    )

    level = st.selectbox("난이도", list(DIFFICULTY_SETTINGS.keys()))
    st.caption("쉬움: H–Ne · 보통: Na–Kr · 어려움: Rb–U")

    if st.button("게임 시작", type="primary"):
        st.session_state.game = create_game(level)
        st.session_state.screen = "game"
        st.rerun()


@st.fragment(run_every=0.08)
def render_game():
    if "game" not in st.session_state:
        st.session_state.screen = "menu"
        st.rerun()
        return

    update_game_clock(time.monotonic())
    game = st.session_state.game

    if game["screen"] == "ended":
        st.title("게임 종료")
        st.metric("최종 점수", game["score"])

        if game.get("completed", False):
            st.success("선택한 난이도의 모든 원소를 완성했습니다!")
        else:
            st.info("목숨을 모두 사용했습니다. 다시 도전해 보세요.")

        left, right = st.columns(2)

        if left.button("메뉴로 돌아가기"):
            st.session_state.screen = "menu"
            st.rerun()

        if right.button("다시 하기", type="primary"):
            st.session_state.game = create_game(game["level"])
            st.rerun()

        return

    atom = current_atom()
    next_atom_index = game["atom_index"] + 1
    next_symbol = (
        game["atom_list"][next_atom_index][1]
        if next_atom_index < len(game["atom_list"])
        else "완성"
    )

    left, spacer, right = st.columns([1, 2, 1])

    with left:
        st.metric("목숨", "♥ " * game["lives"])

    with right:
        st.metric("현재 점수", game["score"])
        st.metric("다음 원소", next_symbol)

    st.subheader(f"{atom[2]} ({atom[1]}) · 원자번호 {atom[0]}")
    st.write(
        f"전자 채우기: "
        f"{min(game['electron_index'], atom[0])} / {atom[0]}"
    )

    if game["screen"] == "countdown":
        remaining = max(
            1,
            3 - int(time.monotonic() - game["countdown_started"]),
        )
        st.info(f"시작까지 {remaining}초")
    else:
        render_orbit()

        if game.get("last_message"):
            st.caption(game["last_message"])

        if st.button(
            "전자 선택 · 클릭",
            type="primary",
            use_container_width=True,
        ):
            handle_click()

        st.caption(
            "노란 전자가 초록 호에 처음 닿으면 3점, "
            "한 바퀴 돌아 다시 닿으면 1점입니다."
        )


def main():
    if "screen" not in st.session_state:
        st.session_state.screen = "menu"

    if st.session_state.screen == "menu":
        render_menu()
    else:
        render_game()


if __name__ == "__main__":
    main()
