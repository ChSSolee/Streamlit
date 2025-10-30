import os

import pandas as pd
import numpy as np
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib import rc
import warnings
warnings.filterwarnings("ignore", message=".*deprecated.*Plotly.*")

st.set_page_config(
    page_title = 'KBO NC Dinos Dashboard',
    page_icon = '⚾️',
    layout = 'wide',
    initial_sidebar_state = 'collapsed',
)


team_colors = {
    'LG': 'rgba(156, 175, 200, 0.8)',
    '한화': 'rgba(156, 175, 200, 0.8)',
    'NC': 'rgba(30, 69, 124, 1)',
    '삼성': 'rgba(156, 175, 200, 0.8)',
    '롯데': 'rgba(156, 175, 200, 0.8)',
    'KT': 'rgba(156, 175, 200, 0.8)',
    '키움': 'rgba(156, 175, 200, 0.8)',
    'SK': 'rgba(156, 175, 200, 0.8)',
    'KIA': 'rgba(156, 175, 200, 0.8)',
    '두산': 'rgba(156, 175, 200, 0.8)',
}

nc_colors = [
    'rgba(30, 69, 124, 1)',
    'rgba(156, 175, 200, 0.8)'
]

koreanize_dict = {'타율': 'avg', '장타율': 'SLG', '출루율': 'OBP', 'OPS': 'OPS',
                  '경기당 득점': 'R/G', '경기당 타점': 'RBI/G', '경기당 안타': 'H/G', '경기당 홈런': 'HR/G',
                  '경기당 루타수': 'TB/G', '경기당 도루성공': 'SB/G', '경기당 도루실패': 'CS/G',
                  '경기당 볼넷': 'BB/G', '경기당 삼진': 'SO/G', '경기당 병살타': 'GDP/G'}

# 데이터 불러오기
def get_df():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    team_df = pd.read_csv(os.path.join(current_dir, 'data/team_rank_table_2008_2018.csv'))
    bat_df = pd.read_csv(os.path.join(current_dir, 'data/regular_season_batter.csv'))
    bat_image = pd.read_csv(os.path.join(current_dir, 'data/nc_player_img.csv'))
    return team_df, bat_df, bat_image

# 선수 세부정보 불러오기
def get_player_detail(column):
    value = nc_bat.loc[nc_bat['batter_name'] == nc_player, column].values[0]
    if value is np.nan:
        return '데이터가 없습니다'
    return value

# 연도별 구단의 경기 당 지표 계산
def stats_by_g(df, stats):
    tmp_df = df.copy()
    col_names = [f'{stat}/G' for stat in stats]
    div_df = tmp_df.apply(lambda x: x[stats] / x['경기'], axis = 1)
    div_df.columns = col_names
    tmp_df = pd.concat([tmp_df, div_df], axis = 1).drop(columns = stats)
    return tmp_df

# 1-10 범위 값을 갖는 rank를 0-1로 min-max 스케일링
def rank_scaling(df):
    df['scaled_rank'] = 1 - ((df['순위'] - df['순위'].min()) / (df['순위'].max() - df['순위'].min()))
    return df

team_df, bat_df, bat_image = get_df()

# 타수 하위 25% 제외
bat_df = bat_df.loc[bat_df['AB'] >= 39, :]
    
# Title section
col1, col2, col3 = st.columns((3.5, 5.5, 1))

# 대시보드 타이틀
with col1:
    st.image("https://www.ncdinos.com/assets/images/sub/emblem01.png"
            ,width = 150)
    st.write('')
with col2:
    st.title('KBO NC Dinos Dashboard')  # st.header('KBO NC dinos Dashboard')
with col3:
    st.write('')
    st.image("https://lgcxydabfbch3774324.cdn.ntruss.com/KBO_IMAGE/KBOHome/resources/images/common/h1_logo.png"
            ,width = 170)
st.divider()

# Player section
st.subheader('NC Dinos Player')

# 선택 위젯 레이아웃 설정
s_col1, s_col2, _, _ = st.columns((0.9, 1.2, 7, 0.9), gap = 'small')

# 조회 연도 선택
with s_col1:
    year = st.selectbox('연도 선택', team_df['연도'].unique(), label_visibility = 'collapsed')

# 조회 선수 선택
if year >= 2013:
    with s_col2:
        nc_bat = bat_df.loc[(bat_df['team'] == 'NC') & (bat_df['year'] == year), :]
        player_lst = list(nc_bat['batter_name'].unique())
        max_ab_pname = nc_bat.sort_values(by='AB',ascending=False)['batter_name'].iloc[0]
        nc_player = st.selectbox('**NC 선수 선택**', player_lst, player_lst.index(max_ab_pname), label_visibility = 'collapsed')
