
import customtkinter as ctk     # CustomTkinter: 현대적 디자인의 Tkinter 확장 라이브러리
import tkinter as tk            # Tkinter: Python 표준 GUI 툴킷
import tkinter.messagebox as messagebox  # 메시지 박스 대화상자 (알림, 확인)
import requests                 # HTTP 요청 처리 라이브러리
import random                   # 무작위 샘플링/랜덤 기능
from io import BytesIO          # 메모리 상의 이진 스트림 처리
from PIL import Image, ImageTk  # Pillow: 이미지 처리 및 Tkinter용 이미지 변환
from datetime import datetime   # 날짜 및 시간 처리
import webbrowser               # 기본 웹 브라우저 열기 기능

# ─── 전역 상수 설정 (테마 색상 및 API 설정) ─────────────────────────────────────
BACKGROUND_COLOR = "#1e2a38"     # 배경 색상 (감성 시네마 테마)
TEXT_COLOR       = "#f0f0f0"     # 기본 텍스트 색상
HIGHLIGHT_COLOR  = "#f4d35e"     # 하이라이트/버튼 색상

API_KEY        = '2bfcc21dcdffb42ad6817ff4f8f4e65e'  # TMDb API 키
BASE_URL       = 'https://api.themoviedb.org/3'       # TMDb API 기본 URL
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w300'    # TMDb 포스터 이미지 URL 템플릿

#영화 데이터베이스에 정보를 부탁하고, 파이썬 자료로 받아 오는 일
def tmdb(path, filters=None):
    """
    BASE_URL+path 로 TMDb GET 요청을 보내고 JSON 반환.
    실패 시 빈 dict 반환.
    """
    # 인증·언어 파라미터 기본 세트
    query = {'api_key': API_KEY, 'language': 'ko-KR'}
    # 호출 시 넘긴 filters(dict)가 있으면 병합
    if filters:
        query.update(filters)
    try:
        resp = requests.get(f"{BASE_URL}{path}", params=query)
        return resp.json()
    except Exception:
        return {}

# ─── 장르 및 감정→장르 매핑 ─────────────────────────────────────────────────────
# TMDb 장르 ID를 한국어 명으로 변환하는 딕셔너리
genre_mapping = {
    28: '액션', 12: '모험', 16: '애니메이션', 35: '코미디', 80: '범죄',
    99: '다큐멘터리', 18: '드라마', 10751: '가족', 14: '판타지', 36: '역사',
    27: '공포', 10402: '뮤지컬', 9648: '미스터리', 10749: '로맨스', 878: 'SF',
    10770: 'TV 영화', 53: '스릴러', 10752: '전쟁', 37: '서부'
}
# 사용자가 느끼는 감정별 추천 장르 리스트
feeling_genre_map = {
    '기쁨': ['코미디', '뮤지컬', '가족', '로맨스', '모험'],
    '슬픔': ['드라마', '다큐멘터리', '로맨스', '역사'],
    '긴장': ['스릴러', '범죄', '공포', '미스터리'],
    '활기': ['액션', '모험', 'SF', '코미디'],
    '차분': ['드라마', '역사', '다큐멘터리', '애니메이션'],
    '설렘': ['로맨스', '뮤지컬', '가족'],
    '흥분': ['액션', '스릴러', '모험', '전쟁', '뮤지컬'],
    '무서움': ['공포', '스릴러', '미스터리'],
    '아무거나': sorted(list(set(genre_mapping.values())))  # 모든 장르
}
#영화 ID로 대한민국 OTT 제공사 목록 조회
def get_tmdb_streaming_services(movie_id):
    kr = tmdb(f"/movie/{movie_id}/watch/providers") \
         .get("results", {}) \
         .get("KR", {})
    return [p["provider_name"] for p in kr.get("flatrate", [])]

#영화 ID로 유튜브 예고편 URL 제공
def get_movie_trailer_url(movie_id):
    videos = tmdb(f"/movie/{movie_id}/videos").get("results", [])
    for i in videos:
        if i.get("site") == "YouTube" and i.get("type") == "Trailer":
            return f"https://www.youtube.com/watch?v={i['key']}"

