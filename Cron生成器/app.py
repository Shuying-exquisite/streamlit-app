import streamlit as st
from croniter import croniter
from datetime import datetime
import pytz

# 配置时间单位参数（移除年字段）
CRON_UNITS = [
    {'name': '秒', 'key': 'second', 'min': 0, 'max': 59, 'default': 0},
    {'name': '分', 'key': 'minute', 'min': 0, 'max': 59, 'default': 0},
    {'name': '时', 'key': 'hour', 'min': 0, 'max': 23, 'default': 0},
    {'name': '日', 'key': 'day', 'min': 1, 'max': 31, 'default': 1},
    {'name': '月', 'key': 'month', 'min': 1, 'max': 12, 'default': 1},
    {'name': '周', 'key': 'week', 'min': 0, 'max': 6, 'default': 0,
     'symbols': ['日', '一', '二', '三', '四', '五', '六']},
]

def generate_cron_part(unit, params):
    """生成单个时间单位的cron表达式部分"""
    mode = params.get('mode', 'each')

    if mode == 'each':
        if unit['key'] == 'week':
            return '?'
        else:
            return '*'

    elif mode == 'range':
        start = params.get('start', unit['min'])
        end = params.get('end', unit['max'])
        return f'{start}-{end}'

    elif mode == 'step':
        interval = params.get('interval', 1)
        return f'*/{interval}'

    elif mode == 'specific':
        values = params.get('values', [])
        if isinstance(values, list):
            return ','.join(map(str, values))
        else:
            return str(values)

    return '*'
    
def parse_cron_expression(expression):
    """解析Cron表达式到各个参数"""
    parts = expression.strip().split()
    len_cron_units = len(CRON_UNITS)
    
    if len(parts) != len_cron_units:
        raise ValueError(f"Cron表达式格式错误，必须为 {len_cron_units} 个字段")
    
    params = {}
    for i, unit in enumerate(CRON_UNITS):
        part = parts[i].strip()
        current_params = params.setdefault(unit['key'], {})
        
        if part == '*':
            current_params['mode'] = 'each'
        elif part == '?':
            if unit['key'] not in ['day', 'week']:
                raise ValueError(f"问号只能用在 '日' 或 '周' 字段，但出现在 {unit['name']} 字段")
            current_params['mode'] = 'each'
        elif '-' in part:
            try:
                start, end = map(int, part.split('-'))
                current_params['mode'] = 'range'
                current_params['start'] = start
                current_params['end'] = end
            except ValueError:
                raise ValueError(f"无效的范围值: {part}")
        elif part.startswith('*/'):
            try:
                interval = int(part[2:])
                current_params['mode'] = 'step'
                current_params['interval'] = interval
            except ValueError:
                raise ValueError(f"无效的间隔值: {part}")
        elif ',' in part:
            try:
                values = list(map(int, part.split(',')))
                current_params['mode'] = 'specific'
                current_params['values'] = values
            except ValueError:
                raise ValueError(f"无效的指定值: {part}")
        else:
            try:
                value = int(part)
                current_params['mode'] = 'specific'
                current_params['values'] = [value]
            except ValueError:
                raise ValueError(f"无效的指定值: {part}")
    
    # 检查 "日" 和 "周" 字段是否同时有值
    day_params = params.get('day', {})
    week_params = params.get('week', {})
    
    if (day_params.get('mode') not in ['each', 'none']) and (week_params.get('mode') not in ['each', 'none']):
        raise ValueError("不能同时指定 '日' 和 '周' 字段")
    
    return params

def get_next_execution_times(cron_exp, count=5):
    """获取下次执行时间"""
    try:
        tz = pytz.timezone('Asia/Shanghai')
        start_time = datetime.now(tz)
        cron = croniter(cron_exp, start_time)
        return [cron.get_next(datetime).astimezone(tz).strftime('%Y-%m-%d %H:%M:%S') 
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
    col_size = [1, 1, 1, 1, 1, 1, 1, 1]  # 自适应列宽
    cols = st.columns(len(CRON_UNITS))

    # 生成时间单位控件
    for i, unit in enumerate(CRON_UNITS):
        with cols[i]:
            st.subheader(unit['name'])
            current_mode = st.session_state.params[unit['key']].get('mode', 'each')
            mode = st.radio(
                f"{unit['name']}模式",
                ['每个', '范围', '间隔', '指定值'],
                index=['each', 'range', 'step', 'specific'].index(current_mode),
                key=f"{unit['key']}_mode"
            )

            if mode == '范围':
                min_val = unit['min']
                max_val = unit['max']
                prev_start = st.session_state.params[unit['key']].get('start', min_val)
                prev_end = st.session_state.params[unit['key']].get('end', max_val) if prev_start <= max_val else max_val
                start = st.number_input(
                    '开始',
                    min_value=min_val,
                    max_value=max_val,
                    value=prev_start,
                    key=f"start_{unit['key']}"
                )
                end = st.number_input(
                    '结束',
                    min_value=start,
                    max_value=max_val,
                    value=prev_end,
                    key=f"end_{unit['key']}"
                )
                st.session_state.params[unit['key']] = {'mode': 'range', 'start': start, 'end': end}

            elif mode == '间隔':
                interval = st.number_input(
                    '间隔',
                    min_value=1,
                    max_value=unit['max'],
                    value=st.session_state.params[unit['key']].get('interval', 1),
                    key=f"interval_{unit['key']}"
                )
                st.session_state.params[unit['key']] = {'mode': 'step', 'interval': interval}

            elif mode == '指定值':
                options = list(range(unit['min'], unit['max'] + 1))
                prev_values = st.session_state.params[unit['key']].get('values', [])
                values = st.multiselect(
                    '选择值',
                    options=options,
                    default=prev_values,
                    key=f"values_{unit['key']}"
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

    # 显示生成的Cron表达式
    st.markdown(f"**生成的Cron表达式：** `{cron_expression}`")

    # 手动输入解析
    with st.expander("高级选项"):
        manual_exp = st.text_input("或直接输入Cron表达式：", value=cron_expression)
        if manual_exp != cron_expression:
            try:
                parsed_params = parse_cron_expression(manual_exp)
                for unit in CRON_UNITS:
                    st.session_state.params[unit['key']] = parsed_params.get(unit['key'], {'mode': 'each'})
                cron_expression = ' '.join([generate_cron_part(u, st.session_state.params[u['key']]) for u in CRON_UNITS])
                st.experimental_rerun()
            except Exception as e:
                st.error(f"解析错误：{str(e)}")

    # 计算下次执行时间
    if st.button('计算下次执行时间'):
        try:
            next_times = get_next_execution_times(cron_expression)
            if next_times:
                st.markdown("**下次执行时间：**")
                for time in next_times:
                    st.write(f"- {time}")
            else:
                st.warning("无法计算执行时间，可能是Cron表达式语法错误或时间逻辑冲突。")
        except Exception as e:
            st.error(f"计算失败: {str(e)}")

if __name__ == "__main__":
    main()