else:
    with s_col2:
        nc_bat = bat_df.loc[(bat_df['team'] == 'NC') & (bat_df['year'] == year), :]
        nc_player = st.selectbox('**NC 선수 선택**', nc_bat['batter_name'].unique(), label_visibility = 'collapsed')

# 차트 레이아웃 설정
if year >= 2013:
    col1, col2, col3, col4, col5 = st.columns((1.2, 1, 2, 2, 3.8), gap = 'small')
    
    # 선수 프로필 이미지
    with col1:
        st.image(bat_image.loc[bat_image['Player Name'] == nc_player, 'Image'].values[0], width='stretch')
    
    # 선수 세부정보
    with col2:
        nc_p_r = get_player_detail('R')
        nc_p_rbi = get_player_detail('RBI')
        nc_p_avg = get_player_detail('avg')
        nc_p_ab = get_player_detail('AB')
        
        st.write('**세부정보**')
        st.write(nc_player)
        st.write(get_player_detail('height/weight'))
        st.write(get_player_detail('position'))
        st.write(f'타율:{nc_p_avg} / 타수:{nc_p_ab}')
        st.write(f'득점:{nc_p_r} / 타점:{nc_p_rbi}')

    with col3:
        team_hr = nc_bat.loc[nc_bat['batter_name'] != nc_player, 'HR'].sum()
        player_hr = nc_bat.loc[nc_bat['batter_name'] == nc_player]['HR'].sum()

        hr_ratio_df = pd.DataFrame({
            'Category': ['팀', '개인'],
            'Count': [team_hr, player_hr]
        })
        hr_ratio_df['Category'] = pd.Categorical(
            hr_ratio_df['Category'],
            categories=['개인', '팀'],
            ordered=True
        )
        hr_ratio_df = hr_ratio_df.sort_values('Category', ascending=True)

        fig = go.Figure(
            data=go.Pie(
                labels=hr_ratio_df['Category'],
                values=hr_ratio_df['Count'],
                hole=0.5,
                marker=dict(colors=nc_colors),
                sort=False,
                hovertemplate=(
                    f"<b>선수명: {nc_player}</b><br>"
                    f"<b>연도: {year}</b><br>"
                    "<b>%{label}: %{value}</b>"
                ),
                textfont=dict(size=14, color='black')
            )
        )

        fig.update_layout(
            title=dict(
                text=f"팀내 홈런 기여도<br><sub>Total: {player_hr + team_hr}</sub>",
                x=0.5,  # 중앙 정렬
                font=dict(size=16, color='black')
            ),
            legend=dict(font=dict(size=14)),
            margin=dict(t=50, b=0, l=0, r=0),
            height=250
        )

        st.plotly_chart(
            fig,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
            use_container_width=True,
            theme="streamlit"
        )
        
    with col4:
        player_bb_so = nc_bat.loc[nc_bat['batter_name'] == nc_player][['BB', 'SO']]
        player_bb_so = player_bb_so.rename(columns={'BB': '볼넷', 'SO': '삼진'})
        bbk = np.where(player_bb_so['삼진'] == 0,
                    player_bb_so['볼넷'],
                    round(player_bb_so['볼넷'] / player_bb_so['삼진'], 3))[0]

        if (player_bb_so['볼넷'] + player_bb_so['삼진']).values[0] != 0:
            player_bb_so = player_bb_so.T.reset_index()
            player_bb_so.columns = ['Category', 'Count']
            player_bb_so['Category'] = pd.Categorical(
                player_bb_so['Category'],
                categories=['볼넷', '삼진'],
                ordered=True
            )

            fig = go.Figure(
                data=go.Pie(
                    labels=player_bb_so['Category'],
                    values=player_bb_so['Count'],
                    hole=0.5,
                    marker=dict(colors=nc_colors),
                    sort=False,
                    hovertemplate=(
                        f"<b>선수명: {nc_player}</b><br>"
                        f"<b>연도: {year}</b><br>"
                        "<b>%{label}: %{value}</b>"
                    ),
                    textfont=dict(size=14, color='black')
                )
            )

            fig.update_layout(
                title=dict(
                    text=f"삼진 대비 볼넷 비율<br><sub>BB/K: {bbk}</sub>",
                    x=0.5,
                    font=dict(size=16, color='black')
                ),
                legend=dict(font=dict(size=14)),
                margin=dict(t=50, b=0, l=0, r=0),
                height=250
            )

            st.plotly_chart(
                fig,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
                use_container_width=True,
                theme="streamlit"
            )


        # 해당 연도에 데이터가 모두 0인 경우
        else:
            empty = pd.DataFrame({'Category': ['볼넷', '삼진'], 'Count': [1, 1]})

            fig = go.Figure(
                data=go.Pie(
                    labels=empty['Category'],
                    values=empty['Count'],
                    hole=0.5,
                    marker=dict(colors=nc_colors),
                    sort=False,
                    hovertemplate=(
                        f"<b>선수명: {nc_player}</b><br>"
                        f"<b>연도: {year}</b><br>"
                        "<b>%{label}: 0</b>"
                    ),
                    textfont=dict(size=14, color='black')
                )
            )

            fig.update_layout(
                title=dict(
                    text=f"삼진 대비 볼넷 비율<br><sub>BB/K: {bbk}</sub>",
                    x=0.5,
                    font=dict(size=16, color='black')
                ),
                legend=dict(font=dict(size=14)),
                margin=dict(t=50, b=0, l=0, r=0),
                height=250
            )

            st.plotly_chart(
                fig,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
                use_container_width=True,
                theme="streamlit"
            )

    # 선택된 선수의 연도별 OPS 차트
    with col5:
        team_avg_ops = bat_df.loc[bat_df['team']=='NC'].groupby('year')['OPS'].mean().reset_index()
        player_ops = bat_df.loc[(bat_df['team']=='NC')&(bat_df['batter_name']==nc_player)]
    
        fig = go.Figure(data=[go.Bar(x=team_avg_ops['year'],
                                     y=team_avg_ops['OPS'],
                                     name='팀 평균 OPS',
                                     marker=dict(color=nc_colors[1])),
                              go.Scatter(x=player_ops['year'],
                                         y=player_ops['OPS'],
                                         name=f'{nc_player} OPS',
                                         mode='lines+markers',
                                         marker=dict(color=nc_colors[0]))])
        fig.update_layout(title=f'연도별 팀 평균 대비 타자 OPS',
                          legend = dict(font = dict(size = 14)),
                          margin = dict(t = 50, b = 0, l = 0, r = 0),
                          yaxis_title='OPS',
                          height = 260)
        st.plotly_chart(
            fig,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
            use_container_width=True,
            theme="streamlit"
        )        
