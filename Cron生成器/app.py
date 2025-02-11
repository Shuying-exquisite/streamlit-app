import streamlit as st
from cron_parser import CronParser  # 使用第三方库 cron-parser

# 定义一个函数来生成 Cron 表达式（去掉年份部分）
def generate_cron_expression(
    second="*",
    minute="*",
    hour="*",
    day_of_month="*",
    month="*",
    day_of_week="*"
):
    cron_expression = f"{second} {minute} {hour} {day_of_month} {month} {day_of_week}"
    return cron_expression

# 定义一个函数来解析 Cron 表达式
def parse_cron_expression(cron_expression):
    try:
        parser = CronParser(cron_expression)
        description = parser.to_description()
        return description
    except Exception as e:
        return f"解析失败: {e}"

# Streamlit 应用程序
def main():
    st.title("Cron 表达式生成与解析工具 V2（去掉年份）")
    st.markdown("---")

    # 侧边栏选择功能
    st.sidebar.title("功能选择")
    option = st.sidebar.radio("选择功能", ["生成 Cron 表达式", "解析 Cron 表达式"])

    if option == "生成 Cron 表达式":
        st.subheader("生成 Cron 表达式")
        col1, col2 = st.columns(2)

        with col1:
            # 分钟
            minute_options = ["*", "每隔 10 分钟", "每隔 30 分钟", "自定义"]
            minute_choice = st.selectbox("分钟", minute_options, index=0)
            if minute_choice == "自定义":
                minute = st.text_input("自定义分钟 (0-59)", "0")
            else:
                if minute_choice == "每隔 10 分钟":
                    minute = "*/10"
                elif minute_choice == "每隔 30 分钟":
                    minute = "*/30"
                else:
                    minute = "*"

            # 小时
            hour_options = ["*", "每隔 1 小时", "每隔 12 小时", "自定义"]
            hour_choice = st.selectbox("小时", hour_options, index=0)
            if hour_choice == "自定义":
                hour = st.text_input("自定义小时 (0-23)", "0")
            else:
                if hour_choice == "每隔 1 小时":
                    hour = "*/1"
                elif hour_choice == "每隔 12 小时":
                    hour = "0 12"
                else:
                    hour = "*"

            # 日期
            date_options = ["*", "每天", "每月 1 号和 15 号", "自定义"]
            date_choice = st.selectbox("日期", date_options, index=0)
            if date_choice == "自定义":
                date = st.text_input("自定义日期 (1-31)", "1")
            else:
                if date_choice == "每月 1 号和 15 号":
                    date = "1,15"
                else:
                    date = "*"

        with col2:
            # 月份
            month_options = ["*", "每年", "每年 1 月和 6 月", "自定义"]
            month_choice = st.selectbox("月份", month_options, index=0)
            if month_choice == "自定义":
                month = st.text_input("自定义月份 (1-12)", "1")
            else:
                if month_choice == "每年 1 月和 6 月":
                    month = "1,6"
                else:
                    month = "*"

            # 星期
            week_options = ["*", "每周一至周五", "每周日", "自定义"]
            week_choice = st.selectbox("星期", week_options, index=0)
            if week_choice == "自定义":
                week = st.text_input("自定义星期 (0-6, 0=周日)", "0")
            else:
                if week_choice == "每周一至周五":
                    week = "1-5"
                elif week_choice == "每周日":
                    week = "0"
                else:
                    week = "*"

        if st.button("生成 Cron 表达式"):
            cron_expr = generate_cron_expression(
                minute=minute,
                hour=hour,
                day_of_month=date,
                month=month,
                day_of_week=week
            )
            st.subheader("生成的 Cron 表达式:")
            st.code(cron_expr)
            st.subheader("Cron 表达式含义:")
            st.markdown(parse_cron_expression(cron_expr))

    elif option == "解析 Cron 表达式":
        st.subheader("解析 Cron 表达式")
        cron_expression = st.text_input("请输入 Cron 表达式 (例如: 0 0 2 * * *)", "0 0 2 * * *")
        if st.button("解析 Cron 表达式"):
            description = parse_cron_expression(cron_expression)
            st.subheader("解析结果:")
            st.write(description)

    st.markdown("---")
    st.markdown("提示: 你可以通过 [Cron 表达式指南](https://crontab.guru/) 了解更多 Cron 表达式的用法和规则。"[^1^])

if __name__ == "__main__":
    main()