#장르,국내/외,최신,성인을 필터링하여 결과 수집집 
def discover_movies_by_genre(genre_name, domestic=True, latest=False, adult_only=False, min_rating=0.0, count=5):
    # 1) 장르 ID
    gid = next((g for g,n in genre_mapping.items() if n==genre_name), None)
    if gid == None:
        return []

    # 2) 언어 결정
    if domestic == True:
        lang = 'ko'
    else:
        lang = 'en'


    # 3) 공통 파라미터
    filters = {
        'with_genres': gid,
        'with_original_language': lang,
        'sort_by': 'popularity.desc',
        'include_adult': str(adult_only).lower(),
        'certification_country': 'KR'
    }
    if adult_only == False:
        filters['certification.lte'] = '15'

    if latest:
        filters['primary_release_date.gte'] = '2010-01-01'
        filters['primary_release_date.lte'] = datetime.now().strftime('%Y-%m-%d')
    if min_rating > 0:
        filters['vote_average.gte'] = str(min_rating)

    # 4) 호출 & 누적
    all_movies = []
    for page in range(1, 6):
        # filters 사전 복사 후 페이지 번호만 추가
        query = filters.copy()
        query['page'] = page
        data = tmdb('/discover/movie', filters=query)
        all_movies.extend(data.get('results', []))


    # 5) 포스터 있는 것만, 샘플링
    valid = [m for m in all_movies if m.get('poster_path')]
    if valid == []:
        return []
    return random.sample(valid, min(count, len(valid)))


#TMDb 장르 ID 리스트 → 한글 장르명 리스트 변환 
def map_genres(genre_ids):
    """
    Args:
        genre_ids (List[int]): TMDb가 반환한 장르 ID들의 리스트

    Returns:
        List[str]: 각 ID에 대응하는 한국어 장르명. 매핑에 없으면 "알수없음" 문자열 반환.
    """
    # 리스트 컴프리헨션을 사용해 각 genre_id를 genre_mapping에서 찾아 반환합니다.
    # genre_mapping은 {ID: '장르명', …} 형태의 사전입니다.
    # .get(key, default)는 키가 없을 때 default를 반환하므로, 알 수 없는 ID는 "알수없음"으로 처리됩니다.
    return [genre_mapping.get(gid, "알수없음")for gid in genre_ids]  # gid가 매핑에 있으면 그 값을, 없으면 "알수없음"           # genre_ids 리스트의 각 ID에 대해 반복

#추천 리스트를 GUI(스크롤 프레임)에 포스터 · 제목 · 정보 · 버튼으로 렌더링 
def recommend_movies(user_genre, user_country, latest=False, adult_only=False, count=5, min_rating=0.0):
    """
    사용자의 선택(장르, 국가, 최신 여부, 성인 여부, 최소 평점)에 맞춰
    영화 목록을 탐색하고 최종 추천 리스트를 반환합니다.

    Args:
        user_genre (str): 사용자가 선택한 한글 장르명 또는 '랜덤 추천'
        user_country (str): '국내' 또는 '국외' (원어 언어 코드 결정)
        latest (bool): True면 2010년 이후 개봉작만 포함
        adult_only (bool): True면 청불 영화만, False면 전체(인증 15세 이하만)
        count (int): 최종 추천할 영화 개수
        min_rating (float): 최소 평점 필터 (예: 7.0 이상)

    Returns:
        List[dict]: genre_names가 추가된 영화 dict 목록
    """
    # 1) 국가 코드 변환: '국내'→'ko', '국외'→'en', 기본 'ko'
    lang_code = {'국내': 'ko', '국외': 'en'}.get(user_country, 'ko')

    # 2) '랜덤 추천'일 경우, genre_mapping의 모든 장르 중 무작위 선택
    if user_genre == '랜덤 추천':
        user_genre = random.choice(list(genre_mapping.values()))

    # 3) TMDb API로 영화 탐색 (count*3만큼 넉넉히 가져와 평점 필터 후 샘플링)
    movies = discover_movies_by_genre(
        genre_name=user_genre,
        domestic=(user_country=='국내'),
        latest=latest,
        adult_only=adult_only,
        min_rating=min_rating,
        count=5)

    # 4) 장르 ID → 한글명 매핑
    for m in movies:
        m['genre_names'] = [genre_mapping.get(gid, "알수없음") for gid in m.get('genre_ids', [])]

    # 5) 최종 리스트 바로 반환
    return movies