else:
    st.markdown('NC Dinos는 **2013년**에 창단했습니다.')

# League section
st.subheader('KBO League')

tab_stat, tab_rank = st.tabs(['지표', '순위'])

## 지표 tab
with tab_stat:
    # 선택 위젯 레이아웃 설정
    _, s_col1, _, s_col2 = st.columns((3.8, 1.2, 4, 1), gap = 'large')
    
    stat_lst = list(koreanize_dict.keys())
    stat_kor = s_col1.selectbox(f'**{year}년 구단별 평균 타격 지표**', stat_lst, stat_lst.index('OPS'), label_visibility = 'collapsed')
    
    positions = ['내야수','외야수','포수']
    selected_positions = s_col2.selectbox('포지션', positions, label_visibility = 'collapsed')
    
    col1, col2 = st.columns(2, gap = 'large')

    # 선택된 연도의 구단별 평균 타격 지표 차트
    with col1:
        bat_columns = ['year', 'team', 'avg', 'R', 'H', 'HR', 'TB', 'RBI', 'SB', 'CS', 'BB', 'HBP', 'SO', 'GDP', 'SLG', 'OBP', 'OPS']
        temp_bat = bat_df.copy()
        temp_bat = bat_df.loc[bat_df['year']==year, :]
        group_df = temp_bat.groupby(['team', 'year'])
        agg_df = group_df.agg({'R': 'sum', 'H': 'sum', 'HR': 'sum', 'TB': 'sum', 'RBI': 'sum', 'SB': 'sum', 'CS': 'sum', 'BB': 'sum', 'HBP': 'sum', 'SO': 'sum', 'GDP': 'sum',
            'avg': 'mean', 'SLG': 'mean', 'OBP': 'mean', 'OPS': 'mean'}).reset_index()
        agg_df = agg_df.merge(team_df.loc[:, '연도':'승률'], left_on = ['year', 'team'], right_on = ['연도', '팀명']).drop(columns = ['연도', '팀명'])
        agg_df = stats_by_g(agg_df, ['R', 'RBI', 'H', 'HR', 'TB', 'SB', 'CS', 'BB', 'SO', 'GDP'])
        agg_df = agg_df.drop(['year', '경기', '승', '패', '무'], axis=1)
        agg_df = agg_df.groupby(['team']).mean().sort_values(by='순위')
        agg_df = rank_scaling(agg_df)
        stat = koreanize_dict[stat_kor]
            
        min_xaxis = np.floor(agg_df[stat].min() * 0.8)
        max_xaxis = np.ceil(agg_df[stat].max() * 100) / 100
        xtick = round((max_xaxis - min_xaxis) / 5)
        
        if agg_df[stat].min() < 1:
            min_xaxis = np.floor(agg_df[stat].min() * 0.8 * 100) / 100
            max_xaxis = np.ceil(agg_df[stat].max() * 100) / 100
            xtick = round((max_xaxis - min_xaxis) / 5 * 100) / 100
        
        fig = go.Figure(data=go.Bar(x = agg_df.index, y = agg_df[stat], name=f'평균 {stat}',
                                    marker = dict(color = [team_colors.get(team) for team in agg_df.index])))
        fig.update_layout(
            yaxis = dict(title=stat_kor, range=[min_xaxis, max_xaxis], dtick=xtick),
            margin = dict(t=50, l=0, r=0),
            title = f'{year}년 구단별 평균 타격 지표',
            height = 450)
        st.plotly_chart(
            fig,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
            use_container_width=True,
            theme="streamlit"
        )    
    # 선택된 연도의 구단별 포지션별 OPS
    with col2:
        temp_bat = bat_df.loc[bat_df['year'] == year, :]
        try:
            pos_df = temp_bat[temp_bat['position'].str.contains(selected_positions)==True]
            pos_df['team'] = pd.Categorical(pos_df['team'], categories = agg_df.index, ordered = True)
            pos_df = pos_df.sort_values('team')
    
            fig = px.box(pos_df, x='team', y='OPS')
            fig.update_traces(marker=dict(color=team_colors['NC']))
            fig.update_layout(xaxis_title=None,
                              height=450,
                              margin=dict(t=50, l=0, r=0),
                              title=f'구단별 {selected_positions} OPS Boxplots',)
            st.plotly_chart(
                fig,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
                use_container_width=True,
                theme="streamlit"
            )
        except:
            fig, ax = plt.subplots()
            st.plotly_chart(fig)

