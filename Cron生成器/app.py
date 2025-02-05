import streamlit as st
from croniter import croniter
from datetime import datetime
import pytz


# 配置时间单位参数
CRON_UNITS = [
    {'name': '秒', 'key': 'second', 'min': 0, 'max': 59, 'default': 0},
    {'name': '分', 'key': 'minute', 'min': 0, 'max': 59, 'default': 0},
    {'name': '时', 'key': 'hour', 'min': 0, 'max': 23, 'default': 0},
    {'name': '日', 'key': 'day', 'min': 1, 'max': 31, 'default': 1},
    {'name': '月', 'key': 'month', 'min': 1, 'max': 12, 'default': 1},
    {'name': '周', 'key': 'week', 'min': 0, 'max': 6, 'default': 0,
     'symbols': ['日', '一', '二', '三', '四', '五', '六']},
    {'name': '年', 'key': 'year', 'min': 2024, 'max': 2100, 'default': '*'}
]

def generate_cron_part(unit, params):
    """生成单个时间单位的cron表达式部分"""
    mode = params['mode']

    if mode == 'each':
        return '*' if unit['key'] != 'week' else '?'

    elif mode == 'range':
        start = params.get('start', unit['min'])
        end = params.get('end', unit['max'])
        return f'{start}-{end}'

    elif mode == 'step':
        interval = params.get('interval', 1)
        return f'*/{interval}'

    elif mode == 'specific':
        values = ','.join(map(str, params.get('values', [])))
        return values if values else '*'

    return '*'

def parse_cron_expression(expression):
    """解析Cron表达式到各个参数"""
    parts = expression.strip().split()
    if len(parts) != 7:
        raise ValueError("无效的Cron表达式")

    params = {}
    for i, unit in enumerate(CRON_UNITS):
        part = parts[i]
        if part == '*':
            params[unit['key']] = {'mode': 'each'}
        elif '-' in part:
            start, end = part.split('-')
            params[unit['key']] = {'mode': 'range', 'start': start, 'end': end}
        elif part.startswith('*/'):
            interval = part[2:]
            params[unit['key']] = {'mode': 'step', 'interval': interval}
        elif ',' in part:
            values = part.split(',')
            params[unit['key']] = {'mode': 'specific', 'values': values}
        else:
            params[unit['key']] = {'mode': 'specific', 'values': [part]}

    return params

def get_next_execution_times(cron_exp, count=5):
    try:
        cron = croniter(
            cron_exp,
            start_time=datetime.now(pytz.utc),
            cron_format='with_seconds' if cron_exp.count(' ') == 6 else 'default'
        )
        return [cron.get_next(datetime).strftime('%Y-%m-%d %H:%M:%S') 
               for _ in range(count)]
    except Exception as e:
        st.error(f"错误: {str(e)}")
        return []

def main():
    st.set_page_config(page_title="Cron表达式生成器", layout="wide")
    st.title("🕒 Cron表达式生成器")

    if 'params' not in st.session_state:
        st.session_state.params = {unit['key']: {'mode': 'each'} for unit in CRON_UNITS}

    # 创建布局
    col_size = [1, 1, 1, 1.5, 1.5, 1.5, 1]
    cols = st.columns(col_size)

    # 生成时间单位控件
    for i, unit in enumerate(CRON_UNITS):
        with cols[i]:
            st.subheader(unit['name'])

            # 模式选择
            mode = st.radio(
                f"{unit['name']}模式",
                ['每个', '范围', '间隔', '指定值'],
                key=f"{unit['key']}_mode",
                index=['each', 'range', 'step', 'specific'].index(
                    st.session_state.params[unit['key']]['mode'])
            )

            # 根据模式显示不同控件
            if mode == '范围':
                c1, c2 = st.columns(2)
                with c1:
                    start = st.number_input(
                        '开始', 
                        min_value=unit['min'],
                        max_value=unit['max'],
                        value=int(st.session_state.params[unit['key']].get('start', unit['min'])),
                        key=f"{unit['key']}_start"
                    )
                with c2:
                    end = st.number_input(
                        '结束',
                        min_value=start,
                        max_value=unit['max'],
                        value=int(st.session_state.params[unit['key']].get('end', unit['max'])),
                        key=f"{unit['key']}_end"
                    )
                st.session_state.params[unit['key']] = {'mode': 'range', 'start': start, 'end': end}

            elif mode == '间隔':
                interval = st.number_input(
                    '间隔值',
                    min_value=1,
                    max_value=unit['max'],
                    value=int(st.session_state.params[unit['key']].get('interval', 1)),
                    key=f"{unit['key']}_interval"
                )
                st.session_state.params[unit['key']] = {'mode': 'step', 'interval': interval}

            elif mode == '指定值':
                values = st.multiselect(
                    '选择值',
                    options=range(unit['min'], unit['max']+1),
                    default=[int(x) for x in st.session_state.params[unit['key']].get('values', [])],
                    key=f"{unit['key']}_values"
                )
                st.session_state.params[unit['key']] = {'mode': 'specific', 'values': values}

            else:
                st.session_state.params[unit['key']] = {'mode': 'each'}

    # 生成Cron表达式
    cron_parts = []
    for unit in CRON_UNITS:
        part = generate_cron_part(unit, st.session_state.params[unit['key']])
        cron_parts.append(part)
    cron_expression = ' '.join(cron_parts)

    # 手动输入解析
    with st.expander("高级选项"):
        manual_exp = st.text_input("或直接输入Cron表达式：", cron_expression)
        if manual_exp != cron_expression:
            try:
                parsed_params = parse_cron_expression(manual_exp)
                for unit in CRON_UNITS:
                    st.session_state.params[unit['key']] = parsed_params[unit['key']]
            except Exception as e:
                st.error(f"错误：{str(e)}")

    # 显示结果
    st.markdown(f"**生成的Cron表达式：** `{cron_expression}`")

    # 计算下次执行时间
    if st.button('计算下次执行时间'):
        try:
            next_times = get_next_execution_times(cron_expression)
            if next_times:
                st.markdown("**下次执行时间：**")
                for time in next_times:
                    st.write(f"- {time}")
            else:
                st.warning("无法计算执行时间")
        except Exception as e:
            st.error(f"错误：{str(e)}")

if __name__ == "__main__":
    st.write(croniter.__version__)  
    main()