def display_recommendation(movies):
    """
    주어진 영화 리스트를 메인 창에 표시합니다.
    각 영화마다 포스터, 제목, 장르/평점/줄거리, '상세 보기' 버튼을 생성합니다.

    Args:
        movies (List[dict]): recommend_movies()가 반환한 영화 데이터 리스트.
    """
    # 1) 이전에 그려진 추천 항목 모두 제거
    for widget in frame.winfo_children():
        widget.destroy()

    # 2) 추천 영화 목록 순회
    for movie in movies:
        # 2-1) 각 영화를 담을 컨테이너 프레임 생성
        container = ctk.CTkFrame(frame, fg_color="white", width=720)
        container.pack(pady=10)             # 위/아래 10px 여백
        container.pack_propagate(False)     # 내부 위젯 크기에 따라 컨테이너 크기 변경 방지

        # 2-2) 포스터와 텍스트를 담을 내부 프레임 생성
        content_frame = tk.Frame(container, bg="white")
        content_frame.pack(fill="x", padx=10, pady=5)

        # 3) 포스터 표시
        poster_path = movie.get('poster_path')
        if poster_path:
            try:
                # 3-1) 이미지 URL 생성 및 다운로드
                full_url = IMAGE_BASE_URL + poster_path
                img_data = BytesIO(requests.get(full_url).content)
                # 3-2) Pillow로 이미지 로드 후 크기 조정
                img = Image.open(img_data).resize((120, 180))
                photo = ImageTk.PhotoImage(img)
                # 3-3) Label에 이미지 삽입
                poster_label = tk.Label(content_frame, image=photo, bg="white")
                poster_label.image = photo   # 참조 유지
                poster_label.pack(side="left", padx=10)  # 왼쪽 정렬, 가로 10px 여백
            except Exception:
                pass  # 이미지 로드 실패 시 무시

        # 4) 텍스트 영역 생성
        text_frame = tk.Frame(content_frame, bg="white")
        text_frame.pack(side="left", fill="both", expand=True)

        # 4-1) 제목 표시
        title = tk.Label(
            text_frame,
            text=movie.get("title", "제목 없음"),
            font=("맑은 고딕", 20, "bold"),  # 제목: 20pt, Bold
            fg="black",
            bg="white"
        )
        title.pack(anchor="w")  # 왼쪽 정렬

        # 4-2) 장르, 평점, 줄거리 전처리
        genres = ", ".join(movie.get("genre_names", []))  # 리스트를 콤마로 연결
        rating = movie.get("vote_average", 'N/A')
        overview_raw = movie.get("overview", "줄거리 없음")
        # 줄거리: 최대 150자, 넘으면 '...' 추가
        overview_trimmed = (overview_raw[:150] + "...") if len(overview_raw) > 150 else overview_raw
        # 50자마다 줄바꿈
        overview_lines = '\n'.join([
            overview_trimmed[i:i+50]
            for i in range(0, len(overview_trimmed), 50)
        ])

        # 4-3) 상세 정보 표시
        detail = tk.Label(
            text_frame,
            text=f"장르: {genres}\n평점: {rating}\n{overview_lines}",
            font=("맑은 고딕", 12),  # 상세 텍스트: 12pt
            justify="left",
            anchor="w",
            fg="black",
            bg="white"
        )
        detail.pack(anchor="w", pady=5)

        # 5) '상세 보기' 버튼 생성
        btn = ctk.CTkButton(
            container,
            text="상세 보기",
            command=lambda m=movie: show_detail_popup(m),  # 클릭 시 팝업 호출
            width=100,
            fg_color=HIGHLIGHT_COLOR,
            text_color="black"
        )
        btn.pack(pady=5)

    # 6) 스크롤 영역 업데이트: 스크롤바 범위 재계산
    frame.update_idletasks()
    canvas.itemconfig("frame", window=outer_frame, anchor="n")
    canvas.configure(scrollregion=canvas.bbox("all"))