## 순위 tab
with tab_rank:
    
    # 선택 위젯 레이아웃 설정
    s_col1, _, s_col2 = st.columns((3, 1.9, 5.1), gap = 'large')
    
    s_col1.write(f'**{year} KBO 정규리그 구단 순위**')
    with s_col2:
        selected_team = st.multiselect(label = "**구단을 선택하세요**",
                                       options = team_df['팀명'].unique(),
                                       default = 'NC',
                                       label_visibility = 'collapsed')
        
    # 차트 레이아웃 설정
    col1, col2 = st.columns(2, gap = 'large')
    
    with col1:
        # 연도별 순위 테이블 출력
        team_tmp = team_df.copy()
        team_tmp = team_tmp.loc[team_tmp['연도'] == year, '순위':'방문']
        st.dataframe(team_tmp,
                     hide_index = True,
                     height = 387,
                     width='stretch')
    
    with col2:
        # 연도별 팀 순위 라인차트
        team_tmp = team_df.copy()
        fig = go.Figure()

        for team in team_tmp['팀명'].unique():
            team_data = team_tmp[team_tmp['팀명'] == team]
            if team in selected_team:
                fig.add_trace(go.Scatter(x = team_data['연도'], y = team_data['순위'], name = team,
                                         line = dict(color = team_colors[team]),
                                         marker = dict(size = 4),
                                         customdata = team_data.loc[:, ['승', '무', '패', '팀명', '승률']],
                                         hovertemplate = "<b>팀명: %{customdata[3]}</b><br><b>연도: %{x}</b><br><b>순위: %{y}</b><br><b>%{customdata[0]}승 %{customdata[1]}무 %{customdata[2]}패</b><br><b>승률: %{customdata[4]}</b>"))
            else:
                fig.add_trace(go.Scatter(x = team_data['연도'], y = team_data['순위'], name = team,
                                         line = dict(color = 'rgba(192, 192, 192, 0.5)'),
                                         marker = dict(size = 4),
                                         customdata = team_data.loc[:, ['승', '무', '패', '팀명', '승률']],
                                         hovertemplate = "<b>팀명: %{customdata[3]}</b><br><b>연도: %{x}</b><br><b>순위: %{y}</b><br><b>%{customdata[0]}승 %{customdata[1]}무 %{customdata[2]}패</b><br><b>승률: %{customdata[4]}</b>"))
        fig.update_layout(
            title = 'KBO 구단 연도별 순위',
            yaxis_title='순위',
            yaxis = dict(range=[10.5, 0.5]),
            margin = dict(l = 0, r = 0, t = 50, b = 10),
            height = 387)
        st.plotly_chart(
            fig,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
            use_container_width=True,
            theme="streamlit"
        )