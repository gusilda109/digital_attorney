import streamlit as st
from datetime import date
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

LOGO_PATH = APP_DIR / "logo_lawyer.png"

st.set_page_config(page_title="Цифровой правозащитник", page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else None)

if LOGO_PATH.exists():
    st.image(str(LOGO_PATH))
else:
    st.warning(f"Логотип не найден: {LOGO_PATH}. Поместите файл сюда или поменяйте путь.")

st.header("Анкета дела — общие данные")


courts = [
    {"id": 1, "name": "Мировой судья участка №1, г. Москва", "address": "ул. Примерная, 1"},
    {"id": 2, "name": "Районный суд Центрального района, г. Самара", "address": "пр. Судебный, 10"},
    {"id": 3, "name": "Ленинский районный суд, г. Казань", "address": "ул. Правовая, 5"},
]
court_labels = [c["name"] for c in courts]

with st.form("case_form"):
    st.subheader("Данные истца")
    fio = st.text_input("ФИО истца *", placeholder="Иванов Иван Иванович", key="fio")
    col1, col2, col3 = st.columns(3)
    with col1:
        region = st.text_input("Регион истца *", placeholder="Московская область", key="region")
    with col2:
        city = st.text_input("Город истца *", placeholder="Москва", key="city")
    with col3:
        address = st.text_input("Адрес истца *", placeholder="ул. Пушкина, д. 10, кв. 5", key="address")

    colc1, colc2 = st.columns(2)
    with colc1:
        email = st.text_input("Email (опц.)", placeholder="name@example.com", key="email")
    with colc2:
        phone = st.text_input("Телефон (опц.)", placeholder="+7 900 000-00-00", key="phone")

    st.subheader("Суд")
    court_idx = st.selectbox("Суд *", options=range(len(court_labels)), format_func=lambda i: court_labels[i], key="court_idx")
    override = st.checkbox("Переопределить название/адрес суда вручную?")
    court_name_override = ""
    court_address_override = ""
    if override:
        court_name_override = st.text_input("Название суда (ручной ввод)", key="court_name_override")
        court_address_override = st.text_input("Адрес суда (ручной ввод)", key="court_address_override")

    st.subheader("Ответчик")
    opponent_name = st.text_input("Ответчик: наименование *", key="opponent_name", placeholder="ООО «Ромашка» / Петров П.П.")
    opponent_address = st.text_input("Ответчик: адрес (желательно)", key="opponent_address", placeholder="г. Москва, ...")

    st.subheader("Детали спора")
    amount = st.number_input("Сумма требований (руб.) *", min_value=0, step=100, key="amount")
    event_date = st.date_input("Дата события *", value=date.today(), key="event_date")
    description = st.text_area(
        "Описание ситуации (3–6 предложений) *",
        height=150,
        placeholder="Кратко опишите, что произошло...",
        key="description",
    )

    st.subheader("Выбор категории спора")
    CATEGORY_LABELS = {
        "Возврат товара": "return_goods",
        "Компенсация услуг ЖКХ": "housing_utilities",
        "Мелкий вред здоровью": "minor_injury",
    }
    category_label = st.selectbox(
        "Категория спора *",
        ["— Выберите категорию —"] + list(CATEGORY_LABELS.keys()),
        key="category_label",
    )


    submitted = st.form_submit_button("Сохранить черновик")

    if submitted:
        errors = {}

        if not fio.strip():
            errors["fio"] = "Укажите ФИО истца."
        if not region.strip():
            errors["region"] = "Укажите регион истца."
        if not city.strip():
            errors["city"] = "Укажите город истца."
        if not address.strip():
            errors["address"] = "Укажите адрес истца."

        if court_idx is None or court_idx < 0 or court_idx >= len(courts):
            errors["court_idx"] = "Выберите суд из справочника."

        if not opponent_name.strip():
            errors["opponent_name"] = "Укажите наименование ответчика."

        if amount is None or amount <= 0:
            errors["amount"] = "Сумма требований должна быть больше 0."

        if event_date is None:
            errors["event_date"] = "Укажите дату события."
        elif event_date > date.today():
            errors["event_date"] = "Дата события не может быть в будущем."

        if not description.strip():
            errors["description"] = "Опишите ситуацию (минимум 1–2 предложения)."
        
        if category_label == "— Выберите категорию —":
            errors["category"] = "Выберите категорию спора."

        if errors:
            st.error("Пожалуйста, исправьте ошибки в форме.")

            if "category" in errors: st.caption(f"❌ {errors['category']}")
            if "fio" in errors: st.caption(f"❌ {errors['fio']}")
            if "region" in errors: st.caption(f"❌ {errors['region']}")
            if "city" in errors: st.caption(f"❌ {errors['city']}")
            if "address" in errors: st.caption(f"❌ {errors['address']}")
            if "court_idx" in errors: st.caption(f"❌ {errors['court_idx']}")
            if "opponent_name" in errors: st.caption(f"❌ {errors['opponent_name']}")
            if "amount" in errors: st.caption(f"❌ {errors['amount']}")
            if "event_date" in errors: st.caption(f"❌ {errors['event_date']}")
            if "description" in errors: st.caption(f"❌ {errors['description']}")
    
        else:
            
            

            st.success("Черновик анкеты валиден и готов к сохранению.")