#영화 ID로 배우(max\_cast)·감독 정보 조회   
def get_movie_credits(movie_id, max_cast=3):
    """
    Args:
        movie_id (int): TMDb 영화 고유 ID
        max_cast (int): 가져올 배우 최대 인원 수 (기본값 3)

    Returns:
        tuple(List[str], str):
            - List[str]: 상위 max_cast 명의 배우 이름
            - str: 감독 이름 (없으면 '정보 없음')
    """
    # 1) API URL 구성: /movie/{movie_id}/credits
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    # 2) 요청 파라미터: API 키와 언어 설정(한국어)
    filters = {
        'api_key': API_KEY,
        'language': 'ko-KR'
    }
    try:
        # 3) HTTP GET 요청 전송
        response = requests.get(url, filters=filters)
        # 4) JSON 응답 파싱
        data = response.json()

        # 5) cast 리스트에서 상위 max_cast 만큼 배우 이름 추출
        #    data.get('cast', [])가 없는 경우 빈 리스트 반환
        cast_list = data.get('cast', [])
        cast_names = [actor['name'] for actor in cast_list[:max_cast]]

        # 6) crew 리스트에서 job == 'Director'인 첫 번째 인물 이름 찾기
        crew_list = data.get('crew', [])
        director = next(
            (member['name'] for member in crew_list if member.get('job') == 'Director'),
            '정보 없음'  # 디렉터 정보가 없으면 기본값
        )

        # 7) 배우 리스트와 감독 이름을 튜플로 반환
        return cast_names, director
    except Exception:
        # 8) 네트워크 오류 또는 파싱 오류 시 안전하게 빈 리스트와 '정보 없음' 반환
        return [], '정보 없음'

#영화 상세 팝업 생성: 제목 포스터 · 평점/개봉일/줄거리(300) · 감독·출연·서비스 · 예고편 버튼 
def show_detail_popup(movie):
    """
    팝업 창은 모달 형태로 메인 윈도우 위에 고정되며,
    Args:
        movie (dict): 영화 데이터 딕셔너리, 키: 'id','title','poster_path',
                      'vote_average','release_date','overview'
    """
    # 1) 팝업창 생성 및 모달 설정
    popup = ctk.CTkToplevel(root)      # 부모(root) 위에 새 창 생성
    popup.transient(root)              # 메인 윈도우 최소화 시 같이 최소화
    popup.lift()                       # 최상위로 띄우기
    popup.title(movie.get('title', '상세 정보'))
    popup.configure(fg_color=BACKGROUND_COLOR)

    # 2) 팝업 크기 초기 고정
    popup.geometry("400x800")         # 너비 400px, 높이 800px

    # 3) 팝업 상단에 영화 제목 표시
    ctk.CTkLabel(
        popup,
        text=movie.get('title', '제목 없음'),
        font=ctk.CTkFont(family="맑은 고딕", size=24, weight="bold"),
        text_color=HIGHLIGHT_COLOR
    ).pack(pady=(20, 10))                # 위쪽 20px, 아래쪽 10px 여백

    # 4) 포스터 표시
    poster_path = movie.get('poster_path')
    if poster_path:
        try:
            # 4-1) 이미지 URL(w500) 생성 및 다운로드
            url = IMAGE_BASE_URL.replace("w300", "w500") + poster_path
            img_data = BytesIO(requests.get(url).content)
            # 4-2) Pillow로 이미지 열고 크기 조정
            img = Image.open(img_data).resize((300, 400))
            photo = ImageTk.PhotoImage(img)
            # 4-3) CTkLabel에 이미지 삽입
            ctk.CTkLabel(popup, image=photo, text="").pack(pady=(0, 10))
            popup.image = photo        # 참조 유지
        except Exception as e:
            print("포스터 로드 실패:", e)

    # 5) 정보 텍스트 준비 (300자 제한)
    overview_raw = movie.get('overview', '줄거리 없음')
    overview = overview_raw[:300] + "..." if len(overview_raw) > 300 else overview_raw

    # 5-1) 평점, 개봉일, 줄거리 포맷팅
    full_text = (
        f"평점: {movie.get('vote_average','정보 없음')}\n"
        f"개봉일: {movie.get('release_date','정보 없음')}\n\n"
        f"줄거리: {overview}\n\n"
    )
    # 5-2) 감독·출연 배우 정보 추가
    cast, director = get_movie_credits(movie.get('id'))
    full_text += f"감독: {director}\n"
    if cast:
        full_text += f"출연: {', '.join(cast)}\n"
    # 5-3) 스트리밍 서비스 정보 추가
    services = get_tmdb_streaming_services(movie.get('id'))
    full_text += f"서비스: {', '.join(services) if services else '정보 없음'}"

    # 5-4) Label에 정보 텍스트 삽입
    info_lbl = tk.Label(
        popup,
        text=full_text,
        wraplength=360,                # 가로 360px에서 줄바꿈
        justify="left",
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR,
        font=("맑은 고딕", 12)
    )
    info_lbl.pack(fill="x", padx=20, pady=(0, 20))

    # 6) 예고편 버튼 배치 (정보 텍스트 바로 아래)
    trailer_url = get_movie_trailer_url(movie.get('id'))
    if trailer_url:
        ctk.CTkButton(
            popup,
            text="🎬 예고편 보기",
            font=ctk.CTkFont(family="맑은 고딕", size=16, weight="bold"),
            command=lambda: webbrowser.open(trailer_url),
            fg_color=HIGHLIGHT_COLOR,
            text_color="black",
            width=180
        ).pack(pady=(00, 30))

    # 7) 컨텐츠에 맞게 최소 크기 재설정
    popup.update_idletasks()
    popup.minsize(popup.winfo_width(), popup.winfo_height())

