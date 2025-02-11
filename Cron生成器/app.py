import streamlit as st
from croniter import croniter
from datetime import datetime
import pytz

# 时间单位配置
TIME_UNITS = [
    {'name': '秒', 'key': 'second', 'min': 0, 'max': 59, 'default': 0},
    {'name': '分', 'key': 'minute', 'min': 0, 'max': 59, 'default': 0},
    {'name': '时', 'key': 'hour', 'min': 0, 'max': 23, 'default': 0},
    {'name': '日', 'key': 'day', 'min': 1, 'max': 31, 'default': 1},
    {'name': '月', 'key': 'month', 'min': 1, 'max': 12, 'default': 1},
    {'name': '周', 'key': 'week', 'min': 0, 'max': 6, 'default': 0,
     'symbols': ['日', '一', '二', '三', '四', '五', '六']},
]

# 生成单个时间单位的Cron表达式部分
def generate_cron_part(unit, params):
    if params['mode'] == '每个':
        return '*' if unit['key'] != 'week' else '?'
    elif params['mode'] == '范围':
        return f"{params['start']}-{params['end']}"
    elif params['mode'] == '间隔':
        return f"*/{params['interval']}"
    elif params['mode'] == '指定值':
        return ','.join(map(str, params['values']))
    else:
        return '*'

# 解析Cron表达式为参数
def parse_cron_expression(cron_expr):
    parts = cron_expr.strip().split()
    if len(parts) != len(TIME_UNITS):
        raise ValueError(f"无效的Cron表达式，应包含 {len(TIME_UNITS)} 个字段")
    
    params = {}
    for i, unit in enumerate(TIME_UNITS):
        part = parts[i].strip()
        current_params = {'mode': '每个'}
        if part == '*':
            current_params['mode'] = '每个'
        elif '-' in part:
            start, end = map(int, part.split('-'))
            current_params['mode'] = '范围'
            current_params['start'] = start
            current_params['end'] = end
        elif part.startswith('*/'):
            interval = int(part[2:])
            current_params['mode'] = '间隔'
            current_params['interval'] = interval
        elif ',' in part:
            current_params['mode'] = '指定值'
            current_params['values'] = list(map(int, part.split(',')))
        else:
            current_params['mode'] = '指定值'
            current_params['values'] = [int(part)]
        params[unit['key']] = current_params
    return params

# 获取下次执行时间
def get_next_execution_times(cron_expr, count=5):
    tz = pytz.timezone('Asia/Shanghai')
    start_time = datetime.now(tz)
    cron = croniter(cron_expr, start_time)
    return [cron.get_next(datetime).astimezone(tz).strftime('%Y-%m-%d %H:%M:%S') 
           for _ in range(count)]

# 主程序
def main():
    st.set_page_config(page_title="Cron表达式生成器", layout="wide")
    st.title("-writing cron 表达式生成器_Refactoring)")

    # 初始化参数
    if 'params' not in st.session_state:
        st.session_state.params = {
            unit['key']: {
                'mode': '每个',
                'values': [unit['default']] if unit['key'] == '秒' else []
            } for unit in TIME_UNITS
        }

    # 创建布局
    col_size = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
    cols = st.columns(len(col_size))

    # 生成控件
    for i, unit in enumerate(TIME_UNITS):
        with cols[i]:
            st.subheader(unit['name'])

            # 获取当前参数
            current = st.session_state.params[unit['key']]

            # 选择模式
            mode = st.radio(
                f"**选择模式**",
                ['每个', '范围', '间隔', '指定值'],
                index=['每个', '范围', '间隔', '指定值'].index(current['mode']),
                key=f"{unit['key']}_mode"
            )

            if mode == '范围':
                min_val = unit['min']
                max_val = unit['max']
                start = st.number_input(
                    '起始值',
                    min_value=min_val,
                    max_value=max_val,
                    value=current.get('start', min_val),
                    key=f"{unit['key']}_start"
                )
                end = st.number_input(
                    '结束值',
                    min_value=start,
                    max_value=max_val,
                    value=current.get('end', max_val),
                    key=f"{unit['key']}_end"
                )
                st.session_state.params[unit['key']] = {
                    'mode': mode,
                    'start': start,
                    'end': end
                }

            elif mode == '间隔':
                interval = st.number_input(
                    '间隔值',
                    min_value=1,
                    max_value=unit['max'],
                    value=current.get('interval', 1),
                    key=f"{unit['key']}_interval"
                )
                st.session_state.params[unit['key']] = {
                    'mode': mode,
                    'interval': interval
                }

            elif mode == '指定值':
                values = st.multiselect(
                    '选择值',
                    options=range(unit['min'], unit['max']+1),
                    default=current.get('values', []),
                    key=f"{unit['key']}_values"
                )
                st.session_state.params[unit['key']] = {
                    'mode': mode,
                    'values': values
                }

            else:
                st.session_state.params[unit['key']] = {
                    'mode': mode
                }

    # 生成Cron表达式
    cron_parts = []
    for unit in TIME_UNITS:
        part = generate_cron_part(unit, st.session_state.params[unit['key']])
        cron_parts.append(part)
    cron_expression = ' '.join(cron_parts)

    # 显示生成的Cron表达式
    st.markdown(f"## **生成的Cron表达式**")
    st.code(cron_expression, language="cron")

    # 手动输入Cron表达式
    with st.expander("高级功能: 直接输入Cron表达式"):
        manual_input = st.text_input(
            "输入Cron表达式",
            value=cron_expression,
            key="manual_input"
        )
        if manual_input and manual_input != cron_expression:
            try:
                parsed_params = parse_cron_expression(manual_input)
                for unit in TIME_UNITS:
                    st.session_state.params[unit['key']] = parsed_params[unit['key']]
                st.experimental_rerun()
            except Exception as e:
                st.error(f"解析错误：{e}")

    # 计算下次执行时间
    st.markdown("## **预测执行时间**")
    if st.button("计算下次执行时间"):
        try:
            next_times = get_next_execution_times(cron_expression)
            for idx, time in enumerate(next_times, 1):
                st.write(f"{idx}. {time}")
        except Exception as e:
            st.warning(f"无法预测执行时间：{e}")

if __name__ == "__main__":
    main()