#감정 선택시 그에 맞는 장르 추천
def update_genre_options(event=None):
    """
    사용자가 '기분' 콤보박스에서 선택을 변경할 때 호출됩니다.
    선택된 기분에 따라 '장르' 콤보박스의 옵션 목록을 갱신합니다.

    Args:
        event: Tkinter 이벤트 객체 (필수 아님)
    """
    # 1) 현재 '기분' 콤보박스에서 선택된 값을 가져옵니다.
    selected_feeling = feeling_entry.get()

    # 2) 사전에 정의된 feeling_genre_map에서 해당 기분에 매핑된 장르 리스트를 조회합니다.
    #    키가 없으면 genre_mapping의 모든 장르명 리스트를 사용합니다.
    genre_list = feeling_genre_map.get(
        selected_feeling,
        list(set(genre_mapping.values()))
    )

    # 3) 기본 '랜덤 추천' 항목을 포함시키기 위해 리스트에 추가한 뒤 중복 제거하고 정렬합니다.
    genre_list = sorted(
        list(set(genre_list + ['랜덤 추천']))
    )

    # 4) '장르' 콤보박스의 옵션(values)을 새로 설정합니다.
    genre_entry.configure(values=genre_list)

    # 5) 콤보박스의 선택값을 기본값 '랜덤 추천'으로 초기화합니다.
    genre_entry.set('랜덤 추천')


#추천 받기 
def on_recommend():
    """
    '🎥 추천 받기' 버튼 클릭 시 호출되는 콜백 함수입니다.
    1) 사용자가 선택한 폼(기분, 장르, 국가, 체크박스) 값을 읽고
    2) recommend_movies() 호출로 영화 추천 리스트 생성
    3) 결과에 따라 메시지박스 또는 display_recommendation으로 화면 갱신

    Args:
        없음 (Tkinter 버튼 클릭 이벤트에 바인딩됨)
    """
    # 1) 폼 위젯에서 현재 선택/체크된 값들을 가져옴
    feeling = feeling_entry.get()          # '기분' 콤보박스 값
    genre = genre_entry.get()              # '장르' 콤보박스 값
    country = country_entry.get()          # '국가' 콤보박스 값 ('국내'/'국외')
    latest = latest_var.get()              # '최신 영화만' 체크박스 여부 (True/False)
    adult_only = adult_var.get()           # '청불 포함' 체크박스 여부
    # 평점 체크: 체크 시 7.0, 아니면 0.0으로 최소 평점 필터 설정
    if rating_var.get():
        min_rating = 7.0
    else:
        min_rating = 0.0


    # 2) recommend_movies 함수 호출: 필터 조건에 맞춰 영화 리스트 반환
    movies = recommend_movies(
        user_genre=genre,
        user_country=country,
        latest=latest,
        adult_only=adult_only,
        count=5,
        min_rating=min_rating
    )

    # 3) 추천 결과가 없으면 알림 대화상자 표시
    if movies == []:
        messagebox.showinfo(
            title="알림",
            message="조건에 맞는 영화를 찾을 수 없습니다."
    )

    # 4) 결과가 있으면 display_recommendation으로 메인 화면 갱신
    else:
        display_recommendation(movies)

def main():
    global root, feeling_entry, genre_entry, country_entry, latest_var, adult_var, rating_var, frame, outer_frame, canvas

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.title("🎬 감정 기반 영화 추천기")
    root.geometry("800x900")

    ctk.CTkLabel(root, text="🎞 오늘 밤 나를 책임져 줄 영화는?", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=25)

    wrapper = ctk.CTkFrame(root, fg_color="transparent")
    wrapper.pack(anchor="center")

    form = ctk.CTkFrame(wrapper, fg_color="transparent")
    form.pack(pady=10, padx=40)

    ctk.CTkLabel(form, text="기분").grid(row=0, column=0, padx=10, pady=8, sticky="w")
    feelings = list(feeling_genre_map.keys())
    feeling_entry = ctk.CTkComboBox(form, values=feelings, width=200, command=update_genre_options)
    feeling_entry.set("기쁨")
    feeling_entry.grid(row=0, column=1, padx=10, pady=8)

    ctk.CTkLabel(form, text="장르").grid(row=1, column=0, padx=10, pady=8, sticky="w")
    genre_entry = ctk.CTkComboBox(form, values=[], width=200)
    genre_entry.grid(row=1, column=1, padx=10, pady=8)
    update_genre_options()

    ctk.CTkLabel(form, text="국가").grid(row=2, column=0, padx=10, pady=8, sticky="w")
    country_entry = ctk.CTkComboBox(form, values=["국내", "국외"], width=200)
    country_entry.set("국내")
    country_entry.grid(row=2, column=1, padx=10, pady=8)

    latest_var = ctk.BooleanVar()
    adult_var = ctk.BooleanVar()
    rating_var = ctk.BooleanVar()
    ctk.CTkCheckBox(form, text="2010년 이후 최신 영화만", variable=latest_var).grid(row=3, columnspan=2, sticky="w", padx=10, pady=5)
    ctk.CTkCheckBox(form, text="청불 영화 포함", variable=adult_var).grid(row=4, columnspan=2, sticky="w", padx=10, pady=5)
    ctk.CTkCheckBox(form, text="평점 7.0 이상만 보기", variable=rating_var).grid(row=5, columnspan=2, sticky="w", padx=10, pady=5)

    ctk.CTkButton(root, text="🎥 추천 받기", command=on_recommend, width=180, height=40).pack(pady=20)

    canvas_frame = ctk.CTkFrame(root, fg_color="#f5f5f5")
    canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)

    canvas = tk.Canvas(canvas_frame, bg="#f5f5f5", bd=0, highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(canvas_frame, orientation="vertical", command=canvas.yview)

    outer_frame = tk.Frame(canvas, bg="#f5f5f5")
    frame = tk.Frame(outer_frame, bg="white")
    frame.pack(anchor="center")  # 수평 중앙 정렬

    canvas.create_window((0, 0), window=outer_frame, anchor="n", tags="frame")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    root.mainloop()

if __name__ == "__main__":
    main()
